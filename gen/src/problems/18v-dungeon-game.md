# DP — Dungeon Game

*[↗ LeetCode: Dungeon Game](https://leetcode.com/problems/dungeon-game/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google, Meta" />

Knight from top-left to bottom-right; each cell gives/takes HP; HP ≥ 1 always. Find min initial HP.

**Constraints** — `1 ≤ m, n ≤ 200`. Brute enumerate paths + simulate is O(2^(m+n)) — 2^400 ≈ 10¹²⁰ paths at max, impossible past 20×20. Reverse DP is O(mn) = 4·10⁴ ops, ~1 ms; forward-DP attempt burns 5 hour of debugging before you realize you can't know future minimum HP.
**Example 1** — `dungeon=[[-2,-3,3],[-5,-10,1],[10,30,-5]]` → `7`
**Example 2** — `dungeon=[[0]]` → `1`
**Example 3** — `dungeon=[[1,-3,3],[0,-2,0],[-3,-3,-3]]` → `3`


<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="dungeon-game" /> <Bookmark problem-slug="dungeon-game" />

<InterviewTimer problem-slug="dungeon-game" />



## Approach 1 — Forward DP (broken — showing why)

**Intuition.** Try to fill `dp[i][j]` = "min HP to reach `(i,j)` alive". Fails because you might arrive with excess HP that soaks a later damage, so the *state must include current HP* — that's exponential.

*In an interview* voice this out: "forward DP would need to track HP as a dimension → O(mn·H) ≈ O(mn·10⁴). Reverse DP eliminates the H dimension because 'HP need' only depends on the future path, not the past."

---

## Approach 2 — Reverse DP from bottom-right (canonical)

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

**Complexity** — Time **O(mn)**; Space **O(mn)** (compressible to O(n)). *Say aloud in an interview:* "when forward DP needs future information, reverse the sweep direction. Same trick powers Rod Cutting, Regular Expression Matching."

---

## Try it yourself

<JavaRunner problem-slug="dungeon-game" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Forward DP with HP state | O(mn·H) | O(mn·H) | Reference — impractical |
| **Reverse DP** | **O(mn)** | O(mn) | **Canonical** |

## When to use which

- **"Min initial resource to survive path"** → reverse DP.
- **"Max resource collectible"** → forward DP.

<AiCompanion problem-slug="dungeon-game" pattern-hint="dynamic programming" />

## Related problems

- [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/)
- [Cherry Pickup](https://leetcode.com/problems/cherry-pickup/)

<FeedbackWidget problem-slug="dungeon-game" />
