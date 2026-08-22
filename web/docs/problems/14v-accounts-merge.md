# Union-Find — Accounts Merge

*[↗ LeetCode: Accounts Merge](https://leetcode.com/problems/accounts-merge/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/union-find)

Given accounts `[name, e1, e2, …]`, merge accounts sharing at least one email. Return merged accounts with emails sorted.

**Example** — `[["John","a@","b@"],["John","c@"],["John","a@","d@"]]` → John merged for emails `[a@, b@, d@]`; separate John for `[c@]`.

---

## Approach 1 — BFS/DFS on the email graph

Build undirected graph on emails; each account contributes a fully-connected clique. Traverse components. O(N α(N)).

## Approach 2 — Union-Find on emails (canonical)

**Insight.** Union all emails within each account. After the pass, group emails by root.



```java
Map<String, String> parent = new HashMap<>();
String find(String x) { while (!x.equals(parent.get(x))) { parent.put(x, parent.get(parent.get(x))); x = parent.get(x); } return x; }
void union(String a, String b) { parent.put(find(a), find(b)); }

List<List<String>> accountsMerge(List<List<String>> accounts) {
    Map<String, String> owner = new HashMap<>();
    for (List<String> acc : accounts) {
        for (int i = 1; i < acc.size(); i++) {
            parent.putIfAbsent(acc.get(i), acc.get(i));
            owner.put(acc.get(i), acc.get(0));
            if (i > 1) union(acc.get(1), acc.get(i));
        }
    }
    Map<String, TreeSet<String>> groups = new HashMap<>();
    for (String email : parent.keySet())
        groups.computeIfAbsent(find(email), k -> new TreeSet<>()).add(email);
    List<List<String>> out = new ArrayList<>();
    for (var e : groups.entrySet()) {
        List<String> row = new ArrayList<>();
        row.add(owner.get(e.getKey()));
        row.addAll(e.getValue());
        out.add(row);
    }
    return out;
}
```



**Complexity** — Time **O(N α(N) + N log N)** (sort); Space **O(N)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| BFS/DFS | O(N α(N)) | O(N) |
| Union-Find | **O(N α(N) + N log N)** | O(N) |

## Related problems

- [Number of Provinces](/problems/union-find-number-of-provinces)
- [Redundant Connection](/problems/redundant-connection) — first edge causing cycle
- [Most Stones Removed](/problems/most-stones-removed-with-same-row-or-column)
