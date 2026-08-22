# Union-Find — Redundant Connection

*[↗ LeetCode: Redundant Connection](https://leetcode.com/problems/redundant-connection/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/union-find)

Given `n` edges forming a graph with exactly one extra edge causing a cycle, return that edge (last one appearing in input if multiple candidates).

**Example** — `[[1,2],[1,3],[2,3]]` → `[2,3]`

---

## Approach — Union-Find, detect cycle on-the-fly

**Insight.** Union each edge's endpoints. The first edge whose two endpoints are already in the same set IS the redundant one.



```java
int[] findRedundantConnection(int[][] edges) {
    int n = edges.length;
    int[] parent = new int[n + 1];
    for (int i = 0; i <= n; i++) parent[i] = i;
    for (int[] e : edges) {
        int a = find(parent, e[0]), b = find(parent, e[1]);
        if (a == b) return e;
        parent[a] = b;
    }
    return new int[0];
}
int find(int[] parent, int x) { while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; } return x; }
```



<CodeTrace
  title="DSU cycle detection — [[1,2],[1,3],[2,3]]"
  :values="['[1,2]','[1,3]','[2,3]']"
  :windowKeys="['i']"
  :cellWidth="52"
  :steps='[
    { pointers: { i: 0 }, vars: { parent: "[0,1,2,3]" }, note: "union(1,2)", added: [0] },
    { pointers: { i: 1 }, vars: { parent: "[0,2,3,3]" }, note: "union(1,3) — path compression" },
    { pointers: { i: 2 }, vars: { "find(2)": 3, "find(3)": 3 }, note: "both roots = 3 → cycle! return [2,3]", added: [2] }
  ]'
/>

**Complexity** — Time **O(n α(n))**; Space **O(n)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Union-Find | **O(n α(n))** | O(n) |

## Related problems

- [Redundant Connection II](https://leetcode.com/problems/redundant-connection-ii/) — directed variant
- [Number of Connected Components](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/)
- [Number of Provinces](/problems/union-find-number-of-provinces)
