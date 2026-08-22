# Backtracking — Combination Sum IV

*[↗ LeetCode: Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Count of ordered combinations of `nums` summing to `target`. `[1,2]` and `[2,1]` are distinct.

> Filed under Backtracking but the intended solution is **DP** — order matters, so we count sequences, not subsets.

---

## Approach 1 — Backtracking
Enumerate all sequences. Blows up: for target=1000 and nums=[1,2,3], count is astronomical → TLE.

---

## Approach 2 — DP (coin-change permutations)
**Insight.** `dp[t] = Σ dp[t - x]` for each `x ∈ nums`. Outer loop is target; inner is nums — this counts ordered sequences.

```java
int combinationSum4(int[] nums, int target) {
    int[] dp = new int[target + 1];
    dp[0] = 1;
    for (int t = 1; t <= target; t++)
        for (int x : nums)
            if (x <= t) dp[t] += dp[t - x];
    return dp[target];
}
```

**Trap.** Java `int` may overflow — problem guarantees fits, but if unsure use `long` and check.

**Complexity** — Time **O(target · n)**; Space **O(target)**.

**Follow-up.** If we wanted unordered (like [Coin Change II](/problems/coin-change-ii)), swap loop order: outer nums, inner target.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Backtracking | — | — | baseline |
| DP (coin-change permutations) | O(target · n) | O(target) | optimum |

## When to use which

- **State it for signal** → Backtracking (—). Correct baseline; call it out then move on.
- **Ship this** → DP (coin-change permutations) (O(target · n), O(target)). Expected optimum in interview.

## Related problems

- [Coin Change II](/problems/coin-change-ii) — unordered
- [Combination Sum](https://leetcode.com/problems/combination-sum/) — subsets, unbounded
