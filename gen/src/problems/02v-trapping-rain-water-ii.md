# Two Pointers — Trapping Rain Water II

*[↗ LeetCode: Trapping Rain Water II](https://leetcode.com/problems/trapping-rain-water-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Google, Amazon" />

2D grid of heights; compute total water trapped.

**Example 1** — `heightMap=[[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]` → `4`

**Constraints** — `1 ≤ m, n ≤ 200`.


<Hints
  hint1="Sort first if the input isn’t already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/>
---

<MarkSolved problem-slug="trapping-rain-water-ii" />

<InterviewTimer problem-slug="trapping-rain-water-ii" />



## Approach — Min-heap Dijkstra-style border expansion (canonical)

**Insight.** Water at any cell is bounded by the shortest wall on ANY path to the boundary. Grow a "reached" set from all border cells; always process the **lowest wall reachable** first. When we enter a lower neighbor, water = `current wall - height`; that neighbor becomes a wall at the higher level.

```java
int trapRainWater(int[][] h) {
    int m = h.length, n = h[0].length;
    if (m < 3 || n < 3) return 0;
    boolean[][] seen = new boolean[m][n];
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[2] - b[2]);
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (i == 0 || j == 0 || i == m - 1 || j == n - 1) {
                pq.offer(new int[]{i, j, h[i][j]}); seen[i][j] = true;
            }
    int[][] D = {{1,0},{-1,0},{0,1},{0,-1}};
    int water = 0;
    while (!pq.isEmpty()) {
        int[] c = pq.poll();
        for (int[] d : D) {
            int ni = c[0] + d[0], nj = c[1] + d[1];
            if (ni < 0 || nj < 0 || ni >= m || nj >= n || seen[ni][nj]) continue;
            seen[ni][nj] = true;
            water += Math.max(0, c[2] - h[ni][nj]);
            pq.offer(new int[]{ni, nj, Math.max(c[2], h[ni][nj])});
        }
    }
    return water;
}
```

<CodeTrace
  title="Min-heap Dijkstra-style border expansion (canonical)"
  :values="['1', '4', '3', '1', '3', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 3 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 5 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(mn log(mn))**; Space **O(mn)**.

---

## Try it yourself

<JavaRunner problem-slug="trapping-rain-water-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Min-heap border expansion | **O(mn log(mn))** | O(mn) | canonical |

## When to use which

- **"Process lowest reachable first"** — same idea in path-with-min-effort, swim-in-water.
- **1D** — see [Trapping Rain Water](/problems/trapping-rain-water) — opposing pointers.

<AiCompanion problem-slug="trapping-rain-water-ii" pattern-hint="two pointers" />

## Related problems

- [Trapping Rain Water](/problems/trapping-rain-water)
- [Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/)
- [Path With Minimum Effort](/problems/path-with-minimum-effort)

<FeedbackWidget problem-slug="trapping-rain-water-ii" />
