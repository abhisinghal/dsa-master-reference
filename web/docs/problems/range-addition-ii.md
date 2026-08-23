# Prefix Sum — Range Addition II

*[↗ LeetCode: Range Addition II](https://leetcode.com/problems/range-addition-ii/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/prefix-sum)

Given matrix of zeros `m × n` and operations `[a, b]` that add 1 to every cell in `[0, a) × [0, b)`, return the count of maximum-valued cells.

**Example 1** — `m=3, n=3, ops=[[2,2],[3,3]]` → `4` (top-left 2×2 has value 2)
**Example 2** — `m=3, n=3, ops=[]` → `9`
**Example 3** — `m=3, n=3, ops=[[1,1]]` → `1`

**Constraints** — `1 ≤ m, n ≤ 4·10⁴`; `0 ≤ ops.length ≤ 10⁴`.


&lt;Hints
  hint1="Ask: can I answer `sum(i, j)` in O(1) given a preprocessed structure?"
  hint2="Prefix sums let you compute range sums as `pref[j+1] - pref[i]`. For ’count subarrays with property X on sum’, use a hash-map of prefix sums."
  hint3="For ’≥ 2 length’ or ’divisible by k’ variants, store first occurrence and check remainders."
/&gt;
---

&lt;MarkSolved problem-slug="range-addition-ii" /&gt;

&lt;InterviewTimer problem-slug="range-addition-ii" /&gt;



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



<CodeTrace
  title="Actually apply operations"
  :values="['2', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(#ops)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="range-addition-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Simulate | O(#ops · m·n) | O(m·n) | baseline |
| Intersect rectangles | **O(#ops)** | **O(1)** | optimum |

## When to use which

- **All rectangles anchored at corner** → intersection min trick.
- **Arbitrary rectangle positions** → 2D difference array.

&lt;AiCompanion problem-slug="range-addition-ii" pattern-hint="prefix sum" /&gt;

## Related problems

- [Range Addition](/problems/range-addition)
- [Matrix Block Sum](/problems/matrix-block-sum)

&lt;FeedbackWidget problem-slug="range-addition-ii" /&gt;
