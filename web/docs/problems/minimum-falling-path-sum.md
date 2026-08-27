# DP — Minimum Falling Path Sum

*[↗ LeetCode: Minimum Falling Path Sum](https://leetcode.com/problems/minimum-falling-path-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google, Meta" />

Grid; falling path picks one cell per row; next row's cell must be in `[j-1, j, j+1]`. Min sum from top to bottom.

**Example 1** — `[[2,1,3],[6,5,4],[7,8,9]]` → `13` (path 1→4→8 = 13)
**Example 2** — `[[-19,57],[-40,-5]]` → `-59` (path -19→-40)
**Example 3** — `[[7]]` → `7` (single cell)

**Constraints** — `1 ≤ n ≤ 100`. Brute enumerate paths is 3ⁿ⁻¹ — at n=25 that's ~10¹² ops. DP is O(n²) = 10⁴.


<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="minimum-falling-path-sum" /> <Bookmark problem-slug="minimum-falling-path-sum" />

<InterviewTimer problem-slug="minimum-falling-path-sum" />



## Approach 1 — Brute recursion

**Intuition.** At each cell, recurse into the three next-row candidates. Return min over all top-row starts.



```java
int minFallingPathSumBrute(int[][] g) {
    int best = Integer.MAX_VALUE;
    for (int j = 0; j < g[0].length; j++) best = Math.min(best, dfs(g, 0, j));
    return best;
}
int dfs(int[][] g, int i, int j) {
    if (j < 0 || j >= g[0].length) return Integer.MAX_VALUE / 2;
    if (i == g.length - 1) return g[i][j];
    int down = dfs(g, i + 1, j);
    int dl = dfs(g, i + 1, j - 1);
    int dr = dfs(g, i + 1, j + 1);
    return g[i][j] + Math.min(down, Math.min(dl, dr));
}
```



**Complexity** — Time **O(3ⁿ)**; Space **O(n)** stack. At n=25 = 8·10¹¹ ops. TLE. *In an interview* say "memoize on (row, col) → O(n²)."

---

## Approach 2 — Row-by-row DP (canonical)

**Insight.** `dp[i][j] = grid[i][j] + min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1])`. Each row only depends on the previous row → roll to 1D.



```java
int minFallingPathSum(int[][] grid) {
    int n = grid.length;
    int[] prev = grid[0].clone();
    for (int i = 1; i < n; i++) {
        int[] cur = new int[n];
        for (int j = 0; j < n; j++) {
            int m = prev[j];
            if (j > 0) m = Math.min(m, prev[j-1]);
            if (j < n-1) m = Math.min(m, prev[j+1]);
            cur[j] = grid[i][j] + m;
        }
        prev = cur;
    }
    int best = Integer.MAX_VALUE;
    for (int v : prev) best = Math.min(best, v);
    return best;
}
```



<CodeTrace
  title="Row-by-row DP (canonical)"
  :values="['2', '1', '3']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n²)**; Space **O(n)**. *Say aloud in an interview:* "grid-path DP with limited transitions — same shape as Minimum Path Sum, Triangle, Dungeon Game."

---

## Try it yourself

<JavaRunner problem-slug="minimum-falling-path-sum" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute recursion | O(3ⁿ) | O(n) | Reference; TLE at n=25 |
| **Row-by-row DP** | **O(n²)** | O(n) | **Canonical** |

## When to use which

- **Row-only transitions** → 1D rolling.
- **Diagonal-only transitions** → [Triangle](https://leetcode.com/problems/triangle/).

<AiCompanion problem-slug="minimum-falling-path-sum" pattern-hint="dynamic programming" />

## Related problems

- [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/)
- [Triangle](https://leetcode.com/problems/triangle/)
- [Dungeon Game](/problems/dungeon-game)

<FeedbackWidget problem-slug="minimum-falling-path-sum" />
