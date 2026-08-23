# DP — Number of Ways to Wear Different Hats to Each Other

*[↗ LeetCode: Number of Ways to Wear Different Hats to Each Other](https://leetcode.com/problems/number-of-ways-to-wear-different-hats-to-each-other/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

n people (≤ 10), 40 hats. Each person has preferences. Each hat used by ≤ 1 person; each person wears one. Count assignments (mod 1e9+7).

**Constraints** — `1 ≤ n ≤ 10`.

**Example 1** — `hats=[[3,4],[4,5],[5]]` → `1`
**Example 2** — `hats=[[3,5,1],[3,5]]` → `4`
**Example 3** — `hats=[[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]` → `24`

---

## Approach — Bitmask DP iterating hats (canonical)

**Insight.** `dp[h][mask]` = # ways to satisfy people in mask using hats 1..h. Transition: skip hat h, or give it to any person p in mask who likes it.



```java
int MOD = 1_000_000_007;
int numberWays(List<List<Integer>> hats) {
    int n = hats.size(), full = 1 << n;
    List<List<Integer>> hatToPeople = new ArrayList<>();
    for (int i = 0; i <= 40; i++) hatToPeople.add(new ArrayList<>());
    for (int p = 0; p < n; p++) for (int h : hats.get(p)) hatToPeople.get(h).add(p);
    int[] dp = new int[full];
    dp[0] = 1;
    for (int h = 1; h <= 40; h++) {
        int[] nd = dp.clone();
        for (int mask = 0; mask < full; mask++)
            for (int p : hatToPeople.get(h))
                if ((mask & (1 << p)) == 0)
                    nd[mask | (1 << p)] = (nd[mask | (1 << p)] + dp[mask]) % MOD;
        dp = nd;
    }
    return dp[full - 1];
}
```



**Complexity** — Time **O(40 · 2ⁿ · n)**; Space **O(2ⁿ)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Bitmask over people | **O(40·2ⁿ·n)** | O(2ⁿ) | canonical |

## When to use which

- **Small n (≤ 10), large "items" domain** → iterate items, mask people.
- **Small items, large people** → reverse.

## Related problems

- [Beautiful Arrangement](/problems/beautiful-arrangement)
- [Partition to K Equal Sum Subsets](/problems/partition-to-k-equal-sum-subsets)