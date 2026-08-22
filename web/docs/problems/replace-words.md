# Trie — Replace Words

*[↗ LeetCode: Replace Words](https://leetcode.com/problems/replace-words/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/trie-pattern)

Given roots and a sentence, replace each word with its shortest root prefix (if any).

**Example** — `dict=["cat","bat","rat"], s="the cattle was rattled by the battery"` → `"the cat was rat by the bat"`

---

## Approach 1 — Trie of roots + prefix walk per word


```java
class Node { Map<Character, Node> ch = new HashMap<>(); String word; }
public String replaceWords(List<String> dict, String s) {
    Node root = new Node();
    for (String r : dict) {
        Node cur = root;
        for (char c : r.toCharArray()) cur = cur.ch.computeIfAbsent(c, k -> new Node());
        cur.word = r;
    }
    StringBuilder out = new StringBuilder();
    for (String w : s.split(" ")) {
        if (out.length() > 0) out.append(' ');
        Node cur = root;
        StringBuilder replaced = new StringBuilder();
        for (char c : w.toCharArray()) {
            if (cur.word != null) { replaced.setLength(0); replaced.append(cur.word); break; }
            if (!cur.ch.containsKey(c)) { replaced.setLength(0); replaced.append(w); break; }
            cur = cur.ch.get(c);
            replaced.append(c);
        }
        if (cur.word != null) { replaced.setLength(0); replaced.append(cur.word); }
        else if (replaced.length() == w.length()) { replaced.setLength(0); replaced.append(w); }
        out.append(replaced);
    }
    return out.toString();
}
```




<CodeTrace
  title="Trie of roots + prefix walk per word"
  :values="['cat', 'bat', 'rat']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize; scan begins." },
    { pointers: { i: 0 }, vars: { phase: "midway" }, note: "Midway through the scan." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "All positions considered — return the answer." }
  ]'
/>


**Complexity** — Time **O(D + S)**; Space **O(D)** where D = total chars in dict.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Trie of roots + prefix walk per word | O(D + S) | O(D) | primary |

## When to use which

- **Ship this** → Trie of roots + prefix walk per word (O(D + S), O(D)). The pattern's standard solution.

## Related problems

- [Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/) — basic trie
- [Word Search II](/problems/trie-word-search-ii)
