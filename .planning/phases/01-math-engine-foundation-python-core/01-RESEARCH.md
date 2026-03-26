# Phase 1: Math Engine Foundation (Python Core) - Research

**Phase:** 01
**Goal:** Build the strict mathematical computation engine in Python.

## Domain Overview
The foundation requires an arbitrary-precision math engine in Python to generate Fibonacci sequences. It exposes a standalone API server and exports rich JSON output containing both vector logic and metadata.

## Architectural Decisions

### 1. API Server Framework
To serve the computation engine robustly, **FastAPI** is the modern Python standard. It provides validation via Pydantic and generates open API schemas automatically, perfect for future UI ingestion. We will use `uvicorn` as the ASGI runner.

### 2. Arbitrary Precision Math
As dictated by **D-02**, we must stick to Python's standard library. 
- Python inherently supports arbitrary-precision integers out of the box (`int`). 
- For specific continuous sequences requiring fractions or decimals in later phases, `decimal.Decimal` with a configured context (`decimal.getcontext().prec`) will handle high precision reliably without `gmpy2` C-extension dependencies.

### 3. JSON Output Structure
**D-03** dictates a rich JSON format. The output structure must standardize around:
```json
{
  "metadata": {
    "engine_version": "1.0",
    "sequence_type": "fibonacci",
    "generation_bounds": {"max_n": 100},
    "calculation_time_ms": 15
  },
  "data": {
    "sequence": ["0", "1", "1", "2", "3", "5", ...]
  }
}
```
*Note: Values are serialized as strings to preserve arbitrary precision without Javascript float corruption when parsed by browsers.*

## Implementation Patterns

### Fibonacci Generator
A simple generator pattern will yield Fibonacci values. Since large numbers can block the event loop, computations for very large sequences should eventually run in a thread pool (e.g. `asyncio.to_thread` or standard `ThreadPoolExecutor` within FastAPI).

### File Structure
```
engine/
├── server.py        # FastAPI app entry point
├── math_core/
│   ├── fibonacci.py # Core generator
│   └── precision.py # Decimal config/constants
└── models.py        # Pydantic schemas for JSON D-03
```

## Validation Architecture
- **Unit Testing**: Pytest for math generators ensuring sequence correctness against known arbitrary-precision truth values.
- **Server Testing**: FastAPI TestClient for endpoints.
- **Data Validation**: Pydantic handles input/output validation.
- **Precision Validation**: Assert that large outputs are correctly parsed as strings.
