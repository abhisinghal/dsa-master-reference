# Prefix Sum — Range Addition II

*[↗ LeetCode: Range Addition II](https://leetcode.com/problems/range-addition-ii/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/prefix-sum)

Given matrix of zeros `m × n` and operations `[a, b]` that add 1 to every cell in `[0, a) × [0, b)`, return the count of maximum-valued cells.

**Example 1** — `m=3, n=3, ops=[[2,2],[3,3]]` → `4` (top-left 2×2 has value 2)
**Example 2** — `m=3, n=3, ops=[]` → `9`
**Example 3** — `m=3, n=3, ops=[[1,1]]` → `1`

**Constraints** — `1 ≤ m, n ≤ 4·10⁴`; `0 ≤ ops.length ≤ 10⁴`.

---

## Approach 1 — Actually apply operations

O(#ops · m·n). Baseline.

## Approach 2 — Intersection of all rectangles (canonical)

**Insight.** Every op starts at (0,0). The max-valued cells are the intersection of all rectangles — i.e., `min(a) × min(b)`.

```java
int maxCount(int m, int n, int[][] ops) {
    for (int[] op : ops) { m = Math.min(m, op[0]); n = Math.min(n, op[1]); }
    return m * n;
}
```

**Complexity** — Time **O(#ops)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Simulate | O(#ops · m·n) | O(m·n) | baseline |
| Intersect rectangles | **O(#ops)** | **O(1)** | optimum |

## When to use which

- **All rectangles anchored at corner** → intersection min trick.
- **Arbitrary rectangle positions** → 2D difference array.

## Related problems

- [Range Addition](/problems/range-addition)
- [Matrix Block Sum](/problems/matrix-block-sum)
