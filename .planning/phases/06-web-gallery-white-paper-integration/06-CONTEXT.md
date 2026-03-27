# Phase 6: Web Gallery & White Paper Integration - Context

**Gathered:** 2026-03-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the web presentation layer: a Next.js static site that showcases pre-rendered 4K math art animations alongside LaTeX-authored academic white papers. Videos are pre-rendered H.264 MP4 — not real-time. This phase covers the site itself; hosting infrastructure and CI/CD deployment pipelines are out of scope.
</domain>

<decisions>
## Implementation Decisions

### Framework
- **D-01:** Use **Next.js with full static export** (`next export`) — outputs pure HTML/CSS/JS with no Node.js server dependency. Can be deployed to any static host (S3, GitHub Pages, Netlify, own server) without a runtime.

### Video Delivery
- **D-02:** **Poster frame first, explicit user-triggered playback.** Each artwork displays a static 4K poster image by default. A visible play control requires the user to deliberately start the video. This prevents multiple large video buffers loading simultaneously on the single-scroll page, satisfying WEB-02's optimized loading requirement.

### White Paper Format
- **D-03:** Papers are **authored in LaTeX** and **compiled to HTML via Pandoc**. LaTeX is the canonical source; Pandoc produces the embedded HTML. Math equations use **MathJax (CDN)** for in-browser rendering — highest fidelity for complex notation, acceptable CDN overhead.

### Gallery Layout
- **D-04:** **Single-scroll showcase.** All artworks stacked on one page, full-width, with video and white paper side-by-side per artwork. No separate index or navigation — one continuous cinematic experience. On mobile, video stacks above paper (WEB-04 responsive requirement).

### Claude's Discretion
- Specific hosting target (S3 bucket, GitHub Pages, Netlify free tier, etc.)
- Video `<video>` element controls styling and poster-to-play transition animation
- Pandoc compilation step (Makefile target, npm script, or manual pre-build)
- Exact responsive breakpoints for mobile stacking
- CSS/styling approach (Tailwind, CSS modules, or plain CSS)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — WEB-01 (static front-end), WEB-02 (4K video playback with bandwidth optimization), WEB-03 (white paper framework side-by-side with video), WEB-04 (mobile responsive design)

### Project Architecture
- `.planning/PROJECT.md` — Core value: offline pre-rendered 4K art; real-time rendering explicitly out of scope

### Video Assets
- `renders/` — Output directory from Phase 5 pipeline; contains `frames/` (PNG sequences) and `output/` (MP4 files) subdirectories

No external ADRs or design specs — requirements fully captured in decisions above.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `renders/output/` — 4K H.264 MP4 files produced by Phase 5 pipeline; these are the video assets the gallery embeds
- `renders/test_frames/` — PNG stills (e.g. `frame_0001.png`); can be used as poster frames

### Established Patterns
- Stack is currently pure Python — this phase introduces the first JavaScript/web code in the project
- No existing component library, design system, or CSS framework established; Claude has full discretion

### Integration Points
- The gallery consumes pre-built artifacts from `renders/`; there is no live API call or server-side data fetch at render time
- Pandoc compilation of `.tex` → `.html` is a build-time step that produces static HTML fragments to embed in Next.js pages
</code_context>

<specifics>
## Specific Ideas

No specific UI references provided — open to standard approaches consistent with the academic/mathematical art aesthetic.
</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.
</deferred>

---

*Phase: 06-web-gallery-white-paper-integration*
*Context gathered: 2026-03-27*
