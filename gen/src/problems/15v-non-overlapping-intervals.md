# Greedy — Non-overlapping Intervals

*[↗ LeetCode: Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

Min intervals to remove so the rest are non-overlapping.

**Example 1** — `intervals=[[1,2],[2,3],[3,4],[1,3]]` → `1`
**Example 2** — `intervals=[[1,2],[1,2],[1,2]]` → `2`
**Example 3** — `intervals=[[1,2],[2,3]]` → `0`

**Constraints** — `1 ≤ n ≤ 10⁵`.

---

## Approach — Sort by end + activity selection (canonical)

**Insight.** Equivalent to maximizing non-overlapping intervals; count to remove = n - maxKept. Sort by end; greedily keep intervals with start ≥ prev end.

```java
int eraseOverlapIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[1] - b[1]);
    int kept = 0, end = Integer.MIN_VALUE;
    for (int[] iv : intervals) if (iv[0] >= end) { end = iv[1]; kept++; }
    return intervals.length - kept;
}
```

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort + activity | **O(n log n)** | O(1) | canonical |

## When to use which

- **"Min remove"** → n − maxKept.
- **"Max keep"** → same skeleton, return count.
- **"Weighted intervals"** → interval scheduling DP.

## Related problems

- [Maximum Length of Pair Chain](/problems/maximum-length-of-pair-chain)
- [Minimum Arrows](/problems/minimum-number-of-arrows-to-burst-balloons)
- [Meeting Rooms](/problems/meeting-rooms)
