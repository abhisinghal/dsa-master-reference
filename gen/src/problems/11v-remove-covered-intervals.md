# Merge Intervals — Remove Covered Intervals

*[↗ LeetCode: Remove Covered Intervals](https://leetcode.com/problems/remove-covered-intervals/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/merge-intervals)

Count intervals remaining after removing every interval covered by another.

**Example 1** — `intervals=[[1,4],[3,6],[2,8]]` → `2` (only [3,6] is covered by [2,8])
**Example 2** — `intervals=[[1,4],[2,3]]` → `1`

**Constraints** — `1 ≤ intervals.length ≤ 1000`.

---

## Approach 1 — All pairs

O(n²). Baseline.

## Approach 2 — Sort by start ascending, end descending; walk (canonical)

**Insight.** Sort by start asc, break ties by end **desc** (so the longest-covering interval comes first when starts tie). Walk; track `maxEnd`. An interval is covered iff its end ≤ `maxEnd`. Count uncovered.

```java
int removeCoveredIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[0] != b[0] ? a[0] - b[0] : b[1] - a[1]);
    int count = 0, maxEnd = 0;
    for (int[] iv : intervals)
        if (iv[1] > maxEnd) { count++; maxEnd = iv[1]; }
    return count;
}
```

<CodeTrace
  title="Sort — [[1,4],[3,6],[2,8]] → sorted [[1,4],[2,8],[3,6]]"
  :values="['[1,4]','[2,8]','[3,6]']"
  :windowKeys="['i']"
  :cellWidth="36"
  :steps='[
    { pointers: { i: 0 }, vars: { maxEnd: 4, count: 1 }, note: "keep" },
    { pointers: { i: 1 }, vars: { maxEnd: 8, count: 2 }, note: "8 > 4 → keep" },
    { pointers: { i: 2 }, vars: { maxEnd: 8, count: 2 }, note: "6 ≤ 8 → covered" }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Pairs | O(n²) | O(1) | baseline |
| Sort + walk | **O(n log n)** | O(1) | optimum |

## When to use which

- **Sort tie-break** matters: same-start intervals — longer must come first.
- **"Count covered instead"** → total − remaining.
- **"Which intervals covered"** → track indices before sort, mark during walk.

## Related problems

- [Merge Intervals](/problems/merge-intervals-classic)
- [Non-overlapping Intervals](/problems/non-overlapping-intervals)
- [Maximum Length of Pair Chain](/problems/maximum-length-of-pair-chain)
