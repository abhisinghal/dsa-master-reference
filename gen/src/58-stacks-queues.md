# Stacks &amp; Queues

A **stack** is your "most-recent-unresolved" memory — think matching brackets, undo, or the call stack of a DFS. A **queue** is "first-in-line" — think BFS or scheduling. In Java, use `ArrayDeque` for both (never the old `Stack` class).

This chapter covers the plain stack/queue *containers* — their operations and canonical uses. For the pattern of using a stack in *monotone order* to find nearest-greater/smaller elements, see the [Monotonic Stack pattern](#monotonic-stack) in Part II.

## Valid Parentheses
*[↗ LeetCode: Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)*

### Problem
Given a string of brackets `()[]{}`, decide if they are **balanced** — every opener closed by the matching type, in the correct order.

**Constraints:** `1 ≤ n ≤ 10⁴`; only bracket characters.

**Example:** `"([])"` → `true`; `"([)]"` → `false`.

### Pattern
Stack matching of nested delimiters.

> [inv] **Invariant** — The stack holds unmatched opening brackets in nesting order; a closer must match the top.

### Java
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

> [note] **Trace it** — `"([)]"`: push `(`, push `[`, then `)` needs the top to be `(` but it's `[` → mismatch → invalid. `"([])"` closes each in reverse order → valid.

Time O(n) · Space O(n).

> [trap] **Common Trap** — Returning `true` without checking `stack.isEmpty()`. *Example:* `s="(()"` — every closer matched, but one `(` was never closed. Return `stack.isEmpty()`, not just `true`.

> [pat] **Pattern Connection** — Stack-based parsing generalizes to expression evaluation (*Basic Calculator*), where operators and signs are pushed and resolved.

### Same pattern, new tweaks

A stack that remembers "unresolved context" handles all kinds of nesting:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Min Remove to Make Valid Parentheses](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/) | push indices of unmatched `(`; drop leftovers at the end | — |
| [Basic Calculator I/II](https://leetcode.com/problems/basic-calculator/) | push running values and signs; resolve on operators and closing brackets | — |
| [Decode String](https://leetcode.com/problems/decode-string/) | push `(repeatCount, prefix)` on `[`, pop and expand on `]` | — |
| [Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses/) | keep a stack of indices to measure the length of each valid span | — |


## Min Stack (O(1) minimum)
*[↗ LeetCode: Min Stack](https://leetcode.com/problems/min-stack/)*

### Problem
Design a stack supporting `push`, `pop`, `top`, and **`getMin`** — all in **O(1)**.

**Constraints:** up to `3·10⁴` operations; `getMin` must be O(1); `pop`/`top`/`getMin` are always called on a non-empty stack.

**Example:** `push(5), push(3), getMin()→3, pop(), getMin()→5`.

### Pattern
Augment each stack entry with the running minimum (or keep a parallel min-stack).

> [inv] **Invariant** — `minStack.peek()` is the minimum of all elements currently in the main stack.

### Java
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

> [note] **Trace it** — push `5,3,7`: the paired min-stack tracks `5,3,3`, so `getMin()` reads `3` in O(1). Pop `3` and the min instantly reverts to `5`.

**Time** O(1) for every operation (`push/pop/top/getMin`) · **Space** O(n) for the paired minimum.

> [trap] **Common Trap** — A single scalar `min` can't be restored after `pop`. *Example:* push 5, push 3 (min=3), pop 3 — should min go back to 5? Without a per-entry or parallel min, you've lost that history. Store the running min with each pushed value.

> [pat] **Pattern Connection** — Carrying an auxiliary aggregate alongside the primary structure is the same idea as a monotonic deque tracking the window max, and as segment-tree nodes storing subrange summaries.

### Same pattern, new tweaks

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

> [key] **Key Insight** — Stack↔queue conversions rest on the observation that reversing twice restores order; the amortized cost is O(1) because each element is transferred once.
