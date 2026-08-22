# DP — Best Time to Buy and Sell Stock IV

*[↗ LeetCode: Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

At most `k` transactions. Max profit.

## Approach 1 — Full DP `dp[i][t][0/1]`

`dp[i][t][held?]`. Transitions:
- `dp[i][t][0] = max(dp[i-1][t][0], dp[i-1][t][1] + price[i])`
- `dp[i][t][1] = max(dp[i-1][t][1], dp[i-1][t-1][0] - price[i])`

Answer `dp[n-1][k][0]`. Space **O(n·k)** or **O(k)** with row-compression.

## Approach 2 — Optimization: k ≥ n/2 → unlimited

**Insight.** With that many allowed transactions we can capture every increasing step → sum of positive diffs.

```java
int maxProfit(int k, int[] prices) {
    int n = prices.length;
    if (k >= n / 2) {
        int sum = 0;
        for (int i = 1; i < n; i++) if (prices[i] > prices[i - 1]) sum += prices[i] - prices[i - 1];
        return sum;
    }
    int[] buy = new int[k + 1], sell = new int[k + 1];
    Arrays.fill(buy, Integer.MIN_VALUE);
    for (int p : prices)
        for (int t = 1; t <= k; t++) {
            buy[t] = Math.max(buy[t], sell[t - 1] - p);
            sell[t] = Math.max(sell[t], buy[t] + p);
        }
    return sell[k];
}
```

**Complexity** — Time **O(n · k)**; Space **O(k)**.

## Related problems

- [With Cooldown](/problems/best-time-to-buy-and-sell-stock-with-cooldown)
- [With Transaction Fee](/problems/best-time-to-buy-and-sell-stock-with-transaction-fee)
- [Best Time to Buy and Sell Stock III](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/) — k=2
