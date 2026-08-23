# DP — Partition to K Equal Sum Subsets

*[↗ LeetCode: Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

&lt;CompanyTags companies="Meta, Amazon, Google" /&gt;

Split nums into k subsets each summing to `total/k`.

**Example 1** — `nums=[4,3,2,3,5,2,1], k=4` → `true`
**Example 2** — `nums=[1,2,3,4], k=3` → `false`

**Constraints** — `1 ≤ n ≤ 16`.


&lt;Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/&gt;
---

## Approach 1 — Backtracking with sort-desc + pruning
Sort desc; place each into buckets; skip mirrored-empty.

## Approach 2 — Bitmask DP (canonical for n ≤ 16)

**Insight.** `dp[mask]` = min "leftover" sum of current bucket after using mask elements. Transition: try adding each unused element if it fits.



```java
boolean canPartitionKSubsets(int[] nums, int k) {
    int total = 0; for (int x : nums) total += x;
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



<CodeTrace
  title="Backtracking with sort-desc + pruning"
  :values="['4', '3', '2', '3', '5', '2', '1']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 3 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 6 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n · 2ⁿ)**; Space **O(2ⁿ)**.

---

## Try it yourself

<JavaRunner problem-slug="partition-to-k-equal-sum-subsets" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Backtracking + sort desc | worst exp | O(k) | works |
| Bitmask DP | **O(n · 2ⁿ)** | O(2ⁿ) | canonical for n ≤ 16 |

## When to use which

- **n ≤ 16** → bitmask DP.
- **Larger n** → backtracking with heavy pruning.
- **k=2** → simpler [Partition Equal Subset Sum](/problems/partition-equal-subset-sum).

## Related problems

- [Partition Equal Subset Sum](/problems/partition-equal-subset-sum)
- [Number of Ways to Wear Different Hats](/problems/number-of-ways-to-wear-different-hats-to-each-other)
- [Beautiful Arrangement](/problems/beautiful-arrangement)