# Union-Find — Most Stones Removed with Same Row or Column

*[↗ LeetCode: Most Stones Removed with Same Row or Column](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/union-find)

<CompanyTags companies="Amazon, Google" />

Given stones on a 2D plane, remove a stone if it shares a row/column with another. Return max stones removable.

**Example 1** — `stones=[[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]` → `5`
**Example 2** — `stones=[[0,0]]` → `0`

**Constraints** — `1 ≤ n ≤ 1000`.


<Hints
  hint1="Are you grouping things by shared property? Adjacent lands, same friend circle, connected components?"
  hint2="Union-Find: `find(x)` returns root; `union(a, b)` merges. Path compression + union by rank gives α(n)."
  hint3="For MST (min-cost connect all): Kruskal sorts edges, unions if disjoint, stops at n−1 edges."
/>
---

## Approach 1 — Simulation

Try every removal order. Exponential.

## Approach 2 — Union-Find: n − #components (canonical)

**Insight.** Stones sharing a row or column form a connected component. From any component of size `k`, we can remove `k - 1` stones (leaving one). Total removable = `n - #components`.

Union rows and columns by treating "row r" and "col c" as separate entities (e.g., cols offset by 10⁴).

```java
int removeStones(int[][] stones) {
    Map<Integer, Integer> parent = new HashMap<>();
    for (int[] s : stones) {
        int r = s[0], c = s[1] + 10001;
        union(parent, r, c);
    }
    Set<Integer> roots = new HashSet<>();
    for (int k : parent.keySet()) roots.add(find(parent, k));
    return stones.length - roots.size();
}
int find(Map<Integer, Integer> p, int x) {
    if (!p.containsKey(x)) { p.put(x, x); return x; }
    if (p.get(x) == x) return x;
    int r = find(p, p.get(x));
    p.put(x, r);
    return r;
}
void union(Map<Integer, Integer> p, int a, int b) {
    p.put(find(p, a), find(p, b));
}
```

<CodeTrace
  title="Simulation"
  :values="['0', '0']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n · α)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="most-stones-removed-with-same-row-or-column" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Simulation | exponential | O(n) | baseline |
| UF: n − components | **O(n · α)** | O(n) | canonical |

## When to use which

- **"Max removable so each remaining is disconnected"** → components trick.
- **"Fewest to keep"** → same result (`#components`).
- **"Sharing row OR col OR diagonal"** → add diagonals as a 3rd entity type.

<AiCompanion problem-slug="most-stones-removed-with-same-row-or-column" pattern-hint="union-find" />

## Related problems

- [Number of Provinces](/problems/union-find-number-of-provinces)
- [Accounts Merge](/problems/accounts-merge)
- [Connecting Cities With Minimum Cost](/problems/connecting-cities-with-minimum-cost)