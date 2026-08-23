# Merge Intervals — Insert Interval

*[↗ LeetCode: Insert Interval](https://leetcode.com/problems/insert-interval/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/merge-intervals)

&lt;CompanyTags companies="Meta, Amazon, Google, LinkedIn" /&gt;

Given sorted, non-overlapping `intervals` and a `newInterval`, insert it and merge if needed.

**Example 1** — `intervals=[[1,3],[6,9]], newInterval=[2,5]` → `[[1,5],[6,9]]`
**Example 2** — `intervals=[[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval=[4,8]` → `[[1,2],[3,10],[12,16]]`
**Example 3** — `intervals=[], newInterval=[5,7]` → `[[5,7]]`

**Constraints** — `0 ≤ intervals.length ≤ 10⁴`.


&lt;Hints
  hint1="Sort by start (or end, depending on the question)."
  hint2="Walk once; each interval either extends the current chunk (overlap) or starts a new one."
  hint3="For ’insert’ or ’intersect’, use the same sweep with a merge/intersection rule at overlaps."
/&gt;
---

&lt;MarkSolved problem-slug="insert-interval" /&gt; &lt;Bookmark problem-slug="insert-interval" /&gt;

&lt;InterviewTimer problem-slug="insert-interval" /&gt;



## Approach 1 — Append + full merge

Insert then run [Merge Intervals](/problems/merge-intervals-classic) O(n log n).

## Approach 2 — Single-pass three-phase (canonical)

**Insight.** Since intervals are pre-sorted, walk once:
1. Copy intervals ending before `newInterval` starts.
2. Merge all intervals overlapping `newInterval`.
3. Copy intervals starting after `newInterval` ends.



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
  title="3-phase — intervals=[[1,2],[3,5],[6,7],[8,10],[12,16]], new=[4,8]"
  :values="['[1,2]','[3,5]','[6,7]','[8,10]','[12,16]']"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "copy" }, note: "[1,2] ends before 4" },
    { pointers: { i: 1 }, vars: { phase: "merge", new: "[3,8]" }, note: "[3,5] overlaps → extend" },
    { pointers: { i: 3 }, vars: { phase: "merge", new: "[3,10]" }, note: "[6,7],[8,10] overlap" },
    { pointers: { i: 4 }, vars: { phase: "tail" }, note: "[12,16] after end → copy" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="insert-interval" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Append + merge | O(n log n) | O(n) | baseline |
| Three-phase single pass | **O(n)** | O(n) | canonical |

## When to use which

- **Streaming inserts into sorted list** → repeated three-phase.
- **Batch merges** → sort once, then O(n) merge.
- **Return "would this overlap?" boolean** → binary-search for first `end ≥ new.start`.

&lt;AiCompanion problem-slug="insert-interval" pattern-hint="merge intervals" /&gt;

## Related problems

- [Merge Intervals](/problems/merge-intervals-classic)
- [Interval List Intersections](/problems/interval-list-intersections)
- [Remove Covered Intervals](/problems/remove-covered-intervals)

&lt;FeedbackWidget problem-slug="insert-interval" /&gt;

&lt;RelatedProblems problems="remove-covered-intervals::Remove Covered Intervals|my-calendar-ii::My Calendar II|meeting-rooms-ii::Meeting Rooms II" /&gt;
