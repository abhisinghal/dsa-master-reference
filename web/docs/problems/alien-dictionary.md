# Topological Sort — Alien Dictionary

*[↗ LeetCode: Alien Dictionary](https://leetcode.com/problems/alien-dictionary/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/topological-sort)

Given a list of words in an alien language's dictionary order, return the letter order (any valid one) or `""` if no valid order exists.

**Example** — `["wrt","wrf","er","ett","rftt"]` → `"wertf"`

---

## Approach 1 — Try every permutation of the alphabet

O(26!). Absurd.

## Approach 2 — Build a DAG from adjacent pairs, then Kahn's topo-sort

**Insight.** From adjacent word pairs, the **first differing character** gives an edge: earlier char → later char.

**Trap.** If a later word is a proper prefix of an earlier word (e.g. `"abc"` before `"ab"`), no valid order exists → return `""`.



```java
String alienOrder(String[] words) {
    Map<Character, Set<Character>> graph = new HashMap<>();
    int[] indeg = new int[26];
    boolean[] seen = new boolean[26];
    for (String w : words) for (char c : w.toCharArray()) { seen[c - 'a'] = true; graph.putIfAbsent(c, new HashSet<>()); }
    for (int i = 0; i < words.length - 1; i++) {
        String a = words[i], b = words[i + 1];
        if (a.length() > b.length() && a.startsWith(b)) return "";      // trap
        int m = Math.min(a.length(), b.length());
        for (int j = 0; j < m; j++)
            if (a.charAt(j) != b.charAt(j)) {
                if (graph.get(a.charAt(j)).add(b.charAt(j))) indeg[b.charAt(j) - 'a']++;
                break;
            }
    }
    Deque<Character> q = new ArrayDeque<>();
    for (int i = 0; i < 26; i++) if (seen[i] && indeg[i] == 0) q.offer((char)('a' + i));
    StringBuilder sb = new StringBuilder();
    while (!q.isEmpty()) {
        char u = q.poll(); sb.append(u);
        for (char v : graph.get(u)) if (--indeg[v - 'a'] == 0) q.offer(v);
    }
    int total = 0; for (int i = 0; i < 26; i++) if (seen[i]) total++;
    return sb.length() == total ? sb.toString() : "";
}
```



<CodeTrace
  title="Alien order — [wrt,wrf,er,ett,rftt]"
  :values="['w','r','t','f','e']"
  :windowKeys="['step']"
  :cellWidth="42"
  :steps='[
    { pointers: { step: 0 }, vars: { edges: "t→f, w→e, r→t, e→r" }, note: "derive edges from adjacent pairs" },
    { pointers: { step: 1 }, vars: { indeg: "{w:0, r:1, t:1, f:1, e:1}" }, note: "compute in-degrees" },
    { pointers: { step: 2 }, vars: { queue: "[w]", out: "w" }, note: "start with w (in-deg 0)", added: [0] },
    { pointers: { step: 3 }, vars: { queue: "[e]", out: "we" }, note: "pop w → e unlocks", added: [4] },
    { pointers: { step: 6 }, vars: { out: "wertf" }, note: "final answer: wertf", added: [0,4,1,2,3] }
  ]'
/>

**Complexity** — Time **O(C)** where C = total chars; Space **O(1)** (26 alphabet).

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Try all permutations | O(26!) | O(1) |
| Topo-sort on DAG | **O(C)** | O(1) |

## Related problems

- [Course Schedule II](/problems/topological-sort-course-schedule) — canonical Kahn's
- [Sequence Reconstruction](/problems/sequence-reconstruction) — unique topological order
- [Verifying an Alien Dictionary](https://leetcode.com/problems/verifying-an-alien-dictionary/) — given order, verify sorted
