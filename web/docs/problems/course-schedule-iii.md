# Greedy — Course Schedule III

*[↗ LeetCode: Course Schedule III](https://leetcode.com/problems/course-schedule-iii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/greedy)

Each course `[duration, lastDay]`. Take max number of courses (one at a time). Each must finish by lastDay.

**Example 1** — `courses=[[100,200],[200,1300],[1000,1250],[2000,3200]]` → `3`

**Constraints** — `1 ≤ n ≤ 10⁴`.

---

## Approach — Sort by deadline + max-heap regret (canonical)

**Insight.** Sort by deadline ascending. Iterate; always take the course; push duration into max-heap. If total time exceeds current deadline, **swap out** the previously-taken course with the largest duration.

**Why greedy works.** After sorting by deadline, dropping the largest duration among taken courses is always at least as good as dropping the current one — swap preserves feasibility for the same count.



```java
int scheduleCourse(int[][] courses) {
    Arrays.sort(courses, (a, b) -> a[1] - b[1]);
    PriorityQueue<Integer> pq = new PriorityQueue<>(Comparator.reverseOrder());
    int time = 0;
    for (int[] c : courses) {
        time += c[0]; pq.offer(c[0]);
        if (time > c[1]) time -= pq.poll();
    }
    return pq.size();
}
```



<CodeTrace
  title="Sort by deadline + max-heap regret (canonical)"
  :values="['100', '200']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(n)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Regret heap | **O(n log n)** | O(n) | canonical |

## When to use which

- **"Max count with deadlines and swap-out"** → regret heap.
- **"Max value"** → weighted variant → DP or different greedy.

## Related problems

- [Maximum Events Attended](https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended/)
- [Task Scheduler](https://leetcode.com/problems/task-scheduler/)
