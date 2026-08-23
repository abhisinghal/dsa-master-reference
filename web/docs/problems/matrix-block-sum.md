# Prefix Sum — Matrix Block Sum

*[↗ LeetCode: Matrix Block Sum](https://leetcode.com/problems/matrix-block-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

&lt;CompanyTags companies="Google, Amazon" /&gt;

Given matrix `mat[m][n]` and integer `k`, return `answer[i][j]` = sum of all elements `mat[r][c]` with `|r-i| ≤ k` and `|c-j| ≤ k`.

**Example 1** — `mat=[[1,2,3],[4,5,6],[7,8,9]], k=1` → `[[12,21,16],[27,45,33],[24,39,28]]`
**Example 2** — `mat=[[1,2,3],[4,5,6],[7,8,9]], k=2` → `[[45,45,45],[45,45,45],[45,45,45]]`

**Constraints** — `1 ≤ m, n ≤ 100`; `1 ≤ k ≤ 100`.


&lt;Hints
  hint1="Ask: can I answer `sum(i, j)` in O(1) given a preprocessed structure?"
  hint2="Prefix sums let you compute range sums as `pref[j+1] - pref[i]`. For ’count subarrays with property X on sum’, use a hash-map of prefix sums."
  hint3="For ’≥ 2 length’ or ’divisible by k’ variants, store first occurrence and check remainders."
/&gt;
---

## Approach 1 — For each cell, sum k-neighborhood

O(m·n·k²). Baseline.

## Approach 2 — 2D prefix sum

**Insight.** Build `pref[i][j]` = sum of `mat[0..i-1][0..j-1]`. Then any rectangle sum = O(1) via inclusion-exclusion.



```java
int[][] matrixBlockSum(int[][] mat, int k) {
    int m = mat.length, n = mat[0].length;
    int[][] pref = new int[m + 1][n + 1];
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            pref[i+1][j+1] = mat[i][j] + pref[i][j+1] + pref[i+1][j] - pref[i][j];
    int[][] ans = new int[m][n];
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) {
            int r1 = Math.max(0, i - k), c1 = Math.max(0, j - k);
            int r2 = Math.min(m - 1, i + k), c2 = Math.min(n - 1, j + k);
            ans[i][j] = pref[r2+1][c2+1] - pref[r1][c2+1] - pref[r2+1][c1] + pref[r1][c1];
        }
    return ans;
}
```



<CodeTrace
  title="2D pref — mat=[[1,2,3],[4,5,6],[7,8,9]], k=1"
  :values="['1','2','3','4','5','6','7','8','9']"
  :windowKeys="['i']"
  :cellWidth="30"
  :steps='[
    { pointers: { i: 0 }, vars: { rect: "[0..1,0..1]", sum: 12 }, note: "cell (0,0) neighborhood sum" },
    { pointers: { i: 4 }, vars: { rect: "[0..2,0..2]", sum: 45 }, note: "middle covers whole grid" }
  ]'
/>

**Complexity** — Time **O(m·n)**; Space **O(m·n)**.

---

## Try it yourself

<JavaRunner problem-slug="matrix-block-sum" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Neighborhood sum | O(m·n·k²) | O(1) | baseline |
| 2D prefix sum | **O(m·n)** | O(m·n) | optimum |

## When to use which

- **Many rectangle-sum queries on static matrix** → 2D prefix sum.
- **Updates + queries** → 2D Fenwick / BIT.
- **1D version** → same technique on a 1D prefix array.

## Related problems

- [Range Sum Query 2D - Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/) — same technique
- [Count Submatrices with Target Sum](/problems/count-submatrices-with-target-sum)
- [Maximal Rectangle](/problems/maximal-rectangle)