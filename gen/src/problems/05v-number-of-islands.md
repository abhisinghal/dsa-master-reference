# Hashing — Number of Islands

*[↗ LeetCode: Number of Islands](https://leetcode.com/problems/number-of-islands/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dfs)

Count connected components of `'1'`s in a grid.

---

## Approach 1 — DFS flood fill
Iterate cells; on unseen `'1'` increment count, DFS/BFS marking `'0'` (or a visited set).

```java
int numIslands(char[][] grid) {
    int m = grid.length, n = grid[0].length, count = 0;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (grid[i][j] == '1') { count++; dfs(grid, i, j); }
    return count;
}
void dfs(char[][] g, int i, int j) {
    if (i < 0 || j < 0 || i >= g.length || j >= g[0].length || g[i][j] != '1') return;
    g[i][j] = '0';
    dfs(g, i + 1, j); dfs(g, i - 1, j); dfs(g, i, j + 1); dfs(g, i, j - 1);
}
```

---

## Approach 2 — BFS
Same idea, queue instead of recursion — avoids stack overflow on huge grids.

---

## Approach 3 — Union-Find
Union adjacent `'1'` cells; final answer = number of components with `'1'`. Useful for streaming variant (Islands II).

**Complexity (all)** — Time **O(mn)**; Space **O(mn)** stack/queue/uf.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| DFS flood fill | — | — | baseline |
| BFS | — | — | improved |
| Union-Find | O(mn) | O(mn) | optimum |

## When to use which

- **State it for signal** → DFS flood fill (—). Correct baseline; call it out then move on.
- **Intermediate refinement** → BFS (—).
- **Ship this** → Union-Find (O(mn), O(mn)). Expected optimum in interview.

## Related problems

- [Number of Islands II](/problems/number-of-islands-ii) — streaming, requires UF
- [Max Area of Island](https://leetcode.com/problems/max-area-of-island/)
- [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/)
