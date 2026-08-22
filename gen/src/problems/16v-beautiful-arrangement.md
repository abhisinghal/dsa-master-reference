# Backtracking — Beautiful Arrangement

*[↗ LeetCode: Beautiful Arrangement](https://leetcode.com/problems/beautiful-arrangement/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

Count permutations of 1..n where for every position `i` (1-indexed), `a[i] % i == 0` or `i % a[i] == 0`.

---

## Approach 1 — Backtracking with used-mask
```java
int countArrangement(int n) {
    return dfs(n, 1, new boolean[n + 1]);
}
int dfs(int n, int pos, boolean[] used) {
    if (pos > n) return 1;
    int count = 0;
    for (int v = 1; v <= n; v++)
        if (!used[v] && (v % pos == 0 || pos % v == 0)) {
            used[v] = true;
            count += dfs(n, pos + 1, used);
            used[v] = false;
        }
    return count;
}
```

---

## Approach 2 — Bitmask DP (n ≤ 15)
`dp[mask]` = # ways to fill first `popcount(mask)` positions using selected numbers.

```java
int countArrangementBM(int n) {
    int full = 1 << n;
    int[] dp = new int[full];
    dp[0] = 1;
    for (int mask = 1; mask < full; mask++) {
        int pos = Integer.bitCount(mask);
        for (int v = 1; v <= n; v++) {
            int bit = 1 << (v - 1);
            if ((mask & bit) == 0) continue;
            if (v % pos == 0 || pos % v == 0) dp[mask] += dp[mask ^ bit];
        }
    }
    return dp[full - 1];
}
```

**Complexity** — Both **O(n · 2ⁿ)** ish; DP is iterative and cleaner for n ≤ 15.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Backtracking with used-mask | — | — | baseline |
| Bitmask DP (n ≤ 15) | O(n · 2ⁿ) | — | optimum |

## When to use which

- **State it for signal** → Backtracking with used-mask (—). Correct baseline; call it out then move on.
- **Ship this** → Bitmask DP (n ≤ 15) (O(n · 2ⁿ), —). Expected optimum in interview.

## Related problems

- [Number of Ways to Wear Different Hats](/problems/number-of-ways-to-wear-different-hats) — bitmask DP
- [Partition to K Equal Sum Subsets](/problems/partition-to-k-equal-sum-subsets)
