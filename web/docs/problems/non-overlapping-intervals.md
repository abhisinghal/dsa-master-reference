# Greedy — Non-overlapping Intervals

*[↗ LeetCode: Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

Minimum intervals to remove so the rest are non-overlapping.

---

## Approach 1 — Sort by end + activity selection
**Insight.** Equivalent to maximizing non-overlapping intervals; the count to remove is `n - maxKept`. Sort by end, greedily keep intervals whose start ≥ previous end.

**Why sort by end.** Choosing the earliest ending interval leaves maximal room for the rest — classic exchange argument.



```java
int eraseOverlapIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[1] - b[1]);
    int kept = 0, end = Integer.MIN_VALUE;
    for (int[] it : intervals)
        if (it[0] >= end) { end = it[1]; kept++; }
    return intervals.length - kept;
}
```



**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort by end + activity selection | O(n log n) | O(1) | primary |

## When to use which

- **Ship this** → Sort by end + activity selection (O(n log n), O(1)). The pattern's standard solution.

## Related problems

- [Minimum Arrows](/problems/minimum-number-of-arrows-to-burst-balloons) — sibling with weak inequality
- [Maximum Length of Pair Chain](/problems/maximum-length-of-pair-chain)
- [Meeting Rooms](/problems/meeting-rooms)
