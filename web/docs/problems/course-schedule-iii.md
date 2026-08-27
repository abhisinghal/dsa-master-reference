# Greedy — Course Schedule III

*[↗ LeetCode: Course Schedule III](https://leetcode.com/problems/course-schedule-iii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/greedy)

<CompanyTags companies="Amazon, Google" />

Each course `[duration, lastDay]`. Take max number of courses (one at a time). Each must finish by lastDay.

**Example 1** — `courses=[[100,200],[200,1300],[1000,1250],[2000,3200]]` → `3`
**Example 2** — `courses=[[1,2]]` → `1`
**Example 3** — `courses=[[3,2],[4,3]]` → `0` (each course exceeds its own deadline before others start)

**Constraints** — `1 ≤ n ≤ 10⁴`. Brute enumeration of subsets is 2ⁿ = 10³⁰⁰⁰ — impossible. Greedy is O(n log n).


<Hints
  hint1="Is there a local rule that provably gives global optimum? (Exchange argument.)"
  hint2="Sort by the greedy criterion (deadline / end / cost). Iterate; make the locally best choice."
  hint3="If greedy fails, DP is likely needed. But prove greedy's correctness before writing it."
/>
---

<MarkSolved problem-slug="course-schedule-iii" /> <Bookmark problem-slug="course-schedule-iii" />

<InterviewTimer problem-slug="course-schedule-iii" />



## Approach 1 — Brute force subset enumeration

**Intuition.** For each subset of courses, sort by deadline, simulate, check feasibility, track the largest feasible subset size.



```java
int scheduleCourseBrute(int[][] courses) {
    int n = courses.length, best = 0;
    for (int mask = 0; mask < (1 << n); mask++) {
        List<int[]> sub = new ArrayList<>();
        for (int i = 0; i < n; i++) if ((mask & (1 << i)) != 0) sub.add(courses[i]);
        sub.sort((a, b) -> a[1] - b[1]);
        int time = 0; boolean ok = true;
        for (int[] c : sub) {
            time += c[0];
            if (time > c[1]) { ok = false; break; }
        }
        if (ok) best = Math.max(best, sub.size());
    }
    return best;
}
```



**Complexity** — Time **O(2ⁿ · n log n)**; Space **O(n)**. Dies past `n=20`. *In an interview* state this then flip to regret-heap greedy.

---

## Approach 2 — Sort by deadline + max-heap regret (canonical)

**Insight.** Sort by deadline ascending. Iterate; always tentatively take the course; push its duration into a max-heap. If total time now exceeds the current deadline, **swap out** the largest-duration course we've already taken.

**Why greedy works — exchange argument.** After sorting by deadline, suppose optimal takes courses `S`. If greedy would drop the largest-duration course to keep feasibility, it can never be worse than dropping any other, because the largest one being replaced by a smaller-or-equal is a straight improvement to total time budget.



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

**Complexity** — Time **O(n log n)**; Space **O(n)**. *Say aloud in an interview:* "regret-heap greedy — take everything speculatively, then evict the worst if constraints break. Also appears in IPO, Task Scheduler, Meeting Rooms II."

---

## Try it yourself

<JavaRunner problem-slug="course-schedule-iii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Subset brute force | O(2ⁿ · n log n) | O(n) | Reference; TLE past n=20 |
| **Sort + regret heap** | **O(n log n)** | O(n) | **Canonical** |

## When to use which

- **"Max count with deadlines and swap-out"** → regret heap.
- **"Max value"** → weighted variant → DP or different greedy.

<AiCompanion problem-slug="course-schedule-iii" pattern-hint="greedy" />

## Related problems

- [Maximum Events Attended](https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended/)
- [Task Scheduler](https://leetcode.com/problems/task-scheduler/)

<FeedbackWidget problem-slug="course-schedule-iii" />

<RelatedProblems problems="jump-game-ii::Jump Game II|jump-game::Jump Game|minimum-number-of-arrows-to-burst-balloons::Minimum Number Of Arrows To Burst Balloons" />
