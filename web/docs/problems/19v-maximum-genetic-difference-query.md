# Trie — Maximum Genetic Difference Query

*[↗ LeetCode: Maximum Genetic Difference Query](https://leetcode.com/problems/maximum-genetic-difference-query/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/trie-pattern)

Given a rooted tree of gene values and queries `[node, val]`, return `max XOR(val, x)` where `x` is any ancestor value of `node` (including node itself).

## Approach — Offline DFS + binary trie with subtree insert/erase

**Insight.** Group queries by node. DFS from root; on entering a node, insert its value into a shared binary trie; on leaving, remove it. Answer each node's queries when the trie contains exactly the ancestor path.



```java
class Node { Node[] ch = new Node[2]; int cnt; }
int[] maxGeneticDifference(int[] parents, int[][] queries) {
    int n = parents.length;
    List<List<Integer>> children = new ArrayList<>();
    for (int i = 0; i < n; i++) children.add(new ArrayList<>());
    int root = -1;
    for (int i = 0; i < n; i++) if (parents[i] == -1) root = i; else children.get(parents[i]).add(i);
    Map<Integer, List<int[]>> qByNode = new HashMap<>();
    for (int i = 0; i < queries.length; i++) qByNode.computeIfAbsent(queries[i][0], k -> new ArrayList<>()).add(new int[]{queries[i][1], i});
    int[] ans = new int[queries.length];
    Node trie = new Node();
    dfs(root, children, qByNode, trie, ans);
    return ans;
}
void dfs(int u, List<List<Integer>> children, Map<Integer, List<int[]>> qByNode, Node trie, int[] ans) {
    insert(trie, u, +1);
    if (qByNode.containsKey(u))
        for (int[] q : qByNode.get(u)) ans[q[1]] = queryMax(trie, q[0]);
    for (int c : children.get(u)) dfs(c, children, qByNode, trie, ans);
    insert(trie, u, -1);
}
void insert(Node root, int x, int delta) {
    Node cur = root;
    for (int i = 17; i >= 0; i--) {
        int b = (x >> i) & 1;
        if (cur.ch[b] == null) cur.ch[b] = new Node();
        cur = cur.ch[b];
        cur.cnt += delta;
    }
}
int queryMax(Node root, int v) {
    Node cur = root;
    int result = 0;
    for (int i = 17; i >= 0; i--) {
        int b = (v >> i) & 1, want = 1 - b;
        if (cur.ch[want] != null && cur.ch[want].cnt > 0) { result |= 1 << i; cur = cur.ch[want]; }
        else cur = cur.ch[b];
    }
    return result;
}
```



**Complexity** — Time **O((n + q) · 18)**; Space **O(n · 18)**.

## Related problems

- [Maximum XOR With an Element From Array](/problems/maximum-xor-with-an-element-from-array) — flat array variant
- [Count Pairs With XOR in a Range](/problems/count-pairs-with-xor-in-a-range)
