# Union-Find — Find Critical and Pseudo-Critical Edges in MST

*[↗ LeetCode: Find Critical and Pseudo-Critical Edges in MST](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/union-find)

Given `n` and weighted edges, classify each edge:
- **Critical** — appears in EVERY MST.
- **Pseudo-critical** — appears in SOME but not all MSTs.

**Example** — return `[criticals, pseudo]`.

---

## Approach — Try each edge with Kruskal

**Insight.** Compute the standard MST cost. For each edge `e`:
1. **Force-exclude** `e`, run Kruskal. If MST cost differs → `e` is *critical*.
2. If not critical, **force-include** `e`, run Kruskal. If cost matches standard MST cost → *pseudo-critical*.

```java
List<List<Integer>> findCriticalAndPseudoCriticalEdges(int n, int[][] edges) {
    int m = edges.length;
    int[][] indexed = new int[m][4];
    for (int i = 0; i < m; i++) indexed[i] = new int[]{edges[i][0], edges[i][1], edges[i][2], i};
    Arrays.sort(indexed, (a, b) -> a[2] - b[2]);
    int mstCost = kruskal(n, indexed, -1, -1);
    List<Integer> critical = new ArrayList<>();
    List<Integer> pseudo = new ArrayList<>();
    for (int i = 0; i < m; i++) {
        if (kruskal(n, indexed, i, -1) > mstCost)      critical.add(indexed[i][3]);
        else if (kruskal(n, indexed, -1, i) == mstCost) pseudo.add(indexed[i][3]);
    }
    return List.of(critical, pseudo);
}
// kruskal builds MST; excludeIdx = skip this edge; includeIdx = start by taking this edge
int kruskal(int n, int[][] edges, int excludeIdx, int includeIdx) {
    int[] parent = new int[n]; for (int i = 0; i < n; i++) parent[i] = i;
    int cost = 0, added = 0;
    if (includeIdx != -1) {
        int[] e = edges[includeIdx];
        parent[find(parent, e[0])] = find(parent, e[1]);
        cost += e[2]; added++;
    }
    for (int i = 0; i < edges.length; i++) {
        if (i == excludeIdx || i == includeIdx) continue;
        int a = find(parent, edges[i][0]), b = find(parent, edges[i][1]);
        if (a != b) { parent[a] = b; cost += edges[i][2]; added++; }
    }
    return added == n - 1 ? cost : Integer.MAX_VALUE;
}
int find(int[] p, int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; }
```

**Complexity** — Time **O(E² α(V))**; Space **O(V)**.

## Related problems

- [Min Cost to Connect All Points](/problems/min-cost-to-connect-all-points) — plain MST
- [Kruskal's canonical](/problems/union-find-number-of-provinces) — Union-Find basics
