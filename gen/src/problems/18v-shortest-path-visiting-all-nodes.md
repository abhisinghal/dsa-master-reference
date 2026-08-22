# DP — Shortest Path Visiting All Nodes

*[↗ LeetCode: Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

Undirected graph. Shortest length path visiting **every** node (may reuse edges/nodes; start anywhere).

## Approach — Bitmask BFS

**Insight.** State = `(node, visitedMask)`. BFS from all `(i, 1 << i)` initial states simultaneously. Terminate when `visitedMask == fullMask`.

```java
int shortestPathLength(int[][] graph) {
    int n = graph.length, full = (1 << n) - 1;
    Queue<int[]> q = new ArrayDeque<>();
    boolean[][] seen = new boolean[n][1 << n];
    for (int i = 0; i < n; i++) {
        q.offer(new int[]{i, 1 << i});
        seen[i][1 << i] = true;
    }
    int steps = 0;
    while (!q.isEmpty()) {
        for (int sz = q.size(); sz > 0; sz--) {
            int[] cur = q.poll();
            int node = cur[0], mask = cur[1];
            if (mask == full) return steps;
            for (int nb : graph[node]) {
                int nMask = mask | (1 << nb);
                if (!seen[nb][nMask]) { seen[nb][nMask] = true; q.offer(new int[]{nb, nMask}); }
            }
        }
        steps++;
    }
    return -1;
}
```

**Complexity** — Time **O(n · 2ⁿ · degree)**; Space **O(n · 2ⁿ)**.

## Related problems

- [Traveling Salesman] — bitmask DP for exact
- [Number of Ways to Wear Different Hats](/problems/number-of-ways-to-wear-different-hats)
- [Find the Shortest Superstring](/problems/find-the-shortest-superstring) — bitmask DP
