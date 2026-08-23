# DP — Longest Palindromic Subsequence

*[↗ LeetCode: Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

&lt;CompanyTags companies="Amazon, Google, Meta" /&gt;

Length of longest palindromic subsequence.

**Example 1** — `s="bbbab"` → `4`
**Example 2** — `s="cbbd"` → `2`

**Constraints** — `1 ≤ n ≤ 1000`.


&lt;Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/&gt;
---

&lt;MarkSolved problem-slug="longest-palindromic-subsequence" /&gt;


## Approach 1 — LCS(s, reverse(s))
O(n²) — quick way.

## Approach 2 — Interval DP (canonical)

**Insight.** `dp[i][j]` = LPS length in `s[i..j]`.



```java
int longestPalindromeSubseq(String s) {
    int n = s.length();
    int[][] dp = new int[n][n];
    for (int i = n - 1; i >= 0; i--) {
        dp[i][i] = 1;
        for (int j = i + 1; j < n; j++) {
            if (s.charAt(i) == s.charAt(j))
                dp[i][j] = dp[i+1][j-1] + 2;
            else
                dp[i][j] = Math.max(dp[i+1][j], dp[i][j-1]);
        }
    }
    return dp[0][n-1];
}
```



<CodeTrace
  title="LCS(s, reverse(s))"
  :values="['b', 'b', 'b', 'a', 'b']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 4 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Corollary.** Min insertions to make s palindrome = `n - LPS(s)`.

**Complexity** — Time **O(n²)**; Space **O(n²)**.

---

## Try it yourself

<JavaRunner problem-slug="longest-palindromic-subsequence" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| LCS(s, rev) | O(n²) | O(n²) | works |
| Interval DP | **O(n²)** | O(n²) | canonical |

## When to use which

- **Standard LPS** → interval DP.
- **Min insertions to palindrome** → same DP.
- **Longest palindromic *substring*** → different — see [Longest Palindromic Substring](/problems/longest-palindromic-substring).

&lt;AiCompanion problem-slug="longest-palindromic-subsequence" pattern-hint="dynamic programming" /&gt;

## Related problems

- [Longest Common Subsequence](/problems/longest-common-subsequence)
- [Palindrome Partitioning II](/problems/palindrome-partitioning-ii)

&lt;FeedbackWidget problem-slug="longest-palindromic-subsequence" /&gt;

&lt;RelatedProblems problems="maximal-square::Maximal Square|delete-and-earn::Delete And Earn|climbing-stairs::Climbing Stairs" /&gt;
