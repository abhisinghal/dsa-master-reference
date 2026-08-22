# Prefix Sum — Count Submatrices With Target Sum

*[↗ LeetCode: Count Submatrices With Target Sum](https://leetcode.com/problems/number-of-submatrices-that-sum-to-target/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/prefix-sum)

Count submatrices whose sum equals `target`.

---

## Approach 1 — Row prefix + 1D subarray-sum-K
**Insight.** Fix two rows `r1, r2`. Compress the column-sums between them into a 1D array; then count subarrays with sum = target using the hash-map prefix-sum trick.

```java
int numSubmatrixSumTarget(int[][] mat, int target) {
    int m = mat.length, n = mat[0].length;
    // rowsum[r][c] = sum of mat[0..r][c] prefix-by-row
    int[][] R = new int[m][n];
    for (int c = 0; c < n; c++) { int s = 0; for (int r = 0; r < m; r++) { s += mat[r][c]; R[r][c] = s; } }
    int count = 0;
    for (int r1 = 0; r1 < m; r1++)
        for (int r2 = r1; r2 < m; r2++) {
            Map<Integer, Integer> map = new HashMap<>();
            map.put(0, 1);
            int prefix = 0;
            for (int c = 0; c < n; c++) {
                int colSum = R[r2][c] - (r1 > 0 ? R[r1 - 1][c] : 0);
                prefix += colSum;
                count += map.getOrDefault(prefix - target, 0);
                map.merge(prefix, 1, Integer::sum);
            }
        }
    return count;
}
```

**Complexity** — Time **O(m²·n)**; Space **O(n)** per pair.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Row prefix + 1D subarray-sum-K | O(m²·n) | O(n) | primary |

## When to use which

- **Ship this** → Row prefix + 1D subarray-sum-K (O(m²·n), O(n)). The pattern's standard solution.

## Related problems

- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k) — 1D building block
- [Matrix Block Sum](/problems/matrix-block-sum)
- [Range Sum Query 2D — Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/)
