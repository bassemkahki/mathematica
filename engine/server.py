import time
from fastapi import FastAPI
from engine.models import SequenceResponse, Metadata, Data
from engine.math_core.fibonacci import generate_fibonacci

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
