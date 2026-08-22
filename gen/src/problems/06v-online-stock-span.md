# Monotonic Stack — Online Stock Span

*[↗ LeetCode: Online Stock Span](https://leetcode.com/problems/online-stock-span/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/monotonic-stack)

Implement `next(price)` returning the number of consecutive days (ending today) with price ≤ today's.

**Example** — `next(100)=1, next(80)=1, next(60)=1, next(70)=2, next(60)=1, next(75)=4, next(85)=6`

---

## Approach 1 — Store all past prices, scan back

O(n) per call, TLE for many calls.

## Approach 2 — Monotonic decreasing stack of `(price, span)` pairs

**Insight.** When a new price arrives, pop every stacked entry with `≤ new price`, accumulating their spans into today's span. Push `(price, todaySpan)`.

**Streaming twin** of Daily Temperatures — same stack pattern, online.

```java
class StockSpanner {
    Deque<int[]> stack = new ArrayDeque<>();
    public int next(int price) {
        int span = 1;
        while (!stack.isEmpty() && stack.peek()[0] <= price)
            span += stack.pop()[1];
        stack.push(new int[]{price, span});
        return span;
    }
}
```

<CodeTrace
  title="Online span — prices 100,80,60,70,60,75,85"
  :values="[100,80,60,70,60,75,85]"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { stack: "[(100,1)]", ret: 1 }, note: "push (100,1)" },
    { pointers: { i: 1 }, vars: { stack: "[(100,1),(80,1)]", ret: 1 }, note: "80 lt 100 → span 1" },
    { pointers: { i: 3 }, vars: { stack: "[(100,1),(80,1),(70,2)]", ret: 2 }, note: "70 pops 60 → span = 1+1 = 2", added: [3] },
    { pointers: { i: 5 }, vars: { stack: "[(100,1),(80,1),(75,4)]", ret: 4 }, note: "75 pops 60,70,60 → span = 1+2+1 = 4", added: [5] },
    { pointers: { i: 6 }, vars: { stack: "[(100,1),(85,6)]", ret: 6 }, note: "85 pops 75,80 → span = 1+4+1 = 6", added: [6] }
  ]'
/>

**Complexity** — Time **O(1) amortized** per call; Space **O(n)** worst-case stack.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Store all + scan back | O(n) per call | O(n) |
| Monotonic stack with spans | **O(1) amortized** | O(n) |

## Related problems

- [Daily Temperatures](/problems/monotonic-stack-daily-temperatures) — offline sibling
- [Next Greater Element II](/problems/next-greater-element-ii) — circular
- [Sum of Subarray Minimums](/problems/sum-of-subarray-minimums) — contribution via monotonic stack
