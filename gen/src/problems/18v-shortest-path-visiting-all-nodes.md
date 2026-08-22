# DP — Shortest Path Visiting All Nodes

*[↗ LeetCode: Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

Undirected graph. Shortest length path visiting every node (may reuse).

**Constraints** — `1 ≤ n ≤ 12`.

---

## Approach — Bitmask BFS (canonical)

**Insight.** State = `(node, visitedMask)`. BFS from all `(i, 1 << i)` starts.

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
            int[] c = q.poll();
            if (c[1] == full) return steps;
            for (int nb : graph[c[0]]) {
                int nMask = c[1] | (1 << nb);
                if (!seen[nb][nMask]) { seen[nb][nMask] = true; q.offer(new int[]{nb, nMask}); }
            }
        }
        steps++;
    }
    return -1;
}
```

**Complexity** — Time **O(n · 2ⁿ · degree)**; Space **O(n · 2ⁿ)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Bitmask BFS | **O(n · 2ⁿ · deg)** | O(n · 2ⁿ) | canonical |

## When to use which

- **Small n + reachable revisits** → bitmask BFS.
- **Exact TSP** → same DP.
- **k people delivery** → k-source BFS extension.

## Related problems

- [Number of Ways to Wear Different Hats](/problems/number-of-ways-to-wear-different-hats-to-each-other)
- [Find the Shortest Superstring](/problems/find-the-shortest-superstring)
