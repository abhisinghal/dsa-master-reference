# DP — Best Time to Buy and Sell Stock IV

*[↗ LeetCode: Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Meta, Amazon, Google, Bloomberg" />

At most `k` transactions. Max profit.

**Constraints** — `1 ≤ k ≤ 100`; `1 ≤ n ≤ 1000`.

**Example 1** — `k=2, prices=[2,4,1]` → `2`
**Example 2** — `k=2, prices=[3,2,6,5,0,3]` → `7`


<Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="best-time-to-buy-and-sell-stock-iv" /> <Bookmark problem-slug="best-time-to-buy-and-sell-stock-iv" />

<InterviewTimer problem-slug="best-time-to-buy-and-sell-stock-iv" />



## Approach — 2k states DP with unlimited-k shortcut (canonical)

**Insight.** If `k ≥ n/2`, unlimited transactions → sum of positive diffs.

```java
int maxProfit(int k, int[] prices) {
    int n = prices.length;
    if (k >= n / 2) {
        int sum = 0;
        for (int i = 1; i < n; i++) if (prices[i] > prices[i-1]) sum += prices[i] - prices[i-1];
        return sum;
    }
    int[] buy = new int[k + 1], sell = new int[k + 1];
    Arrays.fill(buy, Integer.MIN_VALUE);
    for (int p : prices)
        for (int t = 1; t <= k; t++) {
            buy[t] = Math.max(buy[t], sell[t-1] - p);
            sell[t] = Math.max(sell[t], buy[t] + p);
        }
    return sell[k];
}
```

<CodeTrace
  title="2k states DP with unlimited-k shortcut (canonical)"
  :values="['2', '4', '1']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n · k)**; Space **O(k)**.

---

## Try it yourself

<JavaRunner problem-slug="best-time-to-buy-and-sell-stock-iv" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| 2k states DP | **O(n · k)** | O(k) | canonical |

## When to use which

- **Fixed k** → 2k states.
- **k unlimited** → sum positive diffs.

<AiCompanion problem-slug="best-time-to-buy-and-sell-stock-iv" pattern-hint="dynamic programming" />

## Related problems

- [With Cooldown](/problems/best-time-to-buy-and-sell-stock-with-cooldown)
- [With Transaction Fee](/problems/best-time-to-buy-and-sell-stock-with-transaction-fee)
- [Best Time to Buy and Sell Stock III](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/)

<FeedbackWidget problem-slug="best-time-to-buy-and-sell-stock-iv" />
