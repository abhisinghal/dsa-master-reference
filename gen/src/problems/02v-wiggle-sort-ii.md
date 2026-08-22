# Two Pointers — Wiggle Sort II

*[↗ LeetCode: Wiggle Sort II](https://leetcode.com/problems/wiggle-sort-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

Reorder `nums` so `a[0] < a[1] > a[2] < a[3] …` (strict — differs from Wiggle Sort I).

---

## Approach 1 — Sort + interleave
Sort. Place larger half at odd indices (in reverse), smaller half at even indices (in reverse). Reverse orders prevent duplicates on the boundary from colliding.

```java
void wiggleSort(int[] nums) {
    int[] sorted = nums.clone();
    Arrays.sort(sorted);
    int n = nums.length, mid = (n + 1) / 2, r = n - 1, i = 0;
    // even indices get larger-of-smaller-half (reverse), odd get largest (reverse)
    for (int k = 0; k < n; k++)
        nums[k] = (k % 2 == 0) ? sorted[--mid] : sorted[r--];
}
```

Wait: careful. Standard formulation: even indices ← smaller-half reversed; odd ← larger-half reversed. Reversal prevents adjacent duplicates when median values dominate.

**Complexity** — Time **O(n log n)**; Space **O(n)**.

---

## Approach 2 — Quickselect median + 3-way partition + virtual indexing
**Insight.** Find median via Quickselect. Then use a virtual index mapping `A(i) = (2i + 1) % (n | 1)`. Dutch-flag partition wrt median under this mapping places larger on odd indices, smaller on even, with median centered.

**Complexity** — Time **O(n)** average; Space **O(1)** extra.

Code is subtle — study the classic Dutch-flag-with-virtual-index writeup before an interview.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort + interleave | O(n log n) | O(n) | baseline |
| Quickselect median + 3-way partition + vir… | O(n) | O(1) | optimum |

## When to use which

- **State it for signal** → Sort + interleave (O(n log n)). Correct baseline; call it out then move on.
- **Ship this** → Quickselect median + 3-way partition + virtual indexing (O(n), O(1)). Expected optimum in interview.

## Related problems

- [Wiggle Sort I](https://leetcode.com/problems/wiggle-sort/) — non-strict, greedy swap works
- [Kth Largest](/problems/kth-largest-element-in-an-array) — same Quickselect
- [Sort Colors](https://leetcode.com/problems/sort-colors/) — Dutch flag partition
