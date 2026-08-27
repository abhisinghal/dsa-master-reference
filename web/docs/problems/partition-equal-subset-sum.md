# DP — Partition Equal Subset Sum

*[↗ LeetCode: Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Meta, Amazon, Google, Uber" />

Can `nums` split into two subsets with equal sum?

**Example 1** — `nums=[1,5,11,5]` → `true` (`[1,5,5]` vs `[11]`, sum=11 each)
**Example 2** — `nums=[1,2,3,5]` → `false` (sum=11, odd → impossible)
**Example 3** — `nums=[2,2]` → `true`

**Constraints** — `1 ≤ n ≤ 200`; `1 ≤ nums[i] ≤ 100`. Brute is 2ⁿ subsets — 2²⁰⁰ ops = universe-age. Knapsack DP is O(n·sum) ≤ 200·10⁴ = 2·10⁶ ops = 50ms.


<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="partition-equal-subset-sum" /> <Bookmark problem-slug="partition-equal-subset-sum" />

<InterviewTimer problem-slug="partition-equal-subset-sum" />



## Approach 1 — Brute subset enumeration

**Intuition.** Try every subset; if its sum is `total/2`, return true. 2ⁿ combinations.

**Complexity** — Time **O(2ⁿ)**; Space **O(n)** stack. TLE past n=25. *In an interview* say "reduce to subset-sum feasibility — knapsack DP → O(n·sum)."

---

## Approach 2 — Subset-sum DP (0/1 knapsack, canonical)

**Insight.** Possible iff sum even AND a subset sums to `sum/2`. Boolean DP `dp[j]` = "can we hit sum j?".

**Trap** — iterate `j` **descending** for 0/1 knapsack (else you'd count each item multiple times).



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



<CodeTrace
  title="Subset-sum DP (0/1 knapsack, canonical)"
  :values="['1', '5', '11', '5']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n · sum)**; Space **O(sum)**. *Say aloud in an interview:* "canonical 0/1 knapsack — same skeleton as Target Sum, Last Stone Weight II."

## BitSet speedup
`dp |= dp << x` on `BitSet` — word-parallel.

---

## Try it yourself

<JavaRunner problem-slug="partition-equal-subset-sum" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute subsets | O(2ⁿ) | O(n) | TLE past n=25 |
| **0/1 knapsack DP** | **O(n · sum)** | O(sum) | **Canonical** |
| BitSet | O(n · sum / 64) | O(sum) | Polish |

## When to use which

- **Two equal subsets** → this.
- **k subsets** → [Partition to K Equal Sum Subsets](/problems/partition-to-k-equal-sum-subsets).
- **Return the partition** → track parent choices.

<AiCompanion problem-slug="partition-equal-subset-sum" pattern-hint="dynamic programming" />

## Related problems

- [Target Sum](/problems/target-sum)
- [Last Stone Weight II](/problems/last-stone-weight-ii)
- [Partition to K Equal Sum Subsets](/problems/partition-to-k-equal-sum-subsets)

<FeedbackWidget problem-slug="partition-equal-subset-sum" />

<RelatedProblems problems="delete-and-earn::Delete And Earn|climbing-stairs::Climbing Stairs|house-robber-ii::House Robber II" />
