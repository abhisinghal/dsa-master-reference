# BS on Answer — Find K-th Smallest Pair Distance

*[↗ LeetCode: Find K-th Smallest Pair Distance](https://leetcode.com/problems/find-k-th-smallest-pair-distance/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/bs-on-answer)

Given `nums` and integer `k`, return the k-th smallest **absolute** distance among all pairs.

**Example** — `nums=[1,3,1], k=1` → `0` (pair (1,1) has distance 0)

---

## Approach 1 — Enumerate all pairs, sort

O(n²) pairs, O(n² log n²) sort. TLE at n=10⁴.

## Approach 2 — Binary search on distance + sliding window count

**Insight.** Sort the array. `countLE(d)` = number of pairs with distance ≤ d — computed via sliding window in O(n): for each right `j`, shrink left `i` while `a[j] - a[i] > d`; add `j - i` pairs.

`countLE(d)` is monotonic in d. Binary-search the smallest d with `countLE(d) ≥ k`.

```java
int smallestDistancePair(int[] nums, int k) {
    Arrays.sort(nums);
    int n = nums.length;
    int lo = 0, hi = nums[n - 1] - nums[0];
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        int count = 0, i = 0;
        for (int j = 0; j < n; j++) {
            while (nums[j] - nums[i] > mid) i++;
            count += j - i;
        }
        if (count < k) lo = mid + 1;
        else           hi = mid;
    }
    return lo;
}
```

**Complexity** — Time **O(n log(max-min))**; Space **O(1)** aside from sort.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Enumerate all pairs | O(n²) | O(n²) |
| BS on distance | **O(n log(max-min))** | O(1) |

## Related problems

- [Kth Smallest Element in a Sorted Matrix](/problems/kth-smallest-element-in-a-sorted-matrix)
- [Find K Closest Elements](https://leetcode.com/problems/find-k-closest-elements/)
- [Koko Eating Bananas](/problems/bs-on-answer-koko-bananas)
