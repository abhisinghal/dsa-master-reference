# Backtracking — Sudoku Solver

*[↗ LeetCode: Sudoku Solver](https://leetcode.com/problems/sudoku-solver/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Uber" />

Fill the 9×9 board so every row/col/box contains 1..9.

**Example 1** — Standard Sudoku puzzle.
**Example 2** — Sparse puzzle (17 clues, the minimum for unique-solution Sudokus): MRV heuristic solves in ~1ms.
**Example 3** — Devil's Sudoku (crafted worst-case for naive backtracking): naive takes ~10 s, bitmask + MRV solves in ~50 ms.

**Constraints** — 9×9 board, `.` for empty; guaranteed to have a unique solution.


<Hints
  hint1="You're exploring a decision tree. What's the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

<MarkSolved problem-slug="sudoku-solver" /> <Bookmark problem-slug="sudoku-solver" />

<InterviewTimer problem-slug="sudoku-solver" />



## Approach 1 — Naive backtracking with `isValid` scan

**Intuition.** For each empty cell, try digits 1–9. For each try, scan the row, column, and 3×3 box to check for conflicts. Recurse; on failure, backtrack.



```java
boolean solveNaive(char[][] b) {
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            if (b[r][c] != '.') continue;
            for (char d = '1'; d <= '9'; d++) {
                if (!isValid(b, r, c, d)) continue;
                b[r][c] = d;
                if (solveNaive(b)) return true;
                b[r][c] = '.';
            }
            return false;
        }
    return true;
}
boolean isValid(char[][] b, int r, int c, char d) {
    for (int i = 0; i < 9; i++) {
        if (b[r][i] == d || b[i][c] == d) return false;
        if (b[(r/3)*3 + i/3][(c/3)*3 + i%3] == d) return false;
    }
    return true;
}
```



**Complexity** — Time exponential worst; the `isValid` scan is O(27) per attempt. On adversarial puzzles takes 5-10s. *In an interview* state this then upgrade to bitmasks + MRV.

---

## Approach 2 — Backtracking + constraint bitmasks + MRV (canonical)

**Insight.** Two upgrades:
1. **Bitmasks.** Maintain 9-bit masks per row, column, box. Check "is d used?" via `used & (1 << d) != 0` — a single AND, not a 27-cell scan.
2. **MRV heuristic** — Minimum Remaining Values. Instead of scanning cells in order, always pick the empty cell with the **fewest remaining legal digits** first. This cuts the search tree by 10-1000× on hard puzzles.



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



**MRV heuristic**: pick cell with **fewest legal digits** each step. Typical hard puzzles solve in microseconds instead of seconds.

**Complexity** — Worst-case exponential; MRV makes real Sudokus near-instant. *Say aloud in an interview:* "the pattern is Knuth's Dancing Links (Algorithm X, 2000). Sudoku is a classic exact-cover problem, and MRV is the essential heuristic."

---

## Try it yourself

<JavaRunner problem-slug="sudoku-solver" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Naive backtracking + isValid scan | exponential worst | O(1) | Correct baseline |
| **Bitmask + MRV** | **exponential worst, practically fast** | O(1) | **Canonical** |

## When to use which

- **Standard** → bitmask backtracking.
- **Hard puzzles fast** → add MRV.
- **Uniqueness check** → count solutions, stop at 2.

<AiCompanion problem-slug="sudoku-solver" pattern-hint="backtracking" />

## Related problems

- [Valid Sudoku](/problems/valid-sudoku)
- [N-Queens](/problems/backtracking-n-queens)

<FeedbackWidget problem-slug="sudoku-solver" />

<RelatedProblems problems="combination-sum-ii::Combination Sum II|beautiful-arrangement::Beautiful Arrangement|combination-sum-iv::Combination Sum IV" />
