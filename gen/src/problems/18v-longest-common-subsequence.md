# DP — Longest Common Subsequence

*[↗ LeetCode: Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Length of longest subsequence appearing in both strings.

**Example 1** — `text1="abcde", text2="ace"` → `3`
**Example 2** — `text1="abc", text2="abc"` → `3`
**Example 3** — `text1="abc", text2="def"` → `0`

**Constraints** — `1 ≤ m, n ≤ 1000`.

---

## Approach — 2D DP (canonical)

**Insight.** `dp[i][j]` = LCS of prefixes.
- Match → `dp[i-1][j-1] + 1`.
- Else → `max(dp[i-1][j], dp[i][j-1])`.

```java
int longestCommonSubsequence(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++)
            dp[i][j] = s1.charAt(i-1) == s2.charAt(j-1)
                ? dp[i-1][j-1] + 1
                : Math.max(dp[i-1][j], dp[i][j-1]);
    return dp[m][n];
}
```

**Complexity** — Time **O(mn)**; Space **O(mn)** (compress to O(n)).

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| 2D DP | **O(mn)** | O(mn) → O(n) | canonical |

## When to use which

- **Standard LCS** → 2D DP.
- **Return the subsequence** → track predecessors.
- **LCS of 3+ strings** → nD DP.

## Related problems

- [Edit Distance](/problems/edit-distance)
- [Longest Palindromic Subsequence](/problems/longest-palindromic-subsequence)
- [Shortest Common Supersequence](https://leetcode.com/problems/shortest-common-supersequence/)
