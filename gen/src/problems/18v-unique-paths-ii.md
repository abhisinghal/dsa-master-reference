# DP — Unique Paths II

*[↗ LeetCode: Unique Paths II](https://leetcode.com/problems/unique-paths-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Meta, Amazon, Google" />

Grid with obstacles. Count paths from top-left to bottom-right (right/down).

**Example 1** — `[[0,0,0],[0,1,0],[0,0,0]]` → `2`
**Example 2** — `[[0,1],[0,0]]` → `1`

**Constraints** — `1 ≤ m, n ≤ 100`.


<Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="unique-paths-ii" />


## Approach — Grid DP with obstacle guard (canonical)

**Insight.** `dp[i][j] = 0` if obstacle; else `dp[i-1][j] + dp[i][j-1]`.

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

**Complexity** — Time **O(mn)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="unique-paths-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| 1D compressed DP | **O(mn)** | O(n) | canonical |

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
