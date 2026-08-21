"""Add a `### When NOT to use it` block to the pattern chapters that DO have rich
intros but lack this consistency guardrail. Placed right before the first ## H2.
"""
import os, re

ROOT = os.path.join(os.path.dirname(__file__), "src")

WHEN_NOT = {
 "22-two-pointers.md": (
   "The array **isn't sorted** and you can't afford to sort it (O(n log n) prep) — try a hash-map approach instead. "
   "Or the problem needs a *contiguous window* rather than a boundary discard — that's [Sliding Window](#sliding-window)."
 ),
 "24-prefix-sum.md": (
   "You need to *update* array values *and* query ranges in the same run — a plain prefix sum is O(1) query but O(n) update. "
   "For both operations in O(log n), reach for [Fenwick / segment tree](#segment-tree-fenwick-tree)."
 ),
 "25-hashing.md": (
   "You need a *contiguous* result (subarray, substring) and the running quantity is monotone — [Sliding Window](#sliding-window) is O(1) extra space vs. "
   "the map's O(n). Also skip hashing when the *order* between duplicates matters (hash maps lose it)."
 ),
 "27-binary-search.md": (
   "The data isn't sorted / monotone — you can't halve safely. Sort first (O(n log n)) or scan linearly. Also skip when random-access lookup is expensive "
   "(linked lists) — walking to `mid` is O(n) there, killing the log advantage."
 ),
 "35-greedy.md": (
   "A locally-best choice can be regretted later — construct a counterexample (\"if I take the largest coin first…\") and if you find one, switch to [Dynamic Programming](#dynamic-programming). "
   "The exchange-argument proof is what separates a safe greedy from a wrong one."
 ),
 "36-backtracking.md": (
   "You want *one* answer, not all — a pruned DFS or DP is faster than enumerating every branch. Also skip when the state space is polynomial (n·k tuples) and DP fits — "
   "an exponential search is unnecessary."
 ),
 "38-dp.md": (
   "Subproblems don't repeat — pure recursion is fine. Also skip when a **greedy** local choice is provably safe (simpler, same complexity). If state count blows up "
   "beyond ~10⁷, DP is too slow — look for structural insights or Kadane-style running-aggregate tricks."
 ),
 "40-bit-manip.md": (
   "n > ~20 and you're considering bitmask DP — 2ⁿ blows past 10⁶. Also, bit tricks that look clever but yield the same complexity as a `HashSet` add reading cost with no gain — "
   "reserve them for problems where the O(1) bitmap operation is genuinely a win."
 ),
}

RECOGNIZE = {
 "22-two-pointers.md": [
   "sorted array + \"find pair / triplet summing to X\"",
   "\"partition\" / \"in-place two-value split\" — Dutch National Flag, Sort Colors",
   "palindrome check, container-with-most-water, trapping rain water (two-pointer variant)",
 ],
 "24-prefix-sum.md": [
   "many range-sum queries over a static array — precompute pre[], each query is O(1)",
   "\"count subarrays with sum k\" (with hash map, works for negative values too)",
   "\"range-update, point-query\" — the difference-array mirror",
 ],
 "25-hashing.md": [
   "\"pair / triplet summing to target\", \"any duplicate?\", \"first non-repeated\"",
   "\"group by canonical key\" — anagrams, isomorphic strings, group shifted strings",
   "\"seen this before?\" — cycle detection in a functional graph (Happy Number), longest consecutive sequence",
 ],
 "27-binary-search.md": [
   "\"first / last index of x in a sorted array\"",
   "\"search rotated sorted array\", \"find peak\", \"minimum in rotated\"",
   "\"first true / last false\" — any binary boundary in monotone data",
 ],
 "35-greedy.md": [
   "\"fewest / smallest / earliest\" with a locally safe choice",
   "sort-then-sweep problems — activity selection, interval scheduling, non-overlapping intervals",
   "\"jump game\" family, \"gas station\" — verify total feasibility, commit to the earliest reset",
 ],
 "36-backtracking.md": [
   "\"enumerate all\" — subsets, permutations, combinations, N-Queens boards",
   "constraint satisfaction — Sudoku, word search on a grid, expression evaluation",
   "n ≤ ~15 (2ⁿ ≤ 32 K) so exponential search is affordable with pruning",
 ],
 "38-dp.md": [
   "\"how many ways / min-max cost / can I reach\" over discrete choices",
   "overlapping subproblems — the naive recursion re-solves f(n−1), f(n−2) exponentially",
   "families: 1D DP · knapsack · grid · subsequence (LIS/LCS/edit distance) · interval DP · state-machine · tree DP · bitmask DP",
 ],
 "40-bit-manip.md": [
   "n ≤ 20 and you're enumerating subsets — a mask is the set",
   "\"single number\" / \"XOR of everything cancels pairs\"",
   "\"count set bits\" / \"lowest set bit\" / \"is power of two?\"",
 ],
}

def process(fname, when_not, recognize):
    path = os.path.join(ROOT, fname)
    txt = open(path, encoding="utf-8").read()
    if "### When NOT to use it" in txt:
        print(f"  = already has When NOT: {fname}")
        return
    m = re.search(r'^## ', txt, re.MULTILINE)
    if not m:
        print(f"  ! no H2 in {fname}")
        return
    recognize_block = "### Recognize by\n" + "\n".join(f"- {b}" for b in recognize) + "\n\n"
    when_not_block = "### When NOT to use it\n" + when_not + "\n\n---\n\n"
    insert = recognize_block + when_not_block
    new_txt = txt[:m.start()] + insert + txt[m.start():]
    open(path, "w", encoding="utf-8").write(new_txt)
    print(f"  + added Recognize + When NOT: {fname}")

if __name__ == "__main__":
    for fname in RECOGNIZE:
        process(fname, WHEN_NOT[fname], RECOGNIZE[fname])
    print(f"\ndone: {len(RECOGNIZE)} chapters processed")
