# Trie — Design Add and Search Words Data Structure

*[↗ LeetCode: Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/trie-pattern)

<CompanyTags companies="Meta, Amazon, Google, Uber" />

Design `WordDictionary` with `addWord(word)` and `search(word)`. `search` may contain `.` which matches any letter.

**Example** —
```
WordDictionary w = new WordDictionary();
w.addWord("bad"); w.addWord("dad"); w.addWord("mad");
w.search("pad"); // false
w.search("bad"); // true
w.search(".ad"); // true
w.search("b.."); // true
```

**Constraints** — ≤ 25 chars/word; up to 10⁴ ops. Brute HashSet of words + brute-scan on wildcards — O(N·L) per wildcard search dies at 10⁵ queries. Trie + DFS for `.` wildcards is O(L·26^wildcards) per query — ~10⁶ ops even under load.
<Hints
  hint1="Prefix operations? Word set lookups? Autocomplete?"
  hint2="Each node has ≤ σ children (26 for lowercase). Walk char-by-char; create nodes on insert; check `end` flag on search."
  hint3="For XOR max: binary trie of 32-bit values; walk greedily choosing the opposite bit."
/>
---

<MarkSolved problem-slug="design-add-and-search-words-data-structure" /> <Bookmark problem-slug="design-add-and-search-words-data-structure" />

<InterviewTimer problem-slug="design-add-and-search-words-data-structure" />



## Approach 1 — HashSet + linear scan

`search` is O(N · L) worst — too slow with wildcards.

## Approach 2 — Trie with DFS branching on `.` (canonical)

**Insight.** Standard trie for `addWord`. For `search`, DFS: at `.`, try all 26 children; else follow the single edge.

```java
class WordDictionary {
    class Node { Node[] c = new Node[26]; boolean end; }
    Node root = new Node();
    public void addWord(String w) {
        Node cur = root;
        for (char ch : w.toCharArray()) {
            int i = ch - 'a';
            if (cur.c[i] == null) cur.c[i] = new Node();
            cur = cur.c[i];
        }
        cur.end = true;
    }
    public boolean search(String w) { return dfs(root, w, 0); }
    boolean dfs(Node cur, String w, int idx) {
        if (idx == w.length()) return cur.end;
        char ch = w.charAt(idx);
        if (ch == '.') {
            for (Node child : cur.c) if (child != null && dfs(child, w, idx + 1)) return true;
            return false;
        }
        int i = ch - 'a';
        return cur.c[i] != null && dfs(cur.c[i], w, idx + 1);
    }
}
```

<CodeTrace
  title="Trie search '.ad'"
  :values="['.','a','d']"
  :windowKeys="['idx']"
  :cellWidth="34"
  :steps='[
    { pointers: { idx: 0 }, vars: { branch: "all 26" }, note: "" },
    { pointers: { idx: 1 }, vars: { children: "b→a, d→a, m→a" }, note: "" },
    { pointers: { idx: 2 }, vars: { found: true }, note: "e.g. bad exists" }
  ]'
/>

**Complexity** — `addWord` **O(L)**; `search` **O(26^k · L)** worst where k = # dots; usually much less.

---

## Try it yourself

<JavaRunner problem-slug="design-add-and-search-words-data-structure" />

## Complexity summary

| Approach | add | search | Grade |
|---|---|---|---|
| HashSet + scan | O(L) | O(N · L) | rejected |
| Trie + DFS | **O(L)** | **O(26^k · L)** | canonical |

## When to use which

- **Fixed alphabet + wildcards** → trie + DFS branching.
- **Long words** → limit early via length check per branch.
- **Regex support** → NFA / recursive descent.

<AiCompanion problem-slug="design-add-and-search-words-data-structure" pattern-hint="trie" />

## Related problems

- [Implement Trie](/problems/implement-trie) — the base
- [Word Search II](/problems/trie-word-search-ii)
- [Stream of Characters](/problems/stream-of-characters)

<FeedbackWidget problem-slug="design-add-and-search-words-data-structure" />

<RelatedProblems problems="word-search-ii::Word Search II|trie-word-search-ii::Trie Word Search II|stream-of-characters::Stream Of Characters" />
