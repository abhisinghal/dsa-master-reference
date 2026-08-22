# DP — Paint House II

*[↗ LeetCode: Paint House II](https://leetcode.com/problems/paint-house-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

`n` houses, `k` colors. Cost to paint house i color j. Adjacent houses must differ in color. Min total.

---

## Approach 1 — DP O(n · k²)
`dp[i][j] = cost[i][j] + min(dp[i-1][j'])` over j' ≠ j.

---

## Approach 2 — Track min & second-min per row → O(n · k)
**Insight.** From the previous row, the only info needed is the two smallest DP values (and which color the min belongs to). This lets each new cell pick its best predecessor in O(1).

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

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| DP O(n · k²) | — | — | baseline |
| Track min & second-min per row → O(n · k) | O(n · k) | O(1) | optimum |

## When to use which

- **State it for signal** → DP O(n · k²) (—). Correct baseline; call it out then move on.
- **Ship this** → Track min & second-min per row → O(n · k) (O(n · k), O(1)). Expected optimum in interview.

## Related problems

- [Paint House](https://leetcode.com/problems/paint-house/) — k = 3
- [Paint Fence](https://leetcode.com/problems/paint-fence/) — different adjacency rule
