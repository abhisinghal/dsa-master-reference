# Trie — Replace Words

*[↗ LeetCode: Replace Words](https://leetcode.com/problems/replace-words/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/trie-pattern)

<CompanyTags companies="Meta, Amazon, Google" />

Given a dictionary of roots and a `sentence`, replace each word with its **shortest** root that is a prefix. If no root, keep the word.

**Example 1** — `dict=["cat","bat","rat"], sentence="the cattle was rattled by the battery"` → `"the cat was rat by the bat"`

**Constraints** — dict ≤ 1000 roots; sentence words ≤ 1000.


<Hints
  hint1="Prefix operations? Word set lookups? Autocomplete?"
  hint2="Each node has ≤ σ children (26 for lowercase). Walk char-by-char; create nodes on insert; check `end` flag on search."
  hint3="For XOR max: binary trie of 32-bit values; walk greedily choosing the opposite bit."
/>
---

<MarkSolved problem-slug="replace-words" />


## Approach 1 — HashSet + prefix scan

For each word, try prefixes of length 1..L; first match wins. O(word · L²) per word.

## Approach 2 — Trie (canonical)

**Insight.** Insert all roots into a trie. For each word, walk the trie char-by-char; stop at first `end` node — that's the shortest prefix.

```java
class Node { Node[] c = new Node[26]; String word; }

String replaceWords(List<String> dict, String sentence) {
    Node root = new Node();
    for (String r : dict) {
        Node cur = root;
        for (char ch : r.toCharArray()) {
            int i = ch - 'a';
            if (cur.c[i] == null) cur.c[i] = new Node();
            cur = cur.c[i];
        }
        cur.word = r;
    }
    StringBuilder sb = new StringBuilder();
    for (String w : sentence.split(" ")) {
        if (sb.length() > 0) sb.append(' ');
        Node cur = root;
        String replacement = w;
        for (char ch : w.toCharArray()) {
            int i = ch - 'a';
            if (cur.c[i] == null) break;
            cur = cur.c[i];
            if (cur.word != null) { replacement = cur.word; break; }
        }
        sb.append(replacement);
    }
    return sb.toString();
}
```

<CodeTrace
  title="HashSet + prefix scan"
  :values="['cat', 'bat', 'rat']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(D + S)** where D = total root chars, S = sentence chars; Space **O(D)**.

---

## Try it yourself

<JavaRunner problem-slug="replace-words" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| HashSet + prefix scan | O(S · L²) | O(D) | works but wasteful |
| Trie | **O(D + S)** | O(D) | canonical |

## When to use which

- **Many words, many prefix lookups** → trie.
- **Longest prefix instead** → don't break early; track deepest `end`.
- **"Any prefix in dict"** → return boolean at first end.

<AiCompanion problem-slug="replace-words" pattern-hint="trie" />

## Related problems

- [Longest Word in Dictionary](https://leetcode.com/problems/longest-word-in-dictionary/)
- [Implement Trie](/problems/implement-trie)
- [Word Break](https://leetcode.com/problems/word-break/) — DP with trie option

<FeedbackWidget problem-slug="replace-words" />
