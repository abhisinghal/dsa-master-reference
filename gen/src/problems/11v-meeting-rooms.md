# Merge Intervals — Meeting Rooms

*[↗ LeetCode: Meeting Rooms](https://leetcode.com/problems/meeting-rooms/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/merge-intervals)

Given meetings `[start, end]`, return `true` if a single person can attend all (no overlaps).

**Example** — `[[0,30],[5,10],[15,20]]` → `false`

---

## Approach 1 — Brute nested pair

O(n²). Baseline.

## Approach 2 — Sort by start, check adjacent

**Insight.** After sorting by start, an overlap only exists if any adjacent pair has `next.start < prev.end`.

```java
boolean canAttendMeetings(int[][] meetings) {
    Arrays.sort(meetings, (a, b) -> a[0] - b[0]);
    for (int i = 1; i < meetings.length; i++)
        if (meetings[i][0] < meetings[i - 1][1]) return false;
    return true;
}
```

<CodeTrace
  title="Sort + adjacent check — [[0,30],[5,10],[15,20]]"
  :values="['[0,30]','[5,10]','[15,20]']"
  :windowKeys="['i']"
  :cellWidth="60"
  :steps='[
    { pointers: { i: 1 }, vars: { prev_end: 30, cur_start: 5 }, note: "5 lt 30 → overlap → return false", removed: [1] }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(1)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute nested | O(n²) | O(1) |
| Sort + scan | **O(n log n)** | **O(1)** |

## Related problems

- [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii) — return the room count
- [Non-overlapping Intervals](/problems/non-overlapping-intervals) — remove min count
