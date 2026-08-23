# Two Pointers — Largest Rectangle in Histogram

*[↗ LeetCode: Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/monotonic-stack)

<CompanyTags companies="Amazon, Google, Microsoft, Meta, Adobe" />

Given bar heights, return the largest rectangle contained.

**Example 1** — `heights=[2,1,5,6,2,3]` → `10`
**Example 2** — `heights=[2,4]` → `4`

**Constraints** — `1 ≤ n ≤ 10⁵`.


<Hints
  hint1="Sort first if the input isn’t already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/>
---

## Approach 1 — For each bar expand outward

O(n²). Baseline.

## Approach 2 — Monotonic increasing stack (canonical)

**Insight.** When we push bar `i` and pop `t` (because `h[i] < h[t]`), both boundaries of `t`'s maximal rectangle are known: `next smaller = i`, `previous smaller = stack.peek()` after pop.

**Sentinel trick.** Iterate `i` from 0 to n **inclusive** with `h=0` at end to flush the stack.

```java
int largestRectangleArea(int[] h) {
    Deque<Integer> st = new ArrayDeque<>();
    int best = 0, n = h.length;
    for (int i = 0; i <= n; i++) {
        int val = i == n ? 0 : h[i];
        while (!st.isEmpty() && h[st.peek()] > val) {
            int t = st.pop();
            int w = st.isEmpty() ? i : i - st.peek() - 1;
            best = Math.max(best, h[t] * w);
        }
        st.push(i);
    }
    return best;
}
```

<CodeTrace
  title="Mono stack — heights=[2,1,5,6,2,3]"
  :values="['2','1','5','6','2','3']"
  :windowKeys="['i']"
  :cellWidth="30"
  :steps='[
    { pointers: { i: 2 }, vars: { st: "[1,2]" }, note: "" },
    { pointers: { i: 4 }, vars: { pop: 6, area: 6 }, note: "" },
    { pointers: { i: 4 }, vars: { pop: 5, area: 10 }, note: "5×2=10 best" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="largest-rectangle-in-histogram" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Expand | O(n²) | O(1) | baseline |
| Mono stack | **O(n)** | O(n) | canonical |

## When to use which

- **"Largest rectangle"** → mono stack + sentinel.
- **2D binary matrix** → row heights + this template (see [Maximal Rectangle](/problems/maximal-rectangle)).
- **"Range max/min queries"** → sparse table or seg tree.

<AiCompanion problem-slug="largest-rectangle-in-histogram" pattern-hint="two pointers" />

## Related problems

- [Maximal Rectangle](/problems/maximal-rectangle)
- [Sum of Subarray Minimums](/problems/sum-of-subarray-minimums)
- [Trapping Rain Water](/problems/trapping-rain-water)

<FeedbackWidget problem-slug="largest-rectangle-in-histogram" />
