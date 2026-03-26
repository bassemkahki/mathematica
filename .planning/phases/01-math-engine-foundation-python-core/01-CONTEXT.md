# Phase 1: Math Engine Foundation (Python Core) - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the strict mathematical computation engine in Python to generate arbitrary-precision sequences (like Fibonacci) and export them to structured JSON format. Web gallery UI and 3D visual rendering are out of scope for this phase.

</domain>

<decisions>
## Implementation Decisions

### Execution Interface
- **D-01:** Standalone API server. The Python engine will host its own local server that can be triggered (e.g. by future frontend or render pipelines) to compute sequences and generate the JSON files.

### Dependencies Strategy
- **D-02:** Standard library only. Rely on Python's built-in arbitrary precision for integers and the `decimal`/`fractions` modules to avoid cross-platform installation issues with C-extensions like `gmpy2`.

### JSON Output Structure
- **D-03:** Rich JSON documents. The exported output will include the computed mathematical data (e.g. sequences, point coordinates) alongside rich metadata (e.g. equations, generation bounds, calculation time, step counts).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Architecture
- `.planning/PROJECT.md` — Defines the overall project vision (offline renderer + high precision core)
- `.planning/REQUIREMENTS.md` — Defines MATH-01, MATH-02 requirements that this phase must fulfill

</canonical_refs>
