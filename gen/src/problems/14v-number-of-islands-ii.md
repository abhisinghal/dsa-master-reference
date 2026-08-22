# Union-Find — Number of Islands II

*[↗ LeetCode: Number of Islands II](https://leetcode.com/problems/number-of-islands-ii/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/union-find)

Given `m×n` grid initially all water, add land at positions one at a time. After each add, return the current island count.

**Example** — `m=3, n=3, positions=[[0,0],[0,1],[1,2],[2,1]]` → `[1,1,2,3]`

---

## Approach — Union-Find streaming (add-only, so it works)

**Insight.** Sibling of Number of Provinces, but streaming. Each `add(r, c)` becomes: create component, then try to union with each of the 4 already-existing neighbours. Track a running `count`.

```java
List<Integer> numIslands2(int m, int n, int[][] positions) {
    int[] parent = new int[m * n];
    boolean[] land = new boolean[m * n];
    Arrays.fill(parent, -1);
    int count = 0;
    List<Integer> out = new ArrayList<>();
    int[][] DIR = {{1,0},{-1,0},{0,1},{0,-1}};
    for (int[] p : positions) {
        int r = p[0], c = p[1], idx = r * n + c;
        if (land[idx]) { out.add(count); continue; }
        land[idx] = true; parent[idx] = idx; count++;
        for (int[] d : DIR) {
            int nr = r + d[0], nc = c + d[1], ni = nr * n + nc;
            if (nr < 0 || nr >= m || nc < 0 || nc >= n || !land[ni]) continue;
            int a = find(parent, idx), b = find(parent, ni);
            if (a != b) { parent[a] = b; count--; }
        }
        out.add(count);
    }
    return out;
}
int find(int[] p, int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; }
```

**Complexity** — Time **O(k α(mn))** per add; Space **O(mn)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Union-Find | **O(k α(mn))** | O(mn) |

## Related problems

- [Number of Islands](/problems/hashing-number-of-islands) — static
- [Number of Provinces](/problems/union-find-number-of-provinces)
- [Making A Large Island](https://leetcode.com/problems/making-a-large-island/) — flip one 0 to 1
