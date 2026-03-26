# Phase 5: 4K Export Automation - Research

**Researched:** 2026-03-27
**Status:** Complete

## RESEARCH COMPLETE

## 1. Current Codebase State

### Existing Pipeline
- `scripts/export_data.py` — Fetches JSON from engine API (`/api/v1/sequences/primes`, `/api/v1/sequences/fractal`), saves to `data/` directory
- `renderer/render.py` — Blender headless script: ingests JSON, creates icospheres at 3D coordinates, applies Cycles materials + sun lighting + camera tracking
- `data/primes.json` / `data/fractal.json` — Pre-exported 3D point cloud data

### Current Gaps (Phase 5 Must Address)
- `render.py` creates the 3D scene but **never renders frames** — no `bpy.ops.render.render()` call, no output settings
- No frame range / animation keyframes exist — scene is currently static
- No `renders/` output directory structure
- No FFmpeg integration anywhere

### Available Tools
- **Blender:** `/opt/homebrew/bin/blender` (Homebrew install)
- **FFmpeg:** `/opt/homebrew/bin/ffmpeg` v7.0.2

## 2. Blender Frame Export (RNDR-03)

### Render Output Configuration (bpy API)
```python
scene = bpy.context.scene
scene.render.resolution_x = 3840
scene.render.resolution_y = 2160
scene.render.resolution_percentage = 100

# PNG 16-bit
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_depth = '16'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.compression = 15  # 0-100, PNG compression level

# Frame range
scene.frame_start = 1
scene.frame_end = 300  # configurable
scene.render.filepath = "//renders/frames/frame_"
```

### TIFF Export (backup format per CONTEXT D-01)
```python
scene.render.image_settings.file_format = 'TIFF'
scene.render.image_settings.color_depth = '16'
scene.render.image_settings.tiff_codec = 'NONE'  # uncompressed
```

### Rendering Frames
```python
# Single frame
bpy.ops.render.render(write_still=True)

# Animation (all frames in range)
bpy.ops.render.render(animation=True)
```

### Animation / Camera Motion
For a static data visualization that needs multiple frames, the typical approaches:
1. **Camera orbit** — Keyframe camera location around centroid using circular path or manual keyframes
2. **Turntable** — Parent camera to empty, rotate empty over frame range
3. **Parametric** — Use Python driver to compute camera position per-frame

**Recommended:** Turntable orbit is simplest and produces visually compelling results for mathematical sculptures. Keyframe the empty's Z-rotation from 0° to 360° over the frame range.

### Cycles Performance for 4K
- GPU rendering via CUDA/OptiX/Metal dramatically faster than CPU
- Reasonable sample count for final: 128–256 samples with denoiser enabled
- `scene.cycles.use_denoising = True` with OpenImageDenoise 
- Expected per-frame render time: 5–30 seconds at 4K with GPU

## 3. FFmpeg 4K Encoding (RNDR-04)

### Recommended FFmpeg Command
```bash
ffmpeg -y \
  -framerate 60 \
  -i "renders/frames/frame_%04d.png" \
  -c:v libx264 \
  -preset slow \
  -crf 17 \
  -pix_fmt yuv420p \
  -vf "scale=3840:2160" \
  -movflags +faststart \
  "renders/output/mathematica_art.mp4"
```

### Parameter Rationale
| Parameter | Value | Reason |
|-----------|-------|--------|
| `-framerate 60` | 60fps | Per CONTEXT D-03: hyper-smooth cinematic |
| `-c:v libx264` | H.264 | Per CONTEXT D-03: universal compatibility |
| `-preset slow` | Quality-focused | Better compression ratio; acceptable for offline encode |
| `-crf 17` | Near-lossless | CRF 17–18 is "visually lossless" for H.264. Range 0–51, lower = better |
| `-pix_fmt yuv420p` | Standard pixel format | Required for broad player compatibility |
| `-movflags +faststart` | Web-optimized | Moves moov atom to start of file for streaming/web playback |

### Input Pattern
- FFmpeg reads sequential numbered frames: `frame_0001.png`, `frame_0002.png`, etc.
- Padding format: `%04d` for 4-digit zero-padded numbers
- Blender output naming must match this pattern exactly

## 4. Pipeline Orchestration (run_pipeline.py)

### Architecture per CONTEXT D-02
```
run_pipeline.py
├── Step 1: Export data from engine (optional, if not already exported)
├── Step 2: Run Blender headless render (subprocess)
│   └── blender --background --python renderer/render.py -- --input data/primes.json --frames 300
├── Step 3: Run FFmpeg encode (subprocess)
│   └── ffmpeg -framerate 60 -i renders/frames/frame_%04d.png ...
└── Step 4: Validate output
    └── Check MP4 exists, verify resolution/duration with ffprobe
```

### Subprocess Pattern
```python
import subprocess
import sys

result = subprocess.run(
    ["blender", "--background", "--python", "renderer/render.py",
     "--", "--input", "data/primes.json", "--frames", "300"],
    capture_output=True, text=True
)
if result.returncode != 0:
    print(f"Blender failed: {result.stderr}", file=sys.stderr)
    sys.exit(1)
```

### Output Validation with ffprobe
```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,duration \
  -of csv=p=0 renders/output/mathematica_art.mp4
# Expected: 3840,2160,60/1,5.000000
```

## 5. Directory Structure

Per CONTEXT D-04:
```
renders/
├── frames/          # Raw PNG/TIFF image sequences
│   ├── frame_0001.png
│   ├── frame_0001.tiff
│   └── ...
└── output/          # Final MP4 files
    └── mathematica_art.mp4
```

Add `renders/` to `.gitignore` — these are large binary artifacts.

## 6. Key Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Blender not found on PATH | Check `shutil.which("blender")` at pipeline start; clear error message |
| FFmpeg not found on PATH | Check `shutil.which("ffmpeg")` at pipeline start |
| GPU not available for Cycles | Fallback to CPU with reduced samples; warn user |
| Frame numbering mismatch | Use Blender's `####` pattern which matches FFmpeg's `%04d` |
| Large disk usage (4K PNGs) | ~25MB per 4K PNG × 300 frames = ~7.5GB. Warn user, add cleanup option |
| render.py currently has no animation | Must add camera keyframes and frame range before rendering |

## 7. Modifications Required to render.py

The current `render.py` needs these additions for Phase 5:
1. **Command-line args:** `--frames N`, `--output-dir PATH`, `--format png|tiff`
2. **Resolution setup:** Set 3840×2160
3. **Camera animation:** Add turntable orbit keyframes
4. **Render output path:** Set `scene.render.filepath`
5. **Execute render:** Call `bpy.ops.render.render(animation=True)`
6. **Cycles optimization:** Denoiser, sample count, GPU device selection

## Validation Architecture

### Automated Verification
1. **Frame count check:** `ls renders/frames/*.png | wc -l` matches expected frame count
2. **Frame resolution check:** `identify renders/frames/frame_0001.png` shows 3840×2160
3. **MP4 existence:** `test -f renders/output/mathematica_art.mp4`
4. **MP4 resolution/fps:** `ffprobe` output matches 3840×2160 @ 60fps
5. **MP4 duration:** Expected duration = frame_count / 60

### Manual Verification
- Visual inspection of rendered frames for quality
- Playback of final MP4 for smoothness

---
*Phase: 05-4k-export-automation*
*Research completed: 2026-03-27*
