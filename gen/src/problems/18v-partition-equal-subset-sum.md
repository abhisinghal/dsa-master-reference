# DP — Partition Equal Subset Sum

*[↗ LeetCode: Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Can `nums` be split into two subsets with equal sum?

---

## Approach 1 — Subset-sum DP (0/1 knapsack)
**Insight.** Equal partition possible iff sum is even and a subset sums to `sum/2`. Standard 0/1 knapsack on booleans.

```java
boolean canPartition(int[] nums) {
    int sum = 0;
    for (int x : nums) sum += x;
    if (sum % 2 == 1) return false;
    int t = sum / 2;
    boolean[] dp = new boolean[t + 1];
    dp[0] = true;
    for (int x : nums)
        for (int j = t; j >= x; j--)
            dp[j] |= dp[j - x];
    return dp[t];
}
```

**Trap.** Iterate `j` **descending** — the 0/1 knapsack idiom that prevents an item from being counted twice.

**Complexity** — Time **O(n · sum)**; Space **O(sum)**.

## Bitset optimization

Represent `dp` as a `BitSet` (java.util.BitSet); each item is `dp |= dp << x` → speedup by word-size factor.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Subset-sum DP (0/1 knapsack) | O(n · sum) | O(sum) | primary |

## When to use which

- **Ship this** → Subset-sum DP (0/1 knapsack) (O(n · sum), O(sum)). The pattern's standard solution.

## Related problems

- [Target Sum](/problems/target-sum) — reduces to this
- [Last Stone Weight II](/problems/last-stone-weight-ii) — variant
- [Partition to K Equal Sum Subsets](/problems/partition-to-k-equal-sum-subsets) — bitmask DP
