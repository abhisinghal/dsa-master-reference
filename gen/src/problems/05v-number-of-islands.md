# Hashing — Number of Islands

*[↗ LeetCode: Number of Islands](https://leetcode.com/problems/number-of-islands/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dfs)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg, Apple" />

Count connected components of `'1'`s in a binary grid.

**Example 1** — `grid=[["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]` → `1`
**Example 2** — `grid=[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]` → `3`
**Example 3** — `grid=[["0"]]` → `0`

**Constraints** — `1 ≤ m, n ≤ 300`. Brute per-cell BFS/DFS is already O(mn) — the bottleneck is careful marking, not counting. For 300×300 = 9·10⁴ ops. Union-Find variant is O(mn · α(mn)) — same asymptotic but streaming-friendly. Brute checks connectivity between every pair of land cells — O((m·n)²) = 10¹⁰ ops at max grid. BFS/DFS flood-fill visits each cell once → O(m·n) = 9·10⁴ ops = <10 ms.
<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its 'canonical form' — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For 'first duplicate', a `HashSet` and single-pass `add()` is enough."
/>
---

<MarkSolved problem-slug="number-of-islands" /> <Bookmark problem-slug="number-of-islands" />

<InterviewTimer problem-slug="number-of-islands" />



## Approach 1 — DFS flood fill (canonical)

**Insight.** Iterate every cell. When you find an unseen `'1'`, increment the count and DFS to mark the *whole island* as `'0'` (so we never re-count).

```java
int numIslands(char[][] grid) {
    int m = grid.length, n = grid[0].length, count = 0;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (grid[i][j] == '1') { count++; dfs(grid, i, j); }
    return count;
}
void dfs(char[][] g, int i, int j) {
    if (i < 0 || j < 0 || i >= g.length || j >= g[0].length || g[i][j] != '1') return;
    g[i][j] = '0';
    dfs(g, i+1, j); dfs(g, i-1, j); dfs(g, i, j+1); dfs(g, i, j-1);
}
```

## Approach 2 — BFS

**Same idea**, queue instead of recursion — avoids stack overflow on huge grids. For 300×300 = 9·10⁴ cells, DFS recursion depth can hit 9·10⁴ frames on a fully-connected grid — JVM default stack (512 KB, ~15,000 frames) blows. BFS never has that risk.

## Approach 3 — Union-Find

Union adjacent `'1'`s; count distinct components at the end. Useful for the streaming variant *"grids arrive one cell at a time"* — see [Number of Islands II](/problems/number-of-islands-ii). O(mn · α) with path compression + union-by-rank.

**Complexity** — Time **O(mn)** for DFS/BFS; **O(mn · α(mn))** for Union-Find; Space **O(mn)** for grid mark or O(min(m,n)) for BFS queue. *Say aloud in an interview:* "state DFS as the reference, mention BFS for stack-overflow safety on large grids, then say UF for streaming."

---

## Try it yourself

<JavaRunner problem-slug="number-of-islands" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| **DFS** | **O(mn)** | O(mn) stack | **Canonical** |
| BFS | O(mn) | O(min(m,n)) queue | Safer on large grids |
| UF | O(mn·α) | O(mn) | Streaming variant |

## When to use which

- **Static grid, small** → DFS.
- **Deep recursion risk** → BFS.
- **Streaming land additions** → UF (see [Number of Islands II](/problems/number-of-islands-ii)).

<AiCompanion problem-slug="number-of-islands" pattern-hint="hashing" />

## Related problems

- [Number of Islands II](/problems/number-of-islands-ii)
- [Max Area of Island](https://leetcode.com/problems/max-area-of-island/)
- [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/)

<FeedbackWidget problem-slug="number-of-islands" />
