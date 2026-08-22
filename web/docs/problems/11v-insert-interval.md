# Merge Intervals — Insert Interval

*[↗ LeetCode: Insert Interval](https://leetcode.com/problems/insert-interval/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/merge-intervals)

Given a sorted list of non-overlapping intervals and a new interval, insert and merge.

**Example** — `intervals=[[1,3],[6,9]], newInterval=[2,5]` → `[[1,5],[6,9]]`

---

## Approach 1 — Insert + full merge

Add the new interval; sort; run Merge Intervals. O(n log n).

## Approach 2 — One-pass three-phase

**Insight.** Because input is sorted, walk once:
1. **Before overlap.** Add intervals that end before newInterval.start.
2. **Overlap.** Expand newInterval to swallow all intervals whose start ≤ newInterval.end.
3. **After.** Add remaining intervals as-is.



```java
int[][] insert(int[][] intervals, int[] newInterval) {
    List<int[]> out = new ArrayList<>();
    int i = 0, n = intervals.length;
    while (i < n && intervals[i][1] < newInterval[0]) out.add(intervals[i++]);
    while (i < n && intervals[i][0] <= newInterval[1]) {
        newInterval[0] = Math.min(newInterval[0], intervals[i][0]);
        newInterval[1] = Math.max(newInterval[1], intervals[i][1]);
        i++;
    }
    out.add(newInterval);
    while (i < n) out.add(intervals[i++]);
    return out.toArray(new int[0][]);
}
```



<CodeTrace
  title="Three-phase — intervals=[[1,3],[6,9]], newInterval=[2,5]"
  :values="['[1,3]','[6,9]']"
  :windowKeys="['i']"
  :cellWidth="60"
  :steps='[
    { pointers: { i: 0 }, vars: { newInterval: "[2,5]", phase: "overlap" }, note: "[1,3] overlaps → merge → [1,5]", added: [0] },
    { pointers: { i: 1 }, vars: { newInterval: "[1,5]", phase: "after" }, note: "[6,9] after → append. done", added: [1] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)** output.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Insert + full merge | O(n log n) | O(n) |
| One-pass three-phase | **O(n)** | O(n) |

## Related problems

- [Merge Intervals](/problems/merge-intervals-classic) — full merge, sorted-by-start
- [Interval List Intersections](/problems/interval-list-intersections) — two sorted interval lists
- [Non-overlapping Intervals](/problems/non-overlapping-intervals) — remove min count
