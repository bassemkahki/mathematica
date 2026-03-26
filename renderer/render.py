import bpy
import sys
import json
import os

def main():
    # 1. Delete all default objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # 2. Extract arguments
    argv = sys.argv
    if "--" not in argv:
        argv = []
    else:
        argv = argv[argv.index("--") + 1:]
        
    input_file = None
    if "--input" in argv:
        try:
            input_file = argv[argv.index("--input") + 1]
        except IndexError:
            pass
            
    camera_style = "static"
    if "--camera" in argv:
        try:
            camera_style = argv[argv.index("--camera") + 1]
        except IndexError:
            pass

    if not input_file:
        print("Error: --input argument is required", file=sys.stderr)
        sys.exit(1)
        
    if not os.path.exists(input_file):
        print(f"Error: input file {input_file} does not exist", file=sys.stderr)
        sys.exit(1)
        
    # 3. Open and parse the JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)
        
    points = []
    if 'data' in data and 'points' in data['data']:
        points = data['data']['points']
    elif 'points' in data:
        points = data['points']
        
    # ENGINE SETUP
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    
    # MATERIAL SETUP
    mat = bpy.data.materials.new(name="DataMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create Object Info, Principled BSDF, and Material Output
    node_obj_info = nodes.new(type="ShaderNodeObjectInfo")
    node_bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    node_output = nodes.new(type="ShaderNodeOutputMaterial")
    
    node_obj_info.location = (-400, 0)
    node_bsdf.location = (0, 0)
    node_output.location = (400, 0)
    
    # Link Object Info Color -> Base Color and Emission Color
    links.new(node_obj_info.outputs["Color"], node_bsdf.inputs["Base Color"])
    try:
        links.new(node_obj_info.outputs["Color"], node_bsdf.inputs["Emission Color"])
    except KeyError:
        try:
            links.new(node_obj_info.outputs["Color"], node_bsdf.inputs["Emission"])
        except KeyError:
            pass
    
    # MESH GENERATION
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    min_z, max_z = float('inf'), float('-inf')
    
    for idx, pt in enumerate(points):
        x, y, z = pt["x"], pt["y"], pt["z"]
        
        # update bounding box
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)
        min_z, max_z = min(min_z, z), max(max_z, z)
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), radius=0.1)
        obj = bpy.context.active_object
        
        # Assign color (using a simple data-driven coloring logic)
        norm_idx = idx / max(1, len(points) - 1)
        obj.color = (norm_idx, 1.0 - norm_idx, (x+y+z)%1.0, 1.0)
        
        # Assign material
        if len(obj.data.materials) == 0:
            obj.data.materials.append(mat)
            
    if not points:
        min_x, max_x, min_y, max_y, min_z, max_z = 0, 0, 0, 0, 0, 0
        
    # LIGHTING SETUP
    centroid_x = (min_x + max_x) / 2
    centroid_y = (min_y + max_y) / 2
    centroid_z = (min_z + max_z) / 2
    
    bpy.ops.object.light_add(type='SUN', location=(centroid_x + 5, centroid_y - 5, centroid_z + 5))
    sun = bpy.context.active_object
    try:
        sun.data.energy = 5.0
    except AttributeError:
        pass # Handle property name differences
        
    # CAMERA SETUP
    max_dim = max(max_x - min_x, max_y - min_y, max_z - min_z)
    distance = max_dim * 2 if max_dim > 0 else 10
    
    bpy.ops.object.camera_add(location=(centroid_x, centroid_y - distance, centroid_z + (distance * 0.5)))
    cam = bpy.context.active_object
    bpy.context.scene.camera = cam
    
    # Point camera at centroid
    # Create empty at centroid and add Track To constraint
    bpy.ops.object.empty_add(location=(centroid_x, centroid_y, centroid_z))
    target = bpy.context.active_object
    
    track = cam.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    print(f"Render finished. Objects generated: {len(points)}")

if __name__ == "__main__":
    main()
