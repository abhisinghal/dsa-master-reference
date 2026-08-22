# Two Pointers — Trapping Rain Water II

*[↗ LeetCode: Trapping Rain Water II](https://leetcode.com/problems/trapping-rain-water-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/two-pointers)

2D grid of heights; compute total water trapped.

> Filed under Two Pointers because 1D Trapping Rain Water lives here, but the 2D version needs a **min-heap on the boundary**, not opposing pointers.

---

## Approach 1 — Min-heap Dijkstra-style border expansion
**Insight.** Water is bounded by the shortest wall along any path to the boundary. Grow a "reached" frontier from all border cells; always process the **lowest wall reachable** first. When we enter a lower neighbor, water trapped = current wall - neighbor height, and that neighbor becomes a wall at the higher level.

```java
int trapRainWater(int[][] h) {
    int m = h.length, n = h[0].length;
    if (m < 3 || n < 3) return 0;
    boolean[][] seen = new boolean[m][n];
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[2] - b[2]);
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (i == 0 || j == 0 || i == m - 1 || j == n - 1) {
                pq.offer(new int[]{i, j, h[i][j]});
                seen[i][j] = true;
            }
    int[][] D = {{1,0},{-1,0},{0,1},{0,-1}};
    int water = 0;
    while (!pq.isEmpty()) {
        int[] c = pq.poll();
        for (int[] d : D) {
            int ni = c[0] + d[0], nj = c[1] + d[1];
            if (ni < 0 || nj < 0 || ni >= m || nj >= n || seen[ni][nj]) continue;
            seen[ni][nj] = true;
            water += Math.max(0, c[2] - h[ni][nj]);
            pq.offer(new int[]{ni, nj, Math.max(c[2], h[ni][nj])});
        }
    }
    return water;
}
```

**Complexity** — Time **O(mn log(mn))**; Space **O(mn)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Min-heap Dijkstra-style border expansion | O(mn log(mn)) | O(mn) | primary |

## When to use which

- **Ship this** → Min-heap Dijkstra-style border expansion (O(mn log(mn)), O(mn)). The pattern's standard solution.

## Related problems

- [Trapping Rain Water](/problems/trapping-rain-water) — 1D
- [Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/) — same "process lowest first" trick
- [Path With Minimum Effort](/problems/path-with-minimum-effort)
