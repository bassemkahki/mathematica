---
phase: 6
slug: web-gallery-white-paper-integration
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-27
---

# Phase 6 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | jest / playwright (e2e) |
| **Config file** | web/jest.config.ts (Wave 0 installs) |
| **Quick run command** | `cd web && npm test -- --passWithNoTests` |
| **Full suite command** | `cd web && npm test` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `cd web && npm test -- --passWithNoTests`
- **After every plan wave:** Run `cd web && npm test`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 06-01-01 | 01 | 0 | WEB-01 | build | `cd web && npm run build` | ❌ W0 | ⬜ pending |
| 06-01-02 | 01 | 0 | WEB-01 | unit | `cd web && npm test -- --passWithNoTests` | ❌ W0 | ⬜ pending |
| 06-02-01 | 02 | 1 | WEB-02 | build | `cd web && npm run build 2>&1 \| grep -v error` | ✅ | ⬜ pending |
| 06-03-01 | 03 | 1 | WEB-03 | unit | `cd web && npm test -- --testPathPattern=gallery` | ❌ W0 | ⬜ pending |
| 06-04-01 | 04 | 2 | WEB-04 | build | `cd web && npm run build && ls out/` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `web/` directory scaffolded with Next.js 16 + Tailwind CSS 4
- [ ] `web/package.json` — contains jest, @testing-library/react
- [ ] `web/jest.config.ts` — test configuration
- [ ] `pandoc` installed via `brew install pandoc`
- [ ] `web/public/videos/` and `web/public/posters/` directories created
- [ ] `web/scripts/prebuild.sh` — asset copy script stub

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 4K video smooth playback | WEB-02 | Requires browser and display | Open localhost:3000, play a video, confirm no lag |
| Math rendering correctness | WEB-03 | Visual check of LaTeX formulas | Open white paper page, verify equations render |
| Static export deployability | WEB-04 | Requires hosting target | `npx serve out/` and verify all routes load |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
