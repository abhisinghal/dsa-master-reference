# DP — Partition Equal Subset Sum

*[↗ LeetCode: Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Can `nums` split into two subsets with equal sum?

**Example 1** — `nums=[1,5,11,5]` → `true`
**Example 2** — `nums=[1,2,3,5]` → `false`

**Constraints** — `1 ≤ n ≤ 200`.

---

## Approach — Subset-sum DP (0/1 knapsack, canonical)

**Insight.** Possible iff sum even AND a subset sums to `sum/2`.

**Trap** — iterate `j` **descending** for 0/1 knapsack.

```java
boolean canPartition(int[] nums) {
    int sum = 0; for (int x : nums) sum += x;
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

**Complexity** — Time **O(n · sum)**; Space **O(sum)**.

## BitSet speedup
`dp |= dp << x` on `BitSet` — word-parallel.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| 0/1 knapsack DP | **O(n · sum)** | O(sum) | canonical |
| BitSet | O(n · sum / 64) | O(sum) | polish |

## When to use which

- **Two equal subsets** → this.
- **k subsets** → [Partition to K Equal Sum Subsets](/problems/partition-to-k-equal-sum-subsets).
- **Return the partition** → track parent choices.

## Related problems

- [Target Sum](/problems/target-sum)
- [Last Stone Weight II](/problems/last-stone-weight-ii)
- [Partition to K Equal Sum Subsets](/problems/partition-to-k-equal-sum-subsets)
