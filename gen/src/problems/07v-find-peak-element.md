# Binary Search — Find Peak Element

*[↗ LeetCode: Find Peak Element](https://leetcode.com/problems/find-peak-element/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/binary-search)

A peak is `nums[i] > nums[i-1]` and `nums[i] > nums[i+1]`. Return **any** peak's index. O(log n).

**Example 1** — `[1,2,3,1]` → `2`
**Example 2** — `[1,2,1,3,5,6,4]` → `1` or `5`

---

## Approach 1 — Linear scan

O(n). Baseline.

## Approach 2 — Binary search (climb uphill)

**Insight.** At any `mid`, compare `a[mid]` with `a[mid+1]`. If `a[mid] < a[mid+1]`, a peak exists in `(mid, hi]` — climb right. Else a peak exists in `[lo, mid]` — descend left.

**Why it works.** The "uphill" side is guaranteed to hit a peak because the boundary values are `-∞`.

```java
int findPeakElement(int[] a) {
    int lo = 0, hi = a.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < a[mid + 1]) lo = mid + 1;
        else                     hi = mid;
    }
    return lo;
}
```

<CodeTrace
  title="Uphill climb — [1,2,1,3,5,6,4]"
  :values="[1,2,1,3,5,6,4]"
  :windowKeys="['lo','hi']"
  :cellWidth="38"
  :steps='[
    { pointers: { lo: 0, hi: 6, mid: 3 }, vars: { "a[mid]": 3, "a[mid+1]": 5 }, note: "uphill → lo = 4" },
    { pointers: { lo: 4, hi: 6, mid: 5 }, vars: { "a[mid]": 6, "a[mid+1]": 4 }, note: "downhill → hi = 5" },
    { pointers: { lo: 4, hi: 5, mid: 4 }, vars: { "a[mid]": 5, "a[mid+1]": 6 }, note: "uphill → lo = 5" },
    { pointers: { lo: 5, hi: 5 }, vars: { peak: 5 }, note: "converged → peak at idx 5", added: [5] }
  ]'
/>

**Complexity** — Time **O(log n)**; Space **O(1)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Linear | O(n) | O(1) |
| BS uphill | **O(log n)** | **O(1)** |

## Related problems

- [Find Peak Element II (2D)](https://leetcode.com/problems/find-a-peak-element-ii/) — 2D peak
- [Peak Index in Mountain Array](https://leetcode.com/problems/peak-index-in-a-mountain-array/) — guaranteed one peak
- [Find in Mountain Array](https://leetcode.com/problems/find-in-mountain-array/) — peak-then-two-BS
