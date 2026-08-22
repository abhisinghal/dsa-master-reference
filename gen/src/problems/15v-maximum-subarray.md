# Dynamic Programming — Maximum Subarray (Kadane)

*[↗ LeetCode: Maximum Subarray](https://leetcode.com/problems/maximum-subarray/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Find the contiguous subarray with the **largest sum** (must be non-empty).

**Example 1** — `nums=[-2,1,-3,4,-1,2,1,-5,4]` → `6` (the subarray `[4,-1,2,1]`)
**Example 2** — `nums=[1]` → `1`
**Example 3** — `nums=[5,4,-1,7,8]` → `23`

---

## Approach 1 — Brute force (all subarrays)

**Intuition.** Enumerate every subarray `[i..j]`; sum it; track max.

```java
int maxSubArrayBrute(int[] a) {
    int best = Integer.MIN_VALUE;
    for (int i = 0; i < a.length; i++) {
        int s = 0;
        for (int j = i; j < a.length; j++) {
            s += a[j];
            best = Math.max(best, s);
        }
    }
    return best;
}
```

**Complexity** — Time **O(n²)** (with running sum); **O(n³)** without; Space **O(1)**.

---

## Approach 2 — Divide & Conquer

**Insight.** The answer is either entirely in the left half, entirely in the right half, or *spans the middle*. Recurse.

```java
int maxSubArrayDC(int[] a) { return dc(a, 0, a.length - 1); }
int dc(int[] a, int lo, int hi) {
    if (lo == hi) return a[lo];
    int mid = (lo + hi) / 2;
    int left = dc(a, lo, mid);
    int right = dc(a, mid + 1, hi);
    // spanning: max suffix of left + max prefix of right
    int leftSum = Integer.MIN_VALUE, s = 0;
    for (int i = mid; i >= lo; i--) { s += a[i]; leftSum = Math.max(leftSum, s); }
    int rightSum = Integer.MIN_VALUE; s = 0;
    for (int i = mid + 1; i <= hi; i++) { s += a[i]; rightSum = Math.max(rightSum, s); }
    return Math.max(Math.max(left, right), leftSum + rightSum);
}
```

**Complexity** — Time **O(n log n)**; Space **O(log n)** recursion. Elegant but not the tightest.

---

## Approach 3 — Kadane's algorithm (rolling DP)

**Insight from brute.** The only state you need at position `i` is: "best subarray ending here." Grow it (`current += a[i]`) or restart (`current = a[i]`) — whichever is bigger. Track the global best.

**Trap.** Seed with `nums[0]`, not `0` — otherwise an all-negative array returns `0`.

```java
int maxSubArray(int[] a) {
    int cur = a[0], best = a[0];
    for (int i = 1; i < a.length; i++) {
        cur = Math.max(a[i], cur + a[i]);
        best = Math.max(best, cur);
    }
    return best;
}
```

<CodeTrace
  title="Kadane — nums=[-2,1,-3,4,-1,2,1,-5,4]"
  :values="[-2,1,-3,4,-1,2,1,-5,4]"
  :windowKeys="['i']"
  :cellWidth="32"
  :steps='[
    { pointers: { i: 0 }, vars: { cur: -2, best: -2 }, note: "seed" },
    { pointers: { i: 1 }, vars: { cur: 1, best: 1 }, note: "1 beats -2+1 → restart" },
    { pointers: { i: 3 }, vars: { cur: 4, best: 4 }, note: "restart with 4", added: [3] },
    { pointers: { i: 6 }, vars: { cur: 6, best: 6 }, note: "5+1=6 new peak", added: [6] },
    { pointers: { i: 8 }, vars: { cur: 5, best: 6 }, note: "final best = 6" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. Optimal.

---

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute all subarrays | O(n²) | O(1) |
| Divide & conquer | O(n log n) | O(log n) |
| Kadane rolling | **O(n)** | **O(1)** |

## When to use which

- **Cold interview** → brute → Kadane. D&C only if asked for the segment-tree generalization.
- **"Find the subarray, not just its sum"** → track `(start, end)` when you update `best`.

## Related problems

- [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) — track both min and max (negatives)
- [Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/) — `max(Kadane, total - minKadane)`
- [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) — Kadane on the price-diff array
