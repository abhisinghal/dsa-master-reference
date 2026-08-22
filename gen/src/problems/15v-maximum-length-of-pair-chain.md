# Greedy — Maximum Length of Pair Chain

*[↗ LeetCode: Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

Pair `[a,b]` chains with next `[c,d]` iff `c > b`. Return longest chain length.

**Example 1** — `pairs=[[1,2],[2,3],[3,4]]` → `2`
**Example 2** — `pairs=[[1,2],[7,8],[4,5]]` → `3`

**Constraints** — `1 ≤ n ≤ 1000`.

---

## Approach 1 — DP (LIS-style)

Sort by first; O(n²) DP.

## Approach 2 — Sort by second + greedy (canonical)

**Insight.** Activity selection: sort by second value; greedily pick every pair whose start > last picked end.

```java
int findLongestChain(int[][] pairs) {
    Arrays.sort(pairs, (a, b) -> a[1] - b[1]);
    int end = Integer.MIN_VALUE, count = 0;
    for (int[] p : pairs) if (p[0] > end) { end = p[1]; count++; }
    return count;
}
```

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DP | O(n²) | O(n) | baseline |
| Sort + greedy | **O(n log n)** | O(1) | canonical |

## When to use which

- **Chain length** → sort by end + greedy.
- **"Return the chain"** → track predecessor indices.
- **"Weighted chain"** → DP required.

## Related problems

- [Non-overlapping Intervals](/problems/non-overlapping-intervals)
- [Minimum Number of Arrows](/problems/minimum-number-of-arrows-to-burst-balloons)
- [Longest Increasing Subsequence](/problems/longest-increasing-subsequence)
