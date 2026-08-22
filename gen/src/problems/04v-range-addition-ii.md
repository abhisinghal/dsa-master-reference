# Prefix Sum — Range Addition II

*[↗ LeetCode: Range Addition II](https://leetcode.com/problems/range-addition-ii/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/prefix-sum)

`m × n` matrix; each op is `[a, b]` = increment cells `[0..a-1] × [0..b-1]`. After all ops, return the count of the maximum value.

**Example** — `m=3, n=3, ops=[[2,2],[3,3]]` → `4`

---

## Approach 1 — Intersection of all ops
**Insight.** After all ops, the max cells are precisely the intersection: `[0..min(a_i)-1] × [0..min(b_i)-1]`. Count = product of min-dimensions.

```java
int maxCount(int m, int n, int[][] ops) {
    for (int[] op : ops) { m = Math.min(m, op[0]); n = Math.min(n, op[1]); }
    return m * n;
}
```


<CodeTrace
  title="Intersection of all ops"
  :values="['2', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize; scan begins." },
    { pointers: { i: 0 }, vars: { phase: "midway" }, note: "Midway through the scan." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "All positions considered — return the answer." }
  ]'
/>


**Complexity** — Time **O(#ops)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Intersection of all ops | O(#ops) | O(1) | primary |

## When to use which

- **Ship this** → Intersection of all ops (O(#ops), O(1)). The pattern's standard solution.

## Related problems

- [Range Addition](/problems/range-addition) — 1D
- [Corporate Flight Bookings](/problems/corporate-flight-bookings)
