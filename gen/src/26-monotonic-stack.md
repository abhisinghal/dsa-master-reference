# Monotonic Stack

The star technique of this family is the **monotonic stack**: a stack you deliberately keep in sorted order, so that every time you pop something you've just answered a *"nearest bigger/smaller element"* question for it — turning an O(n²) scan into a single O(n) pass.

> [key] **Key Insight** — Whenever a problem asks for the *nearest* element that is greater/smaller (to the left or right), or for spans/rectangles bounded by such elements, a monotonic stack turns an O(n²) scan into O(n): each index is pushed and popped exactly once.

```text
Monotonic decreasing stack (indices), array = 3 1 4 1 5
push 3 | 1<3 push -> [3,1] | 4 pops 1,3 (they found next-greater=4) -> [4] ...
each pop's "next greater" is the current bar
```

```svg
<svg width="720" height="240" viewBox="0 0 720 240" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <defs>
    <marker id="ms-ar-blue" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#2563eb"/></marker>
    <marker id="ms-ar-red" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#dc2626"/></marker>
    <marker id="ms-ar-grn" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#16a34a"/></marker>
    <filter id="ms-s1" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.5"/></filter>
  </defs>
  <rect x="0" y="0" width="720" height="240" fill="#fbfcfe"/>
  <rect x="16" y="32" width="318" height="166" rx="9" fill="#f8fafc" stroke="#d9dee7"/>
  <text x="175" y="56" text-anchor="middle" font-size="12" font-weight="700" fill="#2563eb">before: decreasing stack of unresolved indices</text>
  <g filter="url(#ms-s1)">
    <rect x="88" y="138" width="70" height="34" rx="7" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
    <rect x="88" y="98" width="70" height="34" rx="7" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5"/>
    <rect x="88" y="58" width="70" height="34" rx="7" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5"/>
    <rect x="238" y="82" width="58" height="44" rx="7" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.7"/>
  </g>
  <g font-size="18" font-weight="700" fill="#0b1220" text-anchor="middle">
    <text x="123" y="161">9</text><text x="123" y="121">7</text><text x="123" y="81">4</text><text x="267" y="109">8</text>
  </g>
  <g font-size="11" fill="#5b6472" text-anchor="middle">
    <text x="123" y="186">bottom</text><text x="123" y="48">top</text><text x="267" y="140">new value</text>
  </g>
  <line x1="236" y1="104" x2="166" y2="76" stroke="#16a34a" stroke-width="2" marker-end="url(#ms-ar-grn)"/>
  <path d="M158,76 C196,42 250,44 287,71" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ms-ar-red)"/>
  <path d="M158,116 C206,154 265,150 307,124" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ms-ar-red)"/>
  <text x="232" y="34" text-anchor="middle" font-size="11" font-weight="700" fill="#dc2626">4 and 7 pop: they found next greater = 8</text>
  <line x1="348" y1="112" x2="390" y2="112" stroke="#2563eb" stroke-width="2.3" marker-end="url(#ms-ar-blue)"/>
  <rect x="406" y="32" width="298" height="166" rx="9" fill="#f8fafc" stroke="#d9dee7"/>
  <text x="555" y="56" text-anchor="middle" font-size="12" font-weight="700" fill="#16a34a">after popping: push the new index</text>
  <g filter="url(#ms-s1)">
    <rect x="452" y="138" width="70" height="34" rx="7" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
    <rect x="452" y="98" width="70" height="34" rx="7" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.7"/>
    <rect x="560" y="92" width="126" height="64" rx="9" fill="#f6f8fb" stroke="#d9dee7"/>
  </g>
  <g font-size="18" font-weight="700" fill="#0b1220" text-anchor="middle">
    <text x="487" y="161">9</text><text x="487" y="121">8</text>
  </g>
  <text x="487" y="84" text-anchor="middle" font-size="11" fill="#5b6472">new top</text>
  <text x="623" y="116" text-anchor="middle" font-size="12" font-weight="700" fill="#0b1220">pop while top &lt; new</text>
  <text x="623" y="136" text-anchor="middle" font-size="12" fill="#334155">answer[j] = i − j</text>
  <text x="360" y="220" text-anchor="middle" font-size="12" font-weight="700" fill="#5b6472">each index is pushed once, popped once → O(n)</text>
</svg>
```
<div class="readfig"><b>How to read it:</b> The stack is kept decreasing from bottom to top. When the new value <b>8</b> arrives, every smaller top value (<b>4</b>, then <b>7</b>) is popped and resolved: <code>answer[j] = i − j</code>. The first larger value (<b>9</b>) stops the popping, then <b>8</b> becomes the new top.</div>

### Recognize by
- *nearest greater / smaller* element (left or right)
- spans, histograms, rectangles bounded by taller / shorter neighbours
- "largest rectangle", "trapping rain water" (stack variant), stock spans, remove-k-digits

### When NOT to use it
You need *farthest* rather than *nearest* — or the comparison isn't a simple ordering. If the "answer per element" depends on *aggregating* over a range instead of picking one boundary, reach for a segment tree or sparse table, not a monotonic stack.

---

## Daily Temperatures (Next Greater Element)
*[↗ LeetCode: Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)*

### Problem
For each day, report **how many days you must wait for a warmer temperature** (0 if it never gets warmer).

**Constraints:** `1 ≤ n ≤ 10⁵`; temperatures in `30–100`.

**Example:** `[73,74,75,71,69,72,76,73]` → `[1,1,4,2,1,1,0,0]`.

### Pattern
Monotonic decreasing stack of indices; resolve "days until warmer".

> [inv] **Invariant** — The stack holds indices whose next-greater element is still unknown, in decreasing temperature order.

### Java
```java
int[] dailyTemperatures(int[] t) {
    int[] res = new int[t.length];
    Deque<Integer> st = new ArrayDeque<>();          // indices, decreasing temps
    for (int i = 0; i < t.length; i++) {
        while (!st.isEmpty() && t[i] > t[st.peek()]) {
            int j = st.pop();
            res[j] = i - j;                          // distance to next warmer
        }
        st.push(i);
    }
    return res;
}
```

> [note] **Trace it** — `[73,74,75,71,69,72,76,73]`. The stack holds indices still waiting for a warmer day; when `76` arrives it pops `72,69,71` and fills their waits → answer `[1,1,4,2,1,1,0,0]`.

Time O(n) · Space O(n).

> [trap] **Common Trap** — Storing values instead of indices. *Example:* `temps=[73,74,75]`. The answer at index 0 is 1 (`i=1` is warmer), which is `1-0`. If the stack held temperatures, you'd have to search back to recover the gap. Push **indices**, subtract on pop.

> [pat] **Pattern Connection** — The template (`while top violates: pop and resolve; push i`) is identical for *Next Greater Element I/II* (circular → iterate `2n`), *Stock Span*, and *Online Stock Span*.

### Same pattern, new tweaks

A monotonic stack that "resolves" each element the moment a bigger/smaller one arrives:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Next Greater Element II (circular)](https://leetcode.com/problems/next-greater-element-ii/) | iterate the array twice (`i % n`) so wrap-around neighbours are considered | — |
| [Online Stock Span](https://leetcode.com/problems/online-stock-span/) | streaming version — push `(price, span)` and collapse spans of smaller prices as they arrive | — |
| [Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/) | each element contributes `min × (countLeft × countRight)`; the monotonic stack gives those boundary counts | — |


## Largest Rectangle in Histogram
*[↗ LeetCode: Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)*

### Problem
Given the bar heights of a histogram (each of width 1), find the area of the **largest rectangle** that fits entirely under the bars.

**Constraints:** `1 ≤ n ≤ 10⁵`; heights `≥ 0`.

**Example:** `[2,1,5,6,2,3]` → `10` (bars `5,6` give height 5 × width 2).

### Pattern
Monotonic increasing stack; when a shorter bar arrives, pop taller bars and compute their maximal rectangle.

> [key] **Key Insight** — A bar's maximal rectangle extends left/right until a strictly shorter bar. The stack gives both boundaries: when bar `i` pops bar `top`, `i` is the right boundary and the new stack top is the left boundary.

> [inv] **Invariant** — Stack heights are non-decreasing; each popped bar's width spans from the element below it (exclusive) to `i` (exclusive).

### Java
```java
int largestRectangleArea(int[] h) {
    Deque<Integer> st = new ArrayDeque<>();   // increasing heights (indices)
    int best = 0, n = h.length;
    for (int i = 0; i <= n; i++) {
        int cur = (i == n) ? 0 : h[i];        // sentinel flushes the stack
        while (!st.isEmpty() && cur < h[st.peek()]) {
            int height = h[st.pop()];
            int left = st.isEmpty() ? -1 : st.peek();
            best = Math.max(best, height * (i - left - 1));
        }
        st.push(i);
    }
    return best;
}
```

> [note] **Trace it** — heights `[2,1,5,6,2,3]`. When `2` follows `6`, pop `6` (area 6) and `5` (area 10); the widest rectangle overall is `5×2 = 10` under bars `[5,6]`.

### Complexity
Time O(n) · Space O(n).

> [trap] **Common Trap** — Forgetting the sentinel `0`. *Example:* `heights=[2,1,5,6,2,3]` — the tallest bar (`6`) never sees a shorter one to its right, so it never gets popped. Append a virtual `0` at the end so every remaining bar is resolved uniformly.

> [pat] **Pattern Connection** — *Maximal Rectangle* (binary matrix) reduces each row to a histogram and applies this in O(RC). *Trapping Rain Water* is the "valley" dual of this "peak" problem.

### Same pattern, new tweaks

"For each bar, how far can it extend until a shorter bar stops it?" scales up:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | build a running histogram of consecutive 1s per column, and run this largest-rectangle routine on each row | — |
| [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | the valley dual — a decreasing stack resolves each trapped basin between a left and right wall | — |
| [Remove K Digits / Largest Rectangle variants](https://leetcode.com/problems/remove-k-digits/) | a monotonic stack that greedily pops to keep the sequence as small/large as possible | — |
