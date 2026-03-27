# Phase 6: Web Gallery & White Paper Integration - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions captured in CONTEXT.md — this log preserves the discussion.

**Date:** 2026-03-27
**Phase:** 06-web-gallery-white-paper-integration
**Mode:** discuss (batch)
**Areas discussed:** Framework & Deployment, Video Delivery, White Paper Format, Gallery Layout, Math Rendering

## Questions & Answers

### Batch 1: Core decisions

| Area | Question | Options Presented | User Selection |
|------|----------|-------------------|----------------|
| Framework & Deployment | Deployment target for Next.js | A) Vercel/Netlify (managed), B) Self-hosted static export, C) Self-hosted Node server | **B — Self-hosted static export** |
| Video Delivery | How should 4K files load? | A) Direct embed + lazy loading, B) Adaptive streaming (HLS/DASH), C) Poster frame + explicit play toggle | **C — Poster frame + explicit play toggle** |
| White Paper Format | How are papers authored and rendered? | A) MDX files, B) LaTeX → HTML via Pandoc, C) Plain Markdown + remark | **B — LaTeX → HTML via Pandoc** |
| Gallery Layout | How is the site organized? | A) Grid index + individual artwork pages, B) Single-scroll showcase, C) Dedicated sections | **B — Single-scroll showcase** |

### Follow-up: Math rendering

| Area | Question | Options Presented | User Selection |
|------|----------|-------------------|----------------|
| Math Rendering | How should Pandoc render LaTeX math in HTML? | A) MathJax (CDN), B) KaTeX (local), C) Pre-rendered SVG/static | **A — MathJax (CDN)** |

## Corrections Made

No corrections — all decisions confirmed on first selection.

## Deferred Ideas

None surfaced during discussion.
