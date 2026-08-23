# Backtracking — N-Queens II

*[↗ LeetCode: N-Queens II](https://leetcode.com/problems/n-queens-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/backtracking)

Return **count** of distinct N-Queens solutions.

**Example 1** — `n=4` → `2`

**Constraints** — `1 ≤ n ≤ 9`.

---

## Approach — Bitmask backtracking (canonical)

**Insight.** Track `cols`, `d1`, `d2` bitmasks. Each row: `avail = ~(cols | d1 | d2) & fullMask`; iterate free positions via `avail & -avail` (lowest set bit). Shift diagonals per row.



```java
int totalNQueens(int n) {
    int[] count = {0};
    dfs(n, 0, 0, 0, 0, count);
    return count[0];
}
void dfs(int n, int row, int cols, int d1, int d2, int[] count) {
    if (row == n) { count[0]++; return; }
    int full = (1 << n) - 1;
    int avail = full & ~(cols | d1 | d2);
    while (avail != 0) {
        int pick = avail & -avail;
        avail ^= pick;
        dfs(n, row + 1, cols | pick, (d1 | pick) << 1 & full, (d2 | pick) >>> 1, count);
    }
}
```



**Complexity** — Time **O(n!)** worst; ~50× faster than column-scan in practice.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Bitmask backtracking | **O(n!)** | O(n) | canonical |

## When to use which

- **Count only** → this problem.
- **Return boards** → [N-Queens](/problems/backtracking-n-queens).
- **Very large n** — no known polynomial algorithm.

## Related problems

- [N-Queens](/problems/backtracking-n-queens)
- [Sudoku Solver](/problems/sudoku-solver)
