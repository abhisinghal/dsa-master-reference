# DP — Minimum Cost to Merge Stones

*[↗ LeetCode: Minimum Cost to Merge Stones](https://leetcode.com/problems/minimum-cost-to-merge-stones/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

Merge exactly `k` consecutive piles at a time; cost = sum of merged. Merge all into one; min total cost. Impossible if `(n-1) % (k-1) != 0`.

## Approach — Interval DP with residue trick

**Insight.** `dp[i][j]` = min cost to reduce `stones[i..j]` to `((j-i) mod (k-1)) + 1` piles.
- If we can reduce to 1 pile (`(j-i) % (k-1) == 0`), add `prefix[j+1] - prefix[i]`.
- Split `[i..j]` at some `m` where left reduces to 1 pile and right takes the rest.



```java
int mergeStones(int[] stones, int k) {
    int n = stones.length;
    if ((n - 1) % (k - 1) != 0) return -1;
    int[] pref = new int[n + 1];
    for (int i = 0; i < n; i++) pref[i + 1] = pref[i] + stones[i];
    int[][] dp = new int[n][n];
    for (int len = k; len <= n; len++)
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            dp[i][j] = Integer.MAX_VALUE;
            for (int m = i; m < j; m += k - 1)
                dp[i][j] = Math.min(dp[i][j], dp[i][m] + dp[m + 1][j]);
            if ((j - i) % (k - 1) == 0) dp[i][j] += pref[j + 1] - pref[i];
        }
    return dp[0][n - 1];
}
```



**Complexity** — Time **O(n³ / k)**; Space **O(n²)**.

## Related problems

- [Burst Balloons](/problems/burst-balloons)
- [Stone Game](https://leetcode.com/problems/stone-game/) — interval-DP siblings
