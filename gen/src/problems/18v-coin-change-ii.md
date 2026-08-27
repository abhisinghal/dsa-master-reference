# DP — Coin Change II

*[↗ LeetCode: Coin Change II](https://leetcode.com/problems/coin-change-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google, Meta" />

Count ways to make `amount` from `coins` (unlimited each, **unordered**).

**Example 1** — `amount=5, coins=[1,2,5]` → `4`
**Example 2** — `amount=3, coins=[2]` → `0`
**Example 3** — `amount=10, coins=[10]` → `1`

**Constraints** — `1 ≤ #coins ≤ 300`; `1 ≤ amount ≤ 5000`. Brute recursion is O(k^amount) — for amount=100, k=10 that's 10¹⁰⁰. DP is O(A · C) = 5·10³ · 300 = 1.5·10⁶.


<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="coin-change-ii" /> <Bookmark problem-slug="coin-change-ii" />

<InterviewTimer problem-slug="coin-change-ii" />



## Approach 1 — Brute recursion enumerating combos

**Intuition.** At each recursion, either use coin `c` (stay at `c`) or skip to next. Terminate at amount=0 or exhaust coins.

```java
int changeBrute(int amount, int[] coins) {
    return dfs(amount, coins, 0);
}
int dfs(int rem, int[] coins, int idx) {
    if (rem == 0) return 1;
    if (rem < 0 || idx == coins.length) return 0;
    return dfs(rem - coins[idx], coins, idx) + dfs(rem, coins, idx + 1);
}
```

**Complexity** — Time exponential in amount/coin ratio; Space O(amount) stack. TLE past amount=25. *In an interview* say "memoize on (rem, idx) → O(A · C)."

---

## Approach 2 — Unbounded knapsack counting (canonical)

**Insight.** `dp[amt]` = number of ways to make `amt`. Outer loop = coins, inner = amount. **This ordering counts unordered combinations** (each coin's contribution is decided *once* per outer iteration, so different orderings don't count separately).

**Contrast.** Swap loop order → counts **ordered** sequences → [Combination Sum IV](/problems/combination-sum-iv).

```java
int change(int amount, int[] coins) {
    int[] dp = new int[amount + 1];
    dp[0] = 1;
    for (int c : coins)
        for (int t = c; t <= amount; t++)
            dp[t] += dp[t - c];
    return dp[amount];
}
```

<CodeTrace
  title="Unbounded knapsack counting (canonical)"
  :values="['1', '2', '5']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(amount · |coins|)**; Space **O(amount)**. *Say aloud in an interview:* "loop-order is the *only* thing that distinguishes 'count combinations' from 'count permutations' — same recurrence."

---

## Try it yourself

<JavaRunner problem-slug="coin-change-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute recursion | Exponential | O(A) | Reference; TLE past A=25 |
| **Unbounded knapsack** | **O(A · C)** | O(A) | **Canonical** |

## When to use which

- **Unordered** → outer coins.
- **Ordered** → outer amount.
- **Min coins** → different — see [Coin Change](/problems/coin-change).

<AiCompanion problem-slug="coin-change-ii" pattern-hint="dynamic programming" />

## Related problems

- [Coin Change](/problems/coin-change)
- [Combination Sum IV](/problems/combination-sum-iv)
- [Perfect Squares](/problems/perfect-squares)

<FeedbackWidget problem-slug="coin-change-ii" />

<RelatedProblems problems="longest-increasing-subsequence::Longest Increasing Subsequence|climbing-stairs::Climbing Stairs|min-cost-climbing-stairs::Min Cost Climbing Stairs" />
