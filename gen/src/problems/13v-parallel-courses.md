# Topological Sort — Parallel Courses

*[↗ LeetCode: Parallel Courses](https://leetcode.com/problems/parallel-courses/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/topological-sort)

`n` courses; `relations[i] = [a, b]` means take `a` before `b`. In each semester take any set of courses whose prereqs are satisfied. Return the minimum semesters, or `-1` if impossible.

**Example** — `n=3, relations=[[1,3],[2,3]]` → `2` (semester 1: courses 1,2; semester 2: course 3)

---

## Approach 1 — Kahn's tracking semester level

**Insight.** BFS by *layer* on the DAG. Each layer = one semester's courses.

```java
int minimumSemesters(int n, int[][] relations) {
    int[] indeg = new int[n + 1];
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i <= n; i++) adj.add(new ArrayList<>());
    for (int[] r : relations) { adj.get(r[0]).add(r[1]); indeg[r[1]]++; }
    Deque<Integer> q = new ArrayDeque<>();
    for (int i = 1; i <= n; i++) if (indeg[i] == 0) q.offer(i);
    int semesters = 0, done = 0;
    while (!q.isEmpty()) {
        semesters++;
        for (int size = q.size(); size > 0; size--) {
            int u = q.poll(); done++;
            for (int v : adj.get(u)) if (--indeg[v] == 0) q.offer(v);
        }
    }
    return done == n ? semesters : -1;
}
```

<CodeTrace
  title="Layered BFS — n=3, edges 1→3, 2→3"
  :values="[1,2,3]"
  :windowKeys="['sem']"
  :cellWidth="46"
  :steps='[
    { pointers: { sem: 0 }, vars: { indeg: "[_,0,0,2]", queue: "[1,2]" }, note: "seed: in-deg 0" },
    { pointers: { sem: 1 }, vars: { done: 2, queue: "[3]" }, note: "layer 1: take {1,2}. 3 unlocks", added: [0,1] },
    { pointers: { sem: 2 }, vars: { done: 3 }, note: "layer 2: take {3}. answer 2", added: [2] }
  ]'
/>

**Complexity** — Time **O(V + E)**; Space **O(V + E)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Kahn's by layer | **O(V + E)** | O(V + E) |

## Related problems

- [Course Schedule II](/problems/topological-sort-course-schedule) — return order
- [Parallel Courses II](https://leetcode.com/problems/parallel-courses-ii/) — with a per-semester cap → NP-hard, bitmask DP
- [Parallel Courses III](https://leetcode.com/problems/parallel-courses-iii/) — course durations added
