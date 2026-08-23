# Union-Find — Min Cost to Connect All Points

*[↗ LeetCode: Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/union-find)

<CompanyTags companies="Amazon, Meta" />

Given 2D `points`, connect all with min total Manhattan distance.

**Example 1** — `points=[[0,0],[2,2],[3,10],[5,2],[7,0]]` → `20`
**Example 2** — `points=[[3,12],[-2,5],[-4,1]]` → `18`

**Constraints** — `1 ≤ n ≤ 1000`.


<Hints
  hint1="Are you grouping things by shared property? Adjacent lands, same friend circle, connected components?"
  hint2="Union-Find: `find(x)` returns root; `union(a, b)` merges. Path compression + union by rank gives α(n)."
  hint3="For MST (min-cost connect all): Kruskal sorts edges, unions if disjoint, stops at n−1 edges."
/>
---

## Approach 1 — Kruskal on all pairs

Build O(n²) edges; sort; UF. **O(n² log n)** time; works for n=1000.

```java
int minCostConnectPoints(int[][] points) {
    int n = points.length;
    List<int[]> edges = new ArrayList<>();
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            edges.add(new int[]{i, j, Math.abs(points[i][0]-points[j][0]) + Math.abs(points[i][1]-points[j][1])});
    edges.sort((a, b) -> a[2] - b[2]);
    int[] parent = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;
    int cost = 0, cnt = 0;
    for (int[] e : edges) {
        int ra = find(parent, e[0]), rb = find(parent, e[1]);
        if (ra == rb) continue;
        parent[ra] = rb; cost += e[2];
        if (++cnt == n - 1) break;
    }
    return cost;
}
int find(int[] p, int x) { return p[x] == x ? x : (p[x] = find(p, p[x])); }
```

<CodeTrace
  title="Kruskal on all pairs"
  :values="['0', '0']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

## Approach 2 — Prim with priority queue (canonical for dense)

**Insight.** Start at any node; repeatedly add closest unvisited. O(n²) unvisited scans without heap, or O(E log V) with heap.

**Complexity** — Time **O(n² log n)** heap-based; **O(n²)** without heap; Space **O(n²)** for edges.

---

## Try it yourself

<JavaRunner problem-slug="min-cost-to-connect-all-points" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Kruskal all pairs | O(n² log n) | O(n²) | works |
| Prim + heap | **O(n² log n)** | O(n²) | canonical |
| Prim without heap | O(n²) | O(n) | best for dense |

## When to use which

- **Complete graph (dense)** → Prim without heap.
- **Sparse edges** → Kruskal.
- **"Second best MST"** → replace each edge with next-cheapest non-MST option.

<AiCompanion problem-slug="min-cost-to-connect-all-points" pattern-hint="union-find" />

## Related problems

- [Connecting Cities With Minimum Cost](/problems/connecting-cities-with-minimum-cost)
- [Optimize Water Distribution](/problems/optimize-water-distribution-in-a-village)
- [Find Critical/Pseudo-Critical MST Edges](/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree)