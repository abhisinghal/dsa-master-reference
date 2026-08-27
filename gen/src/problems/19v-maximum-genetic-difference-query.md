# Trie — Maximum Genetic Difference Query

*[↗ LeetCode: Maximum Genetic Difference Query](https://leetcode.com/problems/maximum-genetic-difference-query/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/trie-pattern)

<CompanyTags companies="Google, Amazon" />

Given a rooted tree of gene values `parents[]` and queries `[node, val]`, for each query return `max XOR(val, x)` over `x` in any ancestor of `node` (including `node` itself).

**Constraints** — `1 ≤ n ≤ 10⁵`; queries ≤ 3·10⁴; values ≤ 2¹⁸. Naive per-query walk up ancestors costs O(n·q·18) = 5·10¹⁰ ops. Offline DFS + binary trie is O((n+q)·18) ≈ 2·10⁶.

**Example 1** — `parents=[-1,0,1,1], queries=[[0,2],[3,2],[2,5]]` → `[2,3,7]`
**Example 2** — `parents=[3,7,-1,2,0,7,0,2], queries=[[4,6],[1,15],[0,5]]` → `[6,14,7]`
**Example 3** — `parents=[-1], queries=[[0,10]]` → `[10]` (single-node tree)


<Hints
  hint1="Prefix operations? Word set lookups? Autocomplete?"
  hint2="Each node has ≤ σ children (26 for lowercase). Walk char-by-char; create nodes on insert; check `end` flag on search."
  hint3="For XOR max: binary trie of 32-bit values; walk greedily choosing the opposite bit."
/>
---

<MarkSolved problem-slug="maximum-genetic-difference-query" /> <Bookmark problem-slug="maximum-genetic-difference-query" />

<InterviewTimer problem-slug="maximum-genetic-difference-query" />



## Approach 1 — Per-query naive walk up the tree

**Intuition.** For each query `[node, val]`, walk up from `node` to root; for every ancestor `a` compute `val ^ node_value[a]`; take max.

```java
int[] maxGeneticDifferenceBrute(int[] parents, int[][] queries) {
    int[] ans = new int[queries.length];
    for (int i = 0; i < queries.length; i++) {
        int node = queries[i][0], val = queries[i][1];
        int best = 0;
        for (int u = node; u != -1; u = parents[u]) {
            best = Math.max(best, val ^ u);
        }
        ans[i] = best;
    }
    return ans;
}
```

**Complexity** — Time **O(n · q)** worst case; Space **O(1)**. For n=10⁵ q=3·10⁴, chain-shaped tree → 3·10⁹ ops = TLE. *In an interview* say "offline DFS + binary trie with insert-on-enter / erase-on-exit turns this into O((n+q)·18)."

---

## Approach 2 — Offline DFS + binary trie with subtree insert/erase (canonical)

**Insight.** Group queries by node. Do a single DFS from root. **On entering** a node, insert its value into a shared binary trie. **On leaving**, erase (decrement count). At each node, answer its queries using the trie — which now contains exactly the ancestor path of that node.

The trie tracks counts (not just existence) so that erase-on-exit works without allocating a new trie per subtree.

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

**Complexity** — Time **O((n + q) · 18)**; Space **O(n · 18)**. *Say aloud in an interview:* "offline DFS with add-on-enter / erase-on-exit — same pattern behind Mo's algorithm on trees. Every insert/erase costs one path down the binary trie."

---

## Try it yourself

<JavaRunner problem-slug="maximum-genetic-difference-query" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Per-query walk up | O(n · q) | O(1) | Reference; TLE on chain |
| **Offline DFS + binary trie** | **O((n+q)·18)** | O(n · 18) | **Canonical** |

## When to use which

- **Path queries with XOR** → DFS with add/remove on entry/exit.
- **Adjacent-subtree queries** → Euler tour + Fenwick / mo's algorithm.
- **Static path** (no ancestor constraint) → offline sort on max_allowed.

<AiCompanion problem-slug="maximum-genetic-difference-query" pattern-hint="trie" />

## Related problems

- [Maximum XOR With an Element From Array](/problems/maximum-xor-with-an-element-from-array)
- [Count Pairs With XOR in Range](/problems/count-pairs-with-xor-in-a-range)
- [Maximum XOR of Two Numbers](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/)

<FeedbackWidget problem-slug="maximum-genetic-difference-query" />
