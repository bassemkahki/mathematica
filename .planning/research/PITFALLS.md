# Research: Pitfalls

## Critical Mistakes & Prevention

### 1. Floating-Point Precision Loss
- **Warning sign**: Artifacts or repeating pixel blocks as the visualization zooms in (esp. in infinity representations) or computes large primes.
- **Prevention**: Do not use standard 64-bit floats for deep calculus or fractals. Use `mpmath` or Python's `decimal` for the engine, passing scaled normalized data to the renderer.
- **Phase**: Setup Math Engine.

### 2. Memory Exhaustion During Render
- **Warning sign**: WebGL context crashes or Blender runs out of RAM loading millions of points for a 4K frame.
- **Prevention**: Process data in chunks. Never load a 10-minute 60fps sequence data file all at once. Load frame-by-frame data during the render loop.
- **Phase**: Export Pipeline.

### 3. Video Bandwidth Issues on Gallery
- **Warning sign**: The gallery takes 30 seconds to load the 4K animation for visitors.
- **Prevention**: Serve multiple video qualities (e.g. 1080p fallback) and use proper web codecs (H.265 / VP9 with fallback to H.264) hosted on a CDN.
- **Phase**: Web Gallery / Frontend.
