# DP — Burst Balloons

*[↗ LeetCode: Burst Balloons](https://leetcode.com/problems/burst-balloons/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Google, Amazon, Meta" />

Burst balloons; when bursting `i`, gain `nums[l] * nums[i] * nums[r]` where l, r are alive neighbors. Max coins.

**Example 1** — `nums=[3,1,5,8]` → `167`

**Constraints** — `1 ≤ n ≤ 300`.


<Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="burst-balloons" />


## Approach — Interval DP with "last to burst" trick (canonical)

**Insight.** "First to burst" model fails — neighbors change unpredictably. Instead consider `i` as the **last** to burst in range `(l, r)`: its neighbors at that moment are fixed at `nums[l]` and `nums[r]`. Subproblems `(l, i)` and `(i, r)` are independent.

**Padding.** Prepend and append `1` so base neighbors are always defined.

```java
int maxCoins(int[] nums) {
    int n = nums.length;
    int[] a = new int[n + 2];
    a[0] = a[n + 1] = 1;
    for (int i = 0; i < n; i++) a[i + 1] = nums[i];
    int[][] dp = new int[n + 2][n + 2];
    for (int len = 2; len <= n + 1; len++)
        for (int l = 0; l + len <= n + 1; l++) {
            int r = l + len;
            for (int k = l + 1; k < r; k++)
                dp[l][r] = Math.max(dp[l][r], dp[l][k] + dp[k][r] + a[l] * a[k] * a[r]);
        }
    return dp[0][n + 1];
}
```

<CodeTrace
  title="Interval DP with  last to burst  trick (canonical)"
  :values="['3', '1', '5', '8']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n³)**; Space **O(n²)**.

---

## Try it yourself

<JavaRunner problem-slug="burst-balloons" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Interval DP | **O(n³)** | O(n²) | canonical |

## When to use which

- **"Optimize over splits with fixed boundary contribution"** → interval DP.
- **"Reverse (last first) trick"** → also works in Matrix Chain, Merge Stones.

<AiCompanion problem-slug="burst-balloons" pattern-hint="dynamic programming" />

## Related problems

- [Minimum Cost to Merge Stones](/problems/minimum-cost-to-merge-stones)
- [Palindrome Partitioning II](/problems/palindrome-partitioning-ii)

<FeedbackWidget problem-slug="burst-balloons" />

<RelatedProblems problems="palindrome-partitioning-ii::Palindrome Partitioning II|delete-and-earn::Delete And Earn|unique-paths-ii::Unique Paths II" />
