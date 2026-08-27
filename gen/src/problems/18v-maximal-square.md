# DP — Maximal Square

*[↗ LeetCode: Maximal Square](https://leetcode.com/problems/maximal-square/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google, Meta, Uber" />

Largest square of `1`s in binary matrix. Return area.

**Example 1** — `matrix=[["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]` → `4` (a 2×2 square)
**Example 2** — `matrix=[["0","1"],["1","0"]]` → `1`
**Example 3** — `matrix=[["0"]]` → `0`

**Constraints** — `1 ≤ m, n ≤ 300`. Brute per-cell BFS is O((mn)²) = 8·10⁹ ops at 300×300. DP is O(mn) = 9·10⁴ — 90,000× faster.


<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="maximal-square" /> <Bookmark problem-slug="maximal-square" />

<InterviewTimer problem-slug="maximal-square" />



## Approach 1 — Brute force per-cell expand

**Intuition.** For each cell `(i, j)` with `mat[i][j] == '1'`, try squares of size 1, 2, 3, ..., checking all cells in each candidate square.

```java
int maximalSquareBrute(char[][] mat) {
    int m = mat.length, n = mat[0].length, best = 0;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (mat[i][j] == '1') {
                int s = 1;
                while (i + s < m && j + s < n && allOnes(mat, i, j, s)) s++;
                best = Math.max(best, s);
            }
    return best * best;
}
boolean allOnes(char[][] m, int i, int j, int s) {
    for (int r = i; r <= i + s; r++)
        for (int c = j; c <= j + s; c++)
            if (m[r][c] != '1') return false;
    return true;
}
```

**Complexity** — Time **O((mn)²)**; Space **O(1)**. For 300×300: 8·10⁹ ops = TLE. *In an interview* state this then flip to DP.

---

## Approach 2 — DP `side[i][j]` = largest square ending at (i, j) (canonical)

**Insight.** Define `side[i][j]` = side length of the largest square whose *bottom-right corner* is at `(i, j)`. If `mat[i][j] == '1'`, the largest square there is bounded by the three neighbours already computed:

`side[i][j] = 1 + min(side[i-1][j], side[i][j-1], side[i-1][j-1])`

Take min of three — the tightest neighbour is the bottleneck. Rolling 1D array cuts space to O(n).

```java
int maximalSquare(char[][] mat) {
    int m = mat.length, n = mat[0].length, best = 0;
    int[] dp = new int[n + 1];
    int prev = 0;
    for (int i = 1; i <= m; i++) {
        prev = 0;
        for (int j = 1; j <= n; j++) {
            int tmp = dp[j];
            if (mat[i-1][j-1] == '1') {
                dp[j] = 1 + Math.min(dp[j], Math.min(dp[j-1], prev));
                best = Math.max(best, dp[j]);
            } else dp[j] = 0;
            prev = tmp;
        }
    }
    return best * best;
}
```

**Complexity** — Time **O(mn)**; Space **O(n)**. *Say aloud in an interview:* "min-of-3 neighbours = the tightest bottleneck. Same pattern in Longest Common Substring, Count Square Submatrices."

---

## Try it yourself

<JavaRunner problem-slug="maximal-square" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Per-cell expand | O((mn)²) | O(1) | Reference; TLE at 300×300 |
| **DP min-of-3** | **O(mn)** | O(n) | **Canonical** |

## When to use which

- **Only squares** → this DP.
- **Rectangles** → [Maximal Rectangle](/problems/maximal-rectangle) — row heights + stack.
- **Count all squares** → sum of `side[i][j]`.

<AiCompanion problem-slug="maximal-square" pattern-hint="dynamic programming" />

## Related problems

- [Maximal Rectangle](/problems/maximal-rectangle)
- [Count Square Submatrices](https://leetcode.com/problems/count-square-submatrices-with-all-ones/)

<FeedbackWidget problem-slug="maximal-square" />

<RelatedProblems problems="delete-and-earn::Delete And Earn|climbing-stairs::Climbing Stairs|regular-expression-matching::Regular Expression Matching" />
