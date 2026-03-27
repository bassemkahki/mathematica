# Phase 6: Web Gallery & White Paper Integration - Research

**Researched:** 2026-03-27
**Domain:** Next.js 16 static export, Tailwind CSS 4, Pandoc LaTeX-to-HTML, MathJax 4, HTML5 video optimization
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** Use **Next.js with full static export** (`output: 'export'` in next.config.ts) — outputs pure HTML/CSS/JS with no Node.js server dependency.
- **D-02:** **Poster frame first, explicit user-triggered playback.** `preload="none"` with poster PNG. Play overlay requires deliberate user action. Prevents simultaneous 4K buffer loading.
- **D-03:** Papers authored in **LaTeX**, compiled to HTML via **Pandoc**. Math equations use **MathJax (CDN)** — highest fidelity for complex notation.
- **D-04:** **Single-scroll showcase.** All artworks stacked on one page, full-width, video + white paper side-by-side per artwork. No separate index. On mobile, video stacks above paper.

### Claude's Discretion

- Specific hosting target (S3, GitHub Pages, Netlify, etc.)
- Video `<video>` element controls styling and poster-to-play transition animation
- Pandoc compilation step (Makefile target, npm script, or manual pre-build)
- Exact responsive breakpoints for mobile stacking
- CSS/styling approach (Tailwind, CSS modules, or plain CSS)

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| WEB-01 | Build a static or SSR web gallery front-end | D-01 verified: `output: 'export'` in next.config.ts produces HTML/CSS/JS served from any static host. `next build` generates `out/` directory. |
| WEB-02 | Implement 4K video playback with optimized loading/bandwidth handling | D-02 verified: `<video preload="none" poster="...">` + programmatic play via `useRef`. No buffering until user triggers play. `'use client'` component required for DOM interaction. |
| WEB-03 | Support architectural framework for accompanying mathematical white papers side-by-side with video content | D-03 verified: Pandoc fragment output + `dangerouslySetInnerHTML` in Server Component. MathJax 4 CDN via `<script defer>` in root layout. |
| WEB-04 | Ensure mobile responsive design for reading papers and browsing gallery (video scales down gracefully) | D-04 verified: Tailwind responsive breakpoints (`lg:grid-cols-2`, single column below 1024px), `aspect-ratio: 16/9` wrapper preserves video ratio. |
</phase_requirements>

---

## Summary

This phase introduces the first JavaScript/web code into a previously pure-Python project. The stack is Next.js 16 (static export), Tailwind CSS 4, MathJax 4, and Pandoc 3.9 for LaTeX-to-HTML compilation. All decisions are locked — research confirms they are sound and mutually compatible.

Next.js 16 is the current stable release (published 2025-10-21, latest patch 16.2.1 as of 2026-03-20). The `output: 'export'` configuration produces a static `out/` directory compatible with any static host. Turbopack is now the default bundler. The `next export` CLI command was removed in v14 — the correct mechanism is `output: 'export'` in config plus `next build`.

Tailwind CSS 4 (current: 4.2.2) uses a fundamentally different setup than v3: no `tailwind.config.js`, no `@tailwind base/components/utilities` directives. Instead: install `tailwindcss` + `@tailwindcss/postcss`, add `@import 'tailwindcss'` to global CSS, configure `postcss.config.mjs`. This is a critical breaking change from the v3 pattern most tutorials show.

Pandoc is not installed on this machine (brew shows 3.9.0.2 available, not installed). It must be installed as a prerequisite before the build step can run. The build step produces HTML fragments (omit `--standalone`), math delimiters are preserved as `\(...\)` / `\[...\]`, and MathJax 4 CDN handles in-browser rendering.

**Primary recommendation:** Scaffold the Next.js 16 app with `npx create-next-app@latest` (defaults: TypeScript, Tailwind, ESLint, App Router), add `output: 'export'` + `images: { unoptimized: true }` to `next.config.ts`, install Pandoc via brew, and wire the Pandoc pre-build script per the UI-SPEC contract.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| next | 16.2.1 | React framework with static export | D-01 locked; current stable release |
| react | 19.2.x | UI component model | Peer dependency of Next.js 16 |
| react-dom | 19.2.x | DOM renderer | Peer dependency |
| typescript | 6.0.2 | Type safety | Default in `create-next-app`; Next.js 16 requires 5.1+ |
| tailwindcss | 4.2.2 | Utility-first CSS | Discretion area; UI-SPEC resolved as Tailwind; default in create-next-app |
| @tailwindcss/postcss | 4.2.2 | Tailwind v4 PostCSS integration | Required for Tailwind v4; replaces tailwindcss/nesting |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pandoc (CLI) | 3.9.0.2 | LaTeX .tex → HTML fragment conversion | Build-time pre-step; must be installed via brew |
| MathJax (CDN) | 4.1.1 | Browser-side TeX math rendering | Loaded via `<script defer>` in root layout; no npm install needed |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| MathJax 4 CDN | KaTeX (local npm) | KaTeX is faster but less comprehensive for advanced LaTeX; MathJax locked by D-03 |
| Tailwind CSS 4 | Tailwind CSS 3 | v3 requires `tailwind.config.js`; v4 is simpler setup with `@import 'tailwindcss'` and no config file required for basic use |
| Next.js static export | Plain HTML/JS | Next.js provides component model, TypeScript, build tooling; locked by D-01 |

### Installation

```bash
# Create Next.js app (from project root — creates web/ subdirectory)
npx create-next-app@latest web --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --yes

# Install Pandoc (prerequisite for build)
brew install pandoc

# Verify Pandoc
pandoc --version
```

**Version verification (confirmed 2026-03-27):**

| Package | Registry Version | Published |
|---------|-----------------|-----------|
| next | 16.2.1 | 2026-03-20 |
| tailwindcss | 4.2.2 | 2026-03-xx |
| @tailwindcss/postcss | 4.2.2 | 2026-03-xx |
| react | 19.2.4 | 2026-03-xx |
| typescript | 6.0.2 | 2026-03-xx |
| mathjax (npm) | 4.1.1 | 2026-02-19 |
| pandoc (brew) | 3.9.0.2 | 2026-02-xx |

---

## Architecture Patterns

### Recommended Project Structure

```
web/                          # Next.js project root (sibling to renders/, engine/, etc.)
├── src/
│   ├── app/
│   │   ├── layout.tsx        # Root layout: MathJax CDN script, Google Fonts link, globals.css
│   │   ├── page.tsx          # GalleryPage: single-scroll, maps artworks data
│   │   └── globals.css       # @import 'tailwindcss'; custom CSS vars
│   └── components/
│       ├── ArtworkSection.tsx  # Full-width section: VideoPlayer + PaperColumn grid
│       ├── VideoPlayer.tsx     # 'use client' — poster + play overlay + native controls
│       ├── PaperColumn.tsx     # dangerouslySetInnerHTML for Pandoc HTML fragment
│       └── SiteHeader.tsx      # Display title + tagline
├── public/
│   ├── videos/               # Symlink or copy of renders/output/*.mp4
│   ├── posters/              # Symlink or copy of renders/test_frames/*.png
│   └── papers/               # Pandoc-compiled .html fragments (prebuild output)
├── papers/                   # LaTeX source files (.tex)
├── next.config.ts
├── postcss.config.mjs
├── tsconfig.json
└── package.json
```

**Note on asset paths:** Video MP4 files and poster PNGs must be accessible from `public/` at build time for static export. The plan must include a step to copy (or symlink) from `../renders/` into `web/public/`. Static export does not support dynamic server-side file system reads.

### Pattern 1: Next.js Static Export Configuration

**What:** Set `output: 'export'` in next.config.ts. Add `images: { unoptimized: true }` because the default Next.js Image Optimization API is server-side and incompatible with static export.

**When to use:** Always for this project (D-01 locked).

```typescript
// Source: https://nextjs.org/docs/app/guides/static-exports (version 16.2.1, 2026-03-25)
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'export',
  images: {
    unoptimized: true,  // Required for static export — no Image Optimization API
  },
  // Optional: trailingSlash: true for static hosts that require index.html
}

export default nextConfig
```

**Build command:** `next build` — produces `web/out/` containing all static assets.

### Pattern 2: Tailwind CSS 4 Setup

**What:** Tailwind v4 dropped config-file-based setup. PostCSS plugin is `@tailwindcss/postcss`, not `tailwindcss/nesting` or `autoprefixer`.

**Critical difference from v3:** No `tailwind.config.js`, no `@tailwind base/components/utilities`. Use `@import 'tailwindcss'` in global CSS.

```javascript
// Source: https://nextjs.org/docs/app/getting-started/css (version 16.2.1, 2026-03-25)
// postcss.config.mjs
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
}
```

```css
/* src/app/globals.css */
@import 'tailwindcss';

/* Custom CSS variables for design system */
:root {
  --color-dominant: #0A0A0A;
  --color-secondary: #141414;
  --color-accent: #E8E8E8;
  --color-prose: #C8C8C8;
}
```

### Pattern 3: VideoPlayer Component (Client Component)

**What:** The `<video>` element requires DOM interaction for programmatic play; must be a Client Component. Poster-first pattern: `preload="none"`, overlay play button, `useRef` for programmatic `video.play()`.

**Why 'use client':** Server Components cannot use `useRef`, `useState`, or attach event handlers.

```typescript
// Source: Next.js official video guide (nextjs.org/docs/app/guides/videos, 2026-03-25)
// Pattern adapted from official recommendations
'use client'

import { useRef, useState } from 'react'

interface VideoPlayerProps {
  src: string
  poster: string
  title: string
}

export function VideoPlayer({ src, poster, title }: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [playing, setPlaying] = useState(false)
  const [error, setError] = useState(false)

  function handlePlay() {
    if (!videoRef.current) return
    videoRef.current.play()
    setPlaying(true)
  }

  return (
    <div className="relative w-full" style={{ aspectRatio: '16/9' }}>
      <video
        ref={videoRef}
        src={src}
        poster={poster}
        preload="none"
        controls={playing}
        aria-label={title}
        onError={() => setError(true)}
        className="w-full h-full object-cover"
      />
      {!playing && !error && (
        <button
          onClick={handlePlay}
          aria-label="Play artwork"
          className="absolute inset-0 flex items-center justify-center"
          style={{ minWidth: '44px', minHeight: '44px' }}
        >
          {/* SVG play icon */}
        </button>
      )}
      {error && (
        <p className="italic" style={{ color: '#888', fontSize: '16px' }}>
          Video unavailable — file may still be rendering.
        </p>
      )}
    </div>
  )
}
```

### Pattern 4: Pandoc Build Step and PaperColumn

**What:** Pandoc runs as a pre-build npm script. Output is an HTML fragment (no `--standalone`). Math delimiters are preserved as `\(...\)` for MathJax to pick up. Fragment is read at build time by a Server Component and rendered via `dangerouslySetInnerHTML`.

**Pandoc command (per UI-SPEC):**
```bash
# Produces HTML fragment with MathJax-compatible math delimiters
# --mathjax flag wraps TeX math in \(...\) / \[...\] spans
pandoc --from latex --to html5 --mathjax papers/myart.tex -o web/public/papers/myart.html
```

**Why fragment (not `--standalone`):** The `--standalone` flag produces a full HTML document with `<html>`, `<head>`, `<body>`. We need only the body content to embed inside Next.js pages.

**Why `--mathjax` even without standalone:** The flag still wraps math in the correct delimiters `\(...\)` and span class `math`, which MathJax 4 CDN picks up regardless of whether MathJax's own script tag is injected by Pandoc or by Next.js layout.

```typescript
// PaperColumn.tsx — Server Component (no 'use client' needed)
// Reading file at build time is valid in static export / Server Components
import { readFile } from 'fs/promises'
import path from 'path'

interface PaperColumnProps {
  paperSlug: string
}

export async function PaperColumn({ paperSlug }: PaperColumnProps) {
  const filePath = path.join(process.cwd(), 'public', 'papers', `${paperSlug}.html`)
  const html = await readFile(filePath, 'utf-8')

  return (
    <div
      className="overflow-y-auto prose"
      style={{ maxHeight: '90vh', background: '#141414', color: '#C8C8C8' }}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  )
}
```

**Security note:** `dangerouslySetInnerHTML` is safe here because the HTML is build-time output from Pandoc on developer-controlled `.tex` files — there is no user input path.

### Pattern 5: MathJax 4 CDN in Root Layout

**What:** MathJax 4 is loaded from jsDelivr CDN via `<script defer>` in `app/layout.tsx`. Configuration object is placed in a preceding `<script>` tag.

```typescript
// Source: MathJax 4 docs (docs.mathjax.org/en/v4.0/web/start.html) + jsDelivr
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap"
          rel="stylesheet"
        />
        <script
          dangerouslySetInnerHTML={{
            __html: `
              window.MathJax = {
                tex: { inlineMath: [['\\\\(', '\\\\)']], displayMath: [['\\\\[', '\\\\]']] },
                options: { skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'] }
              };
            `,
          }}
        />
        <script
          defer
          src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js"
        />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

### Pattern 6: Artwork Data Model

**What:** Artworks are defined as a static TypeScript array (no database, no CMS). The page component maps over this array to render `<ArtworkSection>` for each entry.

```typescript
// src/data/artworks.ts
export interface Artwork {
  slug: string
  title: string
  videoSrc: string    // e.g. '/videos/fibonacci.mp4'
  posterSrc: string   // e.g. '/posters/fibonacci.png'
  paperSlug: string   // maps to public/papers/{paperSlug}.html
}

export const artworks: Artwork[] = [
  {
    slug: 'fibonacci',
    title: 'Fibonacci Spiral',
    videoSrc: '/videos/fibonacci.mp4',
    posterSrc: '/posters/fibonacci.png',
    paperSlug: 'fibonacci',
  },
  // Add more as renders complete
]
```

### Anti-Patterns to Avoid

- **Using `next export` CLI command:** Removed in Next.js 14. Use `output: 'export'` in config + `next build`.
- **Using Tailwind v3 syntax (`@tailwind base`):** Tailwind 4 uses `@import 'tailwindcss'`. The old directives will fail with `@tailwindcss/postcss`.
- **Using `--standalone` with Pandoc for fragments:** Produces full `<html>` document; embedding it with `dangerouslySetInnerHTML` injects duplicate `<html>/<head>/<body>` tags.
- **Omitting `images: { unoptimized: true }` in static export:** Build will fail with "Export with Image Optimization API" error when using `next/image` with local image paths.
- **Calling `video.play()` without user gesture:** Browsers block programmatic autoplay without a preceding user interaction event. The play must be triggered inside a click handler.
- **Reading paper HTML files at request time with Server Actions:** Static export has no runtime server; file reads must happen at build time (Server Component `async` function with `fs/promises`).
- **Placing 4K MP4 files inside `src/` or importing them as modules:** Large binary assets must be in `public/` and referenced by path string, not imported.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| LaTeX math rendering | Custom math parser | MathJax 4 CDN | Handles all LaTeX math environments, accessibility, line-breaking; years of edge cases |
| LaTeX-to-HTML conversion | Custom LaTeX parser | Pandoc 3.9 | Handles cross-references, citations, environments, custom macros — impossible to replicate |
| Responsive CSS grid | Custom media query JS | Tailwind responsive prefixes (`lg:grid-cols-2`) | Eliminates JS layout calculation; pure CSS with zero runtime overhead |
| Video loading state | Custom preload manager | `preload="none"` + `poster` HTML attributes | Browser handles deferred loading natively; no JS required until play |

**Key insight:** The LaTeX parsing and math rendering ecosystems are large enough that custom solutions will fail on the first complex equation. Pandoc + MathJax is the academic standard precisely because it handles the edge cases.

---

## Common Pitfalls

### Pitfall 1: `next export` CLI No Longer Exists

**What goes wrong:** Developer runs `npm run build && next export`, gets "Unknown command: export" error.
**Why it happens:** `next export` was deprecated in v13.3, removed in v14.0.
**How to avoid:** Set `output: 'export'` in `next.config.ts`. Running `next build` is the only step needed; it writes to `out/`.
**Warning signs:** Any tutorial or snippet using `next export` as a CLI command is from pre-2024 and wrong.

### Pitfall 2: Tailwind v3 vs v4 Setup Confusion

**What goes wrong:** Developer uses `npx tailwindcss init`, creates `tailwind.config.js`, uses `@tailwind base/components/utilities` — build silently produces no styles or throws PostCSS errors.
**Why it happens:** Tailwind 4 is a complete rewrite. The v3 setup is incompatible with `@tailwindcss/postcss`.
**How to avoid:** Use `postcss.config.mjs` with `'@tailwindcss/postcss': {}` as the only plugin. Global CSS uses `@import 'tailwindcss'` only.
**Warning signs:** Styles not applying in dev; PostCSS error referencing missing config.

### Pitfall 3: Pandoc Fragment vs Standalone

**What goes wrong:** Pandoc is run with `--standalone`, producing a full HTML document. Embedding it via `dangerouslySetInnerHTML` injects a nested `<html>` tag inside the React render tree — browsers silently strip it, breaking the layout.
**Why it happens:** Many examples show `--standalone` for complete, previewed output.
**How to avoid:** Omit `--standalone` (or `-s`). Pandoc's default output is already a fragment. Use `--mathjax` only for the math delimiter wrapping.
**Warning signs:** Paper column renders empty or with broken structure in browser DevTools.

### Pitfall 4: MathJax Not Triggering on Dynamically Injected HTML

**What goes wrong:** MathJax script loads once on page init, processes visible math, but content injected via `dangerouslySetInnerHTML` after initial render is not processed — equations display as raw `\(…\)` text.
**Why it happens:** MathJax runs its typeset pass on `DOMContentLoaded`. HTML injected afterward is not auto-processed unless MathJax is re-invoked.
**How to avoid:** In static export, Server Components render their HTML synchronously at build time — the full DOM is in the initial HTML response, so MathJax's initial typeset pass covers all math. This is NOT a problem for this project's static build pattern, but would be a problem with client-side data fetching.
**Warning signs:** Raw `\(formula\)` text visible in browser after page load in dynamic apps; not expected here.

### Pitfall 5: Video Asset Path Resolution in Static Export

**What goes wrong:** Build-time error or broken video paths because MP4 files in `../renders/output/` are outside the Next.js `public/` directory and cannot be served.
**Why it happens:** Static export only serves files inside `public/` — there is no runtime file system resolution.
**How to avoid:** The build plan must include an explicit asset-copy step: copy `renders/output/*.mp4` to `web/public/videos/` and `renders/test_frames/*.png` to `web/public/posters/` before running `next build`.
**Warning signs:** 404 errors for video src in production; works in dev if `next.config.ts` is misconfigured with `assetPrefix`.

### Pitfall 6: Pandoc Not Installed on Machine

**What goes wrong:** `npm run build` fails with "pandoc: command not found" before Next.js build even starts.
**Why it happens:** Pandoc is a native binary, not an npm package. It must be installed separately.
**How to avoid:** Add `pandoc` installation to the Wave 0 / setup checklist. Verify with `pandoc --version` before running build.
**Warning signs:** `prebuild` script fails immediately in CI or on fresh machine.

### Pitfall 7: `images: { unoptimized: true }` Missing

**What goes wrong:** `next build` throws "Error: Image Optimization using the default loader is not compatible with `next export`."
**Why it happens:** Default `next/image` optimization requires a Node.js server at runtime. Static export has no server.
**How to avoid:** Add `images: { unoptimized: true }` to `next.config.ts`. For poster images (used as `poster` attribute on `<video>`, not as `<Image>` component), this is not relevant — plain `<img>` tags or `poster` strings work without this flag.
**Warning signs:** Build error message containing "export-image-api".

---

## Code Examples

Verified patterns from official sources:

### Next.js 16 Static Export Config

```typescript
// Source: https://nextjs.org/docs/app/guides/static-exports (Next.js 16.2.1 docs, 2026-03-25)
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'export',
  images: { unoptimized: true },
}

export default nextConfig
```

### Tailwind v4 PostCSS Config

```javascript
// Source: https://nextjs.org/docs/app/getting-started/css (Next.js 16.2.1 docs, 2026-03-25)
// postcss.config.mjs
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
}
```

### Tailwind v4 Global CSS

```css
/* Source: https://nextjs.org/docs/app/getting-started/css (2026-03-25) */
/* src/app/globals.css */
@import 'tailwindcss';
```

### Pandoc Fragment Conversion Command

```bash
# Source: pandoc.org MANUAL.html — default is fragment output; --mathjax wraps TeX in delimiters
# Produces HTML fragment with math wrapped as \(...\) for MathJax pickup
pandoc --from latex --to html5 --mathjax papers/artwork.tex -o web/public/papers/artwork.html
```

### MathJax 4 CDN Script Tag

```html
<!-- Source: https://docs.mathjax.org/en/v4.0/web/start.html + jsDelivr CDN (mathjax@4.1.1) -->
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js"></script>
```

### HTML5 Video with Poster and Deferred Load

```html
<!-- Source: https://nextjs.org/docs/app/guides/videos (Next.js 16.2.1 docs, 2026-03-25) -->
<video preload="none" poster="/posters/artwork.png" controls aria-label="Video player">
  <source src="/videos/artwork.mp4" type="video/mp4" />
  Your browser does not support the video tag.
</video>
```

### Desktop/Mobile Grid Layout (Tailwind 4)

```tsx
{/* D-04: Side-by-side on desktop (>=1024px), stacked on mobile */}
<section className="max-w-[1440px] mx-auto px-12 py-12 lg:grid lg:grid-cols-2 lg:gap-8">
  <div>{/* VideoPlayer */}</div>
  <div className="overflow-y-auto lg:max-h-[90vh]">{/* PaperColumn */}</div>
</section>
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `next export` CLI | `output: 'export'` in next.config | Next.js 14.0 (2023) | `next export` throws "Unknown command" error |
| `@tailwind base/components/utilities` | `@import 'tailwindcss'` | Tailwind 4.0 (Jan 2025) | PostCSS config and directives are incompatible between versions |
| `tailwindcss` as PostCSS plugin directly | `@tailwindcss/postcss` as PostCSS plugin | Tailwind 4.0 (Jan 2025) | Old plugin produces no output with v4 |
| `tailwind.config.js` required | No config file needed for basic use | Tailwind 4.0 (Jan 2025) | Config file is now opt-in for customization |
| MathJax 3 (`mathjax@3`) | MathJax 4 (`mathjax@4.1.1`) | Feb 2026 | UI-SPEC already references `mathjax@3` CDN URL; update to `@4` |
| `experimental.turbopack` in Next.js config | `turbopack` at top level (or just run `next build`) | Next.js 16.0 | `experimental.turbopack` in config throws deprecation error |

**Deprecated/outdated:**
- `next export` (CLI): Removed in v14. Do not use.
- `@tailwind base` directive: Incompatible with Tailwind v4 PostCSS setup.
- `mathjax@3` CDN URL: Current version is 4. UI-SPEC references `cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js` — this works but delivers v3, not v4. Recommend using `@4` tag for current version.

---

## Runtime State Inventory

This phase is greenfield web code. No rename/refactor involved.

- **Stored data:** None — no database, no user records.
- **Live service config:** None — no external services in this phase.
- **OS-registered state:** None.
- **Secrets/env vars:** None — fully static, no API keys.
- **Build artifacts:** None yet — this phase creates them (`out/` directory).

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Node.js | Next.js build | Yes | v20.12.2 | — |
| npm | Package management | Yes | 10.5.0 | — |
| pandoc | Pandoc pre-build step | No | — (brew: 3.9.0.2 available) | None — must install |
| Git | Version control | Yes (implied) | — | — |

**Missing dependencies with no fallback:**
- **pandoc** — required for `prebuild` npm script that compiles `.tex` → `.html`. No JavaScript alternative can match Pandoc's LaTeX coverage. Wave 0 must include `brew install pandoc`.

**Missing dependencies with fallback:**
- None identified beyond pandoc.

**Node.js version check:** v20.12.2 meets Next.js 16's minimum requirement of Node.js 20.9+.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Playwright (bundled with Next.js 16 as optional peer `@playwright/test ^1.51.1`) |
| Config file | `playwright.config.ts` — Wave 0 gap |
| Quick run command | `npm run build && npx playwright test --grep smoke` |
| Full suite command | `npm run build && npx playwright test` |

**Rationale for Playwright:** The components in this phase are visual and interaction-based (video play, responsive layout, math rendering). Unit tests with Jest/Vitest cannot validate DOM rendering, video element behavior, or CSS layout. Playwright end-to-end tests against the static export are the appropriate validation method.

**Alternative for unit-level:** Simple Jest/Vitest unit tests for the `artworks` data structure and Pandoc fragment file existence can be added for WEB-01 coverage without Playwright overhead.

### Phase Requirements to Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| WEB-01 | Static export `out/` contains `index.html` | smoke (Playwright or shell) | `test -f web/out/index.html` | Wave 0 |
| WEB-01 | Page renders without JS errors | e2e (Playwright) | `npx playwright test --grep "renders gallery"` | Wave 0 |
| WEB-02 | Video element has `preload="none"` and `poster` attribute | e2e (Playwright) | `npx playwright test --grep "video poster"` | Wave 0 |
| WEB-02 | Clicking play overlay starts video playback | e2e (Playwright) | `npx playwright test --grep "play video"` | Wave 0 |
| WEB-03 | Paper column contains rendered HTML from Pandoc | e2e (Playwright) | `npx playwright test --grep "paper column"` | Wave 0 |
| WEB-03 | MathJax script tag present in document `<head>` | e2e (Playwright) | `npx playwright test --grep "mathjax"` | Wave 0 |
| WEB-04 | At 375px viewport, video stacks above paper | e2e (Playwright) | `npx playwright test --grep "mobile layout"` | Wave 0 |
| WEB-04 | At 1280px viewport, side-by-side grid is active | e2e (Playwright) | `npx playwright test --grep "desktop layout"` | Wave 0 |

### Sampling Rate

- **Per task commit:** `npm run build` (confirms static export compiles)
- **Per wave merge:** `npm run build && npx playwright test`
- **Phase gate:** Full Playwright suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `web/playwright.config.ts` — Playwright config pointing at `web/out/` static server
- [ ] `web/tests/gallery.spec.ts` — covers all 8 test cases above
- [ ] Playwright install: `npm install -D @playwright/test && npx playwright install chromium`
- [ ] `web/public/videos/.gitkeep` — placeholder so public/videos/ exists before MP4 copy step

---

## Open Questions

1. **Where does the `web/` directory live relative to the project root?**
   - What we know: Project root has `renders/`, `engine/`, `renderer/` — no web code yet.
   - What's unclear: Should Next.js app be at `web/` (sibling to `renders/`) or at root?
   - Recommendation: Create `web/` as a subdirectory. Keeps Python project structure clean; `web/package.json` is isolated from Python tooling. All commands run from `web/`.

2. **Should MP4 files be copied into `web/public/videos/` or symlinked?**
   - What we know: Static export requires files in `public/`. MP4 source is `renders/output/`.
   - What's unclear: Whether the renders directory will have predictable filenames from Phase 5.
   - Recommendation: Explicit copy step in `package.json` prebuild (e.g., `"copy:assets": "cp ../renders/output/*.mp4 public/videos/ && cp ../renders/test_frames/*.png public/posters/"`). Symlinks are fragile across platforms and git.

3. **UI-SPEC references MathJax `@3`; current npm version is `@4`. Use v3 or v4?**
   - What we know: UI-SPEC specifies `cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js`. npm latest is `mathjax@4.1.1` (2026-02-19). MathJax 4 is a major version with different component structure.
   - What's unclear: Whether the UI-SPEC `@3` was intentional.
   - Recommendation: Use `mathjax@4` (`cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js`) — it is actively maintained and the math delimiter format is identical. If v3 compatibility is required for a specific reason, the research supports either.

4. **No `.tex` paper files exist yet in the project. Does Wave 1 need placeholder papers?**
   - What we know: `papers/` directory does not exist. The Pandoc prebuild script will fail if no `.tex` files are present.
   - Recommendation: Wave 0 or Wave 1 should create at least one placeholder `papers/fibonacci.tex` with minimal content so the full build pipeline can be validated end-to-end.

---

## Sources

### Primary (HIGH confidence)

- [Next.js 16.2.1 official docs — Static Exports](https://nextjs.org/docs/app/guides/static-exports) — `output: 'export'` config, limitations, build commands
- [Next.js 16.2.1 official docs — CSS / Tailwind](https://nextjs.org/docs/app/getting-started/css) — Tailwind v4 PostCSS setup, `@import 'tailwindcss'`
- [Next.js 16.2.1 official docs — Installation](https://nextjs.org/docs/app/getting-started/installation) — `create-next-app` defaults, TypeScript setup
- [Next.js 16.2.1 official docs — Videos](https://nextjs.org/docs/app/guides/videos) — Self-hosted video, `<video>` attributes, `preload="none"`, poster
- [Next.js 16 release blog](https://nextjs.org/blog/next-16) — Breaking changes, Turbopack default, removed features list
- [Next.js 16.2.1 official docs — Image Optimization](https://nextjs.org/docs/app/getting-started/images) — `unoptimized: true` for static export
- npm registry — `next@16.2.1` (2026-03-20), `tailwindcss@4.2.2`, `@tailwindcss/postcss@4.2.2`, `mathjax@4.1.1` (2026-02-19) — versions verified

### Secondary (MEDIUM confidence)

- [pandoc.org MANUAL.html](https://pandoc.org/MANUAL.html) — Fragment output default, `--mathjax` flag, math delimiter format (accessed via WebSearch; content consistent with official docs)
- [dasroot.net — Converting LaTeX to HTML with Pandoc and MathJax (2026-03)](https://dasroot.net/posts/2026/03/converting-latex-to-html-pandoc-mathjax/) — Practical pitfalls: TikZ unsupported, MathJax injection requires math presence, special characters
- [MathJax 4 docs — Getting Started](https://docs.mathjax.org/en/v4.0/web/start.html) — Script tag, `defer` attribute, configuration object placement
- [jsDelivr — mathjax package](https://www.jsdelivr.com/package/npm/mathjax) — Confirmed `mathjax@4.1.1` current as of 2026-02-19

### Tertiary (LOW confidence)

- WebSearch results on `dangerouslySetInnerHTML` in Next.js 16 — confirmed safe for build-time static HTML; multiple sources agree but not from official Next.js docs page.
- WebSearch results on video `preload="none"` performance — cross-browser behavior documented by MDN and web.dev; well-established.

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all versions verified against npm registry on 2026-03-27; framework docs current
- Architecture: HIGH — patterns verified against Next.js 16 official docs; Tailwind v4 confirmed from official Next.js CSS docs
- Pitfalls: HIGH — `next export` removal and Tailwind v4 changes verified from official changelogs; video and pandoc pitfalls verified against official docs and pandoc manual
- Environment: HIGH — directly probed Node.js version and pandoc availability on this machine

**Research date:** 2026-03-27
**Valid until:** 2026-04-27 (30 days — Next.js and Tailwind patch versions move frequently but breaking changes are unlikely within minors)
