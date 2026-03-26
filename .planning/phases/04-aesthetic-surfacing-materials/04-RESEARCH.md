# Phase 4: Aesthetic Surfacing & Materials - Research

## Objective
Research how to implement Phase 4, specifically addressing the requirements for photorealistic shaders, data-driven material assignments, studio HDRI lighting, and framing options in the existing Blender headless script (`renderer/render.py`).

## Findings

### 1. Photorealistic Visual Style & Data-Driven Materials 
- Data-driven materials can be achieved by creating a single material using `bpy.data.materials.new` and enabling `use_nodes = True`.
- To make materials respond to point spatial position, the shader can use an `Object Info` node. The `Location` output can be fed into a `ColorRamp` or Math nodes to generate dynamic coloring (e.g., mapping height to color hue, or radial distance to emission strength).
- Alternatively, we can assign a specific object color to each geometry via `obj.color = (R, G, B, A)` and read this attribute in the shader using the `Color` output of the `Object Info` node. This allows the math engine to explicitly dictate exact RGBA values per point, which is more powerful.
- The material must be assigned to every generated object using `obj.data.materials.append(mat)`.
- For photorealism, the Material should use the `Principled BSDF` node (which handles glass, rough math, emission, etc.) combined with `Cycles` engine, or an `Emission` node if we want glowing mathematical constructs.

### 2. Studio Lighting Setup (HDRI / Environment)
- Blender uses the World node tree for environmental lighting. `bpy.data.worlds['World'].use_nodes = True`.
- Using an actual HDRI file requires an external `.hdr` or `.exr` file. We can create a setup that expects an `--hdri` CLI argument, and if omitted, falls back to a built-in `Sky Texture` node (`ShaderNodeTexSky`), which provides realistic HDRI-like sun/sky lighting procedurally.
- Alternatively, a programmatic 3-point lighting setup (using 3 Area Lights: Key, Fill, Back) can simulate a photoreal studio environment without relying on external HDRI textures. We will add a 3-point light setup to the script.

### 3. Camera Framing (Static vs Fly-Through)
- A camera must be added to the scene: `bpy.ops.object.camera_add(location=(x, y, z), rotation=(rX, rY, rZ))`.
- It must be set as the active camera: `bpy.context.scene.camera = bpy.context.object`.
- **Static Framing:** We can programmatically compute the bounding box of the input data points (min/max X, Y, Z), compute the centroid, point the camera at the centroid, and pull the camera back along a vector (e.g., Euclidean distance based on bounding box size) so that all points are visible within the camera's FOV.
- **Dynamic Fly-through:** For animation, Blender's Python API allows keyframing. `cam_obj.keyframe_insert(data_path="location", frame=1)`. We can generate a circular orbit path or a sweep through the data bounding box and keyframe the camera location and rotation over `bpy.context.scene.frame_end` frames.

### 4. Rendering Pipeline
- Currently, `renderer/render.py` uses `primitive_ico_sphere_add`. Adding this into a loop with tens of thousands of objects can become slow. However, for initial materials and rendering, it's sufficient until optimization is needed.
- We need to configure the render engine to `CYCLES` for photorealistic results:
  `bpy.context.scene.render.engine = 'CYCLES'`
- Setting device to GPU compute is crucial for 4K rendering:
  `bpy.context.scene.cycles.device = 'GPU'`

## Validation Architecture
- **Materials:** Check if material is assigned and node tree exists.
- **Lighting:** Check if lights exist in `bpy.data.objects`.
- **Camera:** Check if a camera is set as `bpy.context.scene.camera`.
- **CLI parameters:** The headless script must accept parameters to toggle settings, like `--camera-animation orbit` or `--style glass`.

## RESEARCH COMPLETE
