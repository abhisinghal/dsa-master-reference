# Prefix Sum — Range Addition II

*[↗ LeetCode: Range Addition II](https://leetcode.com/problems/range-addition-ii/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/prefix-sum)

`m × n` matrix; each op is `[a, b]` = increment cells `[0..a-1] × [0..b-1]`. After all ops, return the count of the maximum value.

**Example** — `m=3, n=3, ops=[[2,2],[3,3]]` → `4`

## Approach — Intersection of all ops

**Insight.** After all ops, the max cells are precisely the intersection: `[0..min(a_i)-1] × [0..min(b_i)-1]`. Count = product of min-dimensions.

```java
int maxCount(int m, int n, int[][] ops) {
    for (int[] op : ops) { m = Math.min(m, op[0]); n = Math.min(n, op[1]); }
    return m * n;
}
```

**Complexity** — Time **O(#ops)**; Space **O(1)**.

## Related problems

- [Range Addition](/problems/range-addition) — 1D
- [Corporate Flight Bookings](/problems/corporate-flight-bookings)
