# BS on Answer — Path With Minimum Effort

*[↗ LeetCode: Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/bs-on-answer)

In a 2D grid of heights, an "effort" of a path is the max abs-diff between consecutive cells. Return the min effort from top-left to bottom-right (4-connected).

**Example** — `heights=[[1,2,2],[3,8,2],[5,3,5]]` → `2`

---

## Approach 1 — Dijkstra with edge weight = max-so-far

O(mn log mn).

## Approach 2 — Binary search on the effort + BFS reachability

**Insight.** `feasible(e)` = can we walk from start to end using only edges with `|diff| ≤ e`? Monotonic. Binary search minimum `e`.

```java
int minimumEffortPath(int[][] h) {
    int m = h.length, n = h[0].length;
    int lo = 0, hi = 1_000_000;
    int[][] DIR = {{1,0},{-1,0},{0,1},{0,-1}};
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        boolean[][] seen = new boolean[m][n];
        Deque<int[]> q = new ArrayDeque<>();
        q.offer(new int[]{0, 0}); seen[0][0] = true;
        while (!q.isEmpty()) {
            int[] c = q.poll();
            if (c[0] == m - 1 && c[1] == n - 1) break;
            for (int[] d : DIR) {
                int r = c[0] + d[0], col = c[1] + d[1];
                if (r < 0 || r >= m || col < 0 || col >= n || seen[r][col]) continue;
                if (Math.abs(h[r][col] - h[c[0]][c[1]]) <= mid) { seen[r][col] = true; q.offer(new int[]{r, col}); }
            }
        }
        if (seen[m - 1][n - 1]) hi = mid;
        else                    lo = mid + 1;
    }
    return lo;
}
```

**Complexity** — Time **O(mn · log(max))**; Space **O(mn)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Dijkstra | O(mn log mn) | O(mn) |
| BS + BFS | **O(mn log(max))** | O(mn) |

## Related problems

- [Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/) — same idea, sea level = effort
- [Path With Maximum Minimum Value](https://leetcode.com/problems/path-with-maximum-minimum-value/) — dual (maximize min)
