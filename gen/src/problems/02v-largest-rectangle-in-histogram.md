# Two Pointers — Largest Rectangle in Histogram

*[↗ LeetCode: Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/monotonic-stack)

Given bar heights, return the largest rectangle area contained.

> Filed under Two Pointers by our curriculum because the O(n) solution uses **two pointer walks** (previous-smaller and next-smaller). But the canonical implementation is a monotonic stack — see the [Monotonic Stack chapter](/patterns/monotonic-stack).

## Approach 1 — For each bar, expand outward

O(n²) — for each `i`, walk left/right while ≥ heights[i].

## Approach 2 — Monotonic increasing stack

**Insight.** When we push bar `i` and pop bar `t` (because heights[i] < heights[t]), we now know both boundaries of `t`'s maximal rectangle: `next smaller = i`, `previous smaller = stack.peek()` after pop. Area = `heights[t] * (i - prev - 1)`.

```java
int largestRectangleArea(int[] heights) {
    Deque<Integer> stack = new ArrayDeque<>();
    int best = 0, n = heights.length;
    for (int i = 0; i <= n; i++) {
        int h = i == n ? 0 : heights[i];
        while (!stack.isEmpty() && heights[stack.peek()] > h) {
            int t = stack.pop();
            int width = stack.isEmpty() ? i : i - stack.peek() - 1;
            best = Math.max(best, heights[t] * width);
        }
        stack.push(i);
    }
    return best;
}
```

**Sentinel trick.** Iterate `i` to `n` inclusive with `h=0` to flush the stack cleanly.

**Complexity** — Time **O(n)**; Space **O(n)**.

## Related problems

- [Maximal Rectangle](/problems/maximal-rectangle) — stack of largest-rectangle across rows
- [Sum of Subarray Minimums](/problems/sum-of-subarray-minimums)
- [Trapping Rain Water](/problems/trapping-rain-water) — sibling two-pointer/stack problem
