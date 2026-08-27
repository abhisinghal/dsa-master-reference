# DP — Longest Common Subsequence

*[↗ LeetCode: Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Meta, Amazon, Google, Adobe" />

Length of longest subsequence appearing in both strings.

**Example 1** — `text1="abcde", text2="ace"` → `3` ("ace")
**Example 2** — `text1="abc", text2="abc"` → `3`
**Example 3** — `text1="abc", text2="def"` → `0`

**Constraints** — `1 ≤ m, n ≤ 1000`. Brute recursion is O(2^(m+n)) — at m=n=25 that's 10¹⁵ ops. DP is O(mn) = 10⁶.


<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="longest-common-subsequence" /> <Bookmark problem-slug="longest-common-subsequence" />

<InterviewTimer problem-slug="longest-common-subsequence" />



## Approach 1 — Brute recursion

**Intuition.** At each position, either match (advance both) or skip in one string. Recurse; return max.



```java
int lcsBrute(String s1, String s2) {
    return dfs(s1, s2, 0, 0);
}
int dfs(String s1, String s2, int i, int j) {
    if (i == s1.length() || j == s2.length()) return 0;
    if (s1.charAt(i) == s2.charAt(j)) return 1 + dfs(s1, s2, i + 1, j + 1);
    return Math.max(dfs(s1, s2, i + 1, j), dfs(s1, s2, i, j + 1));
}
```



**Complexity** — Time **O(2^(m+n))**; Space **O(m+n)** stack. TLE past m+n=40. *In an interview* say "memoize on (i, j) — 2D state → O(mn)."

---

## Approach 2 — 2D DP (canonical)

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



<CodeTrace
  title="2D DP (canonical)"
  :values="['a', 'b', 'c', 'd', 'e']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 4 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(mn)**; Space **O(mn)** (compress to O(n)). *Say aloud in an interview:* "canonical 2-string DP shape — same skeleton as Edit Distance, Longest Palindromic Subsequence, Distinct Subsequences."

---

## Try it yourself

<JavaRunner problem-slug="longest-common-subsequence" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute recursion | O(2^(m+n)) | O(m+n) | Reference; TLE past m+n=40 |
| **2D DP** | **O(mn)** | O(mn) → O(n) | **Canonical** |

## When to use which

- **Standard LCS** → 2D DP.
- **Return the subsequence** → track predecessors.
- **LCS of 3+ strings** → nD DP.

<AiCompanion problem-slug="longest-common-subsequence" pattern-hint="dynamic programming" />

## Related problems

- [Edit Distance](/problems/edit-distance)
- [Longest Palindromic Subsequence](/problems/longest-palindromic-subsequence)
- [Shortest Common Supersequence](https://leetcode.com/problems/shortest-common-supersequence/)

<FeedbackWidget problem-slug="longest-common-subsequence" />

<RelatedProblems problems="palindrome-partitioning-ii::Palindrome Partitioning II|coin-change::Coin Change|unique-paths-ii::Unique Paths II" />
