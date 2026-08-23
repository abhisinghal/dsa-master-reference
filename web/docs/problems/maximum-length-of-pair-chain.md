# Greedy — Maximum Length of Pair Chain

*[↗ LeetCode: Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

&lt;CompanyTags companies="Amazon, Google, Meta" /&gt;

Pair `[a,b]` chains with next `[c,d]` iff `c > b`. Return longest chain length.

**Example 1** — `pairs=[[1,2],[2,3],[3,4]]` → `2`
**Example 2** — `pairs=[[1,2],[7,8],[4,5]]` → `3`

**Constraints** — `1 ≤ n ≤ 1000`.


&lt;Hints
  hint1="Is there a local rule that provably gives global optimum? (Exchange argument.)"
  hint2="Sort by the greedy criterion (deadline / end / cost). Iterate; make the locally best choice."
  hint3="If greedy fails, DP is likely needed. But prove greedy’s correctness before writing it."
/&gt;
---

## Approach 1 — DP (LIS-style)

Sort by first; O(n²) DP.

## Approach 2 — Sort by second + greedy (canonical)

**Insight.** Activity selection: sort by second value; greedily pick every pair whose start &gt; last picked end.



```java
int findLongestChain(int[][] pairs) {
    Arrays.sort(pairs, (a, b) -> a[1] - b[1]);
    int end = Integer.MIN_VALUE, count = 0;
    for (int[] p : pairs) if (p[0] > end) { end = p[1]; count++; }
    return count;
}
```



<CodeTrace
  title="DP (LIS-style)"
  :values="['1', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="maximum-length-of-pair-chain" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DP | O(n²) | O(n) | baseline |
| Sort + greedy | **O(n log n)** | O(1) | canonical |

## When to use which

- **Chain length** → sort by end + greedy.
- **"Return the chain"** → track predecessor indices.
- **"Weighted chain"** → DP required.

&lt;AiCompanion problem-slug="maximum-length-of-pair-chain" pattern-hint="greedy" /&gt;

## Related problems

- [Non-overlapping Intervals](/problems/non-overlapping-intervals)
- [Minimum Number of Arrows](/problems/minimum-number-of-arrows-to-burst-balloons)
- [Longest Increasing Subsequence](/problems/longest-increasing-subsequence)

&lt;FeedbackWidget problem-slug="maximum-length-of-pair-chain" /&gt;
