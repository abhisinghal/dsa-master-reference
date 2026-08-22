# Greedy — Best Time to Buy and Sell Stock

*[↗ LeetCode: Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/greedy)

At most one buy + one sell. Max profit.

---

## Approach 1 — Compare every pair O(n²)

---

## Approach 2 — Track running minimum
**Insight.** Maximum profit if selling on day `i` is `prices[i] - minPrice(0..i-1)`.



```java
int maxProfit(int[] prices) {
    int min = Integer.MAX_VALUE, best = 0;
    for (int p : prices) {
        min = Math.min(min, p);
        best = Math.max(best, p - min);
    }
    return best;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Compare every pair O(n²) | — | — | baseline |
| Track running minimum | O(n) | O(1) | optimum |

## When to use which

- **State it for signal** → Compare every pair O(n²) (—). Correct baseline; call it out then move on.
- **Ship this** → Track running minimum (O(n), O(1)). Expected optimum in interview.

## Related problems

- [Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) — unlimited transactions, greedy sum of positives
- [Best Time to Buy and Sell Stock III / IV](/problems/best-time-to-buy-and-sell-stock-iv) — at most k transactions, DP
- [With Cooldown](/problems/best-time-to-buy-and-sell-stock-with-cooldown) — state machine DP
- [With Transaction Fee](/problems/best-time-to-buy-and-sell-stock-with-transaction-fee) — state machine DP
