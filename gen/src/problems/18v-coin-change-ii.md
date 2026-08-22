# DP — Coin Change II

*[↗ LeetCode: Coin Change II](https://leetcode.com/problems/coin-change-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Count the number of ways to make `amount` from coins (unlimited each, **unordered**).

## Approach — Unbounded knapsack counting

**Insight.** Loop coins OUTER, amount INNER — this counts **unordered** combinations (each coin's contribution is fixed in order).

```java
int change(int amount, int[] coins) {
    int[] dp = new int[amount + 1];
    dp[0] = 1;
    for (int c : coins)
        for (int t = c; t <= amount; t++)
            dp[t] += dp[t - c];
    return dp[amount];
}
```

**Contrast.** If you swap loop order (amount outer, coins inner), you count **ordered** sequences → that's [Combination Sum IV](/problems/combination-sum-iv).

**Complexity** — Time **O(amount · |coins|)**; Space **O(amount)**.

## Related problems

- [Coin Change](/problems/coin-change) — min coins, not count
- [Combination Sum IV](/problems/combination-sum-iv) — ordered version
- [Perfect Squares](/problems/perfect-squares)
