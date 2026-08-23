# Topological Sort — Sequence Reconstruction

*[↗ LeetCode: Sequence Reconstruction](https://leetcode.com/problems/sequence-reconstruction/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/topological-sort)

&lt;CompanyTags companies="Google, Amazon, Meta" /&gt;

Given a target permutation `nums` and a list of subsequences `sequences`, return `true` iff `nums` is the **unique** permutation reconstructible from the sequences.

**Example 1** — `nums=[1,2,3], sequences=[[1,2],[1,3]]` → `false` (also [1,3,2])
**Example 2** — `nums=[1,2,3], sequences=[[1,2],[1,3],[2,3]]` → `true`
**Example 3** — `nums=[4,1,5,2,6,3], sequences=[[5,2,6,3],[4,1,5,2]]` → `true`

**Constraints** — `1 ≤ n ≤ 10⁴`.


&lt;Hints
  hint1="Directed graph? Prerequisites? You need topological order."
  hint2="Kahn’s BFS: start from nodes with indeg 0; when you pop, decrement neighbors’ indeg; add new zeros."
  hint3="For ’layers/semesters’, process one full BFS layer per timestep. For ’unique order?’, check queue size ≤ 1 at every step."
/&gt;
---

## Approach 1 — Try every topological order

Explode to O(n!) — baseline only.

## Approach 2 — Kahn's BFS with uniqueness check (canonical)

**Insight.** Build a graph from consecutive pairs in each sequence. Toposort using Kahn's; **unique** iff at every step exactly one node has indeg 0. Also verify the produced order equals `nums`.



```java
boolean sequenceReconstruction(int[] nums, List<List<Integer>> sequences) {
    int n = nums.length;
    List<Set<Integer>> g = new ArrayList<>();
    for (int i = 0; i <= n; i++) g.add(new HashSet<>());
    int[] indeg = new int[n + 1];
    Set<Integer> seen = new HashSet<>();
    for (List<Integer> s : sequences) {
        for (int x : s) seen.add(x);
        for (int i = 1; i < s.size(); i++)
            if (g.get(s.get(i - 1)).add(s.get(i))) indeg[s.get(i)]++;
    }
    if (seen.size() != n) return false;
    Queue<Integer> q = new ArrayDeque<>();
    for (int i = 1; i <= n; i++) if (indeg[i] == 0) q.offer(i);
    int idx = 0;
    while (!q.isEmpty()) {
        if (q.size() > 1) return false; // ambiguous
        int c = q.poll();
        if (c != nums[idx++]) return false;
        for (int nxt : g.get(c)) if (--indeg[nxt] == 0) q.offer(nxt);
    }
    return idx == n;
}
```



<CodeTrace
  title="Try every topological order"
  :values="['1', '2', '3']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n + m)**; Space **O(n + m)**.

---

## Try it yourself

<JavaRunner problem-slug="sequence-reconstruction" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Enumerate orders | O(n!) | O(n) | trivia |
| Kahn's + uniqueness | **O(n + m)** | O(n + m) | canonical |

## When to use which

- **"Unique toposort?"** → check queue size ≤ 1 at every step.
- **"Number of topological orders"** → DP on states (bitmask if n ≤ 20).
- **"Restore from partial orderings"** → same graph build + Kahn's.

&lt;AiCompanion problem-slug="sequence-reconstruction" pattern-hint="topological sort" /&gt;

## Related problems

- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)
- [Alien Dictionary](/problems/alien-dictionary)
- [Parallel Courses](/problems/parallel-courses)