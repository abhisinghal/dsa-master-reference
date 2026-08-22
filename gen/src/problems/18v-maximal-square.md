# DP — Maximal Square

*[↗ LeetCode: Maximal Square](https://leetcode.com/problems/maximal-square/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Largest all-ones square in a binary matrix. Return area.

## Approach — DP `side[i][j]` = largest square ending at (i, j)

**Insight.** If `mat[i][j] == '1'`:
`side[i][j] = 1 + min(side[i-1][j], side[i][j-1], side[i-1][j-1])`.

**Why min of three.** The square ending at (i,j) is limited by the shortest of the squares ending at the three neighbors — otherwise a zero would intrude.

```java
int maximalSquare(char[][] mat) {
    int m = mat.length, n = mat[0].length, best = 0;
    int[] dp = new int[n + 1];
    int prev = 0;
    for (int i = 1; i <= m; i++) {
        prev = 0;
        for (int j = 1; j <= n; j++) {
            int tmp = dp[j];
            if (mat[i - 1][j - 1] == '1') {
                dp[j] = 1 + Math.min(dp[j], Math.min(dp[j - 1], prev));
                best = Math.max(best, dp[j]);
            } else dp[j] = 0;
            prev = tmp;
        }
    }
    return best * best;
}
```

**Complexity** — Time **O(mn)**; Space **O(n)**.

## Related problems

- [Maximal Rectangle](/problems/maximal-rectangle) — non-square, stack per row
- [Count Square Submatrices with All Ones](https://leetcode.com/problems/count-square-submatrices-with-all-ones/) — sum of side[i][j]
