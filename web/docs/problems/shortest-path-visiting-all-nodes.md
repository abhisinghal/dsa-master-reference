# DP — Shortest Path Visiting All Nodes

*[↗ LeetCode: Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

&lt;CompanyTags companies="Google, Amazon, Meta" /&gt;

Undirected graph. Shortest length path visiting every node (may reuse).

**Constraints** — `1 ≤ n ≤ 12`.

**Example 1** — `graph=[[1,2,3],[0],[0],[0]]` → `4`
**Example 2** — `graph=[[1],[0,2,4],[1,3,4],[2],[1,2]]` → `4`


&lt;Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/&gt;
---

## Approach — Bitmask BFS (canonical)

**Insight.** State = `(node, visitedMask)`. BFS from all `(i, 1 << i)` starts.



```java
int shortestPathLength(int[][] graph) {
    int n = graph.length, full = (1 << n) - 1;
    Queue<int[]> q = new ArrayDeque<>();
    boolean[][] seen = new boolean[n][1 << n];
    for (int i = 0; i < n; i++) {
        q.offer(new int[]{i, 1 << i});
        seen[i][1 << i] = true;
    }
    int steps = 0;
    while (!q.isEmpty()) {
        for (int sz = q.size(); sz > 0; sz--) {
            int[] c = q.poll();
            if (c[1] == full) return steps;
            for (int nb : graph[c[0]]) {
                int nMask = c[1] | (1 << nb);
                if (!seen[nb][nMask]) { seen[nb][nMask] = true; q.offer(new int[]{nb, nMask}); }
            }
        }
        steps++;
    }
    return -1;
}
```



<CodeTrace
  title="Bitmask BFS (canonical)"
  :values="['1', '2', '3']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n · 2ⁿ · degree)**; Space **O(n · 2ⁿ)**.

---

## Try it yourself

<JavaRunner problem-slug="shortest-path-visiting-all-nodes" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Bitmask BFS | **O(n · 2ⁿ · deg)** | O(n · 2ⁿ) | canonical |

## When to use which

- **Small n + reachable revisits** → bitmask BFS.
- **Exact TSP** → same DP.
- **k people delivery** → k-source BFS extension.

&lt;AiCompanion problem-slug="shortest-path-visiting-all-nodes" pattern-hint="dynamic programming" /&gt;

## Related problems

- [Number of Ways to Wear Different Hats](/problems/number-of-ways-to-wear-different-hats-to-each-other)
- [Find the Shortest Superstring](/problems/find-the-shortest-superstring)