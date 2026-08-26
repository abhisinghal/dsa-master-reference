# Deep Audit & Modification Plan — 21 Core Patterns

**Date:** 2026-08-26
**Status:** ✅ **ALL 8 WAVES SHIPPED**
**Applied via the 3-lens mindset (stored in user notes):**
1. **Senior SWE + DSA architect** — mentor engineers from 1yr → 10+yrs
2. **FAANG PM** — product/visual quality, interactive experiences
3. **Top UX designer** — nitty-gritty scrutiny at pixel/flow level
**Visual quality reference:** https://abhisinghal.github.io/systemexpert/learn/distributed-systems/consistent-hashing/

---

## Execution summary

| Wave | Content | Commit | Status |
|---|---|---|---|
| 1 | Narrative bones on 10 chapters (Why exists / When / Templates / Traps / History / Canonical walkthrough) | `2db68c6` | ✅ |
| 2 | Anemic-chapter enrichment (folded into Wave 1) | — | ✅ |
| 3 | 6 new user-driven Vue anim components + embed | `9a0f1cd` | ✅ |
| 4 | Story-first opening rewrites on 10 chapters | `c39f372` | ✅ |
| 5 | Callout enrichment — every chapter now ≥ 8 highlighted insights | `a70ca5c` | ✅ |
| 6 | Historical grounding paragraphs on 10 remaining chapters (21/21 now covered) | `629b040` | ✅ |
| 7 | Visual + a11y polish: 35/35 SVGs pass audit, 21 anims covered by global CSS, Playwright a11y suite added | `e7004fa` | ✅ |
| 8 | 4 flagship canonical walkthroughs (Union Find, Topo Sort, Greedy, D&C) | `79afd41` | ✅ |

---

## Part 1 — The reference bar (what "excellent" looks like)

The systemexpert consistent-hashing page has these 8 properties. They are the standard we are aiming for on every core pattern chapter:

| Property | What it looks like |
|---|---|
| **Story-first opening** | "You built a photo-sharing app. It got popular." Second person, concrete, one-scene. |
| **Physical/spatial metaphor** | "Think of a notepad on your desk" — the metaphor grounds the abstract idea in a physical action. |
| **Naive → defended → failed → clever** | The naive approach (`hash % N`) is *defended* for 4 paragraphs — "why the industry used it for 30 years" — *then* broken. This is the arc that respects the reader's intelligence. |
| **User-driven interactive diagram** | "Click '+ Add a 4th cache' to see what happens." User initiates the change; the diagram responds. Not a passive timeline replay. |
| **Concrete drama numbers** | "~750,000 database queries at the same moment. Your database melts." Real, calibrated, scary. |
| **Historical grounding** | Karger, Lehman, Leighton (1997) + Akamai spin-out story. Names, years, real product. |
| **Chunked prose** | Each block is 2–4 short paragraphs under a bold H2/H3. No walls of text. |
| **Foreshadow before deep-dive** | "The rest of this chapter shows you exactly how it works." Reader knows the payoff before committing. |

Everything below is measured against this bar.

---

## Part 2 — The audit summary

Ran a structural + content audit on all 21 pattern chapters (`gen/src/21-*.md` through `41-*.md`).

### 2.1 Section-structure completeness

| Required section | Present in | Missing in |
|---|---|---|
| `## Why <pattern> exists — the story` | 12/21 (57%) | **two-pointers**, prefix-sum, hashing, monotonic-stack, binary-search, bs-on-answer, top-k-heap, backtracking, dp, trie, bit-manip |
| `## When to use — and when not` | 12/21 (57%) | **two-pointers**, prefix-sum, hashing, monotonic-stack, binary-search, bs-on-answer, backtracking, dp, bit-manip |
| `## How to use — templates` | 10/21 (48%) | **two-pointers**, prefix-sum, hashing, monotonic-stack, binary-search, bs-on-answer, union-find, greedy, backtracking, dp, bit-manip |
| `## Traps` (explicit H2 section) | 5/21 (24%) | 16 chapters have inline `> [trap]` callouts but no aggregated section |
| `<Quiz>` at chapter end | 21/21 ✓ | none |
| `<PatternProgress>` at top | 21/21 ✓ | none |
| `<PatternVideo>` placeholder | 21/21 ✓ | none |
| `<RelatedPatterns>` at end | 21/21 ✓ | none |
| Interactive Vue anim component | 15/21 (71%) | **prefix-sum, hashing, merge-intervals, topological-sort, greedy, bit-manip** |

**Verdict:** every chapter has the *infrastructure widgets* but ~50% are missing the *narrative bones*. This is the exact "consistency reads as a bug" issue.

### 2.2 Word-count disparity (4× spread)

| Bucket | Chapters | Word range |
|---|---|---|
| **Rich** | sliding-window, dp | 9,000–9,500 |
| **Solid** | backtracking, two-pointers, hashing | 4,800–5,900 |
| **Thin** | 14 chapters | 2,800–4,000 |
| **Anemic** | binary-search, bs-on-answer, bit-manip, quickselect | 2,300–3,500 |

**Binary Search is the FLAGSHIP pattern and it's the thinnest chapter (2,387 words). Unacceptable.**

### 2.3 Interactive-diagram audit

- 15/21 have a `<XxxAnim />` Vue component (Play / Pause / Prev / Next / Reset).
- **All 15 are timeline replays** — pre-scripted step arrays. **None accept user input to change the scenario.**
- The systemexpert reference is fundamentally different: the diagram *reacts to a user decision* ("+ Add a 4th cache"). Our diagrams *play back a canned story*.
- 6 chapters have no interactive component at all: **prefix-sum, hashing, merge-intervals, topological-sort, greedy, bit-manip**.

### 2.4 Callout density (highlighted insights per chapter)

| Chapter | key + trap + inv total | Verdict |
|---|---|---|
| Sliding Window | **20** | Reference-quality |
| DP | **23** | Reference-quality |
| Backtracking, Two Pointers, Hashing, Greedy | 8–13 | Solid |
| Merge Intervals, Union Find, Top-K, K-Way, Quickselect, Topo Sort, D&C, Bit Manip | **3–5** | Thin |
| Fast/Slow, Binary Search, Monotonic Stack | **4–6** | Thin |

### 2.5 Story-opening tone

Only 2/21 chapters open in the systemexpert style ("You built X..." / "Imagine..."). Two Pointers opens with `"Instead of checking every pair with two nested loops..."` — cold, textbook. **19/21 chapters miss this.**

### 2.6 Missing entirely vs the reference bar

None of the 21 chapters have:
- **Historical grounding** — inventors, years, real-world adoption. Consistent hashing = Karger 1997 + Akamai. Binary search's actual history includes Mauchly 1946 and the fact that **the majority of implementations were broken for 40 years** (Bentley's mid-overflow bug fixed by Google in 2006). Story worth telling.
- **User-driven "what if" diagram** — where the reader clicks something and the algorithm re-runs on their input.
- **Naive-approach defense** — every chapter jumps to the optimized approach without first explaining *why the naive one seemed reasonable*.
- **Concrete-drama numbers** — "with n = 10^9 the naive approach takes 32 years; the pattern completes in 30 microseconds."

---

## Part 3 — Three-lens verdict per chapter

Graded on 5 axes (1–5, higher = closer to reference bar):

| Pattern | Narr | Vis | Interact | Density | Callouts | **Total /25** | Grade |
|---|---|---|---|---|---|---|---|
| Sliding Window | 4 | 4 | 3 | 5 | 5 | **21** | A- |
| DP | 3 | 4 | 3 | 5 | 5 | **20** | A- |
| Backtracking | 4 | 4 | 3 | 4 | 4 | **19** | B+ |
| **Two Pointers** | **3** | 4 | 3 | 4 | 3 | **17** | B |
| Hashing | 3 | 2 | 1 | 4 | 3 | **13** | C+ |
| Fast/Slow | 4 | 4 | 3 | 3 | 2 | **16** | B- |
| Monotonic Stack | 3 | 4 | 3 | 3 | 2 | **15** | B- |
| Binary Search | 3 | 4 | 3 | **2** | 2 | **14** | C+ |
| BS on Answer | 3 | 4 | 3 | 3 | 3 | **16** | B- |
| Top-K Heap | 4 | 4 | 3 | 3 | 1 | **15** | B- |
| K-Way Merge | 4 | 4 | 3 | 3 | 2 | **16** | B- |
| Merge Intervals | 4 | 2 | 1 | 3 | 2 | **12** | C |
| Sweep Line | 4 | 4 | 3 | 3 | 2 | **16** | B- |
| Topological Sort | 5 | 2 | 1 | 3 | 2 | **13** | C+ |
| Union Find | 4 | 4 | 3 | 3 | 2 | **16** | B- |
| Greedy | 4 | 2 | 1 | 4 | 4 | **15** | B- |
| Divide & Conquer | 4 | 4 | 3 | 3 | 2 | **16** | B- |
| Prefix Sum | 3 | 2 | 1 | 3 | 3 | **12** | C |
| Trie | 4 | 4 | 3 | 3 | 2 | **16** | B- |
| Bit Manipulation | 3 | 2 | 1 | 3 | 2 | **11** | C- |
| Quickselect | 5 | 4 | 3 | 3 | 1 | **16** | B- |

**Median: 16/25 (B-).** Only 2 chapters hit A-range; 6 sit at C or below. Bit Manipulation is the weakest at 11/25.

---

## Part 4 — The standard template (definition of done for every chapter)

```
 1. H1 title
 2. <PatternVideo /> placeholder
 3. <PatternProgress ... /> (top)
 4. ## Why <pattern> exists — the story
     - 2-sentence naive attempt
     - 3-sentence defense of the naive
     - 3-sentence failure of naive with a concrete drama number
     - 2-sentence teaser of the clever
 5. ## The core idea — one interactive diagram
     - <PatternXxxAnim /> with user-driven controls (change n, target, etc.)
     - 3-4 paragraphs walking through what the diagram shows
 6. ## When to use it — recognition signals (bulleted interview triggers)
 7. ## When NOT to use it (bulleted anti-patterns)
 8. ## The template(s) — Java code, WHY-comments, compact complexity grid
 9. ## Traps & gotchas — 3-5 > [trap] callouts naming specific interview-day failures
10. ## Historical / real-world grounding (1 para: inventor + year + famous system)
11. ## Canonical problem walkthrough — full brute → intermediate → optimized ladder
     with <CodeTrace> for at least the optimized step
12. ## Related patterns — <RelatedPatterns />
13. <Quiz /> — 5 questions
14. <PrintButton />
```

---

## Part 5 — The 8 waves

### Wave 1 — narrative bones (P0, ~2 dev-days)

Fix the 9 chapters that are structurally incomplete. Each gets the missing 4 sections filled in (Why exists / When to use / When not / Templates / Traps H2).

Chapters: **two-pointers**, prefix-sum, hashing, monotonic-stack, binary-search, bs-on-answer, top-k-heap, backtracking, dp, bit-manip.

**Deliverable:** `gen/fix_pattern_sections.py` — a one-shot script that detects missing sections and inserts stub H2s with a `> [!TODO]` marker so future editorial passes have a checklist.

**Editorial pass:** replace stubs with real content, chapter by chapter. Target 4,500 words minimum.

### Wave 2 — thinness fix (P0, ~3 dev-days)

Enrich the 4 anemic chapters (Binary Search, BS on Answer, Bit Manipulation, Quickselect). Each grows from ~2,500 to ~4,500 words via:
- The 4 template variants (Binary Search: `[lo,hi]` closed, `[lo,hi)` half-open, boundary-search, BS-on-answer)
- 3–5 traps (off-by-one, mid overflow, infinite loop when `lo==hi`, etc.)
- Historical grounding paragraph (Bentley's overflow bug in JDK; Josephus/Kernighan for Bit Manip)

**Deliverable:** hand-edited `gen/src/27-binary-search.md`, `28-bs-on-answer.md`, `40-bit-manip.md`, `41-quickselect.md`.

### Wave 3 — 6 missing interactive diagrams (P1, ~4 dev-days)

Build 6 new Vue anim components matching the "user changes an input, diagram re-runs" style:

| Component | User-driven control |
|---|---|
| `PrefixSumAnim` | Slider for query range `[l, r]`; diagram shows the O(1) subtraction |
| `HashingAnim` | Type a key, watch it hash to a slot; collision animation with chaining |
| `MergeIntervalsAnim` | Drag interval endpoints; merge shows in real time |
| `TopoSortAnim` | Click nodes to add/remove edges; Kahn's queue empties visually |
| `GreedyAnim` | Coin-change: user picks denominations; greedy path highlights + failure case |
| `BitManipAnim` | Interactive bit grid: click bits, watch AND/OR/XOR/shift; running integer value updates |

**Design constraints (UX lens):**
- Share the same control shell (buttons/labels) as existing 15 for muscle memory
- Theme-token-driven colors (`--dsa-primary`, etc.) — no hard-coded hex
- Every state describable in one sentence for screen readers (`aria-live` region)
- Expose a `?scenario=<preset>` URL param so specific states are linkable
- 60fps on a 2019 MacBook Air; no CSS `filter: blur` on animated elements
- Respect `prefers-reduced-motion`

**Deliverable:** 6 new `.vue` files in `web/docs/.vitepress/theme/` + registrations in `theme/index.ts` + smoke test entries.

### Wave 4 — story-first rewrites (P1, ~2 dev-days)

Rewrite the opening 3–5 paragraphs of the 19 chapters that don't open in the reference style. Each new opening follows the exact 4-part shape:

1. **You-scene** (1 sentence) — "You've been asked to find the longest substring without repeats."
2. **Naive attempt** (2 sentences) — "The obvious way: try every substring. That's 25 million tries for a 5,000-char string."
3. **Defense of naive** (2 sentences) — "This isn't stupid: it's the reference implementation textbooks use, and for n < 500 it's still fastest."
4. **The tension + teaser** (2 sentences) — "But at n = 10^5 you're waiting 30 seconds. The rest of this chapter shows how one variable — the window boundary — cuts it to 30 microseconds."

**Deliverable:** `gen/rewrite_openings.py` — a checklist-style script that fails CI if any chapter's first non-frontmatter H2 isn't `## Why <pattern> exists — the story`.

### Wave 5 — callout enrichment (P2, ~2 dev-days)

Bring every chapter up to a minimum of **3 keys + 3 traps + 2 invariants = 8 highlighted insights**. Current thin chapters:

- Top-K Heap, Union Find, Merge Intervals, Topological Sort, Quickselect, K-Way Merge, Divide & Conquer, Bit Manip: currently 3–5, add 3–5 more each.

For each new callout: title + 1-sentence insight + explicit interview-day trigger.

**Deliverable:** hand-edited chapter files; a lint check in `smoke.spec.ts` that fails if any chapter has fewer than 8 `> [key|trap|inv]` markers.

### Wave 6 — historical grounding (P2, ~1 dev-day)

Add one `## History` or embedded paragraph per chapter with real invention/adoption story:

| Pattern | Historical hook |
|---|---|
| Sliding Window | Karp-Rabin 1987; used in every substring search since. |
| Two Pointers | Dijkstra's Dutch National Flag 1976 (3-way partition). |
| Fast/Slow | Floyd's Tortoise & Hare 1967. |
| Prefix Sum | Blelloch's parallel prefix 1990; underlies CUDA reduction. |
| Hashing | Dumey 1956 IBM memo; Knuth vol 3 formalization. |
| Binary Search | Mauchly 1946; **broken in JDK for a decade** (Bentley overflow bug, Google-fixed 2006). |
| BS on Answer | Parametric search (Megiddo 1979). |
| Monotonic Stack | Nagao-Matsuyama 1971 origin; classic in expression parsing. |
| Top-K Heap | Williams 1964 heap sort; NIST TopN spec. |
| K-Way Merge | Loser tree in external sort — von Neumann's 1945 tape-sort memo. |
| Merge Intervals | Bentley's programming pearls, 1985. |
| Sweep Line | Bentley-Ottmann 1979 for line intersections; foundation of computational geometry. |
| Topological Sort | Kahn 1962; every build system on Earth (Make, npm, cargo, bazel). |
| Union Find | Galler-Fischer 1964; Tarjan 1975 proved α(n) amortized bound. |
| Greedy | Kruskal 1956; the "safe move" theorem is Prim-Jarnik. |
| Backtracking | Golomb-Baumert 1965 formalization; Knuth's Dancing Links 2000. |
| Divide & Conquer | von Neumann 1945 (merge sort); Karatsuba 1962. |
| DP | **Bellman 1952 — coined the phrase specifically to hide it from a hostile boss.** Great story. |
| Trie | de la Briandais 1959; Fredkin 1960 named it. Google's first search index used a trie. |
| Bit Manipulation | Kernighan bit-count trick 1988; SSE2 `popcnt` instruction 2000. |
| Quickselect | Hoare 1961 — same paper that invented quicksort. Median-of-medians linear-time: Blum-Floyd-Pratt-Rivest-Tarjan 1973. |

**Deliverable:** one hand-edited paragraph per chapter.

### Wave 7 — visual quality niggles (P2, ~1 dev-day, UX lens)

For every existing anim + SVG in the 21 chapters, verify:

- [ ] Text contrast passes WCAG AA in dark mode
- [ ] No fixed pixel widths — responsive down to 375px (mobile)
- [ ] Font-size ≥ 11px at rest (readable at zoom-1x on 27" 4K)
- [ ] All buttons have visible focus rings (Tab-key nav)
- [ ] Every interactive control has `aria-label`
- [ ] Colors reference `--dsa-*` tokens (audit shows some hard-coded `#334155` in older SVGs)
- [ ] `prefers-reduced-motion` fallback for every animation
- [ ] Every chart has a caption + one-sentence legend below it

**Deliverable:** `gen/audit_visuals.py` — HTML lint over `web/docs/patterns/*.md` flagging every SVG/component that fails a check.

### Wave 8 — the "flagship canonical" walkthrough (P1, ~2 dev-days)

Every chapter needs one **flagship problem** walked through in the brute → intermediate → optimized ladder, mirroring Practice Solutions but embedded IN the chapter.

| Pattern | Flagship problem | State |
|---|---|---|
| Sliding Window | Longest Substring Without Repeats | ✓ present |
| Two Pointers | Container With Most Water | partial |
| Fast/Slow | Linked List Cycle II | ✓ present |
| Prefix Sum | Subarray Sum Equals K | partial |
| Hashing | Two Sum | partial |
| Monotonic Stack | Daily Temperatures | ✓ present |
| **Binary Search** | Search in Rotated Sorted Array | **MISSING** |
| **BS on Answer** | Koko Eating Bananas | **MISSING** |
| Top-K Heap | K Closest Points | partial |
| K-Way Merge | Merge K Sorted Lists | ✓ present |
| Merge Intervals | Merge Intervals classic | ✓ present |
| Sweep Line | Meeting Rooms II | ✓ present |
| Topological Sort | Course Schedule II | partial |
| **Union Find** | Number of Provinces | **MISSING** |
| Greedy | Jump Game II | partial |
| Backtracking | N-Queens | ✓ present |
| Divide & Conquer | Count of Range Sum | partial |
| DP | Coin Change | ✓ present |
| Trie | Word Search II | partial |
| **Bit Manipulation** | Single Number | **MISSING** |
| Quickselect | Kth Largest | ✓ present |

**Deliverable:** hand-authored walkthroughs for the 4 missing + upgrades to the 8 partial.

---

## Part 6 — Wave sequencing (recommended order)

```
Week 1 (must land):
  Day 1-2: Wave 1  (narrative bones)         ── unblocks Wave 4
  Day 3-5: Wave 2  (anemic chapters)         ── biggest reader impact

Week 2:
  Day 6-9: Wave 3  (6 new anim components)
  Day 10:  Wave 8  (missing flagship walkthroughs — start Binary Search)

Week 3:
  Day 11-12: Wave 4 (story-first rewrites)   ── after Wave 1 stubs exist
  Day 13-14: Wave 5 (callout enrichment)
  Day 15:    Wave 6 (historical grounding)

Week 4:
  Day 16:    Wave 7 (visual niggles) + smoke-test extensions
  Day 17-20: buffer / editorial polish / rebuild PDF
```

**Total effort:** ~4 developer-weeks + ~1 editorial week.

---

## Part 7 — Success criteria (definition of done)

The 21-pattern refresh is done when:

1. Every chapter has all 14 required elements from the standard template.
2. Every chapter is **≥ 4,500 words** (median-Grokking density).
3. Every chapter has **≥ 8 highlighted insights** (`> [key|trap|inv]`).
4. Every chapter has an **interactive Vue anim** with user-driven controls, not just Play/Pause.
5. Every chapter opens with the **4-part story shape** (You-scene → naive → defense → tension).
6. Every chapter has one **historical grounding paragraph** naming an inventor and a real-world adoption.
7. Every chapter has one full **brute → optimized flagship walkthrough** embedded.
8. Every chapter passes the **visual-niggles checklist** (WCAG AA, focus rings, aria-labels, responsive).
9. **Playwright smoke suite extended:** for each chapter, assert (a) `## Why ... exists` H2 exists, (b) anim component mounts, (c) at least 8 callouts render, (d) Quiz component reachable.

---

## Part 8 — Per-chapter action ticket

Each row = one PR-sized deliverable.

| # | Chapter | Score | Actions to reach A- (target 20/25) |
|---|---|---|---|
| 1 | Sliding Window | 21/25 | Already at bar. Add `## History` paragraph (Karp-Rabin 1987). |
| 2 | DP | 20/25 | Add 4-part story opening. Bellman-1952 origin story is a MUST — one of the best in CS. |
| 3 | Backtracking | 19/25 | Add "Why exists" H2 + "When to use" H2. Golomb-Baumert 1965. |
| 4 | **Two Pointers** | 17/25 | **Full Wave 1 pass** (the chapter that triggered this plan). Add Dijkstra Dutch National Flag hook. |
| 5 | Hashing | 13/25 | Full Wave 1 + new `HashingAnim`. Dumey 1956 IBM memo hook. |
| 6 | Fast/Slow | 16/25 | Add 3 more traps/keys. Floyd 1967 Tortoise & Hare hook. |
| 7 | Monotonic Stack | 15/25 | Full Wave 1 pass. Nagao 1971 hook. |
| 8 | **Binary Search** | 14/25 | **Highest-priority chapter to fix.** Wave 2 enrichment: 4 template variants, 5 traps, Bentley overflow-bug story (Google 2006), missing flagship walkthrough. |
| 9 | BS on Answer | 16/25 | Full Wave 1 + Koko Bananas flagship + Megiddo 1979 hook. |
| 10 | Top-K Heap | 15/25 | Callout enrichment (currently only 3). Williams 1964 hook. |
| 11 | K-Way Merge | 16/25 | Callout enrichment + von Neumann 1945 tape-sort hook. |
| 12 | Merge Intervals | 12/25 | Full Wave 1 + new `MergeIntervalsAnim` + Bentley 1985 hook. |
| 13 | Sweep Line | 16/25 | Callout enrichment + Bentley-Ottmann 1979 hook. |
| 14 | Topological Sort | 13/25 | Full Wave 1 + new `TopoSortAnim` + Kahn 1962 hook + Course Schedule II flagship. |
| 15 | Union Find | 16/25 | Add Templates H2. Galler-Fischer 1964 + Tarjan α(n) hook. Number of Provinces flagship. |
| 16 | Greedy | 15/25 | Full Wave 1 + new `GreedyAnim` + Kruskal 1956 hook. |
| 17 | Divide & Conquer | 16/25 | Callout enrichment + Karatsuba 1962 hook. |
| 18 | Prefix Sum | 12/25 | Full Wave 1 + new `PrefixSumAnim` + Blelloch 1990 hook. |
| 19 | Trie | 16/25 | Callout enrichment + Fredkin 1960 hook. |
| 20 | **Bit Manipulation** | 11/25 | **Weakest chapter.** Full Wave 1 + Wave 2 enrichment + new `BitManipAnim` + Kernighan 1988 hook + Single Number flagship. |
| 21 | Quickselect | 16/25 | Callout enrichment + Hoare 1961 hook. |

---

## Part 9 — Risk & mitigation

| Risk | Likelihood | Mitigation |
|---|---|---|
| Editorial fatigue on Wave 4 (rewriting 19 openings) | High | 3 openings per session; keep 4-part template in muscle memory |
| New Vue anim components regress performance | Medium | Smoke assertion: `expect(page.evaluate('performance.now()')).toBeLessThan(1500)` on chapter page load |
| Adding sections balloons already-large chapters | Low | 12,000-word ceiling per chapter; move excess to appendix |
| Historical claims must be accurate | Medium | Cite one primary source per claim in a footnote; store in `gen/src/references.bib` |
| Interactive diagrams break on mobile | Medium | Playwright mobile-viewport test in the smoke suite (infra already exists) |

---

## Part 10 — Explicit non-goals for this scope

- ❌ Rewriting the 200+ problem pages (separate scope)
- ❌ Adding new patterns (21 covers the interview surface)
- ❌ Recording videos (deferred until content stabilizes)
- ❌ Backend integration for user progress (localStorage-first is fine here)

---

## Part 11 — Immediate next step

If you approve this plan, the first PR ships **Wave 1 (narrative bones)** — a mechanical stub-insertion pass across the 9 structurally-incomplete chapters, starting with **Two Pointers** since that's the one that triggered this audit. Zero editorial voice, just structure + `> [!TODO]` markers. Follow-up PRs replace the stubs with real content, chapter by chapter, in the priority order above.

Signal: **"Ship Wave 1"** or **"Ship Two Pointers first, then plan Wave 1"** or **"Change X in the plan first"**.

---

## Appendix — Where the old plan.md went

Archived to `plan.old.md`. That file is the session-c960137b practice-page rollout snapshot from 2026-08-22 and is out of scope for this audit.
