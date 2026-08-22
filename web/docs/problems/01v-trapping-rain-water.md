# Two Pointers — Trapping Rain Water

*[↗ LeetCode: Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/two-pointers)

Given non-negative heights, compute how much water is trapped between them after rain.

**Example 1** — `heights=[0,1,0,2,1,0,1,3,2,1,2,1]` → `6`
**Example 2** — `heights=[4,2,0,3,2,5]` → `9`

**Constraints** — `1 ≤ n ≤ 2·10⁴`; `0 ≤ h ≤ 10⁵`.

---

## Approach 1 — Brute force (per-index scan)

**Intuition.** For each index `i`, water above it = `min(leftMax, rightMax) − h[i]`, where `leftMax` and `rightMax` are scanned each time.



```java
int trapBrute(int[] h) {
    int total = 0, n = h.length;
    for (int i = 0; i < n; i++) {
        int L = 0, R = 0;
        for (int j = 0; j <= i; j++) L = Math.max(L, h[j]);
        for (int j = i; j < n; j++) R = Math.max(R, h[j]);
        total += Math.max(0, Math.min(L, R) - h[i]);
    }
    return total;
}
```



**Complexity** — Time **O(n²)**; Space **O(1)**.

---

## Approach 2 — Precomputed prefix maxes

**Insight from brute.** `leftMax[i]` and `rightMax[i]` are two prefix scans.



```java
int trapPrefix(int[] h) {
    int n = h.length;
    int[] L = new int[n], R = new int[n];
    L[0] = h[0]; for (int i = 1; i < n; i++) L[i] = Math.max(L[i - 1], h[i]);
    R[n - 1] = h[n - 1]; for (int i = n - 2; i >= 0; i--) R[i] = Math.max(R[i + 1], h[i]);
    int total = 0;
    for (int i = 0; i < n; i++) total += Math.min(L[i], R[i]) - h[i];
    return total;
}
```



**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Approach 3 — Two pointers (O(1) space)

**Insight from prefix.** At each step, whichever side has the smaller running max is *bounded* on that side. Its trapped water depends only on its own running max, not on the other side's yet-to-be-seen values.

**Rule.** Advance from the *shorter* side; carry `leftMax`/`rightMax` incrementally.



```java
int trap(int[] h) {
    int lo = 0, hi = h.length - 1, lMax = 0, rMax = 0, total = 0;
    while (lo < hi) {
        if (h[lo] < h[hi]) {
            lMax = Math.max(lMax, h[lo]);
            total += lMax - h[lo];
            lo++;
        } else {
            rMax = Math.max(rMax, h[hi]);
            total += rMax - h[hi];
            hi--;
        }
    }
    return total;
}
```



<CodeTrace
  title="Two pointers — h=[0,1,0,2,1,0,1,3,2,1,2,1]"
  :values="[0,1,0,2,1,0,1,3,2,1,2,1]"
  :windowKeys="['lo','hi']"
  :cellWidth="30"
  :steps='[
    { pointers: { lo: 0, hi: 11 }, vars: { lMax: 0, rMax: 1, total: 0 }, note: "lo shorter → advance lo" },
    { pointers: { lo: 2, hi: 11 }, vars: { lMax: 1, total: 1 }, note: "trap 1 above idx 2 (lMax-h)", added: [2] },
    { pointers: { lo: 5, hi: 11 }, vars: { total: 4 }, note: "traps at 8,9,10 = +3", added: [8,9,10] },
    { pointers: { lo: 5, hi: 7 }, vars: { total: 6 }, note: "traps at 5,6 = +2. done", added: [5,6] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. Optimal.

---

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute per-index | O(n²) | O(1) |
| Prefix maxes | O(n) | O(n) |
| Two pointers | **O(n)** | **O(1)** |

## When to use which

- **Cold interview** → brute → prefix → two pointers with the "shorter side is bounded" argument.
- **Alternative:** monotonic stack (see Largest Rectangle in Histogram); different intuition, same asymptotic.

## Related problems

- [Trapping Rain Water II (2D)](https://leetcode.com/problems/trapping-rain-water-ii/) — BFS from the boundary with a min-heap
- [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) — different constraint but same two-pointer idea
- [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) — monotonic stack sibling
