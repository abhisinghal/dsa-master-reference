# Backtracking — Unique Paths III

*[↗ LeetCode: Unique Paths III](https://leetcode.com/problems/unique-paths-iii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Amazon, Meta, Google" />

Grid: 1=start, 2=end, 0=empty, -1=obstacle. Count paths visiting every empty cell exactly once.

**Constraints** — grid ≤ 20 cells (n·m ≤ 20). This tight cap is deliberate — Hamiltonian-path counting is NP-hard in general (no polynomial algorithm known). At 20 cells, `2²⁰ ≈ 10⁶` bitmask states are feasible; at 30 cells, `2³⁰ ≈ 10⁹` isn't.

**Example 1** — `grid=[[1,0,0,0],[0,0,0,0],[0,0,2,-1]]` → `2`
**Example 2** — `grid=[[1,0,0,0],[0,0,0,0],[0,0,0,2]]` → `4`
**Example 3** — `grid=[[0,1],[2,0]]` → `0`


<Hints
  hint1="You're exploring a decision tree. What's the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

<MarkSolved problem-slug="unique-paths-iii" /> <Bookmark problem-slug="unique-paths-iii" />

<InterviewTimer problem-slug="unique-paths-iii" />



## Approach 1 — Bitmask DP `dp[cell][visited_mask]`

**Intuition.** State = current cell + bitmask of visited empty cells. Transition = move to each unvisited neighbor. Count paths reaching end cell with all bits set.

**Complexity** — Time **O(4 · mn · 2^cells)** ≈ O(80·10⁶) at 20 cells; Space **O(mn · 2^cells)** ≈ O(80MB) — tight on memory. *In an interview* say "DFS with in-place marking has same asymptotic but uses O(mn) space — mention DP as the general Hamiltonian-path template."

---

## Approach 2 — Hamiltonian-path DFS with in-place marking (canonical)

**Insight.** Track remaining empty cells to visit. On end cell, count if remaining == 0. Mark visited by mutating (restore on return).

```java
int uniquePathsIII(int[][] grid) {
    int m = grid.length, n = grid[0].length, sr = 0, sc = 0, remaining = 1;
    for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) {
        if (grid[i][j] == 1) { sr = i; sc = j; }
        else if (grid[i][j] == 0) remaining++;
    }
    return dfs(grid, sr, sc, remaining);
}
int dfs(int[][] g, int r, int c, int rem) {
    if (r < 0 || c < 0 || r >= g.length || c >= g[0].length || g[r][c] == -1) return 0;
    if (g[r][c] == 2) return rem == 0 ? 1 : 0;
    int tmp = g[r][c];
    g[r][c] = -1;
    int total = dfs(g, r+1, c, rem-1) + dfs(g, r-1, c, rem-1)
              + dfs(g, r, c+1, rem-1) + dfs(g, r, c-1, rem-1);
    g[r][c] = tmp;
    return total;
}
```

<CodeTrace
  title="Hamiltonian-path DFS with in-place marking (canonical)"
  :values="['1', '0', '0', '0']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time exponential (~4^cells); Space O(mn). n·m ≤ 20 makes it feasible. *Say aloud in an interview:* "Hamiltonian path counting is NP-hard — the 20-cell cap is exactly what lets brute-force fit."

---

## Try it yourself

<JavaRunner problem-slug="unique-paths-iii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Bitmask DP | O(mn · 2^cells) | O(mn · 2^cells) | General Hamiltonian template |
| **DFS + in-place mark** | **~O(4^cells)** | O(mn) | **Canonical — least code** |

## When to use which

- **Hamiltonian path count** → DFS with marking.
- **Larger grids** → bitmask DP if ≤ 20 cells.
- **Shortest / longest** → BFS layers.

<AiCompanion problem-slug="unique-paths-iii" pattern-hint="backtracking" />

## Related problems

- [Robot Room Cleaner](/problems/robot-room-cleaner)
- [Shortest Path Visiting All Nodes](/problems/shortest-path-visiting-all-nodes)

<FeedbackWidget problem-slug="unique-paths-iii" />
