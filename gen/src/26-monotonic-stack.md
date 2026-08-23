# Monotonic Stack


<PatternVideo pattern-name="Monotonic Stack" duration="8–12 min" />

Imagine a brute-force solution for "next warmer day": for each day, scan every day to its right until you find a warmer one. That is simple, but it re-checks the same unresolved days again and again — O(n²) in the worst case.

Can we do better? Yes: keep only the days that are still waiting for an answer. When a warmer day arrives, it resolves all colder days sitting on top of that waiting pile. That pile is the pattern.

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
    <marker id="ms-ar-blue" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/></marker>
    <marker id="ms-ar-red" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-danger)"/></marker>
    <marker id="ms-ar-grn" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-success)"/></marker>
    <filter id="ms-s1" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="var(--dsa-neutral)" flood-opacity="0.5"/></filter>
  </defs>
  <rect x="0" y="0" width="720" height="240" fill="var(--dsa-bg)"/>
  <rect x="16" y="32" width="318" height="166" rx="9" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/>
  <text x="175" y="56" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">before: decreasing stack of unresolved indices</text>
  <g filter="url(#ms-s1)">
    <rect x="88" y="138" width="70" height="34" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary-line)" stroke-width="1.5"/>
    <rect x="88" y="98" width="70" height="34" rx="7" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="1.5"/>
    <rect x="88" y="58" width="70" height="34" rx="7" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="1.5"/>
    <rect x="238" y="82" width="58" height="44" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.7"/>
  </g>
  <g font-size="18" font-weight="700" fill="var(--dsa-ink)" text-anchor="middle">
    <text x="123" y="161">9</text><text x="123" y="121">7</text><text x="123" y="81">4</text><text x="267" y="109">8</text>
  </g>
  <g font-size="11" fill="var(--dsa-neutral)" text-anchor="middle">
    <text x="123" y="186">bottom</text><text x="123" y="48">top</text><text x="267" y="140">new value</text>
  </g>
  <line x1="236" y1="104" x2="166" y2="76" stroke="var(--dsa-success)" stroke-width="2" marker-end="url(#ms-ar-grn)"/>
  <path d="M158,76 C196,42 250,44 287,71" fill="none" stroke="var(--dsa-danger)" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ms-ar-red)"/>
  <path d="M158,116 C206,154 265,150 307,124" fill="none" stroke="var(--dsa-danger)" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ms-ar-red)"/>
  <text x="232" y="34" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-danger)">4 and 7 pop: they found next greater = 8</text>
  <line x1="348" y1="112" x2="390" y2="112" stroke="var(--dsa-primary)" stroke-width="2.3" marker-end="url(#ms-ar-blue)"/>
  <rect x="406" y="32" width="298" height="166" rx="9" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/>
  <text x="555" y="56" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-success)">after popping: push the new index</text>
  <g filter="url(#ms-s1)">
    <rect x="452" y="138" width="70" height="34" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary-line)" stroke-width="1.5"/>
    <rect x="452" y="98" width="70" height="34" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.7"/>
    <rect x="560" y="92" width="126" height="64" rx="9" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/>
  </g>
  <g font-size="18" font-weight="700" fill="var(--dsa-ink)" text-anchor="middle">
    <text x="487" y="161">9</text><text x="487" y="121">8</text>
  </g>
  <text x="487" y="84" text-anchor="middle" font-size="11" fill="var(--dsa-neutral)">new top</text>
  <text x="623" y="116" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">pop while top &lt; new</text>
  <text x="623" y="136" text-anchor="middle" font-size="12" fill="var(--dsa-neutral)">answer[j] = i − j</text>
  <text x="360" y="220" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-neutral)">each index is pushed once, popped once → O(n)</text>
</svg>
```
<div class="readfig"><b>How to read it:</b> The stack is kept decreasing from bottom to top. When the new value <b>8</b> arrives, every smaller top value (<b>4</b>, then <b>7</b>) is popped and resolved: <code>answer[j] = i − j</code>. The first larger value (<b>9</b>) stops the popping, then <b>8</b> becomes the new top.</div>

### Recognize by
- *nearest greater / smaller* element (left or right)
- spans, histograms, rectangles bounded by taller / shorter neighbours
- "largest rectangle", "trapping rain water" (stack variant), stock spans, remove-k-digits


<MonoStackAnim />


### When NOT to use it
You need *farthest* rather than *nearest* — or the comparison isn't a simple ordering. If the "answer per element" depends on *aggregating* over a range instead of picking one boundary, reach for a segment tree or sparse table, not a monotonic stack.

---

## Daily Temperatures (Next Greater Element) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)*

<ProgressCheck id="daily-temperatures-next-greater-element" />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <defs>
    <marker id="ar-dt-success" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-success)"/></marker>
    <marker id="ar-dt-danger" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-danger)"/></marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-primary)">A warmer arrival resolves colder stacked days</text>

  <g text-anchor="middle">
    <rect x="8" y="58" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="52" y="58" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="96" y="58" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="140" y="58" width="44" height="44" rx="7" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="184" y="58" width="44" height="44" rx="7" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="228" y="58" width="44" height="44" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="272" y="58" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="316" y="58" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <g font-size="14" font-weight="700" fill="var(--dsa-ink)">
      <text x="30" y="85">73</text><text x="74" y="85">74</text><text x="118" y="85">75</text><text x="162" y="85">71</text>
      <text x="206" y="85">69</text><text x="250" y="85">72</text><text x="294" y="85">76</text><text x="338" y="85">73</text>
    </g>
    <g font-size="10.5" fill="var(--dsa-neutral)">
      <text x="30" y="117">0</text><text x="74" y="117">1</text><text x="118" y="117">2</text><text x="162" y="117">3</text>
      <text x="206" y="117">4</text><text x="250" y="117">5</text><text x="294" y="117">6</text><text x="338" y="117">7</text>
    </g>
  </g>

  <line x1="250" y1="129" x2="250" y2="105" stroke="var(--dsa-success)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-dt-success)"/>
  <text x="250" y="146" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-success)">i=5, 72</text>

  <rect x="284" y="132" width="84" height="82" rx="10" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
  <text x="326" y="151" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">stack</text>
  <rect x="302" y="160" width="48" height="18" rx="5" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.4"/>
  <text x="326" y="173" text-anchor="middle" font-size="11" fill="var(--dsa-neutral)">2:75</text>
  <rect x="302" y="184" width="48" height="18" rx="5" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.4"/>
  <text x="326" y="197" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-success)">5:72</text>

  <path d="M228 134 C250 165 272 170 300 174" fill="none" stroke="var(--dsa-danger)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-dt-danger)"/>
  <path d="M184 128 C225 206 260 210 300 196" fill="none" stroke="var(--dsa-danger)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-dt-danger)" stroke-dasharray="6 4"/>
  <text x="136" y="164" font-size="12" font-weight="700" fill="var(--dsa-danger)">pop 4,3</text>
  <text x="200" y="231" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">monotone-decreasing stack; larger arrival pops smaller unresolved days</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> The stack stores unresolved days in decreasing temperature order; when <b>72</b> arrives, it pops colder days <b>69</b> and <b>71</b> and records their waits.</div>

### Problem
For each day, report **how many days you must wait for a warmer temperature** (0 if it never gets warmer).

**Constraints:** `1 ≤ n ≤ 10⁵`; temperatures in `30–100`.

**Example 1:** `[73,74,75,71,69,72,76,73]` → `[1,1,4,2,1,1,0,0]`.

<ExamplePreview compact :input="['73', '74', '75', '71', '69', '72', '76', '73']" :output="['1', '1', '4', '2', '1', '1', '0', '0']" />

**Example 2:** `[30,40,50,60]` → `[1,1,1,0]`.

<ExamplePreview compact :input="['30', '40', '50', '60']" :output="['1', '1', '1', '0']" />

### Solution — brute force
For every day `i`, scan days `i+1..n-1` until you find the first warmer temperature. The first warmer day gives the wait length; if none appears, the default answer stays `0`.

```java
int[] dailyTemperaturesBrute(int[] t) {
    int[] res = new int[t.length];
    for (int i = 0; i < t.length; i++) {
        for (int j = i + 1; j < t.length; j++) {
            if (t[j] > t[i]) {
                res[i] = j - i;
                break;
            }
        }
    }
    return res;
}
```

O(n²) time, O(1) extra space beyond the answer — too slow for n ≥ 10⁴.

### Solution — optimized
Monotonic decreasing stack of indices; resolve "days until warmer".

> [inv] **Invariant** — The stack holds indices whose next-greater element is still unknown, in decreasing temperature order.

The optimized version keeps a stack of unresolved indices. When `t[i]` is warmer than the temperature at the top index, day `i` is the next warmer day for that popped index; once all colder waiting days are resolved, push `i` as a new unresolved day.

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

<CodeTrace
  title="Daily Temperatures — T=[73,74,75,71,69,72,76,73]"
  :values="[73,74,75,71,69,72,76,73]"
  :windowKeys="['i']"
  :cellWidth="32"
  :steps='[
    { pointers: { i: 0 }, vars: { stack: "[0]", answer: "[0,0,0,0,0,0,0,0]" }, note: "push 0" },
    { pointers: { i: 1 }, vars: { stack: "[1]", answer: "[1,0,0,0,0,0,0,0]" }, note: "74 pops 73 → ans[0]=1", added: [0] },
    { pointers: { i: 2 }, vars: { stack: "[2]", answer: "[1,1,0,0,0,0,0,0]" }, note: "75 pops 74 → ans[1]=1", added: [1] },
    { pointers: { i: 3 }, vars: { stack: "[2,3]", answer: "[1,1,0,0,0,0,0,0]" }, note: "71 pushes (cooler)" },
    { pointers: { i: 4 }, vars: { stack: "[2,3,4]", answer: "[1,1,0,0,0,0,0,0]" }, note: "69 pushes (cooler)" },
    { pointers: { i: 5 }, vars: { stack: "[2,5]", answer: "[1,1,0,2,1,0,0,0]" }, note: "72 pops 69,71 → ans[4]=1, ans[3]=2", added: [3,4] },
    { pointers: { i: 6 }, vars: { stack: "[6]", answer: "[1,1,4,2,1,1,0,0]" }, note: "76 pops 72,75 → ans[5]=1, ans[2]=4", added: [2,5] },
    { pointers: { i: 7 }, vars: { stack: "[6,7]", answer: "[1,1,4,2,1,1,0,0]" }, note: "73 pushes. leftovers stay 0. done" }
  ]'
/>

### Time Complexity
O(n), because each index is pushed onto the stack once and popped at most once. The nested-looking `while` loop is amortized, not O(n²).

### Space Complexity
O(n), because in a strictly decreasing temperature array, every index can remain unresolved on the stack until the end.

> [trap] **Common Trap** — Storing values instead of indices. *Example:* `temps=[73,74,75]`. The answer at index 0 is 1 (`i=1` is warmer), which is `1-0`. If the stack held temperatures, you'd have to search back to recover the gap. Push **indices**, subtract on pop.

<CodeTrace
  title="Trap — Monotonic stack storing values not indices: temps=[73,74,75]"
  :values="[73,74,75]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { stack: "[73]" }, note: "BUG: push value 73" },
    { pointers: { i: 1 }, vars: { stack: "[74]", ans: "?-?" }, note: "BUG: 74 pops 73, but which index? cannot compute distance" },
    { pointers: { i: 0 }, vars: { stack: "[0]" }, note: "FIX: push index 0 (temps[0]=73)" },
    { pointers: { i: 1 }, vars: { stack: "[1]", ans: "1-0=1" }, note: "FIX: pop idx 0, answer[0] = 1-0 = 1", added: [0] }
  ]'
/>

> [pat] **Pattern Connection** — The template (`while top violates: pop and resolve; push i`) is identical for *Next Greater Element I/II* (circular → iterate `2n`), *Stock Span*, and *Online Stock Span*.

### Learning notes
- Why push **indices** instead of values? — the answer is a distance `i - j`, so you need the old index `j`.
- Why a **decreasing** stack? — any warmer current day can resolve all colder unresolved days above it.
- Why `while` and not `if`? — one hot day may answer many previous colder days.
- Why default `res` values can stay `0`? — Java initializes int arrays to zero, matching "no warmer day".
- Why push after popping? — the current day is unresolved until some future warmer day appears.

### Same pattern, new tweaks

A monotonic stack that "resolves" each element the moment a bigger/smaller one arrives:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Next Greater Element II (circular)](https://leetcode.com/problems/next-greater-element-ii/) | iterate the array twice (`i % n`) so wrap-around neighbours are considered | — |
| [Online Stock Span](https://leetcode.com/problems/online-stock-span/) | streaming version — push `(price, span)` and collapse spans of smaller prices as they arrive | — |
| [Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/) | each element contributes `min × (countLeft × countRight)`; the monotonic stack gives those boundary counts | — |


## Largest Rectangle in Histogram <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)*

<ProgressCheck id="largest-rectangle-in-histogram" />

### Problem
Given the bar heights of a histogram (each of width 1), find the area of the **largest rectangle** that fits entirely under the bars.

**Constraints:** `1 ≤ n ≤ 10⁵`; heights `≥ 0`.

**Example 1:** `[2,1,5,6,2,3]` → `10` (bars `5,6` give height 5 × width 2).

<ExamplePreview compact :input="['2', '1', '5', '6', '2', '3']" :output="['10']" />

**Example 2:** `[2,4]` → `4` (either height 2 × width 2 or height 4 × width 1).

<ExamplePreview compact :input="['2', '4']" :output="['4']" />

### Solution — brute force
Treat every pair `(left, right)` as a candidate rectangle span. The height of that rectangle is the minimum bar inside the span, so update that running minimum while expanding `right`.

```java
int largestRectangleAreaBrute(int[] h) {
    int best = 0;
    for (int left = 0; left < h.length; left++) {
        int minHeight = Integer.MAX_VALUE;
        for (int right = left; right < h.length; right++) {
            minHeight = Math.min(minHeight, h[right]);
            best = Math.max(best, minHeight * (right - left + 1));
        }
    }
    return best;
}
```

O(n²) time, O(1) space — too slow for n ≥ 10⁴.

### Solution — optimized
Monotonic increasing stack; when a shorter bar arrives, pop taller bars and compute their maximal rectangle.

> [key] **Key Insight** — A bar's maximal rectangle extends left/right until a strictly shorter bar. The stack gives both boundaries: when bar `i` pops bar `top`, `i` is the right boundary and the new stack top is the left boundary.

> [inv] **Invariant** — Stack heights are non-decreasing; each popped bar's width spans from the element below it (exclusive) to `i` (exclusive).

The optimized version waits until a bar sees its first strictly shorter bar on the right. At that moment, the popped bar's right boundary is known (`i`), and the new stack top gives the first shorter bar on the left.

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

<CodeTrace
  title="Largest Rectangle in Histogram — heights=[2,1,5,6,2,3]"
  :values="[2,1,5,6,2,3]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { stack: "[0]", best: 0 }, note: "push idx 0 (h=2)" },
    { pointers: { i: 1 }, vars: { stack: "[1]", best: 2 }, note: "1 pops 2 → area 2*1=2, then push", added: [0] },
    { pointers: { i: 2 }, vars: { stack: "[1,2]", best: 2 }, note: "5 pushes" },
    { pointers: { i: 3 }, vars: { stack: "[1,2,3]", best: 2 }, note: "6 pushes" },
    { pointers: { i: 4 }, vars: { stack: "[1,4]", best: 10 }, note: "2 pops 6 (area 6), pops 5 (area 10) — NEW BEST", added: [2,3] },
    { pointers: { i: 5 }, vars: { stack: "[1,4,5]", best: 10 }, note: "3 pushes. flush at end gives no bigger", added: [] }
  ]'
/>

### Time Complexity
O(n), because every bar index is pushed once and popped once. Each rectangle area is computed exactly when its limiting shorter bar is discovered.

### Space Complexity
O(n), because an increasing histogram can push all indices before the sentinel flushes them.

> [trap] **Common Trap** — Forgetting the sentinel `0`. *Example:* `heights=[2,1,5,6,2,3]` — the tallest bar (`6`) never sees a shorter one to its right, so it never gets popped. Append a virtual `0` at the end so every remaining bar is resolved uniformly.

<CodeTrace
  title="Trap — Largest Rectangle missing sentinel: heights=[2,1,5,6,2,3]"
  :values="[2,1,5,6,2,3]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 5 }, vars: { stack: "[1,4,5]", best: 10 }, note: "BUG: end of scan. bars 1,2,3 remain unpopped" },
    { pointers: { i: 5 }, vars: { stack: "[1,4,5]", best: 10 }, note: "BUG: their contributions missed (e.g. rectangle spanning [5]=3 wide-1)" },
    { pointers: { i: 6 }, vars: { sentinel: 0, stack: "[]", best: 10 }, note: "FIX: append virtual 0 → all remaining bars pop, area computed uniformly" }
  ]'
/>

> [pat] **Pattern Connection** — *Maximal Rectangle* (binary matrix) reduces each row to a histogram and applies this in O(RC). *Trapping Rain Water* is the "valley" dual of this "peak" problem.

### Learning notes
- Why an **increasing** stack? — a shorter incoming bar is the signal that taller bars can no longer extend right.
- Why store indices? — width needs positions: `i - left - 1`, not just heights.
- Why `cur = (i == n) ? 0 : h[i]`? — the virtual zero flushes every remaining bar at the end.
- Why `left = st.isEmpty() ? -1 : st.peek()`? — empty stack means the popped bar can extend to index `0`.
- Why width `i - left - 1`? — both boundaries are exclusive: shorter bar at `left`, shorter bar at `i`.
- Why compare `cur < h[st.peek()]`? — equal heights can stay stacked without losing the maximal area.

### Same pattern, new tweaks

"For each bar, how far can it extend until a shorter bar stops it?" scales up:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | build a running histogram of consecutive 1s per column, and run this largest-rectangle routine on each row | — |
| [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | the valley dual — a decreasing stack resolves each trapped basin between a left and right wall | — |
| [Remove K Digits / Largest Rectangle variants](https://leetcode.com/problems/remove-k-digits/) | a monotonic stack that greedily pops to keep the sequence as small/large as possible | — |

---

## Check your understanding

<Quiz
  pattern-id="monotonic-stack"
  :questions='[{"q": "What is the amortized cost per element in a monotonic-stack sweep?", "choices": [{"text": "O(1)", "correct": true, "explanation": "Each element pushed and popped at most once → 2n total operations."}, {"text": "O(log n)", "correct": false}, {"text": "O(n)", "correct": false}, {"text": "O(σ)", "correct": false}]}, {"q": "For \"next greater element\", which stack orientation do you maintain?", "choices": [{"text": "Monotonically decreasing from bottom to top", "correct": true, "explanation": "New larger element pops smaller predecessors — those find their answer."}, {"text": "Monotonically increasing", "correct": false, "explanation": "That is for \"next smaller\"."}, {"text": "Not monotonic", "correct": false}, {"text": "Sorted at insertion", "correct": false}]}, {"q": "Why does Largest Rectangle in Histogram benefit from a \"sentinel\" bar?", "choices": [{"text": "A trailing height-0 flushes any remaining stack cleanly", "correct": true, "explanation": "Otherwise you need special-case code after the loop."}, {"text": "To handle negative heights", "correct": false, "explanation": "Heights are non-negative."}, {"text": "For randomness", "correct": false}, {"text": "To detect end-of-input", "correct": false}]}, {"q": "Sum of Subarray Minimums uses \"contribution counting\". What is the key idea?", "choices": [{"text": "For each element, count how many subarrays it is minimum of (L·R spans)", "correct": true, "explanation": "Turn \"for each subarray find min\" into \"for each element count contributions\"."}, {"text": "Sum over all subarrays", "correct": false, "explanation": "That is O(n²)."}, {"text": "Only iterate subarrays of length ≤ log n", "correct": false}, {"text": "Sort the array first", "correct": false}]}, {"q": "For Online Stock Span, what does the stack store?", "choices": [{"text": "(price, span) pairs", "correct": true, "explanation": "On next price ≥ top, pop and accumulate span."}, {"text": "Only prices", "correct": false, "explanation": "Would lose the span info."}, {"text": "Only spans", "correct": false}, {"text": "All prices ever seen", "correct": false, "explanation": "Would defeat the amortization."}]}]'
/>