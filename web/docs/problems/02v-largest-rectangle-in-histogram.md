# Two Pointers / Monotonic Stack — Largest Rectangle in Histogram

*[↗ LeetCode: Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/monotonic-stack)

Given `heights` of bars with unit width, return the area of the largest rectangle that can be formed.

**Example** — `heights=[2,1,5,6,2,3]` → `10` (rectangle of height 5 over indices 2-3)

**Constraints** — `1 ≤ n ≤ 10⁵`; `0 ≤ h[i] ≤ 10⁴`.

---

## Approach 1 — Brute force (per bar, expand)

**Intuition.** For each bar `i`, expand left and right while heights stay ≥ `h[i]`. Area = `h[i] · width`.



```java
int largestRectangleBrute(int[] h) {
    int best = 0, n = h.length;
    for (int i = 0; i < n; i++) {
        int L = i, R = i;
        while (L > 0 && h[L - 1] >= h[i]) L--;
        while (R < n - 1 && h[R + 1] >= h[i]) R++;
        best = Math.max(best, h[i] * (R - L + 1));
    }
    return best;
}
```



**Complexity** — Time **O(n²)** worst; Space **O(1)**.

---

## Approach 2 — Precompute nearest-smaller left/right

**Insight from brute.** For each `i`, the maximum rectangle with height `h[i]` is bounded by the nearest bar shorter than `h[i]` on each side. Precompute those in two passes.

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Approach 3 — Monotonic stack (single pass)

**Insight from precompute.** Both nearest-smaller-left and nearest-smaller-right can be found in **one** left-to-right pass with a monotonically increasing stack of indices. When a bar smaller than the stack top arrives, pop the top and compute its rectangle: **width = new_top_or_-1 to i**, height = `h[popped]`.

**Trap.** Push a sentinel `0` at the end to flush all remaining bars uniformly.



```java
int largestRectangleArea(int[] h) {
    int n = h.length, best = 0;
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i <= n; i++) {
        int cur = i == n ? 0 : h[i];
        while (!stack.isEmpty() && h[stack.peek()] > cur) {
            int height = h[stack.pop()];
            int left = stack.isEmpty() ? -1 : stack.peek();
            best = Math.max(best, height * (i - left - 1));
        }
        stack.push(i);
    }
    return best;
}
```



<CodeTrace
  title="Monotonic stack — heights=[2,1,5,6,2,3]"
  :values="[2,1,5,6,2,3]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { stack: "[0]", best: 0 }, note: "push idx 0" },
    { pointers: { i: 1 }, vars: { stack: "[1]", best: 2 }, note: "1 lt 2 → pop 2, area 2*1=2, then push 1", added: [0] },
    { pointers: { i: 3 }, vars: { stack: "[1,2,3]", best: 2 }, note: "5, 6 push (increasing)" },
    { pointers: { i: 4 }, vars: { stack: "[1,4]", best: 10 }, note: "2 lt 6 → pop 6 (area 6), pop 5 (area 5*2=10) — NEW BEST", added: [2,3] },
    { pointers: { i: 6 }, vars: { stack: "[1,4,5,6]", best: 10 }, note: "flush at sentinel; no bigger. final = 10" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)**. Optimal.

---

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute per-bar | O(n²) | O(1) |
| Precompute L/R | O(n) | O(n) |
| Monotonic stack | **O(n)** | **O(n)** |

## When to use which

- **Cold interview** → brute → stack. State the "increasing until smaller arrives" invariant.
- **Related problem** → Maximal Rectangle: apply this per row of a binary matrix.

## Related problems

- [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) — apply per-row histogram
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) — sibling: nearest-taller instead of nearest-smaller
- [Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/) — contribution technique via monotonic stack
- [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) — same pattern, different comparator
