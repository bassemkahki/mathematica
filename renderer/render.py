"""Blender headless render script for Mathematica Art.

Produces visually stunning 4K mathematical visualizations with:
- Adaptive sphere sizing based on data density and spread
- Vibrant HSV rainbow coloring that reveals mathematical structure
- Glowing emission materials for a cosmic/neon aesthetic
- Rich multi-light setup with colored accent lights
- Deep dark background to make colors pop
- Smooth turntable camera animation
"""
import bpy
import sys
import json
import os
import math
import colorsys


def parse_args():
    """Extract CLI arguments passed after '--'."""
    argv = sys.argv
    if "--" not in argv:
        argv = []
    else:
        argv = argv[argv.index("--") + 1:]

    def get_arg(name, default=None, cast=None):
        if name in argv:
            try:
                val = argv[argv.index(name) + 1]
                return cast(val) if cast else val
            except (IndexError, ValueError):
                pass
        return default

    return {
        "input_file": get_arg("--input"),
        "camera_style": get_arg("--camera", "static"),
        "frame_count": get_arg("--frames", 300, int),
        "output_dir": get_arg("--output-dir", "renders/frames"),
        "output_format": (get_arg("--format", "PNG") or "PNG").upper(),
        "slug": get_arg("--slug", "artwork"),
        "poster_only": "--poster-only" in argv,
    }


def load_points(input_file):
    """Load 3D point data from JSON."""
    with open(input_file, 'r') as f:
        data = json.load(f)

    if 'data' in data and 'points' in data['data']:
        return data['data']['points']
    elif 'points' in data:
        return data['points']
    return []


def compute_bounds(points):
    """Compute bounding box and centroid from points."""
    xs = [p["x"] for p in points]
    ys = [p["y"] for p in points]
    zs = [p["z"] for p in points]

    bounds = {
        "min_x": min(xs), "max_x": max(xs),
        "min_y": min(ys), "max_y": max(ys),
        "min_z": min(zs), "max_z": max(zs),
    }
    bounds["cx"] = (bounds["min_x"] + bounds["max_x"]) / 2
    bounds["cy"] = (bounds["min_y"] + bounds["max_y"]) / 2
    bounds["cz"] = (bounds["min_z"] + bounds["max_z"]) / 2
    bounds["span_x"] = bounds["max_x"] - bounds["min_x"]
    bounds["span_y"] = bounds["max_y"] - bounds["min_y"]
    bounds["span_z"] = bounds["max_z"] - bounds["min_z"]
    bounds["max_span"] = max(bounds["span_x"], bounds["span_y"], bounds["span_z"], 0.01)
    return bounds


def compute_adaptive_radius(points, bounds):
    """Compute sphere radius so points are visible but don't overlap excessively.

    Target: spheres occupy ~3-5% of the scene span per point, adjusted for density.
    For sparse data (< 50 points): larger spheres.
    For dense data (> 500 points): smaller spheres.
    """
    n = len(points)
    span = bounds["max_span"]

    # Base radius: fraction of scene span
    base = span * 0.025

    # Density adjustment: fewer points -> bigger, more points -> smaller
    density_factor = math.pow(100.0 / max(n, 1), 0.3)

    radius = base * density_factor
    # Clamp to reasonable range
    return max(0.05, min(radius, span * 0.08))


def create_point_material(name, color_rgb, emission_strength=2.0):
    """Create a glowing material with emission for a single point.

    Each point gets its own material with a unique color, combining
    surface reflection with emission for a glowing/neon look.
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Principled BSDF for surface
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)
    bsdf.inputs["Base Color"].default_value = (*color_rgb, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.3
    bsdf.inputs["Roughness"].default_value = 0.4

    # Set emission color and strength
    try:
        bsdf.inputs["Emission Color"].default_value = (*color_rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    except KeyError:
        try:
            bsdf.inputs["Emission"].default_value = (*color_rgb, 1.0)
        except KeyError:
            pass

    # Output
    output = nodes.new(type="ShaderNodeOutputMaterial")
    output.location = (400, 0)
    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

    return mat


def point_color(idx, total, points, bounds):
    """Generate vibrant HSV-based color that reveals mathematical structure.

    Hue cycles through the rainbow based on point index (reveals ordering).
    Saturation stays high for vivid colors.
    Value (brightness) stays high for visibility.
    """
    # Hue: full rainbow cycle based on index position
    hue = (idx / max(total - 1, 1))

    # Slight variation based on position for visual depth
    pt = points[idx]
    # Normalize position to 0-1 range within bounds
    nx = (pt["x"] - bounds["min_x"]) / max(bounds["span_x"], 0.001)

    # Saturation: high but with slight position-based variation
    saturation = 0.85 + 0.15 * nx

    # Value: bright
    value = 0.9 + 0.1 * (1.0 - abs(hue - 0.5) * 2)  # slightly brighter at edges

    r, g, b = colorsys.hsv_to_rgb(hue % 1.0, min(saturation, 1.0), min(value, 1.0))
    return (r, g, b)


def setup_lighting(bounds):
    """Create rich multi-light setup for dramatic, beautiful illumination.

    - Key light (warm sun): main directional light
    - Fill light (cool sun): fills shadows with complementary color
    - Rim/accent lights (colored area lights): add colored highlights
    - World: very dark blue-black for cosmic feel with subtle ambient
    """
    cx, cy, cz = bounds["cx"], bounds["cy"], bounds["cz"]
    span = bounds["max_span"]

    # Key light — warm white sun
    bpy.ops.object.light_add(type='SUN', location=(cx + span, cy - span, cz + span * 1.5))
    key = bpy.context.active_object
    key.data.energy = 5.0
    key.data.color = (1.0, 0.95, 0.9)  # warm white

    # Fill light — cool blue sun from opposite side
    bpy.ops.object.light_add(type='SUN', location=(cx - span, cy + span, cz + span * 0.5))
    fill = bpy.context.active_object
    fill.data.energy = 2.5
    fill.data.color = (0.8, 0.85, 1.0)  # cool blue-white

    # Accent area light — magenta/pink from below for dramatic uplighting
    bpy.ops.object.light_add(type='AREA', location=(cx, cy, cz - span * 0.5))
    accent1 = bpy.context.active_object
    accent1.data.energy = 200.0 * (span / 10.0)  # scale with scene size
    accent1.data.color = (1.0, 0.3, 0.6)  # magenta-pink
    accent1.data.size = span * 0.5
    # Point upward
    accent1.rotation_euler = (math.radians(180), 0, 0)

    # Accent area light — cyan from the side
    bpy.ops.object.light_add(type='AREA', location=(cx + span * 0.8, cy, cz))
    accent2 = bpy.context.active_object
    accent2.data.energy = 150.0 * (span / 10.0)
    accent2.data.color = (0.2, 0.8, 1.0)  # cyan
    accent2.data.size = span * 0.3
    accent2.rotation_euler = (0, math.radians(-90), 0)

    # World background — deep dark blue-black
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node is None:
        bg_node = world.node_tree.nodes.new(type="ShaderNodeBackground")
    # Very dark navy — cosmic feel
    bg_node.inputs["Color"].default_value = (0.005, 0.005, 0.02, 1.0)
    bg_node.inputs["Strength"].default_value = 1.0


def setup_camera(bounds, frame_count):
    """Set up camera with turntable animation framing the data nicely."""
    cx, cy, cz = bounds["cx"], bounds["cy"], bounds["cz"]

    # Use the geometric mean of the two largest dimensions for balanced framing.
    # This prevents one very long axis (e.g. primes Y=199) from pushing the
    # camera absurdly far when the other axes are small.
    dims = sorted([bounds["span_x"], bounds["span_y"], bounds["span_z"]], reverse=True)
    lateral_dim = math.sqrt(max(dims[0], 1.0) * max(dims[1], 1.0))
    distance = lateral_dim * 2.0

    # Camera placement
    bpy.ops.object.camera_add(location=(cx, cy - distance, cz + distance * 0.35))
    cam = bpy.context.active_object
    bpy.context.scene.camera = cam
    cam.data.clip_end = max(distance * 10, 1000)

    # Slight depth of field for cinematic feel (focal on centroid)
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = distance
    cam.data.dof.aperture_fstop = 8.0  # subtle blur

    # Track To constraint -> always look at centroid
    bpy.ops.object.empty_add(location=(cx, cy, cz))
    target = bpy.context.active_object
    target.name = "CameraTarget"

    track = cam.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    # Turntable animation
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = frame_count
    cam_elevation = distance * 0.35

    for frame in range(1, frame_count + 1):
        angle = math.radians(360.0 * (frame - 1) / frame_count)
        cam.location.x = cx + distance * math.sin(angle)
        cam.location.y = cy - distance * math.cos(angle)
        cam.location.z = cz + cam_elevation
        cam.keyframe_insert(data_path="location", frame=frame)

    # Linear interpolation for constant orbit speed
    if cam.animation_data and cam.animation_data.action:
        action = cam.animation_data.action
        fcurves = []
        if hasattr(action, 'fcurves'):
            fcurves = action.fcurves
        elif hasattr(action, 'layers'):
            for layer in action.layers:
                for strip in layer.strips:
                    if hasattr(strip, 'channelbags'):
                        for cb in strip.channelbags:
                            fcurves.extend(cb.fcurves)
        for fcurve in fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'

    return cam


def create_connection_curves(points, bounds, radius):
    """Create thin curves connecting sequential points for visual continuity.

    This adds trails/connections that make the mathematical structure visible
    — spirals, paths, and patterns become apparent.
    """
    if len(points) < 2:
        return

    # Create a single curve object with all segments
    curve_data = bpy.data.curves.new(name="ConnectionCurve", type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = radius * 0.15  # thin tubes
    curve_data.bevel_resolution = 2

    # Create spline through all points
    spline = curve_data.splines.new('NURBS')
    spline.points.add(len(points) - 1)  # already has 1 point
    for i, pt in enumerate(points):
        spline.points[i].co = (pt["x"], pt["y"], pt["z"], 1.0)
    spline.use_endpoint_u = True
    spline.order_u = min(4, len(points))

    curve_obj = bpy.data.objects.new("Connections", curve_data)
    bpy.context.collection.objects.link(curve_obj)

    # Glowing white-blue material for the curve
    mat = bpy.data.materials.new(name="CurveMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)
    bsdf.inputs["Base Color"].default_value = (0.6, 0.8, 1.0, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.5
    bsdf.inputs["Roughness"].default_value = 0.3
    try:
        bsdf.inputs["Emission Color"].default_value = (0.4, 0.6, 1.0, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 1.0
    except KeyError:
        pass

    output = nodes.new(type="ShaderNodeOutputMaterial")
    output.location = (400, 0)
    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

    curve_obj.data.materials.append(mat)


def setup_render_settings(output_dir, output_format, frame_count, poster_only):
    """Configure 4K render settings.

    Uses EEVEE for poster-only (fast, great emission support).
    Uses Cycles for full animation (higher quality, GPU-accelerated).
    """
    scene = bpy.context.scene

    # Resolution
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2160
    scene.render.resolution_percentage = 100

    # Output directory
    os.makedirs(output_dir, exist_ok=True)
    scene.render.filepath = os.path.join(output_dir, "frame_")

    # Format
    if output_format == "TIFF":
        scene.render.image_settings.file_format = 'TIFF'
        scene.render.image_settings.color_depth = '16'
    else:
        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_depth = '16'
        scene.render.image_settings.color_mode = 'RGBA'
        scene.render.image_settings.compression = 15

    # Engine selection: EEVEE is much faster and handles emission well
    # Blender 5.x uses 'BLENDER_EEVEE' (not 'BLENDER_EEVEE_NEXT')
    if poster_only:
        scene.render.engine = 'BLENDER_EEVEE'
    else:
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'GPU'
        scene.cycles.samples = 64  # reduced from 128 for speed
        scene.cycles.use_denoising = True
        scene.cycles.denoiser = 'OPENIMAGEDENOISE'

    # Film: transparent background OFF (we want the dark cosmic background)
    scene.render.film_transparent = False

    # Compositor: Bloom/glare for glow effect
    # Blender 5.x uses compositing_node_group (scene.node_tree removed)
    scene.use_nodes = True
    tree = getattr(scene, 'compositing_node_group', None)
    if tree is None:
        tree = bpy.data.node_groups.new('Compositor', 'CompositorNodeTree')
        scene.compositing_node_group = tree
    else:
        for node in list(tree.nodes):
            tree.nodes.remove(node)

    # Render Layers -> Glare -> Output
    render_layers = tree.nodes.new(type='CompositorNodeRLayers')
    render_layers.location = (0, 0)

    glare = tree.nodes.new(type='CompositorNodeGlare')
    glare.location = (300, 0)
    # Blender 5.1: Glare Type is a MENU socket taking string enum values
    try:
        glare.inputs['Type'].default_value = 'Fog Glow'
    except (KeyError, TypeError):
        pass
    try:
        glare.inputs['Threshold'].default_value = 0.3
        glare.inputs['Size'].default_value = 7.0
        glare.inputs['Strength'].default_value = 0.8
    except (KeyError, TypeError):
        pass

    # Blender 5.1: CompositorNodeComposite removed, use NodeGroupOutput
    output_node = tree.nodes.new(type='NodeGroupOutput')
    try:
        tree.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    except Exception:
        pass
    output_node.location = (600, 0)

    tree.links.new(render_layers.outputs['Image'], glare.inputs['Image'])
    tree.links.new(glare.outputs['Image'], output_node.inputs['Image'])

    # Frame range
    if poster_only:
        scene.frame_start = 1
        scene.frame_end = 1
    else:
        scene.frame_start = 1
        scene.frame_end = frame_count


def main():
    # Clear scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    args = parse_args()

    if not args["input_file"]:
        print("Error: --input argument is required", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args["input_file"]):
        print(f"Error: input file {args['input_file']} does not exist", file=sys.stderr)
        sys.exit(1)

    # Load data
    points = load_points(args["input_file"])
    if not points:
        print("Error: no points found in input data", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(points)} points from {args['input_file']}")

    # Compute spatial info
    bounds = compute_bounds(points)
    print(f"Bounds: X[{bounds['min_x']:.2f}, {bounds['max_x']:.2f}] "
          f"Y[{bounds['min_y']:.2f}, {bounds['max_y']:.2f}] "
          f"Z[{bounds['min_z']:.2f}, {bounds['max_z']:.2f}]")

    # Adaptive radius
    radius = compute_adaptive_radius(points, bounds)
    print(f"Adaptive sphere radius: {radius:.4f} (scene span: {bounds['max_span']:.2f})")

    # Create geometry — individual spheres with per-point materials
    n = len(points)
    for idx, pt in enumerate(points):
        x, y, z = pt["x"], pt["y"], pt["z"]

        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=3,
            location=(x, y, z),
            radius=radius,
        )
        obj = bpy.context.active_object
        obj.name = f"Point_{idx:04d}"

        # Vibrant color per point
        color = point_color(idx, n, points, bounds)

        # Emission strength: slightly varied for visual interest
        emission = 2.0 + 1.0 * (idx / max(n - 1, 1))

        mat = create_point_material(f"Mat_{idx:04d}", color, emission)
        if len(obj.data.materials) == 0:
            obj.data.materials.append(mat)
        else:
            obj.data.materials[0] = mat

    # Connection curves between sequential points
    create_connection_curves(points, bounds, radius)

    # Lighting
    setup_lighting(bounds)

    # Camera
    cam = setup_camera(bounds, args["frame_count"])

    # Render settings
    setup_render_settings(
        args["output_dir"],
        args["output_format"],
        args["frame_count"],
        args["poster_only"],
    )

    # Render — always use animation mode for consistent frame_NNNN naming
    if args["poster_only"]:
        print(f"Rendering poster frame at 3840x2160 to {args['output_dir']}...")
    else:
        print(f"Rendering {args['frame_count']} frames at 3840x2160 to {args['output_dir']}...")
    bpy.ops.render.render(animation=True)

    print(f"Render complete. {len(points)} objects generated.")


if __name__ == "__main__":
    main()
