# DP — Maximum Sum Circular Subarray

*[↗ LeetCode: Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Max subarray sum in a **circular** array.

---

## Approach 1 — Kadane on both max and min
**Insight.** Answer is either:
- **Non-wrapping**: standard Kadane max.
- **Wrapping**: `totalSum - minSubarraySum` (subtract out the "middle").

Return `max(kadaneMax, total - kadaneMin)`. **Edge case:** if all numbers are negative, `total - kadaneMin` computes to 0 (empty subarray) — return `kadaneMax` instead.



```java
int maxSubarraySumCircular(int[] nums) {
    int total = 0, curMax = 0, curMin = 0, maxSum = nums[0], minSum = nums[0];
    for (int x : nums) {
        total += x;
        curMax = Math.max(curMax + x, x);
        maxSum = Math.max(maxSum, curMax);
        curMin = Math.min(curMin + x, x);
        minSum = Math.min(minSum, curMin);
    }
    return maxSum > 0 ? Math.max(maxSum, total - minSum) : maxSum;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Kadane on both max and min | O(n) | O(1) | primary |

## When to use which

- **Ship this** → Kadane on both max and min (O(n), O(1)). The pattern's standard solution.

## Related problems

- [Maximum Subarray](/problems/maximum-subarray) — Kadane
- [Maximum Product Subarray](/problems/maximum-product-subarray)
