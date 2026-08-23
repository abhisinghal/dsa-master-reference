# Backtracking — N-Queens

*[↗ LeetCode: N-Queens](https://leetcode.com/problems/n-queens/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/backtracking)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft, Apple" /&gt;

Place `n` queens on an `n × n` board so no two attack each other. Return all distinct solutions.

**Example** — `n=4` → `2` solutions

**Constraints** — `1 ≤ n ≤ 9`.


&lt;Hints
  hint1="You’re exploring a decision tree. What’s the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/&gt;
---

## Approach 1 — Brute force (all n^n placements)

**Intuition.** Try every placement of `n` queens in the `n²` cells → `C(n², n)` combinations. Filter valid ones.

**Complexity** — `C(64, 8) ≈ 4·10⁹` for n=8. TLE.

---

## Approach 2 — Row-by-row backtracking with O(n) validity check

**Insight.** Because there's exactly one queen per row, iterate rows and place a queen in each. For each row `r`, try columns `c = 0..n-1`; validate that `(r, c)` doesn't share a column, main-diagonal, or anti-diagonal with any placed queen.



```java
List<List<String>> solveNQueensSlow(int n) {
    List<List<String>> res = new ArrayList<>();
    int[] queens = new int[n];  // queens[r] = column
    solve(0, n, queens, res);
    return res;
}
void solve(int r, int n, int[] queens, List<List<String>> res) {
    if (r == n) { res.add(render(queens)); return; }
    for (int c = 0; c < n; c++) {
        boolean ok = true;
        for (int i = 0; i < r; i++)
            if (queens[i] == c || Math.abs(queens[i] - c) == r - i) { ok = false; break; }
        if (ok) { queens[r] = c; solve(r + 1, n, queens, res); }
    }
}
```



**Complexity** — Time **O(n! · n)** (n! partial trees × O(n) check); Space **O(n)** recursion.

---

## Approach 3 — Backtracking with bitset conflict tracking

**Insight from row-by-row.** The validity check is O(n) — but conflict membership is really about *sets* (which columns/diagonals are taken). Track them incrementally with three boolean sets: `cols`, `mainDiag` (`r + c`), `antiDiag` (`r - c + n - 1`). O(1) check per placement.

**Trap.** Two bitsets by `r - c` and `r + c` — swapping them rejects valid boards.



```java
List<List<String>> solveNQueens(int n) {
    List<List<String>> res = new ArrayList<>();
    int[] queens = new int[n];
    boolean[] cols = new boolean[n];
    boolean[] main = new boolean[2 * n - 1];   // r + c
    boolean[] anti = new boolean[2 * n - 1];   // r - c + n - 1
    solve(0, n, queens, cols, main, anti, res);
    return res;
}
void solve(int r, int n, int[] queens, boolean[] cols, boolean[] main, boolean[] anti, List<List<String>> res) {
    if (r == n) { res.add(render(queens)); return; }
    for (int c = 0; c < n; c++) {
        int m = r + c, a = r - c + n - 1;
        if (cols[c] || main[m] || anti[a]) continue;
        cols[c] = main[m] = anti[a] = true;
        queens[r] = c;
        solve(r + 1, n, queens, cols, main, anti, res);
        cols[c] = main[m] = anti[a] = false;
    }
}
```



<CodeTrace
  title="Bitset backtracking — n=4"
  :values="[0,1,2,3]"
  :windowKeys="['row']"
  :cellWidth="46"
  :steps='[
    { pointers: { row: 0, col: 0 }, vars: { queens: "[0]" }, note: "row 0 → col 0", added: [0] },
    { pointers: { row: 1, col: 2 }, vars: { queens: "[0,2]" }, note: "row 1 → col 2 (col 1 blocked by diag)" },
    { pointers: { row: 2 }, vars: { queens: "[0,2,?]" }, note: "all cols blocked → backtrack" },
    { pointers: { row: 1, col: 3 }, vars: { queens: "[0,3]" }, note: "try col 3" },
    { pointers: { row: 3, col: 2 }, vars: { queens: "[1,3,0,2]" }, note: "restart from row 0 col 1 → SOLUTION", added: [0,1,2,3] }
  ]'
/>

**Complexity** — Time **O(n!)**; Space **O(n)**. Constant-factor faster than Approach 2 because validation is O(1) per cell.

---

## Try it yourself

<JavaRunner problem-slug="backtracking-n-queens" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| All placements | O(C(n², n)) | O(n) |
| Row backtracking, O(n) check | O(n! · n) | O(n) |
| Row backtracking, bitset O(1) check | **O(n!)** | O(n) |

## When to use which

- **Just needs solutions** → bitset backtracking.
- **Interviewer probes memoization** → NP-complete; no polynomial memo exists (state = full board history).

&lt;AiCompanion problem-slug="backtracking-n-queens" pattern-hint="backtracking" /&gt;

## Related problems (same ladder applies)

- [N-Queens II](https://leetcode.com/problems/n-queens-ii/) — count solutions only
- [Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) — same backtracking, three bitset dimensions (row/col/box)
- [Permutations](https://leetcode.com/problems/permutations/) — swap-in-place backtracking
- [Subsets](https://leetcode.com/problems/subsets/) — start-index backtracking

&lt;FeedbackWidget problem-slug="backtracking-n-queens" /&gt;
