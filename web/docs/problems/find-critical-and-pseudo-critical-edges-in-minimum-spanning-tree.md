# Union-Find — Find Critical and Pseudo-Critical Edges in MST

*[↗ LeetCode: Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/union-find)

&lt;CompanyTags companies="Google, Amazon" /&gt;

Given a graph, classify each edge:
- **Critical** — removing it makes MST cost strictly larger (or disconnects).
- **Pseudo-critical** — appears in at least one MST but is not critical.

**Example 1** — Return `[criticalEdges, pseudoCriticalEdges]`.

**Constraints** — `2 ≤ n ≤ 100`; `1 ≤ E ≤ min(200, C(n,2))`.


&lt;Hints
  hint1="Are you grouping things by shared property? Adjacent lands, same friend circle, connected components?"
  hint2="Union-Find: `find(x)` returns root; `union(a, b)` merges. Path compression + union by rank gives α(n)."
  hint3="For MST (min-cost connect all): Kruskal sorts edges, unions if disjoint, stops at n−1 edges."
/&gt;
---

&lt;MarkSolved problem-slug="find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree" /&gt;

&lt;InterviewTimer problem-slug="find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree" /&gt;



## Approach — Kruskal with per-edge experiments (canonical)

**Insight.** Compute MST cost baseline.
- **Critical:** Skip edge `e`; compute MST cost. If larger (or spanning fails) → critical.
- **Pseudo-critical:** Force `e` in first; compute MST. If cost equals baseline → pseudo-critical.



```java
List<List<Integer>> findCriticalAndPseudoCriticalEdges(int n, int[][] edges) {
    int E = edges.length;
    int[][] tagged = new int[E][4];
    for (int i = 0; i < E; i++) {
        tagged[i][0] = edges[i][0]; tagged[i][1] = edges[i][1];
        tagged[i][2] = edges[i][2]; tagged[i][3] = i;
    }
    Arrays.sort(tagged, (a, b) -> a[2] - b[2]);
    int baseline = kruskal(n, tagged, -1, -1);
    List<Integer> crit = new ArrayList<>(), pseudo = new ArrayList<>();
    for (int i = 0; i < E; i++) {
        if (kruskal(n, tagged, i, -1) > baseline) crit.add(tagged[i][3]);
        else if (kruskal(n, tagged, -1, i) == baseline) pseudo.add(tagged[i][3]);
    }
    return List.of(crit, pseudo);
}
int kruskal(int n, int[][] edges, int skip, int force) {
    int[] parent = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;
    int cost = 0, cnt = 0;
    if (force >= 0) { parent[find(parent, edges[force][0])] = find(parent, edges[force][1]); cost += edges[force][2]; cnt++; }
    for (int i = 0; i < edges.length; i++) {
        if (i == skip || i == force) continue;
        int ra = find(parent, edges[i][0]), rb = find(parent, edges[i][1]);
        if (ra == rb) continue;
        parent[ra] = rb;
        cost += edges[i][2];
        if (++cnt == n - 1) return cost;
    }
    return Integer.MAX_VALUE;
}
int find(int[] p, int x) { return p[x] == x ? x : (p[x] = find(p, p[x])); }
```



**Complexity** — Time **O(E² · α)**; Space **O(n + E)**.

---

## Try it yourself

<JavaRunner problem-slug="find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Per-edge skip/force MST | **O(E² · α)** | O(n + E) | canonical |

## When to use which

- **Small E (≤ 200)** → per-edge experiments.
- **Large E** → Tarjan bridge algorithm on MST after computing baseline.
- **"Count MSTs"** → matrix-tree theorem (Kirchhoff).

&lt;AiCompanion problem-slug="find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree" pattern-hint="union-find" /&gt;

## Related problems

- [Connecting Cities With Minimum Cost](/problems/connecting-cities-with-minimum-cost)
- [Min Cost to Connect All Points](/problems/min-cost-to-connect-all-points)
- [Optimize Water Distribution](/problems/optimize-water-distribution-in-a-village)

&lt;FeedbackWidget problem-slug="find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree" /&gt;
