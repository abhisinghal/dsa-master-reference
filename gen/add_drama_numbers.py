"""One-shot: add hand-crafted drama-number sentences to problem pages missing D.

Each entry is per-problem hand-authored, tied to that problem's specific brute vs canonical
story. Runs from repo root: `python gen/add_drama_numbers.py`.
"""
from __future__ import annotations
import re
from pathlib import Path

# Per-file drama sentence appended to the **Constraints** — line.
# Keep each sentence compact (one line) and tied to the actual problem's numbers.
DRAMA = {
    '01v-fruit-into-baskets.md':
        'Brute enumerates every window in O(n²) = 10¹⁰ ops at n=10⁵ (TLE past ~30 s). Sliding window is O(n) = 10⁵ ops = <10 ms.',
    '01v-max-consecutive-ones-iii.md':
        'Brute expands every window in O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Sliding window with k-tolerance stays O(n) = 10⁵ ops.',
    '01v-minimum-size-subarray-sum.md':
        'Brute enumerates all subarrays in O(n²) = 10¹⁰ ops (TLE past n=10⁴). Sliding window is O(n) = 10⁵ ops = <5 ms.',
    '01v-permutation-in-string.md':
        'Brute compares every window against sorted target — O(n·k·log k) = 10⁴·10⁴·13 ≈ 1.3·10⁹ ops (TLE). Sliding-window frequency compare is O(n·26) = ~2·10⁵ ops.',
    '01v-find-all-anagrams-in-a-string.md':
        'Brute sorts every window in O(n·k·log k) = 3·10⁴·10⁴·13 ≈ 4·10⁹ ops (TLE). Sliding-window freq compare is O(n·26) ≈ 8·10⁵ ops.',
    '01v-longest-substring-with-at-most-k-distinct-characters.md':
        'Brute expands every window in O(n²·k) = 10¹⁰·k ops at n=10⁵ (TLE). Sliding window with a freq map is O(n) = 10⁵ ops.',
    '01v-longest-repeating-character-replacement.md':
        'Brute is O(n²·26) ≈ 2.6·10¹¹ ops at n=10⁵ (TLE). Sliding window (max-freq + k) is O(n·26) ≈ 2.6·10⁶ ops.',
    '01v-subarrays-with-k-different-integers.md':
        'Brute enumerates every subarray in O(n²) = 4·10⁸ ops at n=2·10⁴ (borderline TLE). Two sliding windows (`≤k` − `≤k−1`) run in O(n) = 2·10⁴ ops.',
    '01v-number-of-substrings-containing-all-three-characters.md':
        'Brute is O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Sliding window with the "shrink while valid" trick is O(n) = 10⁵ ops.',
    '01v-count-number-of-nice-subarrays.md':
        'Brute checks every subarray in O(n²) = 2.5·10⁹ ops at n=5·10⁴ (TLE). Sliding-window `atMost(k) − atMost(k−1)` is O(n) = 5·10⁴ ops.',
    '01v-binary-subarrays-with-sum.md':
        'Brute is O(n²) = 9·10⁸ ops at n=3·10⁴ (TLE past 5 s). Sliding-window `atMost(goal) − atMost(goal−1)` runs in O(n) = 3·10⁴ ops.',
    '02v-3sum-closest.md':
        'Brute enumerates every triple in O(n³) = 1.25·10⁸ ops at n=500 (borderline). Sort + two-pointer is O(n²) = 2.5·10⁵ ops.',
    '02v-3sum-smaller.md':
        'Brute is O(n³) ≈ 4·10¹⁰ ops at n=3500 (TLE). Sort + two-pointer with count is O(n²) ≈ 1.2·10⁷ ops.',
    '02v-largest-rectangle-in-histogram.md':
        'Brute enumerates every (l, r) window in O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Monotonic stack runs each index in amortised O(1) → O(n) = 10⁵ ops = <10 ms.',
    '02v-move-zeroes.md':
        'Brute (build a fresh array and copy back) is O(n) time + O(n) space. Two-pointer in-place stays O(n) = 10⁴ ops with O(1) extra space.',
    # --- Batch 2: 20 canonical flagships + high-signal variants ---
    '02-two-pointers-container-with-most-water.md':
        'Brute enumerates every pair in O(n²) = 10¹⁰ ops at n=10⁵ (TLE past ~10 s). Two-pointer inward sweep — provably safe by monotonicity — is O(n) = 10⁵ ops = <5 ms.',
    '03-fast-slow-linked-list-cycle-ii.md':
        'Brute stores every visited node in a HashSet — O(n) time but O(n) memory + hashing overhead (heap allocations dominate cache misses). Floyd\'s tortoise & hare is O(n) time with O(1) extra memory — the canonical answer since 1967.',
    '03v-linked-list-cycle.md':
        'Brute is O(n) time + O(n) memory with a visited HashSet. Floyd\'s tortoise & hare is O(n) time + O(1) space — half a dozen pointer chases per node.',
    '04-prefix-sum-subarray-sum-equals-k.md':
        'Brute enumerates every subarray in O(n²) = 4·10⁸ ops at n=2·10⁴ (borderline TLE). Prefix-sum + hashmap of complements is O(n) = 2·10⁴ ops = <2 ms.',
    '04v-contiguous-array.md':
        'Brute is O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Rewrite as prefix-sum with 0/1→−1/+1, hashmap of first-seen index → O(n) = 10⁵ ops.',
    '06-monotonic-stack-daily-temperatures.md':
        'Brute searches forward for the next warmer day per element — O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Monotonic decreasing stack visits each index once → O(n) = 10⁵ ops with amortised O(1) per push/pop.',
    '07-binary-search-rotated-sorted.md':
        'Brute linear scan is O(n) = 10⁵ ops per query (fine one-off, dies with 10⁴ queries → 10⁹). Modified binary search on the "one half is sorted" invariant is O(log n) = 17 comparisons.',
    '07v-binary-search.md':
        'Brute linear scan is O(n) — 10⁴ ops per query, dies with 10⁵ queries. Binary search is O(log n) = 14 comparisons even at n=10⁴; 30 comparisons at n=10⁹.',
    '07v-find-peak-element.md':
        'Brute linear scan is O(n) = 10³ ops. Binary search on the "climb toward the higher neighbour" invariant is O(log n) ≈ 10 comparisons.',
    '07v-find-minimum-in-rotated-sorted-array.md':
        'Brute linear scan is O(n) = 5·10³ ops. Binary search comparing mid vs right pivot is O(log n) ≈ 13 comparisons.',
    '08v-median-of-two-sorted-arrays.md':
        'Merging both then indexing is O(m+n) = 2·10³ ops. The interviewer wants the O(log min(m,n)) partition-based binary search — ~11 comparisons even at m,n = 10³.',
    '09-top-k-frequent-elements.md':
        'Brute sorts all n values by frequency in O(n log n) = 10⁵·17 ≈ 2·10⁶ ops. Heap of size k is O(n log k) — at k=10 that\'s 10⁵·4 = 4·10⁵ ops. Quickselect on frequency buckets is expected O(n) = 10⁵ ops.',
    '11-merge-intervals-classic.md':
        'Brute checks every pair for overlap in O(n²) = 10⁸ ops at n=10⁴. Sort by start (O(n log n)) then linear sweep with a single "current" interval is O(n log n) = ~10⁵ ops = <10 ms.',
    '13-topological-sort-course-schedule.md':
        'Brute repeatedly scans for zero-indegree nodes: O(V·(V+E)) = 2000·(2000+5000) = 1.4·10⁷ ops. Kahn\'s queue-based BFS is O(V+E) = 7·10³ ops with built-in cycle detection.',
    '14-union-find-number-of-provinces.md':
        'Brute DFS/BFS from every city is O(n²) = 4·10⁴ ops at n=200. Union-Find with path compression + union by rank is O(n²·α(n)) ≈ 4·10⁴ ops — same asymptote, but the DSU wins the moment edges start arriving dynamically.',
    '15-greedy-jump-game-ii.md':
        'Brute DP with min-jumps[i] is O(n²) = 10⁸ ops at n=10⁴ (borderline). Greedy expanding-frontier ("BFS levels on an implicit graph") is O(n) = 10⁴ ops.',
    '15v-best-time-to-buy-and-sell-stock.md':
        'Brute compares every buy/sell pair in O(n²) = 10¹⁰ ops at n=10⁵ (TLE). One-pass tracking min-so-far and max profit is O(n) = 10⁵ ops = <5 ms.',
    '15v-gas-station.md':
        'Brute tries every starting station in O(n²) = 10¹⁰ ops at n=10⁵ (TLE). One-pass greedy using "total tank ≥ 0 → answer exists; skip to i+1 whenever running tank goes negative" is O(n) = 10⁵ ops.',
    '18-dp-house-robber.md':
        'Brute recursion tries include-or-skip at each house — O(2ⁿ) = 10³⁰ ops at n=100 (universe-age). DP with 2-variable rolling state is O(n) = 100 ops = trivial.',
    '20-bit-manip-single-number.md':
        'Brute HashMap of counts is O(n) time + O(n) space. XOR-fold is O(n) time + O(1) space — 3·10⁴ XOR operations for the full input.',
    '21-quickselect-kth-largest.md':
        'Brute sort is O(n log n) = 10⁵·17 ≈ 2·10⁶ ops. Heap of size k is O(n log k). Quickselect with random pivot is expected O(n) = 10⁵ ops, worst-case O(n²) (mitigated by median-of-medians for provable linear).',
    # --- Batch 3: DP + backtracking + trie + bit-manip family (20 pages) ---
    '18v-climbing-stairs.md':
        'Brute recursion is O(2ⁿ) — at n=45 that\'s ~3.5·10¹³ ops (dies past a full year at 10⁶ ops/sec). Rolling 2-variable DP is O(n) = 45 additions.',
    '18v-coin-change.md':
        'Brute recursion tries every coin at every amount — O(coins^amount) ≈ 12^10000 for max input (dies before universe end). Bottom-up DP is O(amount·|coins|) = 10⁴·12 ≈ 10⁶ ops = <10 ms.',
    '18v-edit-distance.md':
        'Brute recursion is O(3^max(m,n)) — at m=n=500 that\'s ~7·10²³⁸ (dead universes). 2D DP is O(m·n) = 2.5·10⁶ ops = <30 ms; compressed to O(min(m,n)) space.',
    '18v-longest-increasing-subsequence.md':
        'Brute enumerates all 2ⁿ subsequences — 2·10³ length = 10⁶⁰²⁰ ops (dead). DP is O(n²) = 4·10⁶ ops = ~20 ms; binary-search patience sort is O(n log n) = 2·10⁴ ops.',
    '18v-longest-palindromic-subsequence.md':
        'Brute enumerates 2ⁿ subsequences — at n=10³ that\'s 10³⁰¹ ops (universe-age × 10²⁸⁰). 2D interval DP is O(n²) = 10⁶ ops = ~5 ms.',
    '18v-perfect-squares.md':
        'Brute BFS over all decompositions is O(n^(√n)) — dies past n=200. DP is O(n·√n) = 10⁴·100 = 10⁶ ops = <10 ms.',
    '18v-target-sum.md':
        'Brute enumerates ±assignments — O(2ⁿ) = 10⁶ ops at n=20 (fine), but 10³⁰ ops at n=100. Knapsack DP is O(n·sum) ≤ 20·10⁴ = 2·10⁵ ops.',
    '18v-partition-to-k-equal-sum-subsets.md':
        'Brute enumerates k^n partitions — at n=16, k=4 that\'s 4·10⁹ ops (borderline TLE). Bitmask DP + prune is O(k·2ⁿ) = 4·65536 ≈ 2·10⁶ ops.',
    '18v-delete-and-earn.md':
        'Brute enumerates 2ⁿ subsets — at n=2·10⁴ = 10⁶⁰⁰⁰ (dead). Reduce to house-robber on bucketed sums → DP O(n + max) = 2·10⁴ + 10⁴ = 3·10⁴ ops = <2 ms.',
    '18v-dungeon-game.md':
        'Brute forward DP fails (need to know future minimum HP). Reverse DP from goal to start is O(m·n) = 200·200 = 4·10⁴ ops = ~1 ms; forward-DP attempt burns hours before you realize it can\'t work.',
    '18v-min-cost-climbing-stairs.md':
        'Brute recursion tries +1 or +2 at each step — O(2ⁿ) = 10³⁰⁰ ops at n=10³. Rolling DP is O(n) = 10³ ops = <1 ms.',
    '18v-house-robber-ii.md':
        'Brute enumerates 2ⁿ include/skip masks — at n=100 that\'s 10³⁰ ops (universe-age). Two-pass linear DP (skip first or last) is O(n) = 200 ops = trivial.',
    '18v-best-time-to-buy-and-sell-stock-with-cooldown.md':
        'Brute enumerates buy/sell/rest states — O(3ⁿ) = ~10⁴⁷ ops at n=100. State-machine DP with 3 rolling variables is O(n) = 5·10³ ops = <1 ms.',
    '18v-best-time-to-buy-and-sell-stock-with-transaction-fee.md':
        'Brute enumerates 2ⁿ buy/sell subsets — at n=5·10⁴ that\'s 10¹⁵⁰⁰⁰ ops. State-machine DP is O(n) = 5·10⁴ ops = <5 ms.',
    '18v-best-time-to-buy-and-sell-stock-iv.md':
        'Brute picks C(n, 2k) buy-sell pairs — at n=1000, k=100 that\'s ~10²³⁰ combinations. 2k-state DP is O(n·k) = 10⁵ ops with the k≥n/2 shortcut collapsing to greedy O(n) = 10³ ops.',
    '16v-permutations.md':
        'Brute checks all n^n placements: at n=8 that\'s ~10⁷ ops. Backtracking with used-mask visits exactly n! = 40320 at n=8; grows to 3·10⁶ at n=10.',
    '16v-permutations-ii.md':
        'Brute enumerates n! permutations then dedups a set — at n=8 with heavy duplicates, dedup HashMap costs 10⁷ hashes. Sort + skip-duplicates in backtrack cuts to true-distinct permutations directly.',
    '16v-subsets-ii.md':
        'Brute enumerates 2ⁿ subsets and dedups — at n=10 with duplicates that\'s 10³ subsets each hashed. Sort + skip-duplicates in backtrack yields exactly distinct subsets in one pass — 10⁶ ops even for max input.',
    '16v-combination-sum-iv.md':
        'Brute recursion tries every ordered combination — at target=1000 with 4 nums that\'s 4^1000 = 10⁶⁰² ops. Bottom-up DP counting orderings is O(target·n) = 10³·200 = 2·10⁵ ops.',
    '19v-replace-words.md':
        'Brute checks every root against every word in O(n·L·m) — 10⁶·L (grows fast). Trie compresses shared prefixes: O(sum-of-lengths) build + O(L) per lookup = 10⁶ ops total.',
    # --- Batch 4 (final push): remaining 85 pages, D 59% -> 100% ---
    # Sliding window tail
    '01v-longest-palindromic-substring.md':
        'Brute checks every substring — O(n³) = 10⁹ ops at n=10³ (~20 min). Expand-around-center is O(n²) = 10⁶ ops; Manacher is O(n) = 10³ ops.',
    '01v-minimum-window-subsequence.md':
        'Brute enumerates windows and matches subseq — O(n²·m) = 10¹⁰ ops at n=2·10⁴ (TLE). Two-pointer scan with backwards refine is O(n·m) = ~4·10⁶ ops.',
    '01v-shortest-subarray-with-sum-at-least-k.md':
        'Brute enumerates all subarrays — O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Prefix sum + monotonic deque is O(n) = 10⁵ ops = <10 ms.',
    '01v-substring-with-concatenation-of-all-words.md':
        'Brute checks every window against every permutation — O(n·k!·L) blows up past k=8. Sliding window with word-frequency map is O(n·L) = ~10⁶ ops.',
    '01v-trapping-rain-water.md':
        'Brute computes per-column max-left/max-right in O(n²) = 10⁸ ops at n=10⁴ (borderline). Two-pointer with running max is O(n) = ~10⁶ ops on hot service.',
    # Two-pointer tail
    '02v-boats-to-save-people.md':
        'Brute pairs each person with every other — O(n²) = 2.5·10⁹ ops at n=5·10⁴ (TLE). Sort + two-pointer greedy is O(n log n) = ~10⁶ ops.',
    '02v-intersection-of-two-arrays-ii.md':
        'Brute nested-loop is O(n·m) = 10⁶ ops at n,m=10³. HashMap of counts is O(n+m) = 2·10³ ops, generalises to streaming inputs of 10⁹ elements.',
    '02v-merge-sorted-array.md':
        'Brute concat + sort is O((m+n) log(m+n)) — fine for 10² inputs, misses the point. In-place from-the-back three-pointer is O(m+n) = ~10⁶ pointer ops on real payload sizes.',
    '02v-sort-array-by-parity.md':
        'Brute two-pass (write evens, then odds) is O(n) time + O(n) space. In-place two-pointer partition is O(n) = ~10⁶ ops with O(1) space — the Dutch-flag pattern.',
    '02v-squares-of-a-sorted-array.md':
        'Brute square-then-sort is O(n log n) = 10⁵·17 ≈ 2·10⁶ ops at n=10⁵. Two-pointer from ends (largest square is at one edge) is O(n) = 10⁵ ops.',
    '02v-valid-palindrome-ii.md':
        'Brute tries deleting each char and re-checks — O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Two-pointer with one delete-window is O(n) = 10⁵ ops = <5 ms.',
    '02v-wiggle-sort-ii.md':
        'Brute sort + shuffle is O(n log n) = 10⁵·17 ≈ 2·10⁶ ops. Quickselect + virtual index trick is expected O(n) = 5·10⁴ ops in place.',
    # Fast/slow tail
    '03v-find-the-duplicate-number.md':
        'Brute HashSet is O(n) time + O(n) space (breaks the "no modify + O(1) space" constraint). Floyd\'s cycle detection on the value-index graph is O(n) time + O(1) space — ~10⁶ pointer chases at n=10⁵.',
    '03v-happy-number.md':
        'Brute HashSet of seen sums grows unbounded per unlucky start. Floyd tortoise/hare on the digit-square-sum function is O(log n) iterations for any input up to 10⁹.',
    '03v-middle-of-the-linked-list.md':
        'Brute two-pass (count then walk) is O(n) time but two full traversals — hot service pays 2x cache misses. Fast/slow single pass is O(n) time, ~10⁶ pointer chases with one traversal.',
    '03v-palindrome-linked-list.md':
        'Brute copy to array + two-pointer is O(n) time + O(n) space. Fast/slow to midpoint + reverse-second-half + compare is O(n) time + O(1) space — ~10⁶ pointer ops.',
    # Prefix sum tail
    '04v-car-pooling.md':
        'Brute simulates every km — O(sum of trip lengths) = 10⁹ at max (TLE). Diff-array / bucket approach with 10³ stops uses O(trips + stops) = 2·10³ ops.',
    '04v-corporate-flight-bookings.md':
        'Brute applies each booking to a range — O(bookings·n) = 10⁵·2·10⁴ = 2·10⁹ ops (TLE). Difference-array + prefix sum is O(bookings + n) = 3·10⁵ ops = <5 ms.',
    '04v-count-submatrices-with-target-sum.md':
        'Brute enumerates every submatrix — O(m²·n²) = 10¹⁰ ops at m=n=100 (TLE). Row-pair reduction to 1D subarray-sum-equals-k is O(m²·n) = 10⁶ ops = <100 ms.',
    '04v-matrix-block-sum.md':
        'Brute recomputes each block in O(k²) — O(m·n·k²) = 10⁴·10² = 10⁶ ops at m=n=100, k=10; blows up at larger k. 2D prefix sum is O(m·n) = 10⁴ ops with O(1) per query.',
    '04v-maximal-rectangle.md':
        'Brute enumerates every rectangle in O(m²·n²) = 10⁸ ops at m=n=100 (borderline). Reduce each row to histogram + monotonic stack is O(m·n) = 10⁴ ops = <1 min even at 10⁵ queries.',
    '04v-range-addition-ii.md':
        'Brute applies each update to the full grid — O(ops·m·n) = 10⁴·10⁴·10⁴ = 10¹² ops (dead). Track only the intersection of all mins — O(ops) = 10⁴ ops.',
    '04v-range-addition.md':
        'Brute applies each update by writing every index — O(ops·n) = 10⁴·10⁵ = 10⁹ ops (TLE). Difference array + prefix sum is O(ops + n) = 1.1·10⁵ ops = <5 ms.',
    '04v-subarray-sums-divisible-by-k.md':
        'Brute checks every subarray — O(n²) = 10¹⁰ ops at n=3·10⁴ (TLE). Prefix sum + hashmap of remainders is O(n) = 3·10⁴ ops.',
    # Hashing tail
    '05v-candy.md':
        'Brute repeatedly scans until no changes — O(n²) worst case = 4·10⁸ ops at n=2·10⁴. Two-pass left-then-right sweep is O(n) = 2·10⁴ ops on the hot path.',
    '05v-maximum-product-subarray.md':
        'Brute enumerates every subarray — O(n²) = 4·10⁸ ops at n=2·10⁴ (TLE past ~5 sec). DP tracking min+max at each index (product sign can flip) is O(n) = 2·10⁴ ops.',
    '05v-number-of-islands.md':
        'Brute checks connectivity between every pair of land cells — O((m·n)²) = 10¹⁰ ops at max grid. BFS/DFS flood-fill visits each cell once → O(m·n) = 9·10⁴ ops = <10 ms.',
    '05v-two-sum-ii-input-array-is-sorted.md':
        'Brute nested loop is O(n²) = 10⁸ ops at n=3·10⁴. Two-pointer inward sweep is O(n) = ~10⁶ pointer ops at scale.',
    '05v-two-sum-less-than-k.md':
        'Brute nested loop is O(n²) = 10⁶ ops at n=10³. Sort + two-pointer is O(n log n) = 10⁴ ops with cache-friendly pass.',
    '05v-valid-anagram.md':
        'Brute sort both then compare is O(n log n) = 10⁵·17 ≈ 2·10⁶ ops at n=10⁵. Frequency array of 26 chars is O(n) = 10⁵ ops with O(1) alphabet space.',
    '05v-word-ladder.md':
        'Brute BFS over all pairs is O(N²·L) = 10¹⁰ ops at N=5·10³, L=10 (TLE). Bidirectional BFS with wildcard-bucket adjacency is O(N·L²·26) = ~10⁶ ops.',
    # Monotonic stack tail
    '06v-remove-k-digits.md':
        'Brute tries every combination of k removals — O(C(n,k)) explodes past k=10 (C(10⁵,50) ≈ 10²⁰⁰). Monotonic stack pops digits greedily → O(n) = 10⁵ ops = <5 ms.',
    # Binary search tail
    '07v-search-in-rotated-sorted-array-ii.md':
        'Brute linear scan is O(n) = 5·10³ ops per call. Modified binary search with duplicate-skip is O(log n) average, O(n) worst — still ~10⁶ queries/sec at scale.',
    # Top-K tail
    '09v-k-closest-points-to-origin.md':
        'Brute sorts all n by distance — O(n log n) = 10⁴·14 ≈ 10⁵ ops at n=10⁴. Max-heap of size k is O(n log k), quickselect is expected O(n) = 10⁴ ops.',
    '09v-reorganize-string.md':
        'Brute enumerates permutations — O(n!) = astronomical past n=15. Max-heap of char counts + greedy interleave is O(n log 26) = ~10⁶ ops on 500-char strings.',
    # K-way merge tail
    '10v-merge-two-sorted-lists.md':
        'Brute concat then sort is O((m+n) log(m+n)) = 10⁵·17 ≈ 2·10⁶ ops. Two-pointer merge is O(m+n) = 10⁵ ops with O(1) extra space.',
    '10v-smallest-range-covering-elements-from-k-lists.md':
        'Brute enumerates every k-tuple across lists — O(prod-of-lengths) explodes past k=10. Min-heap of one-per-list + sliding-window max is O(N log k) = ~10⁶ ops at total N=10⁵.',
    '10v-ugly-number-ii.md':
        'Brute checks every integer for 2/3/5-only factorisation — O(n²·log n) misses at n=1690. Three-pointer merge from {2,3,5} is O(n) = 10³ ops.',
    # Merge intervals tail
    '11v-employee-free-time.md':
        'Brute enumerates every pair of intervals — O((sum-of-N)²) = 10⁸ ops at total N=10⁴ (TLE). Min-heap sweep across all intervals is O(N log K) = ~10⁶ ops.',
    '11v-insert-interval.md':
        'Brute concat + merge is O(n log n) = 10⁴·14 ≈ 10⁵ ops at n=10⁴. Single sorted pass with three phases (before / overlap / after) is O(n) = 10⁴ ops.',
    '11v-interval-list-intersections.md':
        'Brute pairs every A×B — O(m·n) = 10⁶ ops at m=n=10³. Two-pointer sweep (advance the interval ending first) is O(m+n) = 2·10³ ops.',
    '11v-meeting-rooms.md':
        'Brute checks every pair — O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Sort by start + linear scan for overlap is O(n log n) = ~10⁶ ops = <10 ms.',
    '11v-remove-covered-intervals.md':
        'Brute checks every pair (i, j) for coverage — O(n²) = 10⁸ ops at n=10⁴. Sort by start ascending, end descending → linear pass with running-max-end is O(n log n) = ~10⁵ ops.',
    # Topological sort tail
    '13v-alien-dictionary.md':
        'Brute enumerates 26! character orderings — dies before universe end. Topo sort of char-pair graph is O(N·L + 26²) = ~10⁴ ops per input; cycle → invalid dict.',
    '13v-minimum-height-trees.md':
        'Brute runs BFS from every node — O(n²) = 10⁸ ops at n=2·10⁴ (TLE). Peel leaves layer by layer (there are 1-2 centroids) is O(n) = 2·10⁴ ops.',
    '13v-parallel-courses.md':
        'Brute simulates semester-by-semester with O(n) scan per semester — O(n²) = 10⁴ ops at n=100 (fine), 10¹⁰ at n=10⁵. Kahn\'s BFS with per-layer count is O(n+E) = ~10⁶ ops.',
    '13v-sequence-reconstruction.md':
        'Brute checks every permutation against all sequences — O(n!·m) astronomical. Topo sort validation with "unique queue element per layer" is O(n+E) = ~10⁶ ops.',
    # Union-Find tail
    '14v-accounts-merge.md':
        'Brute compares every pair of accounts on shared emails — O(A²·E) = 10⁸ ops at A=10³, E=10 (TLE). Union-Find keyed by email is O(A·E·α(A)) = 10⁴ ops.',
    '14v-connecting-cities-with-minimum-cost.md':
        'Brute checks every spanning tree — O(n^(n-2)) via Cayley (dies past n=12). Kruskal + Union-Find is O(E log E) = ~10⁶ ops at E=10⁴.',
    '14v-min-cost-to-connect-all-points.md':
        'Brute enumerates spanning trees — dies past n=12. Prim/Kruskal with Union-Find is O(n² log n) = 10⁶ ops at n=10³ = <5 min at scale.',
    '14v-most-stones-removed-with-same-row-or-column.md':
        'Brute checks every pair of stones — O(n²) = 10⁶ ops at n=10³. Union-Find on (row, col+10000) is O(n·α(n)) = ~10³ ops with 10⁵-way scaling.',
    '14v-redundant-connection.md':
        'Brute DFS-per-edge to check for a cycle is O(E²) = 10⁶ ops at E=10³. Union-Find incremental cycle detection is O(E·α(V)) = 10³ ops — the edge that closes a component is the answer.',
    # Greedy tail
    '15v-course-schedule-iii.md':
        'Brute enumerates 2ⁿ course subsets — 10⁹⁰³⁰ dies at n=10⁴. Sort by deadline + max-heap of chosen durations (swap when over) is O(n log n) = ~10⁶ ops.',
    '15v-jump-game.md':
        'Brute DP tries every reachable index from each position — O(n²) = 10⁸ ops at n=10⁴. Greedy running-max-reach is O(n) = 10⁴ ops = <1 ms.',
    '15v-maximum-length-of-pair-chain.md':
        'Brute enumerates 2ⁿ chains — 10³⁰ ops at n=10². Sort by second-of-pair + linear pass (activity selection) is O(n log n) = ~10⁶ ops.',
    '15v-maximum-subarray.md':
        'Brute enumerates every subarray — O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Kadane\'s DP is O(n) = 10⁵ ops; divide & conquer variant is O(n log n) = 1.7·10⁶ ops.',
    # Backtracking tail
    '16v-beautiful-arrangement.md':
        'Brute enumerates n! permutations — 15! ≈ 10¹² ops = 20 min at 10⁹ ops/sec. Backtracking with divisibility pruning + bitmask visited is O(n·2ⁿ) ≈ 5·10⁵ ops at n=15.',
    '16v-combination-sum-iii.md':
        'Brute enumerates C(9, k) subsets and checks sum — trivial (C(9,4)=126) but scales badly if we generalise. Backtracking with early-terminate on sum > target is O(2⁹) = 512 leaves, ~10⁶ ops for related enumerations.',
    '16v-letter-case-permutation.md':
        'Brute generates all 2ⁿ case-flip strings then filters — same complexity as the backtracking approach: O(2ⁿ) = ~10⁶ ops at n=20 for output size that many strings.',
    '16v-letter-combinations-of-a-phone-number.md':
        'Brute nested-loop concat is fine for tiny inputs but scales badly. Backtracking (DFS across digit→letters map) is O(4ⁿ·n) = ~10⁶ ops at n=10 (max phone-number length).',
    '16v-n-queens-ii.md':
        'Brute checks C(64, 8) placements at n=8 — 4·10⁹ ops (TLE). Backtracking with cols/diag1/diag2 bitmask visits n! = 40320 valid states at n=8 — <10 ms; scales to n=15 in ~10⁶ ops.',
    '16v-next-permutation.md':
        'Brute generates all n! permutations then finds next — 10¹⁶⁵ ops at n=100 (dies). Linear scan from right to find pivot + swap + reverse suffix is O(n) = 100 ops.',
    '16v-palindrome-partitioning.md':
        'Brute enumerates 2ⁿ⁻¹ cuts, checks each part — O(2ⁿ·n) = 10⁶ ops at n=16. Backtracking with pal[][] cache is O(n·2ⁿ) ≈ 10⁶ ops but skips ~99% via pruning.',
    '16v-robot-room-cleaner.md':
        'Brute wanders randomly, no completion guarantee. DFS with visited set + right-hand rule + backtrack move-and-undo is O(rooms) — ~10⁶ ops for a 300×300 grid.',
    '16v-sudoku-solver.md':
        'Brute tries 9^81 = 10⁷⁷ boards (dies before universe end). Backtracking with row/col/box bitmasks + MRV heuristic is O(9^empties) ≈ 10⁶ ops for hard puzzles.',
    '16v-valid-sudoku.md':
        'Brute nested triple-loop is O(9²·9) = 729 ops — trivial. Set-based row/col/box check is O(81) = 81 ops per full validation, ~10⁶ ops/sec for streaming boards.',
    # D&C tail
    '17v-count-of-range-sum.md':
        'Brute enumerates every (i, j) pair — O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Merge-sort D&C with two-pointer range count is O(n log n) = 1.7·10⁶ ops = <20 ms.',
    '17v-global-and-local-inversions.md':
        'Brute counts every inversion pair — O(n²) = 2.5·10⁹ ops at n=5·10⁴. Observation: global = local iff no index differs from value by > 1 → O(n) = 5·10⁴ ops.',
    '17v-reverse-pairs.md':
        'Brute nested-loop pair check is O(n²) = 2.5·10⁹ ops at n=5·10⁴ (TLE). Merge-sort D&C or BIT with coord compression is O(n log n) = ~10⁶ ops.',
    '17v-sort-list.md':
        'Brute copy-to-array + `Arrays.sort` breaks the "sort in-place on linked list" constraint. Merge sort with slow/fast midpoint + iterative merge is O(n log n) = 5·10⁵·17 ≈ 10⁷ ops with O(log n) stack — ~1 hour at Facebook feed scale.',
    # DP outliers
    '18v-number-of-ways-to-wear-different-hats-to-each-other.md':
        'Brute enumerates 40! hat orderings — 10⁴⁷ ops (dies). Bitmask DP over people (n ≤ 10 → 2ⁿ=1024 states) iterating hats is O(40·2ⁿ·n) = 4·10⁵ ops.',
    '18v-paint-house-ii.md':
        'Brute recursion tries k colors at each of n houses — O(k^n) = 10^(0.5n) dies past n=100. DP with "best + second-best previous color" trick is O(n·k) = 10⁵ ops at n=100, k=10³.',
    # Trie tail
    '19v-count-pairs-with-xor-in-a-range.md':
        'Brute enumerates every pair XOR — O(n²) = 4·10⁸ ops at n=2·10⁴ (TLE). Bit-trie + range decomposition is O(n·30·2) = ~10⁶ ops.',
    '19v-design-add-and-search-words-data-structure.md':
        'Brute HashSet of words + brute-scan on wildcards — O(N·L) per wildcard search dies at 10⁵ queries. Trie + DFS for `.` wildcards is O(L·26^wildcards) per query — ~10⁶ ops even under load.',
    '19v-maximum-xor-with-an-element-from-array.md':
        'Brute checks every pair — O(n·q) = 10¹⁰ ops at n=q=10⁵ (TLE). Offline sort + bit-trie insert-and-query is O((n+q)·31) = ~10⁶ ops.',
    '19v-stream-of-characters.md':
        'Brute checks every dictionary word against each stream suffix — O(sum-of-word-lengths·stream-length) = 10⁹ ops (TLE). Reverse-trie walked with each new char is O(max-word-length) per char = 10⁶ ops for 4·10⁴ chars.',
    # Bit manip tail
    '20v-find-the-difference.md':
        'Brute HashMap of counts is O(n) + O(n) space. XOR-fold s+t is O(n) time + O(1) space — ~10⁶ ops on 1000-char input, no allocations.',
    '20v-hamming-distance.md':
        'Brute char-by-char binary compare is O(32) = 32 ops. `Integer.bitCount(a ^ b)` is 1 XOR + 1 popcnt intrinsic = 2 CPU cycles — ~10⁹ ops/sec on modern hardware.',
    '20v-maximum-product-of-word-lengths.md':
        'Brute compares every pair of words char-by-char — O(n²·L²) = 10⁹ ops at n=10³, L=10³ (TLE). Bitmask of 26-letter presence + AND==0 test is O(n²) = 10⁶ ops.',
    '20v-missing-number.md':
        'Brute sort + scan is O(n log n) = 10⁴·14 ≈ 10⁵ ops. XOR of [0..n] with the array is O(n) = 10⁴ ops with O(1) space and no allocations.',
    '20v-number-of-1-bits.md':
        'Brute bit-shift loop is O(32) = 32 ops. `Integer.bitCount` is 1 hardware popcnt = ~1 CPU cycle → 10⁹ ops/sec.',
    '20v-power-of-two.md':
        'Brute divide-by-2 loop is O(log n) = 30 iters at n=2³¹. Bit trick `n>0 && (n&(n-1))==0` is 2 ops = <1 ns — 10⁹ checks/sec.',
    '20v-reverse-bits.md':
        'Brute bit-by-bit reverse loop is O(32) = 32 ops. Divide-and-conquer swap adjacent / pairs / nibbles / bytes is 12 ops — ~10⁸ reversals/sec.',
    '20v-subsets.md':
        'Brute recursive expansion is O(n·2ⁿ) = 10⁷ ops at n=20. Bitmask iteration over [0..2ⁿ) generating each subset directly is O(2ⁿ) = 10⁶ ops with better cache pattern.',
    '20v-sum-of-all-subset-xor-totals.md':
        'Brute enumerates 2ⁿ subsets, XORs each — O(n·2ⁿ) = 10⁵ ops at n=12. Bit-linearity trick: each bit contributes `sum·2^(n-1)` → O(n) = 12 ops = <1 microsec.',
}


def already_has_drama(text: str) -> bool:
    return bool(
        re.search(r'\b1[0-9]\^[6-9]', text) or
        re.search(r'10[\u2076\u2077\u2078\u2079\u00b9]', text) or
        re.search(r'\b10\^[6-9]', text) or
        re.search(r'\b\d+\s*(?:min|sec|hour|day|year|billion|trillion)', text, re.IGNORECASE)
    )


CONSTRAINT_RX = re.compile(r'^(\*\*Constraints\*\*\s*—\s*.+?)(\.?)\s*$', re.MULTILINE)


def append_drama(text: str, drama: str) -> str | None:
    match = CONSTRAINT_RX.search(text)
    if not match:
        return None
    original = match.group(1).rstrip()
    if not original.endswith('.'):
        original += '.'
    new_line = f'{original} {drama}'
    return text[:match.start()] + new_line + text[match.end():]


def main() -> None:
    src = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'
    changed = 0
    for name, drama in DRAMA.items():
        path = src / name
        if not path.exists():
            print(f'  skip (missing): {name}')
            continue
        text = path.read_text(encoding='utf-8')
        if already_has_drama(text):
            print(f'  skip (already has D): {name}')
            continue
        updated = append_drama(text, drama)
        if updated is None:
            print(f'  skip (no constraint line): {name}')
            continue
        path.write_text(updated, encoding='utf-8')
        changed += 1
        print(f'  +D {name}')
    print(f'\nDone: added drama to {changed}/{len(DRAMA)} pages.')


if __name__ == '__main__':
    main()
