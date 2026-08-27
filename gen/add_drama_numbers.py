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
