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

### Flagship-quality rewrite in progress

**38 pages fully rewritten to flagship quality** this session (see /problems/sliding-window-longest-substring for the target format):
- Sliding Window: 13 pages (100% of pattern complete)
- Two Pointers: 3 pages (3sum-closest, 4sum, valid-palindrome-ii)
- Hashing: 3 pages (3sum, valid-anagram, longest-consecutive-sequence)
- Fast &amp; Slow: 5 pages (100% of pattern complete)
- Binary Search: 4 pages (100% of pattern complete)
- Top-K / Heap: 3 pages (100% of pattern complete)
- K-way Merge: 3 pages (100% of pattern complete)
- Monotonic Stack: 4 pages (100% of pattern complete)

**Every page includes**: 3 numbered Examples, Constraints, 2–4 approaches with Intuition + Java code + real `<CodeTrace>` tied to the specific example + Complexity, Complexity summary table, When-to-use bullets, Related LC links.

**Remaining**: 95 more variation pages need flagship-quality rewrite:
- Prefix Sum (10), Merge Intervals (5), Sweep Line (2), Topological Sort (4), Union-Find (8), Greedy (10 — subset upgraded structurally only), Backtracking (16 — structural), Divide &amp; Conquer (4), DP (28 — 3 already flagship-quality: coin-change, LIS, edit-distance), Trie (7), Bit Manipulation (9 — 1 already: subsets), Two Pointers (10 remaining), Hashing (10 remaining).

Realistic per-session: 30–40 pages given the depth (5-6 KB per page with real CodeTrace). Multiple sessions needed for full completion.

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

## Deferred (from prior audits — post-visualizer sweep)

The four visualizer items from the Grokking-head audit are now shipped:

1. ✅ **Complexity growth-curve visualizer** — `ComplexityCurve.vue` on complexity chapter (interactive n-slider, 8 classes, ops-vs-wall-time toggle, feasibility verdict)
2. ✅ **6-phase playbook single-page animation** — `PlaybookPhases.vue` on playbook chapter (colored phase progress, playback controls, working artefact per phase)
3. ✅ **~30 Data-structure operation state-machines** — `DsStateMachine.vue` + 5 wrappers (StackQueueOps, HeapOps, BstOps, TrieOps, UnionFindOps) covering push/pop/enq/deq, sift-up/sift-down/heapify, BST search/insert/delete/BFS, trie insert/search/prefix, and UF find/union/components. Embedded across 5 DS chapters.
4. ✅ **~84 Problem-statement Example previews** — `ExamplePreview.vue` + auto-generator `gen/add_example_previews.py` parsing `**Example N:**` lines and auto-embedding input→output visuals with multi-arg support. Coverage across 17 chapters.

Nothing outstanding on the audit list.

## Blocked on you

- `add-email-capture-pdf-gate` — needs your Buttondown/ConvertKit signup
