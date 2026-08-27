# Trie — Concatenated Words

*[↗ LeetCode: Concatenated Words](https://leetcode.com/problems/concatenated-words/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/trie-pattern)

<CompanyTags companies="Amazon, Google, Meta" />

Given a list of distinct words, return all words that can be built as a concatenation of **at least two** shorter words from the same list.

**Example 1** — `words=["cat","cats","catsdogcats","dog","dogcatsdog","hippopotamuses","rat","ratcatdogcat"]` → `["catsdogcats","dogcatsdog","ratcatdogcat"]`
**Example 2** — `words=["a","b","ab","abc"]` → `["ab"]` (`a+b`; `abc` cannot use `c`)
**Example 3** — `words=["cat","dog"]` → `[]`

**Constraints** — `1 ≤ n ≤ 10⁴`; each word up to 30 chars. Brute per-word all-splits recursion is O(N·2^L) ≈ 10⁴·10⁹ = TLE. DP-per-word with dict is O(N·L²) ≤ 10⁴·900 ≈ 10⁷ ops = ~1s.


<Hints
  hint1="Prefix operations? Word set lookups? Autocomplete?"
  hint2="Each node has ≤ σ children (26 for lowercase). Walk char-by-char; create nodes on insert; check `end` flag on search."
  hint3="For XOR max: binary trie of 32-bit values; walk greedily choosing the opposite bit."
/>
---

<MarkSolved problem-slug="concatenated-words" /> <Bookmark problem-slug="concatenated-words" />

<InterviewTimer problem-slug="concatenated-words" />



## Approach 1 — Brute force per word

For each word, try all splits recursively; check dict membership. Exponential.

## Approach 2 — Trie + DFS memo (canonical)

**Insight.** Insert all words into a trie. For each word, DFS: walk trie tracking word-end positions; every time we hit an `end`, either finish or restart at root — count sub-words used.

Or (simpler) **DP + hashset**: `dp[i]` = true iff `word[0..i]` splits into dict words; check `dp[n]` with ≥ 2 splits.

```java
List<String> findAllConcatenatedWordsInADict(String[] words) {
    Set<String> dict = new HashSet<>(Arrays.asList(words));
    List<String> out = new ArrayList<>();
    for (String w : words)
        if (canFormFromOthers(w, dict, 0, 0)) out.add(w);
    return out;
}
boolean canFormFromOthers(String w, Set<String> dict, int start, int count) {
    if (start == w.length()) return count >= 2;
    for (int end = start + 1; end <= w.length(); end++) {
        String sub = w.substring(start, end);
        if (dict.contains(sub) && (start > 0 || !sub.equals(w))
            && canFormFromOthers(w, dict, end, count + 1)) return true;
    }
    return false;
}
```

<CodeTrace
  title="Brute force per word"
  :values="['cat', 'cats', 'catsdogcats', 'dog', 'dogcatsdog', 'hippopotamuses', 'rat', 'ratcatdogcat']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 4 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 7 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(N · L² )**; Space **O(N · L)**.

---

## Try it yourself

<JavaRunner problem-slug="concatenated-words" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute recursion | exponential | O(N) | baseline |
| Trie / DP + hashset | **O(N · L²)** | O(N · L) | canonical |

## When to use which

- **Word segmentation problems** → DP + hashset.
- **Trie** wins when dict lookups dominate.
- **"Return the segmentations"** → recurse and collect paths.

<AiCompanion problem-slug="concatenated-words" pattern-hint="trie" />

## Related problems

- [Word Break](https://leetcode.com/problems/word-break/)
- [Word Break II](https://leetcode.com/problems/word-break-ii/)
- [Longest Word in Dictionary](https://leetcode.com/problems/longest-word-in-dictionary/)

<FeedbackWidget problem-slug="concatenated-words" />

<RelatedProblems problems="word-search-ii::Word Search II|design-add-and-search-words-data-structure::Design Add And Search Words Data Structure|trie-word-search-ii::Trie Word Search II" />
