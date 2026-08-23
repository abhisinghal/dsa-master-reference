# Trie — Concatenated Words

*[↗ LeetCode: Concatenated Words](https://leetcode.com/problems/concatenated-words/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/trie-pattern)

Given a list of distinct words, return all words that can be built as a concatenation of **at least two** shorter words from the same list.

**Example 1** — `words=["cat","cats","catsdogcats","dog","dogcatsdog","hippopotamuses","rat","ratcatdogcat"]` → `["catsdogcats","dogcatsdog","ratcatdogcat"]`

**Constraints** — `1 ≤ n ≤ 10⁴`.

---

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



**Complexity** — Time **O(N · L² )**; Space **O(N · L)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute recursion | exponential | O(N) | baseline |
| Trie / DP + hashset | **O(N · L²)** | O(N · L) | canonical |

## When to use which

- **Word segmentation problems** → DP + hashset.
- **Trie** wins when dict lookups dominate.
- **"Return the segmentations"** → recurse and collect paths.

## Related problems

- [Word Break](https://leetcode.com/problems/word-break/)
- [Word Break II](https://leetcode.com/problems/word-break-ii/)
- [Longest Word in Dictionary](https://leetcode.com/problems/longest-word-in-dictionary/)
