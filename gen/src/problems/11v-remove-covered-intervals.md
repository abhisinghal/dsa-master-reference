# Merge Intervals — Remove Covered Intervals

*[↗ LeetCode: Remove Covered Intervals](https://leetcode.com/problems/remove-covered-intervals/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/merge-intervals)

Given intervals, return how many remain after removing intervals fully covered by another.

**Example** — `[[1,4],[3,6],[2,8]]` → `2` ([1,4] covered by [2,8]? no. But [3,6] covered by [2,8]. Answer 2.)

---

## Approach 1 — Brute nested pair

O(n²). Check each interval against every other.

## Approach 2 — Sort by start asc, end desc; count non-covered

**Insight.** Sort by start; break ties by end desc. Walk with `maxEnd` seen so far. Each interval whose end > `maxEnd` is uncovered → count and update `maxEnd`. Others are covered.

```java
int removeCoveredIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[0] != b[0] ? a[0] - b[0] : b[1] - a[1]);
    int count = 0, end = 0;
    for (int[] i : intervals) if (i[1] > end) { count++; end = i[1]; }
    return count;
}
```

<CodeTrace
  title="Sort + running-end — [[1,4],[3,6],[2,8]]"
  :values="['[1,4]','[2,8]','[3,6]']"
  :windowKeys="['i']"
  :cellWidth="60"
  :steps='[
    { pointers: { i: 0 }, vars: { end: 4, count: 1 }, note: "[1,4]. end=4", added: [0] },
    { pointers: { i: 1 }, vars: { end: 8, count: 2 }, note: "[2,8]. 8 gt 4 → count", added: [1] },
    { pointers: { i: 2 }, vars: { end: 8, count: 2 }, note: "[3,6]. 6 not gt 8 → covered, skip" }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(1)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute nested | O(n²) | O(1) |
| Sort + scan | **O(n log n)** | **O(1)** |

## Related problems

- [Merge Intervals](/problems/merge-intervals-classic)
- [Non-overlapping Intervals](/problems/non-overlapping-intervals)
