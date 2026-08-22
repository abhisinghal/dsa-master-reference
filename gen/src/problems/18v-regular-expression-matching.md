# DP — Regular Expression Matching

*[↗ LeetCode: Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

Match `s` against pattern `p` with `.` (any char) and `*` (0+ of previous char).

## Approach — 2D DP

**Insight.** `dp[i][j]` = whether `s[..i]` matches `p[..j]`.
- If `p[j-1] == '*'`:
  - **Zero occurrences**: `dp[i][j] = dp[i][j-2]`.
  - **One or more**: if `s[i-1]` matches `p[j-2]` (or `p[j-2] == '.'`), also `dp[i-1][j]`.
- Else if `s[i-1]` matches `p[j-1]`: `dp[i][j] = dp[i-1][j-1]`.

```java
boolean isMatch(String s, String p) {
    int m = s.length(), n = p.length();
    boolean[][] dp = new boolean[m + 1][n + 1];
    dp[0][0] = true;
    for (int j = 2; j <= n; j++)
        if (p.charAt(j - 1) == '*') dp[0][j] = dp[0][j - 2];
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++) {
            if (p.charAt(j - 1) == '*') {
                dp[i][j] = dp[i][j - 2];
                if (matches(s, p, i, j - 1)) dp[i][j] |= dp[i - 1][j];
            } else if (matches(s, p, i, j)) {
                dp[i][j] = dp[i - 1][j - 1];
            }
        }
    return dp[m][n];
}
boolean matches(String s, String p, int i, int j) {
    char sc = s.charAt(i - 1), pc = p.charAt(j - 1);
    return pc == '.' || pc == sc;
}
```

**Complexity** — Time **O(mn)**; Space **O(mn)** (can compress to O(n)).

## Related problems

- [Wildcard Matching](https://leetcode.com/problems/wildcard-matching/) — `?` and `*` = zero-or-more-any
- [Edit Distance](/problems/edit-distance)
