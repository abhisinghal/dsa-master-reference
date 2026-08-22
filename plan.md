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

### Scaffold pages (auto-generated)

**176 additional problem pages** — one per LC problem across all "Same pattern, new tweaks" variation tables. Each shows: LC link + difficulty badge + the one-line "thing that changes vs the flagship" + links back to the pattern chapter and to the flagship problem page.

Rationale: full 3-approach authoring for 200+ problems would be 50+ hours. Scaffolds give readers immediate navigable coverage with clear "detailed page in progress" signal and direct paths to the existing full write-ups in the pattern chapters.

### Infrastructure

- New `gen/src/problems/` directory (49 old chapters unchanged; 205 new problem files)
- `migrate.py` auto-migrates every `problems/*.md` to `web/docs/problems/*.md` (strips numeric prefixes)
- Top nav: new "Practice" link between Data Structures and System Design
- Sidebar: 21 collapsible pattern groups, 205 clickable problem entries
- Scaffold generator parses "Same pattern, new tweaks" tables for LC link + one-line differentiator

## Cumulative session output

- **177 interactive Execution Traces** across chapters (100% Trace-it coverage + 98% Trap coverage)
- **205 problem pages** in the new /problems/ section
- **~29 fully-authored** multi-approach pages
- **CI-green** on every push; site live at abhisinghal.github.io/dsa-master-reference/

## Recent commits (all live)

- `4576b6e` +8 more full multi-approach pages (upgrade high-value scaffolds)
- `0d69872` +184 variation scaffold pages (205 total)
- `30e4ba8` 21 flagship practice pages
- `3a50063` docs: plan.md — 177 Execution Traces
- `3de6824` Execution Traces in cheatsheets, transcripts, SD
- `4ab7ae3` P0 Trap Traces batch 2 (61 auto)
- `019530f` P0 Trap Traces batch 1 (20 hand)
- `a94d862` Naming: "Execution Trace" badge
- `d1a7683` System Design chapter
- `cdc2ff2` 100% CodeTrace coverage

## Deferred (kept in plan so we don't lose them)

- **Full multi-approach authoring for the remaining ~176 scaffold pages** — each is a ~30-min task. Priority order per pattern is roughly the order in the "Same pattern, new tweaks" tables. Estimated ~90 hours to fully upgrade all scaffolds.
- 227 Problem-statement Example previews across chapters
- 30 Data-structure operation state-machine animations
- Complexity growth-curve visualizer
- 6-phase playbook single-page animation

## Blocked on you

- `add-email-capture-pdf-gate` — needs your Buttondown/ConvertKit signup
