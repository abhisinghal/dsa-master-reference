# Union-Find — Most Stones Removed With Same Row or Column

*[↗ LeetCode: Most Stones Removed With Same Row or Column](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/union-find)

Given stone positions, a stone can be removed if it shares a row or column with another. Return the max stones removable.

**Example** — `stones=[[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]` → `5`

---

## Approach — Union rows & columns, then count components

**Insight.** Two stones connected iff same row OR column → they belong to one connected component. In any component of size k, exactly k-1 can be removed (one must stay to preserve connectivity). Answer = `total − #components`.

Union each stone's row with its column (offset row indices from column indices).

```java
int removeStones(int[][] stones) {
    Map<Integer, Integer> parent = new HashMap<>();
    for (int[] s : stones) {
        int r = s[0], c = s[1] + 10001;                     // separate namespaces
        parent.putIfAbsent(r, r); parent.putIfAbsent(c, c);
        union(parent, r, c);
    }
    Set<Integer> roots = new HashSet<>();
    for (int key : parent.keySet()) roots.add(find(parent, key));
    return stones.length - roots.size();
}
int find(Map<Integer, Integer> p, int x) { while (p.get(x) != x) { p.put(x, p.get(p.get(x))); x = p.get(x); } return x; }
void union(Map<Integer, Integer> p, int a, int b) { p.put(find(p, a), find(p, b)); }
```

**Complexity** — Time **O(n α(n))**; Space **O(n)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Union rows+cols | **O(n α(n))** | O(n) |

## Related problems

- [Number of Provinces](/problems/union-find-number-of-provinces)
- [Redundant Connection](/problems/redundant-connection)
- [Accounts Merge](/problems/accounts-merge)
