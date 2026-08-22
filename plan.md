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

### All variation pages fully authored

**184 variation pages** — every LC problem across all "Same pattern, new tweaks" tables is now a **full multi-approach page**: LC link + difficulty badge + 1–3 approaches with Java code + complexity summary + related-problems cross-links. Zero scaffolds remain.

Delivered across 7 batches: Prefix Sum + Trie + Bit Manip (25), Two Pointers + Hashing (26), Greedy (10), Backtracking (15), Sliding Window (25), DP (28), and prior Merge Intervals / BS on Answer / Union-Find / Monotonic Stack / Binary Search / Topo Sort / Divide &amp; Conquer / Sweep Line / Top-K / K-way Merge / Fast-Slow (55).

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

## Deferred (visual/interactive work — from the Grokking-head audit)

Four items outstanding, ranked by ROI:

1. **227 Problem-statement Example previews** — small "Example →" trace strip beside every problem's example (input/output → 1–2 frame walkthrough of what the transformation does). Reuses existing CodeTrace component; big surface-area win. Est. ~40 hours (batchable).
2. **30 Data-structure operation state-machines** — CodeTrace-style animations for stack push/pop, queue enq/deq, heap sift-up/down, BST rotate, UF union/find, Trie insert/search, deque ops, etc. Each ~1 hour. Est. ~30 hours.
3. **Complexity growth-curve visualizer** — one interactive Vue component: `n` slider (1..10 000) with bar chart comparing O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ) runtimes. Est. ~4 hours.
4. **6-phase playbook single-page animation** — animated walkthrough of Recognize → Model → Verify → Code → Test → Optimize on one example. Est. ~6 hours.

**Note on the audit's "90 mini-traces for new tweaks":** superseded — the 184 fully-authored variation pages each already contain the full solution with Java code and cross-linking, which is a strictly stronger deliverable than a mini-trace.

## Blocked on you

- `add-email-capture-pdf-gate` — needs your Buttondown/ConvertKit signup
