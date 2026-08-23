# Backtracking — Combination Sum IV

*[↗ LeetCode: Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Count ordered sequences of `nums` summing to `target`. `[1,2]` and `[2,1]` are distinct.

**Example 1** — `nums=[1,2,3], target=4` → `7`
**Example 2** — `nums=[9], target=3` → `0`

**Constraints** — `1 ≤ n ≤ 200`.

---

## Approach 1 — Backtracking

Exponential. TLE.

## Approach 2 — DP (coin-change permutations, canonical)

**Insight.** `dp[t] = Σ dp[t - x]` for `x ∈ nums`. Outer loop is target; inner is nums — this counts **ordered** sequences.



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



<CodeTrace
  title="Backtracking"
  :values="['1', '2', '3']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Contrast.** Loop order swap counts **unordered** (see [Coin Change II](/problems/coin-change-ii)).

**Trap** — may overflow — problem guarantees fits in int; if unsure use `long`.

**Complexity** — Time **O(target · n)**; Space **O(target)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Backtracking | exponential | O(target) | baseline |
| DP | **O(target · n)** | O(target) | canonical |

## When to use which

- **Ordered** → outer target, inner nums.
- **Unordered** → outer nums, inner target.
- **"Enumerate sequences"** → backtracking, not DP.

## Related problems

- [Coin Change](/problems/coin-change)
- [Coin Change II](/problems/coin-change-ii)
- [Combination Sum](https://leetcode.com/problems/combination-sum/)
