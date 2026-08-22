# Greedy — Maximum Subarray (Kadane)

*[↗ LeetCode: Maximum Subarray](https://leetcode.com/problems/maximum-subarray/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Max sum of a contiguous non-empty subarray.

---

## Approach 1 — All subarrays O(n²) or prefix-sum O(n²)

---

## Approach 2 — Kadane
**Insight.** `bestEndingHere` either extends previous or restarts at current: `max(x, bestEndingHere + x)`. Global answer = max over all i.

```java
int maxSubArray(int[] nums) {
    int best = nums[0], cur = nums[0];
    for (int i = 1; i < nums.length; i++) {
        cur = Math.max(nums[i], cur + nums[i]);
        best = Math.max(best, cur);
    }
    return best;
}
```

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Approach 3 — Divide & Conquer
`max(left, right, crossing)`. **O(n log n)**. Interview curiosity — used to teach recursion but not competitive with Kadane.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| All subarrays O(n²) or prefix-sum O(n²) | — | — | baseline |
| Kadane | O(n) | O(1) | improved |
| Divide & Conquer | O(n log n) | — | optimum |

## When to use which

- **State it for signal** → All subarrays O(n²) or prefix-sum O(n²) (—). Correct baseline; call it out then move on.
- **Intermediate refinement** → Kadane (O(n)).
- **Ship this** → Divide & Conquer (O(n log n), —). Expected optimum in interview.

## Related problems

- [Maximum Product Subarray](/problems/maximum-product-subarray) — min/max tracking
- [Maximum Sum Circular Subarray](/problems/maximum-sum-circular-subarray) — Kadane + reverse-Kadane
- [Best Time to Buy and Sell Stock](/problems/best-time-to-buy-and-sell-stock) — Kadane on diffs
