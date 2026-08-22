# Merge Intervals — Employee Free Time

*[↗ LeetCode: Employee Free Time](https://leetcode.com/problems/employee-free-time/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/merge-intervals)

Given `k` employees' sorted schedule intervals, return the intervals where **all** are simultaneously free.

**Example** — `[[[1,2],[5,6]],[[1,3]],[[4,10]]]` → `[[3,4]]`

---

## Approach 1 — Flatten + sort + merge, then gaps

Merge every employee's intervals into one flat sorted list; then the gaps between merged intervals are free times.

**Complexity** — Time **O(N log N)**; Space **O(N)** where N = total intervals.

## Approach 2 — Min-heap k-way merge

**Insight.** Same as merging k sorted lists (each employee's schedule). Track the running max end; when a new interval's start &gt; running max, that gap is a free time.



```java
List<int[]> employeeFreeTime(List<List<int[]>> schedule) {
    PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    for (int i = 0; i < schedule.size(); i++) {
        int[] intv = schedule.get(i).get(0);
        heap.offer(new int[]{intv[0], intv[1], i, 0});
    }
    List<int[]> out = new ArrayList<>();
    int prevEnd = heap.peek()[1];
    while (!heap.isEmpty()) {
        int[] top = heap.poll();
        if (top[0] > prevEnd) out.add(new int[]{prevEnd, top[0]});
        prevEnd = Math.max(prevEnd, top[1]);
        int nextIdx = top[3] + 1;
        if (nextIdx < schedule.get(top[2]).size()) {
            int[] intv = schedule.get(top[2]).get(nextIdx);
            heap.offer(new int[]{intv[0], intv[1], top[2], nextIdx});
        }
    }
    return out;
}
```



<CodeTrace
  title="k-way merge — 3 employees"
  :values="['[1,2]','[5,6]','[1,3]','[4,10]']"
  :windowKeys="['step']"
  :cellWidth="52"
  :steps='[
    { pointers: { step: 0 }, vars: { heap: "[[1,2],[1,3],[4,10]]", prevEnd: 2 }, note: "seed with each employee`s first" },
    { pointers: { step: 1 }, vars: { heap: "[[1,3],[4,10]]", prevEnd: 3 }, note: "pop [1,2]; no gap" },
    { pointers: { step: 2 }, vars: { heap: "[[4,10],[5,6]]", prevEnd: 3, out: "[[3,4]]" }, note: "pop [1,3]; then advance emp0 to [5,6]. next=[4,10] → gap [3,4]", added: [0] },
    { pointers: { step: 4 }, vars: { heap: "[]", prevEnd: 10 }, note: "drain; no more gaps" }
  ]'
/>

**Complexity** — Time **O(N log k)**; Space **O(k)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Flatten + merge | O(N log N) | O(N) |
| k-way heap merge | **O(N log k)** | **O(k)** |

## Related problems

- [Merge Intervals](/problems/merge-intervals-classic) — flat variant
- [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii) — max concurrency
- [Interval List Intersections](/problems/interval-list-intersections) — two sorted lists
