# Phase 2: Advanced Geometrization & Infinity Computation - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Expanding the engine to compute spatial vector layouts and point clouds for abstract concepts (Primes, Infinity).

</domain>

<decisions>
## Implementation Decisions

### Primes Mapping Layout
- **D-01:** Map primes using an Ulam spiral projected onto a 3D cylinder.

### Infinity/Fractal Strategy
- **D-02:** Use L-systems to compute fractal geometry, leveraging string-based structures using standard libraries.

### Vector Coordinate Structure
- **D-03:** Format 3D point data in the JSON response using structured dictionaries (e.g., `{"x": x, "y": y, "z": z}`).

### Data Scale and Bounds
- **D-04:** Control generation bounds using a maximum points count (N), extending existing `generation_bounds["max_n"]` logic.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Architecture
- `.planning/PROJECT.md` — Defines overall project vision
- `.planning/REQUIREMENTS.md` — Defines MATH-03, MATH-04, MATH-05 requirements for Phase 2

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `engine/models.py`: existing `Metadata` and `Data` API response models.
- `engine/server.py`: existing FastAPI application setup.

### Established Patterns
- Standalone API server running locally.
- Use Python's built-in standard libraries without heavy numeric extensions.
- Structured JSON with separated data and metadata bounds.

### Integration Points
- Add new sequence generation routing endpoints in `engine/server.py`.
- Enhance or add new spatial payload types in `engine/models.py`.
</code_context>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches
</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope
</deferred>

---

*Phase: 02-advanced-geometrization-infinity-computation*
*Context gathered: 2026-03-26*
