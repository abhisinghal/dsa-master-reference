# DP — Longest Palindromic Subsequence

*[↗ LeetCode: Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Length of the longest subsequence of `s` that is a palindrome.

---

## Approach 1 — LCS(s, reverse(s))
O(n²).

---

## Approach 2 — Interval DP
**Insight.** `dp[i][j]` = LPS length in `s[i..j]`.
- `s[i]==s[j]`: `dp[i][j] = 2 + dp[i+1][j-1]` (with adjustment for i+1 > j-1).
- Else: `max(dp[i+1][j], dp[i][j-1])`.

Iterate over lengths, or iterate `i` descending and `j` ascending from `i`.

```java
int longestPalindromeSubseq(String s) {
    int n = s.length();
    int[][] dp = new int[n][n];
    for (int i = n - 1; i >= 0; i--) {
        dp[i][i] = 1;
        for (int j = i + 1; j < n; j++) {
            if (s.charAt(i) == s.charAt(j))
                dp[i][j] = dp[i + 1][j - 1] + 2;
            else
                dp[i][j] = Math.max(dp[i + 1][j], dp[i][j - 1]);
        }
    }
    return dp[0][n - 1];
}
```

**Complexity** — Time **O(n²)**; Space **O(n²)**.

**Corollary.** Minimum insertions to make `s` a palindrome = `n - LPS(s)` (deleted characters have palindromic siblings; leftover characters need insertions).

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| LCS(s, reverse(s)) | O(n²) | — | baseline |
| Interval DP | O(n²) | O(n²) | optimum |

## When to use which

- **State it for signal** → LCS(s, reverse(s)) (O(n²)). Correct baseline; call it out then move on.
- **Ship this** → Interval DP (O(n²), O(n²)). Expected optimum in interview.

## Related problems

- [Longest Common Subsequence](/problems/longest-common-subsequence)
- [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/)
- [Palindrome Partitioning II](/problems/palindrome-partitioning-ii)
