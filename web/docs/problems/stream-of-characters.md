# Trie — Stream of Characters

*[↗ LeetCode: Stream of Characters](https://leetcode.com/problems/stream-of-characters/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/trie-pattern)

&lt;CompanyTags companies="Amazon, Google" /&gt;

Design `StreamChecker`. `query(c)` returns true iff the last k chars form a word in the dictionary (for any k).

**Example** — with `dict = ["cd","f","kl"]`, streaming `a,b,c,d,e,f,g,h,i,j,k,l` returns `[F,F,F,T,F,T,F,F,F,F,F,T]`.

**Constraints** — dict ≤ 2000 words, each ≤ 200 chars; up to 4·10⁴ queries.


&lt;Hints
  hint1="Prefix operations? Word set lookups? Autocomplete?"
  hint2="Each node has ≤ σ children (26 for lowercase). Walk char-by-char; create nodes on insert; check `end` flag on search."
  hint3="For XOR max: binary trie of 32-bit values; walk greedily choosing the opposite bit."
/&gt;
---

## Approach 1 — Materialize stream, check every suffix

O(k · #dict) per query. Baseline.

## Approach 2 — Reverse trie + suffix walk (canonical)

**Insight.** Insert each word **reversed** into a trie. Maintain running stream in a buffer. On each query, walk from newest char backward through the trie; if we hit an `end` node, return true.



```java
class Node { Node[] c = new Node[26]; boolean end; }
class StreamChecker {
    Node root = new Node();
    StringBuilder stream = new StringBuilder();
    public StreamChecker(String[] words) {
        for (String w : words) {
            Node cur = root;
            for (int i = w.length() - 1; i >= 0; i--) {
                int idx = w.charAt(i) - 'a';
                if (cur.c[idx] == null) cur.c[idx] = new Node();
                cur = cur.c[idx];
            }
            cur.end = true;
        }
    }
    public boolean query(char letter) {
        stream.append(letter);
        Node cur = root;
        for (int i = stream.length() - 1; i >= 0; i--) {
            int idx = stream.charAt(i) - 'a';
            if (cur.c[idx] == null) return false;
            cur = cur.c[idx];
            if (cur.end) return true;
        }
        return false;
    }
}
```



<CodeTrace
  title="Reverse trie — dict [cd, f, kl]"
  :values="['a','b','c','d']"
  :windowKeys="['q']"
  :cellWidth="34"
  :steps='[
    { pointers: { q: 3 }, vars: { stream: "abcd", walk: "d→c", end: true }, note: "matches cd" }
  ]'
/>

**Complexity** — `query` **O(L_max)**; Space **O(D)**.

---

## Try it yourself

<JavaRunner problem-slug="stream-of-characters" />

## Complexity summary

| Approach | Time / query | Space | Grade |
|---|---|---|---|
| Naive suffix check | O(k · #dict) | O(D) | baseline |
| Reverse trie + suffix walk | **O(L_max)** | O(D) | canonical |

## When to use which

- **"Last-k suffix matching"** in streams → reverse trie.
- **"Prefix" instead** → normal trie + walk forward.
- **Aho-Corasick** → optimal for very many patterns, streaming.

## Related problems

- [Implement Trie](/problems/implement-trie)
- [Word Search II](/problems/trie-word-search-ii)
- [Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/)