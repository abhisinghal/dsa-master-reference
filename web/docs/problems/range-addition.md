# Prefix Sum — Range Addition

*[↗ LeetCode: Range Addition](https://leetcode.com/problems/range-addition/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

&lt;CompanyTags companies="Google, Amazon" /&gt;

Given length `n` and updates `[start, end, val]`, return the array after applying all updates.

**Example 1** — `n=5, updates=[[1,3,2],[2,4,3],[0,2,-2]]` → `[-2,0,3,5,3]`
**Example 2** — `n=1, updates=[[0,0,5]]` → `[5]`

**Constraints** — `1 ≤ n ≤ 10⁵`; `0 ≤ updates.length ≤ 10⁴`; inclusive ranges.


&lt;Hints
  hint1="Ask: can I answer `sum(i, j)` in O(1) given a preprocessed structure?"
  hint2="Prefix sums let you compute range sums as `pref[j+1] - pref[i]`. For ’count subarrays with property X on sum’, use a hash-map of prefix sums."
  hint3="For ’≥ 2 length’ or ’divisible by k’ variants, store first occurrence and check remainders."
/&gt;
---

## Approach 1 — Direct fill

O(n · m). Baseline.

## Approach 2 — Difference array (canonical)

**Insight.** Each range update `+val`, `-val` at endpoints; single prefix scan recovers totals.



```java
int[] getModifiedArray(int n, int[][] updates) {
    int[] diff = new int[n + 1];
    for (int[] u : updates) {
        diff[u[0]] += u[2];
        diff[u[1] + 1] -= u[2];
    }
    for (int i = 1; i < n; i++) diff[i] += diff[i - 1];
    return Arrays.copyOf(diff, n);
}
```



<CodeTrace
  title="Diff — n=5, updates=[[1,3,2],[2,4,3],[0,2,-2]]"
  :values="['-2','2+-2','3','5','3']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { deltas: "[-2, 2, 3, -2, 0, -3]" }, note: "sum of endpoint deltas" },
    { pointers: { i: 4 }, vars: { pref: "[-2,0,3,5,3]" }, note: "prefix sum" }
  ]'
/>

**Complexity** — Time **O(n + m)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="range-addition" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Direct fill | O(n·m) | O(n) | baseline |
| Diff array | **O(n+m)** | O(n) | optimum |

## When to use which

- **Static "many adds, one read"** → diff array.
- **Interleaved add + read** → segment tree with lazy propagation.
- **Multi-dim range add** → 2D diff array (see Matrix Block Sum).

&lt;AiCompanion problem-slug="range-addition" pattern-hint="prefix sum" /&gt;

## Related problems

- [Corporate Flight Bookings](/problems/corporate-flight-bookings)
- [Car Pooling](/problems/car-pooling)
- [Range Addition II](/problems/range-addition-ii)

&lt;FeedbackWidget problem-slug="range-addition" /&gt;
