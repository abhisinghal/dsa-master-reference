# Debugging DSA Code

*The single skill that separates senior from junior on the whiteboard isn't algorithm knowledge — it's **not panicking when the first attempt is wrong**. This chapter is the toolkit for that skill: how to catch off-by-ones, how to design adversarial test cases, and the five most costly bugs that appear in coding interviews.*

## The Trace Table — your single most powerful tool

You saw this technique used all through Sliding Window. It's worth its own chapter because most senior candidates *don't* do it, and it catches more bugs than any other single habit.

**How to build a trace table:**

1. Pick the smallest concrete input the problem allows — 3-6 elements is ideal. Not "abc"; something with structure like `[1, 3, -1, 2, 4]`.
2. Draw a table with one row per iteration of your outer loop.
3. Columns: **loop variable, key state (window sum, pointer positions, dp cell, whatever), condition being tested, action taken, answer-so-far**.
4. Fill it in *by hand*, line by line, following your code exactly.
5. Compare the final "answer-so-far" to what a brute force would produce on the same input.

**When to use it:**
- You're about to write code you're not 100% sure about.
- Your code compiles but gives wrong answer.
- Interviewer says "walk me through your solution."

**When NOT to use it:**
- The algorithm is a pattern you've written 10 times — a trace table is wasted time.
- The input space is huge and the trace won't fit. Pick a smaller input first.

Example — Sliding Window "sum of size k=3 in `[1,3,-1,2,4]`":

| right | a[right] | windowSum | window | full? | best |
|---|---|---|---|---|---|
| 0 | 1 | 1 | `[1]` | no | – |
| 1 | 3 | 4 | `[1,3]` | no | – |
| 2 | -1 | 3 | `[1,3,-1]` | yes | 3 |
| 3 | 2 | 4 | `[3,-1,2]` (dropped 1) | yes | 4 |
| 4 | 4 | 5 | `[-1,2,4]` (dropped 3) | yes | 5 |

The table forces you to be explicit about "is the window full yet?" — which is exactly where off-by-ones live.

## Adversarial test-case design

Every DSA problem has *the same five categories* of edge case. Memorize them; run through the list in your head before submitting.

### The five categories

1. **Empty input.** `[]`, `""`, `null`. What does your function return? Does it NPE?
2. **Single element.** `[5]`, `"a"`. Windows of size 1 degenerate. Two-pointers can never meet. Recursion base cases fire immediately.
3. **Two elements.** `[1,2]`, `"ab"`. Smallest case that exercises "both ends" of a two-pointer. Also the smallest case for a linked list to have a cycle (self-loop → cycle of length 1; two-node cycle exists but is rare).
4. **All identical.** `[5,5,5,5]`, `"aaaa"`. Duplicates. Dedup logic. In binary search, does your loop terminate when every element is equal to the target?
5. **Adversarial values.**
   - Negatives (Kadane, prefix sums, division)
   - Zero (division, product accumulator)
   - `Integer.MIN_VALUE` (negation trap)
   - Numbers that make sums overflow `int` (use `long`)
   - Already-sorted or reverse-sorted (best/worst case for many algorithms)

### The adversarial-value drill

Every time you write code, ask three questions about the *values*:

1. **What if there's a negative?** Try `-1`. Then try `[-1, -2, -3]` (all negative).
2. **What if there's a zero?** Try `0`, `[0]`, `[0, 0]`. What about `[0, 1, 0, 1]`?
3. **What if I hit the max?** For `int`: `2³¹ - 1 = 2147483647`. Try `[Integer.MAX_VALUE, 1]` — does your sum overflow?

Answering all three takes 30 seconds and catches most silent-corruption bugs.

## The 5 hardest-to-find bugs in DSA code

### Bug 1: Off-by-one in `[lo, hi)` vs `[lo, hi]`

Binary search's number-one killer. Fix by picking **one convention** (`[lo, hi)` half-open is my recommendation) and being *religious* about it.



```java
// Half-open [lo, hi) — never touch a[hi], loop while lo < hi
while (lo < hi) {
    int mid = lo + (hi - lo) / 2;
    if (pred(a[mid])) hi = mid;
    else lo = mid + 1;
}
// exit: lo == hi == first index where pred is true (or n if none)
```



If you catch yourself writing `while (lo <= hi)`, you're using the closed-interval convention — then your update MUST be `hi = mid - 1`, not `hi = mid`. Mixing them is the single most common binary-search bug.

### Bug 2: Not resetting state between recursion siblings



```java
List<List<Integer>> res = new ArrayList<>();
List<Integer> path = new ArrayList<>();
void dfs(...) {
    if (done) { res.add(path); return; }   // BUG: adds the same reference!
    ...
}
```



The `res.add(path)` stores the *reference*, and after all siblings return, `path` is empty — so `res` is a list of empty lists.

**Fix:** `res.add(new ArrayList<>(path))` — always deep-copy when snapshotting a mutable path.

### Bug 3: Modifying a collection while iterating



```java
for (Integer x : list) if (x < 0) list.remove(x);   // ConcurrentModificationException
```



**Fix:** iterate with an `Iterator` and call `it.remove()`, or copy into a new collection.

### Bug 4: `null`-returning `Map.get` unboxed to `int`



```java
int count = map.get(key);   // NPE if key absent!
int count = map.getOrDefault(key, 0);   // safe
```



Same trap with `Map<K,Integer>` returning `null` — always use `getOrDefault` or `merge`.

### Bug 5: Integer overflow in intermediate calculation



```java
int a = 1_000_000, b = 3_000_000;
int product = a * b;   // 3 × 10¹² doesn't fit in int → wraps to a negative number
```



Or in a sum:


```java
int[] nums = {Integer.MAX_VALUE, 1};
int sum = 0;
for (int x : nums) sum += x;   // overflow to Integer.MIN_VALUE + 0
```



**Fix:** use `long` for the accumulator whenever the *sum* or *product* can exceed `int`. Interview rule: **if the problem lets `n ≥ 10⁴` with values up to `10⁵`, your sum can hit `10⁹` — borderline `int`, use `long`.**

## Debugging by invariant assertion

The most senior debugging technique: state an invariant, then assert it inside the loop. If the assertion fires, you've localized the bug.

Example — sliding window:



```java
for (int right = 0; right < n; right++) {
    windowSum += a[right];
    while (windowSum > target) {
        windowSum -= a[left++];
    }
    // Invariant: windowSum ≤ target here
    assert windowSum <= target : "Invariant broken: sum=" + windowSum + " target=" + target;
    best = Math.min(best, right - left + 1);
}
```



Assertions are for **development, not production** — remove or disable them (`-ea`) before submission. But during construction, they force you to *name* what you're maintaining. If you can't name your invariant, you can't debug the code — because you don't understand what it's doing.

## The "3-example rule" for whiteboard problems

Before writing a line of code:

1. **Example 1**: the one the interviewer gave. Compute the expected output by hand.
2. **Example 2**: a smaller version you invent. Compute the expected output by hand.
3. **Example 3**: an adversarial edge case (empty / single / all-equal). Compute the expected output by hand.

Now your code has three ground-truth samples to check against. Any interviewer will tell you: the candidates who work through 2-3 examples first are the ones who finish. The ones who dive into code without examples get stuck at minute 25.

## The "narrate as you code" habit

Junior candidates go silent while coding. Senior candidates keep talking:

- "I'm going to iterate with `right`; when I add `a[right]`, I'll..."
- "Wait — what if `right` is 0? Let me think... yeah, `windowSum` starts at 0, add `a[0]`, we're fine."
- "OK so now I need to shrink while... hmm, actually let me pause — am I recording `best` before or after the shrink? Because if the window is invalid I shouldn't record."

The narration serves two purposes: **it prevents brain-lock**, and it lets the interviewer *help you when you're wrong* before you finish. If you code silently for 15 minutes and then reveal a bug, you've wasted 15 minutes. If you narrate, they'll nudge you at minute 3.

## Common bug patterns by algorithm family

| Family | Bug pattern | How to catch it |
|---|---|---|
| Binary Search | `[lo, hi]` mixed with `hi = mid` | Trace `[1,2,3,4], target=2` |
| Sliding Window | Not recording after shrink; recording partial windows | Trace with `k=3` and 4 elements |
| Two Pointers | Both pointers moving when only one should | Trace `[-2,-1,0,1,2]` for 2-sum |
| DFS/BFS | Not marking visited, or marking too late (in queue vs pop) | Trace a 4-node graph with cycle |
| DP | Wrong base case; iteration order wrong (using values before ready) | Print the DP table for `n=4` |
| Backtracking | Not un-doing choice; storing reference not copy | Print `path` at every recurse |
| Recursion | Missing base case; infinite loop on unchanged input | Add depth counter, print at each call |
| Heap | Wrong polarity (max-heap when you need min-heap) | Trace with 5 elements, k=2 |

Pin this table above your desk during interview prep.

## What to do when your test fails at minute 30 of a 45-minute interview

1. **Don't panic.** Every senior candidate has this happen. What matters is *how you recover*.
2. **State the failing input aloud.** "OK, for `[1, 2, 3]`, I expected 6 but got 5." Just saying it out loud often surfaces the bug — "Oh, I'm indexing from 1 instead of 0."
3. **Add a print / trace table.** Draw the trace by hand for the failing input. Don't run code again.
4. **State the invariant.** "At line 5 my invariant is X." Then check: is it actually X after line 5? If not, that's the bug.
5. **If you're truly stuck, ask for a hint.** Signaling "I've checked the obvious things and I'm stuck" is a legitimate senior move. "Is my loop invariant wrong, or is my base case wrong?" — a good question narrows the search.

The candidate who calmly debugs their own bug at minute 30 outperforms the candidate who wrote clean code the first time. Confidence under failure is what "senior" means.
