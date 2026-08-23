import { test, expect, Page } from '@playwright/test'

/**
 * Baseline smoke suite.
 *
 * Every page in SAMPLED_PAGES must pass every assertion here. If any component
 * silently regresses to escaped raw text (the Round-9-through-20 bug class),
 * these tests fail loudly BEFORE merge.
 */

const SAMPLED_PAGES = [
  '/',
  '/patterns/',
  '/patterns/sliding-window',
  '/patterns/two-pointers',
  '/patterns/dp',
  '/patterns/backtracking',
  '/problems/sliding-window-longest-substring',
  '/problems/hashing-two-sum',
  '/problems/coin-change',
  '/problems/n-queens',
  '/appendix/interview-day-kit',
  '/appendix/behavioral-crash-course',
  '/foundations/roadmap',
  '/tracks/meta',
]

// Any Vue component tag that MUST NOT appear as escaped raw text anywhere.
const COMPONENTS_MUST_NOT_ESCAPE = [
  'PatternVideo',
  'PatternProgress',
  'CompanyTags',
  'Hints',
  'MarkSolved',
  'JavaRunner',
  'InterviewTimer',
  'AiCompanion',
  'Bookmark',
  'FeedbackWidget',
  'RelatedPatterns',
  'RelatedProblems',
  'DueForReview',
  'BookmarksList',
  'StudyPlanGenerator',
  'RoadmapChecklist',
  'StreakTracker',
  'UserProfile',
  'ProblemStats',
]

async function pageHtml(page: Page): Promise<string> {
  return await page.content()
}

for (const path of SAMPLED_PAGES) {
  test(`smoke: ${path}`, async ({ page }) => {
    const response = await page.goto(path, { waitUntil: 'domcontentloaded' })
    // 200 or 304 both fine.
    expect(response, `no response for ${path}`).toBeTruthy()
    expect(response!.status(), `bad status for ${path}`).toBeLessThan(400)

    // #app must mount (VitePress root).
    await expect(page.locator('#app')).toBeVisible()

    // No escaped Vue component tags in the rendered HTML.
    const html = await pageHtml(page)
    for (const comp of COMPONENTS_MUST_NOT_ESCAPE) {
      expect(
        html.includes(`&lt;${comp}`),
        `Page ${path} contains escaped <${comp}> — check migrate.py KNOWN_HTML whitelist and gen/fix_component_spacing.py`,
      ).toBe(false)
    }

    // Header / nav shell present.
    await expect(page.locator('.VPNav, header').first()).toBeVisible()
  })
}

test('landing has interactive widgets', async ({ page }) => {
  await page.goto('/')
  // These are core landing widgets; if any is missing, the CTO-plan interactive
  // features regressed.
  await expect(page.locator('.stats-strip')).toBeVisible()
  // StreakTracker container class is `.streak-panel` in the component.
  // Missing widget = regression, not a UX preference.
  const hasStreak = await page.locator('.streak-panel').count()
  expect(hasStreak).toBeGreaterThan(0)
})

test('a problem page has Mark Solved + Interview Timer + Bookmark', async ({ page }) => {
  await page.goto('/problems/hashing-two-sum')
  await expect(page.locator('.mark-btn').first()).toBeVisible()
  await expect(page.locator('.bmk-btn').first()).toBeVisible()
  // InterviewTimer is a <details> summary; look for its label.
  await expect(page.getByText('Interview timer').first()).toBeVisible()
})

test('search UI mounts', async ({ page }) => {
  await page.goto('/')
  // VitePress local-search button exists in the nav.
  const searchTrigger = page.locator('.VPNavBarSearch, [aria-label*="Search" i]').first()
  await expect(searchTrigger).toBeVisible()
})

test('404 page uses custom NotFound component', async ({ page }) => {
  const response = await page.goto('/does-not-exist-xyz-abc', { waitUntil: 'domcontentloaded' })
  expect(response!.status()).toBe(404)
  // Custom NotFound has an .nf-wrap container.
  await expect(page.locator('.nf-wrap')).toBeVisible()
})
