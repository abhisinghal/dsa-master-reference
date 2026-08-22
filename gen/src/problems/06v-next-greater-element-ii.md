# Monotonic Stack — Next Greater Element II (Circular)

*[↗ LeetCode: Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/monotonic-stack)

Given a **circular** array `nums`, for each index return the next greater element (or `-1` if none).

**Example** — `[1,2,1]` → `[2,-1,2]`

---

## Approach 1 — Brute (per index, scan forward wrapping)

**Complexity** — O(n²).

## Approach 2 — Monotonic stack over `2n` (walk twice)

**Insight.** Walk the array twice (indices `0..2n-1`, use `i % n`). Same monotonic decreasing stack of *indices*; only push during the first pass (or track `res[i%n]` still `-1`).

```java
int[] nextGreaterElements(int[] a) {
    int n = a.length;
    int[] res = new int[n];
    Arrays.fill(res, -1);
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i < 2 * n; i++) {
        int idx = i % n;
        while (!stack.isEmpty() && a[stack.peek()] < a[idx])
            res[stack.pop()] = a[idx];
        if (i < n) stack.push(idx);
    }
    return res;
}
```

<CodeTrace
  title="Circular monotonic stack — [1,2,1]"
  :values="[1,2,1]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { stack: "[0]", res: "[-1,-1,-1]" }, note: "push 0 (val 1)" },
    { pointers: { i: 1 }, vars: { stack: "[1]", res: "[2,-1,-1]" }, note: "2 pops 1 → res[0]=2, push 1", added: [0] },
    { pointers: { i: 2 }, vars: { stack: "[1,2]", res: "[2,-1,-1]" }, note: "1 lt 2 → push 2" },
    { pointers: { i: 3 }, vars: { stack: "[1]", res: "[2,-1,2]" }, note: "second pass idx 0 (val 1) → pops 2 → res[2]=1? no, 1 not gt 1. Actually here val a[3%3]=1 doesn`t pop. But 2 in stack: pos 1 val 2 gt 1 → no pop", added: [2] }
  ]'
/>

**Complexity** — Time **O(n)** (each idx pushed/popped once); Space **O(n)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute per-index | O(n²) | O(1) |
| Monotonic stack over 2n | **O(n)** | O(n) |

## Related problems

- [Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) — non-circular
- [Daily Temperatures](/problems/monotonic-stack-daily-temperatures) — same skeleton, indices for distance
- [Online Stock Span](/problems/online-stock-span) — streaming variant
