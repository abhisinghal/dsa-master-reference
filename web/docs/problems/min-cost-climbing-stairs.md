# DP — Min Cost Climbing Stairs

*[↗ LeetCode: Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/dp)

Each step has cost. Can start at 0 or 1; step 1 or 2 at a time. Min cost to reach past-the-end.

---

## Approach 1 — DP, O(1) space
**Insight.** `dp[i]` = min cost to arrive at step i. `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`.



```java
int minCostClimbingStairs(int[] cost) {
    int a = 0, b = 0;
    for (int i = 2; i <= cost.length; i++) {
        int c = Math.min(b + cost[i - 1], a + cost[i - 2]);
        a = b; b = c;
    }
    return b;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| DP, O(1) space | O(n) | O(1) | primary |

## When to use which

- **Ship this** → DP, O(1) space (O(n), O(1)). The pattern's standard solution.

## Related problems

- [Climbing Stairs](/problems/climbing-stairs) — counting version
- [House Robber](/problems/dp-house-robber)
