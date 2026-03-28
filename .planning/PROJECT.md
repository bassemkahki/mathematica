# Mathematica: Art of Universals

## What This Is

A mathematical art project that visualizes universally implicative mathematical philosophies (Fibonacci sequence, primes, abstract infinity) through a heavy-compute Python backend driving headless Blender renders with photorealistic Cycles materials, exported as broadcast-quality 4K landscape animations. These animations are showcased in a Next.js web gallery alongside academic-style white papers rendered from LaTeX via Pandoc with MathJax formula support.

## Core Value

Visually communicating profound mathematical truth through mathematically precise, high-fidelity 4K digital art.

## Requirements

### Validated

- ✓ Arbitrary-precision math engine (Fibonacci, primes, fractals) — v1.0
- ✓ 3D geometrization (Ulam cylinder, L-system fractals) with JSON export — v1.0
- ✓ Headless Blender render pipeline with data-driven Cycles materials — v1.0
- ✓ 4K frame export (3840x2160, 16-bit PNG) with turntable animation — v1.0
- ✓ Pipeline orchestrator (Blender → FFmpeg → H.264 MP4) — v1.0
- ✓ Next.js static web gallery with optimized 4K video playback — v1.0
- ✓ LaTeX white paper integration via Pandoc — v1.0
- ✓ Mobile responsive gallery design — v1.0

### Active

- [ ] Interactive lightweight 3D web previews of mathematical models
- [ ] Downloadable raw datasets/equations for offline use
- [ ] Additional mathematical subjects beyond Fibonacci/primes/fractals
- [ ] User-curated equation collections

### Out of Scope

- Real-time 4K client rendering — Pre-rendering ensures maximum visual fidelity; consumer browsers can't handle the compute
- User uploads / custom math — System is built for curated academic art pieces initially

## Context

Shipped v1.0 with ~1,213 LOC Python + ~453 LOC TypeScript across 119 files.
Tech stack: Python/FastAPI (math engine), Blender/Cycles (renderer), FFmpeg (video encoding), Next.js 16/Tailwind v4 (web gallery), Pandoc (LaTeX → HTML), MathJax 4 (formula rendering).
Three mathematical subjects implemented: Fibonacci spiral, prime Ulam cylinder, L-system fractals.

## Constraints

- **Resolution**: 4K landscape (3840x2160) — The rendering pipeline must support ultra-high-definition exports.
- **Accuracy**: Mathematical rigorousness — The underlying data driving the visuals cannot be faked; it must be demonstrably accurate.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Offline Render + Web Gallery | 4K expressive mathematical art + heavy compute is too demanding for reliable real-time web playback | ✓ Good — enables maximum visual quality |
| Blender via Homebrew (headless) | Need reliable 3D renderer that supports Cycles for photorealistic output | ✓ Good — works well, though Blender 5.1 API breaks required fixes |
| Index-based dynamic coloring | Precise programmatic control from generation engine vs complex shader math | ✓ Good — simple and effective |
| Track-to constraint for camera | Ensures geometry is perfectly framed automatically | ✓ Good — reliable centroid targeting |
| Next.js 16 static export | Maximum performance for gallery, no server needed | ✓ Good — fast builds, easy deployment |
| MathJax 4 CDN | Seamless formula rendering in white papers | ✓ Good — works with Pandoc HTML output |
| Pandoc LaTeX → HTML | Academic paper format with server-side rendering | ✓ Good — clean fragments, no full-page wrappers |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-28 after v1.0 milestone*
