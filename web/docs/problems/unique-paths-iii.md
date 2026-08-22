# Backtracking — Unique Paths III

*[↗ LeetCode: Unique Paths III](https://leetcode.com/problems/unique-paths-iii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/backtracking)

Grid: 1=start, 2=end, 0=empty, -1=obstacle. Count paths from 1 → 2 visiting **every** empty cell exactly once.

---

## Approach 1 — Hamiltonian-path DFS with backtracking
**Insight.** Track remaining empty cells to visit; at end cell, count if remaining == 0. Mark visited by mutating in place (restore on return).



```java
int uniquePathsIII(int[][] grid) {
    int m = grid.length, n = grid[0].length, sr = 0, sc = 0, remaining = 1;
    for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) {
        if (grid[i][j] == 1) { sr = i; sc = j; }
        else if (grid[i][j] == 0) remaining++;
    }
    return dfs(grid, sr, sc, remaining);
}
int dfs(int[][] g, int r, int c, int remaining) {
    if (r < 0 || c < 0 || r >= g.length || c >= g[0].length || g[r][c] == -1) return 0;
    if (g[r][c] == 2) return remaining == 0 ? 1 : 0;
    int tmp = g[r][c];
    g[r][c] = -1;
    int total = dfs(g, r+1, c, remaining - 1) + dfs(g, r-1, c, remaining - 1)
              + dfs(g, r, c+1, remaining - 1) + dfs(g, r, c-1, remaining - 1);
    g[r][c] = tmp;
    return total;
}
```



**Complexity** — Time exponential (~4^cells); grid ≤ 20 cells makes it feasible.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Hamiltonian-path DFS with backtracking | — | — | primary |

## When to use which

- **Ship this** → Hamiltonian-path DFS with backtracking (—, —). The pattern's standard solution.

## Related problems

- [Robot Room Cleaner](/problems/robot-room-cleaner) — DFS with in-place marking
- [Shortest Path Visiting All Nodes](/problems/shortest-path-visiting-all-nodes) — bitmask BFS
