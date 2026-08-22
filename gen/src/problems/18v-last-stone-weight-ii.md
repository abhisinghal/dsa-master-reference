# DP — Last Stone Weight II

*[↗ LeetCode: Last Stone Weight II](https://leetcode.com/problems/last-stone-weight-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Smash pairs; if equal both destroyed; else larger becomes diff. Minimize final remaining stone weight.

---

## Approach 1 — Reduce to subset-sum closest to sum/2
**Insight.** Every stone is signed ±. Result = |sum(+) - sum(-)| = |total - 2·subsetSum|. Minimize by picking subset closest to `total/2`. Standard 0/1 knapsack on booleans.

```java
int lastStoneWeightII(int[] stones) {
    int total = 0;
    for (int x : stones) total += x;
    int half = total / 2;
    boolean[] dp = new boolean[half + 1];
    dp[0] = true;
    for (int x : stones)
        for (int j = half; j >= x; j--)
            dp[j] |= dp[j - x];
    for (int j = half; j >= 0; j--)
        if (dp[j]) return total - 2 * j;
    return 0;
}
```

**Complexity** — Time **O(n · total)**; Space **O(total)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Reduce to subset-sum closest to sum/2 | O(n · total) | O(total) | primary |

## When to use which

- **Ship this** → Reduce to subset-sum closest to sum/2 (O(n · total), O(total)). The pattern's standard solution.

## Related problems

- [Partition Equal Subset Sum](/problems/partition-equal-subset-sum) — same reduction
- [Target Sum](/problems/target-sum)
- [Last Stone Weight I](https://leetcode.com/problems/last-stone-weight/) — heap simulation
