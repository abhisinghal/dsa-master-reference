# Union-Find — Number of Islands II

*[↗ LeetCode: Number of Islands II](https://leetcode.com/problems/number-of-islands-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/union-find)

<CompanyTags companies="Google, Amazon, Meta" />

You have an `m × n` grid of water. Given `positions` where each `(r, c)` becomes land, return count of islands after each addition.

**Example 1** — `m=3, n=3, positions=[[0,0],[0,1],[1,2],[2,1]]` → `[1,1,2,3]`

**Constraints** — `1 ≤ m·n ≤ 10⁴`.


<Hints
  hint1="Are you grouping things by shared property? Adjacent lands, same friend circle, connected components?"
  hint2="Union-Find: `find(x)` returns root; `union(a, b)` merges. Path compression + union by rank gives α(n)."
  hint3="For MST (min-cost connect all): Kruskal sorts edges, unions if disjoint, stops at n−1 edges."
/>
---

## Approach 1 — DFS after each addition

O(k · m·n). Too slow for streaming.

## Approach 2 — Streaming Union-Find (canonical)

**Insight.** Each new land cell either starts a new island or merges into existing neighbors. Union-Find handles both:
- Mark cell as land; count++.
- For each of 4 neighbors that is land AND has a different root: union; count--.

```java
List<Integer> numIslands2(int m, int n, int[][] positions) {
    int[] parent = new int[m * n];
    Arrays.fill(parent, -1);
    int[][] D = {{1,0},{-1,0},{0,1},{0,-1}};
    List<Integer> out = new ArrayList<>();
    int count = 0;
    for (int[] p : positions) {
        int r = p[0], c = p[1], id = r * n + c;
        if (parent[id] != -1) { out.add(count); continue; }
        parent[id] = id; count++;
        for (int[] d : D) {
            int nr = r + d[0], nc = c + d[1], nid = nr * n + nc;
            if (nr < 0 || nc < 0 || nr >= m || nc >= n || parent[nid] == -1) continue;
            if (union(parent, id, nid)) count--;
        }
        out.add(count);
    }
    return out;
}
int find(int[] p, int x) { return p[x] == x ? x : (p[x] = find(p, p[x])); }
boolean union(int[] p, int a, int b) {
    int ra = find(p, a), rb = find(p, b);
    if (ra == rb) return false;
    p[ra] = rb; return true;
}
```

<CodeTrace
  title="UF stream — positions=[[0,0],[0,1],[1,2],[2,1]]"
  :values="['(0,0)','(0,1)','(1,2)','(2,1)']"
  :windowKeys="['step']"
  :cellWidth="34"
  :steps='[
    { pointers: { step: 0 }, vars: { count: 1 }, note: "" },
    { pointers: { step: 1 }, vars: { count: 1 }, note: "merged with (0,0)" },
    { pointers: { step: 2 }, vars: { count: 2 }, note: "new island" },
    { pointers: { step: 3 }, vars: { count: 3 }, note: "" }
  ]'
/>

**Complexity** — Time **O(k · α(m·n))**; Space **O(m·n)**.

---

## Try it yourself

<JavaRunner problem-slug="number-of-islands-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DFS per add | O(k · m·n) | O(m·n) | too slow streaming |
| Union-Find streaming | **O(k · α(m·n))** | O(m·n) | canonical |

## When to use which

- **Streaming connectivity** → Union-Find.
- **Static** → DFS/BFS flood fill.
- **Deletion of land** → offline reverse: process removals as additions.

<AiCompanion problem-slug="number-of-islands-ii" pattern-hint="union-find" />

## Related problems

- [Number of Islands](/problems/number-of-islands)
- [Number of Provinces](/problems/union-find-number-of-provinces)
- [Making a Large Island](https://leetcode.com/problems/making-a-large-island/)

<FeedbackWidget problem-slug="number-of-islands-ii" />
