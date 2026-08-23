# Trie — Maximum Genetic Difference Query

*[↗ LeetCode: Maximum Genetic Difference Query](https://leetcode.com/problems/maximum-genetic-difference-query/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/trie-pattern)

Given a rooted tree of gene values `parents[]` and queries `[node, val]`, for each query return `max XOR(val, x)` over `x` in any ancestor of `node` (including `node` itself).

**Constraints** — `1 ≤ n ≤ 10⁵`; queries ≤ 3·10⁴.

**Example 1** — `parents=[-1,0,1,1], queries=[[0,2],[3,2],[2,5]]` → `[2,3,7]`

---

## Approach — Offline DFS + binary trie with subtree insert/erase (canonical)

**Insight.** Group queries by node. DFS from root; on entering a node, insert its value into a shared binary trie; on leaving, remove it. Answer each node's queries when the trie contains exactly the ancestor path.



```java
class Node { Node[] c = new Node[2]; int cnt; }
int[] maxGeneticDifference(int[] parents, int[][] queries) {
    int n = parents.length;
    List<List<Integer>> ch = new ArrayList<>();
    for (int i = 0; i < n; i++) ch.add(new ArrayList<>());
    int root = -1;
    for (int i = 0; i < n; i++) if (parents[i] == -1) root = i; else ch.get(parents[i]).add(i);
    Map<Integer, List<int[]>> qByNode = new HashMap<>();
    for (int i = 0; i < queries.length; i++) qByNode.computeIfAbsent(queries[i][0], k -> new ArrayList<>()).add(new int[]{queries[i][1], i});
    int[] ans = new int[queries.length];
    Node trie = new Node();
    dfs(root, ch, qByNode, trie, ans);
    return ans;
}
void dfs(int u, List<List<Integer>> ch, Map<Integer, List<int[]>> qByNode, Node trie, int[] ans) {
    insert(trie, u, +1);
    if (qByNode.containsKey(u))
        for (int[] q : qByNode.get(u)) ans[q[1]] = queryMax(trie, q[0]);
    for (int v : ch.get(u)) dfs(v, ch, qByNode, trie, ans);
    insert(trie, u, -1);
}
void insert(Node root, int x, int d) {
    Node cur = root;
    for (int i = 17; i >= 0; i--) {
        int b = (x >> i) & 1;
        if (cur.c[b] == null) cur.c[b] = new Node();
        cur = cur.c[b];
        cur.cnt += d;
    }
}
int queryMax(Node root, int v) {
    Node cur = root; int r = 0;
    for (int i = 17; i >= 0; i--) {
        int b = (v >> i) & 1, want = 1 - b;
        if (cur.c[want] != null && cur.c[want].cnt > 0) { r |= 1 << i; cur = cur.c[want]; }
        else cur = cur.c[b];
    }
    return r;
}
```



<CodeTrace
  title="Offline DFS + binary trie with subtree insert/erase (cano..."
  :values="['-1', '0', '1', '1']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O((n + q) · 18)**; Space **O(n · 18)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Offline DFS + binary trie | **O((n+q)·18)** | O(n · 18) | canonical |

## When to use which

- **Path queries with XOR** → DFS with add/remove on entry/exit.
- **Adjacent-subtree queries** → Euler tour + Fenwick / mo's algorithm.
- **Static path** (no ancestor constraint) → offline sort on max_allowed.

## Related problems

- [Maximum XOR With an Element From Array](/problems/maximum-xor-with-an-element-from-array)
- [Count Pairs With XOR in Range](/problems/count-pairs-with-xor-in-a-range)
- [Maximum XOR of Two Numbers](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/)