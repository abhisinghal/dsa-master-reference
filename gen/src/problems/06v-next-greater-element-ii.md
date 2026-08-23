# Monotonic Stack — Next Greater Element II

*[↗ LeetCode: Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/monotonic-stack)

<CompanyTags companies="Amazon, Google, Bloomberg" />

Given a **circular** integer array `nums`, return the next greater element for each position. If none exists, output `-1`.

**Example 1** — `nums = [1,2,1]` → `[2,-1,2]` (position 2 wraps around to position 0's `1`, still not greater; but then to position 1's `2`)
**Example 2** — `nums = [1,2,3,4,3]` → `[2,3,4,-1,4]`
**Example 3** — `nums = [5,4,3,2,1]` → `[-1,5,5,5,5]`

**Constraints** — `1 ≤ n ≤ 10⁴`; `-10⁹ ≤ nums[i] ≤ 10⁹`.


<Hints
  hint1="What element does each `i` ’see’ looking left or right? Nearest greater? Nearest smaller?"
  hint2="Maintain a stack that’s monotonic in one direction. When the new element breaks monotonicity, pop and answer for popped items."
  hint3="Contribution counting: instead of ’for each subarray find X’, ask ’for each element, how many subarrays does it contribute to?’"
/>
---

## Approach 1 — Brute force (2n scan per position)

**Intuition.** For each `i`, walk clockwise (mod n) up to `n-1` positions; return first `nums[j] > nums[i]`.

```java
int[] nextGreaterElementsBrute(int[] nums) {
    int n = nums.length;
    int[] out = new int[n];
    Arrays.fill(out, -1);
    for (int i = 0; i < n; i++) {
        for (int k = 1; k < n; k++) {
            int j = (i + k) % n;
            if (nums[j] > nums[i]) { out[i] = nums[j]; break; }
        }
    }
    return out;
}
```

**Complexity** — Time **O(n²)**; Space **O(1)**.

---

## Approach 2 — Monotonic stack over `2n` indices (canonical)

**Insight from brute.** For the non-circular version, we sweep right-to-left with a **decreasing stack**. To handle circularity, we sweep the array **twice** (iterating `2n - 1` down to 0), taking `i % n` as the real index. On the second pass, the stack is already primed with everything "to the right including wrap."

```java
int[] nextGreaterElements(int[] nums) {
    int n = nums.length;
    int[] out = new int[n];
    Arrays.fill(out, -1);
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 2 * n - 1; i >= 0; i--) {
        int val = nums[i % n];
        while (!stack.isEmpty() && stack.peek() <= val) stack.pop();
        if (i < n) out[i] = stack.isEmpty() ? -1 : stack.peek();
        stack.push(val);
    }
    return out;
}
```

<CodeTrace
  title="Circular NGE — nums=[1,2,1]"
  :values="['1','2','1','1','2','1']"
  :windowKeys="['i']"
  :cellWidth="30"
  :steps='[
    { pointers: { i: 5 }, vars: { stack: "[1]" }, note: "2nd pass: nums[5%3]=1; nothing to pop; push" },
    { pointers: { i: 4 }, vars: { stack: "[2]" }, note: "nums[1]=2 > 1 pops; push 2" },
    { pointers: { i: 3 }, vars: { stack: "[1,2]" }, note: "nums[0]=1; push over 2" },
    { pointers: { i: 2 }, vars: { stack: "[1,1,2]", out: "[·,·,2]" }, note: "i<n → out[2]=stack.peek() beyond current 1s → 2" },
    { pointers: { i: 1 }, vars: { stack: "[2]", out: "[·,-1,2]" }, note: "pops until 2; stack.peek()=2 above 2? empty → -1" },
    { pointers: { i: 0 }, vars: { stack: "[1,2]", out: "[2,-1,2]" }, note: "out[0]=peek=2" }
  ]'
/>

**Complexity** — Time **O(n)** (each index pushed and popped at most twice); Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="next-greater-element-ii" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Brute 2n-scan | O(n²) | O(1) | baseline |
| Monotonic stack, 2n sweep | **O(n)** | O(n) | canonical |

## When to use which

- **Any "next greater / smaller"** problem → monotonic stack.
- **Circular** variant → double the sweep, take `i % n`.
- **Return indices, not values** → push indices instead of values.
- **Nearest greater in a **stream** ** → maintain the stack incrementally; answer only for finalized items.

## Related problems

- [Daily Temperatures](/problems/monotonic-stack-daily-temperatures) — non-circular sibling
- [Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) — subset of positions
- [Sum of Subarray Minimums](/problems/sum-of-subarray-minimums) — count contribution per element
- [Trapping Rain Water](/problems/trapping-rain-water) — monotonic stack solution exists