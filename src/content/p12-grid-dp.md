## The Pattern

Grid DP assigns meaning to each cell and fills the table in an order that satisfies dependencies. The classic shape is `dp[i][j]` from top and left, but the broader pattern includes string grids like Edit Distance and LCS: rows and columns are prefixes, and each cell summarizes the best answer for those two prefixes.

!!! pattern "Recognition signals"
    **Signals:** move only right/down, minimum path cost, number of paths, two-string prefix comparison, edit operations, or "answer for first i chars and first j chars." The grid is not always spatial; it may be an index product.

```diagram
{"type":"dptable","corner":"r\\c","col_head":["0","1","2","3"],"row_head":["0","1","2"],"grid":[["1","1","1","1"],["1","2","3","4"],["1","3","6","10"]],"highlights":[[2,3,"green"],[1,3,"primary"],[2,2,"amber"]],"arrows":[{"from":[1,3],"to":[2,3],"color":"primary"},{"from":[2,2],"to":[2,3],"color":"amber"}]}
```

## The Invariant

**STATE:** `dp[i][j]` is the answer for the subproblem ending at cell `(i, j)` or for prefixes `a[0..i)` and `b[0..j)`, depending on whether the grid is spatial or string-shaped.

**TRANSITION:** combine already-computed neighbors. Path counting: `dp[i][j] = dp[i - 1][j] + dp[i][j - 1]`. Minimum path sum: cell cost plus `min(top, left)`. Edit Distance adds diagonal for replace/match plus top/left for delete/insert; LCS uses diagonal on match, otherwise max of top/left.

**BASE CASE:** initialize boundaries before the main recurrence. First row/column are 1 for Unique Paths, cumulative sums for Minimum Path Sum, and edit costs `i`/`j` for Edit Distance. For LCS, row 0 and column 0 are 0 because an empty prefix has no common subsequence.

## Template

```java
int minPathSum(int[][] grid) {
    int rows = grid.length, cols = grid[0].length;
    int[][] dp = new int[rows][cols];
    dp[0][0] = grid[0][0];

    for (int r = 1; r < rows; r++) dp[r][0] = dp[r - 1][0] + grid[r][0];
    for (int c = 1; c < cols; c++) dp[0][c] = dp[0][c - 1] + grid[0][c];

    for (int r = 1; r < rows; r++) {
        for (int c = 1; c < cols; c++) {
            dp[r][c] = grid[r][c] + Math.min(dp[r - 1][c], dp[r][c - 1]);
        }
    }
    return dp[rows - 1][cols - 1];
}

int uniquePaths1D(int rows, int cols) {
    int[] dp = new int[cols];
    Arrays.fill(dp, 1);
    for (int r = 1; r < rows; r++) {
        for (int c = 1; c < cols; c++) {
            dp[c] += dp[c - 1];
        }
    }
    return dp[cols - 1];
}
```

## Worked Recognition

- **Unique Paths** (Module 12): each cell counts ways to arrive from top or left; boundaries are 1 because there is exactly one straight-line path along an edge.
- **Minimum Path Sum** (Module 12): same dependency shape, but replace addition of counts with `cost + min(top, left)`.
- **Edit Distance** and **LCS** (Module 12): the grid axes are string prefixes. Diagonal represents consuming both characters; top/left represent consuming one side.

## Complexity

!!! complexity "Complexity"
    **T:** O(RC) for an R by C grid or two-prefix table. **S:** O(RC) when reconstruction or full explanation is needed; O(C) when each row depends only on the previous row and current left value.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Skipping boundary initialization, mixing 0-based cells with 1-based prefix states, updating a 1D row in the wrong direction for recurrences that need old left/diagonal values, or treating obstacles as normal cells instead of zeroing/invalidating them before propagation.

## When NOT to use it

Do not use grid DP for unrestricted four-direction movement, shortest paths with cycles, or weighted graphs that require Dijkstra/Bellman-Ford. If dependencies are not acyclic under your fill order, first redefine the state or switch to graph algorithms.
