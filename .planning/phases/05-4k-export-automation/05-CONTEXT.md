# Phase 5: 4K Export Automation - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Complete the physical rendering loop by exporting image sequences and stitching them into broadcast-quality video. Setup a seamless automation layer that generates the final 4K MP4 file from the engine outputs.
</domain>

<decisions>
## Implementation Decisions

### Image Sequence Format
- **D-01:** Export raw frames in **both PNG (16-bit) and TIFF**. This provides both a lossless, easy-to-inspect standard format and an uncompressed highest-quality format for backup.

### Automation Strategy
- **D-02:** Use a **Python Wrapper Script** (`run_pipeline.py`) to orchestrate the pipeline. It will call Blender via `subprocess` and follow up with FFmpeg, keeping the logic scriptable and platform-independent without relying on shell commands directly.

### Output Video Specs
- **D-03:** The 4K MP4 output will be tailored for **60fps H.264**, providing a hyper-smooth cinematic experience and universal compatibility.

### Directory Structure
- **D-04:** Use a **separate `renders/` root directory** with subfolders for `frames/` and `output/` to keep the artifacts cleanly separated from the repository logic.
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Architecture
- `.planning/PROJECT.md` — Overall vision: offline pre-rendered 4K art, accuracy-first
- `.planning/REQUIREMENTS.md` — RNDR-03, RNDR-04: exporting rendered frames as high-bit-depth image sequences and compiling them into 4K MP4 via FFmpeg.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `renderer/render.py` — The existing Blender headless ingestion script.
- Python `subprocess` module to wrap external processes.

### Integration Points
- The output from `render.py` (image frames) will directly feed into FFmpeg inside the wrapper. 

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed completely within phase scope.
</deferred>

---

*Phase: 05-4k-export-automation*
*Context gathered: 2026-03-26*
