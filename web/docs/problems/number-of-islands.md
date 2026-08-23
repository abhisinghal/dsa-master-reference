# Hashing — Number of Islands

*[↗ LeetCode: Number of Islands](https://leetcode.com/problems/number-of-islands/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dfs)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg, Apple" /&gt;

Count connected components of `'1'`s in a binary grid.

**Example 1** — Grid → count.

**Constraints** — `1 ≤ m, n ≤ 300`.


&lt;Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/&gt;
---

&lt;MarkSolved problem-slug="number-of-islands" /&gt;

&lt;InterviewTimer problem-slug="number-of-islands" /&gt;



## Approach 1 — DFS flood fill (canonical)

Iterate cells; on unseen `'1'`, `count++`, DFS marking `'0'`.



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
Same idea, queue instead of recursion — avoids stack overflow on huge grids.

## Approach 3 — Union-Find
Union adjacent `'1'`s; count components at end. Useful for streaming (Islands II).

**Complexity** — Time **O(mn)**; Space **O(mn)**.

---

## Try it yourself

<JavaRunner problem-slug="number-of-islands" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DFS | O(mn) | O(mn) stack | canonical |
| BFS | O(mn) | O(min(m,n)) queue | safer |
| UF | O(mn·α) | O(mn) | streaming variant |

## When to use which

- **Static grid, small** → DFS.
- **Deep recursion risk** → BFS.
- **Streaming land additions** → UF (see [Number of Islands II](/problems/number-of-islands-ii)).

&lt;AiCompanion problem-slug="number-of-islands" pattern-hint="hashing" /&gt;

## Related problems

- [Number of Islands II](/problems/number-of-islands-ii)
- [Max Area of Island](https://leetcode.com/problems/max-area-of-island/)
- [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/)

&lt;FeedbackWidget problem-slug="number-of-islands" /&gt;
