# BS on Answer — Path With Minimum Effort

*[↗ LeetCode: Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/bs-on-answer)

<CompanyTags companies="Amazon, Google" />

In a 2D grid of heights, an "effort" of a path is the max abs-diff between consecutive cells. Return the min effort from top-left to bottom-right (4-connected).

**Example** — `heights=[[1,2,2],[3,8,2],[5,3,5]]` → `2`

**Constraints** — `1 ≤ m, n ≤ 100`; `0 ≤ height[i][j] ≤ 10⁶`.


<Hints
  hint1="Can I write a `feasible(x)` check that returns true iff answer ≤ x (or ≥ x)?"
  hint2="If `feasible` is monotonic in x, binary search over the answer space `[lo, hi]`. Range: min possible value to max possible value."
  hint3="The feasibility check is O(n); total complexity is O(n log range)."
/>
---

<MarkSolved problem-slug="path-with-minimum-effort" />

<InterviewTimer problem-slug="path-with-minimum-effort" />



## Approach 1 — Dijkstra with edge weight = max-so-far

O(mn log mn).

## Approach 2 — Binary search on the effort + BFS reachability

**Insight.** `feasible(e)` = can we walk from start to end using only edges with `|diff| ≤ e`? Monotonic. Binary search minimum `e`.

```java
int minimumEffortPath(int[][] h) {
    int m = h.length, n = h[0].length;
    int lo = 0, hi = 1_000_000;
    int[][] DIR = {{1,0},{-1,0},{0,1},{0,-1}};
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        boolean[][] seen = new boolean[m][n];
        Deque<int[]> q = new ArrayDeque<>();
        q.offer(new int[]{0, 0}); seen[0][0] = true;
        while (!q.isEmpty()) {
            int[] c = q.poll();
            if (c[0] == m - 1 && c[1] == n - 1) break;
            for (int[] d : DIR) {
                int r = c[0] + d[0], col = c[1] + d[1];
                if (r < 0 || r >= m || col < 0 || col >= n || seen[r][col]) continue;
                if (Math.abs(h[r][col] - h[c[0]][c[1]]) <= mid) { seen[r][col] = true; q.offer(new int[]{r, col}); }
            }
        }
        if (seen[m - 1][n - 1]) hi = mid;
        else                    lo = mid + 1;
    }
    return lo;
}
```

<CodeTrace
  title="Dijkstra with edge weight = max-so-far"
  :values="['1', '2', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(mn · log(max))**; Space **O(mn)**.

## Try it yourself

<JavaRunner problem-slug="path-with-minimum-effort" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Dijkstra | O(mn log mn) | O(mn) |
| BS + BFS | **O(mn log(max))** | O(mn) |

## When to use which

- **"Min max edge on path"** → BS on answer OR Dijkstra with max-of-path metric OR MST.
- **Dijkstra variant** — replace sum with max in relaxation.
- **Streaming edge addition** → Union-Find with sorted edges.

<AiCompanion problem-slug="path-with-minimum-effort" pattern-hint="binary search on answer" />

## Related problems

- [Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/) — same idea, sea level = effort
- [Path With Maximum Minimum Value](https://leetcode.com/problems/path-with-maximum-minimum-value/) — dual (maximize min)

<FeedbackWidget problem-slug="path-with-minimum-effort" />
