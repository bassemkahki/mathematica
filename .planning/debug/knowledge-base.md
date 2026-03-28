# GSD Debug Knowledge Base

Resolved debug sessions. Used by `gsd-debugger` to surface known-pattern hypotheses at the start of new investigations.

---

## render-pipeline-broken-after-phase-5 — Seven compounding render pipeline bugs: broken material shader, no 3D points for Fibonacci, missing gallery entries, misnamed poster files, static turntable camera, no ambient lighting, camera distance from wrong axis
- **Date:** 2026-03-27
- **Error patterns:** render, blender, pipeline, material, black dots, camera, turntable, animation, spheres, colored, fibonacci, primes, fractal, poster, gallery, artworks, export, frames, identical, dark
- **Root cause:** Seven bugs compounding: (1) Principled BSDF node not connected to Material Output — shader tree broken; (2) Fibonacci sequence has no 3D point mapping — flat string list, not renderable; (3) artworks.ts only listed Fibonacci — primes/fractal not in gallery; (4) poster files named frame_0001.png not fibonacci.png/primes.png/fractal.png; (5) turntable rotated target.rotation_euler but TRACK_TO tracks position not orientation — all 300 frames identical; (6) single SUN light with no ambient — dark hemisphere of spheres pure black; (7) camera distance driven by max(x,y,z range) — depth axis (y=99) dominated, placing camera 198 units back when lateral spread was only 20 units, making spheres appear as 5px dots
- **Fix:** (1) links.new(node_bsdf.outputs["BSDF"], node_output.inputs["Surface"]); (2) fibonacci_to_spiral_points() added to export_data.py; (3) primes and fractal entries added to artworks.ts; (4) placeholder poster PNGs named correctly; (5) camera location keyframed on orbit circle using sin/cos per frame; (6) fill SUN + world background node (Strength=0.8); (7) lateral_dim = max(x_range, z_range) for camera distance
- **Files changed:** renderer/render.py, scripts/export_data.py, web/src/data/artworks.ts, web/public/posters/fibonacci.png, web/public/posters/primes.png, web/public/posters/fractal.png
---

## webpage-renders-4k-video-broken — Blender 5.1 compositor API breaks, camera framing too distant for elongated data, frontend lacks academic styling
- **Date:** 2026-03-28
- **Error patterns:** render, blender, compositor, dark, near-black, barely visible, dots, camera distance, 4K, poster, video, identical, placeholder, CompositorNodeComposite, Glare, FOG_GLOW, EEVEE, emission, academic, styling, serif
- **Root cause:** Three compounding issues: (1) Blender 5.1 removed CompositorNodeComposite and changed Glare node type from enum 'FOG_GLOW' to string 'Fog Glow' — silent exceptions meant no bloom/glare processing; (2) Camera distance used max of two largest dims directly, placing camera too far for elongated datasets (e.g. primes Y=199 vs X=20); (3) Frontend used generic dark UI instead of academic/scholarly styling.
- **Fix:** (1) Updated compositor to use NodeGroupOutput and 'Fog Glow' string for Blender 5.1 API; added EEVEE for poster-only mode; reduced Cycles samples to 64. (2) Camera distance now uses geometric mean of two largest dims. (3) Added EB Garamond serif typography, refined dark academic theme across all components.
- **Files changed:** renderer/render.py, web/src/app/globals.css, web/src/app/layout.tsx, web/src/app/page.tsx, web/src/components/SiteHeader.tsx, web/src/components/ArtworkSection.tsx, web/src/components/VideoPlayer.tsx, web/src/components/DownloadButton.tsx, web/src/components/PaperColumn.tsx
---

