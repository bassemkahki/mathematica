# Phase 02 Research: Advanced Geometrization & Infinity Computation

## 1. Domain Investigation
**Primes & Ulam Spiral (3D Cylinder)**
- **Prime Generation**: A fast Sieve of Eratosthenes algorithm is needed to generate up to `N` primes.
- **Ulam Spiral 3D Projection**: A standard Ulam spiral maps integers to 2D coordinates `(u, v)`. To project this onto a 3D cylinder, we wrap the `(u, v)` coordinates around a fixed radius `R`. For example, `x = R * cos(u/R)`, `z = R * sin(u/R)`, `y = v`. This perfectly meets the contextual requirement of "Ulam spiral projected onto a 3D cylinder".
- **Fractals (L-System)**: L-systems represent fractals through string rewriting. The context explicitly mentions string-based L-systems. We start with an Axiom (e.g., `F`), and apply Rules (e.g., `F -> F+F--F+F`). To generate 3D point clouds, a 3D turtle graphics interpreter tracks state `(x, y, z, pitch, yaw, roll)` and adds points to a list based on the resulting string.

## 2. Technical Approach
**Data Models** (`engine/models.py`)
- The existing `Data` model only has `sequence: List[str]`.
- We need to support the required JSON format: `{"x": x, "y": y, "z": z}`.
- Introduce `Point3D(BaseModel): x: float; y: float; z: float`.
- Update `Data` to handle points: `points: List[Point3D] = []` (or make it optional/union).

**Endpoint Routing** (`engine/server.py`)
- Create `GET /api/v1/sequences/primes` (accepts `n: int`).
- Create `GET /api/v1/sequences/fractal` (accepts `iterations: int` or `n: int`).

**Math Core Modules**
- Create `engine/math_core/primes.py`: Contains the Sieve of Eratosthenes and the 3D Ulam projection logic.
- Create `engine/math_core/fractals.py`: Contains L-system expansion and 3D coordinate translation.

## 3. Libraries and Patterns
- Adhere strictly to D-02 / Code Context: **Use Python's built-in standard libraries without heavy numeric extensions**. We cannot use `numpy` or `scipy`.
- Python's `math` module provides `sin`, `cos`, and `radians` needed for geometric projections.
- Rely on `FastAPI` and `Pydantic` as already established in the architecture.

## 4. Dependencies
- No new external dependencies required.

## Validation Architecture
- **Unit Tests**: We need new tests in a `tests/` directory.
  - `test_primes.py`: Verify prime generation accuracy (e.g., exactly 25 primes under 100) and coordinate non-nullness.
  - `test_fractals.py`: Verify L-system string rewriting depth and correct 3D point bounding.
- **Endpoint Tests**: Use FastAPI `TestClient` to verify HTTP 200 responses, ensuring `calculation_time_ms` is returned and `generation_bounds["max_n"]` matches the requested points.
- **Data Shape assertions**: Validate that the JSON structure exactly matches the `{"x": x, "y": y, "z": z}` form as decided in D-03.
