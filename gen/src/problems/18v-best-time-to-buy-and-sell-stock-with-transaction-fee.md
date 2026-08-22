# DP — Best Time to Buy and Sell Stock with Transaction Fee

*[↗ LeetCode: Best Time to Buy and Sell Stock with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Unlimited transactions; each sell pays `fee`. Max profit.

## Approach — State-machine DP (two states)

**Insight.** Two states: `hold` (own stock), `cash` (no stock).
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

**Complexity** — Time **O(n)**; Space **O(1)**.

## Related problems

- [With Cooldown](/problems/best-time-to-buy-and-sell-stock-with-cooldown)
- [At Most K Transactions (IV)](/problems/best-time-to-buy-and-sell-stock-iv)
- [Single Transaction](/problems/best-time-to-buy-and-sell-stock)
