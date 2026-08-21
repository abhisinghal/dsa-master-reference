# Prefix Sum &amp; Difference Arrays

Suppose someone keeps asking you *"what's the sum of the array between index i and j?"* — over and over, for different ranges. Re-adding the elements every time is wasteful. So precompute a **running total**: let `pre[k]` be the sum of everything *before* index k. Now **any** range sum is a single subtraction, `pre[j+1] − pre[i]` — O(1) per query instead of O(n).

That's the **prefix sum**: it makes range *queries* cheap. Its mirror image, the **difference array**, makes range *updates* cheap. And the real party trick — pairing prefix sums with a hash map — lets you count subarrays with a target sum even when the numbers go negative (where a sliding window would fail).

```text
a      =   3   1   4   1   5
pre    = 0   3   4   8   9  14      pre[i] = sum of a[0..i-1]
sum(l..r) = pre[r+1] - pre[l]       e.g. sum(1..3)=pre[4]-pre[1]=9-3=6
```

> [key] **Key Insight** — "Sum over a range" ⇒ prefix sums. "Count subarrays whose sum = k" ⇒ prefix sums **as keys in a hash map**: a subarray `(l,r]` has sum k iff `pre[r]-pre[l]=k`, i.e. `pre[l]=pre[r]-k` was seen before.

### Recognize by
- many range-sum queries over a static array — precompute pre[], each query is O(1)
- "count subarrays with sum k" (with hash map, works for negative values too)
- "range-update, point-query" — the difference-array mirror

### When NOT to use it
You need to *update* array values *and* query ranges in the same run — a plain prefix sum is O(1) query but O(n) update. For both operations in O(log n), reach for [Fenwick / segment tree](#segment-tree-fenwick-tree).

---

## Subarray Sum Equals K
*[↗ LeetCode: Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/)*

### Problem
Count how many **contiguous subarrays** sum exactly to `k`. The array may contain **negative** numbers — which is what rules out a sliding window.

**Constraints:** `1 ≤ n ≤ 2·10⁴`; values and `k` fit in `int`; negatives allowed.

**Example:** `nums = [1,2,1,2,1], k = 3` → `4`.

### Pattern
Prefix sum + hash map of prefix frequencies. Handles negatives (sliding window cannot).

> [inv] **Invariant** — `count` maps each prefix-sum value to how many indices produced it among the processed prefix. At index `r`, the number of valid `l` is `count[pre - k]`.

### Java
```java
int subarraySum(int[] a, int k) {
    Map<Long,Integer> count = new HashMap<>();
    count.put(0L, 1);                 // empty prefix
    long pre = 0; int ans = 0;
    for (int x : a) {
        pre += x;
        ans += count.getOrDefault(pre - k, 0);
        count.merge(pre, 1, Integer::sum);
    }
    return ans;
}
```

> [note] **Trace it** — `a=[1,2,1,2,1], k=3`. Running prefixes `0,1,3,4,6,7`. Each time `pre−3` was seen before, you found a subarray: pairs give `[1,2],[2,1],[1,2],[2,1]` → **4**.

### Complexity
Time O(n) · Space O(n).

> [trap] **Common Trap** — Forgetting the `count.put(0,1)` seed drops subarrays that start at index 0. Do **not** use a sliding window here — negatives destroy the monotonic shrink.

> [pat] **Pattern Connection** — The shared idea is **charge a subarray-with-a-target-property to its prefix**: a subarray `(l,r]` has the property iff two prefixes differ by the target, so you store seen prefixes in a map. Recognize it in *Contiguous Array* (map a 0/1 array's ±1 running sum to the first index it appeared — a balanced subarray means equal prefixes) and *Subarray Sums Divisible by K* (bucket prefixes by `pre mod k`; two prefixes in the same bucket bound a divisible subarray). The transfer trick: rephrase "count subarrays where X" as "count prefix pairs that differ by X."

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k/) | key the map on `pre mod k` instead of the raw prefix | — |
| [Contiguous Array (equal 0s and 1s)](https://leetcode.com/problems/contiguous-array/) | treat 0 as −1; a subarray is balanced when two prefixes are equal | — |
| [Continuous Subarray Sum (multiple of k)](https://leetcode.com/problems/continuous-subarray-sum/) | same `mod k` bucketing, but store the earliest index to enforce a length ≥ 2 | — |
| [Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/) | count prefixes equal to `pre − goal` | — |

## Difference Array (Range Update)
*[↗ LeetCode: Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/)*

### Problem
You're given many **range updates** — each adds `v` to every element in `[l, r]` — and you only need the final array *after* all updates. Do it in O(n + m), not O(n·m).

**Constraints:** `n` slots, `m` updates, each `1 ≤ l ≤ r ≤ n`; running totals can exceed int → use `long`.

**Example:** `n = 5`, bookings `[1,2,10], [2,3,20], [2,5,25]` → `[10,55,45,25,25]`.

### Pattern
Invert prefix sum: to add `v` to `[l, r]`, do `diff[l] += v; diff[r+1] -= v`. One final prefix sum materializes all updates.

> [key] **Key Insight** — Batch many range increments in O(1) each, then reconstruct in O(n). Ideal when all updates precede all queries.

> [inv] **Invariant** — After processing, `prefix(diff)[i]` equals the net of all increments covering index `i`.

### Java
```java
// Corporate Flight Bookings: bookings[i] = {first, last, seats} (1-indexed)
int[] corpFlightBookings(int[][] bookings, int n) {
    long[] diff = new long[n + 1];
    for (int[] b : bookings) {
        diff[b[0] - 1] += b[2];
        diff[b[1]]     -= b[2];
    }
    int[] res = new int[n];
    long run = 0;
    for (int i = 0; i < n; i++) { run += diff[i]; res[i] = (int) run; }
    return res;
}
```

> [note] **Trace it** — `n=5`, bookings `[1,2,10],[2,3,20],[2,5,25]`. Endpoint marks then one prefix pass → per-flight seats `[10,55,45,25,25]` — three range adds settled in one sweep.

### Complexity
Time O(n + m) · Space O(n).

> [trap] **Common Trap** — Off-by-one at `r+1`; size the array `n+1` so the closing decrement never overflows the bounds.

> [pat] **Pattern Connection** — 2D difference arrays handle sub-rectangle increments; combined with a 2D prefix sum they answer *Range Sum Query 2D* in O(1) per query.

### Same pattern, new tweaks

"Mark the endpoints of each range, then one prefix pass materializes all updates" scales across dimensions:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/) | +seats at `first`, −seats after `last`; one sweep gives per-flight totals | — |
| [Car Pooling](https://leetcode.com/problems/car-pooling/) | a difference array over the *timeline* of pick-ups (+) and drop-offs (−); check capacity never overflows | — |
| [Range Addition](https://leetcode.com/problems/range-addition/) | the canonical form — apply many `[l, r] += v` in O(1) each, reconstruct once | O(1) |
| [2D — Range Addition II / stamping a grid](https://leetcode.com/problems/range-addition-ii/) | a 2D difference array marks the four corners of each rectangle | — |

## 2D Prefix Sum (Range Sum Query 2D)
*[↗ LeetCode: Range Sum Query 2D](https://leetcode.com/problems/range-sum-query-2d-immutable/)*

### Problem
Preprocess an **immutable** matrix so each query *"sum of the sub-rectangle from (r1,c1) to (r2,c2)"* answers in O(1).

**Constraints:** grid up to ~200×200; many queries → build once, then O(1) each.

**Example:** on `[[3,1],[2,4]]`, `sumRegion(0,0,1,1) = 10` (the whole grid); `sumRegion(1,1,1,1) = 4`.

> [key] **Key Insight** — Inclusion–exclusion: `sum(r1,c1,r2,c2) = P[r2+1][c2+1] − P[r1][c2+1] − P[r2+1][c1] + P[r1][c1]`.

### Java
```java
class NumMatrix {
    private final long[][] P;
    NumMatrix(int[][] m) {
        int R = m.length, C = m[0].length;
        P = new long[R + 1][C + 1];
        for (int i = 0; i < R; i++)
            for (int j = 0; j < C; j++)
                P[i+1][j+1] = m[i][j] + P[i][j+1] + P[i+1][j] - P[i][j];
    }
    int sumRegion(int r1, int c1, int r2, int c2) {
        return (int)(P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]);
    }
}
```

> [note] **Trace it** — `m=[[3,1],[2,4]]`. The padded prefix table gives `sumRegion(0,0,1,1) = P[2][2] − P[0][2] − P[2][0] + P[0][0] = 10 − 0 − 0 + 0 = 10` (the whole grid), and `sumRegion(1,1,1,1)=4` (just the corner).

Time: O(RC) build, O(1) query.

> [inv] **Invariant** — `P[i][j]` holds the sum of the sub-rectangle from `(0,0)` to `(i-1,j-1)`; the padding row/column of zeros makes every query boundary-safe.

> [trap] **Common Trap** — Sign/index errors in the four-term formula, or omitting the `+1` padding — then corner queries read out of bounds. Add back the double-subtracted corner (`+ P[r1][c1]`).

> [pat] **Pattern Connection** — The +/−/− /+ inclusion–exclusion pattern reappears in *Maximal Rectangle* accounting and 2D sweep problems.

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Matrix Block Sum](https://leetcode.com/problems/matrix-block-sum/) | answer each cell as the sum of a `k`-radius block using the same four-corner formula | — |
| [Count Submatrices With Target Sum](https://leetcode.com/problems/count-submatrices-with-target-sum/) | fix a pair of rows, collapse columns to 1D prefix sums, then reuse the "subarray sum = k" hash-map count | — |
| [Maximal Square / Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | combine per-row prefix counts with a histogram/DP to bound the largest all-ones region | — |
