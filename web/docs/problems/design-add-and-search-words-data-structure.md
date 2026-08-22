# Trie — Design Add and Search Words Data Structure

*[↗ LeetCode: Design Add and Search Words](https://leetcode.com/problems/design-add-and-search-words-data-structure/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/trie-pattern)

Support `addWord(w)` and `search(w)` where `w` may contain `'.'` matching any single letter.

---

## Approach 1 — Trie + wildcard-aware DFS
**Insight.** Standard trie for adds. Search recursively; when hitting `'.'`, try every child.



```java
class WordDictionary {
    static class Node { Map<Character, Node> ch = new HashMap<>(); boolean end; }
    Node root = new Node();
    public void addWord(String w) {
        Node cur = root;
        for (char c : w.toCharArray()) cur = cur.ch.computeIfAbsent(c, k -> new Node());
        cur.end = true;
    }
    public boolean search(String w) { return dfs(root, w, 0); }
    boolean dfs(Node node, String w, int i) {
        if (i == w.length()) return node.end;
        char c = w.charAt(i);
        if (c != '.') return node.ch.containsKey(c) && dfs(node.ch.get(c), w, i + 1);
        for (Node child : node.ch.values()) if (dfs(child, w, i + 1)) return true;
        return false;
    }
}
```



**Complexity** — addWord: **O(L)**; search: **O(L)** avg, **O(26^L)** worst-case with all dots.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Trie + wildcard-aware DFS | O(L) | O(L) | primary |

## When to use which

- **Ship this** → Trie + wildcard-aware DFS (O(L), O(L)). The pattern's standard solution.

## Related problems

- [Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/) — no wildcards
- [Word Search II](/problems/trie-word-search-ii)
- [Replace Words](/problems/replace-words)
