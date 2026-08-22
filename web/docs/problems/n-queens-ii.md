# Backtracking — N-Queens II

*[↗ LeetCode: N-Queens II](https://leetcode.com/problems/n-queens-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/backtracking)

Return the **count** of distinct solutions to N-Queens (no need to list boards).

---

## Approach 1 — Bitmask backtracking (fastest classical)
**Insight.** Encode occupied columns and diagonals as three bitmasks: `cols`, `d1` (top-left to bottom-right), `d2` (top-right to bottom-left). Each row, iterate free positions using `available = ~(cols | d1 | d2) & fullMask`. Shift d1 left, d2 right per row.



```java
int totalNQueens(int n) {
    int[] count = new int[]{0};
    dfs(n, 0, 0, 0, 0, count);
    return count[0];
}
void dfs(int n, int row, int cols, int d1, int d2, int[] count) {
    if (row == n) { count[0]++; return; }
    int full = (1 << n) - 1;
    int avail = full & ~(cols | d1 | d2);
    while (avail != 0) {
        int pick = avail & -avail; // lowest set bit
        avail ^= pick;
        dfs(n, row + 1, cols | pick, (d1 | pick) << 1 & full, (d2 | pick) >> 1, count);
    }
}
```



**Complexity** — Time **O(n!)** worst case; each step is O(1) bit-op instead of O(n) column scan → ~50× faster in practice.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Bitmask backtracking (fastest classical) | O(n!) | — | primary |

## When to use which

- **Ship this** → Bitmask backtracking (fastest classical) (O(n!), —). The pattern's standard solution.

## Related problems

- [N-Queens](/problems/backtracking-n-queens) — return boards, not just count
- [Sudoku Solver](/problems/sudoku-solver) — same bitmask domain-pruning idea
