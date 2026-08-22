# DP — Number of Ways to Wear Different Hats to Each Other

*[↗ LeetCode: Number of Ways to Wear Different Hats to Each Other](https://leetcode.com/problems/number-of-ways-to-wear-different-hats-to-each-other/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

`n` people (n ≤ 10), 40 hats. Each person has a preference list. Each hat used by ≤ 1 person; each person wears exactly one hat. Count assignments (mod 1e9+7).

---

## Approach 1 — Bitmask DP over people, iterate hats
**Insight.** Iterate hats (there are more of them but each contributes only if some person likes it). `dp[h][mask]` = # ways to satisfy people in mask using hats `1..h`. Transition:
- Skip hat h: `dp[h][mask] += dp[h-1][mask]`.
- Give hat h to any person p in mask who likes it: `dp[h][mask] += dp[h-1][mask ^ (1 << p)]`.

Answer: `dp[40][fullMask]`.

```java
int MOD = 1_000_000_007;
int numberWays(List<List<Integer>> hats) {
    int n = hats.size(), full = 1 << n;
    List<List<Integer>> hatToPeople = new ArrayList<>();
    for (int i = 0; i <= 40; i++) hatToPeople.add(new ArrayList<>());
    for (int p = 0; p < n; p++)
        for (int h : hats.get(p)) hatToPeople.get(h).add(p);
    int[] dp = new int[full];
    dp[0] = 1;
    for (int h = 1; h <= 40; h++) {
        int[] nd = dp.clone();
        for (int mask = 0; mask < full; mask++) {
            for (int p : hatToPeople.get(h))
                if ((mask & (1 << p)) == 0)
                    nd[mask | (1 << p)] = (nd[mask | (1 << p)] + dp[mask]) % MOD;
        }
        dp = nd;
    }
    return dp[full - 1];
}
```

**Complexity** — Time **O(40 · 2ⁿ · n)**; Space **O(2ⁿ)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Bitmask DP over people, iterate hats | O(40 · 2ⁿ · n) | O(2ⁿ) | primary |

## When to use which

- **Ship this** → Bitmask DP over people, iterate hats (O(40 · 2ⁿ · n), O(2ⁿ)). The pattern's standard solution.

## Related problems

- [Beautiful Arrangement](/problems/beautiful-arrangement) — bitmask DP
- [Partition to K Equal Sum Subsets](/problems/partition-to-k-equal-sum-subsets)
- [Shortest Path Visiting All Nodes](/problems/shortest-path-visiting-all-nodes)
