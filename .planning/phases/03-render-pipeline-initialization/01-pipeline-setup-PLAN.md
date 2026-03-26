---
wave: 1
depends_on: []
files_modified: ["scripts/export_data.py", "renderer/render.py", "tests/test_render_pipeline.py"]
autonomous: true
requirements: ["RNDR-01"]
---

# Plan: Phase 3 Render Pipeline Initialization

**Objective**: Set up headless Blender to ingest static mathematical JSON data from the python math engine and successfully spawn default geometric icospheres at exactly the 3D coordinates provided.

## Tasks

<task>
<description>Create utility script to export JSON data from engine to disk</description>
<read_first>
- `engine/server.py`
- `engine/models.py`
</read_first>
<action>
Create `scripts/export_data.py`. Inside this script:
1. Fetch `http://127.0.0.1:8000/api/v1/sequences/primes?n=100` using the `urllib.request` standard library module.
2. Read the response body and decode it as a JSON string.
3. Write the exact JSON dictionary out to a file at `data/primes.json`.
4. Ensure the `data/` directory exists by using `os.makedirs('data', exist_ok=True)`.
5. Support a command line argument `--type fractal` which instead fetches `http://127.0.0.1:8000/api/v1/sequences/fractal?iterations=3` and writes to `data/fractal.json`.
</action>
<acceptance_criteria>
- File `scripts/export_data.py` exists
- Running `python scripts/export_data.py --type primes` exits 0 and creates `data/primes.json`
- `data/primes.json` contains `"points":[`
</acceptance_criteria>
</task>

<task>
<description>Create headless Blender renderer script to ingest JSON data</description>
<read_first>
- `.planning/phases/03-render-pipeline-initialization/03-CONTEXT.md`
- `.planning/phases/03-render-pipeline-initialization/03-RESEARCH.md`
</read_first>
<action>
Create `renderer/render.py`. Inside this script:
1. Delete all default objects (Cube, Camera, Light) using `bpy.ops.object.select_all(action='SELECT')` and `bpy.ops.object.delete(use_global=False)`.
2. Extract the `--input` command line argument using `sys.argv` (ignoring arguments before `--`).
3. Open and parse the JSON file specified by `--input`.
4. Iterate over the dictionaries inside the `data['points']` array. Each dictionary has `x`, `y`, and `z` keys.
5. For each dictionary, call `bpy.ops.mesh.primitive_ico_sphere_add(location=(pt["x"], pt["y"], pt["z"]), radius=0.1)`.
6. Print `"Render finished. Objects generated: X"` where X is the number of points processed.
</action>
<acceptance_criteria>
- File `renderer/render.py` exists
- Script imports `bpy` and `sys` and `json`
- Executing `blender --background --python renderer/render.py -- --input data/primes.json` exits status 0
- Standard output from the blender execution contains "Render finished."
</acceptance_criteria>
</task>

<task>
<description>Create verification tests for Phase 3 pipeline</description>
<read_first>
- `scripts/export_data.py`
- `renderer/render.py`
</read_first>
<action>
Create `tests/test_render_pipeline.py`. Inside this pytest file:
1. Write `test_export_script_produces_file` which invokes `subprocess.run(["python", "scripts/export_data.py", "--type", "primes"])` and asserts that `os.path.exists("data/primes.json")` is True. Let it use a `pytest.fixture(autouse=True)` to clean up the `data/` directory before testing.
2. Write `test_blender_headless_ingestion` which invokes `subprocess.run(["blender", "--background", "--python", "renderer/render.py", "--", "--input", "data/primes.json"], capture_output=True, text=True)`. Assert that the returncode is 0 and that the string "Render finished. Objects generated:" is in `result.stdout`.
</action>
<acceptance_criteria>
- File `tests/test_render_pipeline.py` exists
- File defines `test_export_script_produces_file`
- File defines `test_blender_headless_ingestion`
</acceptance_criteria>
</task>

## Verification Criteria

### Must Haves
- The JSON output from the FastAPI engine must be persisted to the `data/` folder verbatim.
- The Blender script must be runnable from CLI using `--background`.
- The icospheres must be spawned exactly corresponding to the JSON input arrays.
- Validation scripts must assert these processes pass.

## PLANNING COMPLETE
