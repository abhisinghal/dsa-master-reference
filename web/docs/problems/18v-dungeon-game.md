# DP — Dungeon Game

*[↗ LeetCode: Dungeon Game](https://leetcode.com/problems/dungeon-game/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

Knight from top-left to bottom-right; each cell gives/takes HP; HP must stay ≥ 1 throughout. Find min initial HP.

## Approach — Reverse DP from bottom-right

**Insight.** Forward DP fails because "min HP needed" depends on **future** losses. Instead, DP from `(m-1, n-1)` back to `(0, 0)`: `need[i][j]` = min HP required to survive starting from `(i, j)`.

- Base: at bottom-right, `need = max(1, 1 - room[m-1][n-1])`.
- Transition: `nextNeed = min(need[i+1][j], need[i][j+1])`; `need[i][j] = max(1, nextNeed - room[i][j])`.



```java
int calculateMinimumHP(int[][] room) {
    int m = room.length, n = room[0].length;
    int[][] need = new int[m + 1][n + 1];
    for (int[] r : need) Arrays.fill(r, Integer.MAX_VALUE);
    need[m][n - 1] = need[m - 1][n] = 1;
    for (int i = m - 1; i >= 0; i--)
        for (int j = n - 1; j >= 0; j--) {
            int min = Math.min(need[i + 1][j], need[i][j + 1]);
            need[i][j] = Math.max(1, min - room[i][j]);
        }
    return need[0][0];
}
```



**Complexity** — Time **O(mn)**; Space **O(mn)** — compressible to O(n).

**Why reverse.** Forward propagation of "min HP" doesn't compose — the required HP at `(i, j)` depends on the worst path from there onward, which is only known once the future is resolved.

## Related problems

- [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/)
- [Cherry Pickup](https://leetcode.com/problems/cherry-pickup/) — 2 knights DP
