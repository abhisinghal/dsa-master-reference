# Greedy — Course Schedule III

*[↗ LeetCode: Course Schedule III](https://leetcode.com/problems/course-schedule-iii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/greedy)

Each course `[duration, lastDay]`. Take max number of courses (one at a time, must finish by lastDay).

## Approach — Sort by deadline + max-heap of durations (regret-based)

**Insight.** Sort by deadline. Iterate; always take the course. If cumulative time exceeds the current deadline, **swap out** the previously-taken course with the largest duration (that's the "regret" step). This keeps the count maximal.

```java
int scheduleCourse(int[][] courses) {
    Arrays.sort(courses, (a, b) -> a[1] - b[1]);
    PriorityQueue<Integer> pq = new PriorityQueue<>(Comparator.reverseOrder());
    int time = 0;
    for (int[] c : courses) {
        time += c[0];
        pq.offer(c[0]);
        if (time > c[1]) time -= pq.poll();
    }
    return pq.size();
}
```

**Why greedy works.** After sorting by deadline, dropping the largest duration among taken courses is always at least as good as dropping the current one — swapping preserves feasibility for the same number of courses picked so far.

**Complexity** — Time **O(n log n)**; Space **O(n)**.

## Related problems

- [Maximum Number of Events That Can Be Attended II](https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended-ii/) — DP variant
- [Task Scheduler](https://leetcode.com/problems/task-scheduler/) — greedy sibling
