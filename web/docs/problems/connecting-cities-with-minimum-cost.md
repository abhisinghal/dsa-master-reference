# Union-Find — Connecting Cities With Minimum Cost

*[↗ LeetCode: Connecting Cities With Minimum Cost](https://leetcode.com/problems/connecting-cities-with-minimum-cost/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/union-find)

Given `n` cities and `connections=[city1, city2, cost]`, return min cost to connect all cities, or `-1` if impossible.

**Example** — `n=3, [[1,2,5],[1,3,6],[2,3,1]]` → `6` (edges [2,3,1] + [1,2,5])

---

## Approach 1 — Kruskal's MST
Same skeleton as Min Cost to Connect All Points, but edges are given rather than computed.



```java
int minimumCost(int n, int[][] connections) {
    Arrays.sort(connections, (a, b) -> a[2] - b[2]);
    int[] parent = new int[n + 1];
    for (int i = 0; i <= n; i++) parent[i] = i;
    int cost = 0, added = 0;
    for (int[] e : connections) {
        int a = find(parent, e[0]), b = find(parent, e[1]);
        if (a != b) { parent[a] = b; cost += e[2]; added++; }
    }
    return added == n - 1 ? cost : -1;
}
int find(int[] p, int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; }
```




<CodeTrace
  title="Kruskal's MST"
  :values="['1', '2', '5']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize; scan begins." },
    { pointers: { i: 0 }, vars: { phase: "midway" }, note: "Midway through the scan." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "All positions considered — return the answer." }
  ]'
/>


**Complexity** — Time **O(E log E)**; Space **O(n)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Kruskal's MST | O(E log E) | O(n) | primary |

## When to use which

- **Ship this** → Kruskal's MST (O(E log E), O(n)). The pattern's standard solution.

## Related problems

- [Min Cost to Connect All Points](/problems/min-cost-to-connect-all-points) — coordinates → distances
- [Optimize Water Distribution](/problems/optimize-water-distribution-in-a-village) — MST with virtual source
- [Find Critical and Pseudo-Critical Edges](/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree)
