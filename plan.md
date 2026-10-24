# Plan — Pattern Chapters, Basic → Advanced

**Date:** 2026-10-24
**Scope:** All 21 core pattern chapters in `gen/src/21-*.md` through `41-*.md`.
**Governing principle:** Every improvement must take the reader **basic → advanced** in the pattern. No chapter upgrade is "done" if it skips the beginner-grounding layer, the full set of sub-variations, OR the advanced extensions. Interview polish alone is not sufficient — the previous Wave-9 plan already brought problem pages to 10/10 against an interview rubric; this plan serves mastery.

---

## Part 0 — Context

### Current state (from audit, 2026-10-24)

The 21 chapters divide along **two axes**, content density and shape. Classifying them on content alone is misleading — a 1244-LOC chapter (sliding-window) can still be shape-weak if the basic layer, template anchor, sub-variation H3s, and advanced tier are missing.

| Content density | Chapters | How to read it |
|---|---|---|
| **Dense** (≥600 LOC, ≥3 CodeTraces, embedded anim, multiple worked examples) | 9: sliding-window, two-pointers, hashing, prefix-sum, bs-on-answer, greedy, backtracking, dp, bit-manip | Already has the material — needs shape + advanced tier |
| **Medium** (300-600 LOC, structure 50-60%) | 5: monotonic-stack, trie-pattern, top-k-heap, topo-sort, union-find | Needs shape + 2-5 missing sub-variations |
| **Light** (<300 LOC, 1-2 CodeTraces) | 7: **binary-search (FLAGSHIP)**, fast-slow, quickselect, merge-intervals, sweep-line, k-way-merge, divide-conquer | Needs the full build — shape, sub-variations, visuals, advanced tier |

Total: 21 chapters. (Earlier audit miscounted at 20 — `35-greedy.md` was missed and is now included.)

**Shape audit (what every chapter needs regardless of density):** 11 of 21 chapters are missing an explicit `## THE template` H2; 20 of 21 are missing `## The bare mechanic`; ~18 of 21 are missing a named `## Sub-variations of the template` section (the sub-variations exist as problem walkthroughs but aren't flagged as specializations); 21 of 21 are missing `## Advanced`; `<StepStrip>` is used in 1 of 21.

**Consequence:** no chapter is "done" without a shape pass + advanced tier. The density band only tells you how much writing is left after the shape pass — not whether the shape pass is needed.

### The three biggest leverage gaps

1. **"THE template" is not a clear H2** in 11/21 chapters. Templates are either scattered inside problem walkthroughs or folded under "How to use." A beginner cannot answer "what's the one shape I should memorize for this pattern?" from the current layout.
2. **`<StepStrip>` is used in exactly 1 chapter (hashing).** This is the single highest-leverage visual aid for seeing a pattern in action — a step-by-step trace of state over time — and it's effectively absent across 20 of 21 chapters.
3. **Sub-variation worked examples live outside the chapter.** The important problems that teach the pattern's full range (Insert Interval, Lower/Upper Bound, Happy Number, Find Median from Stream, Alien Dictionary, …) exist as problem pages but aren't pulled INTO the pattern chapter. A reader finishes the chapter without seeing the pattern applied beyond its one canonical example.

### What "basic → advanced" means per chapter

Each chapter must deliver three layers, in order:

**Basic (ground floor):** The bare mechanic shown in two lines on the simplest possible input, with one tiny visual, BEFORE any optimized version. Many chapters today open at the clever form — a beginner has nowhere to stand first.

**Intermediate (full variation surface):** Every common sub-variation of the pattern, each with its own template-diff from the standard template, its own worked example, and its own one-visual step-by-step trace. A learner who finishes the intermediate layer can recognize and apply the pattern to any problem in its canonical interview range.

**Advanced (depth to mastery):** Hard variants, "what if…" interview follow-ups, the pattern's known breaking points, and the one or two problems where the pattern meets another (sliding window + hashing, binary search + DP, backtracking + trie). Mostly absent today, even in the RICH chapters.

---

## Part 1 — The chapter template every pattern must match

Target 17 sections, in this order. Mandatory sections marked **[M]**. Mastery-tier mandates (what makes this a mastery curriculum rather than a reference) marked **[MASTERY]**.

```
1.  H1 title
2.  <PatternVideo />
3.  <PatternProgress />
4.  <PatternSubVariationNav />                                    [NEW infra]
5.  <DueForReview scope="this-chapter" />                         [MASTERY]
      (shows "N sub-variations due in this chapter" when the reader has
      past interactions. 0 on first visit — invisible then.)
6.  ## Why <pattern> exists — the story                           [M]
      (naive → defense of naive → failure with drama number → tension teaser)
7.  ## The bare mechanic — simplest working example               [M, BASIC layer]
      (2–5 lines of code on a 4-element input, one tiny SVG; no cleverness.
      Explicit "this is NOT the production version; it is the shape you must
      first see work.")
8.  ## When to use it — recognition signals                       [M]
9.  ## When NOT to use it                                         [M]
10. ## THE template                                               [M, INTERMEDIATE anchor]
      <PatternTemplateCard>                                       [NEW infra]
        - one canonical, reusable code block, wrapped in <TemplateReveal>
          so the learner can attempt-then-reveal                 [MASTERY]
        - <InvariantProof> with init / maintenance / termination  [MASTERY — replaces InvariantPanel]
        - complexity row
        - <AmortizedPanel> for the 6 patterns needing it          [MASTERY]
          (monotonic-stack, union-find, two-pointers, sliding-window,
           quickselect, DP space-optimization)
        - "specializations" row linking to each sub-variation H3 in §11
11. ## Sub-variations of the template                             [M, INTERMEDIATE]
      One H3 per flavor (≥3 required). Each H3 contains:
        a. Problem statement + example input/output
        b. Template-diff from §10 (just the lines that change)
        c. <StepStrip> visual trace                               [NEW infra]
        d. Java inside <TemplateReveal> + <CodeTrace> on hot path [MASTERY on TemplateReveal]
        e. <InvariantProof> for THIS specialization's invariant   [MASTERY]
        f. <MarkSolved> button registering the sub-variation
           in the spaced-review schedule                          [MASTERY]
        g. Complexity row and one-liner "when to pick THIS variant"
12. ## Traps & gotchas                                            [M]
      ≥3 named failure modes rendered as <TrapTrace> embeds       [MASTERY]
      (buggy code → trip input → wrong output → diagnosis → fix),
      plus a tail of further `> [trap]` callouts for named modes
      the TrapTrace doesn't walk.
13. ## History                                                    [M]
      Inventor + year + a real-world adoption line.
    ### In the wild                                               [MASTERY]
      One ~10-line snippet from a real OSS project (JDK, Spring,
      PostgreSQL, Redis, Kafka, Linux kernel, …) using this pattern,
      with a link to the source. Named explicitly: "here is this
      pattern outside LeetCode."
14. ## Interactive diagram                                        [M]
      <XxxAnim /> with 3-paragraph walkthrough. User-driven controls preferred.
15. ## Recognition drill                                          [MASTERY]
      <RecognitionDrill pattern="<slug>" count="10" />
      Pulls 10 problem statements with hidden tags from
      recognition.problems.json. Reader guesses "does this pattern
      apply, and if yes which sub-variation?" before revealing.
      Scores persisted; "retake" link to /recognize?pattern=<slug>.
      Cross-link to /mixed-drill for interleaved practice across all 21.
16. ## Advanced — follow-ups and failure modes                    [M, ADVANCED layer]
      - 3–5 "what if…" interview follow-ups with crisp answers
      - 1–2 known breaking points of the pattern (when to switch tools)
      - ≥3 cross-pattern problems (where this pattern meets another)
                                                                  [MASTERY — upgraded from 1 to ≥3]
      - For the 6 amortized patterns: ### Why the amortized bound
        H3 with the aggregate / accounting / potential derivation
        and a worked numeric example                              [MASTERY]
17. ## Related patterns + Check your understanding
      <RelatedPatterns />, <Quiz /> (5 questions, mastery-tuned:
      1 on invariant, 1 on sub-variation specialization, 1 on trap,
      1 on advanced follow-up, 1 on cross-pattern recognition),
      <PrintButton />
```

**Section lengths (soft guidance, not CI):**

- §6 story: 4 paragraphs.
- §7 bare mechanic: ≤80 lines total.
- §10 THE template: ≤120 lines total.
- §11 each sub-variation: 60–150 lines.
- §15 recognition drill: self-rendering, ~0 markdown LOC.
- §16 advanced: ≥250 lines (bumped from 200 to accommodate 3+ cross-pattern problems and amortized derivation H3).
- Chapter total: 900–1700 lines (vs current spread of 300–1500).

**Lint-worthy (optional CI additions):**

- Fail if `## The bare mechanic` is missing.
- Fail if `## THE template` is missing.
- Fail if `## Sub-variations of the template` has fewer than 3 H3 children.
- Fail if `## Advanced` is missing.
- Fail if `## Recognition drill` is missing.                                      **[MASTERY]**
- Fail if `## In the wild` H3 is missing under §13 History.                        **[MASTERY]**
- Fail if any `<InvariantProof>` has empty `initialization`/`maintenance`/`termination`. **[MASTERY]**
- Fail if `<TrapTrace>` appears fewer than 3 times in the file.                    **[MASTERY]**
- Fail if a pattern marked `requiresAmortized: true` has no `<AmortizedPanel>`.    **[MASTERY]**
- Fail if `patterns.subvariations.json` lists a sub-variation that doesn't appear as an H3 in §11.
- Fail if `recognition.problems.json` has fewer than 10 entries for the pattern.   **[MASTERY]**

---

## Part 2 — Shared infra to build first

These components get built once and consumed by every chapter upgrade. Prioritized by leverage. **Mastery infra (P1.5) is the delta from the earlier plan** — recognition drills, blind-solve, tripartite invariant proofs, and amortized-complexity derivations are what turn comprehension into mastery. They land in Phase 1 so every chapter upgrade can consume them from day one.

### P1 — Visual + shape infra (~2 days)

1. **`PatternTemplateCard.vue`** — the canonical presentation card for "THE template" in §9. Props: `code`, `language`, `invariant`, `complexity: {time, space}`, `specializations[]`. Renders the code with syntax highlighting, the invariant proof slot below it, the complexity row, and a chip row linking to each sub-variation H3 in the chapter. One per chapter, consistent slot, impossible to miss. Internally mounts an `<InvariantProof>` and (when the pattern needs it) an `<AmortizedPanel>`.

2. **`StepStrip.vue` generalization + 6 specialization wrappers** — the step-by-step visual trace. Current `StepStrip.vue` is bespoke per-chapter; generalize to accept `{states: Array<State>, narration: string[], highlight: HighlightSpec}`. Then publish:
   - `WindowTraceStrip` (sliding-window, two-pointers)
   - `BinarySearchStepStrip` (binary-search, bs-on-answer)
   - `PartitionStepStrip` (quickselect, dutch-flag two-pointers)
   - `IntervalRibbon` (merge-intervals, sweep-line)
   - `EventTimelineStrip` (sweep-line variants)
   - `LinkedListStepStrip` (fast-slow)
   Each specialization is ~80-120 LOC Vue consuming the generalized core.

### P1.5 — Mastery drill infra (~5 days) — **the delta that turns comprehension into mastery**

3. **`InvariantProof.vue`** — replaces the simpler `InvariantPanel` from the earlier plan. The one-line invariant is still prominent at the top, BUT below it a collapsible three-part proof is required: **Initialization** (holds on entry), **Maintenance** (holds after each loop iteration / recursive call), **Termination** (what the invariant implies at exit). Props: `statement`, `initialization`, `maintenance`, `termination`. The three parts render as a horizontal strip of three cards when expanded. One-line statements without the proof are rejected by lint. Mandatory on every §9 THE template and every §10 sub-variation H3.

4. **`TemplateReveal.vue`** (promoted from P4 nice-to-have to P1.5 mandatory). The learner is shown the problem shape and the invariant; a textarea invites them to type the template themselves (optional but encouraged). The canonical template is hidden until they click "Reveal canonical template." On reveal, if they typed something, the component diffs their attempt against canonical line-by-line and highlights divergences. Blind-solve drills template memorization WITHOUT framing it as a test — the reveal is one click away. Persistence: whether a reader revealed vs attempted-first is tracked in localStorage via existing `storage.setJson('dsa-template-reveal:...')`. Mandatory wrapping every §10 sub-variation code block.

5. **`RecognitionDrill.vue`** — a per-chapter drill block typically at the end of §10 or in §13. The reader is shown 5-10 problem *statements* with the pattern tag hidden. For each, they guess: "does this pattern apply here, YES/NO/MAYBE and if yes, which sub-variation?" The component reveals the tag and the matching sub-variation after each guess, scores the reader, and persists the score to `storage.setJson('dsa-recognition:<pattern>', ...)`. Reads problem list from `recognition.problems.json`. Mandatory per chapter.

6. **`recognition.problems.json`** — single source of truth for recognition drills. Shape: `{ "<pattern-slug>": [{ "statement": "...", "subVariation": "<slug>" , "distractors": ["<other-pattern-slug>", ...] }, ...] }`. Each pattern needs ≥10 entries; distractors are the other patterns the problem could plausibly be mistaken for. Enforces that recognition is drilled against the hard-to-tell-apart cases (sliding-window vs two-pointers, backtracking vs DP, mono-stack vs mono-deque).

7. **`AmortizedPanel.vue`** — a boxed component rendering the amortized-complexity *derivation*, not just the statement. Props: `method: 'aggregate' | 'accounting' | 'potential'`, `argument` (markdown), `workedExample` (optional numeric trace showing credits/potential over time). Mandatory for the 6 patterns where amortized analysis IS the content: monotonic-stack (O(n) via each-element-pushed-popped-at-most-once), union-find (α(n) via path compression + union-by-rank), two-pointers (O(n) via "sum of l-advances + r-advances ≤ 2n"), sliding-window (O(n) via the same argument), quickselect (O(n) expected via linearity + randomized pivot), DP space-optimization (O(k) via rolling arrays).

8. **`<TrapTrace>` mandate** — the component already exists in the repo (used in 1 chapter). The upgrade is not building it, but requiring ≥3 `<TrapTrace>` embeds per chapter — each showing the buggy code, the input that trips it, the wrong output, and the fix. Updates `patterns.subvariations.json` to also list `requiredTraps[]` per chapter.

9. **`<DueForReview>` + `<MarkSolved>` chapter integration** — both components exist. The upgrade is requiring every chapter to register its sub-variations in the spaced-review schedule on page load (via a `<script setup>` block that calls the existing storage helpers) and surface a "N items due in this chapter" counter at the top. Also adds a global `/review` page listing all due items across all 21 chapters.

10. **`/recognize` + `/mixed-drill` site-level pages** — two new pages at the site root, both backed by `recognition.problems.json`. `/recognize` runs the drill scoped to one pattern (chapter-local link). `/mixed-drill` picks N problems *randomly across all 21 patterns*, forcing interleaved recognition — the mastery-level test. Both pages use `RecognitionDrill` in different source modes.

### P2 — Chapter navigation (~1 day)

11. **`PatternSubVariationNav.vue`** — top-of-chapter mini-ToC filtered to the §10 H3s, so the user sees "this chapter covers 5 sub-variations" before diving in. Reads from `patterns.subvariations.json`.

12. **`patterns.subvariations.json`** — single source of truth listing the required sub-variations per pattern. Example:
    ```json
    {
      "binary-search": {
        "subVariations": [
          { "slug": "lower-upper-bound", "title": "Lower / upper bound" },
          { "slug": "rotated", "title": "Rotated sorted array" },
          { "slug": "peak-bitonic", "title": "Peak in bitonic array" },
          { "slug": "2d-matrix", "title": "Search 2D matrix" },
          { "slug": "first-last-position", "title": "First and last position" }
        ],
        "requiredTraps": 3,
        "requiresAmortized": false,
        "inTheWildSource": "jdk.util.Arrays.binarySearch"
      },
      ...
    }
    ```
    Consumed by `PatternSubVariationNav`, `RecognitionDrill`, the review scheduler, and an optional CI smoke test.

### P3 — DP infra (~3 days, after DP chapter is prioritized)

13. **`DpTableAnim.vue`** — generalize the existing `DpFillAnim` to render any DP table (1D / 2D / interval / bitmask / grid) from a JSON spec of `{dims, transitions[]}`. The DP chapter would use it ~10 times; grid-DP and backtracking chapters would use it 1-2 times each.

### P4 — Grid infra (~2 days, defer until Phase 3)

14. **`GridPathAnim.vue`** — shared by grid-DP, grid-backtracking, Word Search II (trie). Currently each chapter inlines its own grid SVG.

---

## Part 3 — Per-chapter upgrade plan

### Mastery additions that apply to **every** chapter uniformly

The 21 per-chapter specs below call out the pattern-specific **basic / intermediate / advanced** work. In addition, every chapter upgrade — regardless of band — must deliver the following mastery additions (defined once here so each spec below stays focused on content, not boilerplate):

1. **`<DueForReview scope="this-chapter" />`** at the top of the page (above §6 Why).
2. **Every §10 THE template and every §11 sub-variation H3** wraps its code block in `<TemplateReveal>` (blind-solve: textarea → reveal → diff).
3. **Every invariant** (§10 and each §11 H3) uses `<InvariantProof>` with init / maintenance / termination — never the one-line statement alone.
4. **≥3 `<TrapTrace>` embeds** in §12 Traps & gotchas: buggy code → trip input → wrong output → diagnosis → fix. Additional traps may remain as `> [trap]` callouts.
5. **One `## In the wild` H3** under §13 History: a ~10-line real OSS snippet showing the pattern in production, with source link.
6. **One `<RecognitionDrill pattern="<slug>" count="10" />` block** at §15 Recognition drill. Backed by ≥10 entries in `recognition.problems.json` for that pattern, each with 2-3 distractor patterns the problem could plausibly be mistaken for.
7. **A `<MarkSolved>` button** inside every §11 sub-variation H3 that registers the item in the spaced-review schedule on click.
8. **≥3 cross-pattern problems** in §16 Advanced (upgraded from the earlier plan's "≥1"). Named examples: "where pattern X meets pattern Y."

### Mastery additions that apply to **specific** chapters only

- **`<AmortizedPanel>` + `### Why the amortized bound` H3 in §16** — mandatory for the 6 patterns where amortized analysis IS the content:
  - **`26-monotonic-stack`** — aggregate method (each element pushed and popped at most once → total O(n) across all ops).
  - **`34-union-find`** — potential method (Ackermann's inverse α(n), bound = O((m+n) α(n)) under path compression + union-by-rank). Worked example tracking rank changes over 10 ops.
  - **`22-two-pointers`** — aggregate (`l` and `r` each monotone, so advances summed ≤ 2n).
  - **`21-sliding-window`** — aggregate (same argument as two-pointers, applied to window ends).
  - **`41-quickselect`** — expected analysis via linearity of expectation on randomized pivot (not a true amortized bound, but belongs here as "the complexity derivation that is the content").
  - **`38-dp`** — specifically the DP-space-optimization sub-topic: rolling-array amortizes 2D DP memory down to O(min(rows, cols)); the derivation lives here.

- **`<InTheWild>` snippet suggestions** (not binding — pick the clearest real example):
  - sliding-window → `java.util.concurrent.atomic.LongAdder` rate-limit windows, or Linux kernel's connection tracker.
  - two-pointers → PostgreSQL's merge-join operator.
  - fast-slow → the libc GNU malloc free-list cycle check.
  - prefix-sum → NumPy `np.cumsum`, or TensorFlow's `tf.cumsum` XLA kernel.
  - hashing → the JDK 8 `HashMap` tree-ification threshold logic.
  - monotonic-stack → the LLVM constant-propagation worklist (uses a stack with ordering guarantees).
  - binary-search → `java.util.Arrays.binarySearch` with the off-by-one documentation.
  - bs-on-answer → Kubernetes scheduler's bin-packing feasibility check.
  - top-k-heap → Elasticsearch top-N aggregation.
  - k-way-merge → the external sort step in PostgreSQL's `tuplesort.c`.
  - merge-intervals → Google Calendar's conflict-detection path.
  - sweep-line → Mapbox's label-collision avoidance.
  - topo-sort → Make / Bazel's build-DAG scheduler, or Spring's `@DependsOn` resolution.
  - union-find → Git's object-reachability check during fetch; incremental graph libraries.
  - greedy → Linux kernel's CFS task scheduler (which is partly greedy on vruntime).
  - backtracking → PostgreSQL's query planner join-order search (bounded backtracking).
  - divide-conquer → NumPy's FFT (Cooley-Tukey).
  - DP → the Levenshtein-distance implementation in `git diff`, or SQLite's `likelihood()`.
  - trie-pattern → Google's QUIC URL-router or `java.util.jar.JarFile`'s manifest trie.
  - bit-manip → the JDK `Integer.bitCount` with its popcnt intrinsic, or Linux kernel bitmask ops.
  - quickselect → NumPy's `np.partition`.

---

### The 7 Light chapters (priority order)

#### 1. `27-binary-search.md` — FLAGSHIP, highest priority

**Why first:** It's the most-cited pattern in interviews, currently the thinnest WEAK chapter, and the ideal pattern to demonstrate basic → advanced (easy to teach the bare mechanic, rich sub-variations, clean advanced tier). Fixing it establishes the standard every other chapter copies.

**Basic layer to add:**
- "The bare mechanic" section showing `[lo, hi)` half-open on a 6-element sorted array for value `=`. 15 lines of Java, one tiny trace diagram.
- Explicit statement: "every binary search in this chapter is a specialization of this exact loop. Memorize this and the specializations become one-line diffs."

**Intermediate layer — sub-variations H3s (5):**
- `lower_bound` / `upper_bound` — the comparison predicate and what it returns. Worked on "find first position ≥ target."
- Search in rotated sorted array — "which half is sorted?" pivot check.
- Peak in bitonic array — comparing `a[mid]` with `a[mid+1]`.
- Search 2D matrix — treat the row-major-sorted matrix as a flat sorted array; cell = `(idx/cols, idx%cols)`.
- Find first and last position — two bounds, same template, different predicate.
Each H3 gets a `BinarySearchStepStrip` showing `lo, mid, hi` per iteration on a concrete input.

**Advanced layer:**
- "What if the sorted array has duplicates and we must find the FIRST occurrence?" — leads to lower_bound reasoning.
- "What if you can only call a function `isBad(k)` that returns a boolean and is monotone?" — bridges to BS-on-answer.
- "What if the array is on disk and random access costs 10ms?" — hybrid interpolation + galloping search.
- Breaking point: unsorted or sorted-with-partial-rotation-pivot-unknown.
- Cross-pattern: "Median of Two Sorted Arrays" — BS over the partition index.

**Visuals:**
- `BinarySearchStepStrip` on the bare mechanic (5 steps on `[1,3,5,7,9,11]` finding `7`).
- Rotated-array SVG showing the two sorted halves and the pivot.
- Bitonic SVG showing the "ascending → descending" shape.
- 2D matrix SVG with the index flattening.

**Promote these problem pages into the chapter as walkthroughs:** `find-first-and-last-position`, `find-peak-element`, `search-a-2d-matrix-ii`, `binary-search-rotated-sorted`.

---

#### 2. `23-fast-slow.md`

**Basic layer to add:**
- "The bare mechanic" showing hare-tortoise on a 6-node linked list without a cycle, then with. The pointer positions after each step as a tiny table.

**Intermediate layer — sub-variations H3s (5):**
- Linked List Cycle II (where the cycle starts — Floyd's lemma).
- Middle of a linked list (fast moves 2, slow moves 1, slow lands at middle).
- Nth node from end (fast-ahead-by-N, then both advance in lockstep).
- Happy Number (array/number sequence treated as a linked list for cycle detection).
- Find the Duplicate Number (array as a linked list; cycle detection finds the duplicate).

**Advanced layer:**
- "What if the sequence is only partially cyclic (ρ-shape with a tail)?" — leads to the cycle-length / cycle-entry lemma.
- "What if memory is tight and you cannot modify the list?" — the fast-slow pointer is why this pattern exists; compare against the HashSet approach.
- Cross-pattern: Floyd's algorithm as the proof backbone of Brent's algorithm (improved cycle detection).

**Visuals:**
- `LinkedListStepStrip` showing hare and tortoise positions per step for 4 of the 5 sub-variations.

**Promote:** `happy-number`, `find-the-duplicate-number`, `middle-of-the-linked-list`, `remove-nth-node-from-end`.

---

#### 3. `41-quickselect.md`

**Basic layer:**
- "The bare mechanic" showing one pass of Lomuto partition on a 6-element array for finding the 3rd smallest.

**Intermediate layer — sub-variations H3s (3):**
- Median via quickselect (two calls for even-length).
- Top-K via quickselect vs. heap-of-K — decision subsection with a complexity table side-by-side.
- Hoare vs. Lomuto pivot — invariants compared, bugs each is prone to.

**Advanced layer:**
- "What if the input is adversarial and quickselect degenerates to O(n²)?" — introduce median-of-medians (BFPRT), state the O(n) worst-case bound, note that the constant is bad enough that quickselect is still preferred in practice.
- "What if you need the top-K and the stream is unbounded?" — can't use quickselect; must use heap-of-K.
- Cross-pattern: Kth Smallest in a BST (completely different approach — in-order traversal, no partitioning).

**Visuals:**
- `PartitionStepStrip` on one Lomuto pass (one swap at a time, highlighting pivot and the growing "known-smaller" prefix).

**Promote:** `wiggle-sort-ii`, `kth-smallest-element-in-a-sorted-matrix`.

---

#### 4. `31-merge-intervals.md`

**Basic layer:**
- "The bare mechanic" — sort by start, then one-pass fold: either extend the last interval or append a new one. 10 lines of Java on `[[1,3],[2,6],[8,10],[15,18]]`.

**Intermediate layer — sub-variations H3s (4):**
- Classic Merge Intervals.
- Insert Interval (no need to sort — overlap-while-left-is-before-new, then append-and-skip-overlap, then append-rest).
- Non-overlapping Intervals (greedy by end — minimum deletions to make non-overlapping).
- Meeting Rooms I (just a sort + overlap-check for a boolean).

**Advanced layer:**
- "What if intervals are coming as a stream?" — switch to a TreeMap keyed by start.
- "What if intervals carry weights and you want the max-weight non-overlapping subset?" — leads to DP on sorted intervals (Weighted Interval Scheduling).
- Breaking point: when the interval count exceeds memory, you must switch to a sweep-line approach (see §32 sweep-line).
- Cross-pattern: Meeting Rooms II is in sweep-line, not here — explain why.

**Visuals:**
- `IntervalRibbon` showing the 1D interval layout for each of the 4 variants.

**Promote:** `insert-interval`, `non-overlapping-intervals`, `interval-list-intersections`.

---

#### 5. `32-sweep-line.md`

**Basic layer:**
- "The bare mechanic" — represent each interval as two events (`+1` at start, `-1` at end), sort events by time, sweep accumulating. Show on 3 overlapping intervals computing max simultaneous.

**Intermediate layer — sub-variations H3s (4):**
- Meeting Rooms II (classic event sweep).
- Car Pooling (diff-array sweep when timeline is bounded and discrete).
- The Skyline Problem (sweep + max-heap for active heights).
- Employee Free Time (sweep merging intervals from multiple sorted lists).

**Advanced layer:**
- "What if events are weighted or carry metadata?" — Bentley-Ottmann for line intersections.
- "What if the sweep direction matters?" — rectangle union area (sweep by x, track active y-ranges).
- Breaking point: 2D sweep problems rapidly become O(n²) without a secondary structure (segment tree, balanced BST).
- Cross-pattern: Range Addition problems are a 1D sweep over a diff-array, same idea applied to arrays instead of events.

**Visuals:**
- `EventTimelineStrip` showing event-by-event state transitions.

**Promote:** `car-pooling`, `the-skyline-problem`, `employee-free-time`, `my-calendar-ii`.

---

#### 6. `30-k-way-merge.md`

**Basic layer:**
- "The bare mechanic" — a min-heap of (value, list-index, element-index) tuples; pop smallest, push its successor. Show on 3 sorted lists of 3 elements each.

**Intermediate layer — sub-variations H3s (3):**
- Classic Merge K Sorted Lists.
- Find K Pairs with Smallest Sums (k-way over Cartesian products with a visited-set).
- Find Median from Data Stream (two-heap variant — bridges to top-K-heap chapter).

**Advanced layer:**
- "What if K is very large (K ≈ N)?" — switch to pairwise merging in rounds (merge-sort step), O(N log K) → O(N log N).
- "What if the lists are themselves streamed?" — tournament / loser tree used in external sort.
- Breaking point: when K is small (≤ 10) and lists are short, direct nested loops often win on cache locality.

**Visuals:**
- Heap-state visualization at 3 successive pops.

**Promote:** `find-k-pairs-with-smallest-sums`, `find-median-from-data-stream`.

---

#### 7. `37-divide-conquer.md`

**Basic layer:**
- "The bare mechanic" — classic merge sort shown on 8 elements, with the "divide, conquer, merge" phases labeled explicitly.

**Intermediate layer — sub-variations H3s (4):**
- Merge Sort as the canonical shape.
- Pow(x, n) by binary exponentiation.
- Count of Smaller Numbers After Self (defer counting until the merge step — the key D&C trick).
- Majority Element (D&C variant — compare top-of-left to top-of-right).

**Advanced layer:**
- "What if the problem reduces to d dimensions?" — Closest Pair of Points in 2D (O(n log n) via D&C + strip merge).
- "What if the recursive subproblems overlap?" — switch to DP.
- Breaking point: when the merge step is itself O(n²), the total is O(n² log n), worse than iterative O(n²).
- Cross-pattern: Quicksort is D&C where the "merge" is a no-op — compare partitioning cost vs. merging cost.

**Visuals:**
- Recursion tree SVG showing the halving + merge-up for each sub-variation.

**Promote:** `powx-n`, `majority-element` (D&C variant), `count-of-smaller-numbers-after-self`.

---

### The 5 Medium chapters — shape normalization + sub-variation gap-fill

Each needs the same shape pass as the Dense band: `## The bare mechanic`, `## THE template` (`PatternTemplateCard`), §10 sub-variations H3 rename, per-sub-variation visuals, `## Advanced`. The difference from Dense is that these chapters are also thin on sub-variation coverage (2-3 current walkthroughs, not 5-9), so each gets 2-3 new H3s added. ~1.5 days each.

---

#### `26-monotonic-stack.md` (611 LOC, 2 walkthroughs — Daily Temperatures, Largest Rectangle)

**Current:** Standard shape, 2 walkthroughs. Missing: bare mechanic, template card, H3 rename, Advanced, 3 sub-variations.

**Basic layer:** §6 "Next Greater Element on `[2, 1, 2, 4, 3]`" — walk left-to-right, pop smaller, push current, output the stack top at pop-time. Show the stack contents at each of 5 steps. 15 lines Java, one `MonoStackAnim` snippet (existing component).

**Intermediate:** §9 `PatternTemplateCard` with 2 tabs: `next-greater-to-right` (push, pop-smaller), `next-greater-to-left` (reverse direction or dual-pass). §10 H3s: next-greater-element-right, next-greater-element-left (new), daily-temperatures (= NGE-right with index diff), stock-span (new — NGE-left variant), largest-rectangle-in-histogram, remove-k-digits (new — lexicographic greedy via mono-stack), 132-pattern (new — the three-element variant). Each H3 gets a `MonoStackAnim` state at 4-5 steps.

**Advanced:** "What if the stack must support min AND max?" (two mono-stacks, one monotone-increasing, one monotone-decreasing — bridges to monotonic-deque). "What if the elements come in reversed and you need the OTHER side?" (dual-pass trick). "What if the problem is 2D, not 1D?" (Maximum Rectangle in binary matrix = Largest Rectangle on each row's histogram). "What if the elements are distances in a sliding window?" (sliding-window maximum via mono-deque — surface the §21 sliding-window chapter's problem 7 as the sliding version of this pattern). Breaking point: when the "greater than" relation isn't transitive on the input — mono-stack no longer valid. Cross-pattern: Trapping Rain Water admits BOTH two-pointer and mono-stack solutions — recognition drill.

**Visuals:** 7 × reuse `MonoStackAnim`.

**Promote:** 2 H2s → H3s; add 5 new H3s (NGE-right, NGE-left, stock-span, remove-k-digits, 132-pattern).

**Estimated:** 1.5 days.

---

#### `29-top-k-heap.md` (405 LOC, 2 walkthroughs — K Closest Points, Kth Largest/Top K Frequent)

**Current:** Standard shape, 2 walkthroughs. Missing: bare mechanic, template card, H3 rename, Advanced, 3-4 sub-variations.

**Basic layer:** §6 "Find the 3 smallest in `[7, 2, 5, 1, 9, 4, 6]`." Keep a max-heap of size 3; push each, if size > 3 pop. Show the heap state at each of 7 steps. 12 lines Java, one `HeapAnim` snippet (existing component).

**Intermediate:** §9 `PatternTemplateCard` with 3 tabs: `heap-of-k` (bounded buffer), `two-heaps` (median stream — min-heap top half + max-heap bottom half), `heap-with-lazy-deletion` (sliding-window median). §10 H3s: top-k-smallest (new — bare-mechanic promoted), top-k-frequent, k-closest-points-to-origin, kth-largest-in-array, find-median-from-data-stream (new — the two-heap canonical), merge-k-sorted-lists (cross-link to §30 k-way-merge), task-scheduler (new — cross-link to §35 greedy). Each H3 gets a heap-state visual at 3-4 steps.

**Advanced:** "What if K is very small (K ≤ 10) and N is huge?" (heap-of-K dominates quickselect by cache locality; benchmark). "What if the data is streamed and you need the median at any point?" (two-heap canonical — exact algorithm with the balance invariant). "What if you need the median of a SLIDING window of size k?" (two-heap with lazy deletion via a `delayed` hashmap — tricky). "What if you need the K-th order statistic once (not top-K)?" (switch to quickselect — bridges to §41). "What if the heap must support decrease-key (Dijkstra)?" (Java's `PriorityQueue` doesn't — use TreeSet<long[]> or a Fibonacci-heap implementation). Breaking point: when the comparator breaks reflexivity (NaN, non-total order) → runtime errors. Cross-pattern: top-K via heap (O(N log K)) vs top-K via quickselect (O(N) average) — recognition drill.

**Visuals:** 7 × reuse `HeapAnim`.

**Promote:** 2 H2s → H3s; add 5 new H3s (top-k-smallest, kth-largest, median-from-stream, merge-k-cross-link, task-scheduler-cross-link).

**Estimated:** 2 days (median-from-stream and sliding-window-median are both involved).

---

#### `33-topological-sort.md` (460 LOC, 2 walkthroughs — Course Schedule II, Course Schedule)

**Current:** Standard shape, §Kahn vs DFS, §Building the graph, 2 walkthroughs. Missing: bare mechanic, template card, H3 rename, Advanced, 2-3 sub-variations.

**Basic layer:** §6 "Topo sort on `0→1, 0→2, 1→3, 2→3`" using Kahn's. Show in-degree table over 4 steps as nodes are removed. 15 lines Java, one `TopoSortAnim` snippet (existing component).

**Intermediate:** §9 `PatternTemplateCard` with 2 tabs: `kahn-bfs` (in-degree queue), `dfs-postorder` (reverse postorder). Each `InvariantPanel` names its invariant (Kahn: "queue holds all nodes with in-degree 0"; DFS: "postorder reversed = topo order on a DAG"). §10 H3s: course-schedule-i (cycle detect), course-schedule-ii (one topo order), alien-dictionary (new — build graph from relative order of strings), minimum-height-trees (new — trim leaves iteratively, dual of Kahn), parallel-courses (new — level-wise BFS gives the min semesters), sequence-reconstruction (new — unique topo order check). Each H3 gets a `TopoSortAnim` state at 3-4 steps.

**Advanced:** "What if the graph has a cycle and you must find it?" (DFS with WHITE/GRAY/BLACK — gray-on-gray is the back edge). "What if updates come at runtime?" (incremental topo sort — maintain approximate order and repair). "What if the ordering has multiple valid results?" (all topo orders via backtracking — exponential, when it's acceptable). "What if the graph is implicit?" (Alien Dictionary builds the graph from input — the usual real challenge). Breaking point: when the "DAG" has cycles — topo sort returns partial order; need Tarjan's SCC first to collapse cycles, then topo-sort the condensation. Cross-pattern: shortest path in a DAG uses topo order + relaxation (bridges to graph algorithms).

**Visuals:** 6 × reuse `TopoSortAnim`.

**Promote:** 2 H2s → H3s; add 4 new H3s (alien-dictionary, minimum-height-trees, parallel-courses, sequence-reconstruction).

**Estimated:** 1.5 days.

---

#### `34-union-find.md` (510 LOC, 2-3 walkthroughs — Number of Provinces, Union-Find, Kruskal MST)

**Current:** §Why, §When, §History, §Canonical (Number of Provinces), 3 problem H2s. Missing: bare mechanic, template card, §When NOT, §Templates, §Traps, H3 rename, Advanced, 2 sub-variations.

**Basic layer:** §6 "Union-find on 5 nodes." Initialize `parent[i] = i`; union(0,1); union(2,3); find(0) vs find(2). Show the parent-array state after each op. 15 lines Java, one `UnionFindAnim` snippet (existing component).

**Intermediate:** §9 `PatternTemplateCard` with 2 tabs: `path-compression` (iterative find with parent-rewrite), `union-by-rank` (keep tree shallow). `InvariantPanel`: "find(x) is the root of x's tree; two nodes connected ⟺ find(a) == find(b)." §10 H3s: basic-dsu (new — bare mechanic promoted), number-of-provinces, redundant-connection (new — classic DSU-detects-cycle), accounts-merge (new — DSU on string IDs), kruskal-mst, graph-valid-tree (new), swim-in-rising-water (new — Kruskal-style with sorted edges), smallest-string-with-swaps (new). Each H3 gets a `UnionFindAnim` state at 3-4 steps.

**Advanced:** "Weighted union-find" (store a weight-to-parent for difference queries — Satisfiability of Equality Equations variant). "Union-find with rollback" (used in offline queries — reverse unions in reverse order; small-to-large linking only). "Persistent union-find" (functional; keeps all versions). "Online MST maintenance" (link-cut trees — frontier). Breaking point: when deletions are required — classical DSU can't remove edges; must switch to link-cut trees or offline + rollback. Cross-pattern: MST problems admit BOTH Kruskal (DSU) and Prim (heap) — when to pick which (dense vs sparse graphs).

**Visuals:** 7 × reuse `UnionFindAnim`.

**Promote:** 3 H2s → H3s; add 5 new H3s (basic-dsu, redundant-connection, accounts-merge, graph-valid-tree, swim-in-rising-water).

**Estimated:** 1.5 days.

---

#### `39-trie-pattern.md` (623 LOC, 2 walkthroughs — Word Search II, Max XOR)

**Current:** §Why, §How (binary-trie template), §When, §NOT when, §Templates, §Traps, §History, §Canonical (Word Search II), 2 problem H2s. Missing: bare mechanic, template card (unify two template sections), H3 rename, Advanced, 2-3 sub-variations.

**Basic layer:** §6 "Insert `cat`, `car`, `can` into a trie, then prefix-search `ca`." Show the trie growing node-by-node, then the walk down for `ca` landing on 3 descendants. 20 lines Java, one `TrieWalkAnim` snippet (existing component).

**Intermediate:** §9 `PatternTemplateCard` with 2 tabs: `word-trie` (26-way or hashmap children), `binary-trie` (bit-indexed children for XOR). `InvariantPanel`: "a path from root to a node encodes a prefix." §10 H3s: implement-trie (new — bare-mechanic promoted), word-search-ii (trie + backtracking combo), replace-words (new — shortest-prefix replacement), map-sum-pairs (new — prefix-sum over values), search-suggestions-system (new — autocomplete top-3), word-break-ii (new — trie + DP), maximum-xor-of-two-numbers (binary trie), concatenated-words (new — DFS over trie). Each H3 gets a `TrieWalkAnim` state at 3-4 steps.

**Advanced:** "What if the alphabet is huge (Unicode)?" (hashmap children instead of fixed array; memory tradeoff). "What if the trie must support deletion?" (ref-count + lazy node removal). "What if the queries are approximate (edit distance 1)?" (BK-tree, or trie walk with error budget). "Aho-Corasick" (trie + fail-links for multi-pattern matching — the trie's natural extension to streaming). "Suffix trie / suffix tree / suffix array" (frontier: full-text indexing). Breaking point: when words share no common prefix, trie's size = sum-of-word-lengths with no savings → use hashmap instead. Cross-pattern: Word Search II is backtracking + trie (surface §36 backtracking's grid variant explicitly here).

**Visuals:** 8 × reuse `TrieWalkAnim`.

**Promote:** 2 H2s → H3s; add 6 new H3s (implement-trie, replace-words, map-sum-pairs, search-suggestions, word-break-ii, concatenated-words).

**Estimated:** 2 days (most sub-variations added of any Medium chapter).

### The 8 Dense chapters — shape pass + advanced tier

These have the raw material but not the shape. Each needs the full §6 (bare mechanic), §9 (`PatternTemplateCard`), §10 renaming (H2 problem walkthroughs → H3s under `## Sub-variations of the template`), per-sub-variation visual strips, `InvariantPanel`s, and §14 (Advanced). ~1-1.5 days each. The content stays — this is mostly restructuring + visual overlays + the advanced-tier add.

#### `21-sliding-window.md` — audited; representative of what this band needs

**Current state (1244 LOC, 7 problem walkthroughs as H2s):**
- Has: §Why story, §When to use, §How to use (two templates), §Monotonicity test, §False friends, §Limitations, 7 problem walkthroughs, `<SlidingWindowAnim>`, `<CodeTrace>` on hot paths.
- Missing: `## The bare mechanic` (basic layer), `## THE template` with `PatternTemplateCard`, `## Sub-variations of the template` (the 7 problems are H2s not H3s), `## Traps & gotchas` (traps are scattered as per-problem "Common Mistakes" H3s), `## Advanced`, `WindowTraceStrip` per sub-variation, `InvariantPanel`.

**Basic layer to add:**
- §6 "The bare mechanic — fixed window of 3 on `[2, 1, 5, 1, 3, 2]`" showing the sum-then-slide move: compute `sum = a[0]+a[1]+a[2]`, then for `i = 3..n-1` do `sum += a[i] - a[i-3]`. 10 lines of Java, one tiny SVG with the window moving one step. Explicit "this is the single move that makes sliding window O(n) instead of O(n·k) — everything in §10 is a specialization of this."

**Intermediate layer (shape rename + visuals):**
- §9 "THE template" rewritten as one `PatternTemplateCard` with two tabs: `fixed` and `variable`. Each tab is <40 lines Java. The card's "specializations" chip row links to the 7 §10 H3s.
- §10 "Sub-variations of the template" — demote the 7 problem H2s to H3s. Order: fixed-size warm-up → smallest-subarray-with-sum → longest-substring-no-repeat → min-window-substring → longest-repeating-char-replacement → subarray-product-less-than-k → sliding-window-maximum. Each H3 keeps its existing content, gains an `InvariantPanel` at the top ("the window `[l..r)` always satisfies X") and a `WindowTraceStrip` showing 5-7 window states on a 6-element input.
- Hoist the "Common Mistakes" H3s into a new §11 `## Traps & gotchas` as named `> [trap]` callouts (keep per-problem inline, but also surface them centrally).

**Advanced layer to add:**
- "What if the stream is unbounded?" — reservoir sampling on top of a fixed window; the "constant memory" invariant breaks.
- "What if the window must support max/min in O(1)?" — monotonic deque (already in problem 7, surface explicitly as the cross-pattern).
- "What if the window must support the median?" — two heaps (bridges to §30 k-way-merge).
- "What if the validity predicate is NOT monotone?" — e.g., "longest subarray with sum ≤ K AND no two consecutive negatives" — shrinking can re-break validity; sliding window no longer works, must switch to DP or two-pointer with memoization.
- "What if the input is a stream of events, not an array?" — bucketed count-min sketch; window of time, not of index.
- Breaking point: when the validity test is O(k) per step (hashmap rebuild, not incremental), total is O(n·k) and sliding window has NO advantage over brute force.
- Cross-pattern: Sliding window + hashing (minimum window substring is the canonical example — surface this).

**Visual needs:** `WindowTraceStrip` × 7, one per sub-variation.

**Promote (already present as H2s, convert to H3s):** all 7 problems in-place; no new content needed.

Estimated: 1.5 days (0.5 day shape rename + traps hoist, 0.5 day WindowTraceStrip × 7, 0.5 day Advanced tier).

#### `22-two-pointers.md` (911 LOC, 5 problem walkthroughs as H2s)

**Current:** §Why, §Core idea, §When, §NOT when, §Templates, §Traps, §History, §Canonical walkthrough (Container With Most Water), then 5 problem H2s: 3Sum, Container With Most Water (dup), Squaring, Sort Colors, Trapping Rain Water. Missing: `## The bare mechanic`, `## THE template` (card), §10 sub-variations H3 rename, per-sub-variation visuals, `## Advanced`.

**Basic layer:** §6 "Converge from both ends — pair-sum on `[2, 7, 11, 15]` for target 9." Show `l=0, r=3` → `sum=17>9` → `r--` → `sum=13>9` → `r--` → `sum=9` → return. 10 lines Java, one tiny SVG with the two pointers walking.

**Intermediate (shape rename + visuals):** §9 `PatternTemplateCard` with 3 tabs: `converge` (sorted-array sum family), `partition` (Dutch flag / in-place rewrites), `fast-slow-same-array` (remove-duplicates). §10 H3s demoted from H2s, order: pair-sum (new), container-with-most-water, 3Sum, squaring-a-sorted-array, remove-duplicates (new), sort-colors (Dutch flag), trapping-rain-water. Each H3 gets an `InvariantPanel` and a `WindowTraceStrip`-styled trace (reuse the same component — pointers are just a 2-element window).

**Advanced:** "What if the array isn't sorted?" (sort cost O(n log n) kills the pattern vs hashing's O(n) — when to sort anyway). "What if there are duplicates and you must skip them cleanly?" (the 3Sum skip-while idiom). "What if you need 4Sum, 5Sum, k-Sum?" (recursive 3Sum, when to switch to meet-in-the-middle). Breaking point: when the predicate is NOT monotone-in-pointer-direction (two-pointer no longer eliminates batches). Cross-pattern: Container With Most Water vs Trapping Rain Water — same shape, different invariant (why water-trap also admits the mono-stack solution).

**Visuals:** 7 × `WindowTraceStrip` (reused as pointer-strip).

**Promote (already present H2s → H3s):** all 5 problems in place; add pair-sum + remove-duplicates as new short H3s.

**Estimated:** 1.5 days.

---

#### `25-hashing.md` (832 LOC, 4 walkthroughs)

**Current:** Standard shape (§Why, §Core, §When, §Templates, §Traps, §History, §Canonical, 4 problem H2s: Two Sum, Group Anagrams, Product of Array Except Self, Longest Consecutive Sequence). Missing: bare mechanic, template card, sub-variations H3 rename, Advanced.

**Basic layer:** §6 "One-pass Two Sum on `[2, 7, 11, 15]` for target 9." Walk the loop: see 2, store `2→0`; see 7, 9-7=2 is in map, return `[0,1]`. 8 lines Java, one SVG showing the hashmap growing.

**Intermediate:** §9 `PatternTemplateCard` with 3 tabs: `complement-lookup` (Two Sum family), `canonical-key` (anagram grouping, isomorphic strings), `hashset-of-starts` (longest-consecutive trick). §10 H3s: two-sum-one-pass, two-sum-ii-sorted (bridges to two-pointers), group-anagrams, longest-consecutive-sequence, subarray-sum-equals-k (new — pulled from prefix-sum chapter as the hashing variant), top-k-frequent (bucket-sort hashmap). Each H3 gets a hashmap-state visual snapshot (new mini-component `HashMapStateStrip`, or just inline SVG) showing the map at 3 steps.

**Advanced:** "What if memory is tight?" (counting sort vs hashmap for bounded values; Bloom filter for approximate membership). "What if the hash is adversarial?" (collision attacks; LinkedHashMap vs HashMap; Java 8 tree-ified buckets). "What if ordering matters?" (TreeMap for range queries, LinkedHashMap for insertion order). "What if the key is a complex object?" (equals/hashCode contract — the most common silent bug). Breaking point: when range queries matter → TreeMap; when prefix queries over values matter → Fenwick keyed by hashmap-ids. Cross-pattern: Two Sum II (sorted) is two-pointer, Two Sum I (unsorted) is hashing — recognition drill.

**Visuals:** 6 × hashmap-state SVG inline (no new component needed if simple; promote to component if reused ≥3 times).

**Promote:** 4 current H2s → H3s; add two-sum-ii, subarray-sum-k, top-k-frequent as new H3s.

**Estimated:** 1.5 days.

---

#### `24-prefix-sum.md` (634 LOC, 3 walkthroughs)

**Current:** Standard shape, 3 walkthroughs (Subarray Sum = K, Difference Array, 2D Prefix Sum). Missing: bare mechanic, template card, H3 rename, Advanced.

**Basic layer:** §6 "Cumulative sum of `[2, 1, 3, 4]` → `[0, 2, 3, 6, 10]`" (note the leading 0 for off-by-one safety); then one query `sum(1..3) = prefix[4] - prefix[1] = 10 - 2 = 8`. 8 lines Java, one SVG showing the prefix array growing beneath the input.

**Intermediate:** §9 `PatternTemplateCard` with 4 tabs: `range-sum-1d`, `range-sum-2d`, `diff-array-range-update`, `prefix-hashmap-count`. §10 H3s: range-sum-1d (new — the simplest form), subarray-sum-equals-k (prefix-hashmap), difference-array (range update), 2d-prefix-sum, prefix-xor (new — parity queries), prefix-mod (new — subarrays divisible by K). Each H3 gets a `PrefixSumAnim` cell-fill visual (existing component, reuse).

**Advanced:** "What if updates come at point granularity?" (prefix-sum breaks — switch to Fenwick/BIT). "What if updates are range updates and queries are point queries?" (diff array + prefix; two-level trick). "What if updates AND queries are both range?" (Fenwick-of-Fenwick or segment tree with lazy). "What if the dimension is 3+?" (nD prefix sum with inclusion-exclusion — 2^d terms). Breaking point: streaming data — prefix sum needs the full array. Cross-pattern: subarray-sum-equals-k is prefix-sum + hashing (combo recognition).

**Visuals:** 6 × reuse of existing `PrefixSumAnim`.

**Promote:** 3 current H2s → H3s; add range-sum-1d, prefix-xor, prefix-mod as new H3s.

**Estimated:** 1 day.

---

#### `28-bs-on-answer.md` (598 LOC, 3 walkthroughs)

**Current:** Standard shape, 3 walkthroughs (Koko Eating Bananas, Split Array Largest Sum, Median of Two Sorted Arrays). Missing: bare mechanic, template card, H3 rename, Advanced.

**Basic layer:** §6 "Minimum eating speed to finish `[3, 6, 7, 11]` in 8 hours." Define the feasibility predicate `feasible(k)` = "can finish at speed k in ≤ 8 h", then binary-search `k` over `[1, max]`. Show the first 3 iterations with `lo, mid, hi` and the predicate verdict. 15 lines Java, one `BinarySearchStepStrip`.

**Intermediate:** §9 `PatternTemplateCard` showing the one canonical "lo, hi, while lo<hi, mid, feasible?, shrink" loop with an `InvariantPanel` ("the answer lives in `[lo, hi]` and `feasible` is monotone over k"). §10 H3s: capacity-to-ship-within-D-days (new), koko-eating-bananas, find-the-smallest-divisor (new), split-array-largest-sum, median-of-two-sorted-arrays (partition BS — different because searching an index, not a rate). Each H3 gets a `BinarySearchStepStrip` showing lo/mid/hi over 4-5 iterations.

**Advanced:** "What if the predicate is monotone-but-with-wide-plateaus?" (BS still works; the lower-bound variant isolates the first True). "What if the predicate is NOT monotone?" (parametric search no longer applies — must linear-scan or switch to ternary if unimodal). "What if evaluating the predicate is itself expensive?" (bound total work by log(range) × cost(predicate); when to precompute). "What if the answer is real-valued?" (BS on floats with ε tolerance; floor-count instead of iteration count). Breaking point: discrete answer space with non-monotone feasibility — must use linear scan + feasibility cache. Cross-pattern: Median of Two Sorted Arrays is BS on partition index, not BS on answer — recognition drill.

**Visuals:** 5 × `BinarySearchStepStrip`.

**Promote:** 3 H2s → H3s; add capacity-to-ship + find-the-smallest-divisor as new H3s.

**Estimated:** 1 day.

---

#### `35-greedy.md` (623 LOC, 4 walkthroughs)

**Current:** §Why, §When (local choices with proof), §History, §Canonical walkthrough (Jump Game II), 4 problem H2s (Jump Game II, Gas Station, Task Scheduler, Non-overlapping Intervals), §When greedy fails → DP. Missing: `## The core idea`, `## When NOT to use it`, `## The templates`, `## Traps & gotchas`, bare mechanic, template card, sub-variations H3 rename, Advanced. **Shape-wise the thinnest Dense chapter** — needs the most work.

**Basic layer:** §6 "Pick the fewest coins for amount 7 from `{1, 5}`." Greedy says take 5 then 1,1 → 3 coins. Show it works. Then show the SAME greedy FAILING on amount 7 from `{1, 3, 4}` (greedy says 4+1+1+1 = 4 coins; optimal is 3+4 = 2 coins). Explicit: "greedy only works when the problem has the greedy-choice property — don't guess, prove."

**Intermediate:** §9 `PatternTemplateCard` with 3 tabs: `sort-then-sweep` (activity selection, non-overlapping intervals), `heap-driven` (task scheduler, meeting rooms), `exchange-argument` (jump game, gas station). Each tab's `InvariantPanel` names the greedy choice property being exploited. §10 H3s: activity-selection (new — the canonical "earliest-finish-first"), non-overlapping-intervals, jump-game-ii (farthest-reach), gas-station (prefix-balance), task-scheduler (heap + cooldown), huffman-encoding (new — the archetype of greedy-with-proof). Each H3 gets a greedy-step visual.

**Advanced:** "How do you prove greedy works?" (exchange argument walkthrough on activity selection). "What if the greedy choice is wrong?" (coin change counterexample above — switch to DP). "What if the greedy must look ahead?" (regret-based: scheduling with deadlines). "What are matroids?" (the theoretical frontier of when greedy is correct — Kruskal's as matroid-greedy). Breaking point: coin change with arbitrary denominations — greedy fails, DP wins. Cross-pattern: when greedy and DP both work, greedy is faster — Kruskal (greedy) vs Prim (also greedy) vs Floyd (DP); when to pick which.

**Visuals:** 6 × greedy-step SVG (small, inline).

**Promote:** 4 H2s → H3s; add activity-selection + huffman as new H3s; absorb §"When greedy fails → DP" into §14 Advanced as the counter-example.

**Estimated:** 2 days (needs the most work because current shape is thinnest).

---

#### `36-backtracking.md` (1023 LOC, 5 walkthroughs)

**Current:** Standard shape + canonical N-Queens walkthrough, 5 problem H2s (Subsets, Permutations, Combination Sum, N-Queens, Word Search). Missing: bare mechanic, template card, sub-variations H3 rename, Advanced. **Second-densest content behind DP** — this is mostly a shape pass.

**Basic layer:** §6 "Subsets of `[1, 2]` by pick/skip decision tree." Show the 2^2 = 4 leaves of the recursion tree with explicit `path = []` → branches `[1]`, `[]` → `[1,2]`, `[1]`, `[2]`, `[]`. 15 lines Java, one tiny recursion-tree SVG.

**Intermediate:** §9 `PatternTemplateCard` with 3 tabs: `start-index` (subsets/combinations), `used-set` (permutations), `grid-dfs-with-restore` (word search / N-Queens on an implicit grid). §10 H3s demoted from H2s: subsets, combinations, permutations-swap, permutations-used-array, combination-sum (reuse), n-queens, word-search, letter-combinations-phone (new — a classic). Each H3 keeps its existing content, gains an `InvariantPanel` ("at return, `path` is restored to its state at entry") and a small decision-tree snippet SVG (3-4 levels max).

**Advanced:** "What if the state space is 2^n but most branches dead-end quickly?" (pruning strength matters — order branches by information gain, N-Queens' column-attacked set). "What if the state is encodable in a 64-bit int?" (bitmask backtracking — N-Queens with 3 bitmasks for cols/diag1/diag2 is 10× faster). "When does backtracking turn into DP?" (overlapping subproblems — memoize the decision function on the state). "What is Dancing Links?" (Knuth's exact-cover algorithm; Sudoku's gold-standard solver). "What if the state space is a graph, not a tree?" (switch to BFS with a visited set). Breaking point: when state space exceeds memory + no overlap — only pruning helps; constraint propagation (AC-3) extends backtracking's reach. Cross-pattern: Word Search II is backtracking + trie (surface in §40 trie-pattern).

**Visuals:** 7 × tiny recursion-tree SVG (inline).

**Promote:** 5 H2s → H3s; add letter-combinations-phone + permutations-swap as additional H3s.

**Estimated:** 1.5 days.

---

#### `38-dp.md` (1500 LOC, 9 archetype walkthroughs — densest chapter)

**Current:** §Why, §Core, §When, §NOT when, §Four archetypes (prose), §Traps, §History, §Canonical (Coin Change), then 9 problem H2s covering 1D, Max Subarray, Knapsack, Coin Change (unbounded), Grid DP, Subsequence DP, Interval DP, State-Machine DP, Bitmask DP, plus Tree DP + Digit DP pointers. Missing: bare mechanic, template card, sub-variations H3 rename, Advanced. **Richest chapter — the shape pass alone is substantial.**

**Basic layer:** §6 "Fibonacci bottom-up on 5 cells." Table `dp[0..4]`; `dp[0]=0, dp[1]=1`, loop fills the rest. 10 lines Java, one `DpFillAnim` 1-D filling left-to-right. Explicit: "every DP in this chapter follows the same 3-step shape — define the state, write the transition, choose the fill order."

**Intermediate:** §9 `PatternTemplateCard` with 4 tabs: `top-down-memo` (recursion + cache), `bottom-up-table`, `space-optimized-rolling`, `bitmask-state`. §10 H3s demoted from the current 9 H2s: 1D-linear (climbing-stairs, house-robber), max-subarray (Kadane), 0/1-knapsack, coin-change-unbounded, grid-dp (unique-paths, min-path-sum), subsequence-dp (LIS, LCS, edit-distance), interval-dp (matrix-chain, burst-balloons), state-machine-dp (stock trading), bitmask-dp (TSP), tree-dp (new section — currently a pointer only). Each H3 gets a `DpFillAnim` or inline SVG table showing 3-4 cells filling.

**Advanced:** "Convex hull trick" (O(n²) DP where transition is `dp[i] = min_{j<i} (dp[j] + f(i,j))` with specific structure → O(n log n) via CHT). "Divide-and-conquer DP optimization" (when `opt[i]` is monotone in `i`). "SOS DP" (sum-over-subsets — bitmask DP over 2^n). "Digit DP" (count numbers with property). "Knuth's optimization" (when the DP matrix is monotone quadrangle-inequality-satisfying). "Bitmask DP + meet-in-the-middle." Breaking points: DP with state size exceeding memory → sqrt decomposition on time axis; DP with infinite state space → BFS over state graph. Cross-pattern: when BFS = DP (both compute shortest path on a DAG); when DP = memoized backtracking (overlapping subproblems recognition).

**Visuals:** 10 × `DpFillAnim` or inline table (Phase 6 generalizes `DpFillAnim` into `DpTableAnim` which this chapter leverages).

**Promote:** 9 current H2s → H3s; add tree-dp as a new H3 (not a pointer).

**Estimated:** **2 days** — richest Advanced surface of all 21.

---

#### `40-bit-manip.md` (601 LOC, 3 walkthroughs + §Core identities)

**Current:** Standard shape + §Core identities, 3 walkthroughs (Single Number I/II/III, Counting Bits, Subset generation). Missing: bare mechanic, template card, sub-variations H3 rename, Advanced.

**Basic layer:** §6 "Isolate the low bit with `x & -x` on `x = 12 (1100)` → `4 (0100)`." Then "count set bits by `while (x) { count++; x &= x-1; }`" (Brian Kernighan). 10 lines Java, one SVG showing the binary representation with the low bit highlighted.

**Intermediate:** §9 `PatternTemplateCard` with 4 tabs: `xor-cancellation` (Single Number), `low-bit-isolate` (counting bits, Fenwick-style), `bitmask-as-set` (subset enumeration), `bit-dp` (counting-bits-via-dp). §10 H3s: single-number-xor, single-number-ii-mod3, single-number-iii-two-missing (new — explicit treatment), counting-bits-dp, reverse-bits (new), power-of-two-check (new — `x & (x-1) == 0`), subset-generation-via-masks, swap-without-temp (new — classic). Each H3 gets an inline SVG of the binary bits highlighting the operation.

**Advanced:** "SIMD-era tricks" (hardware popcnt via `Integer.bitCount`, lzcnt, bzhi/pdep/pext — mention JDK 20+ `Integer.compress`/`expand`). "Bit-plane DP" (DP where the state is a column of a bitmask). "Gray code" (adjacent codes differ by 1 bit — used in combinatorial generation and error-correction). "Hamming weight for compressed graph representation" (sparse-table queries). Breaking point: when values exceed 64 bits — BigInteger kills the pattern; must switch to custom bitset arrays. Cross-pattern: bitmask DP (§38 DP) uses bit-manip as the state representation — explicit cross-link.

**Visuals:** 8 × inline binary-bits SVG.

**Promote:** 3 H2s → H3s; add 5 new H3s (single-number-iii, reverse-bits, power-of-two, swap-without-temp, bit-subsets).

**Estimated:** 1.5 days.

---

## Part 4 — Execution sequencing

Two exemplars first — one for the Light band (binary-search), one for the Dense band (sliding-window). The Dense exemplar is critical because 8 of 21 chapters are in that band and the work is different from Light-band work: it's a shape pass over existing dense content, not a from-scratch build.

### Phase 1 — Shared infra (~7 days)

Two tracks that can run in parallel:

**Track A — Visual + shape infra (~2 days):** `PatternTemplateCard`, `StepStrip` generalization + 3 specializations (`WindowTraceStrip`, `BinarySearchStepStrip`, `PartitionStepStrip`), `PatternSubVariationNav`, `patterns.subvariations.json`. The other `StepStrip` specializations get added as their consumer chapters are picked up.

**Track B — Mastery drill infra (~5 days):** `InvariantProof` (replaces `InvariantPanel`), `TemplateReveal` with blind-solve textarea + diff, `RecognitionDrill` + `recognition.problems.json` scaffolding (empty entries per pattern — populated per-chapter during that chapter's upgrade), `AmortizedPanel`, mandatory wiring of existing `TrapTrace` + `DueForReview` + `MarkSolved` into the chapter template. Also ship `/recognize` and `/mixed-drill` site-level pages.

Phase 1 lands as a single PR covering both tracks before Phase 2 begins.

**Per-chapter effort now includes ~0.5 day of mastery work on top of the band-specific work:**
- Author 10 `recognition.problems.json` entries for the pattern (with distractors).
- Pick + transcribe 1 OSS snippet for §13.5 "In the wild".
- Convert any surviving one-line invariants to `<InvariantProof>` tripartite.
- Pick ≥3 traps and author them as `<TrapTrace>` embeds (not just callouts).
- Write the amortized derivation for the 6 patterns that need it.
These are baked into the per-chapter day counts below.

### Phase 2a — Light-band exemplar: `27-binary-search.md` (~2.5 days)

Rebuild the flagship Light-band chapter end-to-end + all mastery additions. Establishes the shape for a from-scratch build AND the mastery-tier bar. By end of Phase 2a: reading this one chapter tells you the full standard.

### Phase 2b — Dense-band exemplar: `21-sliding-window.md` (~2 days)

Shape pass + advanced tier + mastery additions on the Dense-band chapter you asked about. Establishes the shape for a content-rich chapter where almost nothing is written from scratch — just restructured, overlaid with visuals, and drilled. By end of Phase 2b: both exemplars exist, both bands' templates proven at mastery tier.

**Checkpoint with the user at end of Phase 2b.** If either exemplar's shape or mastery additions need tuning, that happens before Phase 3 scales to the other 19 chapters.

### Phase 3 — Apply the Light-band shape + mastery to the 6 remaining Light chapters (~15 days)

Order: `23-fast-slow`, `41-quickselect` (gets amortized derivation), `31-merge-intervals`, `32-sweep-line`, `30-k-way-merge`, `37-divide-conquer`.

~2.5 days per chapter. Rolling commits — one chapter per PR.

### Phase 4 — Apply the Dense-band shape + mastery to the 8 remaining Dense chapters (~16 days)

Order: `22-two-pointers` **(2d — gets amortized)**, `25-hashing` (2d), `24-prefix-sum` (1.5d), `28-bs-on-answer` (1.5d), `35-greedy` **(2.5d — thinnest shape)**, `36-backtracking` (2d), `40-bit-manip` (2d), `38-dp` **(2.5d — richest Advanced + gets amortized on space-optimization)**.

Rolling commits — one chapter per PR.

### Phase 5 — Shape-normalize + mastery for the 5 Medium chapters (~10 days)

Each gets the Dense-band shape pass + mastery additions + 2-5 new sub-variations.

Order: `26-monotonic-stack` **(2d — gets amortized, the exemplar for the aggregate method)**, `34-union-find` **(2d — gets amortized, the exemplar for the potential method)**, `33-topological-sort` (2d), `29-top-k-heap` (2d), `39-trie-pattern` (2d).

### Phase 6 — Infra for DP + grid patterns (~3 days)

Generalize `DpFillAnim` into `DpTableAnim` and backfill the 10 DP archetypes with table animations. Build `GridPathAnim` and use it in the grid-DP, grid-backtracking, and Word Search II walkthroughs. Can run in parallel with Phase 4 (DP sub-phase) if desired.

### Total

~7-8 weeks of focused work. Phase 1 ~7d + Phase 2a 2.5d + Phase 2b 2d + Phase 3 ~15d + Phase 4 ~16d + Phase 5 ~10d + Phase 6 ~3d = ~55 working days, call it 7-8 weeks with slack. The repo stays shippable at every checkpoint — each chapter upgrade is a self-contained PR that passes CI independently. The mastery infra lands in Phase 1 so every chapter from Phase 2 onward is mastery-tier from first commit.

---

## Part 5 — Success criteria (definition of done)

A chapter is "done" against this plan when all of the following hold:

**Structural (shape):**
1. All 17 sections from Part 1 are present, in order.
2. The basic layer (§7) shows the pattern working on a trivial input WITHOUT any optimization.
3. The intermediate layer (§11) has ≥3 H3 sub-variations, each with its own template-diff, worked example, and `StepStrip` visual.
4. The advanced layer (§16) has ≥3 "what if…" follow-ups + ≥1 breaking point + **≥3 cross-pattern problems**.
5. `patterns.subvariations.json` lists every sub-variation present in §11, and nothing listed is missing.
6. `PatternTemplateCard` is in §10 with: code (wrapped in `<TemplateReveal>`), invariant proof, complexity, specializations list.

**Mastery:**
7. **Every** code block in §10 and §11 is wrapped in `<TemplateReveal>` (blind-solve + diff).
8. **Every** invariant is rendered as `<InvariantProof>` with non-empty init / maintenance / termination — one-line statements alone are rejected.
9. §12 "Traps & gotchas" has **≥3 `<TrapTrace>` embeds** (buggy code → trip input → wrong output → diagnosis → fix).
10. §13 "History" has an `## In the wild` H3 with a ~10-line real OSS snippet and source link.
11. §15 "Recognition drill" renders `<RecognitionDrill>` with `count ≥ 10`, backed by `recognition.problems.json`.
12. **Every** §11 sub-variation has a `<MarkSolved>` button that registers it in the spaced-review schedule.
13. For patterns marked `requiresAmortized: true` in `patterns.subvariations.json`, §16 Advanced has a `### Why the amortized bound` H3 with `<AmortizedPanel>` + a worked numeric example.

**Quality:**
14. `<Quiz>` has ≥5 questions covering: the invariant, one sub-variation specialization, one trap, one advanced follow-up, one cross-pattern recognition.
15. Chapter builds green under both `CF_PAGES=1` and the GitHub Pages build.
16. Playwright smoke test asserts: (a) `## The bare mechanic` H2 renders, (b) `PatternTemplateCard` mounts, (c) `## Advanced` H2 renders, (d) `<RecognitionDrill>` mounts, (e) `<InvariantProof>` has non-empty tripartite content.

---

## Part 6 — Non-goals (explicit scope exclusions)

- ❌ Expanding to new patterns (24+). The 21 cover the interview surface; adding more dilutes focus. Advanced topics (KMP/Z/suffix array, max-flow, HLD, FFT, game theory) belong in a separate "Part V — Advanced Algorithms" section covered under a different plan.
- ❌ Rewriting the 206 problem pages. Those are already at 10/10 against the interview rubric; this plan pulls them INTO the pattern chapters as walked examples, not rewrites them.
- ❌ Recording videos. Deferred until content stabilizes.
- ❌ i18n of chapter content. Not in scope.
- ❌ Changing the deploy pipeline. Current `gen/src/ → migrate.py → VitePress → GH Pages + Cloudflare Pages` is working; the plan ships inside this pipeline.

---

## Part 7 — Immediate next step

**Phase 1 — build the shared infra (now ~7 days, two parallel tracks).**

- **Track A (visual + shape, ~2 days):** `PatternTemplateCard`, `StepStrip` generalization + 3 specializations (`WindowTraceStrip`, `BinarySearchStepStrip`, `PartitionStepStrip`), `PatternSubVariationNav`, `patterns.subvariations.json`.
- **Track B (mastery drill infra, ~5 days):** `InvariantProof`, `TemplateReveal` with blind-solve + diff, `RecognitionDrill` + `recognition.problems.json` scaffolding, `AmortizedPanel`, chapter-template integration of existing `TrapTrace` + `DueForReview` + `MarkSolved`, `/recognize` + `/mixed-drill` site-level pages.

After Phase 1 lands, both exemplars begin: Phase 2a (binary-search, Light-band build at mastery tier) and Phase 2b (sliding-window, Dense-band shape pass at mastery tier). I'd suggest 2a then 2b sequentially — the shape of 2a informs 2b — but either order works.

Signal to begin: **"Ship Phase 1."** Alternative signals:
- **"Change <X> in the plan first"** — tune the shape before implementation.
- **"Drop mastery addition <N>"** — if you want a specific mastery item (recognition drill / blind-solve / amortized panel / in-the-wild / tripartite proofs / mandatory TrapTrace / cross-pattern expansion / spaced-review wiring) dropped from scope. Each item has an independent cost in Phase 1 time.
- **"Start with sliding-window first"** — swap 2a and 2b (Dense exemplar before Light).
- **"Compress to one chapter end-to-end first, then plan expansion"** — if you'd rather see one chapter fully upgraded (infra + one chapter's content in one go) before committing to the full plan. Say which chapter (binary-search or sliding-window).
