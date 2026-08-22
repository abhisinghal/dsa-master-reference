# DP — Target Sum

*[↗ LeetCode: Target Sum](https://leetcode.com/problems/target-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Assign + or − to each `nums[i]`; count ways to reach `target`.

**Example 1** — `nums=[1,1,1,1,1], target=3` → `5`
**Example 2** — `nums=[1], target=1` → `1`

**Constraints** — `1 ≤ n ≤ 20`.

---

## Approach 1 — Backtracking
O(2ⁿ). Baseline.

## Approach 2 — Reduce to subset-sum count (canonical)

**Insight.** `P - N = target`, `P + N = total` → `P = (total + target) / 2`. Count subsets summing to P.

```java
int findTargetSumWays(int[] nums, int target) {
    int total = 0; for (int x : nums) total += x;
    if (Math.abs(target) > total || (total + target) % 2 != 0) return 0;
    int P = (total + target) / 2;
    int[] dp = new int[P + 1];
    dp[0] = 1;
    for (int x : nums)
        for (int j = P; j >= x; j--)
            dp[j] += dp[j - x];
    return dp[P];
}
```

**Complexity** — Time **O(n · P)**; Space **O(P)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Backtracking | O(2ⁿ) | O(n) | baseline |
| Reduce + subset-sum | **O(n · P)** | O(P) | canonical |

## When to use which

- **± assignment counting** → reduce to subset-sum.
- **Return the assignment** → track parent choices.

## Related problems

- [Partition Equal Subset Sum](/problems/partition-equal-subset-sum)
- [Coin Change II](/problems/coin-change-ii)
