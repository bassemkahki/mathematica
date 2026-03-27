---
status: resolved
trigger: "render-pipeline-broken-after-phase-5"
created: 2026-03-27T00:00:00Z
updated: 2026-03-27T03:00:00Z
---

## Current Focus
<!-- OVERWRITE on each update - reflects NOW -->

hypothesis: CONFIRMED — Three scene setup bugs fixed in renderer/render.py
test: Code analysis + geometry math verified all three bugs and fixes
expecting: User runs pipeline and sees colored, varied frames with orbiting camera
next_action: Await human verification of rendered output

## Symptoms
<!-- Written during gathering, then IMMUTABLE -->

expected: All math sequences (Fibonacci, primes, etc.) should render with data-driven materials and colors, export 4K PNGs and videos
actual: Only Fibonacci sequence renders. Other sequences (primes, etc.) do not render. No data-driven materials or colors applied. No videos generated. Exported PNGs look wrong/unexpected.
errors: Not yet checked — investigate console/logs during investigation
reproduction: Run the Blender render pipeline
started: Broke after Phase 5 (Blender renderer) was executed

## Eliminated
<!-- APPEND only - prevents re-investigating -->

- hypothesis: Phase 5 broke the render.py data parsing logic
  evidence: render.py data parsing code (lines 68-72) is unchanged from Phase 4 and correctly reads data.data.points for primes/fractal JSON
  timestamp: 2026-03-27T01:00:00Z

- hypothesis: FFmpeg frame naming mismatch
  evidence: render.py uses "frame_" as filepath base → Blender produces "frame_0001.png"; FFmpeg expects "frame_%04d.png" — these match
  timestamp: 2026-03-27T01:00:00Z

## Evidence
<!-- APPEND only - facts discovered -->

- timestamp: 2026-03-27T01:00:00Z
  checked: data/ directory contents
  found: Only primes.json and fractal.json exist — NO fibonacci.json
  implication: Fibonacci cannot be rendered via run_pipeline.py because there is no fibonacci.json data file

- timestamp: 2026-03-27T01:00:00Z
  checked: engine/server.py fibonacci endpoint response format
  found: Fibonacci endpoint returns {data: {sequence: ['0','1','1',...], points: null}} — no 3D points, only string sequence
  implication: Even if a fibonacci.json were created from the API, render.py would extract 0 points and render an empty scene

- timestamp: 2026-03-27T01:00:00Z
  checked: export_data.py
  found: Only exports "primes" and "fractal" types — no fibonacci export path
  implication: There is no way to export fibonacci data for rendering via existing tools

- timestamp: 2026-03-27T01:00:00Z
  checked: render.py material setup
  found: DataMaterial uses Object Info Color node → Principled BSDF Base Color. obj.color is set per object. BUT the Principled BSDF Material Output is NOT connected — links.new missing for node_bsdf → node_output connection.
  implication: Material output is disconnected → no shading applied, renders appear plain/grey

- timestamp: 2026-03-27T01:00:00Z
  checked: render.py node connections
  found: Lines 97-104 connect Object Info → BSDF inputs. But there is NO link connecting node_bsdf.outputs["BSDF"] to node_output.inputs["Surface"]. Material tree is broken.
  implication: Data-driven colors not applied to rendered output

- timestamp: 2026-03-27T01:00:00Z
  checked: web/src/data/artworks.ts
  found: Only "fibonacci" artwork listed. No primes or fractal entries.
  implication: Gallery only shows Fibonacci. This is why "only Fibonacci renders" — it's the only one in the gallery data.

- timestamp: 2026-03-27T01:00:00Z
  checked: web/public/posters/
  found: Contains frame_0001.png, frame_0002.png, frame_0003.png (test frames from renders/test_frames). Artwork expects /posters/fibonacci.png — this file does NOT exist.
  implication: Poster image for Fibonacci is broken (wrong filename)

- timestamp: 2026-03-27T01:00:00Z
  checked: web/public/videos/
  found: Empty directory (only .gitkeep). No MP4 files.
  implication: No videos have ever been generated. The pipeline has never been run end-to-end.

- timestamp: 2026-03-27T01:00:00Z
  checked: run_pipeline.py
  found: Script exists and is correct but has never been run with actual Blender+FFmpeg. Verification was static analysis only (05-VERIFICATION.md confirms "human verification items noted for optional manual testing").
  implication: Videos not generated because pipeline was never executed end-to-end

- timestamp: 2026-03-27T01:00:00Z
  checked: Fibonacci 3D geometry
  found: fibonacci.py generates a flat list of integers (strings) with no 3D coordinates. Unlike primes (Ulam cylinder with x,y,z) and fractal (L-system with x,y,z), Fibonacci has no Point3D mapping.
  implication: Fibonacci cannot produce a 3D visualization without a spiral/coordinate mapping function

- timestamp: 2026-03-27T02:00:00Z
  checked: render.py turntable animation logic (lines 198-218)
  found: target.rotation_euler is keyframed from (0,0,0) to (0,0,360deg). Camera has TRACK_TO constraint aimed at target. Rotating an object's OWN euler angles changes its local orientation but NOT its world position. TRACK_TO tracks position. The camera never moves.
  implication: All 300 frames are identical — the camera stays fixed throughout the animation. This explains "all frames look the same."

- timestamp: 2026-03-27T02:00:00Z
  checked: render.py lighting setup
  found: Only a single SUN light is added (line 141). No world/ambient lighting is configured. No emission strength on the Principled BSDF material. With a single directional sun and no fill light, the dark hemisphere of each sphere is pure black (0,0,0). Small spheres at distance mostly show the terminator/dark side.
  implication: Spheres appear black — the lit side may have color but at 5px size the dark side dominates. This explains "uniform black dots."

- timestamp: 2026-03-27T02:00:00Z
  checked: render.py camera distance calculation (line 149)
  found: max_dim = max(x_range, y_range, z_range). For primes: y_range=99, x_range=20, z_range=20. max_dim=99, distance=198. But the visual spread the camera needs to frame is only 20 units wide. Camera is placed 198 units back to accommodate the y-axis depth, making x/z-spread appear as ~560px wide at 4K. Spheres are ~5px each.
  implication: Spheres are tiny dots because camera is far away due to wrong axis driving the distance calculation.

## Resolution
<!-- OVERWRITE as understanding evolves -->

root_cause: Seven compounding bugs across two sessions:
  SESSION 1 (found previously):
  1. MISSING MATERIAL OUTPUT LINK: render.py created DataMaterial but never connected node_bsdf.outputs["BSDF"] to node_output.inputs["Surface"]. Material shader tree incomplete.
  2. FIBONACCI HAS NO 3D POINTS: fibonacci endpoint returns flat string sequence, no Point3D. No export path existed.
  3. GALLERY ONLY LISTS FIBONACCI: artworks.ts only had one entry. Primes and fractal not in gallery.
  4. POSTER FILES MISNAMED: Gallery expects /posters/fibonacci.png but renders produce frame_0001.png etc.

  SESSION 2 (found this session — explains "black dots, no variation"):
  5. TURNTABLE ANIMATION BROKEN: Code rotated target.rotation_euler (0→360deg) but TRACK_TO constraint tracks target POSITION not orientation. Rotating an empty's euler angles does NOT move the camera. All 300 frames were identical because the camera never moved.
  6. NO AMBIENT LIGHTING: Only one SUN light, no world/ambient. With a single directional light, the dark hemisphere of each sphere is pure black (0,0,0) in Cycles. Small spheres at distance mostly show the terminator/dark side, making them appear uniformly black.
  7. CAMERA DISTANCE FROM WRONG AXIS: max_dim used max of all three axis ranges. For primes, y-range=99 dominates but y is depth (not lateral spread). Camera placed 198 units back when lateral spread is only 20 units. Spheres appeared as 5.6px dots instead of 22px.

fix:
  Session 1 fixes (previously applied):
  1. renderer/render.py: links.new(node_bsdf.outputs["BSDF"], node_output.inputs["Surface"])
  2. scripts/export_data.py: fibonacci_to_spiral_points() + fibonacci export path
  3. web/src/data/artworks.ts: primes and fractal entries added
  4. web/public/posters/: placeholder poster files named correctly

  Session 2 fixes (applied this session):
  5. TURNTABLE FIX: Replaced target.rotation_euler keyframes with camera location keyframes. Camera orbits centroid on a circle using cam.location = (centroid + distance*sin(angle), centroid - distance*cos(angle), elevation) per frame. TRACK_TO keeps camera aimed at centroid.
  6. LIGHTING FIX: Added fill SUN light from opposite side (energy=1.5). Added world background node with Strength=0.8 to provide ambient illumination, eliminating pure-black shadow regions.
  7. CAMERA DISTANCE FIX: Changed distance calculation from max(x,y,z range) to lateral_dim = max(x_range, z_range). For primes: distance=50 (was 198). Spheres now 22px at 4K (was 5.6px). Added cam.data.clip_end = max(distance*10, 1000) to prevent far-clip culling.

verification: CONFIRMED by user — test render produced 10 different frames with colored spheres, no black dots, camera orbiting correctly. Human-verified 2026-03-27.
files_changed:
  - renderer/render.py (session 1 + session 2)
  - scripts/export_data.py (session 1)
  - web/src/data/artworks.ts (session 1)
  - web/public/posters/fibonacci.png (session 1)
  - web/public/posters/primes.png (session 1)
  - web/public/posters/fractal.png (session 1)
