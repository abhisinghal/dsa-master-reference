# DP — Maximum Sum Circular Subarray

*[↗ LeetCode: Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google, Meta" />

Max subarray sum in a **circular** array.

**Example 1** — `nums=[1,-2,3,-2]` → `3` (`[3]`, no wrap)
**Example 2** — `nums=[5,-3,5]` → `10` (wrap: `[5]…[5]`)
**Example 3** — `nums=[-3,-2,-3]` → `-2` (all-negative: must return single largest)

**Constraints** — `1 ≤ n ≤ 3·10⁴`. Brute is O(n²) doubled-array Kadane — 10⁹ ops = TLE. Two-Kadane trick is O(n) = 3·10⁴ ops = <1ms.


<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="maximum-sum-circular-subarray" /> <Bookmark problem-slug="maximum-sum-circular-subarray" />

<InterviewTimer problem-slug="maximum-sum-circular-subarray" />



## Approach 1 — Brute doubled-array Kadane

**Intuition.** Concatenate `nums` with itself, then run Kadane restricted to windows of size ≤ n. O(n²).

**Complexity** — Time **O(n²)**; Space **O(n)**. TLE past n=3000. *In an interview* say "wrap-around = complement of a non-wrap minimum subarray → two-pass Kadane on max and min → O(n)."

---

## Approach 2 — Kadane on both max and min (canonical)

**Insight.** Answer is either:
- **Non-wrapping**: standard Kadane max.
- **Wrapping**: `totalSum − minSubarraySum` (peel off the worst middle chunk).

**Edge case.** If all negative, `total − minSubSum = 0` (empty subarray) → return kadaneMax instead.

```java
int maxSubarraySumCircular(int[] nums) {
    int total = 0, curMax = 0, curMin = 0, maxS = nums[0], minS = nums[0];
    for (int x : nums) {
        total += x;
        curMax = Math.max(curMax + x, x);
        maxS = Math.max(maxS, curMax);
        curMin = Math.min(curMin + x, x);
        minS = Math.min(minS, curMin);
    }
    return maxS > 0 ? Math.max(maxS, total - minS) : maxS;
}
```

<CodeTrace
  title="Kadane on both max and min (canonical)"
  :values="['1', '-2', '3', '-2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. *Say aloud in an interview:* "same cyclic-to-linear reduction as House Robber II — two linear DPs cover both regimes."

---

## Try it yourself

<JavaRunner problem-slug="maximum-sum-circular-subarray" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Doubled Kadane | O(n²) | O(n) | TLE past n=3000 |
| **Kadane × 2 + edge** | **O(n)** | O(1) | **Canonical** |

## When to use which

- **Circular** → dual Kadane.
- **Linear** → standard Kadane.
- **"Return the subarray"** → track indices.

<AiCompanion problem-slug="maximum-sum-circular-subarray" pattern-hint="dynamic programming" />

## Related problems

- [Maximum Subarray](/problems/maximum-subarray)
- [Maximum Product Subarray](/problems/maximum-product-subarray)

<FeedbackWidget problem-slug="maximum-sum-circular-subarray" />
