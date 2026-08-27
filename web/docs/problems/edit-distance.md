# Dynamic Programming — Edit Distance

*[↗ LeetCode: Edit Distance](https://leetcode.com/problems/edit-distance/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Uber" />

Given two strings `word1` and `word2`, return the minimum number of edits (insert, delete, replace) to convert `word1` → `word2`.

**Example 1** — `word1="horse", word2="ros"` → `3`
**Example 2** — `word1="intention", word2="execution"` → `5`

**Constraints** — `0 ≤ m, n ≤ 500`. Brute recursion is O(3^max(m,n)) — at m=n=500 that's ~7·10²³⁸ (dead universes). 2D DP is O(m·n) = 2.5·10⁶ ops = &lt;30 ms; compressed to O(min(m,n)) space.
<Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="edit-distance" /> <Bookmark problem-slug="edit-distance" />

<InterviewTimer problem-slug="edit-distance" />



## Approach 1 — Brute recursion → Approach 2 — Memoized

Same skeleton as Coin Change / House Robber. At `(i, j)`: if chars match, `f(i-1, j-1)`; else `1 + min(insert, delete, replace)`. Brute is exponential; memoization brings it to O(m·n).

## Approach 3 — Bottom-up DP



```java
int minDistance(String a, String b) {
    int m = a.length(), n = b.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++) {
            if (a.charAt(i - 1) == b.charAt(j - 1))
                dp[i][j] = dp[i - 1][j - 1];
            else
                dp[i][j] = 1 + Math.min(dp[i - 1][j], Math.min(dp[i][j - 1], dp[i - 1][j - 1]));
        }
    return dp[m][n];
}
```



<CodeTrace
  title="Edit Distance — word1=&quot;horse&quot;, word2=&quot;ros&quot;"
  :values="['h','o','r','s','e']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 1, j: 1 }, vars: { "dp[1][1]": 1, "h vs r": "mismatch" }, note: "1 + min(1,1,0) = 1" },
    { pointers: { i: 2, j: 2 }, vars: { "dp[2][2]": 1, "o vs o": "match" }, note: "= dp[1][1] = 1" },
    { pointers: { i: 3, j: 3 }, vars: { "dp[3][3]": 2, "r vs s": "mismatch" }, note: "1 + min(2,2,1) = 2" },
    { pointers: { i: 5, j: 3 }, vars: { "dp[5][3]": 3 }, note: "final = 3 (delete h, r→s, delete e)", added: [0,2,4] }
  ]'
/>

**Complexity** — Time **O(m·n)**; Space **O(m·n)** (reducible to **O(min(m,n))** with rolling row).

## Try it yourself

<JavaRunner problem-slug="edit-distance" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute recursion | O(3^(m+n)) | O(m+n) |
| Memoized | O(m·n) | O(m·n) |
| Tabulated | **O(m·n)** | O(m·n) |
| Rolling row | O(m·n) | **O(min(m,n))** |

## When to use which

- **Standard edit distance** → 2D DP.
- **Only insertions allowed** → LCS variant.
- **Return the operations** → track parent choices during DP.

<AiCompanion problem-slug="edit-distance" pattern-hint="dynamic programming" />

## Related problems

- [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) — same shape, different recurrence
- [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) — count matches instead
- [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) — same 2D table skeleton

<FeedbackWidget problem-slug="edit-distance" />

<RelatedProblems problems="min-cost-climbing-stairs::Min Cost Climbing Stairs|maximal-square::Maximal Square|coin-change-ii::Coin Change II" />
