# Backtracking — Valid Sudoku

*[↗ LeetCode: Valid Sudoku](https://leetcode.com/problems/valid-sudoku/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/hashing)

Check partial Sudoku validity (no duplicates within row/col/box among filled cells).

**Constraints** — 9×9 board.

---

## Approach 1 — Three passes

Rows, columns, boxes — separate scans.

## Approach 2 — One pass with encoded keys (canonical)

**Insight.** Emit three keys per filled cell into a set: `"r{r}={d}"`, `"c{c}={d}"`, `"b{r/3}{c/3}={d}"`. Duplicate → invalid.

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
`rows[9]`, `cols[9]`, `boxes[9]` as ints; check + set bit for each cell.

**Complexity** — Time **O(1)** (fixed 81); Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Three-pass | O(81) | O(9) | baseline |
| One-pass keys | **O(81)** | O(1) | canonical |
| Bitmasks | O(81) | O(1) | fastest |

## When to use which

- **Standard** → encoded keys.
- **Speed** → bitmasks.
- **Solve, not validate** → see [Sudoku Solver](/problems/sudoku-solver).

## Related problems

- [Sudoku Solver](/problems/sudoku-solver)
