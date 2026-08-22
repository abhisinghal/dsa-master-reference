# Greedy — Minimum Number of Arrows to Burst Balloons

*[↗ LeetCode: Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

Each balloon spans `[x_start, x_end]`. A vertical arrow at `x` bursts every balloon whose span contains `x`. Minimum arrows.

---

## Approach 1 — Sort by end + shoot at end of first alive
**Insight.** Sort by `x_end`. Shoot the first balloon at its end. That arrow bursts every balloon starting ≤ end. Move to first balloon starting &gt; end, repeat.



```java
int findMinArrowShots(int[][] points) {
    Arrays.sort(points, (a, b) -> Integer.compare(a[1], b[1])); // avoid int overflow
    int arrows = 1, end = points[0][1];
    for (int i = 1; i < points.length; i++)
        if (points[i][0] > end) { arrows++; end = points[i][1]; }
    return arrows;
}
```



**Trap.** Use `Integer.compare` — subtraction can overflow when spans include `INT_MAX/INT_MIN`.

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort by end + shoot at end of first alive | O(n log n) | O(1) | primary |

## When to use which

- **Ship this** → Sort by end + shoot at end of first alive (O(n log n), O(1)). The pattern's standard solution.

## Related problems

- [Non-overlapping Intervals](/problems/non-overlapping-intervals) — strict inequality variant
- [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii)
