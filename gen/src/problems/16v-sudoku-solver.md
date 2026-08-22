# Backtracking — Sudoku Solver

*[↗ LeetCode: Sudoku Solver](https://leetcode.com/problems/sudoku-solver/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/backtracking)

Fill the 9×9 board so every row/col/box contains 1..9.

---

## Approach 1 — Backtracking + constraint tracking
**Insight.** Maintain 9-bit masks for each row, col, and box. Try each digit at each empty cell. Backtrack on dead ends.

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

## Interview extension — MRV heuristic

Pick the empty cell with the **fewest legal digits** each step (Minimum Remaining Values). Typical hard puzzles solve in microseconds.

**Complexity** — Time worst case exponential; MRV makes real Sudokus near instant.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Backtracking + constraint tracking | — | — | primary |

## When to use which

- **Ship this** → Backtracking + constraint tracking (—, —). The pattern's standard solution.

## Related problems

- [Valid Sudoku](/problems/valid-sudoku) — validation only
- [N-Queens](/problems/backtracking-n-queens) — same constraint-tracking style
