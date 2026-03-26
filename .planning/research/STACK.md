# Research: Stack

## Standard Stack

### Math Engine (Backend Compute)
- **Python (NumPy, SciPy, SymPy)**: The gold standard for rigorous mathematical computation, sequence generation (Fibonacci, primes), and analytical geometry. Standard for generating abstract data without losing precision.
- **Numba or Cython**: For JIT compiling heavy fractal calculations or very large sequence visualizations.
- **JSON/NDJSON or HDF5**: For serializing the mathematical frame data to pass to the renderer.

### Rendering Engine (Offline 4K Export)
- **Blender (Python API / Geometry Nodes)**: The ultimate standard for offline 4K abstract and geometric art matching. Easily driven by Python scripts.
- **Three.js / React-Three-Fiber (Headless via Puppeteer)**: If using WebGL shaders is strongly preferred, you can run a headless browser to export 4K TIFFs/PNGs frame-by-frame and compile via FFmpeg.
- **FFmpeg**: Essential for stitching extremely high-resolution image sequences into 4K MP4 assets.

### Web Gallery (Presentation)
- **Next.js**: The industry standard for high-performance gallery sites and blog architectures (for the white papers).
- **Vercel / AWS**: For hosting the site and streaming 4K video reliably.

## What NOT to use
- **Pure JavaScript for Math**: JS numbers (double-precision floats) lack the arbitrary precision needed to correctly display extremely large primes or deep Fibonacci sequences.
- **Real-time WebGL for 4K visuals on the Gallery**: It's too demanding and introduces hardware variability for the end user.
