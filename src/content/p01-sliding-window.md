## The Pattern

Sliding window turns "best/number of contiguous subarrays or substrings satisfying X" into one pass by maintaining state for a live interval `[left, right]`. Expand `right` to include new evidence; for variable windows, shrink `left` until the validity condition is restored or until the window is minimal.

!!! pattern "Recognition signals"
    Contiguous range, substring/subarray, "longest/shortest/count with constraint," a bounded violation budget, or frequency-count state over characters/elements. Fixed-size windows say "length k"; variable windows say "at most/at least/exactly K," "no repeats," or "cover all required chars."

```diagram
{"type":"array","values":["A","D","O","B","E","C"],"pointers":[{"name":"L","index":1,"color":"primary","side":"bottom"},{"name":"R","index":4,"color":"accent","side":"bottom"}],"brackets":[{"from":1,"to":4,"label":"window","color":"green","row":0}],"caption":"The algorithm only reasons about the live interval; counts are updated as L/R cross elements."}
```

## The Invariant

At every iteration, the auxiliary state exactly describes `nums[left..right]` (or `s[left..right]`): counts, sum, distinct count, missing requirements, max frequency, etc. The while-loop is not cleanup; it is the proof step that re-establishes the window's validity or minimality before recording an answer.

For fixed windows, the invariant is "window length is k after warm-up." For variable windows, define a predicate such as `valid(counts, need)` or `sum <= target`, then choose whether to record answers while valid (minimum-cover style) or after making valid (longest-valid style).

## Template

```java
// Variable-size window: expand right, then shrink left while the invariant requires it.
int solve(char[] a) {
    int left = 0, best = 0;
    int[] freq = new int[128];
    int violations = 0;

    for (int right = 0; right < a.length; right++) {
        int in = a[right];
        if (freq[in]++ == 1) violations++; // example: duplicate introduced

        while (violations > 0) {
            int out = a[left++];
            if (--freq[out] == 1) violations--;
        }

        best = Math.max(best, right - left + 1);
    }
    return best;
}

// Fixed-size window: add right, remove the element that falls out.
int fixedWindow(int[] nums, int k) {
    int sum = 0, best = Integer.MIN_VALUE;
    for (int right = 0; right < nums.length; right++) {
        sum += nums[right];
        if (right >= k) sum -= nums[right - k];
        if (right >= k - 1) best = Math.max(best, sum);
    }
    return best;
}
```

## Worked Recognition

- **Longest Substring Without Repeating Characters**: contiguous substring, maximize length, invalidity is a duplicate character. Use frequency counts and shrink until every count is ≤ 1.
- **Minimum Window Substring**: shortest substring covering a multiset. Expand to satisfy all required counts, then shrink while still valid to prove minimality.
- **Sliding Window Maximum**: still a window, but the state is not a frequency map; it needs a monotonic deque. See **Sliding Window Maximum** for the specialized state structure.

```diagram
{"type":"flow","width":440,"box":260,"title":"Variable window control loop","steps":[{"type":"start","text":"left = 0; state = empty"},{"type":"process","text":"include a[right] in state"},{"type":"decision","text":"window violates predicate?","yes":"yes","branch":{"label":"no","text":"record candidate","role":"green"}},{"type":"process","text":"remove a[left]; left++"},{"type":"end","text":"answer after all right positions"}]}
```

## Complexity

!!! complexity "Complexity"
    **T:** O(n) because each endpoint only moves forward; every element is added once and removed at most once. **S:** O(Σ) for frequency state over the alphabet/domain, or O(1) when the domain is fixed.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Recording the answer on the wrong side of the shrink loop; letting the count state drift from the actual window; using "exactly K" directly instead of `atMost(K) - atMost(K - 1)` when counting; assuming sliding window works with negative numbers and a sum constraint.

## When NOT to use it

Do not use sliding window when the chosen validity predicate is not monotone under moving `left` (for example, arbitrary negative numbers with target sum), when the range is not contiguous, or when the needed state requires global reordering rather than endpoint updates.
