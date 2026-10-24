## Concepts & Mental Models

Stacks and queues are disciplined ways to delay work.

A **stack** is LIFO: the newest unresolved thing is the first one you revisit. It models nested structure, backtracking, call frames, and “the nearest candidate to the left.” A **queue** is FIFO: the oldest pending thing is served first. It models breadth-first expansion, buffering, rate-limited work, and sliding windows where old elements expire.

In Java interviews, the default concrete type is **`ArrayDeque`**. It is faster and cleaner than legacy `Stack`, supports `push`/`pop`/`peek` for stack behavior, and `offerLast`/`pollFirst`/`peekFirst` for queue behavior. Do not use `ArrayDeque` with `null`; it forbids null elements, which is useful because `peek()` returning null unambiguously means empty.

!!! key "ArrayDeque as both abstractions"
    Use one implementation, but keep the vocabulary honest: stack code should read as `push`, `pop`, `peek`; queue/deque code should read as `offerLast`, `pollFirst`, `peekFirst`, `peekLast`. The method names document the invariant.

The advanced pattern in this chapter is the **monotonic stack/deque**. Instead of storing every unresolved value, store only candidates that remain useful under an order invariant: increasing heights, decreasing temperatures, decreasing window values, etc. Whenever a new element makes older candidates impossible, pop them immediately.

!!! pattern "Pattern: Monotonic Stack/Deque · T: amortized O(n) · S: O(n)"
    **Signals:** nearest greater/smaller element, span until a blocking element, rectangle bounded by smaller bars, sliding-window maximum/minimum. Maintain indices, not just values, so distance, expiry, and widths are available.

The amortized proof is the same every time: each index is **pushed once** when first seen, and **popped at most once** when it becomes obsolete or resolved. A loop that appears nested is still linear because the inner pops cannot repeat for the same element. Across the whole scan, total pushes ≤ n and total pops ≤ n.

---

## Valid Parentheses

!!! pattern "Pattern: Stack for nested structure · T: O(n) · S: O(n)"
    **Signals:** balanced delimiters, last opener must match first closer, nesting matters.

### 1. Problem

Given a string containing only `()[]{}`, return whether every closing bracket matches the most recent unmatched opening bracket and all openings are eventually closed.

### 2. Key Observation

!!! key "Key observation"
    Parentheses are not just counted; they are **nested**. The only opener a closer may match is the most recent unmatched opener, exactly the LIFO rule of a stack.

### 3. Invariant

After scanning `s[0..i]`, the stack contains the unmatched opening brackets in bottom-to-top order. The top is the only legal match for the next closing bracket.

### 4. Visual Explanation

```diagram
{"type":"stack","items":["(","["],"highlights":{"1":"amber"},"top_label":"next ']' must match '['"}
```

### 5. Algorithm

Scan characters left to right. Push opening brackets. For a closing bracket, fail if the stack is empty or the popped opener is not its matching pair. At the end, succeed only if the stack is empty.

### 6. Java

```java
import java.util.ArrayDeque;
import java.util.Deque;

boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (c == '(' || c == '[' || c == '{') {
            stack.push(c);
        } else {
            if (stack.isEmpty()) return false;
            char open = stack.pop();
            if ((c == ')' && open != '(') ||
                (c == ']' && open != '[') ||
                (c == '}' && open != '{')) {
                return false;
            }
        }
    }
    return stack.isEmpty();
}
```

### 7. Complexity

!!! complexity "Complexity"
    **T:** O(n) — one scan. **S:** O(n) — all characters may be openers, e.g. `((((`.

### 8. Pattern Connection

This is the canonical stack problem: when the current token resolves the most recent unresolved token, use LIFO state. The same mental model appears in expression parsing, directory simplification, decoding strings, and monotonic stacks.

---

## Min Stack

!!! pattern "Pattern: Auxiliary stack state · T: O(1) operations · S: O(n)"
    **Signals:** normal stack operations plus a query over all current elements, usually minimum/maximum.

### 1. Problem

Design a stack supporting `push`, `pop`, `top`, and `getMin`, all in O(1) time.

### 2. Key Observation

!!! key "Key observation"
    The current minimum changes only when a pushed value is ≤ the old minimum or when the element being popped was the current minimum. Store the minimum **at each stack depth** so rollback is automatic.

### 3. Invariant

`stack.peek()` stores a pair `(value, minAtThisDepth)`. For every depth, `minAtThisDepth` is the minimum of all values from bottom through that node.

### 4. Visual Explanation

```diagram
{"type":"stack","items":["5|min5","2|min2","7|min2"],"highlights":{"1":"green","2":"amber"},"top_label":"top=7, min=2"}
```

### 5. Algorithm

On push, compute `newMin = stack.isEmpty() ? x : Math.min(x, stack.peek()[1])` and push `{x, newMin}`. Pop removes both the value and the minimum snapshot for that depth. `getMin` returns the second field at the top.

### 6. Java

```java
import java.util.ArrayDeque;
import java.util.Deque;

class MinStack {
    private final Deque<int[]> stack = new ArrayDeque<>();

    public void push(int val) {
        int min = stack.isEmpty() ? val : Math.min(val, stack.peek()[1]);
        stack.push(new int[] {val, min});
    }

    public void pop() {
        stack.pop();
    }

    public int top() {
        return stack.peek()[0];
    }

    public int getMin() {
        return stack.peek()[1];
    }
}
```

### 7. Complexity

!!! complexity "Complexity"
    **T:** O(1) for every operation. **S:** O(n) for n pushed elements and one minimum snapshot per element.

### 8. Pattern Connection

This is stack augmentation: attach exactly the aggregate needed to restore state after a pop. The same idea supports max stack, bracket parse state, undo logs, and DFS metadata.

---

## Daily Temperatures (monotonic stack)

!!! pattern "Pattern: Monotonic decreasing stack · T: O(n) · S: O(n)"
    **Signals:** for each index, find distance to the next strictly greater value on the right.

### 1. Problem

Given `temperatures[i]`, return an array `ans` where `ans[i]` is the number of days until a warmer temperature. If no future day is warmer, `ans[i] = 0`.

### 2. Intuition

A day remains unresolved until we see a warmer future day. If today's temperature is warmer than the day at the top of the stack, today resolves that day. It may also resolve several colder days behind it. Any day that survives must be warmer than or equal to today, because today's value could not resolve it.

### 3. Naive

For each day `i`, scan `j = i + 1..n-1` until `temperatures[j] > temperatures[i]`. This is O(n²) in decreasing or flat input, where most days scan to the end.

### 4. Key Observation

!!! key "Key observation"
    Keep only unresolved indices whose temperatures are in **monotonically non-increasing** order from bottom to top. When a warmer temperature arrives, repeatedly pop colder indices; the current index is exactly their next warmer day because all earlier scanned days failed to warm them.

### 5. Pattern Recognition

**Signals.** “Next greater to the right,” “how many days until,” one-dimensional array, answer per index.

**Shortcut.** If the question asks for the first future element that beats the current one, scan left-to-right with an unresolved stack or right-to-left with a candidate stack.

**Related.** Next Greater Element, Stock Span, Online Stock Span, car fleets, visibility problems.

### 6. Invariant

Before processing index `i`, the stack contains unresolved indices in increasing index order from bottom to top, and their temperatures are monotonically non-increasing: for adjacent stack indices `a` below `b`, `temperatures[a] >= temperatures[b]`. Every index not in the stack is already resolved or has no warmer day among processed indices.

### 7. Visual Explanation

```diagram
{"type":"stack","items":["0:73","1:74","2:75"],"highlights":{"2":"amber"},"top_label":"before i=3 temp=71"}
```

```diagram
{"type":"stack","items":["0:73","1:74","2:75","3:71","4:69"],"highlights":{"3":"red","4":"red"},"top_label":"i=5 temp=72 pops 4 then 3"}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":460,"box":270,"title":"Resolve colder pending days","steps":[{"type":"start","text":"i = 0, stack empty"},{"type":"decision","text":"stack not empty and temp[i] > temp[top]?","yes":"yes","branch":{"label":"no","text":"push i","role":"primary"}},{"type":"process","text":"j = pop()\nans[j] = i - j"},{"type":"process","text":"repeat while current day is warmer"},{"type":"end","text":"after scan, unresolved answers stay 0"}]}
```

### 9. Walkthrough

For `[73,74,75,71,69,72,76,73]`:

| i | temp | action | stack after | answer updates |
|---|---:|---|---|---|
| 0 | 73 | push | `[0]` | — |
| 1 | 74 | pop 0, push 1 | `[1]` | `ans[0]=1` |
| 2 | 75 | pop 1, push 2 | `[2]` | `ans[1]=1` |
| 3 | 71 | push | `[2,3]` | — |
| 4 | 69 | push | `[2,3,4]` | — |
| 5 | 72 | pop 4,3; push 5 | `[2,5]` | `ans[4]=1`, `ans[3]=2` |
| 6 | 76 | pop 5,2; push 6 | `[6]` | `ans[5]=1`, `ans[2]=4` |
| 7 | 73 | push | `[6,7]` | — |

### 10. Why It Works

When index `j` is popped by current index `i`, `temperatures[i] > temperatures[j]`. No processed index between `j` and `i` was warmer than `j`; otherwise `j` would have been popped earlier. Therefore `i` is the first warmer day for `j`, and `i - j` is exact. Indices left in the stack at the end have no warmer day to their right, so their default 0 is correct.

The monotonic invariant is restored after popping: all colder top elements are removed, so either the stack is empty or the new top has temperature ≥ `temperatures[i]`; pushing `i` preserves non-increasing temperature order.

### 11. Java

```java
import java.util.ArrayDeque;
import java.util.Deque;

int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] ans = new int[n];
    Deque<Integer> stack = new ArrayDeque<>(); // unresolved indices

    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
            int j = stack.pop();
            ans[j] = i - j;
        }
        stack.push(i);
    }
    return ans;
}
```

### 12. Code Walkthrough

`stack` stores indices, not temperatures, because the output is a distance. The `while` loop resolves every colder pending day for which `i` is the first warmer day. Equal temperatures are not popped because the problem requires strictly warmer. Unresolved entries remain 0 because Java initializes `int[]` to zero.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n) amortized. Each index is pushed exactly once and popped at most once; the total number of loop iterations across all `while` loops is at most n. **S:** O(n) for the unresolved stack in decreasing input.

### 14. Edge Cases

- Empty array → empty result.
- Single day → `[0]`.
- Strictly decreasing or all equal → all zeros; stack grows to n.
- Strictly increasing → every previous day resolves immediately with distance 1.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Popping equal temperatures (`>=`) is wrong because equal is not warmer. Storing values instead of indices loses distance. Using `Stack<Integer>` adds legacy synchronization and awkward API; use `ArrayDeque<Integer>`.

### 16. Optimization

The algorithm is already asymptotically optimal. A right-to-left jump-table solution can skip through answers, but it is less general than the monotonic-stack pattern and not usually clearer.

### 17. Alternatives

- Brute force: O(n²), simple but fails long decreasing inputs.
- Right-to-left monotonic stack: also O(n), stores candidate warmer days to the right.
- Bounded-temperature buckets: if temperatures are limited to 30..100, track next index per temperature; O(71n) = O(n), but pattern-specific.

### 18. Interview Follow-Ups

- Return the next warmer temperature rather than distance.
- Change “warmer” to “warmer or equal”; update the pop comparison.
- Process temperatures as a stream; unresolved indices must be retained until resolved.

### 19. Variations

Daily Temperatures is Next Greater Element over an array of temperatures with output transformed to distance. Stock Span reverses the direction and asks how far left until a greater blocker. Visibility problems often use the same stack but count popped elements.

### 20. Pattern Connection

This is the cleanest entry point to monotonic stacks: unresolved elements wait until a future element proves itself to be their first greater neighbor. The amortized push-once/pop-once argument is identical in histogram rectangles and next-greater circular arrays.

---

## Next Greater Element I/II

!!! pattern "Pattern: Monotonic decreasing stack · T: O(n) · S: O(n)"
    **Signals:** first greater value to the right; variant II wraps around circularly.

### 1. Problem

For each element, find the next greater element to its right. In Next Greater Element I, answer queries for `nums1` values using their positions in `nums2`. In Next Greater Element II, treat the array as circular and return `-1` when no greater element exists.

### 2. Key Observation

!!! key "Key observation"
    A decreasing stack stores values or indices still waiting for a greater value. When `x` arrives, it is the next greater for every smaller top it pops.

### 3. Invariant

For the non-circular scan, the stack contains unresolved values in strictly decreasing order from bottom to top. For the circular version, store indices and simulate two passes; push only during the first pass so each index is represented once.

### 4. Visual Explanation

```diagram
{"type":"stack","items":["4","2"],"highlights":{"1":"red"},"top_label":"current 3 pops 2; nextGreater[2]=3"}
```

### 5. Algorithm

For NGE I, scan `nums2`, pop smaller values and map them to the current value, then push current. Remaining values map to `-1`. For NGE II, iterate `i = 0..2n-1`, use `idx = i % n`, pop smaller indexed values and fill answers, but push `idx` only when `i < n`.

### 6. Java

```java
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.HashMap;
import java.util.Map;

int[] nextGreaterElement(int[] nums1, int[] nums2) {
    Map<Integer, Integer> next = new HashMap<>();
    Deque<Integer> stack = new ArrayDeque<>();

    for (int x : nums2) {
        while (!stack.isEmpty() && x > stack.peek()) {
            next.put(stack.pop(), x);
        }
        stack.push(x);
    }

    int[] ans = new int[nums1.length];
    for (int i = 0; i < nums1.length; i++) {
        ans[i] = next.getOrDefault(nums1[i], -1);
    }
    return ans;
}

int[] nextGreaterElementsCircular(int[] nums) {
    int n = nums.length;
    int[] ans = new int[n];
    Arrays.fill(ans, -1);
    Deque<Integer> stack = new ArrayDeque<>();

    for (int i = 0; i < 2 * n; i++) {
        int idx = i % n;
        while (!stack.isEmpty() && nums[idx] > nums[stack.peek()]) {
            ans[stack.pop()] = nums[idx];
        }
        if (i < n) stack.push(idx);
    }
    return ans;
}
```

### 7. Complexity

!!! complexity "Complexity"
    **T:** O(n + m) for NGE I, O(n) for NGE II. **S:** O(n) for stack plus answer/map storage. Circular scanning is still linear because each index is pushed once and popped once.

### 8. Pattern Connection

This is the value-returning sibling of Daily Temperatures. Use values when the value uniquely identifies the query and distance is irrelevant; use indices for duplicates, circularity, expiry, or widths.

---

## Largest Rectangle in Histogram (monotonic stack)

!!! pattern "Pattern: Monotonic increasing stack · T: O(n) · S: O(n)"
    **Signals:** largest area over contiguous bars; every candidate height is bounded by nearest smaller bars.

### 1. Problem

Given an array `heights`, where each value is a histogram bar of width 1, return the area of the largest rectangle formed by contiguous bars.

### 2. Intuition

For any bar `k`, the largest rectangle using `heights[k]` as the limiting height extends left and right until hitting a bar strictly shorter than `heights[k]`. So the problem reduces to finding, for each bar, its nearest smaller bar on both sides. A monotonic increasing stack discovers the right boundary exactly when a shorter bar arrives.

### 3. Naive

For every starting index, extend right while maintaining the minimum height and update `minHeight * width`. This is O(n²). A divide-and-conquer approach that repeatedly picks the minimum bar is O(n log n) with a segment tree but still more machinery than needed.

### 4. Key Observation

!!! key "Key observation"
    Maintain indices in the stack with **strictly increasing heights** from bottom to top after equal-height consolidation. When the current bar is shorter than the stack top, the popped bar's right boundary is current index `i`, and its left boundary is the new stack top. Its maximal rectangle is now fully known.

### 5. Pattern Recognition

**Signals.** Largest rectangle, contiguous range, limiting minimum, nearest smaller element.

**Shortcut.** If a range's score is `min(range) * width`, each bar wants to know the widest range where it remains the minimum.

**Related.** Maximal Rectangle in a Binary Matrix, Sum of Subarray Minimums, Trapping Rain Water variants, Cartesian tree construction.

### 6. Invariant

Before processing index `i`, the stack contains indices in strictly increasing order, and their heights are strictly increasing from bottom to top: if `a` is below `b`, then `heights[a] < heights[b]`. For every index in the stack, no shorter bar has appeared to its right among processed indices.

### 7. Visual Explanation

```diagram
{"type":"bars","values":[2,1,5,6,2,3],"highlights":{"2":"green","3":"green"}}
```

```diagram
{"type":"stack","items":["1:h1","2:h5","3:h6"],"highlights":{"2":"red"},"top_label":"i=4 h=2 pops h6 then h5"}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":470,"box":285,"title":"Finalize rectangles when a shorter bar appears","steps":[{"type":"start","text":"scan i from 0 through n\nuse sentinel height 0 at i=n"},{"type":"decision","text":"stack top height >= current height?","yes":"yes","branch":{"label":"no","text":"push i","role":"primary"}},{"type":"process","text":"mid = pop()\nright = i\nleft = stack.peek or -1"},{"type":"process","text":"area = height[mid] * (right-left-1)\nupdate best"},{"type":"end","text":"best is max rectangle"}]}
```

### 9. Walkthrough

For `[2,1,5,6,2,3]`, the best rectangle is height 5 over indices 2..3, area 10.

| i | h | action | stack after | area considered |
|---|---:|---|---|---:|
| 0 | 2 | push | `[0]` | — |
| 1 | 1 | pop 0, push 1 | `[1]` | `2 * 1 = 2` |
| 2 | 5 | push | `[1,2]` | — |
| 3 | 6 | push | `[1,2,3]` | — |
| 4 | 2 | pop 3, pop 2, push 4 | `[1,4]` | `6 * 1 = 6`, `5 * 2 = 10` |
| 5 | 3 | push | `[1,4,5]` | — |
| 6 | 0 | drain | `[]` | `3`, `8`, `6` |

### 10. Why It Works

When `mid` is popped at current index `i`, `heights[i]` is the first processed bar to the right that is shorter than or equal to `heights[mid]` under the chosen equality policy. After popping, the new stack top is the nearest strictly smaller bar to the left; everything between `left + 1` and `i - 1` has height at least `heights[mid]`. Therefore width `i - left - 1` is the widest possible rectangle with height `heights[mid]`.

Every maximal rectangle has some bar of minimum height. That bar is popped exactly when its right boundary becomes known, so the algorithm evaluates the rectangle corresponding to that minimum bar and cannot miss the optimum.

### 11. Java

```java
import java.util.ArrayDeque;
import java.util.Deque;

long largestRectangleArea(int[] heights) {
    int n = heights.length;
    long best = 0;
    Deque<Integer> stack = new ArrayDeque<>();

    for (int i = 0; i <= n; i++) {
        int current = (i == n) ? 0 : heights[i];
        while (!stack.isEmpty() && heights[stack.peek()] >= current) {
            int mid = stack.pop();
            int left = stack.isEmpty() ? -1 : stack.peek();
            long width = i - left - 1L;
            best = Math.max(best, (long) heights[mid] * width);
        }
        stack.push(i);
    }
    return best;
}
```

### 12. Code Walkthrough

The loop runs one extra iteration with sentinel height 0, forcing all remaining bars to be finalized. The stack stores indices so width can be computed from boundaries. The comparison `>= current` consolidates equal heights; this keeps the stack strictly increasing and lets the later equal-height index represent the wider future rectangle. `long` is used for multiplication even if the platform's final answer fits `int`.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n) amortized. Each index, including the sentinel index, is pushed once and popped at most once; the total work inside all popping loops is linear. **S:** O(n) for increasing histograms.

### 14. Edge Cases

- Empty input → 0.
- One bar → its height.
- All increasing → sentinel drains and computes widths.
- All decreasing → each new bar finalizes the previous one.
- Equal heights → use a consistent comparison (`>=` here) to avoid duplicate boundary ambiguity.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Using `i - left` instead of `i - left - 1` overcounts by including a shorter boundary. Forgetting the sentinel leaves increasing suffixes unevaluated. Multiplying two `int` values before widening can overflow; cast before multiplication.

### 16. Optimization

The stack solution is optimal for comparison-based scanning. You can precompute nearest-smaller-left and nearest-smaller-right arrays in two passes, but that uses more memory and duplicates what the one-pass stack discovers online.

### 17. Alternatives

- Brute force expansion: O(n²).
- Divide and conquer with segment tree RMQ: O(n log n), useful as a theoretical bridge to Cartesian trees.
- Two arrays of boundaries: O(n) time, O(n) space, easier to debug but less compact.

### 18. Interview Follow-Ups

- Extend to Maximal Rectangle in a binary matrix by treating each row as a histogram of consecutive ones.
- Return rectangle boundaries, not just area; store `bestLeft` and `bestRight` when updating.
- Handle very large heights/widths; return `long` instead of `int`.

### 19. Variations

Sum of Subarray Minimums also assigns each subarray to a unique minimum using nearest smaller boundaries, with careful tie-breaking. Trapping Rain Water looks similar but uses boundary maxima rather than minimum-height rectangles.

### 20. Pattern Connection

Histogram is the “nearest smaller boundary” counterpart to Daily Temperatures' “next greater resolver.” Both are amortized O(n) because each index enters the stack once and leaves once; the apparent nested loop is paid for by popping unique elements.

---

## Sliding Window Maximum (monotonic deque)

!!! pattern "Pattern: Monotonic decreasing deque · T: O(n) · S: O(k)"
    **Signals:** maximum/minimum over every fixed-size moving window; old indices expire while dominated indices become useless.

### 1. Problem

Given `nums` and window size `k`, return the maximum value in each contiguous window of length `k`.

### 2. Intuition

A max window needs only candidates that could still become maximum before they expire. If a new value is greater than or equal to the value at the deque's back, the older smaller value can never win: the new value is larger and expires later. Remove dominated backs, append the new index, then remove expired fronts.

### 3. Naive

Compute every window maximum by scanning its k elements. This is O(nk), too slow when both n and k are large. A heap gives O(n log k) but needs lazy deletion of expired indices. A monotonic deque is the direct O(n) structure.

### 4. Key Observation

!!! key "Key observation"
    Maintain a deque of indices in increasing index order and **strictly decreasing values** from front to back. The front is always the maximum of the current window; smaller elements behind a newer larger element are dominated forever.

### 5. Pattern Recognition

**Signals.** Fixed-size window, query max/min per window, one element enters and one element leaves each step.

**Shortcut.** If you need the best element under both value order and expiry order, use a deque: front handles expiry/output, back handles dominance.

**Related.** Sliding Window Minimum, shortest subarray with prefix sums at least K, constrained subsequence sum.

### 6. Invariant

After processing index `i` and removing expired indices, the deque contains indices within the current window `[i-k+1, i]`, increasing from front to back, and their values are strictly decreasing: for adjacent indices `a` before `b`, `nums[a] > nums[b]`. Therefore `nums[deque.peekFirst()]` is the window maximum.

### 7. Visual Explanation

```diagram
{"type":"array","values":[1,3,-1,-3,5,3],"highlights":{"1":"green","2":"amber","3":"amber"},"pointers":[{"name":"L","index":1,"color":"primary","side":"bottom"},{"name":"R","index":3,"color":"primary","side":"bottom"}],"brackets":[{"from":1,"to":3,"label":"k=3","color":"primary","row":0}],"caption":"Window [3,-1,-3] has maximum 3 at the deque front."}
```

```diagram
{"type":"queue","items":["1:3","2:-1","3:-3"],"orient":"horizontal","highlights":{"0":"green"},"top_label":"front is max"}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":470,"box":285,"title":"Maintain expiry at front and dominance at back","steps":[{"type":"start","text":"for i = 0..n-1"},{"type":"process","text":"remove front while index <= i-k"},{"type":"process","text":"remove back while nums[back] <= nums[i]"},{"type":"process","text":"offerLast(i)"},{"type":"decision","text":"i >= k-1?","yes":"yes","branch":{"label":"no","text":"continue","role":"red"}},{"type":"end","text":"ans[i-k+1] = nums[front]"}]}
```

### 9. Walkthrough

For `nums = [1,3,-1,-3,5,3,6,7]`, `k = 3`:

| i | x | deque after maintenance | output |
|---|---:|---|---:|
| 0 | 1 | `[0:1]` | — |
| 1 | 3 | `[1:3]` | — |
| 2 | -1 | `[1:3,2:-1]` | 3 |
| 3 | -3 | `[1:3,2:-1,3:-3]` | 3 |
| 4 | 5 | `[4:5]` | 5 |
| 5 | 3 | `[4:5,5:3]` | 5 |
| 6 | 6 | `[6:6]` | 6 |
| 7 | 7 | `[7:7]` | 7 |

### 10. Why It Works

The front is never expired because expiry is removed before output. The deque is decreasing by value because all back indices with value ≤ the incoming value are removed before insertion. Such removed indices are safe to discard: the new index has at least as large a value and a later expiry, so it will be preferable in every future window containing both.

Every valid window maximum is therefore present at the front. If a larger value existed behind the front, the decreasing invariant would be violated; if a larger value existed outside the deque, it was either expired or dominated by an even newer value that remains a better candidate.

### 11. Java

```java
import java.util.ArrayDeque;
import java.util.Deque;

int[] maxSlidingWindow(int[] nums, int k) {
    int n = nums.length;
    if (n == 0 || k <= 0 || k > n) return new int[0];

    int[] ans = new int[n - k + 1];
    Deque<Integer> deque = new ArrayDeque<>();

    for (int i = 0; i < n; i++) {
        while (!deque.isEmpty() && deque.peekFirst() <= i - k) {
            deque.pollFirst();
        }
        while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[i]) {
            deque.pollLast();
        }
        deque.offerLast(i);

        if (i >= k - 1) {
            ans[i - k + 1] = nums[deque.peekFirst()];
        }
    }
    return ans;
}
```

### 12. Code Walkthrough

The deque stores indices, not values, because indices determine expiry. Expiry uses `<= i - k`: an index at most `i-k` lies left of the current window's left boundary. The back-pop comparison uses `<=` to remove equal older values; keeping the newer equal value is at least as good because it expires later.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n) amortized. Each index is offered once, removed from the back at most once by domination, and removed from the front at most once by expiry. **S:** O(k) because the deque holds only indices in the current window.

### 14. Edge Cases

- `k = 1` → output equals input.
- `k = n` → one maximum.
- Strictly decreasing input → deque may hold k indices.
- Strictly increasing input → each new index dominates all previous candidates.
- Negative values work unchanged; comparisons are order-only.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Storing values instead of indices makes expiry ambiguous with duplicates. Removing expired elements after writing the answer can output a value outside the window. Using `<` instead of `<=` for equality is still correct but keeps older duplicates longer and weakens the strict invariant.

### 16. Optimization

The monotonic deque is optimal: every input element must be inspected, and output size is `n-k+1`. The main production tweak is returning `long[]` only when the values themselves are wider; no arithmetic overflow is involved in max comparisons.

### 17. Alternatives

- Heap of `(value,index)`: O(n log k), works but needs lazy deletion.
- Balanced tree/multiset: O(n log k), useful when you need median or arbitrary deletes.
- Block decomposition prefix/suffix maxima: O(n) time, O(n) space, strong for static offline arrays but less natural for streams.

### 18. Interview Follow-Ups

- Sliding window minimum: reverse the comparison.
- Variable-size windows: combine deque with two pointers if the validity predicate is monotone.
- Return indices of maxima; output `deque.peekFirst()` instead of the value.

### 19. Variations

Constrained subsequence sum uses a decreasing deque of DP values over the last k positions. Shortest Subarray with Sum at Least K uses an increasing deque of prefix sums, where front removal proves a valid length and back removal discards dominated prefixes.

### 20. Pattern Connection

This is the queue-shaped version of monotonic structure. A stack handles one-sided “next greater/smaller” resolution; a deque adds time expiry at the front. The same amortized push-once/pop-once proof gives linear time despite nested-looking loops.

