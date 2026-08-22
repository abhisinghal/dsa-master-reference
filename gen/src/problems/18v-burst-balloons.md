# DP — Burst Balloons

*[↗ LeetCode: Burst Balloons](https://leetcode.com/problems/burst-balloons/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

Burst balloons; when bursting `i`, gain `nums[l] * nums[i] * nums[r]` where l, r are alive neighbors. Maximize coins.

## Approach — Interval DP with "last to burst" trick

**Insight.** Directly modeling "first to burst" fails — the neighbors change unpredictably. Instead, think of `i` as the **last** balloon burst in the range `(l, r)` (open interval): its neighbors at that moment are `nums[l]` and `nums[r]` — fixed! Then subproblems `(l, i)` and `(i, r)` are independent.

Padding: prepend and append `1` so the base "neighbors" are always defined.

```java
int maxCoins(int[] nums) {
    int n = nums.length;
    int[] a = new int[n + 2];
    a[0] = a[n + 1] = 1;
    for (int i = 0; i < n; i++) a[i + 1] = nums[i];
    int[][] dp = new int[n + 2][n + 2];
    for (int len = 2; len <= n + 1; len++)
        for (int l = 0; l + len <= n + 1; l++) {
            int r = l + len;
            for (int k = l + 1; k < r; k++)
                dp[l][r] = Math.max(dp[l][r], dp[l][k] + dp[k][r] + a[l] * a[k] * a[r]);
        }
    return dp[0][n + 1];
}
```

**Complexity** — Time **O(n³)**; Space **O(n²)**.

## Related problems

- [Minimum Cost to Merge Stones](/problems/minimum-cost-to-merge-stones) — interval DP with k-groupings
- [Matrix Chain Multiplication] — canonical interval DP
- [Palindrome Partitioning II](/problems/palindrome-partitioning-ii)
