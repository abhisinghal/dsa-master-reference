# Topological Sort — Minimum Height Trees

*[↗ LeetCode: Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/topological-sort)

&lt;CompanyTags companies="Amazon, Google, Meta" /&gt;

Given an undirected tree of `n` nodes, return all nodes that when picked as root give minimum height tree. At most 2 exist.

**Example 1** — `n=4, edges=[[1,0],[1,2],[1,3]]` → `[1]`
**Example 2** — `n=6, edges=[[3,0],[3,1],[3,2],[3,4],[5,4]]` → `[3,4]`

**Constraints** — `1 ≤ n ≤ 2·10⁴`.


&lt;Hints
  hint1="Directed graph? Prerequisites? You need topological order."
  hint2="Kahn’s BFS: start from nodes with indeg 0; when you pop, decrement neighbors’ indeg; add new zeros."
  hint3="For ’layers/semesters’, process one full BFS layer per timestep. For ’unique order?’, check queue size ≤ 1 at every step."
/&gt;
---

&lt;MarkSolved problem-slug="minimum-height-trees" /&gt;


## Approach 1 — Try each node as root, BFS

O(n²). TLE at n=2·10⁴.

## Approach 2 — Peel leaves inward (canonical topological peeling)

**Insight.** MHT roots are always at the **center(s)** of the tree — 1 or 2 nodes. Repeatedly remove leaves (degree-1 nodes) layer by layer. The last remaining 1 or 2 nodes are the answer.



```java
List<Integer> findMinHeightTrees(int n, int[][] edges) {
    if (n == 1) return List.of(0);
    List<Set<Integer>> g = new ArrayList<>();
    for (int i = 0; i < n; i++) g.add(new HashSet<>());
    for (int[] e : edges) { g.get(e[0]).add(e[1]); g.get(e[1]).add(e[0]); }
    List<Integer> leaves = new ArrayList<>();
    for (int i = 0; i < n; i++) if (g.get(i).size() == 1) leaves.add(i);
    int remaining = n;
    while (remaining > 2) {
        remaining -= leaves.size();
        List<Integer> next = new ArrayList<>();
        for (int leaf : leaves) {
            int parent = g.get(leaf).iterator().next();
            g.get(parent).remove(leaf);
            if (g.get(parent).size() == 1) next.add(parent);
        }
        leaves = next;
    }
    return leaves;
}
```



<CodeTrace
  title="Peel — n=6, tree with center 3-4 edge"
  :values="['0','1','2','3','4','5']"
  :windowKeys="['round']"
  :cellWidth="30"
  :steps='[
    { pointers: { round: 0 }, vars: { leaves: "[0,1,2,5]" }, note: "initial leaves" },
    { pointers: { round: 1 }, vars: { remaining: 2, leaves: "[3,4]" }, note: "after peeling; 2 center nodes" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="minimum-height-trees" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| BFS from each root | O(n²) | O(n) | baseline |
| Peel leaves | **O(n)** | O(n) | canonical |

## When to use which

- **Tree center problems** → leaf peeling.
- **General graph center** → different — use eccentricity / all-pairs BFS.
- **"Return the actual height"** → 2-BFS: BFS from any node to find farthest u; BFS from u to find diameter.

&lt;AiCompanion problem-slug="minimum-height-trees" pattern-hint="topological sort" /&gt;

## Related problems

- [Course Schedule](/problems/topological-sort-course-schedule) — general graph toposort
- [Tree Diameter](https://leetcode.com/problems/tree-diameter/)
- [Longest Path in Tree](https://leetcode.com/problems/longest-path-with-different-adjacent-characters/)

&lt;FeedbackWidget problem-slug="minimum-height-trees" /&gt;
