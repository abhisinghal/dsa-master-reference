# DP — Paint House II

*[↗ LeetCode: Paint House II](https://leetcode.com/problems/paint-house-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

&lt;CompanyTags companies="LinkedIn, Facebook, Meta, Google" /&gt;

`n` houses, `k` colors. cost to paint. No two adjacent same color. Min total.

**Constraints** — `1 ≤ n·k ≤ 5000`.

**Example 1** — `costs=[[1,5,3],[2,9,4]]` → `5`
**Example 2** — `costs=[[1,3],[2,4]]` → `5`


&lt;Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/&gt;
---

&lt;MarkSolved problem-slug="paint-house-ii" /&gt;


## Approach 1 — O(n · k²) DP
`dp[i][j] = cost[i][j] + min(dp[i-1][j'])` over `j' ≠ j`.

## Approach 2 — Track min & second-min per row → O(n · k) (canonical)

**Insight.** Only need two smallest values from previous row + which index was min.



```java
int minCostII(int[][] costs) {
    int n = costs.length, k = costs[0].length;
    int min1 = 0, min2 = 0, idx1 = -1;
    for (int i = 0; i < n; i++) {
        int nMin1 = Integer.MAX_VALUE, nMin2 = Integer.MAX_VALUE, nIdx1 = -1;
        for (int j = 0; j < k; j++) {
            int c = costs[i][j] + (j == idx1 ? min2 : min1);
            if (c < nMin1) { nMin2 = nMin1; nMin1 = c; nIdx1 = j; }
            else if (c < nMin2) nMin2 = c;
        }
        min1 = nMin1; min2 = nMin2; idx1 = nIdx1;
    }
    return min1;
}
```



<CodeTrace
  title="O(n · k²) DP"
  :values="['1', '5', '3']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n · k)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="paint-house-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| O(n·k²) DP | O(n·k²) | O(k) | baseline |
| Min+second min | **O(n·k)** | O(1) | canonical |

## When to use which

- **Standard** → min + second-min trick.
- **Only 3 colors** → O(n) with 3-way check.
- **Return coloring** → track color chosen.

&lt;AiCompanion problem-slug="paint-house-ii" pattern-hint="dynamic programming" /&gt;

## Related problems

- [Paint House](https://leetcode.com/problems/paint-house/)
- [Paint Fence](https://leetcode.com/problems/paint-fence/)

&lt;FeedbackWidget problem-slug="paint-house-ii" /&gt;
