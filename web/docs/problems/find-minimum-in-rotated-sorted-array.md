# Binary Search — Find Minimum in Rotated Sorted Array

*[↗ LeetCode: Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/binary-search)

Given a rotated ascending array with distinct values, return the minimum. O(log n).

**Example** — `[4,5,6,7,0,1,2]` → `0`

---

## Approach 1 — Linear scan

O(n). Baseline.

## Approach 2 — Binary search for the pivot

**Insight.** The array has two ascending halves. Compare `nums[mid]` to `nums[hi]`:
- If `nums[mid] > nums[hi]`: the min is in `(mid, hi]`; go right.
- Else: min is in `[lo, mid]`; go left (keep mid as candidate).

**Trap.** Compare to `nums[hi]`, not `nums[lo]`. Using lo fails on already-sorted (rotation = 0).



```java
int findMin(int[] a) {
    int lo = 0, hi = a.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] > a[hi]) lo = mid + 1;
        else                hi = mid;
    }
    return a[lo];
}
```



<CodeTrace
  title="Pivot search — [4,5,6,7,0,1,2]"
  :values="[4,5,6,7,0,1,2]"
  :windowKeys="['lo','hi']"
  :cellWidth="38"
  :steps='[
    { pointers: { lo: 0, hi: 6, mid: 3 }, vars: { "a[mid]": 7, "a[hi]": 2 }, note: "7 gt 2 → lo = mid+1 = 4" },
    { pointers: { lo: 4, hi: 6, mid: 5 }, vars: { "a[mid]": 1, "a[hi]": 2 }, note: "1 lt 2 → hi = mid = 5" },
    { pointers: { lo: 4, hi: 5, mid: 4 }, vars: { "a[mid]": 0 }, note: "0 lt 2 → hi = 4" },
    { pointers: { lo: 4, hi: 4 }, vars: { min: 0 }, note: "converged → 0", added: [4] }
  ]'
/>

**Complexity** — Time **O(log n)**; Space **O(1)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Linear | O(n) | O(1) |
| Binary search | **O(log n)** | **O(1)** |

## Related problems

- [Search in Rotated Sorted Array](/problems/binary-search-rotated-sorted) — this + one more BS
- [Find Minimum in Rotated Sorted Array II](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/) — with duplicates → worst-case O(n)
- [Find Peak Element](/problems/find-peak-element)
