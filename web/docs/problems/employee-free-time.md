# Merge Intervals — Employee Free Time

*[↗ LeetCode: Employee Free Time](https://leetcode.com/problems/employee-free-time/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/merge-intervals)

Given schedules (each a list of disjoint intervals), return the intersection of all employees' free time.

**Example 1** — `schedule=[[[1,2],[5,6]],[[1,3]],[[4,10]]]` → `[[3,4]]`
**Example 2** — `schedule=[[[1,3],[6,7]],[[2,4]],[[2,5],[9,12]]]` → `[[5,6],[7,9]]`

**Constraints** — `1 ≤ #employees ≤ 50`; total intervals ≤ 10⁴.

---

## Approach 1 — Flatten + merge + gaps

**Intuition.** Collect all intervals; merge overlapping; consecutive gaps are common free time.



```java
List<Interval> employeeFreeTime(List<List<Interval>> schedule) {
    List<Interval> all = new ArrayList<>();
    for (List<Interval> emp : schedule) all.addAll(emp);
    all.sort((a, b) -> a.start - b.start);
    List<Interval> merged = new ArrayList<>();
    for (Interval iv : all) {
        if (merged.isEmpty() || merged.get(merged.size()-1).end < iv.start) merged.add(iv);
        else merged.get(merged.size()-1).end = Math.max(merged.get(merged.size()-1).end, iv.end);
    }
    List<Interval> free = new ArrayList<>();
    for (int i = 1; i < merged.size(); i++)
        free.add(new Interval(merged.get(i-1).end, merged.get(i).start));
    return free;
}
```



<CodeTrace
  title="Flatten + merge + gaps"
  :values="['1', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(N log N)**; Space **O(N)** where N = total intervals.

---

## Approach 2 — Min-heap sweep (canonical for k-way)

**Insight.** Use min-heap of `(interval, empIndex, listIndex)` — pop earliest start; if it starts after current-max-end, we've found a gap. Advance pointer within employee.

**Complexity** — Time **O(N log k)**; Space **O(k)**.

Better when k is much smaller than N.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Flatten + merge | O(N log N) | O(N) | baseline |
| Min-heap sweep | **O(N log k)** | **O(k)** | canonical for k-way |

## When to use which

- **Small k, many intervals per employee** → heap sweep.
- **Balanced input** → flatten + merge is simpler.
- **"Find first common free slot ≥ duration D"** → augment sweep with duration check.

## Related problems

- [Merge Intervals](/problems/merge-intervals-classic)
- [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii)
- [Interval List Intersections](/problems/interval-list-intersections)
- [Smallest Range Covering k Lists](/problems/smallest-range-covering-elements-from-k-lists)
