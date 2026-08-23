# DP — House Robber II

*[↗ LeetCode: House Robber II](https://leetcode.com/problems/house-robber-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

&lt;CompanyTags companies="Amazon, Google, Meta" /&gt;

Houses in a **circle** — first and last adjacent. Max rob without adjacent.

**Example 1** — `nums=[2,3,2]` → `3`
**Example 2** — `nums=[1,2,3,1]` → `4`

**Constraints** — `1 ≤ n ≤ 100`.


&lt;Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/&gt;
---

&lt;MarkSolved problem-slug="house-robber-ii" /&gt;


## Approach — Two linear runs (canonical)

**Insight.** rob(first) forbids rob(last). Optimum = max of two subarrays: `[0..n-2]` and `[1..n-1]`.



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

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="house-robber-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Two linear runs | **O(n)** | O(1) | canonical |

## When to use which

- **Circular house robber** → this.
- **Linear** → [House Robber](/problems/dp-house-robber).
- **Tree** → [House Robber III](https://leetcode.com/problems/house-robber-iii/).

&lt;AiCompanion problem-slug="house-robber-ii" pattern-hint="dynamic programming" /&gt;

## Related problems

- [House Robber](/problems/dp-house-robber)
- [Delete and Earn](/problems/delete-and-earn)

&lt;FeedbackWidget problem-slug="house-robber-ii" /&gt;
