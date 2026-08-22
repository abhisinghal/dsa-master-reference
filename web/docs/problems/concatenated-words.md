# Trie — Concatenated Words

*[↗ LeetCode: Concatenated Words](https://leetcode.com/problems/concatenated-words/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/trie-pattern)

Return all words in the dictionary that are concatenations of **two or more** other words in the dictionary.

## Approach — Sort by length + DP with trie / word-set

**Insight.** Sort words shortest-first. For each word, check if it can be split into ≥ 2 shorter dictionary words using DP (Word Break style). Use a hash set of words seen so far.



```java
List<String> findAllConcatenatedWordsInADict(String[] words) {
    Arrays.sort(words, (a, b) -> a.length() - b.length());
    Set<String> dict = new HashSet<>();
    List<String> out = new ArrayList<>();
    for (String w : words) {
        if (canForm(w, dict)) out.add(w);
        dict.add(w);
    }
    return out;
}
boolean canForm(String w, Set<String> dict) {
    if (dict.isEmpty()) return false;
    boolean[] dp = new boolean[w.length() + 1];
    dp[0] = true;
    for (int i = 1; i <= w.length(); i++)
        for (int j = 0; j < i; j++)
            if (dp[j] && dict.contains(w.substring(j, i))) { dp[i] = true; break; }
    return dp[w.length()];
}
```



**Complexity** — Time **O(N · L²)** where L = max length; Space **O(N + L)**.

**Alternative** — build a trie for O(L²) per word using trie-walk instead of substring lookup.

## Related problems

- [Word Break](https://leetcode.com/problems/word-break/) — single-word variant
- [Word Break II](https://leetcode.com/problems/word-break-ii/) — return all sentences
- [Word Search II](/problems/trie-word-search-ii)
