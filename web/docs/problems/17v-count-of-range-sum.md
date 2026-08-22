# Divide & Conquer — Count of Range Sum

*[↗ LeetCode: Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/divide-conquer)

Given `nums` and `[lower, upper]`, count subarray sums in `[lower, upper]`.

**Example** — `nums=[-2,5,-1], lower=-2, upper=2` → `3` (subarrays: `[-2]`, `[-2,5,-1]`, `[-1]`)

---

## Approach 1 — Brute (all subarrays)

O(n²). TLE at n=10⁵.

## Approach 2 — Merge sort on prefix sums

**Insight.** Subarray sum `nums[i..j] = P[j+1] - P[i]`. Count pairs `(i, j)` with `lower ≤ P[j] − P[i] ≤ upper`.

Merge sort the prefix-sums array. During each merge, since both halves are sorted, use two pointers per left value to count right values within the range.



```java
int countRangeSum(int[] nums, int lower, int upper) {
    long[] P = new long[nums.length + 1];
    for (int i = 0; i < nums.length; i++) P[i + 1] = P[i] + nums[i];
    return countMerge(P, 0, P.length - 1, lower, upper);
}
int countMerge(long[] P, int lo, int hi, int lower, int upper) {
    if (lo >= hi) return 0;
    int mid = (lo + hi) / 2;
    int count = countMerge(P, lo, mid, lower, upper) + countMerge(P, mid + 1, hi, lower, upper);
    int j = mid + 1, k = mid + 1;
    for (int i = lo; i <= mid; i++) {
        while (j <= hi && P[j] - P[i] < lower) j++;
        while (k <= hi && P[k] - P[i] <= upper) k++;
        count += k - j;
    }
    // standard merge
    long[] tmp = new long[hi - lo + 1];
    int p = lo, q = mid + 1, idx = 0;
    while (p <= mid && q <= hi) tmp[idx++] = P[p] <= P[q] ? P[p++] : P[q++];
    while (p <= mid) tmp[idx++] = P[p++];
    while (q <= hi)  tmp[idx++] = P[q++];
    for (int i = 0; i < tmp.length; i++) P[lo + i] = tmp[i];
    return count;
}
```



**Complexity** — Time **O(n log n)**; Space **O(n)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute | O(n²) | O(1) |
| Merge sort on prefixes | **O(n log n)** | O(n) |

## Related problems

- [Reverse Pairs](/problems/reverse-pairs) — same technique on raw values
- [Count of Smaller Numbers After Self](/problems/divide-conquer-inversions) — merge sort + counting
- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k) — exact target, hash map suffices
