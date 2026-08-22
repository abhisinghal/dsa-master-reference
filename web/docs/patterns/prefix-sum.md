# Prefix Sum &amp; Difference Arrays

Suppose someone keeps asking you *"what's the sum of the array between index i and j?"* — over and over, for different ranges. Re-adding the elements every time is wasteful. So precompute a **running total**: let `pre[k]` be the sum of everything *before* index k. Now **any** range sum is a single subtraction, `pre[j+1] − pre[i]` — O(1) per query instead of O(n).

That's the **prefix sum**: it makes range *queries* cheap. Its mirror image, the **difference array**, makes range *updates* cheap. And the real party trick — pairing prefix sums with a hash map — lets you count subarrays with a target sum even when the numbers go negative (where a sliding window would fail).



```text
a      =   3   1   4   1   5
pre    = 0   3   4   8   9  14      pre[i] = sum of a[0..i-1]
sum(l..r) = pre[r+1] - pre[l]       e.g. sum(1..3)=pre[4]-pre[1]=9-3=6
```



<Callout kind="key" title="Key Insight">

"Sum over a range" ⇒ prefix sums. "Count subarrays whose sum = k" ⇒ prefix sums **as keys in a hash map**: a subarray `(l,r]` has sum k iff `pre[r]-pre[l]=k`, i.e. `pre[l]=pre[r]-k` was seen before.

</Callout>

### Recognize by
- many range-sum queries over a static array — precompute pre[], each query is O(1)
- "count subarrays with sum k" (with hash map, works for negative values too)
- "range-update, point-query" — the difference-array mirror

### When NOT to use it
You need to *update* array values *and* query ranges in the same run — a plain prefix sum is O(1) query but O(n) update. For both operations in O(log n), reach for [Fenwick / segment tree](/data-structures/segment-fenwick).

---

## Subarray Sum Equals K <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/)*

<ProgressCheck id="subarray-sum-equals-k" />





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <defs>
    <marker id="ar-ps-primary" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/></marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-primary)">Subarray sum = difference between two prefixes</text>
  <text x="44" y="86" text-anchor="end" font-size="12" font-weight="700" fill="var(--dsa-neutral)">nums</text>
  <text x="44" y="158" text-anchor="end" font-size="12" font-weight="700" fill="var(--dsa-neutral)">prefix</text>
  <g text-anchor="middle">
    <rect x="70" y="58" width="44" height="44" rx="7" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="122" y="58" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="174" y="58" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="226" y="58" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <g font-size="17" font-weight="700" fill="var(--dsa-ink)">
      <text x="92" y="86">1</text><text x="144" y="86">2</text><text x="196" y="86">3</text><text x="248" y="86">4</text>
    </g>
    <rect x="118" y="50" width="104" height="60" rx="10" fill="none" stroke="var(--dsa-primary)" stroke-width="var(--dsa-outline-stroke)"/>
    <text x="170" y="45" font-size="12" font-weight="700" fill="var(--dsa-primary)">subarray [2,3]</text>
    <rect x="70" y="130" width="44" height="44" rx="7" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="122" y="130" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="174" y="130" width="44" height="44" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="226" y="130" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <g font-size="17" font-weight="700" fill="var(--dsa-ink)">
      <text x="92" y="158">1</text><text x="144" y="158">3</text><text x="196" y="158">6</text><text x="248" y="158">10</text>
    </g>
  </g>
  <path d="M94 180 C110 210 180 210 196 180" fill="none" stroke="var(--dsa-primary)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-ps-primary)"/>
  <rect x="286" y="86" width="92" height="74" rx="9" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
  <text x="332" y="109" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">k = 5</text>
  <text x="332" y="130" text-anchor="middle" font-size="12" fill="var(--dsa-success)">6 - 1 = 5</text>
  <text x="332" y="150" text-anchor="middle" font-size="11" fill="var(--dsa-neutral)">pre[3]-pre[0]</text>
  <text x="200" y="228" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">at each prefix, ask how many earlier prefixes equal current - k</text>
</svg>
</div>




<div class="readfig"><b>How to read it:</b> The subarray <b>[2,3]</b> is found by subtracting an earlier prefix from the current prefix; the hashmap version counts how often <code>prefix - k</code> has appeared.</div>

### Problem
Count how many **contiguous subarrays** sum exactly to `k`. The array may contain **negative** numbers — which is what rules out a sliding window.

**Constraints:** `1 ≤ n ≤ 2·10⁴`; values and `k` fit in `int`; negatives allowed.

**Example 1:** `nums = [1,2,1,2,1], k = 3` → `4`.

&lt;ExamplePreview compact :input="['1', '2', '1', '2', '1', '|', '3']" :output="['4']" /&gt;

**Example 2:** `nums = [1,-1,0], k = 0` → `3` (`[1,-1]`, `[1,-1,0]`, and `[0]`).

&lt;ExamplePreview compact :input="['1', '-1', '0', '|', '0']" :output="['3']" /&gt;

### Solution — brute force
Start with the direct baseline: enumerate every candidate and compute the answer from scratch. It is correct, but it repeats the exact work that the pattern is meant to reuse.



```java
int subarraySumBrute(int[] a, int k) {
    int ans = 0;
    for (int left = 0; left < a.length; left++) {
        int sum = 0;
        for (int right = left; right < a.length; right++) {
            sum += a[right];
            if (sum == k) ans++;
        }
    }
    return ans;
}
```



**Brute-force cost:** O(n²) time, O(1) space — too slow for n ≥ 10⁴.

### Solution — optimized
The optimized idea counts prefix pairs. At running prefix `pre`, every earlier prefix equal to `pre - k` forms a subarray ending here with sum `k`, so a frequency map gives the answer immediately.

**Pattern.**
Prefix sum + hash map of prefix frequencies. Handles negatives (sliding window cannot).

**Java.**


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



### Time Complexity
Existing summary: Time O(n) · Space O(n).

The scan is O(n) because each array value updates one running prefix and performs two expected-O(1) hash-map operations.

### Space Complexity
Space is O(n) in the worst case because every prefix sum can be distinct and stored in the map.

### Learning notes
- Why `Map<Long,Integer>`? — prefix sums can exceed int range.
- Why `count.put(0L, 1)`? — it represents the empty prefix before index 0.
- Why add `count.getOrDefault(pre - k, 0)`? — those prior prefixes make subarrays summing to k.
- Why merge `pre` after counting? — the current prefix should be available only to future endings.
- Why frequencies, not one index? — multiple prior prefixes can create multiple valid subarrays.

<Callout kind="inv" title="Invariant">

`count` maps each prefix-sum value to how many indices produced it among the processed prefix. At index `r`, the number of valid `l` is `count[pre - k]`.

</Callout>

<Callout kind="note" title="Trace it">

`a=[1,2,1,2,1], k=3`. Running prefixes `0,1,3,4,6,7`. Each time `pre−3` was seen before, you found a subarray: pairs give `[1,2],[2,1],[1,2],[2,1]` → **4**.

</Callout>

<Callout kind="trap" title="Common Trap">

Forgetting the `count.put(0,1)` seed drops subarrays that start at index 0. Do **not** use a sliding window here — negatives destroy the monotonic shrink.

</Callout>


<CodeTrace
  title="Subarray Sum Equals K — a=[1,2,1,2,1], k=3"
  :values="[1,2,1,2,1]"
  :windowKeys="['i']"
  :cellWidth="38"
  :steps='[
    { pointers: { i: 0 }, vars: { pre: 1, "need pre-k": -2, count: 0, "seen": "{0:1}" }, note: "map miss. seen[1]=1" },
    { pointers: { i: 1 }, vars: { pre: 3, "need pre-k": 0, count: 1, "seen": "{0:1,1:1}" }, note: "seen[0]=1 → +1. seen[3]=1", added: [0,1] },
    { pointers: { i: 2 }, vars: { pre: 4, "need pre-k": 1, count: 2, "seen": "{0:1,1:1,3:1}" }, note: "seen[1]=1 → +1. seen[4]=1", added: [1,2] },
    { pointers: { i: 3 }, vars: { pre: 6, "need pre-k": 3, count: 3, "seen": "{0:1,1:1,3:1,4:1}" }, note: "seen[3]=1 → +1. seen[6]=1", added: [2,3] },
    { pointers: { i: 4 }, vars: { pre: 7, "need pre-k": 4, count: 4, "seen": "{...,4:1,6:1}" }, note: "seen[4]=1 → +1. final count=4", added: [3,4] }
  ]'
/>

<Callout kind="pat" title="Pattern Connection">

The shared idea is **charge a subarray-with-a-target-property to its prefix**: a subarray `(l,r]` has the property iff two prefixes differ by the target, so you store seen prefixes in a map. Recognize it in *Contiguous Array* (map a 0/1 array's ±1 running sum to the first index it appeared — a balanced subarray means equal prefixes) and *Subarray Sums Divisible by K* (bucket prefixes by `pre mod k`; two prefixes in the same bucket bound a divisible subarray). The transfer trick: rephrase "count subarrays where X" as "count prefix pairs that differ by X."

</Callout>

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k/) | key the map on `pre mod k` instead of the raw prefix | — |
| [Contiguous Array (equal 0s and 1s)](https://leetcode.com/problems/contiguous-array/) | treat 0 as −1; a subarray is balanced when two prefixes are equal | — |
| [Continuous Subarray Sum (multiple of k)](https://leetcode.com/problems/continuous-subarray-sum/) | same `mod k` bucketing, but store the earliest index to enforce a length ≥ 2 | — |
| [Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/) | count prefixes equal to `pre − goal` | — |

## Difference Array (Range Update) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/)*

<ProgressCheck id="difference-array-range-update" />

### Problem
You're given many **range updates** — each adds `v` to every element in `[l, r]` — and you only need the final array *after* all updates. Do it in O(n + m), not O(n·m).

**Constraints:** `n` slots, `m` updates, each `1 ≤ l ≤ r ≤ n`; running totals can exceed int → use `long`.

**Example 1:** `n = 5`, bookings `[1,2,10], [2,3,20], [2,5,25]` → `[10,55,45,25,25]`.

**Example 2:** `n = 3`, bookings `[1,1,5]` → `[5,0,0]` (single-point range closes immediately after index 0).

&lt;ExamplePreview compact :input="['3']" :output="['1', '1', '5']" /&gt;

### Solution — brute force
Start with the direct baseline: enumerate every candidate and compute the answer from scratch. It is correct, but it repeats the exact work that the pattern is meant to reuse.



```java
int[] corpFlightBookingsBrute(int[][] bookings, int n) {
    int[] res = new int[n];
    for (int[] b : bookings)
        for (int i = b[0] - 1; i <= b[1] - 1; i++) res[i] += b[2];
    return res;
}
```



**Brute-force cost:** O(n·m) time, O(n) output space — too slow when both flights and bookings are large.

### Solution — optimized
A range add can be represented by two endpoint marks: start adding at `l`, stop adding after `r`. One final prefix pass turns those marks into the actual per-index totals.

**Pattern.**
Invert prefix sum: to add `v` to `[l, r]`, do `diff[l] += v; diff[r+1] -= v`. One final prefix sum materializes all updates.

**Java.**


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



### Time Complexity
Existing summary: Time O(n + m) · Space O(n).

Processing m bookings is O(m) because each update writes two diff cells; reconstructing n flights is O(n), so total time is O(n + m).

### Space Complexity
Space is O(n) for the difference array and output array. The extra `+1` slot is a boundary sentinel for closing ranges at the end.

### Learning notes
- Why `long[] diff`? — many bookings can accumulate beyond int during reconstruction.
- Why `b[0] - 1`? — bookings are 1-indexed, Java arrays are 0-indexed.
- Why `diff[b[1]] -= b[2]`? — `b[1]` is the first index after the inclusive range.
- Why length `n + 1`? — ranges ending at flight n need a safe closing decrement.
- Why one prefix pass? — the running sum materializes all active increments.

<Callout kind="key" title="Key Insight">

Batch many range increments in O(1) each, then reconstruct in O(n). Ideal when all updates precede all queries.

</Callout>

<Callout kind="inv" title="Invariant">

After processing, `prefix(diff)[i]` equals the net of all increments covering index `i`.

</Callout>

<Callout kind="note" title="Trace it">

`n=5`, bookings `[1,2,10],[2,3,20],[2,5,25]`. Endpoint marks then one prefix pass → per-flight seats `[10,55,45,25,25]` — three range adds settled in one sweep.

</Callout>

<Callout kind="trap" title="Common Trap">

Off-by-one at `r+1`; size the array `n+1` so the closing decrement never overflows the bounds.

</Callout>


<CodeTrace
  title="Corporate Flight Bookings — n=5, three bookings"
  :values="[0,0,0,0,0]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { diff: "[10,0,-10,0,0,0]" }, note: "booking [1,2,10] → diff[0]+=10, diff[2]-=10" },
    { pointers: { i: 1 }, vars: { diff: "[10,20,-10,-20,0,0]" }, note: "[2,3,20] → diff[1]+=20, diff[3]-=20" },
    { pointers: { i: 2 }, vars: { diff: "[10,45,-10,-20,0,-25]" }, note: "[2,5,25] → diff[1]+=25, diff[5]-=25" },
    { pointers: { i: 0 }, vars: { seats: "[10,_,_,_,_]" }, note: "prefix pass: seats[0]=10", added: [0] },
    { pointers: { i: 1 }, vars: { seats: "[10,55,_,_,_]" }, note: "seats[1]=10+45=55", added: [1] },
    { pointers: { i: 2 }, vars: { seats: "[10,55,45,_,_]" }, note: "seats[2]=55−10=45", added: [2] },
    { pointers: { i: 3 }, vars: { seats: "[10,55,45,25,_]" }, note: "seats[3]=45−20=25", added: [3] },
    { pointers: { i: 4 }, vars: { seats: "[10,55,45,25,25]" }, note: "seats[4]=25+0=25 — final", added: [4] }
  ]'
/>

<Callout kind="pat" title="Pattern Connection">

2D difference arrays handle sub-rectangle increments; combined with a 2D prefix sum they answer *Range Sum Query 2D* in O(1) per query.

</Callout>

### Same pattern, new tweaks

"Mark the endpoints of each range, then one prefix pass materializes all updates" scales across dimensions:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/) | +seats at `first`, −seats after `last`; one sweep gives per-flight totals | — |
| [Car Pooling](https://leetcode.com/problems/car-pooling/) | a difference array over the *timeline* of pick-ups (+) and drop-offs (−); check capacity never overflows | — |
| [Range Addition](https://leetcode.com/problems/range-addition/) | the canonical form — apply many `[l, r] += v` in O(1) each, reconstruct once | O(1) |
| [2D — Range Addition II / stamping a grid](https://leetcode.com/problems/range-addition-ii/) | a 2D difference array marks the four corners of each rectangle | — |

## 2D Prefix Sum (Range Sum Query 2D) <span class="diff diff-m">Medium</span>
*[↗ LeetCode: Range Sum Query 2D](https://leetcode.com/problems/range-sum-query-2d-immutable/)*

### Problem
Preprocess an **immutable** matrix so each query *"sum of the sub-rectangle from (r1,c1) to (r2,c2)"* answers in O(1).

**Constraints:** grid up to ~200×200; many queries → build once, then O(1) each.

**Example 1:** on `[[3,1],[2,4]]`, `sumRegion(0,0,1,1) = 10` (the whole grid); `sumRegion(1,1,1,1) = 4`.

**Example 2:** on `[[5]]`, `sumRegion(0,0,0,0) = 5` (padding handles the smallest rectangle).

&lt;ExamplePreview compact :input="['[[5]]']" :output="['5']" /&gt;

### Solution — brute force
Start with the direct baseline: enumerate every candidate and compute the answer from scratch. It is correct, but it repeats the exact work that the pattern is meant to reuse.



```java
class NumMatrixBrute {
    private final int[][] m;
    NumMatrixBrute(int[][] matrix) { m = matrix; }
    int sumRegion(int r1, int c1, int r2, int c2) {
        int sum = 0;
        for (int r = r1; r <= r2; r++)
            for (int c = c1; c <= c2; c++) sum += m[r][c];
        return sum;
    }
}
```



**Brute-force cost:** O(R·C) per query in the worst case, O(1) extra space — too slow when many queries arrive.

### Solution — optimized
The optimized class pays one preprocessing pass to build a padded 2D prefix table. Every query then becomes four table lookups using inclusion–exclusion.

**Java.**


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



Time: O(RC) build, O(1) query.

### Time Complexity
Building `P` is O(RC) because each matrix cell contributes to one prefix-table cell. Each `sumRegion` call is O(1) because it reads four precomputed corners.

### Space Complexity
Space is O(RC) for the padded prefix table `P`; the extra top row and left column simplify boundary math.

### Learning notes
- Why `long[][] P`? — rectangle sums can be larger than one cell value.
- Why size `R + 1` by `C + 1`? — padding makes boundary queries safe.
- Why write `P[i+1][j+1]`? — prefix indices mean sum before this row/col boundary.
- Why subtract `P[i][j]` while building? — the top-left rectangle was added twice.
- Why the query has `- - +` terms? — subtract top/left strips, then add back their overlap.

<Callout kind="key" title="Key Insight">

Inclusion–exclusion: `sum(r1,c1,r2,c2) = P[r2+1][c2+1] − P[r1][c2+1] − P[r2+1][c1] + P[r1][c1]`.

</Callout>

<Callout kind="note" title="Trace it">

`m=[[3,1],[2,4]]`. The padded prefix table gives `sumRegion(0,0,1,1) = P[2][2] − P[0][2] − P[2][0] + P[0][0] = 10 − 0 − 0 + 0 = 10` (the whole grid), and `sumRegion(1,1,1,1)=4` (just the corner).

</Callout>

<CodeTrace
  title="2D Range Sum — matrix [[3,1],[2,4]], query sumRegion(1,1,1,1)"
  :values="[3,1,2,4]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { P: "[[0,0,0],[0,3,4],[0,5,10]]" }, note: "build prefix P with 1-row/col padding" },
    { pointers: { i: 3 }, vars: { r1: 1, c1: 1, r2: 1, c2: 1 }, note: "query (1,1)-(1,1) → single cell", added: [3] },
    { pointers: { i: 0 }, vars: { formula: "P[2][2] − P[1][2] − P[2][1] + P[1][1]" }, note: "10 − 4 − 5 + 3 = 4 ✓" }
  ]'
/>

<Callout kind="inv" title="Invariant">

`P[i][j]` holds the sum of the sub-rectangle from `(0,0)` to `(i-1,j-1)`; the padding row/column of zeros makes every query boundary-safe.

</Callout>

<Callout kind="trap" title="Common Trap">

Sign/index errors in the four-term formula, or omitting the `+1` padding — then corner queries read out of bounds. Add back the double-subtracted corner (`+ P[r1][c1]`).

</Callout>

<Callout kind="pat" title="Pattern Connection">

The +/−/− /+ inclusion–exclusion pattern reappears in *Maximal Rectangle* accounting and 2D sweep problems.

</Callout>

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Matrix Block Sum](https://leetcode.com/problems/matrix-block-sum/) | answer each cell as the sum of a `k`-radius block using the same four-corner formula | — |
| [Count Submatrices With Target Sum](https://leetcode.com/problems/count-submatrices-with-target-sum/) | fix a pair of rows, collapse columns to 1D prefix sums, then reuse the "subarray sum = k" hash-map count | — |
| [Maximal Square / Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | combine per-row prefix counts with a histogram/DP to bound the largest all-ones region | — |

---

## Check your understanding

<Quiz patternId="prefix-sum" :questions='[
  {
    "q": "You must count subarrays with sum k, and numbers may be negative. Which pattern applies?",
    "choices": [
      {
        "text": "Plain sliding window",
        "explanation": "Negatives destroy the monotone shrink rule."
      },
      {
        "text": "Prefix sum plus hash map",
        "correct": true,
        "explanation": "Yes. A previous prefix of current minus k identifies each valid subarray."
      },
      {
        "text": "Two sorted pointers"
      },
      {
        "text": "Monotonic stack"
      }
    ]
  },
  {
    "q": "Why seed the prefix-count map with sum 0 having count 1?",
    "choices": [
      {
        "text": "To handle empty input only"
      },
      {
        "text": "To count subarrays starting at index zero",
        "correct": true,
        "explanation": "Correct. If prefix itself equals k, the missing earlier prefix is the initial zero."
      },
      {
        "text": "To avoid sorting prefixes"
      },
      {
        "text": "To force positive sums"
      }
    ]
  },
  {
    "q": "Many range increments are known before any final query. What is the efficient tool?",
    "choices": [
      {
        "text": "Difference array",
        "correct": true,
        "explanation": "Right. Each update changes two boundaries, then one prefix pass reconstructs all values."
      },
      {
        "text": "Nested loop updates"
      },
      {
        "text": "Kahn topological sort"
      },
      {
        "text": "Quickselect partition"
      }
    ]
  }
]' />
