## The Pattern

A monotonic stack keeps candidate indices in increasing or decreasing value order so each new element resolves all earlier elements it dominates. The stack is not storing answers; it stores unresolved positions whose nearest greater/smaller neighbor has not appeared yet.

!!! pattern "Recognition signals"
    "Next greater/smaller," "previous greater/smaller," nearest boundary, span, visibility, temperatures until warmer day, or largest rectangle constrained by the first smaller bar on both sides.

```diagram
{"type":"array","values":[73,74,75,71,69,72],"pointers":[{"name":"i","index":5,"color":"accent","side":"bottom"}],"highlights":{"2":"green","3":"amber","4":"amber","5":"primary"},"caption":"When 72 arrives, it resolves colder unresolved days 69 and 71, but not 75."}
```

```diagram
{"type":"stack","items":[2,3,4],"highlights":{"2":"amber"},"top_label":"top"}
```

## The Invariant

For a decreasing stack used for next greater, indices on the stack have values in non-increasing order from bottom to top, and none has yet found a greater element to its right. When `a[i]` is greater than the top, `i` is the nearest greater index for that popped position because every index between them failed to pop it earlier.

Flip the comparison for next smaller. Store indices, not values, so you can compute distances, widths, and write answers at the original positions.

## Template

```java
// Next greater element to the right; unresolved positions remain -1.
int[] nextGreater(int[] a) {
    int n = a.length;
    int[] ans = new int[n];
    Arrays.fill(ans, -1);
    ArrayDeque<Integer> stack = new ArrayDeque<>();

    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && a[i] > a[stack.peek()]) {
            int j = stack.pop();
            ans[j] = i;
        }
        stack.push(i);
    }
    return ans;
}

// Histogram: increasing stack of bar indices, with a sentinel flush.
int largestRectangleArea(int[] heights) {
    ArrayDeque<Integer> stack = new ArrayDeque<>();
    int best = 0;
    for (int i = 0; i <= heights.length; i++) {
        int h = (i == heights.length) ? 0 : heights[i];
        while (!stack.isEmpty() && h < heights[stack.peek()]) {
            int height = heights[stack.pop()];
            int leftLess = stack.isEmpty() ? -1 : stack.peek();
            int width = i - leftLess - 1;
            best = Math.max(best, height * width);
        }
        stack.push(i);
    }
    return best;
}
```

## Worked Recognition

- **Daily Temperatures (monotonic stack)**: next greater to the right, but answer is distance `i - j` instead of the value.
- **Next Greater Element I/II**: direct next-greater template; circular arrays simulate two passes while only writing answers for real indices.
- **Largest Rectangle in Histogram (monotonic stack)**: next smaller boundaries define the maximal width for each popped height.

```diagram
{"type":"flow","width":440,"box":270,"title":"Resolve dominated stack entries","steps":[{"type":"start","text":"stack = unresolved indices"},{"type":"process","text":"read a[i]"},{"type":"decision","text":"a[i] dominates stack top?","yes":"pop and answer top","branch":{"label":"no","text":"push i","role":"green"}},{"type":"process","text":"repeat until invariant restored"},{"type":"end","text":"leftovers have no next greater/smaller"}]}
```

## Complexity

!!! complexity "Complexity"
    **T:** O(n) amortized. Each index is pushed once and popped once, so the inner while-loop is not nested quadratic work. **S:** O(n) for unresolved indices and the answer array.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Storing values instead of indices; using `<` vs `<=` without deciding how equal values should behave; forgetting the sentinel pass in histogram; computing histogram width as `i - stack.peek()` instead of `i - leftLess - 1`; assuming amortized O(n) without the push-once/pop-once argument.

## When NOT to use it

Do not use a monotonic stack when you need arbitrary range maximum queries with updates, k-window maxima (prefer monotonic deque; see **Sliding Window Maximum**), or global sorting/ranking rather than nearest greater/smaller boundaries.
