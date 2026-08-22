# DP — Longest Common Subsequence

*[↗ LeetCode: Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Length of the longest subsequence appearing in both strings.

## Approach — 2D DP

**Insight.** `dp[i][j]` = LCS of `s1[..i]` and `s2[..j]`.
- If `s1[i-1] == s2[j-1]`: `dp[i][j] = 1 + dp[i-1][j-1]`.
- Else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.



```java
int longestCommonSubsequence(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++)
            dp[i][j] = s1.charAt(i - 1) == s2.charAt(j - 1)
                    ? dp[i - 1][j - 1] + 1
                    : Math.max(dp[i - 1][j], dp[i][j - 1]);
    return dp[m][n];
}
```



**Complexity** — Time **O(mn)**; Space **O(mn)**; can compress to **O(n)** with two rows.

## Related problems

- [Edit Distance](/problems/edit-distance) — sibling DP
- [Longest Palindromic Subsequence](/problems/longest-palindromic-subsequence) — LCS of `s` and `reverse(s)`
- [Shortest Common Supersequence](https://leetcode.com/problems/shortest-common-supersequence/)
