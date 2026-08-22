# Topological Sort — Course Schedule II

*[↗ LeetCode: Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/topological-sort)

Given `numCourses` and `prerequisites[i] = [a, b]` meaning "to take `a` you must first take `b`", return an ordering, or `[]` if impossible (cycle).

**Example 1** — `n=2, [[1,0]]` → `[0,1]`
**Example 2** — `n=4, [[1,0],[2,0],[3,1],[3,2]]` → `[0,1,2,3]` or `[0,2,1,3]`
**Example 3** — `n=2, [[1,0],[0,1]]` → `[]` (cycle)

**Constraints** — `1 ≤ n ≤ 2000`; `0 ≤ #prereqs ≤ n·(n−1)/2`.

---

## Approach 1 — Brute force (try every permutation)

**Intuition.** Enumerate every permutation; return the first that respects all prerequisites.

**Complexity** — Time **O(n!)** — impossible past n≈10.

---

## Approach 2 — DFS with color marking (post-order)

**Insight from brute.** A course can be placed *after* all its prerequisites; DFS in post-order emits nodes in reverse topological order.

Use 3 colors: `WHITE` = unvisited, `GRAY` = on the current path (cycle detection), `BLACK` = finished.

**Trap.** If DFS revisits a `GRAY` node → cycle → return `[]`.

```java
int[] findOrderDFS(int n, int[][] prereqs) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] p : prereqs) adj.get(p[1]).add(p[0]);
    int[] color = new int[n];
    LinkedList<Integer> post = new LinkedList<>();
    for (int i = 0; i < n; i++) if (color[i] == 0 && !dfs(i, adj, color, post)) return new int[0];
    int[] out = new int[n];
    int k = 0;
    for (int x : post) out[k++] = x;
    return out;
}
boolean dfs(int u, List<List<Integer>> adj, int[] color, LinkedList<Integer> post) {
    color[u] = 1;                                       // gray
    for (int v : adj.get(u)) {
        if (color[v] == 1) return false;                // back-edge → cycle
        if (color[v] == 0 && !dfs(v, adj, color, post)) return false;
    }
    color[u] = 2;                                       // black
    post.addFirst(u);                                    // prepend for reverse post-order
    return true;
}
```

**Complexity** — Time **O(V + E)**; Space **O(V + E)**. Optimal.

---

## Approach 3 — Kahn's algorithm (BFS on in-degrees)

**Insight from DFS.** Iteratively remove nodes whose in-degree is 0 — they are "always safe next." Repeat until empty (or cycle).

**Bonus.** Kahn's naturally returns the topological order forward-emitting (no reverse); easier for interviewers to trust.

```java
int[] findOrder(int n, int[][] prereqs) {
    int[] indeg = new int[n];
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] p : prereqs) { adj.get(p[1]).add(p[0]); indeg[p[0]]++; }
    Deque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.offer(i);
    int[] out = new int[n];
    int k = 0;
    while (!q.isEmpty()) {
        int u = q.poll();
        out[k++] = u;
        for (int v : adj.get(u)) if (--indeg[v] == 0) q.offer(v);
    }
    return k == n ? out : new int[0];                    // cycle → k < n
}
```

<CodeTrace
  title="Kahn — n=4, edges 0→1, 0→2, 1→3, 2→3"
  :values="[0,1,2,3]"
  :windowKeys="['emitted']"
  :cellWidth="46"
  :steps='[
    { pointers: { emitted: 0 }, vars: { indeg: "[0,1,1,2]", queue: "[0]" }, note: "seed with in-degree 0" },
    { pointers: { emitted: 1 }, vars: { indeg: "[_,0,0,2]", queue: "[1,2]", out: "[0]" }, note: "pop 0 → 1 and 2 unlock", added: [0] },
    { pointers: { emitted: 2 }, vars: { indeg: "[_,_,0,1]", queue: "[2]", out: "[0,1]" }, note: "pop 1", added: [1] },
    { pointers: { emitted: 3 }, vars: { indeg: "[_,_,_,0]", queue: "[3]", out: "[0,1,2]" }, note: "pop 2 → 3 unlocks", added: [2] },
    { pointers: { emitted: 4 }, vars: { queue: "[]", out: "[0,1,2,3]" }, note: "pop 3. k=n → success", added: [3] }
  ]'
/>

**Complexity** — Time **O(V + E)**; Space **O(V + E)**.

---

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Permutations | O(n!) | O(n) |
| DFS post-order | **O(V + E)** | O(V + E) |
| Kahn BFS | **O(V + E)** | O(V + E) |

## When to use which

- **Cold interview** → Kahn is easier to explain and debug live.
- **DFS variant** → useful when you also need SCC or bridges.
- **Cycle detection is the primary need** → either works; DFS with color is cleaner.

## Related problems (same ladder applies)

- [Course Schedule I](https://leetcode.com/problems/course-schedule/) — Kahn returns just "can we finish?"
- [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) — build the DAG from adjacent word pairs, then topo-sort
- [Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/) — peel leaves iteratively (topo-sort variant)
- [Parallel Courses](https://leetcode.com/problems/parallel-courses/) — Kahn tracking levels (semesters)
