# Backtracking — Robot Room Cleaner

*[↗ LeetCode: Robot Room Cleaner](https://leetcode.com/problems/robot-room-cleaner/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Meta, Google, Amazon" />

Robot API: `move()`, `turnLeft()`, `turnRight()`, `clean()`. No coordinates. Clean every reachable cell.

**Constraints** — grid unknown; obstacles hidden.

**Example 1** — Room modeled as grid with obstacles; robot at `(row, col)`. Robot cleans every reachable cell.


<Hints
  hint1="You’re exploring a decision tree. What’s the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

## Approach — DFS with relative coords + backtrack move (canonical)

**Insight.** Assign start as `(0,0)`. Maintain direction `d ∈ {0,1,2,3}` (up/right/down/left). Recurse, marking visited. Backtrack = reverse: 180° turn, move, 180° turn.

```java
int[][] D = {{-1,0},{0,1},{1,0},{0,-1}};
void cleanRoom(Robot robot) { dfs(robot, 0, 0, 0, new HashSet<>()); }
void dfs(Robot r, int x, int y, int d, Set<String> seen) {
    seen.add(x + "," + y);
    r.clean();
    for (int k = 0; k < 4; k++) {
        int nd = (d + k) % 4;
        int nx = x + D[nd][0], ny = y + D[nd][1];
        if (!seen.contains(nx + "," + ny) && r.move()) {
            dfs(r, nx, ny, nd, seen);
            r.turnRight(); r.turnRight();
            r.move();
            r.turnRight(); r.turnRight();
        }
        r.turnRight();
    }
}
```

**Complexity** — Time **O(4^(cells))**; each cell has 4 turns + 1 move at most.

---

## Try it yourself

<JavaRunner problem-slug="robot-room-cleaner" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DFS with reverse-move backtrack | **O(cells)** | O(cells) | canonical |

## When to use which

- **Unknown grid + directional API** → DFS + relative coords.
- **Known grid** → simpler DFS/BFS.
- **Multi-agent** → parallel exploration primitives.

## Related problems

- [Number of Islands](/problems/number-of-islands)
- [Unique Paths III](/problems/unique-paths-iii)