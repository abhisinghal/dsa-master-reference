# Prefix Sum — Maximal Rectangle

*[↗ LeetCode: Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/prefix-sum)

Given a binary matrix, find the largest all-1s axis-aligned rectangle.

**Example** — `matrix=[[1,0,1,0,0],[1,0,1,1,1],[1,1,1,1,1],[1,0,0,1,0]]` → `6`

---

## Approach 1 — Per-row histogram + Largest Rectangle in Histogram
**Insight.** For each row, compute the running "height" of consecutive 1s above each column. That row of heights = a histogram. The answer is `max` over each row's LRH.

```java
int maximalRectangle(char[][] mat) {
    if (mat.length == 0) return 0;
    int m = mat.length, n = mat[0].length;
    int[] h = new int[n];
    int best = 0;
    for (int r = 0; r < m; r++) {
        for (int c = 0; c < n; c++) h[c] = mat[r][c] == '1' ? h[c] + 1 : 0;
        best = Math.max(best, largestRectangle(h));
    }
    return best;
}
int largestRectangle(int[] h) {
    Deque<Integer> stack = new ArrayDeque<>();
    int best = 0;
    for (int i = 0; i <= h.length; i++) {
        int cur = i == h.length ? 0 : h[i];
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
  title="Per-row histogram + Largest Rectangle in Histogram"
  :values="['1', '0', '1', '0', '0']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize; scan begins." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through the scan." },
    { pointers: { i: 4 }, vars: { phase: "done" }, note: "All positions considered — return the answer." }
  ]'
/>


**Complexity** — Time **O(m·n)**; Space **O(n)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Per-row histogram + Largest Rectangle in H… | O(m·n) | O(n) | primary |

## When to use which

- **Ship this** → Per-row histogram + Largest Rectangle in Histogram (O(m·n), O(n)). The pattern's standard solution.

## Related problems

- [Largest Rectangle in Histogram](/problems/largest-rectangle-in-histogram)
- [Maximal Square](https://leetcode.com/problems/maximal-square/) — sibling DP
- [Count Submatrices With Target Sum](/problems/count-submatrices-with-target-sum)
