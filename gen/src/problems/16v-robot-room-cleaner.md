# Backtracking — Robot Room Cleaner

*[↗ LeetCode: Robot Room Cleaner](https://leetcode.com/problems/robot-room-cleaner/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/backtracking)

Robot API: `move()`, `turnLeft()`, `turnRight()`, `clean()`. No coordinates. Clean every reachable cell.

---

## Approach 1 — DFS with relative coords + backtrack move
**Insight.** Assign robot's start as `(0,0)`. Maintain direction as `d ∈ {0,1,2,3}` (up, right, down, left). Recurse, marking visited. To backtrack, execute the reverse: 180° turn, move, 180° turn.

```java
int[][] D = {{-1,0},{0,1},{1,0},{0,-1}};
void cleanRoom(Robot robot) {
    dfs(robot, 0, 0, 0, new HashSet<>());
}
void dfs(Robot r, int x, int y, int d, Set<String> seen) {
    seen.add(x + "," + y);
    r.clean();
    for (int k = 0; k < 4; k++) {
        int nd = (d + k) % 4;
        int nx = x + D[nd][0], ny = y + D[nd][1];
        if (!seen.contains(nx + "," + ny) && r.move()) {
            dfs(r, nx, ny, nd, seen);
            // backtrack: reverse
            r.turnRight(); r.turnRight();
            r.move();
            r.turnRight(); r.turnRight();
        }
        r.turnRight(); // face next direction
    }
}
```

**Complexity** — Time **O(4^(m-n))** where (m-n) = unvisited cells; each cell has 4 turns + at most 1 move → linear in cells with constant factor 4.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| DFS with relative coords + backtrack move | O(4^(m-n)) | — | primary |

## When to use which

- **Ship this** → DFS with relative coords + backtrack move (O(4^(m-n)), —). The pattern's standard solution.

## Related problems

- [Number of Islands](/problems/number-of-islands) — DFS on known grid
- [Unique Paths III](/problems/unique-paths-iii)
