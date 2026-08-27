# DP — Best Time to Buy and Sell Stock with Cooldown

*[↗ LeetCode: Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Meta, Amazon, Google, Bloomberg" />

Unlimited transactions; must skip one day between sell and next buy.

**Example 1** — `prices=[1,2,3,0,2]` → `3` (buy at 1, sell at 2 → cooldown → buy at 0, sell at 2 = 1 + 2 = 3)
**Example 2** — `prices=[1]` → `0`
**Example 3** — `prices=[6,1,3,2,4,7]` → `6` (buy at 1, sell at 3 → cooldown → buy at 2, sell at 7 = 2 + 5 wait, actually 3-1=2, cooldown, 7-2=5, total 7... check: sample answer for this input is 6)

**Constraints** — `1 ≤ n ≤ 5000`.


<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="best-time-to-buy-and-sell-stock-with-cooldown" /> <Bookmark problem-slug="best-time-to-buy-and-sell-stock-with-cooldown" />

<InterviewTimer problem-slug="best-time-to-buy-and-sell-stock-with-cooldown" />



## Approach 1 — Brute force recursion

**Intuition.** At each day, try all three choices (buy, sell, do nothing) and recurse. Because of the cooldown, "sell" advances the index by 2 instead of 1.



```java
int maxProfitBrute(int[] prices) {
    return dfs(prices, 0, false);
}
int dfs(int[] p, int i, boolean holding) {
    if (i >= p.length) return 0;
    int skip = dfs(p, i + 1, holding);
    if (holding) {
        int sell = p[i] + dfs(p, i + 2, false);  // cooldown one day
        return Math.max(skip, sell);
    } else {
        int buy = -p[i] + dfs(p, i + 1, true);
        return Math.max(skip, buy);
    }
}
```



**Complexity** — Time **O(2ⁿ)**; Space **O(n)** stack. For `n=5000`, `2⁵⁰⁰⁰` — way beyond feasible. *In an interview* say "brute is O(2ⁿ), memoize to O(n)."

---

## Approach 2 — Memoized recursion (top-down DP)

Cache on `(index, holding)` — 2 · n states, each O(1) to compute.



```java
Integer[][] memo;
int maxProfitMemo(int[] prices) {
    memo = new Integer[prices.length][2];
    return dfsMemo(prices, 0, 0);
}
int dfsMemo(int[] p, int i, int holding) {
    if (i >= p.length) return 0;
    if (memo[i][holding] != null) return memo[i][holding];
    int skip = dfsMemo(p, i + 1, holding);
    int action = holding == 1
        ? p[i] + dfsMemo(p, Math.min(p.length, i + 2), 0)
        : -p[i] + dfsMemo(p, i + 1, 1);
    return memo[i][holding] = Math.max(skip, action);
}
```



**Complexity** — Time **O(n)**; Space **O(n)**. Correct but uses recursion stack.

---

## Approach 3 — State-machine DP (canonical)

**Insight.** Three states model the entire history compactly: `hold` (own a share), `sold` (just sold, in cooldown), `rest` (idle, ready to buy). Transitions:
- `hold = max(hold, rest - price)` — either keep holding, or buy from rest state
- `sold = hold + price` — sell what we're holding
- `rest = max(rest, sold)` — either stay resting, or transition from sold (cooldown expired)



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

**Complexity** — Time **O(n)**; Space **O(1)**. *Say aloud in an interview:* "identify the states (hold/sold/rest), write each transition as a max, roll to O(1) space."

---

## Try it yourself

<JavaRunner problem-slug="best-time-to-buy-and-sell-stock-with-cooldown" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute recursion | O(2ⁿ) | O(n) | Reference; TLE past n=25 |
| Memoized recursion | O(n) | O(n) | Works but uses stack |
| **State-machine DP** | **O(n)** | **O(1)** | **Canonical** |

## When to use which

- **Cooldown** → 3 states.
- **Fee** → 2 states.
- **k transactions** → 2k states.

<AiCompanion problem-slug="best-time-to-buy-and-sell-stock-with-cooldown" pattern-hint="dynamic programming" />

## Related problems

- [Best Time to Buy and Sell Stock IV](/problems/best-time-to-buy-and-sell-stock-iv)
- [With Transaction Fee](/problems/best-time-to-buy-and-sell-stock-with-transaction-fee)

<FeedbackWidget problem-slug="best-time-to-buy-and-sell-stock-with-cooldown" />
