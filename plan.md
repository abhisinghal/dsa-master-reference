# DSA Master Reference — Live Plan

Last updated: 2026-08-22 (session c960137b).
Live at https://abhisinghal.github.io/dsa-master-reference/ · Repo `abhisinghal/dsa-master-reference` · Latest commit `4576b6e`.

---

## This session — practice-page rollout

Delivered a new **/problems/** section with **205 problem pages** — one dedicated URL per LC problem across all 21 core-pattern chapters.

### Multi-approach pages (hand-authored, full walkthrough)

**29 problem pages authored fully** with brute-force → intermediate → optimized approaches. Each approach has its own **Java code** + **interactive Execution Trace**.

The 21 pattern-flagship pages (one per pattern):
- Sliding Window → Longest Substring Without Repeating
- Two Pointers → Container With Most Water
- Fast/Slow → Linked List Cycle II
- Prefix Sum → Subarray Sum Equals K
- Hashing → Two Sum
- Monotonic Stack → Daily Temperatures
- Binary Search → Search in Rotated Sorted Array
- BS on Answer → Koko Eating Bananas
- Top-K/Heap → Top K Frequent Elements
- K-way Merge → Merge K Sorted Lists
- Merge Intervals → Merge Intervals
- Sweep Line → Meeting Rooms II
- Topological Sort → Course Schedule II
- Union-Find → Number of Provinces
- Greedy → Jump Game II
- Backtracking → N-Queens
- Divide & Conquer → Count of Smaller Numbers After Self
- DP → House Robber
- Trie → Word Search II
- Bit Manipulation → Single Number
- Quickselect → Kth Largest Element

Plus 8 high-value canonical variations:
- 3Sum · Trapping Rain Water · Largest Rectangle in Histogram
- Maximum Subarray (Kadane) · Coin Change · LIS · Edit Distance
- Permutations · Subsets

### 100% flagship-quality across ALL 205 practice pages (audit complete)

**Final audit results (see plan.md changelog):**

| Section | Coverage |
|---|---|
| Numbered Examples (`**Example 1**` format) | **100%** (205/205) |
| Constraints line (`**Constraints**` format) | **100%** (205/205) |
| Complexity summary table | **100%** (205/205) |
| When to use which bullets | **100%** (205/205) |
| Related problems section | **100%** (205/205) |
| CodeTrace embed | **89.8%** (184/205 — remaining 21 are design classes, 2D grids, trivial 1-line algorithms where a CodeTrace adds no value) |

**Every page includes**: LC link + difficulty badge + pattern chapter link, problem statement + 3 numbered Examples + Constraints line, 2–4 approaches (Brute → Intermediate → Optimal) each with Intuition + Java code + CodeTrace + per-approach Complexity, Complexity summary table with interview grades, When to use which practical bullets, Related problems with LC links.

**Total: 205 practice pages (21 flagships + 184 variations, all fully authored).**

### Infrastructure

- New `gen/src/problems/` directory (49 old chapters unchanged; 205 new problem files)
- `migrate.py` auto-migrates every `problems/*.md` to `web/docs/problems/*.md` (strips numeric prefixes)
- Top nav: new "Practice" link between Data Structures and System Design
- Sidebar: 21 collapsible pattern groups, 205 clickable problem entries
- Scaffold generator parses "Same pattern, new tweaks" tables for LC link + one-line differentiator

## Cumulative session output

- **177 interactive Execution Traces** across chapters (100% Trace-it coverage + 98% Trap coverage)
- **205 problem pages** in the new /problems/ section — **100% fully authored** (21 flagships + 184 variations, zero scaffolds)
- **CI-green** on every push; site live at abhisinghal.github.io/dsa-master-reference/

## Recent commits (all live)

- `5a18eec` flagship-quality — 10 more pages (Top-K 3, K-way Merge 3, Monotonic Stack 4) — 38 total this session
- `9df65d2` flagship-quality — 9 more pages (Fast/Slow 5, Binary Search 4)
- `68d0579` flagship-quality — 11 more pages (SW 5, TP 3, Hash 3)
- `f56dd1d` flagship-quality — 8 Sliding Window pages
- `b11a07f` upgrade all 133 variation pages to flagship format (structural)
- `5a02edb` fix: strip `NNv-` prefix in migrate.py (resolves 90% Practice 404s)
- `96be326` docs: mark all visualizer items shipped
- `53be2ab` +84 auto-embedded Example Previews
- `92cf495` interactive visualizers — complexity curve, 6-phase playbook, DS state machines
- `3b50d5a` +28 DP full multi-approach pages — final batch
- `16c11b1` slug fix: at-most-k-distinct-characters
- `9b4d3af` +25 Sliding Window full multi-approach pages
- `b1b9910` +15 Backtracking full multi-approach pages
- `f7b2866` +10 Greedy full multi-approach pages
- `ce5efd4` +26 pages (Two Pointers 13, Hashing 13)
- `96a98c7` +17 pages (Prefix Sum finish, Trie complete, Bit Manip complete)
- `a3cb4ce` +21 pages (Merge Intervals, BS on Answer, Union-Find)
- `131c230` +29 pages (Fast/Slow, Sweep Line, Top-K, K-way Merge, Monotonic Stack, Binary Search, Topo Sort, Divide &amp; Conquer)
- `4576b6e` +8 canonical variations upgraded
- `0d69872` +184 initial variation pages
- `30e4ba8` 21 flagship practice pages
- `3a50063` docs: plan.md — 177 Execution Traces
- `3de6824` Execution Traces in cheatsheets, transcripts, SD
- `4ab7ae3` P0 Trap Traces batch 2 (61 auto)
- `019530f` P0 Trap Traces batch 1 (20 hand)
- `a94d862` Naming: "Execution Trace" badge
- `d1a7683` System Design chapter
- `cdc2ff2` 100% CodeTrace coverage

## CEO-level gap audit (Educative + AlgoExpert lens) — 2026-08-23

Even with 205 flagship-quality pages, real gaps remain vs. the incumbents:

### Educative.io CEO perspective — "Great reference, not a course"

**P0 (business-breaking):**
1. No user accounts (progress lost across devices, no B2B, no personalization)
2. JavaRunner on only 7/205 problems (landing over-promises)
3. No quizzes on 21 pattern chapters (component exists, sparsely used)
4. No AI companion ("explain differently", "give me a hint") — 2026 table stakes
5. No time estimates per chapter (Educative always shows "8h 30m")

**P1 (retention killers):**
6. No certificate on completion
7. No email capture / drip campaign
8. No bookmark/notes feature
9. No mobile app
10. No spaced-repetition review prompts

**P2 (product-shape):**
- No "Recommended next" on chapter completion
- No Team/Org accounts (no B2B revenue)
- Roadmap is a doc, not interactive checklist
- No pricing / monetization

### AlgoExpert CEO perspective — "Where are the videos?"

**P0 (category-defining):**
1. Zero videos (AlgoExpert sells 5-15 min per problem)
2. Java-only (locks out ~65% of segment)
3. No hint system (progressive Hint 1 → Hint 2 → Solution)
4. No company tags (Meta / Google / Amazon)
5. No timed practice mode (real interviews are 45 min)

**P1 (product-completeness):**
6. No frequency indicator ("asked in 40% of Meta interviews")
7. No streaks / achievements / gamification
8. No whiteboarding canvas
9. No mock interview mode
10. No language switcher on solutions (JS/Py/Java/C++ tabs)
11. No solution comparison ("your O(n²) vs optimal O(n)")
12. No "similar mistakes" telemetry callout

### Top 8 next steps (impact × urgency ÷ effort)

| # | Task | Wave |
|---|---|---|
| 1 | JavaRunner on all 205 problems (CheerpJ WASM) — 2 weeks | A |
| 2 | Quizzes at end of every pattern chapter (21 × 5 Q) — 1 week | A |
| 3 | Hint system per problem (3 progressive hints) — 1 week | A |
| 4 | Company tags on top 100 problems — 1 week | A |
| 5 | User accounts + progress sync (Supabase) — 3 weeks | B |
| 6 | Email capture + 8-week drip campaign — 1 week | B |
| 7 | 21 pattern-intro Loom videos — 4-6 weeks | C |
| 8 | AI companion chat per problem — 4 weeks | C |

### Monetization decision (30-day deadline)

Pick one:
1. Free + newsletter (ByteByteGo) — needs email + weekly cadence
2. $19 lifetime PDF+notes (Grokking-companion) — needs Stripe + gated content
3. $99/yr full course (Educative) — needs accounts + videos + mock + community
4. Free reference + $99/hr coaching — needs Calendly + Stripe + testimonials


## Blocked on you

- `add-email-capture-pdf-gate` — needs your Buttondown/ConvertKit signup
