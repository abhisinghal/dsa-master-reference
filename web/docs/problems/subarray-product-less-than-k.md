# Sliding Window — Subarray Product Less Than K

*[↗ LeetCode: Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Count contiguous subarrays whose product is strictly less than `k`. **Positive values only.**

---

## Approach 1 — Sliding window with product
**Insight.** Fix `r`. Shrink `l` while product ≥ k. Every subarray ending at `r` with left ≥ current `l` is valid → contributes `r - l + 1` new subarrays.



```java
int numSubarrayProductLessThanK(int[] nums, int k) {
    if (k <= 1) return 0;
    long prod = 1;
    int count = 0, l = 0;
    for (int r = 0; r < nums.length; r++) {
        prod *= nums[r];
        while (prod >= k) prod /= nums[l++];
        count += r - l + 1;
    }
    return count;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

**Trap.** `k <= 1` — no product of positives is &lt; 1, return 0 early. Guard against integer overflow with `long prod`.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sliding window with product | O(n) | O(1) | primary |

## When to use which

- **Ship this** → Sliding window with product (O(n), O(1)). The pattern's standard solution.

## Related problems

- [Binary Subarrays With Sum](/problems/binary-subarrays-with-sum) — count = f(≤ goal) - f(≤ goal-1)
- [Count Number of Nice Subarrays](/problems/count-number-of-nice-subarrays)
- [Subarrays with K Different Integers](/problems/subarrays-with-k-different-integers) — same "≤ K minus ≤ K-1" trick
