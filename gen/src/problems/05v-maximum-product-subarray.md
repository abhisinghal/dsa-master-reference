# Hashing — Maximum Product Subarray

*[↗ LeetCode: Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Return max product of a contiguous subarray. (Filed near hashing/DP.)

---

## Approach 1 — Try every subarray
O(n²).

---

## Approach 2 — Track min and max ending at i
**Insight.** A negative number flips min ↔ max on the next step. Maintain both.

```java
int maxProduct(int[] nums) {
    int maxE = nums[0], minE = nums[0], best = nums[0];
    for (int i = 1; i < nums.length; i++) {
        int x = nums[i];
        int nMax = Math.max(x, Math.max(maxE * x, minE * x));
        int nMin = Math.min(x, Math.min(maxE * x, minE * x));
        maxE = nMax; minE = nMin;
        best = Math.max(best, maxE);
    }
    return best;
}
```

**Complexity** — Time **O(n)**; Space **O(1)**.

**Trap.** Reset both to `nums[i]` when a zero appears (implicitly handled by the `max(x, …)`/`min(x, …)`).

---

## Approach 3 — Prefix + suffix product sweep
Two passes: multiply running prefix; on zero reset to 1. Repeat right-to-left. Answer = max over both sweeps. Elegant on paper; slower to explain.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Try every subarray | O(n²) | — | baseline |
| Track min and max ending at i | O(n) | O(1) | improved |
| Prefix + suffix product sweep | — | — | optimum |

## When to use which

- **State it for signal** → Try every subarray (O(n²)). Correct baseline; call it out then move on.
- **Intermediate refinement** → Track min and max ending at i (O(n)).
- **Ship this** → Prefix + suffix product sweep (—, —). Expected optimum in interview.

## Related problems

- [Maximum Subarray (Kadane)](/problems/maximum-subarray) — sum sibling
- [Maximum Sum Circular Subarray](/problems/maximum-sum-circular-subarray)
