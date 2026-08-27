# DP — Palindrome Partitioning II

*[↗ LeetCode: Palindrome Partitioning II](https://leetcode.com/problems/palindrome-partitioning-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Google, Amazon, Meta" />

Min cuts so every part of `s` is palindrome.

**Example 1** — `s="aab"` → `1` (`aa | b`)
**Example 2** — `s="a"` → `0`
**Example 3** — `s="ab"` → `1`

**Constraints** — `1 ≤ n ≤ 2000`. Brute recursive-split is O(2ⁿ) — 10⁶⁰⁰ ops at n=2000, TLE past n=25. Two-DP is O(n²) = 4·10⁶ ops = ~50ms.


<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="palindrome-partitioning-ii" /> <Bookmark problem-slug="palindrome-partitioning-ii" />

<InterviewTimer problem-slug="palindrome-partitioning-ii" />



## Approach 1 — Brute recursive split

**Intuition.** Try every cut position; recurse on the right side. O(2ⁿ) partitions.

**Complexity** — Time **O(2ⁿ)**; Space **O(n)** stack. TLE past n=25. *In an interview* say "precompute pal[i][j] with 2D DP, then compute cuts[i] as 1D DP → O(n²)."

---

## Approach 2 — Two DPs (canonical)

**Insight.**
1. Precompute `pal[i][j]` = whether `s[i..j]` palindrome (interval DP).
2. `cuts[i]` = min cuts for `s[0..i]`. If `pal[0][i]`, 0; else `min(cuts[j] + 1)` over `j` with `pal[j+1][i]`.



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

**Complexity** — Time **O(n²)**; Space **O(n²)**. *Say aloud in an interview:* "interval DP for palindrome table + linear DP over prefixes — canonical 2-stage pattern."

---

## Try it yourself

<JavaRunner problem-slug="palindrome-partitioning-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute split | O(2ⁿ) | O(n) | TLE past n=25 |
| **Two-stage DP** | **O(n²)** | O(n²) | **Canonical** |

## When to use which

- **Min cuts** → this.
- **Enumerate partitions** → [Palindrome Partitioning I](/problems/palindrome-partitioning).
- **Longest palindrome** → LPS DP.

<AiCompanion problem-slug="palindrome-partitioning-ii" pattern-hint="dynamic programming" />

## Related problems

- [Palindrome Partitioning](/problems/palindrome-partitioning)
- [Longest Palindromic Subsequence](/problems/longest-palindromic-subsequence)

<FeedbackWidget problem-slug="palindrome-partitioning-ii" />

<RelatedProblems problems="longest-palindromic-subsequence::Longest Palindromic Subsequence|min-cost-climbing-stairs::Min Cost Climbing Stairs|partition-equal-subset-sum::Partition Equal Subset Sum" />
