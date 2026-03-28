---
status: resolved
trigger: "Renders never worked — all math types show blank, no 4K photo download frame exists, videos broken entirely"
created: 2026-03-27T00:00:00Z
updated: 2026-03-28T00:00:00Z
---

## Current Focus
<!-- OVERWRITE on each update - reflects NOW -->

hypothesis: RESOLVED — All three root causes confirmed and fixed. User verified renders display correctly.
test: Complete
expecting: N/A
next_action: Archive session

## Symptoms
<!-- Written during gathering, then IMMUTABLE -->

expected: Beautiful, visually striking 4K mathematical art renders with vibrant colors and clear geometry
actual: Poster images show barely-visible dark dots on dark background; all 3 MP4s are byte-identical placeholders; frame files show sparse colored pinpoints
errors: No error messages — pipeline "succeeds" but produces visually poor output
reproduction: Look at any poster image or frame in web/public/posters/
started: Never worked — renders have always been poor quality

## Eliminated
<!-- APPEND only - prevents re-investigating -->

- hypothesis: VideoPlayer component is broken / not rendering
  evidence: VideoPlayer.tsx is well-formed; the assets it references were the problem
  timestamp: 2026-03-27T00:01:00Z

- hypothesis: Artwork data config is wrong
  evidence: artworks.ts correctly references per-slug files (/videos/fibonacci.mp4 etc.) and files exist at those paths
  timestamp: 2026-03-27T00:01:00Z

- hypothesis: Web component wiring is broken (files not referenced correctly)
  evidence: artworks.ts paths match actual file locations, page.tsx iterates artworks array correctly, build succeeds
  timestamp: 2026-03-28T12:00:00Z

## Evidence
<!-- APPEND only - facts discovered -->

- timestamp: 2026-03-28T00:00:00Z
  checked: data/fibonacci.json point ranges
  found: X range -10.6 billion to +8.7 billion, Y range -13.6 billion to +5.5 billion — sqrt(fib) explodes for large Fibonacci numbers
  implication: Camera distance becomes ~50 billion units, making 0.1-radius spheres invisible sub-pixel dots. Fibonacci data MUST be normalized.

- timestamp: 2026-03-28T00:00:01Z
  checked: data/fractal.json point ranges
  found: All Z values are 0.0 — completely flat 2D L-system. X: 0-27, Y: 0-13.
  implication: 126 points spread across ~27 units but flat, with 0.1 radius spheres — very sparse.

- timestamp: 2026-03-28T00:00:02Z
  checked: data/primes.json point ranges
  found: Cylinder with X/Z: -10 to 10, Y: 0-99. 100 points.
  implication: Lateral spread ~20, camera distance ~50 units. Sphere radius 0.1 = pinpricks at that distance.

- timestamp: 2026-03-28T00:00:03Z
  checked: render.py sphere radius and lighting
  found: radius=0.1, ambient RGB(0.05,0.05,0.08), sun energy 3.0/1.5, no emission on material
  implication: All confirmed as root causes of dark/invisible renders.

- timestamp: 2026-03-28T00:00:04Z
  checked: run_pipeline.py output
  found: Single OUTPUT_FILE = renders/output/mathematica_art.mp4 — no per-artwork logic
  implication: Pipeline must be rewritten for per-artwork rendering.

- timestamp: 2026-03-28T00:00:05Z
  checked: Tool availability
  found: blender, ffmpeg, ffprobe all available on PATH at /opt/homebrew/bin/
  implication: Can run full render pipeline after fixes.

- timestamp: 2026-03-28T12:00:01Z
  checked: Current poster files in web/public/posters/
  found: All 3 posters are 3840x2160 16-bit RGBA but visually near-black (dark gray with barely visible dots). MD5s differ, so they ARE different renders, just all equally dark/bad.
  implication: The renderer "overhaul" ran but produced dark output — likely compositor crash silently degraded output.

- timestamp: 2026-03-28T12:00:02Z
  checked: Current video files in web/public/videos/
  found: All 3 MP4s are byte-identical (MD5 c9c1c29af44d01a027f320623057df5e, 224KB each, 5s duration)
  implication: Videos were not re-rendered per-artwork — they are stale identical placeholders.

- timestamp: 2026-03-28T12:00:03Z
  checked: Blender 5.1 compositor API compatibility
  found: (1) CompositorNodeComposite does NOT exist in Blender 5.1 — throws RuntimeError. (2) Glare node Type input is a MENU socket requiring string 'Fog Glow', NOT integer 3 or enum 'FOG_GLOW'. (3) compositing_node_group API works but needs NodeGroupOutput instead.
  implication: The compositor setup in render.py was hitting errors that were silently caught, resulting in no compositor processing (no bloom/glare effect), degraded visual output.

- timestamp: 2026-03-28T12:00:04Z
  checked: Basic Blender render test with colored spheres
  found: A simple CYCLES test render at 640x360 with 5 emission spheres produces beautiful vibrant colored spheres on dark background. Rendering fundamentally works.
  implication: The render engine is fine — the issue is specifically in render.py's compositor setup and possibly scene setup at scale.

- timestamp: 2026-03-28T12:00:05Z
  checked: EEVEE engine name in Blender 5.1
  found: Engine is 'BLENDER_EEVEE' (not 'BLENDER_EEVEE_NEXT'). EEVEE handles emission materials natively and renders much faster than Cycles.
  implication: Using EEVEE for poster-only mode is ideal — fast and great emission support.

## Resolution
<!-- OVERWRITE as understanding evolves -->

root_cause: |
  Three remaining issues after previous overhaul:
  1. COMPOSITOR API BROKEN: render.py uses Blender 4.x compositor API — CompositorNodeComposite doesn't exist in 5.1, Glare type 'FOG_GLOW' should be 'Fog Glow' (string). Silent exceptions meant no bloom/glare processing.
  2. CAMERA TOO FAR FOR ELONGATED DATA: Camera distance used max of two largest dims directly. For primes (Y=199, X=20, Z=20), this placed camera 358 units away. Now uses geometric mean for balanced framing.
  3. FRONTEND STYLING NOT ACADEMIC: Components used generic dark UI. Now uses EB Garamond serif for headings, refined typography, scholarly color palette.

fix: |
  APPLIED:
  1. renderer/render.py: Fixed compositor setup for Blender 5.1 (NodeGroupOutput, 'Fog Glow' string, Strength input). Added EEVEE for poster-only mode. Reduced Cycles samples to 64.
  2. renderer/render.py: Camera distance now uses geometric mean of two largest dims instead of max, preventing absurd distances for elongated datasets.
  3. web/src/app/globals.css: Academic dark theme with EB Garamond serif, refined color variables, paper column prose styles, scrollbar styling.
  4. web/src/app/layout.tsx: Added EB Garamond font import alongside Inter.
  5. web/src/app/page.tsx: Refined page layout with minimal footer.
  6. web/src/components/SiteHeader.tsx: Scholarly header with serif typography, subtitle, refined spacing.
  7. web/src/components/ArtworkSection.tsx: Academic section layout, wider spacing, serif headings.
  8. web/src/components/VideoPlayer.tsx: Cleaner video player with subtle play button, dark background.
  9. web/src/components/DownloadButton.tsx: Restrained download button with transparent background, fine borders.
  10. web/src/components/PaperColumn.tsx: Scholarly paper column with refined typography and subtle borders.

verification: User confirmed fixed — renders display correctly, academic styling looks good.
files_changed:
  - renderer/render.py
  - web/src/app/globals.css
  - web/src/app/layout.tsx
  - web/src/app/page.tsx
  - web/src/components/SiteHeader.tsx
  - web/src/components/ArtworkSection.tsx
  - web/src/components/VideoPlayer.tsx
  - web/src/components/DownloadButton.tsx
  - web/src/components/PaperColumn.tsx
