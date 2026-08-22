# DP — Perfect Squares

*[↗ LeetCode: Perfect Squares](https://leetcode.com/problems/perfect-squares/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Min count of perfect squares summing to `n`.

## Approach 1 — DP (min coin change, coins = squares)

**Insight.** Standard unbounded-min-coin: `dp[i] = 1 + min(dp[i - k²])` over all `k² ≤ i`.

```java
int numSquares(int n) {
    int[] dp = new int[n + 1];
    Arrays.fill(dp, Integer.MAX_VALUE);
    dp[0] = 0;
    for (int i = 1; i <= n; i++)
        for (int k = 1; k * k <= i; k++)
            if (dp[i - k * k] != Integer.MAX_VALUE)
                dp[i] = Math.min(dp[i], dp[i - k * k] + 1);
    return dp[n];
}
```

**Complexity** — Time **O(n · √n)**; Space **O(n)**.

## Approach 2 — Lagrange's four-square theorem

Every positive integer = sum of ≤ 4 squares. Result is always in `{1, 2, 3, 4}`.
- 1 iff n is a perfect square.
- 4 iff n = 4^k · (8m + 7) (Legendre's three-square theorem).
- Else check if n = a² + b² for some a, b → return 2; else return 3.

**O(√n)** — beat the DP.

## Related problems

- [Coin Change](/problems/coin-change) — min-count with arbitrary coins
- [Word Break](https://leetcode.com/problems/word-break/)
