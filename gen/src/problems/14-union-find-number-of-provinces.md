# Union-Find — Number of Provinces

*[↗ LeetCode: Number of Provinces](https://leetcode.com/problems/number-of-provinces/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/union-find)

<CompanyTags companies="Amazon, Google, Meta, LinkedIn" />

Given `isConnected[n][n]` (adjacency matrix; `1` if direct road), return the number of connected components.

**Example 1** — `[[1,1,0],[1,1,0],[0,0,1]]` → `2`
**Example 2** — `[[1,0,0],[0,1,0],[0,0,1]]` → `3`

**Constraints** — `1 ≤ n ≤ 200`.


<Hints
  hint1="Are you grouping things by shared property? Adjacent lands, same friend circle, connected components?"
  hint2="Union-Find: `find(x)` returns root; `union(a, b)` merges. Path compression + union by rank gives α(n)."
  hint3="For MST (min-cost connect all): Kruskal sorts edges, unions if disjoint, stops at n−1 edges."
/>
---

## Approach 1 — DFS from each unvisited city

**Intuition.** For each unvisited node, DFS the whole component; each fresh start = new province.

```java
int findCircleNumDFS(int[][] g) {
    int n = g.length, count = 0;
    boolean[] seen = new boolean[n];
    for (int i = 0; i < n; i++) if (!seen[i]) { dfs(i, g, seen); count++; }
    return count;
}
void dfs(int u, int[][] g, boolean[] seen) {
    seen[u] = true;
    for (int v = 0; v < g.length; v++) if (g[u][v] == 1 && !seen[v]) dfs(v, g, seen);
}
```

**Complexity** — Time **O(n²)**; Space **O(n)** recursion.

---

## Approach 2 — BFS from each unvisited city

**Intuition.** Same as DFS but iterative (avoids stack overflow on dense graphs).

**Complexity** — Time **O(n²)**; Space **O(n)** queue. Same asymptotic; different stack risk.

---

## Approach 3 — Union-Find (Disjoint Set Union) with union-by-size + path compression

**Insight from DFS/BFS.** DFS/BFS re-traverses each component. Union-Find pre-computes the parent forest as we scan edges once; the final component count = distinct roots.

**Trap.** Without union-by-size (or rank), naive union chains linearly → O(n) per find. With union-by-size + path compression, each op is O(α(n)) ≈ O(1).

```java
int findCircleNum(int[][] g) {
    int n = g.length;
    int[] parent = new int[n], size = new int[n];
    for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
    int count = n;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (g[i][j] == 1 && union(parent, size, i, j)) count--;
    return count;
}
int find(int[] parent, int x) {
    while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
    return x;
}
boolean union(int[] parent, int[] size, int a, int b) {
    int ra = find(parent, a), rb = find(parent, b);
    if (ra == rb) return false;
    if (size[ra] < size[rb]) { int t = ra; ra = rb; rb = t; }
    parent[rb] = ra; size[ra] += size[rb];
    return true;
}
```

<CodeTrace
  title="Union-Find — [[1,1,0],[1,1,0],[0,0,1]]"
  :values="[0,1,2]"
  :windowKeys="['edge']"
  :cellWidth="46"
  :steps='[
    { pointers: { edge: 0 }, vars: { parent: "[0,1,2]", count: 3 }, note: "each city its own root" },
    { pointers: { edge: 1 }, vars: { parent: "[0,0,2]", count: 2 }, note: "union(0,1) — merge → count 2", added: [0,1] },
    { pointers: { edge: 2 }, vars: { parent: "[0,0,2]", count: 2 }, note: "no edges from 2. answer = 2" }
  ]'
/>

**Complexity** — Time **O(n² α(n)) ≈ O(n²)**; Space **O(n)**. Same big-O as DFS but *incremental* — supports streaming edges.

---

## Try it yourself

<JavaRunner problem-slug="union-find-number-of-provinces" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| DFS from each city | O(n²) | O(n) |
| BFS from each city | O(n²) | O(n) |
| Union-Find | **O(n² α(n))** | O(n) |

## When to use which

- **Static graph, one query** → DFS/BFS are fine.
- **Dynamic edges (streaming)** → Union-Find (only structure that supports incremental unions).
- **Also need "are these two nodes connected?"** → Union-Find with path compression gives O(1) queries.

## Related problems (same ladder applies)

- [Accounts Merge](https://leetcode.com/problems/accounts-merge/) — union emails belonging to the same person
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/) — find the edge whose two endpoints are already connected
- [Number of Islands II](https://leetcode.com/problems/number-of-islands-ii/) — streaming version of Number of Islands
- [Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) — Kruskal's MST via Union-Find