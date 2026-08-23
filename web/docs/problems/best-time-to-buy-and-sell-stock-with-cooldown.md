# DP — Best Time to Buy and Sell Stock with Cooldown

*[↗ LeetCode: Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Unlimited transactions; must skip one day between sell and next buy.

**Example 1** — `prices=[1,2,3,0,2]` → `3`

**Constraints** — `1 ≤ n ≤ 5000`.

---

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

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| State machine DP | **O(n)** | O(1) | canonical |

## When to use which

- **Cooldown** → 3 states.
- **Fee** → 2 states.
- **k transactions** → 2k states.

## Related problems

- [Best Time to Buy and Sell Stock IV](/problems/best-time-to-buy-and-sell-stock-iv)
- [With Transaction Fee](/problems/best-time-to-buy-and-sell-stock-with-transaction-fee)
