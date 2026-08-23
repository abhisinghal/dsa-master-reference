# Topological Sort — Parallel Courses

*[↗ LeetCode: Parallel Courses](https://leetcode.com/problems/parallel-courses/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/topological-sort)

<CompanyTags companies="Amazon, Google, Meta" />

Given `n` courses and prerequisites `[a, b]` (must take `a` before `b`), each semester you can take any courses whose prereqs are met. Return the min number of semesters. `-1` if impossible.

**Example 1** — `n=3, prerequisites=[[1,3],[2,3]]` → `2` (sem 1: {1,2}; sem 2: {3})
**Example 2** — `n=3, prerequisites=[[1,2],[2,3],[3,1]]` → `-1` (cycle)

**Constraints** — `1 ≤ n ≤ 5000`.


<Hints
  hint1="Directed graph? Prerequisites? You need topological order."
  hint2="Kahn’s BFS: start from nodes with indeg 0; when you pop, decrement neighbors’ indeg; add new zeros."
  hint3="For ’layers/semesters’, process one full BFS layer per timestep. For ’unique order?’, check queue size ≤ 1 at every step."
/>
---

<MarkSolved problem-slug="parallel-courses" />


## Approach 1 — DFS with recursion depth

Overestimate. Baseline.

## Approach 2 — Kahn's BFS by levels (canonical)

**Insight.** Toposort in **layers** — each layer is one semester. Count layers.

```java
int minimumSemesters(int n, int[][] relations) {
    List<List<Integer>> g = new ArrayList<>();
    for (int i = 0; i <= n; i++) g.add(new ArrayList<>());
    int[] indeg = new int[n + 1];
    for (int[] r : relations) { g.get(r[0]).add(r[1]); indeg[r[1]]++; }
    Queue<Integer> q = new ArrayDeque<>();
    for (int i = 1; i <= n; i++) if (indeg[i] == 0) q.offer(i);
    int sem = 0, taken = 0;
    while (!q.isEmpty()) {
        sem++;
        for (int sz = q.size(); sz > 0; sz--) {
            int c = q.poll();
            taken++;
            for (int nxt : g.get(c))
                if (--indeg[nxt] == 0) q.offer(nxt);
        }
    }
    return taken == n ? sem : -1;
}
```

<CodeTrace
  title="Layered BFS — n=3, prereqs [[1,3],[2,3]]"
  :values="['1','2','3']"
  :windowKeys="['sem']"
  :cellWidth="34"
  :steps='[
    { pointers: { sem: 1 }, vars: { taken: "{1,2}" }, note: "both indeg 0" },
    { pointers: { sem: 2 }, vars: { taken: "{3}" }, note: "3 unlocked" }
  ]'
/>

**Complexity** — Time **O(n + m)**; Space **O(n + m)**.

---

## Try it yourself

<JavaRunner problem-slug="parallel-courses" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DFS depth | O(n + m) | O(n) | valid but subtle |
| Layered BFS | **O(n + m)** | O(n + m) | canonical |

## When to use which

- **"Min semesters" / "layers"** → layered Kahn's.
- **"Order courses list"** → flat toposort.
- **Course capacity ≤ k per semester** → see [Parallel Courses III](https://leetcode.com/problems/parallel-courses-iii/) — DP on levels.

<AiCompanion problem-slug="parallel-courses" pattern-hint="topological sort" />

## Related problems

- [Course Schedule](/problems/topological-sort-course-schedule)
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)
- [Alien Dictionary](/problems/alien-dictionary)

<FeedbackWidget problem-slug="parallel-courses" />

<RelatedProblems problems="course-schedule::Course Schedule|minimum-height-trees::Minimum Height Trees|sequence-reconstruction::Sequence Reconstruction" />
