# Prefix Sum — Matrix Block Sum

*[↗ LeetCode: Matrix Block Sum](https://leetcode.com/problems/matrix-block-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

For each `(i, j)`, return the sum of `mat[r][c]` over all `(r, c)` with `|r-i| ≤ k` and `|c-j| ≤ k`.

## Approach — 2D prefix sums

Precompute `P[i+1][j+1] = sum(mat[0..i][0..j])`. Any block sum via inclusion-exclusion: `P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]`.



```java
int[][] matrixBlockSum(int[][] mat, int k) {
    int m = mat.length, n = mat[0].length;
    int[][] P = new int[m + 1][n + 1];
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            P[i + 1][j + 1] = P[i][j + 1] + P[i + 1][j] - P[i][j] + mat[i][j];
    int[][] out = new int[m][n];
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) {
            int r1 = Math.max(0, i - k), c1 = Math.max(0, j - k);
            int r2 = Math.min(m - 1, i + k), c2 = Math.min(n - 1, j + k);
            out[i][j] = P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1];
        }
    return out;
}
```



**Complexity** — Time **O(m·n)**; Space **O(m·n)** for the prefix table.

## Related problems

- [Range Sum Query 2D — Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/) — same prefix table
- [Count Submatrices With Target Sum](/problems/count-submatrices-with-target-sum)
- [Maximal Rectangle](/problems/maximal-rectangle)
