import time
from fastapi import FastAPI
from engine.models import SequenceResponse, Metadata, Data, Point3D
from engine.math_core.fibonacci import generate_fibonacci
from engine.math_core.primes import generate_ulam_cylinder
from engine.math_core.fractals import generate_lsystem, evaluate_lsystem_3d

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/sequences/fibonacci", response_model=SequenceResponse)
def get_fibonacci(n: int):
    start_time = time.perf_counter()
    
    # Generate sequence
    sequence = generate_fibonacci(n)
    
    end_time = time.perf_counter()
    calculation_time_ms = (end_time - start_time) * 1000.0

    return SequenceResponse(
        metadata=Metadata(
            engine_version="1.0",
            sequence_type="fibonacci",
            generation_bounds={"max_n": n},
            calculation_time_ms=calculation_time_ms
        ),
        data=Data(
            sequence=sequence
        )
    )

@app.get("/api/v1/sequences/primes", response_model=SequenceResponse)
def get_primes(n: int):
    start_time = time.perf_counter()
    
    raw_points = generate_ulam_cylinder(n)
    points = [Point3D(**p) for p in raw_points]
    
    end_time = time.perf_counter()
    calculation_time_ms = (end_time - start_time) * 1000.0

    return SequenceResponse(
        metadata=Metadata(
            engine_version="1.0",
            sequence_type="primes",
            generation_bounds={"max_n": n},
            calculation_time_ms=calculation_time_ms
        ),
        data=Data(
            sequence=[],
            points=points
        )
    )

@app.get("/api/v1/sequences/fractal", response_model=SequenceResponse)
def get_fractal(iterations: int):
    start_time = time.perf_counter()
    
    lsys = generate_lsystem(iterations)
    raw_points = evaluate_lsystem_3d(lsys)
    points = [Point3D(**p) for p in raw_points]
    
    end_time = time.perf_counter()
    calculation_time_ms = (end_time - start_time) * 1000.0

    return SequenceResponse(
        metadata=Metadata(
            engine_version="1.0",
            sequence_type="fractal",
            generation_bounds={"iterations": iterations},
            calculation_time_ms=calculation_time_ms
        ),
        data=Data(
            sequence=[],
            points=points
        )
    )
