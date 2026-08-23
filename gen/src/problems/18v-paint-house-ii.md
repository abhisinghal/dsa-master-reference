# DP — Paint House II

*[↗ LeetCode: Paint House II](https://leetcode.com/problems/paint-house-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

`n` houses, `k` colors. cost to paint. No two adjacent same color. Min total.

**Constraints** — `1 ≤ n·k ≤ 5000`.

**Example 1** — `costs=[[1,5,3],[2,9,4]]` → `5`
**Example 2** — `costs=[[1,3],[2,4]]` → `5`

---

## Approach 1 — O(n · k²) DP
`dp[i][j] = cost[i][j] + min(dp[i-1][j'])` over `j' ≠ j`.

## Approach 2 — Track min & second-min per row → O(n · k) (canonical)

**Insight.** Only need two smallest values from previous row + which index was min.

```java
int minCostII(int[][] costs) {
    int n = costs.length, k = costs[0].length;
    int min1 = 0, min2 = 0, idx1 = -1;
    for (int i = 0; i < n; i++) {
        int nMin1 = Integer.MAX_VALUE, nMin2 = Integer.MAX_VALUE, nIdx1 = -1;
        for (int j = 0; j < k; j++) {
            int c = costs[i][j] + (j == idx1 ? min2 : min1);
            if (c < nMin1) { nMin2 = nMin1; nMin1 = c; nIdx1 = j; }
            else if (c < nMin2) nMin2 = c;
        }
        min1 = nMin1; min2 = nMin2; idx1 = nIdx1;
    }
    return min1;
}
```

**Complexity** — Time **O(n · k)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| O(n·k²) DP | O(n·k²) | O(k) | baseline |
| Min+second min | **O(n·k)** | O(1) | canonical |

## When to use which

- **Standard** → min + second-min trick.
- **Only 3 colors** → O(n) with 3-way check.
- **Return coloring** → track color chosen.

## Related problems

- [Paint House](https://leetcode.com/problems/paint-house/)
- [Paint Fence](https://leetcode.com/problems/paint-fence/)