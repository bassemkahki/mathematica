# Research Summary

Visualizing rigorous mathematics as expressive 4K art works best as a **three-tier architecture**. 

1. **The Math Generator**: Python is the absolute standard here. Avoid JavaScript's float limitations by doing the deep math (Fibonacci, Primes, Infinity) in Python and exporting normalized plotting or vector data.
2. **The Renderer**: Headless WebGL (Three.js/Shaders) or Blender automation should ingest this data frame-by-frame (to prevent memory exhaustion) and spit out 4K image sequences.
3. **The Gallery**: Use Next.js associated with a CDN pipeline. Do not attempt to render the math art in real-time in the browser; deliver pre-rendered MP4/WebM files to guarantee pristine 4K quality for the viewer. Keep an adjacent MDX/CMS system for the accompanying white papers. 

This approach minimizes technical risk (floating point issues, WebGL crashing) while maximizing output quality.
