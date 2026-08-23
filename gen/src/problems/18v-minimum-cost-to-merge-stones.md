# DP — Minimum Cost to Merge Stones

*[↗ LeetCode: Minimum Cost to Merge Stones](https://leetcode.com/problems/minimum-cost-to-merge-stones/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

Merge exactly k consecutive piles at a time; cost = sum. Min total to merge all into one. `-1` if impossible.

**Example 1** — `stones=[3,2,4,1], k=2` → `20`

**Constraints** — `1 ≤ n ≤ 30`; `2 ≤ k ≤ 30`.

---

## Approach — Interval DP with residue trick (canonical)

**Insight.** Feasible iff `(n-1) % (k-1) == 0`. `dp[i][j]` = min cost to reduce to `((j-i) mod (k-1)) + 1` piles.

```java
int mergeStones(int[] stones, int k) {
    int n = stones.length;
    if ((n - 1) % (k - 1) != 0) return -1;
    int[] pref = new int[n + 1];
    for (int i = 0; i < n; i++) pref[i+1] = pref[i] + stones[i];
    int[][] dp = new int[n][n];
    for (int len = k; len <= n; len++)
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            dp[i][j] = Integer.MAX_VALUE;
            for (int m = i; m < j; m += k - 1)
                dp[i][j] = Math.min(dp[i][j], dp[i][m] + dp[m+1][j]);
            if ((j - i) % (k - 1) == 0) dp[i][j] += pref[j+1] - pref[i];
        }
    return dp[0][n-1];
}
```

<CodeTrace
  title="Interval DP with residue trick (canonical)"
  :values="['3', '2', '4', '1']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n³ / k)**; Space **O(n²)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Interval DP + residue | **O(n³/k)** | O(n²) | canonical |

## When to use which

- **Merge k at a time** → residue trick.
- **k=2** → merge sort merging pattern.
- **Optimal binary search tree** — similar interval DP.

## Related problems

- [Burst Balloons](/problems/burst-balloons)
