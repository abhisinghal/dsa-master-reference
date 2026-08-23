# DP — Delete and Earn

*[↗ LeetCode: Delete and Earn](https://leetcode.com/problems/delete-and-earn/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Delete `x` to earn `x` points; also removes all `x-1` and `x+1`. Max points.

**Example 1** — `nums=[3,4,2]` → `6`
**Example 2** — `nums=[2,2,3,3,3,4]` → `9`

**Constraints** — `1 ≤ n ≤ 2·10⁴`.

---

## Approach — Reduce to House Robber (canonical)

**Insight.** Bucket totals: `points[v] = v · count(v)`. Picking `v` forbids `v±1` — exactly House Robber on `points[]`.



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

| Approach | Time | Space | Grade |
|---|---|---|---|
| Reduce to House Robber | **O(n + max)** | O(max) | canonical |

## When to use which

- **"Adjacent-value taboo"** → reduce to House Robber.
- **Sparse values** → skip zeros; use TreeMap.

## Related problems

- [House Robber](/problems/dp-house-robber)
- [House Robber II](/problems/house-robber-ii)
