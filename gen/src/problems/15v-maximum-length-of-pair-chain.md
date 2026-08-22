# Greedy — Maximum Length of Pair Chain

*[↗ LeetCode: Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

Pairs `[a, b]` chain if next pair `[c, d]` has `c > b`. Max chain length.

---

## Approach 1 — DP (LIS style)
Sort by first; `dp[i] = 1 + max(dp[j])` over `j` with `pair[j].b < pair[i].a`. O(n²).

---

## Approach 2 — Greedy (activity selection)
**Insight.** Sort by **second** value. Greedily pick every pair whose start > last picked end. Same as interval scheduling.

```java
int findLongestChain(int[][] pairs) {
    Arrays.sort(pairs, (a, b) -> a[1] - b[1]);
    int end = Integer.MIN_VALUE, count = 0;
    for (int[] p : pairs)
        if (p[0] > end) { end = p[1]; count++; }
    return count;
}
```

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| DP (LIS style) | O(n²) | — | baseline |
| Greedy (activity selection) | O(n log n) | O(1) | optimum |

## When to use which

- **State it for signal** → DP (LIS style) (O(n²)). Correct baseline; call it out then move on.
- **Ship this** → Greedy (activity selection) (O(n log n), O(1)). Expected optimum in interview.

## Related problems

- [Non-overlapping Intervals](/problems/non-overlapping-intervals) — identical algorithm
- [Minimum Number of Arrows](/problems/minimum-number-of-arrows-to-burst-balloons)
