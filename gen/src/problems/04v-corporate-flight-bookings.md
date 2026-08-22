# Prefix Sum — Corporate Flight Bookings

*[↗ LeetCode: Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

Given `n` flights and bookings `[first, last, seats]` (1-indexed inclusive), return per-flight seat totals.

**Example** — `n=5, [[1,2,10],[2,3,20],[2,5,25]]` → `[10,55,45,25,25]`

---

## Approach 1 — Difference array + prefix pass
**Insight.** Range add `[l, r] += x` via `diff[l] += x, diff[r+1] -= x`. One prefix pass reconstructs per-position totals.

```java
int[] corpFlightBookings(int[][] bookings, int n) {
    int[] diff = new int[n + 1];
    for (int[] b : bookings) { diff[b[0] - 1] += b[2]; diff[b[1]] -= b[2]; }
    int[] out = new int[n];
    int run = 0;
    for (int i = 0; i < n; i++) { run += diff[i]; out[i] = run; }
    return out;
}
```


<CodeTrace
  title="Difference array + prefix pass"
  :values="['1', '2', '10']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize; scan begins." },
    { pointers: { i: 0 }, vars: { phase: "midway" }, note: "Midway through the scan." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "All positions considered — return the answer." }
  ]'
/>


**Complexity** — Time **O(n + b)**; Space **O(n)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Difference array + prefix pass | O(n + b) | O(n) | primary |

## When to use which

- **Ship this** → Difference array + prefix pass (O(n + b), O(n)). The pattern's standard solution.

## Related problems

- [Car Pooling](/problems/car-pooling) — same idea, capacity check
- [Range Addition](/problems/range-addition)
- [Range Addition II](/problems/range-addition-ii)
