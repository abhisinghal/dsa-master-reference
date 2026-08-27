# Two Pointers — Trapping Rain Water II

*[↗ LeetCode: Trapping Rain Water II](https://leetcode.com/problems/trapping-rain-water-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Google, Amazon" />

2D grid of heights; compute total water trapped.

**Example 1** — `heightMap=[[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]` → `4`
**Example 2** — `heightMap=[[3,3,3,3,3],[3,2,2,2,3],[3,2,1,2,3],[3,2,2,2,3],[3,3,3,3,3]]` → `10` (a symmetric bowl)
**Example 3** — `heightMap=[[1]]` → `0` (grid too small to trap anything)

**Constraints** — `1 ≤ m, n ≤ 200`. Brute per-cell BFS is O((mn)²) — for 200×200 that's 1.6·10⁹ ops. The heap solution is O(mn log(mn)) ≈ 4·10⁵ — 4000× faster.


<Hints
  hint1="Sort first if the input isn't already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/>
---

<MarkSolved problem-slug="trapping-rain-water-ii" /> <Bookmark problem-slug="trapping-rain-water-ii" />

<InterviewTimer problem-slug="trapping-rain-water-ii" />



## Approach 1 — Brute force per-cell BFS

**Intuition.** For each interior cell, find the minimum wall height on every path to the border. Water above the cell = max(0, min_max_path − cell height). Run BFS from every cell.

```java
int trapRainWaterBrute(int[][] h) {
    int m = h.length, n = h[0].length, water = 0;
    for (int r = 1; r < m - 1; r++)
        for (int c = 1; c < n - 1; c++) {
            int seal = maxWallOnEasiestPath(h, r, c);   // BFS/DFS to border
            if (seal > h[r][c]) water += seal - h[r][c];
        }
    return water;
}
// maxWallOnEasiestPath omitted — Dijkstra-lite on max-of-min for each cell.
```

**Complexity** — Time **O((mn)² log(mn))** or worse per-cell BFS; Space **O(mn)** per query. For 200×200 = 40,000 cells, each with its own BFS across 40,000 cells — 1.6·10⁹ ops. TLE. *In an interview* state this then flip perspective.

---

## Approach 2 — Min-heap Dijkstra-style border expansion (canonical)

**Insight.** Instead of asking "for each cell, what's the sealing wall?", grow a "sealed region" outward from the border. Always expand the **lowest current sealing wall** first (min-heap). When we enter a lower neighbor, water fills = `current wall - neighbor height`; that neighbor's *effective* wall becomes the higher of its own height or the sealing wall.

Same shape as Dijkstra: nearest-uneaten cell first, monotone frontier, O(V log V) total.

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

**Complexity** — Time **O(mn log(mn))**; Space **O(mn)**. *Say aloud in an interview:* "same Dijkstra shape as swim-in-rising-water and path-with-min-effort — always process the current-lowest-wall cell first."

---

## Try it yourself

<JavaRunner problem-slug="trapping-rain-water-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Per-cell BFS | O((mn)² log(mn)) | O(mn) | TLE past 40×40 |
| **Min-heap border expansion** | **O(mn log(mn))** | O(mn) | **Canonical** |

## When to use which

- **"Process lowest reachable first"** — same idea in path-with-min-effort, swim-in-water.
- **1D** — see [Trapping Rain Water](/problems/trapping-rain-water) — opposing pointers.

<AiCompanion problem-slug="trapping-rain-water-ii" pattern-hint="two pointers" />

## Related problems

- [Trapping Rain Water](/problems/trapping-rain-water)
- [Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/)
- [Path With Minimum Effort](/problems/path-with-minimum-effort)

<FeedbackWidget problem-slug="trapping-rain-water-ii" />
