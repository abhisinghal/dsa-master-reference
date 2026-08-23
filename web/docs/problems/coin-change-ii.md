# DP — Coin Change II

*[↗ LeetCode: Coin Change II](https://leetcode.com/problems/coin-change-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

&lt;CompanyTags companies="Amazon, Google, Meta" /&gt;

Count ways to make `amount` from `coins` (unlimited each, **unordered**).

**Example 1** — `amount=5, coins=[1,2,5]` → `4`
**Example 2** — `amount=3, coins=[2]` → `0`
**Example 3** — `amount=10, coins=[10]` → `1`

**Constraints** — `1 ≤ #coins ≤ 300`; `1 ≤ amount ≤ 5000`.


&lt;Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/&gt;
---

&lt;MarkSolved problem-slug="coin-change-ii" /&gt; &lt;Bookmark problem-slug="coin-change-ii" /&gt;

&lt;InterviewTimer problem-slug="coin-change-ii" /&gt;



## Approach — Unbounded knapsack counting (canonical)

**Insight.** Outer loop = coins; inner = amount. This counts **unordered** combinations.



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

**Contrast.** Swap loop order → counts **ordered** sequences → [Combination Sum IV](/problems/combination-sum-iv).

**Complexity** — Time **O(amount · |coins|)**; Space **O(amount)**.

---

## Try it yourself

<JavaRunner problem-slug="coin-change-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Unbounded knapsack | **O(A · C)** | O(A) | canonical |

## When to use which

- **Unordered** → outer coins.
- **Ordered** → outer amount.
- **Min coins** → different — see [Coin Change](/problems/coin-change).

&lt;AiCompanion problem-slug="coin-change-ii" pattern-hint="dynamic programming" /&gt;

## Related problems

- [Coin Change](/problems/coin-change)
- [Combination Sum IV](/problems/combination-sum-iv)
- [Perfect Squares](/problems/perfect-squares)

&lt;FeedbackWidget problem-slug="coin-change-ii" /&gt;

&lt;RelatedProblems problems="longest-increasing-subsequence::Longest Increasing Subsequence|climbing-stairs::Climbing Stairs|min-cost-climbing-stairs::Min Cost Climbing Stairs" /&gt;
