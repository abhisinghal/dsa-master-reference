# Merge Intervals — Meeting Rooms

*[↗ LeetCode: Meeting Rooms](https://leetcode.com/problems/meeting-rooms/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/merge-intervals)

&lt;CompanyTags companies="Meta, Amazon, Google, Bloomberg" /&gt;

Given meeting time intervals, return `true` iff a person can attend all.

**Example 1** — `intervals=[[0,30],[5,10],[15,20]]` → `false`
**Example 2** — `intervals=[[7,10],[2,4]]` → `true`
**Example 3** — `intervals=[]` → `true`

**Constraints** — `0 ≤ intervals.length ≤ 10⁴`.


&lt;Hints
  hint1="Sort by start (or end, depending on the question)."
  hint2="Walk once; each interval either extends the current chunk (overlap) or starts a new one."
  hint3="For ’insert’ or ’intersect’, use the same sweep with a merge/intersection rule at overlaps."
/&gt;
---

&lt;MarkSolved problem-slug="meeting-rooms" /&gt;


## Approach 1 — Every pair

O(n²). Baseline.

## Approach 2 — Sort by start; adjacent overlap check

**Insight.** After sorting by start, only adjacent intervals can conflict. Walk once.



```java
boolean canAttendMeetings(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
    for (int i = 1; i < intervals.length; i++)
        if (intervals[i][0] < intervals[i-1][1]) return false;
    return true;
}
```



<CodeTrace
  title="Sort + adjacent — [[0,30],[5,10],[15,20]]"
  :values="['[0,30]','[5,10]','[15,20]']"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 1 }, vars: { prevEnd: 30, currStart: 5 }, note: "5 < 30 → overlap → false" }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="meeting-rooms" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Every pair | O(n²) | O(1) | baseline |
| Sort + walk | **O(n log n)** | O(1) | optimum |

## When to use which

- **Boolean feasibility** → sort + walk.
- **Count rooms needed** → [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii) — heap or sweep line.
- **Return conflict pairs** → keep sorted; walk once collecting pairs.

&lt;AiCompanion problem-slug="meeting-rooms" pattern-hint="merge intervals" /&gt;

## Related problems

- [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii)
- [Merge Intervals](/problems/merge-intervals-classic)
- [Non-overlapping Intervals](/problems/non-overlapping-intervals)

&lt;FeedbackWidget problem-slug="meeting-rooms" /&gt;
