# DP — Dungeon Game

*[↗ LeetCode: Dungeon Game](https://leetcode.com/problems/dungeon-game/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google, Meta" />

Knight from top-left to bottom-right; each cell gives/takes HP; HP ≥ 1 always. Find min initial HP.

**Constraints** — `1 ≤ m, n ≤ 200`.

**Example 1** — `dungeon=[[-2,-3,3],[-5,-10,1],[10,30,-5]]` → `7`
**Example 2** — `dungeon=[[0]]` → `1`


<Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="dungeon-game" /> <Bookmark problem-slug="dungeon-game" />

<InterviewTimer problem-slug="dungeon-game" />



## Approach — Reverse DP from bottom-right (canonical)

**Insight.** Forward fails: HP need depends on future losses. Instead DP backward: `need[i][j]` = min HP required to survive starting here.



```java
int calculateMinimumHP(int[][] room) {
    int m = room.length, n = room[0].length;
    int[][] need = new int[m + 1][n + 1];
    for (int[] r : need) Arrays.fill(r, Integer.MAX_VALUE);
    need[m][n-1] = need[m-1][n] = 1;
    for (int i = m - 1; i >= 0; i--)
        for (int j = n - 1; j >= 0; j--) {
            int min = Math.min(need[i+1][j], need[i][j+1]);
            need[i][j] = Math.max(1, min - room[i][j]);
        }
    return need[0][0];
}
```



<CodeTrace
  title="Reverse DP from bottom-right (canonical)"
  :values="['-2', '-3', '3']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(mn)**; Space **O(mn)** (compressible).

---

## Try it yourself

<JavaRunner problem-slug="dungeon-game" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Reverse DP | **O(mn)** | O(mn) | canonical |

## When to use which

- **"Min initial resource to survive path"** → reverse DP.
- **"Max resource collectible"** → forward DP.

<AiCompanion problem-slug="dungeon-game" pattern-hint="dynamic programming" />

## Related problems

- [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/)
- [Cherry Pickup](https://leetcode.com/problems/cherry-pickup/)

<FeedbackWidget problem-slug="dungeon-game" />
