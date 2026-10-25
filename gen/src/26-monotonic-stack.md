# Monotonic Stack


<PatternVideo pattern-name="Monotonic Stack" duration="8–12 min" />

<PatternProgress pattern-id="monotonic-stack" problems="monotonic-stack-daily-temperatures, next-greater-element-ii, online-stock-span, remove-k-digits, sum-of-subarray-minimums" />

<script setup>
const theTemplateSpecializations = [
  { slug: `next-greater-right-bare-mechanic-easy`, title: `Next Greater (right) — bare mechanic` },
  { slug: `next-greater-left-easy`, title: `Next Greater (left) — mirror sweep` },
  { slug: `daily-temperatures-next-greater-element-medium`, title: `Daily Temperatures (= NGE-right with index diff)` },
  { slug: `stock-span-nge-left-variant-medium`, title: `Stock Span (NGE-left variant)` },
  { slug: `largest-rectangle-in-histogram-hard`, title: `Largest Rectangle in Histogram` },
  { slug: `remove-k-digits-lexicographic-greedy-medium`, title: `Remove K Digits (lexicographic greedy)` },
  { slug: `_132-pattern-three-element-variant-medium`, title: `132 Pattern (three-element variant)` },
]

const theTemplateCode = `// Next Greater Element to the right — THE template
// Variants: flip < to > for next-smaller; iterate right-to-left for previous-* ;
// walk 2n-1 times with "push only if i<n" for the circular variant.
int[] nextGreater(int[] a) {
    int n = a.length;
    int[] res = new int[n];
    Arrays.fill(res, -1);
    Deque<Integer> stack = new ArrayDeque<>();   // INDICES, values decreasing bottom->top
    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && a[stack.peek()] < a[i]) {
            res[stack.pop()] = i;                 // the pop ANSWERS this index
        }
        stack.push(i);                            // i is now unresolved
    }
    return res;
}`

const nextGreaterLeftCode = `// Previous (next-greater-to-the-left) — mirror sweep: iterate RIGHT->LEFT.
int[] previousGreater(int[] a) {
    int n = a.length;
    int[] res = new int[n];
    Arrays.fill(res, -1);
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = n - 1; i >= 0; i--) {
        while (!stack.isEmpty() && a[stack.peek()] < a[i]) {
            res[stack.pop()] = i;                 // a[i] is their previous greater
        }
        stack.push(i);
    }
    return res;
}`

const stockSpanCode = `// Online Stock Span — streaming NGE-to-the-left variant.
// span[i] = number of consecutive days ending today with price <= today's.
class StockSpanner {
    Deque<int[]> st = new ArrayDeque<>();         // (price, span) pairs

    public int next(int price) {
        int span = 1;
        while (!st.isEmpty() && st.peek()[0] <= price) {
            span += st.pop()[1];                  // absorb earlier spans whose prices this one dominates
        }
        st.push(new int[]{price, span});
        return span;
    }
}`

const removeKDigitsCode = `// Remove K Digits — pop while top is bigger than incoming (keep sequence lex-smallest).
String removeKdigits(String num, int k) {
    Deque<Character> st = new ArrayDeque<>();     // monotonically non-decreasing stack
    for (char c : num.toCharArray()) {
        while (k > 0 && !st.isEmpty() && st.peek() > c) {
            st.pop(); k--;
        }
        st.push(c);
    }
    while (k-- > 0 && !st.isEmpty()) st.pop();    // extra budget → trim tail
    // build result left-to-right from stack bottom, drop leading zeros
    StringBuilder sb = new StringBuilder();
    for (Character c : st) sb.append(c);
    sb.reverse();
    int i = 0;
    while (i < sb.length() - 1 && sb.charAt(i) == '0') i++;
    return sb.substring(i);
}`

const pattern132Code = `// 132 pattern — scan right-to-left, maintain stack of candidate "3" values,
// and track the MAX popped value which will serve as the "2".
boolean find132pattern(int[] a) {
    Deque<Integer> stack = new ArrayDeque<>();    // candidate 3-values, decreasing bottom->top
    int two = Integer.MIN_VALUE;                  // best "2" so far (largest popped)
    for (int i = a.length - 1; i >= 0; i--) {
        if (a[i] < two) return true;              // a[i] is the "1" we needed
        while (!stack.isEmpty() && stack.peek() < a[i]) {
            two = Math.max(two, stack.pop());     // this popped value becomes a candidate "2"
        }
        stack.push(a[i]);
    }
    return false;
}`

const amortizedExplanation = `Each index is pushed at most once and popped at most once across the entire sweep.
The <strong>outer for-loop</strong> runs n times, so total pushes ≤ n. The <strong>inner
while-loop</strong> only runs when it pops, and the total number of pops across the full
run is bounded by total pushes ≤ n. Total work: at most 2n stack operations. Even though
a single iteration of the outer loop can perform many pops, the pops are redistributed —
"borrowed" from past iterations that paid the push cost. Aggregate argument: 2n stack ops
over n outer iterations → <strong>O(1) amortized per element</strong>, <strong>O(n) total</strong>.`

const mastery5 = [
  {
    q: `What's the AMORTIZED cost per element in a monotonic-stack sweep?`,
    choices: [
      { text: `O(1)`, correct: true, explanation: `Each element pushed and popped at most once → 2n total ops across n outer iterations.` },
      { text: `O(log n)`, correct: false },
      { text: `O(n) — because of the inner while-loop`, correct: false, explanation: `Classic trap. The inner while is bounded globally, not per iteration.` },
      { text: `O(sqrt n)`, correct: false },
    ],
  },
  {
    q: `For "next GREATER" element to the right, which stack orientation do you maintain?`,
    choices: [
      { text: `Monotonically DECREASING from bottom to top`, correct: true, explanation: `A larger incoming element pops smaller unresolved predecessors — those just found their answer.` },
      { text: `Monotonically increasing`, correct: false, explanation: `That's for "next smaller".` },
      { text: `Not monotonic`, correct: false },
      { text: `Sorted at insertion`, correct: false },
    ],
  },
  {
    q: `Why does Largest Rectangle in Histogram need a trailing SENTINEL bar of height 0?`,
    choices: [
      { text: `To flush bars still on the stack whose right boundary never materialized`, correct: true, explanation: `Without it, the tallest bars never see a strictly shorter bar on their right.` },
      { text: `To handle negative heights`, correct: false, explanation: `Heights are non-negative.` },
      { text: `To detect end-of-input`, correct: false },
      { text: `For better cache behaviour`, correct: false },
    ],
  },
  {
    q: `Sum of Subarray Minimums uses "contribution counting". What's the key reformulation?`,
    choices: [
      { text: `For each element, count how many subarrays it is the min of (L × R span-counts)`, correct: true, explanation: `Turns "for each subarray find min" (O(n²)) into "for each element count contributions" (O(n)).` },
      { text: `Just sort the array first`, correct: false },
      { text: `Only iterate subarrays of length ≤ log n`, correct: false },
      { text: `Precompute suffix sums and binary-search`, correct: false },
    ],
  },
  {
    q: `For Remove K Digits, the stack is monotonically NON-DECREASING. What does popping a larger top accomplish?`,
    choices: [
      { text: `Removes a digit at a position where a smaller digit is about to appear — producing a lex-smaller number`, correct: true, explanation: `Keeping the smaller digit earlier dominates the lex order; the budget k is the number of pops you're allowed.` },
      { text: `Normalizes the number to base 10`, correct: false },
      { text: `Only prevents overflow`, correct: false },
      { text: `Is a bug — the stack should be strictly increasing`, correct: false, explanation: `Non-decreasing is correct — equal digits may stack.` },
    ],
  },
]
</script>

## Why monotonic stack exists — the story

You're building a weather app. Users want to know: *"For each day, how many days until the next warmer day?"* The array is 365 daily temperatures. For January 1st, when was the first day that got warmer than January 1st?

The honest brute force: for each day `i`, scan forward from `i+1` looking for a warmer day. Return that gap. Simple, correct.

For 365 days that's about 66,000 comparisons — fast enough that nobody notices. For a decade of hourly temperature data (`n = 87,600`), you're at `4 × 10⁹` comparisons — **20 seconds** on a modern CPU. Users close the app. And the wasted work is embarrassing: you keep re-scanning the same cold January stretches, once for each earlier day that hasn't been resolved yet.

The insight is this: when a warmer day finally arrives, it **resolves every colder day that's still waiting.** They should be "answered" and forgotten. If we maintain a stack of *"days still waiting for an answer, in decreasing temperature order,"* each new day pops off every day it's warmer than — each pop answers exactly one query. Each day is pushed once and popped at most once. **Total: O(n).** For the decade of hourly data: 20 seconds → **1 millisecond.** A 20,000-times speedup because we track only what's unresolved.

This is the **monotonic stack**: a stack you deliberately keep in sorted (monotonic) order, so that every time you *pop* something, you've just answered a "nearest bigger/smaller element" question about it. It's one of the most under-appreciated interview techniques — half of the "Hard" LeetCode array problems collapse to monotonic stack once you spot the pattern.

## The core idea — the stack holds unresolved elements only

<MonoStackAnim />

Every problem in this family has the same three-part shape:

1. **What do we push?** The current element (or its index). Almost always the index — you'll need it for distance / range queries.
2. **What triggers a pop?** A monotonicity violation. If the stack must stay decreasing and the incoming element is larger, pop until it's decreasing again.
3. **What does each pop compute?** The answer for the popped element — its "next greater," or "next smaller," or "span," or "area."

The stack at any moment holds the **unresolved suffix** of what we've seen. A "resolved" element is one whose answer we've already recorded and forgotten. Every element enters the stack exactly once, leaves exactly once — total work is O(n) amortized, even though the inner `while` loop can pop many elements at a step.

> [key] **Key Insight** — Whenever a problem asks for the *nearest* element that is greater/smaller (to the left or right), or for spans/rectangles bounded by such elements, a monotonic stack turns an O(n²) scan into O(n): each index is pushed and popped exactly once.

## When to use it — recognition signals

Reach for a monotonic stack when the problem says:

- **"Next greater element"** / "next smaller element" / "previous greater" / "previous smaller" — any variant of the four directions. Daily Temperatures, Next Greater Element I / II / III.
- **"Largest rectangle" / "maximal rectangle in a histogram"** — the O(n) solution uses a monotonic increasing stack to find, for each bar, the widest strip it can dominate.
- **"Trapping rain water"** — one clean formulation counts water on top of each popped bar.
- **"Span" problems** — Online Stock Span, "how many consecutive days does today's price beat?"
- **"Sum of subarray minimums / maximums"** — sum over all subarrays of the min or max, in O(n) via contribution counting with a monotonic stack.
- **"Remove k digits to form the smallest number"** — greedy pop of increasing prefix to lock in a smaller lexicographic value.
- **"Lexicographically smallest / largest sequence" after some operation** — often a monotonic stack greedy.
- **Circular variants** — walk the array twice, size the stack for `2n - 1` iterations.

If the problem asks about *the nearest X-satisfying element* or *a range bounded by extremes*, the answer is almost certainly a monotonic stack.

## When NOT to use it

- **You need the k-th greater / k-th smaller** — the stack only remembers unresolved elements, not history. Use a heap or a sorted structure.
- **The array is sorted** — monotonic stack shines on *unsorted* input where you need to discover local extremes. On sorted input, plain scanning is cheaper.
- **You need updates in the middle of the array** — the stack processes left-to-right in one pass. If elements change mid-processing, you need a segment tree instead.
- **The "monotonic" comparison is on multiple fields** — a stack is one-dimensional. For "nearest element that is both taller and heavier," a 2D structure is needed.
- **Range aggregate queries with unrestricted ranges** — sparse table, segment tree, or Fenwick tree.
- **Very small n (n ≤ 100)** — brute force is simpler and equally fast in practice. Save monotonic stack for `n ≥ 1000`.

## THE template

Every monotonic-stack problem is a specialization of **"maintain a sorted stack of unresolved indices; a violation triggers a pop, and each pop resolves exactly one element."** Four parameters distinguish the family: push order (push value vs. push index), direction (left-to-right vs. right-to-left), comparison (`<` strict vs. `≤` lax), and what each pop computes.

<PatternTemplateCard
  slug="monotonic-stack-nge-right"
  title="Next Greater Element (right) — THE monotonic-stack template"
  language="java"
  :code="theTemplateCode"
  :invariant="{
    statement: 'The stack holds indices in strictly decreasing order of a[]. Every index still on the stack has no next-greater element found yet; every index popped has res[i] set.',
    initialization: 'Before iteration 0: stack is empty (trivially decreasing); res[] = -1 everywhere.',
    maintenance: 'For iteration i: pop every top whose a[top] < a[i], setting res[top] = i (correct: a[i] is to their right and greater). The remaining stack is still decreasing because the popped tops were violating. Pushing i preserves the decreasing invariant because i was popped-until the top ≥ a[i].',
    termination: 'After iteration n-1: every index not popped has no element to its right greater than it; res[i] remains -1, as required.',
  }"
  :complexity="{ time: 'O(n) amortized — 2n stack ops over n iterations', space: 'O(n) for the stack in a strictly decreasing input' }"
  :specializations="theTemplateSpecializations"
>
  <template #amortized>
<AmortizedPanel
  method="aggregate"
  bound="O(n) total across the entire sweep"
  statement="Each index is pushed at most once and popped at most once, so total stack operations are at most 2n."
  :workedExample="amortizedExplanation"
/>
  </template>
</PatternTemplateCard>

The three canonical "flavors" are: **next-greater-right** (above — the base case), **next-greater-left** (iterate right-to-left, same logic), and **largest-rectangle in histogram** (increasing stack, each pop computes `height × width`, requires a trailing sentinel 0).

## False friends — not every stack-based sweep is monotonic

- **Parentheses matching** uses a plain stack — no monotonic ordering. The invariant is "stack contents are the unmatched openers in LIFO order," not any value comparison. Don't call it monotonic.
- **DFS-with-stack / iterative tree traversal** — the stack holds *frames*, not *values to compare*. The pop condition is "frame has no more children," not "incoming value violates ordering."
- **Shunting-yard operator precedence** — the stack IS monotonic in precedence, so this is a monotonic stack. (This is where Nagao-Matsuyama originally found the pattern.)
- **Expression trees / RPN** — plain stack of operands; no ordering.
- **Sliding-window maximum** uses a monotonic *deque*, not stack — the max can be popped from either end. The flavor is similar but it's not quite the same tool.

## History — Nagao-Matsuyama, 1971

The monotonic stack technique was first formalized by **Makoto Nagao and Takahiko Matsuyama** in a 1971 paper on **expression parsing** — specifically the shunting-yard algorithm's operator-precedence stack, where the stack is kept in decreasing order of precedence. The pattern generalized to array problems through the "largest rectangle in a histogram" algorithm (used in compiler dead-code elimination) and became an interview staple in the early 2000s.

The pattern also underlies **online query structures** in competitive programming — the "Cartesian tree" data structure, which represents an array as a heap-ordered binary tree, can be built in O(n) using exactly this stack technique. Interviewers who ask about "amortized analysis on a stack-based algorithm" are almost always testing whether you understand *this* pattern.

## Sub-variations of the template

<PatternSubVariationNav pattern="monotonic-stack" />

The sub-variations below walk the template through its canonical seven forms — bare mechanic, mirror sweep, index-diff variant, streaming span, histogram rectangle, lexicographic greedy, and the three-element 132-pattern. Each builds on the previous; by the end, they all read as "same template, different pop semantics."

### Next Greater (right) — bare mechanic <span class="diff diff-e">Easy</span>

The simplest instance of the pattern. Given `nums[]`, return `res[]` where `res[i]` is the next index `j > i` with `nums[j] > nums[i]`, or `-1` if none.

> [inv] **Invariant** — The stack holds indices in strictly decreasing order of `nums[]`; every index still on the stack has no next-greater element found yet.

<InvariantProof
  statement="At the end of iteration i, (a) the stack is strictly decreasing in nums[], and (b) res[j] = i for every j popped during iteration i, where i is the smallest index > j with nums[i] > nums[j]."
  initialization="Before iteration 0: empty stack (trivially decreasing); res[] = -1."
  maintenance="During iteration i, pop every top whose nums[top] < nums[i], setting res[top] = i. Correctness: top was unresolved (no next-greater yet) with every subsequent index k in (top, i) having nums[k] ≤ nums[top] (else top would have been popped earlier). So i is the smallest index > top with nums[i] > nums[top]. The remaining stack stays decreasing; pushing i preserves it because we popped until the top ≥ nums[i]."
  termination="Every index not popped by the end has no element to its right with a larger value — res[i] = -1, correct."
/>

> [key] **Blind-solve prompt** — *Before revealing the template, try to solve it:* given `nums[]`, return the array where each entry is the next-greater element to the right, or `-1`. Make it O(n).

<TemplateReveal
  slug="monotonic-stack-nge-right"
  language="java"
  :canonical="theTemplateCode"
/>

**Trace** on `nums=[2, 1, 2, 4, 3]`:

| i | nums[i] | stack (indices) | pops | res after |
|---|---|---|---|---|
| 0 | 2 | [0] | — | `[-1, -1, -1, -1, -1]` |
| 1 | 1 | [0, 1] | — | `[-1, -1, -1, -1, -1]` |
| 2 | 2 | [0, 2] | pop 1 (res[1]=2) | `[-1, 2, -1, -1, -1]` |
| 3 | 4 | [3] | pop 2 (res[2]=3), pop 0 (res[0]=3) | `[3, 2, 3, -1, -1]` |
| 4 | 3 | [3, 4] | — | `[3, 2, 3, -1, -1]` |

Final: `[3, 2, 3, -1, -1]` ✓

### Next Greater (left) — mirror sweep <span class="diff diff-e">Easy</span>

Same template, iterated **right-to-left**. The pop condition remains "stack top's value < nums[i]" — the only change is the loop direction. Every answer is now the first index to the *left* with a larger value.

> [inv] **Invariant** — At iteration `i` (sweeping right-to-left), the stack holds indices in strictly decreasing order of `nums[]`; each popped index `top` is resolved with `res[top] = i` (its first-greater-to-the-left).

<TemplateReveal
  slug="previous-greater"
  language="java"
  :canonical="nextGreaterLeftCode"
/>

**Compare:** NGE-right finds `res[i] = j` where `j > i` and `nums[j] > nums[i]` is the *first* such `j`. NGE-left finds `res[i] = j` where `j < i` and `nums[j] > nums[i]` is the *first* such `j`. Choice of pass direction is the entire difference.

<details>
<summary><strong>Pedagogical: the 3-approach ladder for Daily Temperatures (brute → stack → reverse stack)</strong></summary>

**Problem** ([↗ LeetCode](https://leetcode.com/problems/daily-temperatures/)): Given an array `temperatures` representing daily temperatures, return an array `answer` such that `answer[i]` is the *number of days* you have to wait after day `i` to get a warmer temperature. If there is no future warmer day, `answer[i] = 0`.

#### Approach 1 — Brute force

For each day, scan forward until warmer.

```java
int[] dailyTemperaturesBrute(int[] t) {
    int n = t.length;
    int[] res = new int[n];
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (t[j] > t[i]) { res[i] = j - i; break; }
        }
    }
    return res;
}
```

**Complexity:** O(n²) time, O(1) space (excluding output). For `n = 10⁵`, that's 10¹⁰ ops — TLE.

### Approach 2 — Monotonic decreasing stack (the interview answer)

Walk left to right. Maintain a stack of unresolved days (whose warmer day hasn't been found yet), in decreasing order of temperature. Each new day pops off every earlier day it's warmer than — those days now know their answer.

```java
int[] dailyTemperatures(int[] t) {
    int n = t.length;
    int[] res = new int[n];
    Deque<Integer> stack = new ArrayDeque<>();      // decreasing t[i] from bottom to top
    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && t[stack.peek()] < t[i]) {
            int j = stack.pop();
            res[j] = i - j;                          // days waited
        }
        stack.push(i);
    }
    // Any indices remaining on the stack have res[j] = 0 (already zero-init'd)
    return res;
}
```

**Complexity:** O(n) time (amortized), O(n) space (stack + output).

**Interview commentary:**
- *"For each day, brute force is O(n²). I can do O(n) by tracking only the unresolved days."*
- *"Maintain a stack of indices in decreasing temperature. When a new warmer day arrives, it resolves every unresolved day it's warmer than."*
- *"Each index is pushed and popped at most once, so amortized O(n)."*
- *"Days remaining on the stack at the end have no future warmer day — their answer stays 0."*

### Approach 3 — Reverse iteration variant (equivalent)

Walk right to left. For each day, pop off cooler days at the top of the stack (they can never be the next-warmer-day for anything to their left). The stack top after popping is the answer.

```java
int[] dailyTemperaturesReverse(int[] t) {
    int n = t.length;
    int[] res = new int[n];
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = n - 1; i >= 0; i--) {
        while (!stack.isEmpty() && t[stack.peek()] <= t[i]) stack.pop();
        res[i] = stack.isEmpty() ? 0 : stack.peek() - i;
        stack.push(i);
    }
    return res;
}
```

Same O(n) complexity. Pick whichever direction is more intuitive — both work.

#### Complexity ladder

| Approach | Time | Space | When |
|---|---|---|---|
| Brute force | O(n²) | O(1) | Reference / n ≤ 500 |
| **Forward monotonic stack** | **O(n)** | **O(n)** | **Interview default** |
| Reverse monotonic stack | O(n) | O(n) | Equivalent; use if it reads cleaner |

</details>

---



```text
Monotonic decreasing stack (indices), array = 3 1 4 1 5
push 3 | 1<3 push -> [3,1] | 4 pops 1,3 (they found next-greater=4) -> [4] ...
each pop's "next greater" is the current bar
```

```svg
<svg role="img" width="720" height="240" viewBox="0 0 720 240" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif" aria-label="Diagram illustrating: Complexity ladder">
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

### Daily Temperatures (= NGE-right with index diff) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)*

<ProgressCheck id="daily-temperatures-next-greater-element" />

```svg
<svg role="img" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Diagram illustrating: Daily Temperatures (Next Greater Element) Medium">
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
    <g font-size="11" fill="var(--dsa-neutral)">
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


### Largest Rectangle in Histogram <span class="diff diff-h">Hard</span>

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

### Stock Span (NGE-left variant) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Online Stock Span](https://leetcode.com/problems/online-stock-span/)*

A **streaming** version of NGE-left. Each `next(price)` returns how many consecutive previous days (including today) had a price ≤ today's. The twist: we don't want to recompute spans from scratch; past spans can be **absorbed** when a bigger price dominates them.

> [inv] **Invariant** — The stack holds `(price, span)` pairs in strictly decreasing price order; a popped pair's span is already included in the current `span` accumulator.

<TemplateReveal
  slug="stock-span"
  language="java"
  :canonical="stockSpanCode"
/>

**Trace** `next(100), next(80), next(60), next(70), next(60), next(75), next(85)`:

| call | pops absorbed | span | stack after |
|---|---|---|---|
| 100 | — | 1 | `[(100,1)]` |
| 80 | — | 1 | `[(100,1), (80,1)]` |
| 60 | — | 1 | `[(100,1), (80,1), (60,1)]` |
| 70 | (60,1) | 2 | `[(100,1), (80,1), (70,2)]` |
| 60 | — | 1 | `[(100,1), (80,1), (70,2), (60,1)]` |
| 75 | (60,1), (70,2) | 4 | `[(100,1), (80,1), (75,4)]` |
| 85 | (75,4), (80,1) | 6 | `[(100,1), (85,6)]` |

Each span absorption is **amortized**: a pair's span can only be absorbed once in its lifetime, so total absorptions over any sequence of N calls is ≤ N. **Amortized O(1) per call.**

### Remove K Digits (lexicographic greedy) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Remove K Digits](https://leetcode.com/problems/remove-k-digits/)*

Given a non-negative integer as a string `num` and an integer `k`, remove exactly `k` digits to produce the **lexicographically smallest** remaining number. The monotonic stack lets us greedily enforce the invariant "whenever we're about to append a digit, pop any larger digits from the right end of the current result (budget permitting)."

> [key] **Blind-solve prompt** — *Before revealing:* why does popping a bigger `top` when a smaller `incoming` arrives always produce a lex-smaller result? Walk through `num = "1432219", k = 3` on paper.

> [inv] **Invariant** — The stack is monotonically non-decreasing; it holds the smallest-prefix-of-result-so-far using at most (processed - popped) digits.

<TemplateReveal
  slug="remove-k-digits"
  language="java"
  :canonical="removeKDigitsCode"
/>

**Trace** `num = "1432219", k = 3`:

| i | c | pops | stack after |
|---|---|---|---|
| 0 | '1' | — | `[1]` |
| 1 | '4' | — | `[1, 4]` |
| 2 | '3' | pop '4' (k=2) | `[1, 3]` |
| 3 | '2' | pop '3' (k=1) | `[1, 2]` |
| 4 | '2' | — | `[1, 2, 2]` |
| 5 | '1' | pop '2' (k=0) | `[1, 2, 1]`  |
| 6 | '9' | — | `[1, 2, 1, 9]` |

k=0 after i=5, so we stop popping. Reading bottom-to-top: `"1219"`. ✓

### 132 Pattern (three-element variant) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: 132 Pattern](https://leetcode.com/problems/132-pattern/)*

Return `true` iff there exist indices `i < j < k` with `a[i] < a[k] < a[j]`. The clever reformulation: scan **right-to-left**, maintain a stack of candidates for the "3" position, and track the **largest value we've popped so far** as the "2" candidate. On the left, we just need any element < that "2".

> [inv] **Invariant** — While scanning right-to-left, the stack holds decreasing values (candidate "3"s), and `two` is the maximum of all values that have ever been popped — the best candidate "2" compatible with some "3" to its right.

<TemplateReveal
  slug="pattern-132"
  language="java"
  :canonical="pattern132Code"
/>

**Why this works:** when `a[idx]` is popped, we know `a[idx] < a[curr]` where `curr` is some later element on the stack. That makes `(curr, a[idx])` a valid (3, 2) pair. Keeping `two` as the max popped value gives the loosest constraint on "1". If we later find any `a[i] < two`, we have `(a[i], two, something_in_stack)` — a valid 132.

**Trace** on `nums = [3, 1, 4, 2]`:

| i | a[i] | before pops | after pops | two | push |
|---|---|---|---|---|---|
| 3 | 2 | stack=[] | — | -∞ | stack=[2] |
| 2 | 4 | stack=[2] | pop 2 (two=2) | 2 | stack=[4] |
| 1 | 1 | stack=[4] | a[i]=1 < two=2 → **return true** | — | — |

✓ The 132 pattern is `(1, 4, 2)` at indices `(1, 2, 3)`.

## Traps & gotchas

<TrapTrace
  title="Trap 1 — Storing values instead of indices"
  bug="t = [73, 74, 75]. Stack holds VALUES, not indices. When 74 arrives, pop 73 — but which index was that? Can't compute days-waited."
  fix="Push INDICES. Compute distance on pop: res[j] = i - j. Look up values on demand via a[stack.peek()]."
/>

<TrapTrace
  title="Trap 2 — Wrong strict/non-strict comparison on ties"
  bug='nums = [2, 2, 2, 3] with pop condition "a[top] ≤ a[i]" (non-strict). The second and third 2s pop the first 2 unnecessarily — their "next greater" should still be 3, but you redirect them to each other first. Equal-value inputs silently misbehave.'
  fix='Use strict "<" for "next STRICTLY greater" and "≤" only when the problem says "next greater OR EQUAL". Test every monotonic-stack solution on an all-equal input before claiming correctness.'
/>

<TrapTrace
  title="Trap 3 — Forgetting the sentinel in histogram problems"
  bug="heights = [2, 1, 5, 6, 2, 3]. The main loop ends with bars 1, 4, 5 still on the stack. Their rectangles (bars 4 and 5 could each extend some width) are never computed. Answer under-reports."
  fix="Iterate i from 0 to n INCLUSIVE and use cur = (i == n ? 0 : h[i]). The virtual height-0 at index n flushes every remaining bar. Alternative: post-loop while-pop with right-boundary = n."
/>

## In the wild — LLVM's constant-propagation worklist & `java.util.ArrayDeque`

**LLVM's `SCCP` pass** (Sparse Conditional Constant Propagation) uses a *monotonic-stack-like* worklist. The worklist holds "SSA values whose lattice state has not stabilized," ordered by the lattice height. Each pop either resolves a value (concrete constant) or pushes new consequences. The analysis is monotonic in the lattice (⊥ → constant → ⊤ only), ensuring termination in O(n) worklist operations — the same amortization argument we use for the array variant.

```cpp
// llvm/lib/Transforms/Scalar/SCCP.cpp — paraphrased
void SCCPSolver::Solve() {
  while (!InstWorkList.empty() || !OverdefinedInstWorkList.empty()) {
    while (!OverdefinedInstWorkList.empty()) {
      Instruction *I = OverdefinedInstWorkList.pop_back_val();
      // Overdefined values can only transition DOWN the lattice (toward ⊤).
      // Each instruction is pushed/popped at most O(1) times per lattice level,
      // giving total work O(n × lattice_height) — same amortized trick.
      for (User *U : I->users())
        if (auto *UI = dyn_cast<Instruction>(U))
          visit(*UI);
    }
    // ...
  }
}
```

**Four more real-world monotonic-stack sightings:**

1. **PostgreSQL's `width_bucket()` histogram optimizer** — bucket boundary lookup uses an increasing-stack-like structure for O(1) amortized bucket assignment per row during bulk inserts.
2. **Shunting-yard operator-precedence parsing** (Dijkstra, 1961) — the operator stack is kept in decreasing precedence; a higher-precedence incoming token pops lower-precedence operators. This is where Nagao & Matsuyama (1971) formalized the pattern.
3. **Dynamic histogram equalization in image processing** — row-wise largest-rectangle under a 1-pixel-wide moving window; identical O(n) algorithm.
4. **Protein folding dynamic programming** (NUPACK, Vienna RNA) — the "nearest unpaired base" lookup along a chain uses NGE-right internally for O(n) chain traversal.

## Recognition drill

<RecognitionDrill pattern="monotonic-stack" :count="10" />

## Advanced — follow-ups and failure modes

<details>
<summary><strong>What if you need the next k-th greater element, not just the next?</strong></summary>

The stack only remembers unresolved elements, so once popped, an answer is final — but you can push each element **k times** before resolving them, representing k "copies" of each unresolved answer slot. Alternatively, use a **persistent segment tree** or a Chtholly-tree-style structure for O(n log n). For k = 1, the monotonic stack is strictly better.
</details>

<details>
<summary><strong>What if the array is streaming and you need to answer "next greater" on prefix queries?</strong></summary>

**Persistent monotonic stack:** each version of the stack is kept, and the "next greater" query at time `t` references version `t`. Memory grows O(n), but query becomes O(log n). This is how competitive-programming "offline queries" are solved; a classic trick for CS problems.

For truly online queries (answer "next greater of a[i]" after each a[i] is appended), a plain monotonic stack is enough: push and pop as in Daily Temperatures; keep an array of resolved answers.
</details>

<details>
<summary><strong>What if the "monotonic" ordering is on a non-trivial key (e.g., 2D comparison)?</strong></summary>

A stack is one-dimensional. For 2D ordering ("nearest element greater in BOTH height and weight"), you need a **2D sweep** (sort by one key, use a monotonic stack on the other) or a **segment tree on sorted key**. A monotonic stack alone is insufficient — the comparison needs to be a total order to maintain the invariant.

Example: "Find the next element with higher score AND higher ranking" over students — sort by score, run a monotonic stack over ranking.
</details>

<details>
<summary><strong>What if you need to UPDATE elements mid-stream?</strong></summary>

The monotonic stack is one-shot — it processes left-to-right and never looks back. An update invalidates the whole stack. For an updatable version, use:
- **Segment tree with lazy propagation** — O(log n) per update, O(log n) per "next greater" query.
- **Treap or splay tree** — supports arbitrary updates and "greater-than" successor queries in O(log n) amortized.

The monotonic stack trades flexibility for a constant-factor speedup on static arrays.
</details>

<details>
<summary><strong>What if the problem has multiple pop conditions?</strong></summary>

Example: "next greater element that is also at least 2 apart in index." The classic template fails because a popped element might have a valid "next greater" further down the array. The fix: delay the pop by one step, or use a **monotonic deque** that supports lookahead at both ends.

In practice, 95% of interview problems have a single pop condition. If you see multiple, consider whether a two-pointer or segment-tree approach is cleaner.
</details>

### Breaking point

Monotonic stack **stops being optimal** when:
- The problem allows arbitrary queries at any index (segment tree is better).
- The array is dynamic (updates mid-processing — segment tree or treap).
- The ordering is not total (2D or multi-key — need a sweep + segment tree).
- You need all k nearest-greater elements, not just the first.
- The input is huge and must stream with constant memory (use a sliding-window maximum deque instead).

### Three cross-pattern problems

- [Maximum Width Ramp (962)](https://leetcode.com/problems/maximum-width-ramp/) — decreasing stack from the left + reverse sweep from the right; a non-obvious combination.
- [Beautiful Towers II (2866)](https://leetcode.com/problems/beautiful-towers-ii/) — monotonic stack to find "nearest smaller to left/right" + prefix-sum arithmetic.
- [Score of Parentheses (856)](https://leetcode.com/problems/score-of-parentheses/) — plain stack with monotonic-like depth tracking; a bridge to the parsing family.

---

## Check your understanding

<Quiz pattern-id="monotonic-stack" :questions="mastery5" />

<PrintButton />

<RelatedPatterns pattern-id="monotonic-stack" />
