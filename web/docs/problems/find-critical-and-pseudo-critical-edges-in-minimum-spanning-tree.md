# Union-Find — Find Critical and Pseudo-Critical Edges in MST

*[↗ LeetCode: Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/union-find)

<CompanyTags companies="Google, Amazon" />

Given a graph, classify each edge:
- **Critical** — removing it makes MST cost strictly larger (or disconnects).
- **Pseudo-critical** — appears in at least one MST but is not critical.

**Example 1** — `n=5, edges=[[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]` → `[[0,1],[2,3,4,5]]` (edges 0,1 critical; 2-5 pseudo)
**Example 2** — `n=4, edges=[[0,1,1],[1,2,1],[2,3,1],[0,3,1]]` → `[[],[0,1,2,3]]` (all four are pseudo — 4-cycle with equal weights)
**Example 3** — `n=2, edges=[[0,1,5]]` → `[[0],[]]` (only one edge, must be critical)

**Constraints** — `2 ≤ n ≤ 100`; `1 ≤ E ≤ min(200, C(n,2))`. Naive Steiner-tree brute force is `2^E ≈ 10⁶⁰` — impossible. Per-edge MST runs is O(E² · α) ≈ 200² · 4 = 1.6·10⁵.


<Hints
  hint1="Are you grouping things by shared property? Adjacent lands, same friend circle, connected components?"
  hint2="Union-Find: `find(x)` returns root; `union(a, b)` merges. Path compression + union by rank gives α(n)."
  hint3="For MST (min-cost connect all): Kruskal sorts edges, unions if disjoint, stops at n−1 edges."
/>
---

<MarkSolved problem-slug="find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree" /> <Bookmark problem-slug="find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree" />

<InterviewTimer problem-slug="find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree" />



## Approach 1 — Enumerate all spanning trees

**Intuition.** For each subset of `n-1` edges, check if it forms a spanning tree (connected + acyclic). Track the MST cost + which edges appear in some MST. Then classify each edge.

**Complexity** — `C(E, n-1)` subsets. For `E=200, n=100`, `C(200, 99) ≈ 10⁵⁷` — universe-age. Only mentioned as the mental reference before flipping to the smart approach.

---

## Approach 2 — Kruskal with per-edge skip/force experiments (canonical)

**Insight.** Compute the MST cost baseline. Then for each edge `e`, run Kruskal *twice*:
- **Skip `e`.** If MST cost is larger than baseline (or spanning fails) → `e` was essential → **critical**.
- **Force `e` first.** Start MST with `e` already included. If MST cost equals baseline → `e` participates in some MST → **pseudo-critical**.

An edge is either critical (removing it hurts), pseudo-critical (some MST uses it), or unused (some MST cheaper without it).



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



**Complexity** — Time **O(E² · α(n))**; Space **O(n + E)**. For `E=200`: 2·E MST runs = 400 Kruskals ≈ 40,000 union-finds. *Say aloud in an interview:* "the skip-force pattern generalises — same technique classifies critical edges in flow networks, and separators in graph decomposition."

---

## Try it yourself

<JavaRunner problem-slug="find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Spanning-tree enumeration | O(C(E, n-1)) | O(n) | Universe-age; reference only |
| **Per-edge skip/force MST** | **O(E² · α)** | O(n + E) | **Canonical** |

## When to use which

- **Small E (≤ 200)** → per-edge experiments.
- **Large E** → Tarjan bridge algorithm on MST after computing baseline.
- **"Count MSTs"** → matrix-tree theorem (Kirchhoff).

<AiCompanion problem-slug="find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree" pattern-hint="union-find" />

## Related problems

- [Connecting Cities With Minimum Cost](/problems/connecting-cities-with-minimum-cost)
- [Min Cost to Connect All Points](/problems/min-cost-to-connect-all-points)
- [Optimize Water Distribution](/problems/optimize-water-distribution-in-a-village)

<FeedbackWidget problem-slug="find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree" />
