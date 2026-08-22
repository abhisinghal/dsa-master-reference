# Backtracking — Valid Sudoku

*[↗ LeetCode: Valid Sudoku](https://leetcode.com/problems/valid-sudoku/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/hashing)

Check partial Sudoku validity (no duplicates within any row/col/box among filled cells).

## Approach 1 — Three passes

Rows, columns, boxes — separate scans. O(81).

## Approach 2 — One pass with encoded keys

**Insight.** Emit three keys per filled cell into a set: `"r{r}={d}"`, `"c{c}={d}"`, `"b{r/3}{c/3}={d}"`. Any duplicate = invalid.

```java
boolean isValidSudoku(char[][] board) {
    Set<String> seen = new HashSet<>();
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            char d = board[r][c];
            if (d == '.') continue;
            if (!seen.add("r" + r + d) || !seen.add("c" + c + d) || !seen.add("b" + r/3 + c/3 + d)) return false;
        }
    return true;
}
```

## Approach 3 — Bitmasks (fastest)

`rows[9]`, `cols[9]`, `boxes[9]` as ints. Check + set the bit for each cell. Same shape as Sudoku Solver.

**Complexity** — Time **O(1)** (fixed 81); Space **O(1)**.

## Related problems

- [Sudoku Solver](/problems/sudoku-solver) — full backtracking
