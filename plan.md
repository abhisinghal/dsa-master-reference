# DSA Master Reference — Live Plan

Last updated: 2026-08-22 (session c960137b).
Live at https://abhisinghal.github.io/dsa-master-reference/ · Repo `abhisinghal/dsa-master-reference` · Latest commit `80c2057`.

---

## Where we are — honest scorecard

### Shipped this session ✅

**Foundation (Tier-1 visuals sprint):**
- Design token system (`--dsa-*`, light + dark) in `web/docs/.vitepress/theme/style.css`
- `StepStrip.vue` + `TwoSumStepStrip.vue` (1 real usage on Two Sum)
- 49 static SVGs across 26 files (all 30 canonical problems + concept diagrams)
- 15 animation Vue components, 14 pattern chapters embed one
- Icon system: `Icon.vue` with 15 lucide-style SVGs; emojis swapped in 5 Vue components + 23 markdown files

**Grokking-style code-run-flow trace (new this turn):**
- `CodeTrace.vue` — reusable component that renders a horizontal comic-strip of per-iteration SVG frames
- 11 flagship problems have a visual trace (122 step-frames total)
- Bonus fix: `migrate.py` `KNOWN_HTML` regex tightened to allow `>` in quoted Vue attribute values (prevents recurrence of the bare-`>` bug)

**CEO-review Wave A/B (before this turn):**
- CheerpJ browser Java runner (no rate limit)
- Sidebar filter, URL slug normalization, 100% difficulty-badge coverage
- Per-pattern quizzes (63 questions across 21 chapters)
- How-this-compares + Changelog pages, author bio, video callout placeholders, PDF messaging

**Critical infra fixes:**
- `transform_svg_fences()` strips blank lines inside inline SVGs (fixes the 7-hour dp.md build hang)
- `KNOWN_HTML` regex handles multi-line Vue tags with `>` in quoted attrs

### Honest completion vs original 50-60h Tier-1 scope: **~90%**

---

## What's actually left

### Currently pending in the todo list (5 items)

| id | title | true state | est. effort |
|---|---|---|---|
| c2-rss-changelog | RSS feed on changelog | I wrote `gen-rss.mjs` but never wired it into `config.mts` or verified it produces `dist/rss.xml`. In-progress but stalled. | 30 min |
| a1-token-audit | Design token audit | Not started. Need to grep for hardcoded `#hex` in older SVGs and replace with `var(--dsa-*)`. | 90 min |
| a2-more-stepstrips | 4 more StepStrip wrappers | Not started. Need custom step content per problem (Sliding Window, House Robber, Subsets, Binary Search). | 2 h |
| a3-embed-anims | Embed remaining anims | Not started. Reuse existing anims in prefix-sum, k-way-merge, greedy, trees, heaps, trie, segment-fenwick. | 1.5 h |
| a4-landing-screenshots | Real landing screenshots | Not started. Requires a browser + puppeteer or manual screen-capture. | 30 min |
| b2-system-design-intro | System design intro chapter | Not started. Biggest single content lift (25-35 pages: URL shortener, rate limiter, KV store). | 8-10 h |

### Newly-visible gaps I owe you (not in the todo list yet)

**CodeTrace coverage is 12%, not 100%.** I shipped 11 traces on flagship problems; there are 76 more `> [note] **Trace it**` callouts across the book that have text but no visual. Full audit:

| Chapter | Text traces | Visual traces |
|---|---|---|
| 21-sliding-window | 6 | 2 |
| 22-two-pointers | 5 | 2 |
| 23-fast-slow | 1 | 0 |
| 24-prefix-sum | 3 | 1 |
| 25-hashing | 4 | 1 |
| 26-monotonic-stack | 2 | 1 |
| 27-binary-search | 1 | 1 ✅ |
| 28-bs-on-answer | 3 | 0 |
| 29-top-k-heap | 1 | 0 |
| 30-k-way-merge | 2 | 0 |
| 31-merge-intervals | 1 | 0 |
| 32-sweep-line | 2 | 0 |
| 33-topological-sort | 1 | 0 |
| 34-union-find | 2 | 0 |
| 35-greedy | 4 | 0 |
| 36-backtracking | 5 | 0 |
| 37-divide-conquer | 1 | 0 |
| 38-dp | 9 | 3 |
| 39-trie-pattern | 2 | 0 |
| 40-bit-manip | 3 | 0 |
| 41-quickselect | 1 | 0 |
| 42-math | 3 | 0 |
| 44-design | 3 | 0 |
| 50-arrays | 1 | 0 |
| 52-strings | 2 | 0 |
| 56-linked-lists | 2 | 0 |
| 58-stacks-queues | 2 | 0 |
| 60-trees | 6 | 0 |
| 62-heaps | 1 | 0 |
| 64-trie | 1 | 0 |
| 66-graphs | 4 | 0 |
| 68-segment-fenwick | 3 | 0 |
| **Total** | **87** | **11 (12%)** |

Each additional trace needs **~10-15 minutes of authoring** (extract from the existing text trace, structure as steps, verify), so full 100% coverage is **~15 hours** of focused work.

### Blocked (needs your action, not mine) ⏸

| id | title | needs |
|---|---|---|
| add-email-capture-pdf-gate | Email capture on PDF download | You to sign up for Buttondown or ConvertKit and share the API endpoint/key |

---

## What I recommend as the next single-session batch

**Priority 1 (do first, ~2 h):** Finish what I already started
- `c2-rss-changelog` — wire up the generator (30 min)
- `a1-token-audit` — sweep hardcoded hex (90 min)

**Priority 2 (highest-impact user-visible work, ~15 h):** Full CodeTrace coverage
- Author the remaining 76 CodeTrace embeds across all 32 chapters. This delivers the Grokking "every problem has a visual code-run-flow" promise everywhere, not just 12% of it.
- Can be split across sessions.

**Priority 3 (~11 h):** Round out Tier-1
- `a3-embed-anims` (1.5 h)
- `a2-more-stepstrips` (2 h)
- `a4-landing-screenshots` (30 min, may need your screen-capture help)
- `b2-system-design-intro` (8 h — biggest single content lift for senior/staff audience)

## Blockers still waiting on you

1. **Newsletter provider** — Buttondown / ConvertKit / Substack. Pick one to unblock C1.
2. **Screen recording** — for real landing screenshots (A4) and any pattern walkthrough Loom videos (deferred).

---

## Bigger bets deferred (kept here so we don't lose them)

- AI companion chat (multi-day; API-key strategy)
- Auth / accounts / cross-device progress sync (multi-day; backend)
- Community / forum / comments (moderation strategy)
- Mock-interview AI voice mode (multi-week)
- Job board integration
- Mobile app

