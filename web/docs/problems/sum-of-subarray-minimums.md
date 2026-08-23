# Monotonic Stack — Sum of Subarray Minimums

*[↗ LeetCode: Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/monotonic-stack)

&lt;CompanyTags companies="Amazon, Google" /&gt;

Given an integer array `arr`, return the sum of `min(subarray)` over every contiguous subarray. Return modulo `10⁹ + 7`.

**Example 1** — `arr = [3,1,2,4]` → `17` (mins over all subarrays: 3+1+2+4 + 1+1+2 + 1+1 + 1 = 17)
**Example 2** — `arr = [11,81,94,43,3]` → `444`

**Constraints** — `1 ≤ n ≤ 3 · 10⁴`; `1 ≤ arr[i] ≤ 3 · 10⁴`.


&lt;Hints
  hint1="What element does each `i` ’see’ looking left or right? Nearest greater? Nearest smaller?"
  hint2="Maintain a stack that’s monotonic in one direction. When the new element breaks monotonicity, pop and answer for popped items."
  hint3="Contribution counting: instead of ’for each subarray find X’, ask ’for each element, how many subarrays does it contribute to?’"
/&gt;
---

## Approach 1 — Enumerate every subarray

**Intuition.** For each `[i, j]`, track min. Sum all.



```java
int sumSubarrayMinsBrute(int[] arr) {
    long sum = 0;
    int MOD = 1_000_000_007;
    for (int i = 0; i < arr.length; i++) {
        int mn = arr[i];
        for (int j = i; j < arr.length; j++) {
            mn = Math.min(mn, arr[j]);
            sum = (sum + mn) % MOD;
        }
    }
    return (int) sum;
}
```



**Complexity** — Time **O(n²)**; Space **O(1)**.

---

## Approach 2 — Monotonic stack: count contribution per element (canonical)

**Insight from brute.** Instead of "for each subarray, find min," ask "for each element, how many subarrays have this as the min?" Element `arr[i]` is the min of every subarray whose range covers `i` and stays within the region where all values are ≥ `arr[i]`.

Let `L[i]` = distance from `i` to previous strictly smaller (or edge), `R[i]` = distance from `i` to next strictly-or-equal smaller. Then `arr[i]` contributes to `L[i] · R[i]` subarrays, adding `arr[i] · L[i] · R[i]` to the sum.

**Trap** — the "strict / equal" boundary on the two sides must be **asymmetric** to avoid double-counting subarrays where multiple equal minima appear.



```java
int sumSubarrayMins(int[] arr) {
    int n = arr.length;
    int[] L = new int[n], R = new int[n];
    Deque<Integer> st = new ArrayDeque<>();
    // previous strictly smaller
    for (int i = 0; i < n; i++) {
        while (!st.isEmpty() && arr[st.peek()] >= arr[i]) st.pop();
        L[i] = st.isEmpty() ? i + 1 : i - st.peek();
        st.push(i);
    }
    st.clear();
    // next smaller-or-equal
    for (int i = n - 1; i >= 0; i--) {
        while (!st.isEmpty() && arr[st.peek()] > arr[i]) st.pop();
        R[i] = st.isEmpty() ? n - i : st.peek() - i;
        st.push(i);
    }
    long sum = 0, MOD = 1_000_000_007;
    for (int i = 0; i < n; i++)
        sum = (sum + (long) arr[i] * L[i] * R[i]) % MOD;
    return (int) sum;
}
```



<CodeTrace
  title="Contribution — arr=[3,1,2,4]"
  :values="['3','1','2','4']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { L: 1, R: 1, contrib: 3 }, note: "3 mins only in [3]" },
    { pointers: { i: 1 }, vars: { L: 2, R: 3, contrib: 6 }, note: "1 mins in 6 subarrays: covers all with 1" },
    { pointers: { i: 2 }, vars: { L: 1, R: 2, contrib: 4 }, note: "2 mins in [2], [2,4] → 2*2*1... check" },
    { pointers: { i: 3 }, vars: { L: 1, R: 1, contrib: 4 }, note: "4 mins in [4]" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="sum-of-subarray-minimums" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Every subarray | O(n²) | O(1) | baseline; TLE at 3·10⁴ |
| Contribution via monotonic stack | **O(n)** | O(n) | canonical |

## When to use which

- **"Sum / count over all subarrays'**  min or max"** → contribution counting via monotonic stack.
- **"Sum of subarray maximums"** → symmetric — flip inequalities.
- **"Sum of (max − min) over subarrays"** → do both, subtract.
- **Handling duplicates** — asymmetric strict/non-strict boundaries prevent double-counting.

## Related problems

- [Largest Rectangle in Histogram](/problems/largest-rectangle-in-histogram) — same L/R spanning trick
- [Sum of Subarray Ranges](https://leetcode.com/problems/sum-of-subarray-ranges/) — max − min
- [Maximum Sum of Minimum of Every Subarray](https://leetcode.com/problems/maximum-of-minimum-values-in-all-subarrays/) — related