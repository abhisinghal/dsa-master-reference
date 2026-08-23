# DP — Min Cost Climbing Stairs

*[↗ LeetCode: Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/dp)

Each step has cost. Start at 0 or 1; step 1 or 2. Min cost to reach past-the-end.

**Example 1** — `cost=[10,15,20]` → `15`
**Example 2** — `cost=[1,100,1,1,1,100,1,1,100,1]` → `6`

**Constraints** — `2 ≤ n ≤ 1000`.

---

## Approach — DP O(1) space (canonical)

**Insight.** `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`.

```java
int minCostClimbingStairs(int[] cost) {
    int a = 0, b = 0;
    for (int i = 2; i <= cost.length; i++) {
        int c = Math.min(b + cost[i-1], a + cost[i-2]);
        a = b; b = c;
    }
    return b;
}
```

<CodeTrace
  title="DP O(1) space (canonical)"
  :values="['10', '15', '20']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Rolling DP | **O(n)** | O(1) | canonical |

## When to use which

- **Standard** → rolling DP.
- **Return steps taken** → track predecessors.
- **k-step variants** → same skeleton with min over last k.

## Related problems

- [Climbing Stairs](/problems/climbing-stairs)
- [House Robber](/problems/dp-house-robber)
