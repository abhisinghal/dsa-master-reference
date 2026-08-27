# DP — Min Cost Climbing Stairs

*[↗ LeetCode: Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Meta, Google" />

Each step has cost. Start at 0 or 1; step 1 or 2. Min cost to reach past-the-end.

**Example 1** — `cost=[10,15,20]` → `15` (start at 1, one step past → cost 15)
**Example 2** — `cost=[1,100,1,1,1,100,1,1,100,1]` → `6` (skip the 100s)
**Example 3** — `cost=[0,0,0,0]` → `0` (all free)

**Constraints** — `2 ≤ n ≤ 1000`. Brute recursion tries +1 or +2 at each step — O(2ⁿ) ≈ 10³⁰¹ ops at n=1000 (10¹ magnitude → dead universes over). Rolling DP is O(n) = 10⁶ pointer ops at hot-path scale = &lt;1 ms.
<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="min-cost-climbing-stairs" /> <Bookmark problem-slug="min-cost-climbing-stairs" />

<InterviewTimer problem-slug="min-cost-climbing-stairs" />



## Approach 1 — Brute recursion (no memo)

**Intuition.** Recurse from each starting step; at each step, try +1 or +2. Return min.

**Complexity** — Time **O(2ⁿ)**; Space **O(n)** stack. TLE past n=30. *In an interview* say "same subproblems retread — memoize on step index → O(n)."

---

## Approach 2 — DP O(1) space (canonical)

**Insight.** `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`. Only need last two → constant space.



```java
int minCostClimbingStairs(int[] cost) {
    int a = 0, b = 0;
    for (int i = 2; i <= cost.length; i++) {
        int c = Math.min(b + cost[i-1], a + cost[i-2]);
        a = b; b = c;
    }
    return b;
}
```



<CodeTrace
  title="DP O(1) space (canonical)"
  :values="['10', '15', '20']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. *Say aloud in an interview:* "same rolling-DP as Climbing Stairs and Fibonacci — 2-element rolling window."

---

## Try it yourself

<JavaRunner problem-slug="min-cost-climbing-stairs" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute recursion | O(2ⁿ) | O(n) | TLE past n=30 |
| **Rolling DP** | **O(n)** | O(1) | **Canonical** |

## When to use which

- **Standard** → rolling DP.
- **Return steps taken** → track predecessors.
- **k-step variants** → same skeleton with min over last k.

<AiCompanion problem-slug="min-cost-climbing-stairs" pattern-hint="dynamic programming" />

## Related problems

- [Climbing Stairs](/problems/climbing-stairs)
- [House Robber](/problems/dp-house-robber)

<FeedbackWidget problem-slug="min-cost-climbing-stairs" />

<RelatedProblems problems="longest-palindromic-subsequence::Longest Palindromic Subsequence|longest-common-subsequence::Longest Common Subsequence|climbing-stairs::Climbing Stairs" />
