# Trie — Word Search II

*[↗ LeetCode: Word Search II](https://leetcode.com/problems/word-search-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/trie-pattern)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Uber" />

Given `board[m][n]` of letters and a dictionary `words`, return all words in `words` that can be traced through adjacent cells (no cell reused within a single word).

**Example** — `board=[[o,a,a,n],[e,t,a,e],[i,h,k,r],[i,f,l,v]], words=["oath","pea","eat","rain"]` → `["oath","eat"]`

**Constraints** — `1 ≤ m, n ≤ 12`; up to 3·10⁴ words.


<Hints
  hint1="Prefix operations? Word set lookups? Autocomplete?"
  hint2="Each node has ≤ σ children (26 for lowercase). Walk char-by-char; create nodes on insert; check `end` flag on search."
  hint3="For XOR max: binary trie of 32-bit values; walk greedily choosing the opposite bit."
/>
---

<MarkSolved problem-slug="trie-word-search-ii" />


## Approach 1 — DFS per word

**Intuition.** For each word, DFS from every cell; return true if the whole word can be traced.

```java
List<String> findWordsBrute(char[][] b, String[] words) {
    List<String> res = new ArrayList<>();
    for (String w : words) if (exists(b, w)) res.add(w);
    return res;
}
// exists = classic Word Search I DFS. O(m·n·4^L) per word.
```

**Complexity** — Time **O(k · m·n · 4^L)** where `k = #words`, `L = max length`; Space **O(L)** stack.

At k=3·10⁴, L=10 this is astronomical. TLE.

---

## Approach 2 — DFS + pruning by common prefix (shared traversal)

**Intuition.** Many words share prefixes. Group them by prefix and traverse once per shared prefix.

But *managing shared prefixes explicitly* is exactly what a **trie** does — which is Approach 3.

---

## Approach 3 — Trie + one DFS pass

**Insight from brute.** Load all words into a trie. Now DFS from every cell **once**; at each step, check the child character in the trie. If absent, prune the whole subtree.

**Optimization** — mark a trie node's `word` field when we collect it, and set to `null` afterwards, so we don't collect duplicates.

**Trap** — restore the cell after DFS returns (Word Search discipline). Otherwise sibling paths can't reuse a cell.

```java
class TrieNode {
    Map<Character, TrieNode> ch = new HashMap<>();
    String word;                                 // set at end-of-word
}
List<String> findWords(char[][] b, String[] words) {
    TrieNode root = new TrieNode();
    for (String w : words) {
        TrieNode cur = root;
        for (char c : w.toCharArray()) cur = cur.ch.computeIfAbsent(c, k -> new TrieNode());
        cur.word = w;
    }
    List<String> out = new ArrayList<>();
    for (int r = 0; r < b.length; r++)
        for (int c = 0; c < b[0].length; c++)
            dfs(b, r, c, root, out);
    return out;
}
void dfs(char[][] b, int r, int c, TrieNode node, List<String> out) {
    if (r < 0 || r >= b.length || c < 0 || c >= b[0].length) return;
    char ch = b[r][c];
    TrieNode next = node.ch.get(ch);
    if (next == null) return;
    if (next.word != null) { out.add(next.word); next.word = null; }   // dedup
    b[r][c] = '#';
    dfs(b, r + 1, c, next, out); dfs(b, r - 1, c, next, out);
    dfs(b, r, c + 1, next, out); dfs(b, r, c - 1, next, out);
    b[r][c] = ch;
}
```

<CodeTrace
  title="Trie DFS finding &apos;oath&apos; on grid"
  :values="['o','a','t','h']"
  :windowKeys="['depth']"
  :cellWidth="46"
  :steps='[
    { pointers: { depth: 0 }, vars: { cell: "(0,0)=o", trie: "root→o exists" }, note: "dive", added: [0] },
    { pointers: { depth: 1 }, vars: { cell: "(0,1)=a", trie: "o→a exists" }, note: "continue", added: [0,1] },
    { pointers: { depth: 2 }, vars: { cell: "(1,1)=t", trie: "a→t" }, note: "continue", added: [0,1,2] },
    { pointers: { depth: 3 }, vars: { cell: "(1,0)=h", trie: "t→h.word=oath" }, note: "END → collect ‘oath‘", added: [0,1,2,3] },
    { pointers: { depth: 2 }, vars: { cell: "(1,1)→x", trie: "a→x?" }, note: "no x child → prune whole subtree" }
  ]'
/>

**Complexity** — Time **O(m·n · 4^L)** — the whole word list is walked in one traversal; Space **O(#chars in dict)** for the trie.

---

## Try it yourself

<JavaRunner problem-slug="trie-word-search-ii" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| DFS per word | O(k · m·n · 4^L) | O(L) |
| Trie + one DFS | **O(m·n · 4^L)** | O(dict) |

## When to use which

- **Many words, short board** → trie wins by orders of magnitude.
- **One word, big board** → plain DFS is fine.
- **Interviewer probes "any way to prune early?"** → the trie IS the pruner.

<AiCompanion problem-slug="trie-word-search-ii" pattern-hint="trie" />

## Related problems (same ladder applies)

- [Word Search I](https://leetcode.com/problems/word-search/) — one word, DFS only
- [Concatenated Words](https://leetcode.com/problems/concatenated-words/) — trie + DP
- [Replace Words](https://leetcode.com/problems/replace-words/) — trie for shortest root prefix
- [Stream of Characters](https://leetcode.com/problems/stream-of-characters/) — trie in reverse

<FeedbackWidget problem-slug="trie-word-search-ii" />
