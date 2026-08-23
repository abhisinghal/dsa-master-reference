# Dynamic Programming — Coin Change

*[↗ LeetCode: Coin Change](https://leetcode.com/problems/coin-change/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg, Uber" /&gt;

Given `coins` (unbounded supply of each) and `amount`, return the **minimum** number of coins that sum to `amount`, or `-1` if impossible.

**Example 1** — `coins=[1,2,5], amount=11` → `3` (`5+5+1`)
**Example 2** — `coins=[2], amount=3` → `-1`
**Example 3** — `coins=[1], amount=0` → `0`

**Constraints** — `1 ≤ #coins ≤ 12`; `0 ≤ amount ≤ 10⁴`.


&lt;Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/&gt;
---

&lt;MarkSolved problem-slug="coin-change" /&gt;


## Approach 1 — Brute force recursion

**Intuition.** `f(rem) = 1 + min(f(rem - c))` over all coins. Base: `f(0) = 0`; `f(<0) = ∞`.



```java
int coinChangeBrute(int[] coins, int amount) {
    int r = rec(coins, amount);
    return r == Integer.MAX_VALUE ? -1 : r;
}
int rec(int[] coins, int rem) {
    if (rem == 0) return 0;
    if (rem < 0) return Integer.MAX_VALUE;
    int best = Integer.MAX_VALUE;
    for (int c : coins) {
        int r = rec(coins, rem - c);
        if (r != Integer.MAX_VALUE) best = Math.min(best, r + 1);
    }
    return best;
}
```



**Complexity** — Time **O(k^amount)**; Space **O(amount)** stack. TLE at amount=10⁴.

---

## Approach 2 — Memoized recursion (top-down DP)

**Insight from brute.** Same subproblem `rec(rem)` is called exponentially. Cache.



```java
int coinChangeMemo(int[] coins, int amount) {
    Integer[] memo = new Integer[amount + 1];
    int r = rec(coins, amount, memo);
    return r == Integer.MAX_VALUE ? -1 : r;
}
int rec(int[] coins, int rem, Integer[] memo) {
    if (rem == 0) return 0;
    if (rem < 0) return Integer.MAX_VALUE;
    if (memo[rem] != null) return memo[rem];
    int best = Integer.MAX_VALUE;
    for (int c : coins) {
        int r = rec(coins, rem - c, memo);
        if (r != Integer.MAX_VALUE) best = Math.min(best, r + 1);
    }
    return memo[rem] = best;
}
```



**Complexity** — Time **O(amount · k)**; Space **O(amount)**.

---

## Approach 3 — Bottom-up DP (tabulation)

**Insight from memo.** Iterate `w` from 1 to `amount`. `dp[w] = 1 + min(dp[w - c])` for feasible `c`.

**Trap.** Use `amount + 1` as the "unreachable" sentinel — `Integer.MAX_VALUE + 1` wraps to negative.



```java
int coinChange(int[] coins, int amount) {
    int sentinel = amount + 1;
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, sentinel);
    dp[0] = 0;
    for (int w = 1; w <= amount; w++)
        for (int c : coins)
            if (c <= w) dp[w] = Math.min(dp[w], dp[w - c] + 1);
    return dp[amount] == sentinel ? -1 : dp[amount];
}
```



<CodeTrace
  title="Bottom-up DP — coins=[1,2,5], amount=11"
  :values="[0,1,1,2,2,1,2,2,3,3,2,3]"
  :windowKeys="['w']"
  :cellWidth="30"
  :steps='[
    { pointers: { w: 1 }, vars: { pick: "coin 1", dp: 1 }, note: "1 = 1", added: [1] },
    { pointers: { w: 5 }, vars: { pick: "coin 5", dp: 1 }, note: "5 = 5", added: [5] },
    { pointers: { w: 6 }, vars: { pick: "5+1", dp: 2 }, note: "6 = 5+1" },
    { pointers: { w: 10 }, vars: { pick: "5+5", dp: 2 }, note: "10 = 5+5", added: [10] },
    { pointers: { w: 11 }, vars: { pick: "5+5+1", dp: 3 }, note: "11 = 5+5+1 → answer 3", added: [11] }
  ]'
/>

**Complexity** — Time **O(amount · k)**; Space **O(amount)**. Optimal.

---

## Try it yourself

<JavaRunner problem-slug="coin-change" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute recursion | O(k^amount) | O(amount) |
| Memoized | O(amount · k) | O(amount) |
| Bottom-up tabulation | **O(amount · k)** | **O(amount)** |

## When to use which

- **Cold interview** → brute → memo → table.
- **BFS variant** → BFS layer = fewest coins; also O(amount · k). Sometimes faster in practice.

&lt;AiCompanion problem-slug="coin-change" pattern-hint="dynamic programming" /&gt;

## Related problems

- [Coin Change II](https://leetcode.com/problems/coin-change-ii/) — **count** the ways, not the min
- [Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/) — same skeleton with ordered sequences
- [Perfect Squares](https://leetcode.com/problems/perfect-squares/) — coins = square numbers
- [Minimum Cost For Tickets](https://leetcode.com/problems/minimum-cost-for-tickets/) — variant with day-based DP

&lt;FeedbackWidget problem-slug="coin-change" /&gt;

&lt;RelatedProblems problems="min-cost-climbing-stairs::Min Cost Climbing Stairs|target-sum::Target Sum|burst-balloons::Burst Balloons" /&gt;
