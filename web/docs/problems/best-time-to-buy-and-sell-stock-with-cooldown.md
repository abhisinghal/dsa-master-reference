# DP — Best Time to Buy and Sell Stock with Cooldown

*[↗ LeetCode: Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Unlimited transactions, but you must skip one day between sell and next buy.

## Approach — State-machine DP

**Insight.** Three states each day:
- `hold[i]` = max profit holding a stock at end of day i
- `sold[i]` = max profit just sold today
- `rest[i]` = max profit not holding, not just sold (cooldown or idle)

Transitions:
- `hold[i] = max(hold[i-1], rest[i-1] - price[i])`
- `sold[i] = hold[i-1] + price[i]`
- `rest[i] = max(rest[i-1], sold[i-1])`

Answer: `max(sold[n-1], rest[n-1])`.



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



**Complexity** — Time **O(n)**; Space **O(1)**.

## Related problems

- [Best Time to Buy and Sell Stock IV](/problems/best-time-to-buy-and-sell-stock-iv) — at most k transactions
- [Best Time to Buy and Sell Stock with Transaction Fee](/problems/best-time-to-buy-and-sell-stock-with-transaction-fee)
- [Best Time to Buy and Sell Stock](/problems/best-time-to-buy-and-sell-stock) — single transaction
