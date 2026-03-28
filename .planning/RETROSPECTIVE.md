# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.0 — MVP

**Shipped:** 2026-03-28
**Phases:** 6 | **Plans:** 11

### What Was Built
- Arbitrary-precision math engine (FastAPI) with Fibonacci, prime Ulam cylinder, and L-system fractal computation
- Headless Blender render pipeline with photorealistic Cycles materials, HDRI lighting, and turntable camera
- 4K export automation (3840x2160 16-bit PNG → H.264 MP4 via FFmpeg)
- Next.js web gallery with optimized video playback, Pandoc white papers, and MathJax formulas

### What Worked
- Fast 3-day timeline from project init to shipped gallery — clear phase decomposition kept momentum
- Math engine → renderer → web layering meant each phase built cleanly on the last
- Headless Blender approach avoided GUI complexity entirely
- Static Next.js export eliminated server deployment concerns

### What Was Inefficient
- Requirement checkbox tracking fell behind during execution — 9/13 requirements weren't checked off despite being complete
- Traceability table had incorrect phase mappings from initial definition (e.g., MATH-03 mapped to Phase 1 but built in Phase 2)
- Blender 5.1 API breaks required debugging after initial render pipeline was working — could have pinned version
- Multiple debug sessions for render pipeline bugs (7 compounding issues in one session)

### Patterns Established
- Pipeline orchestrator pattern (scripts/run_pipeline.py) — single command runs full render pipeline
- Pandoc LaTeX → HTML fragment build step integrated into Next.js build
- Data-driven material assignment via spatial index coloring

### Key Lessons
1. Update requirement checkboxes during phase transitions, not just at milestone completion — prevents bookkeeping debt
2. Pin major tool versions (Blender) to avoid API break surprises mid-milestone
3. The math engine API-first approach (JSON coordinates) cleanly decoupled computation from rendering — keep this pattern

### Cost Observations
- Model mix: primarily opus for planning/execution
- Notable: 6 phases completed in 3 days — high velocity for a greenfield project

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Phases | Plans | Key Change |
|-----------|--------|-------|------------|
| v1.0 | 6 | 11 | Initial project — established pipeline pattern |

### Top Lessons (Verified Across Milestones)

1. (First milestone — lessons above will be verified in v1.1+)
