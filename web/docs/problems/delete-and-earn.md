# DP — Delete and Earn

*[↗ LeetCode: Delete and Earn](https://leetcode.com/problems/delete-and-earn/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google, Meta" />

Delete `x` to earn `x` points; also removes all `x-1` and `x+1`. Max points.

**Example 1** — `nums=[3,4,2]` → `6`
**Example 2** — `nums=[2,2,3,3,3,4]` → `9`
**Example 3** — `nums=[1,1,1,2,4,5,5,5,6]` → `18`

**Constraints** — `1 ≤ n ≤ 2·10⁴`; `1 ≤ nums[i] ≤ 10⁴`. Brute subset enumeration is 2ⁿ — impossible past n=25. Reduction to House Robber gives O(n + max) ≈ 4·10⁴. Brute enumerates 2ⁿ subsets — at n=2·10⁴ = 10⁶⁰⁰⁰ (dead). Reduce to house-robber on bucketed sums → DP O(n + max) = 2·10⁴ + 10⁴ = 3·10⁴ ops = &lt;2 ms.
<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="delete-and-earn" /> <Bookmark problem-slug="delete-and-earn" />

<InterviewTimer problem-slug="delete-and-earn" />



## Approach 1 — Brute subset enumeration

**Intuition.** For each subset of values in nums, check if any two are adjacent (differ by 1). If not, sum the values. Track max.

**Complexity** — Time **O(2ⁿ · n)**; Space **O(n)**. TLE past n=20. *In an interview* say "the 'adjacent-value taboo' has the same structure as House Robber → O(n + max)."

---

## Approach 2 — Reduce to House Robber (canonical)

**Insight.** Bucket totals: `points[v] = v · count(v)`. Picking bucket `v` forbids `v±1` — exactly **House Robber** on the `points[]` array indexed by value.



```java
int deleteAndEarn(int[] nums) {
    int max = 0;
    for (int x : nums) max = Math.max(max, x);
    int[] points = new int[max + 1];
    for (int x : nums) points[x] += x;
    int prev = 0, curr = 0;
    for (int v = 0; v <= max; v++) {
        int t = Math.max(curr, prev + points[v]);
        prev = curr; curr = t;
    }
    return curr;
}
```



<CodeTrace
  title="Reduce to House Robber (canonical)"
  :values="['3', '4', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n + max)**; Space **O(max)**. *Say aloud in an interview:* "spot the reduction — every 'pick or skip with adjacency taboo' is House Robber wearing a different hat."

---

## Try it yourself

<JavaRunner problem-slug="delete-and-earn" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute subsets | O(2ⁿ · n) | O(n) | Reference; TLE past n=20 |
| **Reduce to House Robber** | **O(n + max)** | O(max) | **Canonical** |

## When to use which

- **"Adjacent-value taboo"** → reduce to House Robber.
- **Sparse values** → skip zeros; use TreeMap.

<AiCompanion problem-slug="delete-and-earn" pattern-hint="dynamic programming" />

## Related problems

- [House Robber](/problems/dp-house-robber)
- [House Robber II](/problems/house-robber-ii)

<FeedbackWidget problem-slug="delete-and-earn" />

<RelatedProblems problems="coin-change-ii::Coin Change II|min-cost-climbing-stairs::Min Cost Climbing Stairs|unique-paths-ii::Unique Paths II" />
