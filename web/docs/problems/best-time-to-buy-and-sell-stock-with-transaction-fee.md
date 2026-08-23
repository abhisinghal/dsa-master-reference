# DP — Best Time to Buy and Sell Stock with Transaction Fee

*[↗ LeetCode: Best Time to Buy and Sell Stock with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google, Meta" />

Unlimited transactions; each sell pays `fee`. Max profit.

**Example 1** — `prices=[1,3,2,8,4,9], fee=2` → `8`

**Constraints** — `1 ≤ n ≤ 5·10⁴`.


<Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="best-time-to-buy-and-sell-stock-with-transaction-fee" /> <Bookmark problem-slug="best-time-to-buy-and-sell-stock-with-transaction-fee" />

<InterviewTimer problem-slug="best-time-to-buy-and-sell-stock-with-transaction-fee" />



## Approach — State-machine DP (canonical)

**States.** `hold`, `cash`.
- `hold = max(hold, cash - price)`
- `cash = max(cash, hold + price - fee)`



```java
int maxProfit(int[] prices, int fee) {
    int cash = 0, hold = -prices[0];
    for (int i = 1; i < prices.length; i++) {
        int nCash = Math.max(cash, hold + prices[i] - fee);
        int nHold = Math.max(hold, cash - prices[i]);
        cash = nCash; hold = nHold;
    }
    return cash;
}
```



<CodeTrace
  title="State-machine DP (canonical)"
  :values="['1', '3', '2', '8', '4', '9']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 3 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 5 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="best-time-to-buy-and-sell-stock-with-transaction-fee" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| State machine DP | **O(n)** | O(1) | canonical |

## When to use which

- **Fee on transaction** → 2 states.
- **Cooldown** → 3 states.

<AiCompanion problem-slug="best-time-to-buy-and-sell-stock-with-transaction-fee" pattern-hint="dynamic programming" />

## Related problems

- [With Cooldown](/problems/best-time-to-buy-and-sell-stock-with-cooldown)
- [Best Time to Buy and Sell Stock IV](/problems/best-time-to-buy-and-sell-stock-iv)

<FeedbackWidget problem-slug="best-time-to-buy-and-sell-stock-with-transaction-fee" />
