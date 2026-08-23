# Monotonic Stack — Online Stock Span

*[↗ LeetCode: Online Stock Span](https://leetcode.com/problems/online-stock-span/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/monotonic-stack)

&lt;CompanyTags companies="Amazon, Google" /&gt;

Design `StockSpanner`. Method `next(price)` returns the span of the current day — the max number of consecutive days (going back and including today) where the price was **less than or equal to** today's.

**Example 1** —


```
StockSpanner S = new StockSpanner();
S.next(100);   // 1
S.next(80);    // 1
S.next(60);    // 1
S.next(70);    // 2 (70 > 60)
S.next(60);    // 1
S.next(75);    // 4 (75 > 60,70,60)
S.next(85);    // 6
```



**Constraints** — `1 ≤ price ≤ 10⁵`; up to `10⁴` calls.


&lt;Hints
  hint1="What element does each `i` ’see’ looking left or right? Nearest greater? Nearest smaller?"
  hint2="Maintain a stack that’s monotonic in one direction. When the new element breaks monotonicity, pop and answer for popped items."
  hint3="Contribution counting: instead of ’for each subarray find X’, ask ’for each element, how many subarrays does it contribute to?’"
/&gt;
---

&lt;MarkSolved problem-slug="online-stock-span" /&gt;


## Approach 1 — Store all prices, scan on each `next`

**Intuition.** Keep list of all prices; on each call, walk backward counting.

**Complexity** — Time **O(n)** per `next`, **O(n²)** worst total; Space **O(n)**.

---

## Approach 2 — Monotonic decreasing stack (canonical)

**Insight from brute.** Each incoming price collapses a run of smaller-or-equal older prices — those older prices can never contribute to a future span (this bigger price sits between them and the future). Store `(price, span)` pairs on a stack; on `next(p)`, pop everything ≤ p, sum spans, push `(p, totalSpan)`.

**Why amortized O(1).** Each price is pushed once and popped at most once — total work is O(N) across N calls.



```java
class StockSpanner {
    Deque<int[]> stack = new ArrayDeque<>();
    public int next(int price) {
        int span = 1;
        while (!stack.isEmpty() && stack.peek()[0] <= price) span += stack.pop()[1];
        stack.push(new int[]{price, span});
        return span;
    }
}
```



<CodeTrace
  title="Stack (price,span) — prices=100,80,60,70,60,75,85"
  :values="['100','80','60','70','60','75','85']"
  :windowKeys="['call']"
  :cellWidth="30"
  :steps='[
    { pointers: { call: 2 }, vars: { stack: "[(100,1),(80,1),(60,1)]" }, note: "each so far returns 1" },
    { pointers: { call: 3 }, vars: { stack: "[(100,1),(80,1),(70,2)]" }, note: "70 pops (60,1); span=1+1=2" },
    { pointers: { call: 4 }, vars: { stack: "[(100,1),(80,1),(70,2),(60,1)]" }, note: "60 alone; span=1" },
    { pointers: { call: 5 }, vars: { stack: "[(100,1),(80,1),(75,4)]" }, note: "75 pops (60,1) and (70,2); span=1+1+2=4" },
    { pointers: { call: 6 }, vars: { stack: "[(100,1),(85,6)]" }, note: "85 pops all except 100; span=1+4+1=6" }
  ]'
/>

**Complexity** — Amortized **O(1)** per `next`; Space **O(n)** worst.

---

## Try it yourself

<JavaRunner problem-slug="online-stock-span" />

## Complexity summary

| Approach | Time per next | Space | Interview grade |
|---|---|---|---|
| Store and scan | O(n) | O(n) | baseline |
| Monotonic stack `(price, span)` | **O(1) amortized** | O(n) | canonical |

## When to use which

- **Streaming NGE / span** → monotonic stack with span-accumulation.
- **"Return the actual indices, not span"** → push (price, index); span = current - stack.peek().index.
- **Offline max — no streaming** → non-streaming variant is [Daily Temperatures](/problems/monotonic-stack-daily-temperatures).
- **"Span with equality reversed (strictly less)"** → change the pop condition to `< price`.

&lt;AiCompanion problem-slug="online-stock-span" pattern-hint="monotonic stack" /&gt;

## Related problems

- [Daily Temperatures](/problems/monotonic-stack-daily-temperatures)
- [Next Greater Element II](/problems/next-greater-element-ii) — circular sibling
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) — deque-based sibling

&lt;FeedbackWidget problem-slug="online-stock-span" /&gt;

&lt;RelatedProblems problems="remove-k-digits::Remove K Digits|sum-of-subarray-minimums::Sum Of Subarray Minimums|next-greater-element-ii::Next Greater Element II" /&gt;
