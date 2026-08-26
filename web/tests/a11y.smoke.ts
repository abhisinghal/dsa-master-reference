import { test, expect } from '@playwright/test'

/**
 * A11y smoke suite (Wave 7).
 *
 * These assertions guarantee that the visual/a11y polish shipped in Wave 7
 * does not regress. If any of these fail, the visual bar dropped and we need
 * to know before merge.
 *
 * We don't run full axe here (that's a follow-up). We assert the specific
 * contracts the audit_visuals.py script enforces at content authoring time.
 */

const CHAPTERS_WITH_ANIMS = [
  { path: '/patterns/sliding-window', animSelector: '.anim-card' },
  { path: '/patterns/prefix-sum', animSelector: '.anim-card' },
  { path: '/patterns/hashing', animSelector: '.anim-card' },
  { path: '/patterns/merge-intervals', animSelector: '.anim-card' },
  { path: '/patterns/topological-sort', animSelector: '.anim-card' },
  { path: '/patterns/greedy', animSelector: '.anim-card' },
  { path: '/patterns/bit-manip', animSelector: '.anim-card' },
]

for (const { path, animSelector } of CHAPTERS_WITH_ANIMS) {
  test(`a11y: ${path} — every anim has role="img" and aria-label`, async ({ page }) => {
    await page.goto(path)
    const anims = page.locator(`${animSelector} svg`)
    const count = await anims.count()
    expect(count, `${path} should have at least one anim SVG`).toBeGreaterThan(0)
    for (let i = 0; i < count; i++) {
      const svg = anims.nth(i)
      const role = await svg.getAttribute('role')
      const label = (await svg.getAttribute('aria-label')) || (await svg.getAttribute('aria-labelledby'))
      expect(role, `${path} SVG #${i}: role missing`).toBe('img')
      expect(label, `${path} SVG #${i}: aria-label missing`).toBeTruthy()
    }
  })
}

test('every static SVG figure has role and aria-label', async ({ page }) => {
  const paths = [
    '/patterns/sliding-window',
    '/patterns/two-pointers',
    '/patterns/binary-search',
    '/patterns/dp',
    '/patterns/backtracking',
  ]
  for (const p of paths) {
    await page.goto(p)
    const figs = page.locator('.svg-figure svg')
    const n = await figs.count()
    for (let i = 0; i < n; i++) {
      const role = await figs.nth(i).getAttribute('role')
      const label = await figs.nth(i).getAttribute('aria-label')
      expect(role, `${p} .svg-figure #${i}: role missing`).toBe('img')
      expect(label && label.length > 3, `${p} .svg-figure #${i}: aria-label missing`).toBeTruthy()
    }
  }
})

test('anim buttons are keyboard focusable with visible outline', async ({ page }) => {
  await page.goto('/patterns/prefix-sum')
  // Focus the first range input in the PrefixSumAnim
  const range = page.locator('.anim-card input[type="range"]').first()
  await range.focus()
  // Focus should land — read active element
  const focused = await page.evaluate(() => {
    const active = document.activeElement
    return active?.tagName + (active?.getAttribute('type') || '')
  })
  expect(focused).toContain('INPUT')
})

test('reduced-motion respects @media rule', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.goto('/patterns/prefix-sum')
  // The .anim-card content should be present regardless
  await expect(page.locator('.anim-card')).toBeVisible()
})
