# DP — Best Time to Buy and Sell Stock with Transaction Fee

*[↗ LeetCode: Best Time to Buy and Sell Stock with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Unlimited transactions; each sell pays `fee`. Max profit.

**Example 1** — `prices=[1,3,2,8,4,9], fee=2` → `8`

**Constraints** — `1 ≤ n ≤ 5·10⁴`.

---

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

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| State machine DP | **O(n)** | O(1) | canonical |

## When to use which

- **Fee on transaction** → 2 states.
- **Cooldown** → 3 states.

## Related problems

- [With Cooldown](/problems/best-time-to-buy-and-sell-stock-with-cooldown)
- [Best Time to Buy and Sell Stock IV](/problems/best-time-to-buy-and-sell-stock-iv)
