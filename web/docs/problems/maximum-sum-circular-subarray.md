# DP — Maximum Sum Circular Subarray

*[↗ LeetCode: Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Max subarray sum in a **circular** array.

**Example 1** — `nums=[1,-2,3,-2]` → `3`
**Example 2** — `nums=[5,-3,5]` → `10`
**Example 3** — `nums=[-3,-2,-3]` → `-2`

**Constraints** — `1 ≤ n ≤ 3·10⁴`.

---

## Approach — Kadane on both max and min (canonical)

**Insight.** Answer is either:
- **Non-wrapping**: standard Kadane max.
- **Wrapping**: `totalSum - minSubarraySum`.

**Edge case.** If all negative, `total - minSubSum = 0` (empty) → return kadaneMax instead.



```java
int maxSubarraySumCircular(int[] nums) {
    int total = 0, curMax = 0, curMin = 0, maxS = nums[0], minS = nums[0];
    for (int x : nums) {
        total += x;
        curMax = Math.max(curMax + x, x);
        maxS = Math.max(maxS, curMax);
        curMin = Math.min(curMin + x, x);
        minS = Math.min(minS, curMin);
    }
    return maxS > 0 ? Math.max(maxS, total - minS) : maxS;
}
```



<CodeTrace
  title="Kadane on both max and min (canonical)"
  :values="['1', '-2', '3', '-2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Kadane × 2 + edge | **O(n)** | O(1) | canonical |

## When to use which

- **Circular** → dual Kadane.
- **Linear** → standard Kadane.
- **"Return the subarray"** → track indices.

## Related problems

- [Maximum Subarray](/problems/maximum-subarray)
- [Maximum Product Subarray](/problems/maximum-product-subarray)
