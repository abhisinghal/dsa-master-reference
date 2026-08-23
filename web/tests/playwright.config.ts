import { defineConfig, devices } from '@playwright/test'

/**
 * Playwright smoke suite for the DSA Master Reference site.
 *
 * These are contract tests, not user-flow tests. They ensure that:
 *  - the build produces working HTML for a representative set of pages
 *  - no Vue components leak through as escaped raw text (the migrate.py bug class)
 *  - #app mounts on every sampled page
 *  - navigation and search UI are present
 *
 * We run against a preview server of the freshly-built dist/, not the live site.
 * CI (see .github/workflows/test.yml) starts `npm run docs:preview` and points here.
 */
export default defineConfig({
  testDir: '.',
  testMatch: /.*\.smoke\.ts$/,
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: process.env.CI ? [['list'], ['html', { open: 'never' }]] : 'list',
  use: {
    baseURL: process.env.SMOKE_BASE_URL || 'http://localhost:4173',
    trace: 'on-first-retry',
    navigationTimeout: 15_000,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
  webServer: process.env.CI
    ? undefined
    : {
        command: 'npm run docs:preview',
        url: 'http://localhost:4173',
        reuseExistingServer: true,
        timeout: 60_000,
        cwd: '..',
      },
})
