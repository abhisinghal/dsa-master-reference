# DP — Best Time to Buy and Sell Stock with Cooldown

*[↗ LeetCode: Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

&lt;CompanyTags companies="Meta, Amazon, Google, Bloomberg" /&gt;

Unlimited transactions; must skip one day between sell and next buy.

**Example 1** — `prices=[1,2,3,0,2]` → `3`

**Constraints** — `1 ≤ n ≤ 5000`.


&lt;Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/&gt;
---

&lt;MarkSolved problem-slug="best-time-to-buy-and-sell-stock-with-cooldown" /&gt; &lt;Bookmark problem-slug="best-time-to-buy-and-sell-stock-with-cooldown" /&gt;

&lt;InterviewTimer problem-slug="best-time-to-buy-and-sell-stock-with-cooldown" /&gt;



## Approach — State-machine DP (canonical)

**States.** `hold`, `sold`, `rest`.
- `hold = max(hold, rest - price)`
- `sold = hold + price`
- `rest = max(rest, sold)`



```java
int maxProfit(int[] prices) {
    int hold = -prices[0], sold = 0, rest = 0;
    for (int i = 1; i < prices.length; i++) {
        int nHold = Math.max(hold, rest - prices[i]);
        int nSold = hold + prices[i];
        int nRest = Math.max(rest, sold);
        hold = nHold; sold = nSold; rest = nRest;
    }
    return Math.max(sold, rest);
}
```



<CodeTrace
  title="State-machine DP (canonical)"
  :values="['1', '2', '3', '0', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 4 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="best-time-to-buy-and-sell-stock-with-cooldown" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| State machine DP | **O(n)** | O(1) | canonical |

## When to use which

- **Cooldown** → 3 states.
- **Fee** → 2 states.
- **k transactions** → 2k states.

&lt;AiCompanion problem-slug="best-time-to-buy-and-sell-stock-with-cooldown" pattern-hint="dynamic programming" /&gt;

## Related problems

- [Best Time to Buy and Sell Stock IV](/problems/best-time-to-buy-and-sell-stock-iv)
- [With Transaction Fee](/problems/best-time-to-buy-and-sell-stock-with-transaction-fee)

&lt;FeedbackWidget problem-slug="best-time-to-buy-and-sell-stock-with-cooldown" /&gt;
