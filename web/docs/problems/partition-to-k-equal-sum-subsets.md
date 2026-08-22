# DP — Partition to K Equal Sum Subsets

*[↗ LeetCode: Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Can we split nums into k non-empty subsets each summing to `total/k`?

## Approach 1 — Backtracking with sort-desc + pruning

Sort desc; try to place each number into one of k buckets; skip mirrored empty buckets to avoid re-exploring.

## Approach 2 — Bitmask DP

**Insight.** `dp[mask]` = min "leftover" sum of the current partially-filled bucket after using elements in mask. Transition: for each unused element `i`, add it to the current bucket if it fits (leftover + nums[i] ≤ target). When a bucket fills, reset leftover to 0.



```java
boolean canPartitionKSubsets(int[] nums, int k) {
    int total = 0;
    for (int x : nums) total += x;
    if (total % k != 0) return false;
    int target = total / k;
    int n = nums.length, full = 1 << n;
    int[] dp = new int[full];
    Arrays.fill(dp, -1);
    dp[0] = 0;
    for (int mask = 0; mask < full; mask++) {
        if (dp[mask] < 0) continue;
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) continue;
            if (dp[mask] + nums[i] > target) continue;
            int nm = mask | (1 << i);
            dp[nm] = (dp[mask] + nums[i]) % target;
        }
    }
    return dp[full - 1] == 0;
}
```



**Complexity** — Time **O(n · 2ⁿ)**; Space **O(2ⁿ)** — n ≤ 16.

## Related problems

- [Partition Equal Subset Sum](/problems/partition-equal-subset-sum) — k=2
- [Number of Ways to Wear Different Hats](/problems/number-of-ways-to-wear-different-hats) — bitmask DP
- [Beautiful Arrangement](/problems/beautiful-arrangement)
