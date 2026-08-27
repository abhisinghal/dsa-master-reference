# DP — Unique Paths II

*[↗ LeetCode: Unique Paths II](https://leetcode.com/problems/unique-paths-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Meta, Amazon, Google" />

Grid with obstacles. Count paths from top-left to bottom-right (right/down).

**Example 1** — `[[0,0,0],[0,1,0],[0,0,0]]` → `2` (go around the center obstacle two ways)
**Example 2** — `[[0,1],[0,0]]` → `1`
**Example 3** — `[[1]]` → `0` (start blocked)

**Constraints** — `1 ≤ m, n ≤ 100`. Brute DFS is exponential (~2^(m+n) ≈ 10⁶⁰ at m=n=100). DP is O(mn) = 10⁴.


<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="unique-paths-ii" /> <Bookmark problem-slug="unique-paths-ii" />

<InterviewTimer problem-slug="unique-paths-ii" />



## Approach 1 — Brute DFS

**Intuition.** From each cell try both moves (right, down); count paths that reach the end without stepping on obstacles.

**Complexity** — Time **O(2^(m+n))**; Space **O(m+n)** stack. TLE past 15×15. *In an interview* say "many overlapping subpaths — memoize on (i, j) → O(mn)."

---

## Approach 2 — Grid DP with obstacle guard (canonical)

**Insight.** `dp[i][j] = 0` if obstacle; else `dp[i-1][j] + dp[i][j-1]`. Compressed to a single row.

```java
int uniquePathsWithObstacles(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    int[] dp = new int[n];
    dp[0] = grid[0][0] == 0 ? 1 : 0;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == 1) dp[j] = 0;
            else if (j > 0) dp[j] += dp[j - 1];
        }
    return dp[n - 1];
}
```

<CodeTrace
  title="Grid DP with obstacle guard (canonical)"
  :values="['0', '0', '0']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(mn)**; Space **O(n)**. *Say aloud in an interview:* "standard grid-DP skeleton — same as Unique Paths, Min Path Sum, and Dungeon Game (reverse direction)."

---

## Try it yourself

<JavaRunner problem-slug="unique-paths-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute DFS | O(2^(m+n)) | O(m+n) | TLE past 15×15 |
| **1D compressed DP** | **O(mn)** | O(n) | **Canonical** |

## When to use which

- **Count paths** → this DP.
- **Return path** → track predecessors.
- **Min sum instead** → same shape, min not add.

<AiCompanion problem-slug="unique-paths-ii" pattern-hint="dynamic programming" />

## Related problems

- [Unique Paths](https://leetcode.com/problems/unique-paths/)
- [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/)
- [Minimum Falling Path Sum](/problems/minimum-falling-path-sum)

<FeedbackWidget problem-slug="unique-paths-ii" />

<RelatedProblems problems="palindrome-partitioning-ii::Palindrome Partitioning II|min-cost-climbing-stairs::Min Cost Climbing Stairs|coin-change::Coin Change" />
