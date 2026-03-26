# Phase 4: Aesthetic Surfacing & Materials - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement the expressive digital art shaders, textures, and materials bounding the underlying mathematical forms. Setup photorealistic materials driven by sequence data, configure studio HDRI lighting, and define camera framing options.
</domain>

<decisions>
## Implementation Decisions

### Visual Style (Shading)
- **D-01:** Photorealistic. Use realistic materials (e.g. glass, metal, emissive) to complement the 4K offline rendering pipeline established in Phase 3.

### Material Assignment
- **D-02:** Data-driven logic. Material properties (such as color or emission) will be driven by the math sequence data (e.g., coordinate position, sequence index) to visually communicate mathematical properties.

### Lighting Setup
- **D-03:** Studio stylized HDRI lighting.

### Camera Framing
- **D-04:** Both options supported. The script should be able to render a static wide shot capturing the entire data bounds as well as a dynamic/animated camera fly-through.
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Architecture
- `.planning/PROJECT.md` — Overall vision: offline pre-rendered 4K art, accuracy-first
- `.planning/REQUIREMENTS.md` — RNDR-02: Apply abstract geometry and fractal shaders/materials to mathematical dataset

### Integration Contract
- `renderer/render.py` — The existing Blender headless ingestion script to build upon.
</canonical_refs>
