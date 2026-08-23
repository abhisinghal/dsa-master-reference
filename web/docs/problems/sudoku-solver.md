# Backtracking — Sudoku Solver

*[↗ LeetCode: Sudoku Solver](https://leetcode.com/problems/sudoku-solver/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/backtracking)

Fill the 9×9 board so every row/col/box contains 1..9.

**Example 1** — Standard Sudoku puzzle.

**Constraints** — 9×9 board, `.` for empty.

---

## Approach — Backtracking + constraint bitmasks (canonical)

**Insight.** Maintain 9-bit masks for each row, col, box. Try each digit at each empty cell.



```java
int[] rows = new int[9], cols = new int[9], boxes = new int[9];
void solveSudoku(char[][] board) {
    for (int r = 0; r < 9; r++) for (int c = 0; c < 9; c++)
        if (board[r][c] != '.') set(r, c, board[r][c] - '0');
    dfs(board, 0);
}
boolean dfs(char[][] b, int p) {
    if (p == 81) return true;
    int r = p / 9, c = p % 9;
    if (b[r][c] != '.') return dfs(b, p + 1);
    int box = (r / 3) * 3 + c / 3;
    int used = rows[r] | cols[c] | boxes[box];
    for (int d = 1; d <= 9; d++) {
        int bit = 1 << d;
        if ((used & bit) != 0) continue;
        b[r][c] = (char) ('0' + d);
        set(r, c, d);
        if (dfs(b, p + 1)) return true;
        unset(r, c, d);
        b[r][c] = '.';
    }
    return false;
}
void set(int r, int c, int d) { int bit = 1 << d; rows[r] |= bit; cols[c] |= bit; boxes[(r/3)*3 + c/3] |= bit; }
void unset(int r, int c, int d) { int bit = 1 << d; rows[r] ^= bit; cols[c] ^= bit; boxes[(r/3)*3 + c/3] ^= bit; }
```



## MRV heuristic
Pick cell with **fewest legal digits** each step — typical hard puzzles solve in microseconds.

**Complexity** — Worst-case exponential; MRV makes real Sudokus near-instant.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Backtracking + bitmasks | **exponential worst** | O(1) | canonical |
| + MRV | practically fast | O(1) | polish |

## When to use which

- **Standard** → bitmask backtracking.
- **Hard puzzles fast** → add MRV.
- **Uniqueness check** → count solutions, stop at 2.

## Related problems

- [Valid Sudoku](/problems/valid-sudoku)
- [N-Queens](/problems/backtracking-n-queens)
