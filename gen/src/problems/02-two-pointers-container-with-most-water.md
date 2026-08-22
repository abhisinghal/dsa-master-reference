# Two Pointers — Container With Most Water

*[↗ LeetCode: Container With Most Water](https://leetcode.com/problems/container-with-most-water/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

Given `n` non-negative integer heights, find two vertical lines that form a container holding the maximum amount of water. Water volume = `min(h[i], h[j]) × (j − i)`.

**Example 1** — `heights = [1,8,6,2,5,4,8,3,7]` → `49` (indices 1 and 8: `min(8,7)*7`)
**Example 2** — `heights = [1,1]` → `1`
**Constraints** — `2 ≤ n ≤ 10⁵`, `0 ≤ h[i] ≤ 10⁴`.

---

## Approach 1 — Brute force (all pairs)

**Intuition.** Try every pair `(i, j)`; compute area; keep the max.

```java
int maxAreaBrute(int[] h) {
    int best = 0, n = h.length;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            best = Math.max(best, Math.min(h[i], h[j]) * (j - i));
    return best;
}
```

<CodeTrace
  title="Brute — heights=[1,8,6,2,5,4,8,3,7]: sampling a few pairs"
  :values="[1,8,6,2,5,4,8,3,7]"
  :windowKeys="['i','j']"
  :cellWidth="32"
  :steps='[
    { pointers: { i: 0, j: 8 }, vars: { area: 8 }, note: "min(1,7)*8 = 8" },
    { pointers: { i: 1, j: 8 }, vars: { area: 49 }, note: "min(8,7)*7 = 49 → best", added: [1,8] },
    { pointers: { i: 1, j: 6 }, vars: { area: 40 }, note: "min(8,8)*5 = 40" }
  ]'
/>

**Complexity** — Time **O(n²)**; Space **O(1)**. Fails at n=10⁵.

---

## Approach 2 — Two pointers from ends

**Insight from brute.** Start with the widest window `[0, n-1]`. Its area = `min(h[0], h[n-1]) * (n-1)`. Moving the **taller** wall inward can only *shrink* the width; the height is capped by the shorter wall so the area can only decrease. Moving the **shorter** wall inward might find a taller neighbour and win.

**Rule:** always advance the pointer at the *shorter* wall.

```java
int maxArea(int[] h) {
    int lo = 0, hi = h.length - 1, best = 0;
    while (lo < hi) {
        int area = Math.min(h[lo], h[hi]) * (hi - lo);
        best = Math.max(best, area);
        if (h[lo] < h[hi]) lo++;
        else               hi--;
    }
    return best;
}
```

<CodeTrace
  title="Two pointers — heights=[1,8,6,2,5,4,8,3,7]"
  :values="[1,8,6,2,5,4,8,3,7]"
  :windowKeys="['lo','hi']"
  :cellWidth="32"
  :steps='[
    { pointers: { lo: 0, hi: 8 }, vars: { area: 8, best: 8 }, note: "min(1,7)*8=8. lo shorter → lo++" },
    { pointers: { lo: 1, hi: 8 }, vars: { area: 49, best: 49 }, note: "min(8,7)*7=49 → new best. hi shorter → hi--" },
    { pointers: { lo: 1, hi: 7 }, vars: { area: 18, best: 49 }, note: "min(8,3)*6=18. hi--" },
    { pointers: { lo: 1, hi: 6 }, vars: { area: 40, best: 49 }, note: "min(8,8)*5=40. tie → shrink either" },
    { pointers: { lo: 1, hi: 5 }, vars: { area: 16, best: 49 }, note: "min(8,4)*4=16. hi--" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. Optimal.

**Trap.** Advancing the taller wall is provably wrong because the container's limiting dimension is the shorter wall — you'd shrink width without any chance of the height going up.

---

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(1) |
| Two pointers | **O(n)** | O(1) |

## When to use which

- **Interviewer opens cold** → state brute, then jump to two-pointer with the correctness argument.
- **Interviewer asks "why not move the taller wall?"** → the exchange argument above.

## Related problems (same ladder applies)

- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) — two pointers + per-side max
- [3Sum](https://leetcode.com/problems/3sum/) — sort, fix pivot, two-pointer the tail
- [Sort Colors](https://leetcode.com/problems/sort-colors/) — three-way partition (Dutch flag)
- [Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/) — two pointers from ends, fill back-to-front
