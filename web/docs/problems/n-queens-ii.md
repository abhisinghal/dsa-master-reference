# Backtracking — N-Queens II

*[↗ LeetCode: N-Queens II](https://leetcode.com/problems/n-queens-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Meta, Amazon, Google, Microsoft" />

Return **count** of distinct N-Queens solutions.

**Example 1** — `n=4` → `2`
**Example 2** — `n=1` → `1`
**Example 3** — `n=8` → `92` (the classic 8-queens count)

**Constraints** — `1 ≤ n ≤ 9`.


<Hints
  hint1="You're exploring a decision tree. What's the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

<MarkSolved problem-slug="n-queens-ii" /> <Bookmark problem-slug="n-queens-ii" />

<InterviewTimer problem-slug="n-queens-ii" />



## Approach 1 — Brute force (arrays for column + diagonals)

**Intuition.** Standard N-Queens: recurse row by row. At each row, try every column; check conflicts against arrays `cols[]`, `d1[]`, `d2[]`. If none conflict, mark, recurse, unmark.



```java
int totalNQueensBrute(int n) {
    boolean[] cols = new boolean[n];
    boolean[] d1 = new boolean[2 * n];   // r + c
    boolean[] d2 = new boolean[2 * n];   // r - c + n
    int[] count = {0};
    dfs(n, 0, cols, d1, d2, count);
    return count[0];
}
void dfs(int n, int row, boolean[] cols, boolean[] d1, boolean[] d2, int[] count) {
    if (row == n) { count[0]++; return; }
    for (int c = 0; c < n; c++) {
        if (cols[c] || d1[row + c] || d2[row - c + n]) continue;
        cols[c] = d1[row + c] = d2[row - c + n] = true;
        dfs(n, row + 1, cols, d1, d2, count);
        cols[c] = d1[row + c] = d2[row - c + n] = false;
    }
}
```



**Complexity** — Time **O(n!)** worst case; Space **O(n)** for the arrays. Correct and standard for `n ≤ 9`. *In an interview* state this and mention bitmask is a ~50× constant-factor speedup.

---

## Approach 2 — Bitmask backtracking (canonical)

**Insight.** Instead of boolean arrays, track `cols`, `d1`, `d2` as `int` bitmasks. Available columns per row = `~(cols | d1 | d2) & fullMask`. Iterate free positions via `avail & -avail` (isolate lowest set bit). Shift diagonals by one per row (`d1 << 1`, `d2 >>> 1`). Every check becomes a single AND — no memory writes, cache-friendly.



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



**Complexity** — Time **O(n!)** worst but ~50× faster than Approach 1 in practice; Space **O(n)** recursion only. *Say aloud in an interview:* "the `avail & -avail` idiom isolates the lowest set bit — that's every 'try this column' becoming a single-cycle op."

---

## Try it yourself

<JavaRunner problem-slug="n-queens-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Boolean-array backtracking | O(n!) | O(n) | Correct baseline |
| **Bitmask backtracking** | **O(n!)** | O(n) | **Canonical (50× faster constant)** |

## When to use which

- **Count only** → this problem.
- **Return boards** → [N-Queens](/problems/backtracking-n-queens).
- **Very large n** — no known polynomial algorithm.

<AiCompanion problem-slug="n-queens-ii" pattern-hint="backtracking" />

## Related problems

- [N-Queens](/problems/backtracking-n-queens)
- [Sudoku Solver](/problems/sudoku-solver)

<FeedbackWidget problem-slug="n-queens-ii" />

<RelatedProblems problems="permutations::Permutations|sudoku-solver::Sudoku Solver|beautiful-arrangement::Beautiful Arrangement" />
