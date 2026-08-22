# Monotonic Stack — Sum of Subarray Minimums

*[↗ LeetCode: Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/monotonic-stack)

Sum of `min(subarray)` over every contiguous subarray. Answer mod `10⁹+7`.

**Example** — `arr=[3,1,2,4]` → `17`

---

## Approach 1 — Brute (all subarrays)

O(n²). TLE at n=3·10⁴.

## Approach 2 — Contribution technique via monotonic stack

**Insight.** Each element `a[i]` contributes to answer proportional to the number of subarrays where it is the min. Count = `(i − L) × (R − i)` where:
- `L` = index of nearest **strictly smaller** on the left (or -1)
- `R` = index of nearest **smaller-or-equal** on the right (or n) — tie-break rule prevents double-counting.

Compute L and R in two monotonic-stack passes.

```java
int sumSubarrayMins(int[] a) {
    int n = a.length, mod = 1_000_000_007;
    int[] L = new int[n], R = new int[n];
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        while (!st.isEmpty() && a[st.peek()] >= a[i]) st.pop();
        L[i] = st.isEmpty() ? -1 : st.peek();
        st.push(i);
    }
    st.clear();
    for (int i = n - 1; i >= 0; i--) {
        while (!st.isEmpty() && a[st.peek()] > a[i]) st.pop();
        R[i] = st.isEmpty() ? n : st.peek();
        st.push(i);
    }
    long total = 0;
    for (int i = 0; i < n; i++) total = (total + (long) a[i] * (i - L[i]) * (R[i] - i)) % mod;
    return (int) total;
}
```

<CodeTrace
  title="Contribution technique — arr=[3,1,2,4]"
  :values="[3,1,2,4]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { "L,R": "-1,1", contrib: "3*1*1=3" }, note: "3 is min of [3] only" },
    { pointers: { i: 1 }, vars: { "L,R": "-1,4", contrib: "1*2*3=6" }, note: "1 is min of many subarrays: 6 total" },
    { pointers: { i: 2 }, vars: { "L,R": "1,4", contrib: "2*1*2=4" }, note: "2 is min of [2], [2,4]" },
    { pointers: { i: 3 }, vars: { "L,R": "2,4", contrib: "4*1*1=4" }, note: "4 is min of [4] only. sum = 3+6+4+4 = 17", added: [0,1,2,3] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute | O(n²) | O(1) |
| Contribution + mono stack | **O(n)** | O(n) |

## Related problems

- [Sum of Subarray Ranges](https://leetcode.com/problems/sum-of-subarray-ranges/) — same idea, max − min per subarray
- [Number of Subarrays Where Boundary Elements Are Maximum](https://leetcode.com/problems/number-of-subarrays-where-boundary-elements-are-maximum/)
- [Largest Rectangle in Histogram](/problems/largest-rectangle-in-histogram) — nearest-smaller-both-sides pattern
