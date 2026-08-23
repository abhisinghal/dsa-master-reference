# Greedy — Best Time to Buy and Sell Stock

*[↗ LeetCode: Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/greedy)

At most one buy + one sell. Max profit.

**Example 1** — `prices=[7,1,5,3,6,4]` → `5`
**Example 2** — `prices=[7,6,4,3,1]` → `0`

**Constraints** — `1 ≤ n ≤ 10⁵`.

---

## Approach 1 — Compare every pair

O(n²). Baseline.

## Approach 2 — Track running minimum (canonical)

**Insight.** Max profit if selling on day `i` = `prices[i] - min(prices[0..i-1])`.



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



<CodeTrace
  title="Min tracking — prices=[7,1,5,3,6,4]"
  :values="['7','1','5','3','6','4']"
  :windowKeys="['i']"
  :cellWidth="30"
  :steps='[
    { pointers: { i: 1 }, vars: { min: 1, best: 0 }, note: "" },
    { pointers: { i: 4 }, vars: { min: 1, best: 5 }, note: "" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Pairs | O(n²) | O(1) | baseline |
| Min tracking | **O(n)** | O(1) | canonical |

## When to use which

- **Single transaction** → min tracking.
- **Unlimited transactions** → sum positive diffs (see [Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)).
- **k transactions** → DP (see [Stock IV](/problems/best-time-to-buy-and-sell-stock-iv)).

## Related problems

- [Best Time to Buy and Sell Stock IV](/problems/best-time-to-buy-and-sell-stock-iv)
- [With Cooldown](/problems/best-time-to-buy-and-sell-stock-with-cooldown)
- [With Transaction Fee](/problems/best-time-to-buy-and-sell-stock-with-transaction-fee)
