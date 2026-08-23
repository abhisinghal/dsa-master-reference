# Union-Find — Redundant Connection

*[↗ LeetCode: Redundant Connection](https://leetcode.com/problems/redundant-connection/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/union-find)

Given an undirected graph that starts as a tree with `n` nodes and has **one** extra edge added, return that redundant edge.

**Example 1** — `edges=[[1,2],[1,3],[2,3]]` → `[2,3]`
**Example 2** — `edges=[[1,2],[2,3],[3,4],[1,4],[1,5]]` → `[1,4]`

**Constraints** — `3 ≤ n ≤ 1000`; `edges.length == n`.

---

## Approach 1 — DFS to detect cycle for each edge

Try removing each edge; DFS to check connectivity. O(n²).

## Approach 2 — Union-Find (canonical)

**Insight.** Process edges in order. First edge whose endpoints already share a root would create a cycle — that's the redundant one.



```java
int[] findRedundantConnection(int[][] edges) {
    int n = edges.length;
    int[] parent = new int[n + 1];
    for (int i = 0; i <= n; i++) parent[i] = i;
    for (int[] e : edges) {
        int ra = find(parent, e[0]), rb = find(parent, e[1]);
        if (ra == rb) return e;
        parent[ra] = rb;
    }
    return new int[0];
}
int find(int[] p, int x) { return p[x] == x ? x : (p[x] = find(p, p[x])); }
```



<CodeTrace
  title="UF — edges=[[1,2],[1,3],[2,3]]"
  :values="['1','2','3']"
  :windowKeys="['e']"
  :cellWidth="34"
  :steps='[
    { pointers: { e: 0 }, vars: { union: "1-2" }, note: "" },
    { pointers: { e: 1 }, vars: { union: "1-3" }, note: "" },
    { pointers: { e: 2 }, vars: { conflict: "2-3 already connected" }, note: "return [2,3]" }
  ]'
/>

**Complexity** — Time **O(n · α(n))**; Space **O(n)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DFS check per edge | O(n²) | O(n) | baseline |
| Union-Find | **O(n · α(n))** | O(n) | canonical |

## When to use which

- **Undirected cycle detection with edges processed in order** → Union-Find.
- **Directed variant (LC 685)** → more complex — need to handle 2-parent + cycle cases.
- **"Return all redundant edges"** → skip returning early; collect all matches.

## Related problems

- [Number of Provinces](/problems/union-find-number-of-provinces)
- [Redundant Connection II](https://leetcode.com/problems/redundant-connection-ii/) — directed
- [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/)
