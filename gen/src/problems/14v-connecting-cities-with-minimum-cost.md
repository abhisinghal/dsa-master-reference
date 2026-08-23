# Union-Find — Connecting Cities With Minimum Cost

*[↗ LeetCode: Connecting Cities With Minimum Cost](https://leetcode.com/problems/connecting-cities-with-minimum-cost/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/union-find)

<CompanyTags companies="Amazon, Google, Meta" />

Given `n` cities and `connections[i] = [a, b, cost]`, return the minimum cost to make all connected. `-1` if impossible.

**Example 1** — `n=3, connections=[[1,2,5],[1,3,6],[2,3,1]]` → `6` (pick [2,3,1] and [1,2,5])
**Example 2** — `n=4, connections=[[1,2,3],[3,4,4]]` → `-1`

**Constraints** — `1 ≤ n ≤ 10⁴`.


<Hints
  hint1="Are you grouping things by shared property? Adjacent lands, same friend circle, connected components?"
  hint2="Union-Find: `find(x)` returns root; `union(a, b)` merges. Path compression + union by rank gives α(n)."
  hint3="For MST (min-cost connect all): Kruskal sorts edges, unions if disjoint, stops at n−1 edges."
/>
---

<MarkSolved problem-slug="connecting-cities-with-minimum-cost" />

<InterviewTimer problem-slug="connecting-cities-with-minimum-cost" />



## Approach 1 — Try all spanning trees

Exponential. Baseline.

## Approach 2 — Kruskal MST (canonical)

**Insight.** Sort edges by cost; process ascending. Add if it unions two components; skip otherwise. Stop when we have n-1 edges. If fewer, return -1.

```java
int minimumCost(int n, int[][] connections) {
    Arrays.sort(connections, (a, b) -> a[2] - b[2]);
    int[] parent = new int[n + 1];
    for (int i = 0; i <= n; i++) parent[i] = i;
    int cost = 0, edges = 0;
    for (int[] e : connections) {
        int ra = find(parent, e[0]), rb = find(parent, e[1]);
        if (ra == rb) continue;
        parent[ra] = rb;
        cost += e[2];
        if (++edges == n - 1) return cost;
    }
    return -1;
}
int find(int[] p, int x) { return p[x] == x ? x : (p[x] = find(p, p[x])); }
```

<CodeTrace
  title="Kruskal — n=3, sorted [[2,3,1],[1,2,5],[1,3,6]]"
  :values="['[2,3,1]','[1,2,5]','[1,3,6]']"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { cost: 1, edges: 1 }, note: "" },
    { pointers: { i: 1 }, vars: { cost: 6, edges: 2 }, note: "n-1 reached → return 6" }
  ]'
/>

**Complexity** — Time **O(E log E)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="connecting-cities-with-minimum-cost" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Enumerate ST | exponential | O(n) | baseline |
| Kruskal + UF | **O(E log E)** | O(n) | canonical |

## When to use which

- **Sparse graph** → Kruskal.
- **Dense graph** → Prim + heap: O(E + V log V).
- **"Second-best MST"** → replace each MST edge with best non-MST alternative.

<AiCompanion problem-slug="connecting-cities-with-minimum-cost" pattern-hint="union-find" />

## Related problems

- [Min Cost to Connect All Points](/problems/min-cost-to-connect-all-points)
- [Optimize Water Distribution](/problems/optimize-water-distribution-in-a-village)
- [Find Critical/Pseudo-Critical MST Edges](/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree)

<FeedbackWidget problem-slug="connecting-cities-with-minimum-cost" />

<RelatedProblems problems="min-cost-to-connect-all-points::Min Cost To Connect All Points|number-of-islands-ii::Number Of Islands II|accounts-merge::Accounts Merge" />
