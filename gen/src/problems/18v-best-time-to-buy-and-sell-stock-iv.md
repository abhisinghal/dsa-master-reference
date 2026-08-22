# DP — Best Time to Buy and Sell Stock IV

*[↗ LeetCode: Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

At most `k` transactions. Max profit.

**Constraints** — `1 ≤ k ≤ 100`; `1 ≤ n ≤ 1000`.

---

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

**Complexity** — Time **O(n · k)**; Space **O(k)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| 2k states DP | **O(n · k)** | O(k) | canonical |

## When to use which

- **Fixed k** → 2k states.
- **k unlimited** → sum positive diffs.

## Related problems

- [With Cooldown](/problems/best-time-to-buy-and-sell-stock-with-cooldown)
- [With Transaction Fee](/problems/best-time-to-buy-and-sell-stock-with-transaction-fee)
- [Best Time to Buy and Sell Stock III](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/)
