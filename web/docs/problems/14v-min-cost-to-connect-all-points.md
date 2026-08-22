# Union-Find — Min Cost to Connect All Points

*[↗ LeetCode: Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/union-find)

Given `points[][2]`, connect all with the minimum total Manhattan distance. Return the min total cost. (Classic **MST**.)

**Example** — `points=[[0,0],[2,2],[3,10],[5,2],[7,0]]` → `20`

---

## Approach — Kruskal's algorithm (edges + Union-Find)

**Insight.** Build all `C(n,2)` weighted edges; sort by weight; add cheapest-first that don't create a cycle (checked via Union-Find). Stop when `n-1` edges added.



```java
int minCostConnectPoints(int[][] p) {
    int n = p.length;
    List<int[]> edges = new ArrayList<>();
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) {
            int w = Math.abs(p[i][0] - p[j][0]) + Math.abs(p[i][1] - p[j][1]);
            edges.add(new int[]{w, i, j});
        }
    edges.sort((a, b) -> a[0] - b[0]);
    int[] parent = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;
    int cost = 0, added = 0;
    for (int[] e : edges) {
        if (added == n - 1) break;
        int a = find(parent, e[1]), b = find(parent, e[2]);
        if (a != b) { parent[a] = b; cost += e[0]; added++; }
    }
    return cost;
}
int find(int[] p, int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; }
```



**Complexity** — Time **O(n² log n)** (edge sort dominates); Space **O(n²)**.

## Alternative — Prim's algorithm

Priority queue of edges from the growing tree; O(n² log n) too.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Kruskal + Union-Find | **O(n² log n)** | O(n²) |
| Prim + PQ | O(n² log n) | O(n²) |

## Related problems

- [Number of Provinces](/problems/union-find-number-of-provinces)
- [Connecting Cities with Minimum Cost](/problems/connecting-cities-with-minimum-cost)
- [Optimize Water Distribution](/problems/optimize-water-distribution-in-a-village) — MST with virtual source
