# Research: Architecture

## Component Boundaries

### 1. Data Generation Service
Calculates the exact mathematical vertices, color mapping points, or geometry specifications. Runs heavily in Python. Generates static structured data (JSON/CSV point clouds or algebraic geometry descriptions).

### 2. Render Pipeline
Consumes the data generated in step 1. Uses a rendering tool (Blender via Python or headless Three.js via WebGL shaders) to execute the visual creation and render high bit-depth frame sequences. Converts sequences into 4K container formats using FFmpeg.

### 3. Front-End Web Gallery
A static-generated or server-rendered web application (Next.js) holding the content. It stores the video files (on a CDN or S3) and maps them to clean academic text pages (white papers).

## Data Flow
`Python Math Computation -> JSON/Points -> Render Engine (WebGL/Blender) -> Image Sequence -> FFmpeg -> 4K MP4 -> Web Server -> End User Browser`

## Build Order
1. Build and verify the Math Engine (ensure math maps to structural JSON).
2. Build the Renderer (ensure you can read JSON and export a 4K frame).
3. Automate frame-to-video export.
4. Build the Web Gallery to host the videos.
