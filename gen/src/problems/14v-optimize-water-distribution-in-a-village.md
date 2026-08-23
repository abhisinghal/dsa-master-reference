# Union-Find — Optimize Water Distribution in a Village

*[↗ LeetCode: Optimize Water Distribution in a Village](https://leetcode.com/problems/optimize-water-distribution-in-a-village/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/union-find)

<CompanyTags companies="Amazon, Google" />

Given `n` houses, `wells[i]` = cost to dig a well at house `i`, and `pipes[i] = [a, b, cost]` = cost to build a pipe between houses. Provide water to all houses at min cost.

**Example 1** — `n=3, wells=[1,2,2], pipes=[[1,2,1],[2,3,1]]` → `3` (dig at 1: 1; pipes 1-2:1 and 2-3:1)

**Constraints** — `2 ≤ n ≤ 10⁴`.


<Hints
  hint1="Are you grouping things by shared property? Adjacent lands, same friend circle, connected components?"
  hint2="Union-Find: `find(x)` returns root; `union(a, b)` merges. Path compression + union by rank gives α(n)."
  hint3="For MST (min-cost connect all): Kruskal sorts edges, unions if disjoint, stops at n−1 edges."
/>
---

<MarkSolved problem-slug="optimize-water-distribution-in-a-village" />

<InterviewTimer problem-slug="optimize-water-distribution-in-a-village" />



## Approach — Add virtual node + MST (canonical)

**Insight.** Model wells as **virtual pipes from node 0** to each house. Now the problem is a standard MST over `n+1` nodes.

```java
int minCostToSupplyWater(int n, int[] wells, int[][] pipes) {
    List<int[]> edges = new ArrayList<>();
    for (int i = 0; i < n; i++) edges.add(new int[]{0, i + 1, wells[i]});
    for (int[] p : pipes) edges.add(p);
    edges.sort((a, b) -> a[2] - b[2]);
    int[] parent = new int[n + 1];
    for (int i = 0; i <= n; i++) parent[i] = i;
    int cost = 0, cnt = 0;
    for (int[] e : edges) {
        int ra = find(parent, e[0]), rb = find(parent, e[1]);
        if (ra == rb) continue;
        parent[ra] = rb; cost += e[2];
        if (++cnt == n) break;
    }
    return cost;
}
int find(int[] p, int x) { return p[x] == x ? x : (p[x] = find(p, p[x])); }
```

<CodeTrace
  title="Virtual root — n=3"
  :values="['0-1:1','0-2:2','0-3:2','1-2:1','2-3:1']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { pick: "0-1:1" }, note: "dig at 1" },
    { pointers: { i: 3 }, vars: { pick: "1-2:1", cost: 2 }, note: "" },
    { pointers: { i: 4 }, vars: { pick: "2-3:1", cost: 3 }, note: "n-1 edges → done" }
  ]'
/>

**Complexity** — Time **O((n + E) log(n + E))**; Space **O(n + E)**.

---

## Try it yourself

<JavaRunner problem-slug="optimize-water-distribution-in-a-village" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Kruskal + virtual root | **O((n+E) log(n+E))** | O(n+E) | canonical |

## When to use which

- **"Free option per node"** → virtual root MST.
- **"Free option per subset"** → generalizes with more virtual nodes.
- **Dense pipes** → Prim + heap.

<AiCompanion problem-slug="optimize-water-distribution-in-a-village" pattern-hint="union-find" />

## Related problems

- [Min Cost to Connect All Points](/problems/min-cost-to-connect-all-points)
- [Connecting Cities With Minimum Cost](/problems/connecting-cities-with-minimum-cost)
- [Find Critical/Pseudo-Critical MST Edges](/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree)

<FeedbackWidget problem-slug="optimize-water-distribution-in-a-village" />
