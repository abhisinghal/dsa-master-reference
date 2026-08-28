# Backtracking — Robot Room Cleaner

*[↗ LeetCode: Robot Room Cleaner](https://leetcode.com/problems/robot-room-cleaner/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Meta, Google, Amazon" />

Robot API: `move()`, `turnLeft()`, `turnRight()`, `clean()`. No coordinates. Clean every reachable cell.

**Constraints** — grid unknown; obstacles hidden. Grid ≤ 200×200. Brute wanders randomly, no completion guarantee. DFS with visited set + right-hand rule + backtrack move-and-undo is O(rooms) — ~10⁶ ops for a 300×300 grid.
**Example 1** — Room modeled as grid with obstacles; robot at `(row, col)`. Robot cleans every reachable cell.
**Example 2** — Room is `[[1,1,1,1,1,0,1,1],[1,1,1,1,1,0,1,1],[1,0,1,1,1,1,1,1],[0,0,0,1,0,0,0,0],[1,1,1,1,1,1,1,1]]`, start=`(1,3)` → robot visits all `1`s reachable from start.
**Example 3** — Sealed by obstacles at every direction → robot cleans only starting cell.


<Hints
  hint1="You're exploring a decision tree. What's the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

<MarkSolved problem-slug="robot-room-cleaner" /> <Bookmark problem-slug="robot-room-cleaner" />

<InterviewTimer problem-slug="robot-room-cleaner" />



## Approach 1 — Random walk (naive baseline)

**Intuition.** Randomly pick a direction, try to move, mark visited. Repeat until all cells seem visited (approximate with "stop after k moves without new cell").

**Why it fails.** In a snake-like corridor of 200 cells the expected time to visit all is O(cells²) — 40,000 moves for a small grid. And you cannot *know* when you're done without exhaustive tracking. Interviewers reject this as unbounded.

---

## Approach 2 — DFS with relative coords + backtrack move (canonical)

**Insight.** Because the grid has no absolute coordinates, assign start as `(0,0)` and track relative position. Maintain direction `d ∈ {0,1,2,3}` (up/right/down/left). Recurse depth-first, marking visited by relative `(x,y)` string.

**Backtrack move.** When returning from a recursive call, the robot must return to the caller's cell. Do it with: 180° turn (2 rights) → move → 180° turn back. That reverses the last physical move without needing coordinates.

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

**Complexity** — Time **O(cells)** with each cell visited at most 4 times; Space **O(cells)** for the seen set. *Say aloud in an interview:* "the 180-turn-move-180-turn dance is the only way to backtrack without global coordinates. Every DFS-on-unknown-graph problem uses some version of this."

---

## Try it yourself

<JavaRunner problem-slug="robot-room-cleaner" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Random walk | O(cells²) expected | O(cells) | Unbounded — reject |
| **DFS + backtrack move** | **O(cells)** | O(cells) | **Canonical** |

## When to use which

- **Unknown grid + directional API** → DFS + relative coords.
- **Known grid** → simpler DFS/BFS.
- **Multi-agent** → parallel exploration primitives.

<AiCompanion problem-slug="robot-room-cleaner" pattern-hint="backtracking" />

## Related problems

- [Number of Islands](/problems/number-of-islands)
- [Unique Paths III](/problems/unique-paths-iii)

<FeedbackWidget problem-slug="robot-room-cleaner" />
