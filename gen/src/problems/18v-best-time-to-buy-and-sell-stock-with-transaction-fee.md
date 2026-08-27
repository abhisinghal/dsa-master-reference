# DP — Best Time to Buy and Sell Stock with Transaction Fee

*[↗ LeetCode: Best Time to Buy and Sell Stock with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google, Meta" />

Unlimited transactions; each sell pays `fee`. Max profit.

**Example 1** — `prices=[1,3,2,8,4,9], fee=2` → `8` (buy 1, sell 8 → profit 7-2=5; buy 4, sell 9 → 5-2=3; total 8)
**Example 2** — `prices=[1,3,7,5,10,3], fee=3` → `6`
**Example 3** — `prices=[1,2,3,4,5], fee=1` → `3` (buy 1, sell 5 → 4 - 1 = 3, better than chained trades because fee eats them)

**Constraints** — `1 ≤ n ≤ 5·10⁴`; `0 ≤ fee ≤ 5·10⁴`. For n=5·10⁴, brute force is O(2ⁿ) — the age of the universe. DP fits in 50µs. Brute enumerates 2ⁿ buy/sell subsets — at n=5·10⁴ that's 10¹⁵⁰⁰⁰ ops. State-machine DP is O(n) = 5·10⁴ ops = <5 ms.
<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="best-time-to-buy-and-sell-stock-with-transaction-fee" /> <Bookmark problem-slug="best-time-to-buy-and-sell-stock-with-transaction-fee" />

<InterviewTimer problem-slug="best-time-to-buy-and-sell-stock-with-transaction-fee" />



## Approach 1 — Brute force recursion

**Intuition.** At each day, try buy / sell / skip. Recurse on the remaining prefix.

```java
int maxProfitBrute(int[] prices, int fee) {
    return dfs(prices, fee, 0, false);
}
int dfs(int[] p, int fee, int i, boolean holding) {
    if (i == p.length) return 0;
    int skip = dfs(p, fee, i + 1, holding);
    int action = holding
        ? (p[i] - fee) + dfs(p, fee, i + 1, false)
        : -p[i] + dfs(p, fee, i + 1, true);
    return Math.max(skip, action);
}
```

**Complexity** — Time **O(2ⁿ)**; Space **O(n)** stack. For `n=50000`, universe-age. *In an interview* say "brute is O(2ⁿ), we can memoize on (day, holding) to O(n)."

---

## Approach 2 — State-machine DP (canonical)

**Insight.** Two states — `cash` (idle, no share) and `hold` (own a share). Transitions:
- `hold = max(hold, cash - price)` — either keep holding, or buy from cash
- `cash = max(cash, hold + price - fee)` — either stay idle, or sell (net of fee)

**The fee subtraction happens on sell**, not buy. Convention is arbitrary but must be consistent — if you subtract on buy, `hold` initializes to `-prices[0] - fee`.

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

**Complexity** — Time **O(n)**; Space **O(1)**. *Say aloud in an interview:* "fee is orthogonal to the state count — always 2 states — but it changes the sell transition. If fee > average price swing, it forces fewer, larger transactions."

---

## Try it yourself

<JavaRunner problem-slug="best-time-to-buy-and-sell-stock-with-transaction-fee" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute recursion | O(2ⁿ) | O(n) | Reference; TLE past n=25 |
| **State-machine DP** | **O(n)** | **O(1)** | **Canonical** |

## When to use which

- **Fee on transaction** → 2 states.
- **Cooldown** → 3 states.

<AiCompanion problem-slug="best-time-to-buy-and-sell-stock-with-transaction-fee" pattern-hint="dynamic programming" />

## Related problems

- [With Cooldown](/problems/best-time-to-buy-and-sell-stock-with-cooldown)
- [Best Time to Buy and Sell Stock IV](/problems/best-time-to-buy-and-sell-stock-iv)

<FeedbackWidget problem-slug="best-time-to-buy-and-sell-stock-with-transaction-fee" />
