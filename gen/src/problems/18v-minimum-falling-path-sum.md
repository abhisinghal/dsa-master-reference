# DP — Minimum Falling Path Sum

*[↗ LeetCode: Minimum Falling Path Sum](https://leetcode.com/problems/minimum-falling-path-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Grid; falling path picks one cell per row; next row's cell must be in `[j-1, j, j+1]`. Min sum from top to bottom.

**Example 1** — `[[2,1,3],[6,5,4],[7,8,9]]` → `13`

**Constraints** — `1 ≤ n ≤ 100`.

---

## Approach — Row-by-row DP (canonical)

**Insight.** `dp[i][j] = grid[i][j] + min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1])`.

```java
int minFallingPathSum(int[][] grid) {
    int n = grid.length;
    int[] prev = grid[0].clone();
    for (int i = 1; i < n; i++) {
        int[] cur = new int[n];
        for (int j = 0; j < n; j++) {
            int m = prev[j];
            if (j > 0) m = Math.min(m, prev[j-1]);
            if (j < n-1) m = Math.min(m, prev[j+1]);
            cur[j] = grid[i][j] + m;
        }
        prev = cur;
    }
    int best = Integer.MAX_VALUE;
    for (int v : prev) best = Math.min(best, v);
    return best;
}
```

<CodeTrace
  title="Row-by-row DP (canonical)"
  :values="['2', '1', '3']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n²)**; Space **O(n)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Row-by-row DP | **O(n²)** | O(n) | canonical |

## When to use which

- **Row-only transitions** → 1D rolling.
- **Diagonal-only transitions** → [Triangle](https://leetcode.com/problems/triangle/).

## Related problems

- [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/)
- [Triangle](https://leetcode.com/problems/triangle/)
- [Dungeon Game](/problems/dungeon-game)
