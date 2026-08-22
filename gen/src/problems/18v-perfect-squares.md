# DP — Perfect Squares

*[↗ LeetCode: Perfect Squares](https://leetcode.com/problems/perfect-squares/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Min count of perfect squares summing to `n`.

**Example 1** — `n=12` → `3` (`4+4+4`)
**Example 2** — `n=13` → `2` (`4+9`)

**Constraints** — `1 ≤ n ≤ 10⁴`.

---

## Approach 1 — DP (min coin change with square coins)

`dp[i] = 1 + min(dp[i - k²])` over `k² ≤ i`.

```java
int numSquares(int n) {
    int[] dp = new int[n + 1];
    Arrays.fill(dp, Integer.MAX_VALUE);
    dp[0] = 0;
    for (int i = 1; i <= n; i++)
        for (int k = 1; k * k <= i; k++)
            if (dp[i - k*k] != Integer.MAX_VALUE)
                dp[i] = Math.min(dp[i], dp[i - k*k] + 1);
    return dp[n];
}
```

**Complexity** — Time **O(n · √n)**; Space **O(n)**.

## Approach 2 — Lagrange's four-square theorem
Every positive integer = sum of ≤ 4 squares. Result ∈ {1,2,3,4}.
- 1 iff n is perfect square.
- 4 iff `n = 4^k · (8m + 7)`.
- Else check if `n = a² + b²` → 2; else 3.

**O(√n).** Beat the DP.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DP | O(n · √n) | O(n) | canonical |
| Lagrange | **O(√n)** | O(1) | polish |

## When to use which

- **Interview** → DP first.
- **"Fast bound"** → Lagrange trick.
- **Return the squares** → DP with parent pointers.

## Related problems

- [Coin Change](/problems/coin-change)
- [Word Break](https://leetcode.com/problems/word-break/)
