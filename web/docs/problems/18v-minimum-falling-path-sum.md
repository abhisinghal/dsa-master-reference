# DP — Minimum Falling Path Sum

*[↗ LeetCode: Minimum Falling Path Sum](https://leetcode.com/problems/minimum-falling-path-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Grid; falling path picks one cell per row; next row's cell must be in `[j-1, j, j+1]`. Min sum from top row to bottom.

## Approach — Bottom-up DP row by row

**Insight.** `dp[i][j] = grid[i][j] + min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1])` with boundary clamps.



```java
int minFallingPathSum(int[][] grid) {
    int n = grid.length;
    int[] prev = grid[0].clone();
    for (int i = 1; i < n; i++) {
        int[] cur = new int[n];
        for (int j = 0; j < n; j++) {
            int m = prev[j];
            if (j > 0) m = Math.min(m, prev[j - 1]);
            if (j < n - 1) m = Math.min(m, prev[j + 1]);
            cur[j] = grid[i][j] + m;
        }
        prev = cur;
    }
    int best = Integer.MAX_VALUE;
    for (int v : prev) best = Math.min(best, v);
    return best;
}
```



**Complexity** — Time **O(n²)**; Space **O(n)**.

## Related problems

- [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) — right/down only
- [Triangle](https://leetcode.com/problems/triangle/) — sibling
- [Dungeon Game](/problems/dungeon-game) — reversed DP direction
