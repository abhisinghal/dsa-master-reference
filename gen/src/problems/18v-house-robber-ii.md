# DP — House Robber II

*[↗ LeetCode: House Robber II](https://leetcode.com/problems/house-robber-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google, Meta" />

Houses in a **circle** — first and last adjacent. Max rob without adjacent.

**Example 1** — `nums=[2,3,2]` → `3` (rob only house 1: `3`; can't rob 0 and 2 together — adjacent in circle)
**Example 2** — `nums=[1,2,3,1]` → `4` (rob houses 0 and 2: `1+3=4`)
**Example 3** — `nums=[1]` → `1`

**Constraints** — `1 ≤ n ≤ 100`. Brute 2ⁿ subset enumeration is 2¹⁰⁰ = universe-age. Two linear-DP runs is O(n) = 100 ops.


<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="house-robber-ii" /> <Bookmark problem-slug="house-robber-ii" />

<InterviewTimer problem-slug="house-robber-ii" />



## Approach 1 — Brute enumeration

**Intuition.** For each subset, check if it's a valid pick (no adjacent in circle) and track max sum. `2ⁿ` states.

**Complexity** — Time **O(2ⁿ · n)**; Space **O(n)**. Dies past n=25. *In an interview* say "linear DP twice: once excluding last house, once excluding first → O(n)."

---

## Approach 2 — Two linear runs (canonical)

**Insight.** rob(first) forbids rob(last). So the optimum = max of two independent subproblems on subarrays: `[0..n-2]` (skip last) and `[1..n-1]` (skip first). Each is standard linear House Robber.

```java
int rob(int[] nums) {
    int n = nums.length;
    if (n == 1) return nums[0];
    return Math.max(linear(nums, 0, n - 2), linear(nums, 1, n - 1));
}
int linear(int[] nums, int lo, int hi) {
    int prev = 0, curr = 0;
    for (int i = lo; i <= hi; i++) {
        int t = Math.max(curr, prev + nums[i]);
        prev = curr; curr = t;
    }
    return curr;
}
```

<CodeTrace
  title="Two linear runs (canonical)"
  :values="['2', '3', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. *Say aloud in an interview:* "reduce a cyclic problem to two acyclic subproblems — same technique in Circular Array Loop, Rotate Array."

---

## Try it yourself

<JavaRunner problem-slug="house-robber-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute subsets | O(2ⁿ · n) | O(n) | TLE past n=25 |
| **Two linear runs** | **O(n)** | O(1) | **Canonical** |

## When to use which

- **Circular house robber** → this.
- **Linear** → [House Robber](/problems/dp-house-robber).
- **Tree** → [House Robber III](https://leetcode.com/problems/house-robber-iii/).

<AiCompanion problem-slug="house-robber-ii" pattern-hint="dynamic programming" />

## Related problems

- [House Robber](/problems/dp-house-robber)
- [Delete and Earn](/problems/delete-and-earn)

<FeedbackWidget problem-slug="house-robber-ii" />

<RelatedProblems problems="min-cost-climbing-stairs::Min Cost Climbing Stairs|delete-and-earn::Delete And Earn|maximal-square::Maximal Square" />
