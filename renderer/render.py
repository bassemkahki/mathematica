import bpy
import sys
import json
import os

def main():
    # 1. Delete all default objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # 2. Extract the --input command line argument
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
            
    if not input_file:
        print("Error: --input argument is required", file=sys.stderr)
        sys.exit(1)
        
    if not os.path.exists(input_file):
        print(f"Error: input file {input_file} does not exist", file=sys.stderr)
        sys.exit(1)
        
    # 3. Open and parse the JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)
        
    # Handle both data['data']['points'] and data['points'] variations
    points = []
    if 'data' in data and 'points' in data['data']:
        points = data['data']['points']
    elif 'points' in data:
        points = data['points']
        
    # 4 & 5. Iterate and generate icospheres
    for pt in points:
        bpy.ops.mesh.primitive_ico_sphere_add(location=(pt["x"], pt["y"], pt["z"]), radius=0.1)
        
    # 6. Print result
    print(f"Render finished. Objects generated: {len(points)}")

if __name__ == "__main__":
    main()
