---
title: "Phase 1: Math Engine Foundation (Python Core)"
wave: 1
depends_on: []
files_modified: ["engine/models.py", "engine/math_core/fibonacci.py", "engine/math_core/precision.py", "engine/server.py", "requirements.txt"]
requirements: ["MATH-01", "MATH-02"]
autonomous: true
---

# Phase 1: Math Engine Foundation (Python Core)

<objective>
Build a standalone FastAPI Python engine that calculates arbitrary-precision mathematical sequences (specifically Fibonacci) and serves them as robust JSON arrays via an HTTP endpoint.
</objective>

<tasks>
## Task 1: Setup API Server Foundation & Schemas
<read_first>
- `.planning/phases/01-math-engine-foundation-python-core/01-CONTEXT.md` (for JSON structure)
</read_first>
<action>
1. Create `requirements.txt` with `fastapi` and `uvicorn`.
2. Create `engine/models.py`. Define Pydantic models for the JSON response matching D-03 exactly:
   - `Metadata` model with `engine_version`, `sequence_type`, `generation_bounds` (dict), and `calculation_time_ms` (float).
   - `Data` model with `sequence` (list of strings).
   - `SequenceResponse` model containing `metadata` and `data`.
3. Create `engine/server.py` and instantiate a basic FastAPI app.
   - Add a GET `/health` endpoint returning `{"status": "ok"}`.
</action>
<acceptance_criteria>
- `requirements.txt` contains `fastapi` and `uvicorn`.
- `engine/models.py` contains `class SequenceResponse(BaseModel):`
- `python -m pytest` or manual curl to `http://localhost:8000/health` returns `{"status": "ok"}`
</acceptance_criteria>

## Task 2: Implement Arbitrary Precision Math Core
<read_first>
- `engine/models.py`
</read_first>
<action>
1. Create `engine/math_core/precision.py`:
   - Initialize decimal precision to a high default e.g., `import decimal; decimal.getcontext().prec = 1000`.
2. Create `engine/math_core/fibonacci.py`:
   - Implement `def generate_fibonacci(n: int) -> list[str]:` that uses arbitrary precision integers to calculate the sequence up to `n` elements.
   - The function must cast all integers to strings before returning to preserve arbitrary precision.
</action>
<acceptance_criteria>
- `engine/math_core/fibonacci.py` contains `def generate_fibonacci(`
- Return list must contain strictly string elements representing the sequence.
- Manually testing `generate_fibonacci(5)` returns `["0", "1", "1", "2", "3"]`.
</acceptance_criteria>

## Task 3: Expose Sequence Generation Endpoint
<read_first>
- `engine/server.py`
- `engine/math_core/fibonacci.py`
- `engine/models.py`
</read_first>
<action>
1. Update `engine/server.py`.
2. Add a GET `/api/v1/sequences/fibonacci` endpoint.
   - Accepts query param `n: int`.
   - Records start time using `time.perf_counter()`.
   - Calls `generate_fibonacci(n)`.
   - Records end time and calculates `calculation_time_ms`.
   - Constructs and returns a `SequenceResponse` object.
   - Metadata values: `engine_version="1.0"`, `sequence_type="fibonacci"`, `generation_bounds={"max_n": n}`.
</action>
<acceptance_criteria>
- `engine/server.py` contains `@app.get("/api/v1/sequences/fibonacci")`
- Curl to `/api/v1/sequences/fibonacci?n=100` returns the expected JSON structure with 100 stringified numbers.
</acceptance_criteria>
</tasks>

<verification>
To verify Phase 1 is complete:
1. `pip install -r requirements.txt`
2. `python -m uvicorn engine.server:app --reload &`
3. `curl "http://localhost:8000/api/v1/sequences/fibonacci?n=100" > output.json`
4. Inspect `output.json`. 
   - Ensure `metadata.calculation_time_ms` exists.
   - Ensure `data.sequence` length is 100.
   - Ensure every element in `data.sequence` is a string to prevent float corruption.
   - Ensure `data.sequence[-1]` is the correct large number.
</verification>

<must_haves>
- FastAPI integration for the server.
- String output for math sequence lists to preserve precision.
- Valid JSON schema aligning with Document D-03.
</must_haves>
