import { test, expect } from '@playwright/test'

// WEB-01: Static export
test('renders gallery — out/index.html exists and page loads', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveTitle(/Mathematica/)
})

// WEB-01: No JS errors on load
test('renders gallery — no console errors on load', async ({ page }) => {
  const errors: string[] = []
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()) })
  await page.goto('/')
  expect(errors.filter(e => !e.includes('MathJax'))).toHaveLength(0)
})

// WEB-02: Video poster and preload
test('video poster — video element has preload=none and poster attribute', async ({ page }) => {
  await page.goto('/')
  const video = page.locator('video').first()
  await expect(video).toHaveAttribute('preload', 'none')
  await expect(video).toHaveAttribute('poster')
})

// WEB-02: Play interaction
test('play video — clicking play overlay starts video', async ({ page }) => {
  await page.goto('/')
  const playBtn = page.getByRole('button', { name: /play artwork/i }).first()
  await expect(playBtn).toBeVisible()
  await playBtn.click()
  const video = page.locator('video').first()
  await expect(video).toHaveAttribute('controls')
})

// WEB-03: Paper column HTML present
test('paper column — paper column contains rendered HTML from Pandoc', async ({ page }) => {
  await page.goto('/')
  // PaperColumn renders dangerouslySetInnerHTML; check for paragraph or heading content
  const paperCol = page.locator('[data-testid="paper-column"]').first()
  await expect(paperCol).not.toBeEmpty()
})

// WEB-03: MathJax script in head
test('mathjax — MathJax script tag is present in document head', async ({ page }) => {
  await page.goto('/')
  const mathJaxScript = page.locator('script[src*="mathjax"]')
  await expect(mathJaxScript).toHaveCount(1)
})

// WEB-04: Mobile layout — video stacks above paper at 375px
test('mobile layout — video stacks above paper at 375px viewport', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 })
  await page.goto('/')
  const videoCol = page.locator('[data-testid="video-column"]').first()
  const paperCol = page.locator('[data-testid="paper-column"]').first()
  const videoBound = await videoCol.boundingBox()
  const paperBound = await paperCol.boundingBox()
  // Video must appear above paper (lower y value = higher on screen)
  expect(videoBound!.y).toBeLessThan(paperBound!.y)
})

// WEB-04: Desktop layout — side-by-side at 1280px
test('desktop layout — side-by-side grid active at 1280px viewport', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 })
  await page.goto('/')
  const videoCol = page.locator('[data-testid="video-column"]').first()
  const paperCol = page.locator('[data-testid="paper-column"]').first()
  const videoBound = await videoCol.boundingBox()
  const paperBound = await paperCol.boundingBox()
  // On desktop, columns are side by side: same y (within 20px tolerance), different x
  expect(Math.abs(videoBound!.y - paperBound!.y)).toBeLessThan(20)
  expect(videoBound!.x).toBeLessThan(paperBound!.x)
})
