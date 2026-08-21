# Stacks &amp; Queues

A **stack** is your "most-recent-unresolved" memory — think matching brackets, undo, or the call stack of a DFS. A **queue** is "first-in-line" — think BFS or scheduling. In Java, use `ArrayDeque` for both (never the old `Stack` class).

This chapter covers the plain stack/queue *containers* — their operations and canonical uses. For the pattern of using a stack in *monotone order* to find nearest-greater/smaller elements, see the [Monotonic Stack pattern](/patterns/monotonic-stack) in Part II.

## Valid Parentheses <span class="diff diff-e">Easy</span>


*[↗ LeetCode: Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)*

<ProgressCheck id="valid-parentheses" />

### Problem

Given a string of brackets `()[]{}`, decide if they are **balanced** — every opener closed by the matching type, in the correct order.

**Constraints:** `1 ≤ n ≤ 10⁴`; only bracket characters.

**Example:** `"([])"` → `true`; `"([)]"` → `false`.

**Example 1:** "([])" -&gt; true.

**Example 2:** "([)]" -&gt; false.

### Solution — brute force

Ignore the structural shortcut and scan/recompute from scratch for each decision.



```text
for each query or candidate:
  scan the relevant array/list/tree/graph state
  recompute the answer directly
```



Brute-force complexity: usually O(n) per operation or O(n^2)+ overall, with extra space when a copied structure is used.

### Solution — optimized

**Pattern:**
Stack matching of nested delimiters.

<Callout kind="inv" title="Invariant">

The stack holds unmatched opening brackets in nesting order; a closer must match the top.

</Callout>

**Java:**


```java
boolean isValid(String s) {
    Deque<Character> st = new ArrayDeque<>();
    Map<Character,Character> match = Map.of(')','(', ']','[', '}','{');
    for (char c : s.toCharArray()) {
        if (match.containsValue(c)) st.push(c);
        else if (st.isEmpty() || st.pop() != match.get(c)) return false;
    }
    return st.isEmpty();
}
```



<Callout kind="note" title="Trace it">

`"([)]"`: push `(`, push `[`, then `)` needs the top to be `(` but it's `[` → mismatch → invalid. `"([])"` closes each in reverse order → valid.

</Callout>


<Callout kind="trap" title="Common Trap">

Returning `true` without checking `stack.isEmpty()`. *Example:* `s="(()"` — every closer matched, but one `(` was never closed. Return `stack.isEmpty()`, not just `true`.

</Callout>

<Callout kind="pat" title="Pattern Connection">

Stack-based parsing generalizes to expression evaluation (*Basic Calculator*), where operators and signs are pushed and resolved.

</Callout>

### Time Complexity

O(n): each bracket is pushed or popped at most once.

Original summary: Time O(n) · Space O(n).

### Space Complexity

O(n) worst case for all opening brackets.

### Learning notes

- Why stack? Closers must match the most recent opener.
- Why closer-&gt;opener map? It gives the required top value immediately.
- Why empty check before pop? Leading closers are invalid.
- Why final isEmpty? Unclosed openers must fail.

#### Same pattern, new tweaks

A stack that remembers "unresolved context" handles all kinds of nesting:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Min Remove to Make Valid Parentheses](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/) | push indices of unmatched `(`; drop leftovers at the end | — |
| [Basic Calculator I/II](https://leetcode.com/problems/basic-calculator/) | push running values and signs; resolve on operators and closing brackets | — |
| [Decode String](https://leetcode.com/problems/decode-string/) | push `(repeatCount, prefix)` on `[`, pop and expand on `]` | — |
| [Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses/) | keep a stack of indices to measure the length of each valid span | — |

## Min Stack (O(1) minimum) <span class="diff diff-m">Medium</span>


*[↗ LeetCode: Min Stack](https://leetcode.com/problems/min-stack/)*

<ProgressCheck id="min-stack-o-1-minimum" />

### Problem

Design a stack supporting `push`, `pop`, `top`, and **`getMin`** — all in **O(1)**.

**Constraints:** up to `3·10⁴` operations; `getMin` must be O(1); `pop`/`top`/`getMin` are always called on a non-empty stack.

**Example:** `push(5), push(3), getMin()→3, pop(), getMin()→5`.

**Example 1:** push(5), push(3), getMin() -&gt; 3, pop(), getMin() -&gt; 5.

**Example 2:** push(2), push(2), pop(), getMin() -&gt; 2.

### Solution — brute force

Ignore the structural shortcut and scan/recompute from scratch for each decision.



```text
for each query or candidate:
  scan the relevant array/list/tree/graph state
  recompute the answer directly
```



Brute-force complexity: usually O(n) per operation or O(n^2)+ overall, with extra space when a copied structure is used.

### Solution — optimized

**Pattern:**
Augment each stack entry with the running minimum (or keep a parallel min-stack).

<Callout kind="inv" title="Invariant">

`minStack.peek()` is the minimum of all elements currently in the main stack.

</Callout>

**Java:**


```java
class MinStack {
    private final Deque<int[]> st = new ArrayDeque<>();   // {value, minSoFar}
    public void push(int x) {
        int min = st.isEmpty() ? x : Math.min(x, st.peek()[1]);
        st.push(new int[]{x, min});
    }
    public void pop()      { st.pop(); }
    public int  top()      { return st.peek()[0]; }
    public int  getMin()   { return st.peek()[1]; }
}
```



<Callout kind="note" title="Trace it">

push `5,3,7`: the paired min-stack tracks `5,3,3`, so `getMin()` reads `3` in O(1). Pop `3` and the min instantly reverts to `5`.

</Callout>


<Callout kind="trap" title="Common Trap">

A single scalar `min` can't be restored after `pop`. *Example:* push 5, push 3 (min=3), pop 3 — should min go back to 5? Without a per-entry or parallel min, you've lost that history. Store the running min with each pushed value.

</Callout>

<Callout kind="pat" title="Pattern Connection">

Carrying an auxiliary aggregate alongside the primary structure is the same idea as a monotonic deque tracking the window max, and as segment-tree nodes storing subrange summaries.

</Callout>

### Time Complexity

O(1) for push, pop, top, and getMin.

Original summary: **Time** O(1) for every operation (`push/pop/top/getMin`) · **Space** O(n) for the paired minimum.

### Space Complexity

O(n) because each entry stores value and min-so-far.

### Learning notes

- Why minSoFar per entry? Pop restores the previous minimum instantly.
- Why int[] pair? It carries value and min together cheaply.
- Why not one scalar min? It loses history after popping the minimum.
- Why ArrayDeque? It is the modern Java stack/deque choice.

#### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Max Stack](https://leetcode.com/problems/max-stack/) | track a running max per entry (or a second stack) for O(1) `peekMax` | O(1) |
| [Sliding Window Minimum/Maximum](https://leetcode.com/problems/sliding-window-maximum/) | the queue version — a monotonic deque holding candidate extremes | — |
| [Stock Span / Online Stock Span](https://leetcode.com/problems/online-stock-span/) | each entry carries the span it dominates, collapsed as smaller values arrive | — |

## Queue &amp; Deque essentials
<p class="secgoal"><b>What & why:</b> the core queue/deque operations and the monotonic-deque trick. Goal — know exactly which method does what (offer / poll / peek / offerFirst) and when a double-ended queue beats a plain one.</p>

- **BFS** uses a FIFO queue; see Graphs/Trees. `ArrayDeque` as a queue: `offer`/`poll`.
- **Monotonic deque** (both-ended) generalizes the monotonic stack to sliding windows — see *Sliding Window Maximum*.
- **Implement queue with two stacks** — amortized O(1): push onto `in`; when popping, if `out` empty, pour `in`→`out` (reversing order). Each element moves at most twice.

<Callout kind="key" title="Key Insight">

Stack↔queue conversions rest on the observation that reversing twice restores order; the amortized cost is O(1) because each element is transferred once.

</Callout>
