# Binary Search — Search in Rotated Sorted Array II (with duplicates)

*[↗ LeetCode: Search in Rotated Sorted Array II](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/binary-search)

Same as I but duplicates allowed. Return true/false.

**Example** — `nums=[2,5,6,0,0,1,2], target=0` → `true`

---

## Approach 1 — Linear scan

O(n). Baseline.

## Approach 2 — Modified binary search with duplicate shrink

**Insight from Search Rotated I.** The "sorted-half" detection relied on `a[lo] != a[mid]`. When they're equal (and `a[hi]` too), we can't decide → shrink `lo`/`hi` by 1 each and try again.

```java
boolean search(int[] a, int t) {
    int lo = 0, hi = a.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == t) return true;
        if (a[lo] == a[mid] && a[mid] == a[hi]) { lo++; hi--; }
        else if (a[lo] <= a[mid]) {
            if (a[lo] <= t && t < a[mid]) hi = mid - 1;
            else                          lo = mid + 1;
        } else {
            if (a[mid] < t && t <= a[hi]) lo = mid + 1;
            else                          hi = mid - 1;
        }
    }
    return false;
}
```

<CodeTrace
  title="With duplicates — [2,5,6,0,0,1,2], target=0"
  :values="[2,5,6,0,0,1,2]"
  :windowKeys="['lo','hi']"
  :cellWidth="38"
  :steps='[
    { pointers: { lo: 0, hi: 6, mid: 3 }, vars: { "a": "[2,5,6,0,0,1,2]" }, note: "a[mid]=0 = target → return true", added: [3] }
  ]'
/>

**Complexity** — Time **O(log n)** avg, **O(n)** worst-case (all duplicates); Space **O(1)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Linear | O(n) | O(1) |
| BS with dup shrink | **O(log n)** avg, O(n) worst | **O(1)** |

## Related problems

- [Search in Rotated Sorted Array I](/problems/binary-search-rotated-sorted) — no duplicates
- [Find Minimum in Rotated Sorted Array II](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/) — same dup handling
