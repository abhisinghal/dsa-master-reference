# DP — Palindrome Partitioning II

*[↗ LeetCode: Palindrome Partitioning II](https://leetcode.com/problems/palindrome-partitioning-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

Minimum cuts so every part of `s` is a palindrome.

## Approach — Two DPs (pal[i][j] + cuts[i])

**Insight.**
1. Precompute `pal[i][j]` = whether `s[i..j]` is palindrome — DP in O(n²).
2. `cuts[i]` = min cuts to partition `s[0..i]`. If `s[0..i]` is palindrome, cuts[i] = 0. Else `cuts[i] = min(cuts[j] + 1)` over all `j` with `s[j+1..i]` palindrome.



```java
int minCut(String s) {
    int n = s.length();
    boolean[][] pal = new boolean[n][n];
    for (int i = n - 1; i >= 0; i--)
        for (int j = i; j < n; j++)
            if (s.charAt(i) == s.charAt(j) && (j - i < 2 || pal[i + 1][j - 1]))
                pal[i][j] = true;
    int[] cuts = new int[n];
    for (int i = 0; i < n; i++) {
        if (pal[0][i]) { cuts[i] = 0; continue; }
        cuts[i] = i;
        for (int j = 0; j < i; j++)
            if (pal[j + 1][i]) cuts[i] = Math.min(cuts[i], cuts[j] + 1);
    }
    return cuts[n - 1];
}
```



**Complexity** — Time **O(n²)**; Space **O(n²)**.

## Related problems

- [Palindrome Partitioning](/problems/palindrome-partitioning) — enumerate all
- [Longest Palindromic Subsequence](/problems/longest-palindromic-subsequence)
- [Word Break](https://leetcode.com/problems/word-break/) — same "cut-DP" style
