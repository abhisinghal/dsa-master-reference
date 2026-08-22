# DP — Delete and Earn

*[↗ LeetCode: Delete and Earn](https://leetcode.com/problems/delete-and-earn/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Delete a number x to earn x points, but doing so also removes all x-1 and x+1. Maximize points.

---

## Approach 1 — Reduce to House Robber
**Insight.** Bucket totals: `points[v] = v · count(v)`. Picking `v` forbids `v±1` — this is exactly House Robber on the `points[]` array indexed by value.



```java
int deleteAndEarn(int[] nums) {
    int max = 0;
    for (int x : nums) max = Math.max(max, x);
    int[] points = new int[max + 1];
    for (int x : nums) points[x] += x;
    int prev = 0, curr = 0;
    for (int v = 0; v <= max; v++) {
        int t = Math.max(curr, prev + points[v]);
        prev = curr; curr = t;
    }
    return curr;
}
```



**Complexity** — Time **O(n + max)**; Space **O(max)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Reduce to House Robber | O(n + max) | O(max) | primary |

## When to use which

- **Ship this** → Reduce to House Robber (O(n + max), O(max)). The pattern's standard solution.

## Related problems

- [House Robber](/problems/dp-house-robber) — the reduction target
- [House Robber II](/problems/house-robber-ii)
