# Greedy — Maximum Subarray (Kadane)

*[↗ LeetCode: Maximum Subarray](https://leetcode.com/problems/maximum-subarray/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, LinkedIn, Bloomberg, Apple" />

Max sum of a contiguous non-empty subarray.

**Example 1** — `nums=[-2,1,-3,4,-1,2,1,-5,4]` → `6` (`[4,-1,2,1]`)
**Example 2** — `nums=[1]` → `1`
**Example 3** — `nums=[5,4,-1,7,8]` → `23`

**Constraints** — `1 ≤ n ≤ 10⁵`; `-10⁴ ≤ nums[i] ≤ 10⁴`.


<Hints
  hint1="Is there a local rule that provably gives global optimum? (Exchange argument.)"
  hint2="Sort by the greedy criterion (deadline / end / cost). Iterate; make the locally best choice."
  hint3="If greedy fails, DP is likely needed. But prove greedy’s correctness before writing it."
/>
---

<MarkSolved problem-slug="maximum-subarray" />

<InterviewTimer problem-slug="maximum-subarray" />



## Approach 1 — All subarrays

O(n²). Baseline.

## Approach 2 — Kadane (canonical)

**Insight.** `curr = max(x, curr + x)` — either extend or restart. Global answer = max over all i.

```java
int maxSubArray(int[] nums) {
    int cur = nums[0], best = nums[0];
    for (int i = 1; i < nums.length; i++) {
        cur = Math.max(nums[i], cur + nums[i]);
        best = Math.max(best, cur);
    }
    return best;
}
```

<CodeTrace
  title="Kadane — nums=[-2,1,-3,4,-1,2,1,-5,4]"
  :values="['-2','1','-3','4','-1','2','1','-5','4']"
  :windowKeys="['i']"
  :cellWidth="30"
  :steps='[
    { pointers: { i: 3 }, vars: { cur: 4, best: 4 }, note: "restart" },
    { pointers: { i: 6 }, vars: { cur: 6, best: 6 }, note: "extend" },
    { pointers: { i: 8 }, vars: { cur: 4, best: 6 }, note: "final" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

## Approach 3 — Divide & Conquer

`max(left, right, crossing)`. **O(n log n)**. Interview curiosity.

---

## Try it yourself

<JavaRunner problem-slug="maximum-subarray" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| All subarrays | O(n²) | O(1) | baseline |
| Kadane | **O(n)** | O(1) | canonical |
| D&C | O(n log n) | O(log n) | trivia |

## When to use which

- **Standard** → Kadane.
- **"Return the subarray"** → track `(bestStart, bestEnd)` alongside sums.
- **Circular array** → [Maximum Sum Circular Subarray](/problems/maximum-sum-circular-subarray) — Kadane + reverse.

<AiCompanion problem-slug="maximum-subarray" pattern-hint="greedy" />

## Related problems

- [Maximum Product Subarray](/problems/maximum-product-subarray) — min/max dual tracking
- [Maximum Sum Circular Subarray](/problems/maximum-sum-circular-subarray)
- [Best Time to Buy and Sell Stock](/problems/best-time-to-buy-and-sell-stock)

<FeedbackWidget problem-slug="maximum-subarray" />

<RelatedProblems problems="jump-game-ii::Jump Game II|jump-game::Jump Game|non-overlapping-intervals::Non Overlapping Intervals" />
