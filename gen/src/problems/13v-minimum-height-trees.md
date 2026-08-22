# Topological Sort — Minimum Height Trees

*[↗ LeetCode: Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/topological-sort)

Given an undirected tree with `n` nodes, return all roots that give minimum tree height (at most 2 such roots).

**Example** — `n=6, edges=[[3,0],[3,1],[3,2],[3,4],[5,4]]` → `[3,4]`

---

## Approach 1 — Try every node as root, BFS

**Complexity** — O(V·(V+E)). O(V²) on a tree. TLE at V=10⁴.

## Approach 2 — Peel leaves iteratively (BFS from the outside)

**Insight.** The **center** of a tree is the last node(s) surviving when you repeatedly remove leaves. For trees on ≥ 3 nodes, always 1 or 2 centers.

**Trap.** Special-case `n ≤ 2`: all nodes are roots.

```java
List<Integer> findMinHeightTrees(int n, int[][] edges) {
    if (n <= 2) { List<Integer> a = new ArrayList<>(); for (int i = 0; i < n; i++) a.add(i); return a; }
    List<Set<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new HashSet<>());
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
    List<Integer> leaves = new ArrayList<>();
    for (int i = 0; i < n; i++) if (adj.get(i).size() == 1) leaves.add(i);
    int remaining = n;
    while (remaining > 2) {
        remaining -= leaves.size();
        List<Integer> next = new ArrayList<>();
        for (int leaf : leaves) {
            int neighbor = adj.get(leaf).iterator().next();
            adj.get(neighbor).remove(leaf);
            if (adj.get(neighbor).size() == 1) next.add(neighbor);
        }
        leaves = next;
    }
    return leaves;
}
```

<CodeTrace
  title="Peel leaves — n=6, tree of 6 nodes"
  :values="[0,1,2,3,4,5]"
  :windowKeys="['round']"
  :cellWidth="42"
  :steps='[
    { pointers: { round: 0 }, vars: { leaves: "[0,1,2,5]", remaining: 6 }, note: "initial leaves (deg 1)" },
    { pointers: { round: 1 }, vars: { leaves: "[3,4]", remaining: 2 }, note: "peel 0,1,2,5. 3 and 4 now leaves", added: [3,4] },
    { pointers: { round: 2 }, vars: { done: true }, note: "remaining ≤ 2 → done. answer [3,4]" }
  ]'
/>

**Complexity** — Time **O(V + E)**; Space **O(V + E)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Try every root | O(V·(V+E)) | O(V+E) |
| Peel leaves | **O(V + E)** | O(V + E) |

## Related problems

- [Course Schedule II](/problems/topological-sort-course-schedule) — Kahn's on directed DAG
- [Redundant Connection](/problems/redundant-connection) — cycle finding
- [Tree Diameter](https://leetcode.com/problems/tree-diameter/) — 2 BFS or DP-on-tree
