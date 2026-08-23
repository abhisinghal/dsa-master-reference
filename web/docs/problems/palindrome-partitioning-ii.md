# DP — Palindrome Partitioning II

*[↗ LeetCode: Palindrome Partitioning II](https://leetcode.com/problems/palindrome-partitioning-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

&lt;CompanyTags companies="Google, Amazon, Meta" /&gt;

Min cuts so every part of `s` is palindrome.

**Example 1** — `s="aab"` → `1`
**Example 2** — `s="a"` → `0`
**Example 3** — `s="ab"` → `1`

**Constraints** — `1 ≤ n ≤ 2000`.


&lt;Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/&gt;
---

## Approach — Two DPs (canonical)

**Insight.**
1. Precompute `pal[i][j]` = whether `s[i..j]` palindrome.
2. `cuts[i]` = min cuts for `s[0..i]`. If `pal[0][i]`, 0; else `min(cuts[j] + 1)` for `j` with `pal[j+1][i]`.



```java
int minCut(String s) {
    int n = s.length();
    boolean[][] pal = new boolean[n][n];
    for (int i = n - 1; i >= 0; i--)
        for (int j = i; j < n; j++)
            if (s.charAt(i) == s.charAt(j) && (j - i < 2 || pal[i+1][j-1]))
                pal[i][j] = true;
    int[] cuts = new int[n];
    for (int i = 0; i < n; i++) {
        if (pal[0][i]) { cuts[i] = 0; continue; }
        cuts[i] = i;
        for (int j = 0; j < i; j++)
            if (pal[j+1][i]) cuts[i] = Math.min(cuts[i], cuts[j] + 1);
    }
    return cuts[n-1];
}
```



<CodeTrace
  title="Two DPs (canonical)"
  :values="['a', 'a', 'b']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n²)**; Space **O(n²)**.

---

## Try it yourself

<JavaRunner problem-slug="palindrome-partitioning-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Two-stage DP | **O(n²)** | O(n²) | canonical |

## When to use which

- **Min cuts** → this.
- **Enumerate partitions** → [Palindrome Partitioning I](/problems/palindrome-partitioning).
- **Longest palindrome** → LPS DP.

&lt;AiCompanion problem-slug="palindrome-partitioning-ii" pattern-hint="dynamic programming" /&gt;

## Related problems

- [Palindrome Partitioning](/problems/palindrome-partitioning)
- [Longest Palindromic Subsequence](/problems/longest-palindromic-subsequence)

&lt;FeedbackWidget problem-slug="palindrome-partitioning-ii" /&gt;
