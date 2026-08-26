# Prefix Sum &amp; Difference Arrays


<PatternVideo pattern-name="Prefix Sum" duration="8–12 min" />

<PatternProgress pattern-id="prefix-sum" problems="prefix-sum-subarray-sum-equals-k, subarray-sums-divisible-by-k, contiguous-array, continuous-subarray-sum, corporate-flight-bookings, car-pooling, range-addition, matrix-block-sum, count-submatrices-with-target-sum, maximal-rectangle" />



## Why prefix sum exists — the story

You built a dashboard for a stock trading desk. Traders keep asking the same question in different forms: *"How much revenue did we book between March 3rd and March 17th?"* *"What's the total volume from tick 200 to tick 800?"* Every question is a **range sum** over the same underlying array.

The obvious answer: sum the range. A `for` loop from `l` to `r`, accumulate, return. It's five lines. For one query on 1,000 elements it's instant. For a hundred queries it's a hundred loops — still fine.

But the desk sends **50,000 queries per second** and the array has **10⁶ elements**. Now every query averages `5·10⁵` operations; total workload is `2.5·10¹⁰` per second. The CPU has 10⁹ cycles per second. **You are 25× slower than realtime.** Traders are getting stale numbers; the manager is asking questions in Slack. Every query is redoing work — array element `a[500]` gets added into every range that includes it, over and over.

The pattern is to trade one-time prep for permanently cheap queries. Compute a **running total** array `pre[]` once: `pre[i]` = sum of everything strictly before index `i`. Now every range sum becomes **one subtraction**: `sum(l..r) = pre[r+1] - pre[l]`. **O(n) prep + O(1) per query.** For the trading desk: prep once (10⁶ ops), then every query is a single subtraction — the CPU handles 50K queries per second with time to spare.

The mirror image — the **difference array** — makes range *updates* cheap: instead of adding `+5` to every element in `[l, r]`, you flag `+5` at `l` and `-5` at `r+1`, then run a prefix sum at the end to materialize the final array. Range-update problems that would be O(nQ) become O(n + Q).

And the party trick: pair prefix sums with a hash map to count subarrays with a target sum — even with negative numbers, where a sliding window silently fails. That's the pattern behind Subarray Sum Equals K, one of the top-10 most-asked LeetCode problems in FAANG interviews.

## The core idea — precompute once, query in O(1) forever

```text
a      =   3   1   4   1   5
pre    = 0   3   4   8   9  14      pre[i] = sum of a[0..i-1]
sum(l..r) = pre[r+1] - pre[l]       e.g. sum(1..3)=pre[4]-pre[1]=9-3=6
```

Read that carefully. `pre[]` has **length n+1**, not `n`. The extra slot at `pre[0] = 0` is not a mistake — it lets you query `sum(0..r) = pre[r+1] - pre[0]` without special-casing the left edge. Every off-by-one bug in prefix sum comes from getting `pre[]`'s length wrong.

> [key] **Key Insight** — "Sum over a range" ⇒ prefix sums. "Count subarrays whose sum = k" ⇒ prefix sums **as keys in a hash map**: a subarray `(l,r]` has sum k iff `pre[r]-pre[l]=k`, i.e. `pre[l]=pre[r]-k` was seen before.

## When to use it — recognition signals

Reach for prefix sum (or its variants) when:

- **Many range-sum queries on a static array** — build once, answer each in O(1).
- **Count subarrays with sum = k** (or divisible by k, or in a range) — combine prefix sum with a HashMap of `pre -> count`.
- **Range updates on an array** followed by a materialization pass — difference array turns O(nQ) into O(n+Q). Classic examples: Corporate Flight Bookings, Car Pooling, Range Addition.
- **2D range-sum queries** — extend to 2D prefix sum (a.k.a. summed-area tables). Answers rectangle-sum queries in O(1) with O(nm) prep. Used by image-processing algorithms.
- **Contiguous subarray with equal 0s and 1s** — remap `0 → -1`, then a subarray sums to 0 iff `pre[l] == pre[r]`. This is the *equal-partition* trick.
- **Sliding window doesn't work because values can be negative** — a window can't reliably shrink when the sum can go up or down. Prefix sums + hashing is the escape hatch.

## When NOT to use it

- **You need range operations other than sum** — prefix sum extends to prefix-max only for immutable arrays; prefix-min/max with updates is a **segment tree**, not prefix sum.
- **The array is dynamic (values change between queries)** — prefix sum recomputes from scratch after every update. If you have thousands of updates interleaved with queries, use a **Fenwick tree (BIT)** or **segment tree** for O(log n) both.
- **Just one query on the whole array** — prefix sum's prep cost equals the query cost. Just accumulate in a single loop.
- **Multi-dimensional ranges beyond 2D** — 3D prefix sum works but memory is O(nmp) and inclusion-exclusion has 8 terms. Consider whether the problem really needs that dimensionality.
- **The subarray-sum target is 0 and the array is all zeros** — degenerate case; the count blows up quadratically. Handle explicitly.

## The templates

### Template 1: 1D prefix sum for range queries

```java
class RangeSumQuery {
    int[] pre;                              // length n+1; pre[0]=0

    RangeSumQuery(int[] a) {
        pre = new int[a.length + 1];
        for (int i = 0; i < a.length; i++) {
            pre[i + 1] = pre[i] + a[i];     // running total
        }
    }

    int sum(int l, int r) {                 // inclusive [l, r]
        return pre[r + 1] - pre[l];         // O(1) per query
    }
}
```

**Invariant:** `pre[i]` equals `a[0] + a[1] + ... + a[i-1]`. Length is `n+1`. `pre[0] = 0` is the sum of the empty prefix.
**Complexity:** O(n) build, O(1) per query, O(n) space.

### Template 2: Subarray Sum Equals K (the hash-map trick)

```java
int subarraySumEqualsK(int[] a, int k) {
    Map<Integer, Integer> countByPrefix = new HashMap<>();
    countByPrefix.put(0, 1);                // empty prefix has sum 0, seen once
    int running = 0, answer = 0;
    for (int x : a) {
        running += x;
        // Any earlier position with prefix (running - k) gives a subarray summing to k.
        answer += countByPrefix.getOrDefault(running - k, 0);
        countByPrefix.merge(running, 1, Integer::sum);
    }
    return answer;
}
```

**Invariant:** at every iteration, `countByPrefix` holds the number of times each prefix sum has appeared *up to and including* the current position.
**Complexity:** O(n) time, O(n) space. **Handles negative numbers** — the killer feature vs. sliding window.

**The `put(0, 1)` line matters.** It represents the "empty prefix": if the running total ever equals `k` itself, that's a valid subarray starting at index 0. Forgetting this line makes the code silently return `answer - 1` for those cases.

### Template 3: Difference array for range updates

```java
int[] applyRangeUpdates(int n, int[][] updates) {   // updates[i] = [l, r, delta]
    int[] diff = new int[n + 1];
    for (int[] u : updates) {
        diff[u[0]]     += u[2];             // start of range
        diff[u[1] + 1] -= u[2];             // one past end
    }
    int[] result = new int[n];
    result[0] = diff[0];
    for (int i = 1; i < n; i++) {
        result[i] = result[i - 1] + diff[i];   // prefix sum reveals final values
    }
    return result;
}
```

**Invariant:** at the end, `result[i]` equals the sum of `delta` values from all updates whose range contains `i`.
**Complexity:** O(n + Q). Compare to naive: O(nQ).

### Template 4: 2D prefix sum (summed-area table)

```java
class RangeSum2D {
    int[][] pre;

    RangeSum2D(int[][] m) {
        int r = m.length, c = m[0].length;
        pre = new int[r + 1][c + 1];
        for (int i = 0; i < r; i++)
            for (int j = 0; j < c; j++)
                pre[i+1][j+1] = m[i][j] + pre[i][j+1] + pre[i+1][j] - pre[i][j];
    }

    int rectSum(int r1, int c1, int r2, int c2) {   // inclusive rectangle
        return pre[r2+1][c2+1] - pre[r1][c2+1] - pre[r2+1][c1] + pre[r1][c1];
    }
}
```

**Invariant:** `pre[i][j]` = sum of the sub-rectangle from `(0,0)` to `(i-1, j-1)`.
**Complexity:** O(rc) build, O(1) per query.
**Trap:** the inclusion-exclusion in `rectSum` has four terms — miss a sign and you get random wrong answers.

### Complexity summary

| Approach | Build | Query | Update | Space |
|---|---|---|---|---|
| Naive range sum | 0 | O(n) | O(1) | O(n) |
| **1D prefix sum** | **O(n)** | **O(1)** | **O(n) rebuild** | **O(n)** |
| Fenwick tree | O(n log n) | O(log n) | O(log n) | O(n) |
| Segment tree | O(n) | O(log n) | O(log n) | O(n) |
| **2D prefix sum** | **O(rc)** | **O(1)** | **O(rc) rebuild** | **O(rc)** |
| **Difference array** | **O(n+Q)** | **O(1) after materialize** | **O(1)** | **O(n)** |

Rule of thumb: **prefix sum when array is static; Fenwick/segment tree when updates are frequent.**

## Traps & gotchas — the 5 that fail candidates on interview day

> [trap] **Trap 1 — Off-by-one on `pre[]` length.** The most common bug in this pattern. `pre[]` must have length `n+1`, with `pre[0] = 0`. If you allocate `pre[n]`, you have no `pre[0]` sentinel and must special-case queries starting at index 0. **Rule: always size `pre[]` to `n+1`.**

> [trap] **Trap 2 — Forgetting `countByPrefix.put(0, 1)` in the hash-map variant.** This entry represents the empty prefix. Without it, subarrays that start at index 0 are undercounted. On input `[3, 4]` with `k = 3`, you should return `1` but return `0`. **Rule: seed the hash with `{0: 1}` before the loop.**

> [trap] **Trap 3 — Integer overflow.** `pre[i]` for `n = 10⁵` values of `10⁹` reaches `10¹⁴` — well outside `int`. Use `long[]`. This is the same bug class as Bloch's overflow in binary search: silent, sometimes returns negative garbage. **Rule: if `Σa[i]` might exceed `2·10⁹`, prefix sums must be `long`.**

> [trap] **Trap 4 — Difference array's `r+1` bound is out of range.** For `diff[r+1]` where `r == n-1`, `r+1 == n` — you must allocate `diff` of size `n+1`, not `n`. Off-by-one array-out-of-bounds is a runtime crash the interviewer sees clearly.

> [trap] **Trap 5 — Trying to reuse a prefix sum after mutating the input.** Prefix sums are a **snapshot**. If you modify `a[]` after building `pre[]`, every subsequent query returns stale data. In a follow-up "now support point updates" question, migrate to a Fenwick tree instead of hoping to patch `pre[]` in place.

## History — Blelloch's parallel prefix, 1990

The prefix-sum operation was formalized by **Guy Blelloch** at CMU in his 1990 paper *"Prefix Sums and Their Applications."* The paper proved that prefix sum — despite looking inherently sequential — could be **parallelized** to O(log n) depth using `n` processors via a "work-efficient" tree-reduction pattern. That algorithm became the foundation of **CUDA's `thrust::inclusive_scan`** and every modern GPU primitive for reductions, sorting, and histogram-building.

Every time you `git diff` and see a fast enumeration of changed lines, or your ML framework runs an `argmax` reduction across 10⁴ GPU cores, you're seeing Blelloch's algorithm in action. In interviews, dropping the phrase *"the parallel-prefix-scan variant"* signals depth beyond LeetCode.

The difference-array trick appears informally in Knuth's *Art of Computer Programming* Vol 1 (1968), but the modern interview form — turning `Q` range updates into a single O(n) pass — was popularized on TopCoder and Codeforces in the mid-2000s.

## Canonical problem walkthrough — Subarray Sum Equals K

**Problem** ([↗ LeetCode](https://leetcode.com/problems/subarray-sum-equals-k/)): Given an integer array `nums` and integer `k`, return the number of contiguous subarrays whose sum equals `k`. Values can be negative.

### Approach 1 — Brute force

Two nested loops. For each start `i`, extend to each `j ≥ i` and check if the sum equals `k`.

```java
int subarraySumBrute(int[] nums, int k) {
    int count = 0;
    for (int i = 0; i < nums.length; i++) {
        int sum = 0;
        for (int j = i; j < nums.length; j++) {
            sum += nums[j];
            if (sum == k) count++;
        }
    }
    return count;
}
```

**Complexity:** O(n²) time, O(1) space. For `n = 2·10⁴`, that's `4·10⁸` operations — tight but might squeak by LeetCode's 2-second limit. Interviewer smiles thinly.

### Approach 2 — Prefix sums with linear scan for pair search

Build `pre[]`, then for each `r`, scan all `l ≤ r` looking for `pre[l] == pre[r+1] - k`.

```java
int subarraySumTwoLoop(int[] nums, int k) {
    int n = nums.length;
    long[] pre = new long[n + 1];
    for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + nums[i];
    int count = 0;
    for (int r = 0; r < n; r++)
        for (int l = 0; l <= r; l++)
            if (pre[r + 1] - pre[l] == k) count++;
    return count;
}
```

**Complexity:** still O(n²), but the inner check is O(1) instead of accumulating a fresh sum. Slightly faster constant factor. Not the point — this is a stepping stone showing you've *identified* prefix sum but haven't yet hashed.

### Approach 3 — Prefix sums with hash map (the interview answer)

The key insight: for each new position `r`, we want to count how many earlier prefixes `pre[l]` satisfy `pre[l] == pre[r+1] - k`. That's a **lookup**, not a scan — so use a HashMap.

```java
int subarraySum(int[] nums, int k) {
    Map<Long, Integer> seen = new HashMap<>();
    seen.put(0L, 1);                        // empty prefix — one occurrence of "sum 0 so far"
    long running = 0;
    int count = 0;
    for (int x : nums) {
        running += x;
        count += seen.getOrDefault(running - k, 0);      // how many earlier prefixes complete a k-subarray?
        seen.merge(running, 1, Integer::sum);            // record the current prefix
    }
    return count;
}
```

**Complexity:** O(n) time (one pass, O(1) hash ops), O(n) space (worst-case, every prefix distinct).

**Interview commentary:**
- *"Brute force is O(n²). I can do better."*
- *"For each index r, a subarray ending at r has sum k iff `pre[r+1] - pre[l] = k` for some earlier `l`. That means `pre[l] = pre[r+1] - k`."*
- *"So keep a HashMap of prefix sums seen so far. At each r, look up how many earlier positions had the required prefix value."*
- *"O(n) time and space. The `put(0, 1)` handles the case where a subarray from index 0 sums to k."*

### Complexity ladder

| Approach | Time | Space | When |
|---|---|---|---|
| Brute force | O(n²) | O(1) | Reference / very small n |
| Prefix + scan | O(n²) | O(n) | Stepping stone during whiteboard |
| **Prefix + HashMap** | **O(n)** | **O(n)** | **Interview default** |

---



### Recognize by
- many range-sum queries over a static array — precompute pre[], each query is O(1)
- "count subarrays with sum k" (with hash map, works for negative values too)
- "range-update, point-query" — the difference-array mirror

### When NOT to use it
You need to *update* array values *and* query ranges in the same run — a plain prefix sum is O(1) query but O(n) update. For both operations in O(log n), reach for [Fenwick / segment tree](#segment-tree-fenwick-tree).

---

## Subarray Sum Equals K <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/)*

<ProgressCheck id="subarray-sum-equals-k" />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
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
```

<div class="readfig"><b>How to read it:</b> The subarray <b>[2,3]</b> is found by subtracting an earlier prefix from the current prefix; the hashmap version counts how often <code>prefix - k</code> has appeared.</div>

### Problem
Count how many **contiguous subarrays** sum exactly to `k`. The array may contain **negative** numbers — which is what rules out a sliding window.

**Constraints:** `1 ≤ n ≤ 2·10⁴`; values and `k` fit in `int`; negatives allowed.

**Example 1:** `nums = [1,2,1,2,1], k = 3` → `4`.

<ExamplePreview compact :input="['1', '2', '1', '2', '1', '|', '3']" :output="['4']" />

**Example 2:** `nums = [1,-1,0], k = 0` → `3` (`[1,-1]`, `[1,-1,0]`, and `[0]`).

<ExamplePreview compact :input="['1', '-1', '0', '|', '0']" :output="['3']" />

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

> [inv] **Invariant** — `count` maps each prefix-sum value to how many indices produced it among the processed prefix. At index `r`, the number of valid `l` is `count[pre - k]`.

> [note] **Trace it** — `a=[1,2,1,2,1], k=3`. Running prefixes `0,1,3,4,6,7`. Each time `pre−3` was seen before, you found a subarray: pairs give `[1,2],[2,1],[1,2],[2,1]` → **4**.

> [trap] **Common Trap** — Forgetting the `count.put(0,1)` seed drops subarrays that start at index 0. Do **not** use a sliding window here — negatives destroy the monotonic shrink.


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

> [pat] **Pattern Connection** — The shared idea is **charge a subarray-with-a-target-property to its prefix**: a subarray `(l,r]` has the property iff two prefixes differ by the target, so you store seen prefixes in a map. Recognize it in *Contiguous Array* (map a 0/1 array's ±1 running sum to the first index it appeared — a balanced subarray means equal prefixes) and *Subarray Sums Divisible by K* (bucket prefixes by `pre mod k`; two prefixes in the same bucket bound a divisible subarray). The transfer trick: rephrase "count subarrays where X" as "count prefix pairs that differ by X."

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

<ExamplePreview compact :input="['3']" :output="['1', '1', '5']" />

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

> [key] **Key Insight** — Batch many range increments in O(1) each, then reconstruct in O(n). Ideal when all updates precede all queries.

> [inv] **Invariant** — After processing, `prefix(diff)[i]` equals the net of all increments covering index `i`.

> [note] **Trace it** — `n=5`, bookings `[1,2,10],[2,3,20],[2,5,25]`. Endpoint marks then one prefix pass → per-flight seats `[10,55,45,25,25]` — three range adds settled in one sweep.

> [trap] **Common Trap** — Off-by-one at `r+1`; size the array `n+1` so the closing decrement never overflows the bounds.


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

> [pat] **Pattern Connection** — 2D difference arrays handle sub-rectangle increments; combined with a 2D prefix sum they answer *Range Sum Query 2D* in O(1) per query.

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

<ExamplePreview compact :input="['[[5]]']" :output="['5']" />

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

> [key] **Key Insight** — Inclusion–exclusion: `sum(r1,c1,r2,c2) = P[r2+1][c2+1] − P[r1][c2+1] − P[r2+1][c1] + P[r1][c1]`.

> [note] **Trace it** — `m=[[3,1],[2,4]]`. The padded prefix table gives `sumRegion(0,0,1,1) = P[2][2] − P[0][2] − P[2][0] + P[0][0] = 10 − 0 − 0 + 0 = 10` (the whole grid), and `sumRegion(1,1,1,1)=4` (just the corner).

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

> [inv] **Invariant** — `P[i][j]` holds the sum of the sub-rectangle from `(0,0)` to `(i-1,j-1)`; the padding row/column of zeros makes every query boundary-safe.

> [trap] **Common Trap** — Sign/index errors in the four-term formula, or omitting the `+1` padding — then corner queries read out of bounds. Add back the double-subtracted corner (`+ P[r1][c1]`).

> [pat] **Pattern Connection** — The +/−/− /+ inclusion–exclusion pattern reappears in *Maximal Rectangle* accounting and 2D sweep problems.

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Matrix Block Sum](https://leetcode.com/problems/matrix-block-sum/) | answer each cell as the sum of a `k`-radius block using the same four-corner formula | — |
| [Count Submatrices With Target Sum](https://leetcode.com/problems/count-submatrices-with-target-sum/) | fix a pair of rows, collapse columns to 1D prefix sums, then reuse the "subarray sum = k" hash-map count | — |
| [Maximal Square / Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | combine per-row prefix counts with a histogram/DP to bound the largest all-ones region | — |

---

## Check your understanding

<Quiz
  pattern-id="prefix-sum"
  :questions='[{"q": "What does `count[preSum - k]` count in Subarray Sum Equals K?", "choices": [{"text": "Number of subarrays ending at current index with sum k", "correct": true, "explanation": "Every earlier prefix with value `preSum - k` gives a valid subarray."}, {"text": "Total number of elements less than k", "correct": false}, {"text": "Number of prefixes divisible by k", "correct": false}, {"text": "Number of distinct values in nums", "correct": false}]}, {"q": "When using prefix mod k, why initialize `count[0] = 1`?", "choices": [{"text": "To count subarrays starting from index 0", "correct": true, "explanation": "The \"prefix sum before index 0\" is 0; without this, subarrays sum-to-k starting at 0 are missed."}, {"text": "To handle negative numbers", "correct": false}, {"text": "It is required by Java", "correct": false}, {"text": "To avoid null exceptions", "correct": false}]}, {"q": "For range-add + point-query, what is the O(1)-per-add data structure?", "choices": [{"text": "Segment tree", "correct": false, "explanation": "Works but O(log n) per op — overkill if only one final scan."}, {"text": "Difference array (then prefix sum at the end)", "correct": true, "explanation": "O(1) per add; one O(n) prefix sweep to recover values."}, {"text": "Hash map", "correct": false}, {"text": "BIT / Fenwick tree", "correct": false, "explanation": "Works but heavier than needed."}]}, {"q": "In Contiguous Array (equal 0s and 1s), what mapping enables prefix sum?", "choices": [{"text": "Map 0 → -1 and 1 → +1; equal counts iff prefix returns to a prior value", "correct": true, "explanation": "Same prefix twice → the delta is 0 → equal 0s and 1s."}, {"text": "Sort the array", "correct": false}, {"text": "Use bitwise XOR", "correct": false}, {"text": "Impossible in O(n)", "correct": false}]}, {"q": "Time to answer any 2D rectangle-sum query after O(mn) preprocessing?", "choices": [{"text": "O(1)", "correct": true, "explanation": "Inclusion-exclusion on the 2D prefix table."}, {"text": "O(log(mn))", "correct": false}, {"text": "O(m + n)", "correct": false}, {"text": "O(mn)", "correct": false}]}]'
/>

<PrintButton />

<RelatedPatterns pattern-id="prefix-sum" />
