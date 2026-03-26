# Phase 3: Render Pipeline Initialization - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-26
**Phase:** 03-render-pipeline-initialization
**Areas discussed:** Renderer Choice, Data Ingestion, Geometry Representation, Renderer Invocation
**Mode:** --batch (4 questions in one turn)

---

## Renderer Choice

| Option | Description | Selected |
|--------|-------------|----------|
| Blender (headless) | Battle-tested 3D renderer, Python-scriptable, wide format support, natural fit for 4K offline renders | ✓ |
| Three.js (Node, headless) | Web-native, lighter to set up, less mature for 4K offline export | |

**User's choice:** Blender (headless)
**Notes:** Recommended for the 4K animation goal — selected without hesitation.

---

## Data Ingestion

| Option | Description | Selected |
|--------|-------------|----------|
| Pre-export JSON files to disk | Engine saves `.json` files; renderer reads directly — no live server dependency | ✓ |
| Call live API at render time | Renderer calls `localhost:8000/api/v1/...` — dynamic but requires server running | |

**User's choice:** Pre-export JSON files to disk
**Notes:** Simpler, decoupled approach preferred.

---

## Geometry Representation

| Option | Description | Selected |
|--------|-------------|----------|
| Sphere/icosphere | Smooth, scalable, natural representation of a mathematical point in space | ✓ |
| Point/vertex cloud | Raw points, minimal geometry, fast | |
| Agent's Discretion | Let planner choose based on what renders cleanly at 4K | |

**User's choice:** Sphere/icosphere
**Notes:** Icosphere specifically preferred for its geometric smoothness.

---

## Renderer Invocation

| Option | Description | Selected |
|--------|-------------|----------|
| Standalone CLI script | e.g. `blender --python render.py -- --input data.json` — clean separation | |
| Called from FastAPI server | `/render` endpoint triggers Blender as subprocess | |
| Agent's Discretion | Let planner decide best invocation mechanism | ✓ |

**User's choice:** Agent's Discretion
**Notes:** Priority is clean decoupling between engine and renderer; invocation mechanism left to planner.

---

## Agent's Discretion

- Renderer invocation mechanism — how Blender is triggered (CLI, subprocess, Makefile, etc.)

## Deferred Ideas

None
