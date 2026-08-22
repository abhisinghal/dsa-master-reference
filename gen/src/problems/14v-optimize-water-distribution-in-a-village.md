# Union-Find — Optimize Water Distribution in a Village

*[↗ LeetCode: Optimize Water Distribution in a Village](https://leetcode.com/problems/optimize-water-distribution-in-a-village/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/union-find)

Each house `i` can have a well (cost `wells[i]`) or share a pipe (cost `pipes[j][2]`). Return min total cost to supply water to every house.

**Example** — `n=3, wells=[1,2,2], pipes=[[1,2,1],[2,3,1]]` → `3`

---

---

## Approach 1 — Virtual node 0 + Kruskal's MST
**Insight.** Model each well as an edge from a virtual node 0 to house i with weight `wells[i]`. Now it's a standard MST on n+1 nodes.

```java
int minCostToSupplyWater(int n, int[] wells, int[][] pipes) {
    List<int[]> edges = new ArrayList<>();
    for (int i = 0; i < n; i++) edges.add(new int[]{0, i + 1, wells[i]});
    for (int[] p : pipes) edges.add(p);
    edges.sort((a, b) -> a[2] - b[2]);
    int[] parent = new int[n + 1];
    for (int i = 0; i <= n; i++) parent[i] = i;
    int cost = 0, added = 0;
    for (int[] e : edges) {
        if (added == n) break;
        int a = find(parent, e[0]), b = find(parent, e[1]);
        if (a != b) { parent[a] = b; cost += e[2]; added++; }
    }
    return cost;
}
int find(int[] p, int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; }
```


<CodeTrace
  title="Virtual node 0 + Kruskal's MST"
  :values="['1', '2', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize; scan begins." },
    { pointers: { i: 0 }, vars: { phase: "midway" }, note: "Midway through the scan." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "All positions considered — return the answer." }
  ]'
/>


**Complexity** — Time **O((n + p) log (n + p))**; Space **O(n + p)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Virtual node 0 + Kruskal's MST | O((n + p) log (n + p)) | O(n + p) | primary |

## When to use which

- **Ship this** → Virtual node 0 + Kruskal's MST (O((n + p) log (n + p)), O(n + p)). The pattern's standard solution.

## Related problems

- [Connecting Cities with Minimum Cost](/problems/connecting-cities-with-minimum-cost) — plain MST
- [Min Cost to Connect All Points](/problems/min-cost-to-connect-all-points)
