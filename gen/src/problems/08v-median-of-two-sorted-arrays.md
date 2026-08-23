# BS on Answer — Median of Two Sorted Arrays

*[↗ LeetCode: Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/bs-on-answer)

Given two sorted arrays, return the median in **O(log(min(m,n)))**.

**Example** — `A=[1,3], B=[2]` → `2.0`

**Constraints** — `0 ≤ n, m ≤ 1000`; total ≥ 1.

---

## Approach 1 — Merge sort halves

O(m+n). Doesn't beat the log bar.

## Approach 2 — Binary search on the partition point

**Insight.** A valid partition places `(m+n+1)/2` elements on the left. Search `i` in `A`; then `j = (m+n+1)/2 - i` in `B`. Valid when `A[i-1] ≤ B[j]` and `B[j-1] ≤ A[i]`.

**Trap.** Always search the *shorter* array to keep `j` in range.

```java
double findMedianSortedArrays(int[] A, int[] B) {
    if (A.length > B.length) return findMedianSortedArrays(B, A);
    int m = A.length, n = B.length;
    int total = m + n;
    int lo = 0, hi = m;
    while (lo <= hi) {
        int i = (lo + hi) / 2, j = (total + 1) / 2 - i;
        int Aleft = i == 0 ? Integer.MIN_VALUE : A[i - 1];
        int Aright = i == m ? Integer.MAX_VALUE : A[i];
        int Bleft = j == 0 ? Integer.MIN_VALUE : B[j - 1];
        int Bright = j == n ? Integer.MAX_VALUE : B[j];
        if (Aleft <= Bright && Bleft <= Aright) {
            if (total % 2 == 1) return Math.max(Aleft, Bleft);
            return (Math.max(Aleft, Bleft) + Math.min(Aright, Bright)) / 2.0;
        }
        if (Aleft > Bright) hi = i - 1;
        else                lo = i + 1;
    }
    return 0;
}
```

**Complexity** — Time **O(log(min(m, n)))**; Space **O(1)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Merge halves | O(m + n) | O(1) |
| BS on partition | **O(log min(m,n))** | O(1) |

## When to use which

- **"Median of two sorted"** → BS on smaller array (O(log min)).
- **"Median of k sorted"** → heap or divide-and-conquer.
- **"kth of two sorted"** → same BS with different partition target.

## Related problems

- [Kth Smallest in Two Sorted Arrays](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/)
- [Merge Two Sorted Lists](/problems/merge-two-sorted-lists)