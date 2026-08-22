# Binary Search on the Answer

The motivating problem is usually something like: "What is the minimum speed/capacity/threshold that works?" Brute force tries every possible answer and runs the checker each time, which becomes impossible when the answer range goes up to `10⁹`.

Can we do better? If a candidate answer works, every larger candidate usually works too. That one-way yes/no behavior gives you a sorted boolean array over the answer space: `false, false, true, true`.

You know the answer lies in a numeric range — a capacity, a speed, a threshold — and a boolean test `feasible(x)` flips false -&gt; true exactly once as x grows. Binary-search that flip point. Each test is often O(n), so total O(n log range).

<Callout kind="key" title="Key Insight">

The technique doesn't search *values* in an array; it searches the *answer space*. What makes it work is monotonicity of `feasible(x)`.

</Callout>

### Recognize by
- "minimum X such that…" / "maximum X such that…"
- you can *check* a candidate x in linear time but *searching* every x is too slow
- phrases like "minimum capacity to ship in D days", "slowest speed to finish", "largest minimum gap"

### When NOT to use it
The feasibility predicate isn't monotone — you can find an x where `feasible(x)` is true but `feasible(x+1)` is false. Then you're not searching a single flip point; the search space has multiple boundaries and this technique gives the wrong answer.

---

## Koko Eating Bananas (Search on Answer — rate) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/)*

<ProgressCheck id="koko-eating-bananas-search-on-answer-rate" />





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="27" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">binary search over the answer: eating rate k</text>
  <line x1="48" y1="72" x2="352" y2="72" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <circle cx="58" cy="72" r="6" fill="var(--dsa-primary)"/>
  <circle cx="342" cy="72" r="6" fill="var(--dsa-primary)"/>
  <line x1="202" y1="49" x2="202" y2="153" stroke="var(--dsa-primary)" stroke-width="2" stroke-dasharray="6 5"/>
  <text x="58" y="52" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">low=1</text>
  <text x="342" y="52" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">high=max</text>
  <text x="202" y="43" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">mid k=4</text>
  <text x="200" y="92" text-anchor="middle" font-size="11.5" fill="var(--dsa-neutral)">rate k</text>
  <g text-anchor="middle">
    <rect x="82" y="114" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <rect x="134" y="114" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <rect x="186" y="114" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
    <rect x="238" y="114" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <g font-size="17" font-weight="700" fill="var(--dsa-ink)">
      <text x="104" y="142">3</text><text x="156" y="142">6</text><text x="208" y="142">7</text><text x="260" y="142">11</text>
    </g>
    <g font-size="11" fill="var(--dsa-neutral)">
      <text x="104" y="173">1h</text><text x="156" y="173">2h</text><text x="208" y="173">2h</text><text x="260" y="173">3h</text>
    </g>
  </g>
  <rect x="100" y="186" width="200" height="28" rx="10" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <text x="200" y="205" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-success)">hours = 1+2+2+3 = 8 ≤ h=8</text>
  <text x="200" y="234" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">monotone predicate: feasible(k) is non-decreasing in k</text>
</svg>
</div>




<div class="readfig"><b>How to read it:</b> Guess a rate, compute total hours with ceiling division, then use the yes/no result to keep the smallest feasible side of the search range.</div>

### Problem
Koko eats `k` bananas/hour (one pile per hour; leftovers still cost a full hour). Find the **minimum `k`** that finishes all piles within `h` hours.

**Constraints:** `1 ≤ piles.length ≤ 10⁴`; `piles.length ≤ h ≤ 10⁹`; pile sizes up to 10⁹.

**Example 1:** `piles = [3,6,7,11], h = 8` → `4`.

**Example 2:** `piles = [30,11,23,4,20], h = 5` → `30`.

### Solution — brute force
Brute force tries every eating speed `k` from 1 up to the largest pile and simulates the total hours for each speed. The feasibility check is O(n), so this is O(n·maxPile) time and O(1) space, far too slow when pile sizes hit `10⁹`. The optimized version keeps the same feasibility check but binary-searches the monotone speed range for the first speed that works.



```java
int minEatingSpeedBrute(int[] piles, int h) {
    int max = 0;
    for (int p : piles) max = Math.max(max, p);
    for (int k = 1; k <= max; k++) {
        long hours = 0;
        for (int p : piles) hours += (p + k - 1) / k;
        if (hours <= h) return k;
    }
    return max;
}
```



O(n·maxPile) time, O(1) space — too slow when pile sizes can be 10⁹.

### Solution — optimized
Binary search the *eating speed*; feasibility "can finish within h hours at speed k" is monotone in k.

<Callout kind="inv" title="Invariant">

`feasible(k)` true ⇒ `feasible(k+1)` true. Find the minimum feasible k = first-true boundary over `[1, max(pile)]`.

</Callout>

The optimized version keeps the O(n) simulation but runs it only for O(log maxPile) guessed speeds. A feasible speed means "try slower"; an infeasible speed means "must go faster."



```java
int minEatingSpeed(int[] piles, int h) {
    int lo = 1, hi = 0;
    for (int p : piles) hi = Math.max(hi, p);
    while (lo < hi) {
        int k = lo + (hi - lo) / 2;
        long hours = 0;
        for (int p : piles) hours += (p + k - 1) / k;   // ceil division
        if (hours <= h) hi = k; else lo = k + 1;        // feasible -> go slower
    }
    return lo;
}
```



<Callout kind="note" title="Trace it">

`piles=[3,6,7,11], h=8`. Speed 4 takes `1+2+2+3 = 8` hours (feasible); speed 3 takes 10 (too slow). Binary search on speed lands on **4**.

</Callout>

### Time Complexity
O(n log(maxPile)), because each feasibility check scans all piles once, and binary search performs O(log maxPile) checks.

### Space Complexity
O(1), because the search stores only bounds and the running `hours` counter.

<Callout kind="note" title="Interview script">

"I first confirm Koko chooses one integer speed and every partially eaten pile still costs a full hour. I start with brute force by trying every speed and simulating hours, which is O(n·maxPile) time and O(1) space. I optimize by binary-searching the first feasible speed, using the same O(n) check, for O(n log maxPile) time and O(1) space."

</Callout>


<Callout kind="key" title="Key Insight">

The moment you see "minimum speed/capacity/time such that a constraint holds," define `feasible(x)` as an O(n) check and binary-search x. The array order is irrelevant; the *answer* is what's monotone.

</Callout>

<Callout kind="trap" title="Common Trap">

Feasibility direction flipped. *Example:* `piles=[3,6,7,11]`, `h=8`. If `feasible(speed)` returns `true` when speed is too slow, binary search converges to the fastest failing speed. Sanity-check: `feasible(min)` should be `false` and `feasible(max)` should be `true`.

</Callout>

<Callout kind="pat" title="Pattern Connection">

Identical structure to *Capacity to Ship Packages in D Days* (feasibility on capacity) and *Minimize Max Distance to Gas Station*.

</Callout>

### Learning notes
- Why `lo = 1`? — speed zero is invalid, and the slowest possible positive speed is 1 banana/hour.
- Why `hi = max(pile)`? — at that speed, every pile finishes in one hour, so it is always feasible.
- Why `(p + k - 1) / k`? — integer ceil division counts a partially eaten pile as a full hour.
- Why `long hours`? — total hours can exceed `int` while summing many large piles.
- Why `hi = k` on feasible? — `k` might be the minimum working speed, so keep it in the search range.
- Why `lo = k + 1` on infeasible? — if speed `k` is too slow, every smaller speed is also too slow.

### Same pattern, new tweaks

"Guess an answer, check feasibility in O(n), binary-search the threshold" — only the feasibility test changes:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Capacity to Ship Packages in D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | guess a ship capacity; feasibility = "can we finish in ≤ D days at this capacity?" | — |
| [Split Array Largest Sum / Book Allocation](https://leetcode.com/problems/split-array-largest-sum/) | guess a max segment sum; feasibility = "≤ m parts needed?" | — |
| [Minimize Max Distance to Gas Station](https://leetcode.com/problems/minimize-max-distance-to-gas-station/) | guess a distance; feasibility counts how many stations you'd have to add (works on real numbers, so fix an iteration count or epsilon) | — |

## Split Array Largest Sum / Book Allocation (Search on Answer — partition) <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/)*

<ProgressCheck id="split-array-largest-sum-book-allocation-search-on-answer-partition" />

### Problem
Split the array into `m` **contiguous** subarrays so as to **minimize the largest** subarray sum.

**Constraints:** `1 ≤ n ≤ 1000`; `1 ≤ m ≤ n`; values `≥ 0`, sums up to ~10⁹.

**Example 1:** `[7,2,5,10,8], m = 2` → `18` (split `[7,2,5] | [10,8]`).

**Example 2:** `[1,2,3,4,5], m = 2` → `9` (split `[1,2,3] | [4,5]`).

### Solution — brute force
Brute force enumerates every way to place `m-1` cuts between elements, computes the largest segment sum for that partition, and keeps the minimum. There are exponentially many cut patterns (or combinatorially many for fixed `m`), so it is correct but not scalable. The optimized view guesses the largest allowed segment sum and greedily counts how many parts are needed, then binary-searches the smallest feasible cap.



```java
int splitArrayBrute(int[] a, int m) {
    return splitDfs(a, 0, m);
}
int splitDfs(int[] a, int start, int parts) {
    if (parts == 1) {
        int sum = 0;
        for (int i = start; i < a.length; i++) sum += a[i];
        return sum;
    }
    int best = Integer.MAX_VALUE, cur = 0;
    for (int cut = start; cut <= a.length - parts; cut++) {
        cur += a[cut];
        best = Math.min(best, Math.max(cur, splitDfs(a, cut + 1, parts - 1)));
    }
    return best;
}
```



Exponential time over cut placements, O(m) recursion space — too slow beyond small n.

### Solution — optimized
Binary search the *maximum allowed segment sum*; feasibility "can partition into ≤ m parts with each part ≤ cap" is monotone in cap and checked greedily.

<Callout kind="key" title="Key Insight">

Larger cap ⇒ fewer required parts (monotone). `lo = max(element)` (a part must hold its largest element), `hi = sum(all)`. Answer = smallest cap needing ≤ m parts.

</Callout>

The optimized version guesses the largest allowed subarray sum. For a fixed cap, the greedy scan starts a new segment only when adding the next value would exceed the cap; if that needs at most `m` parts, try a smaller cap.



```java
int splitArray(int[] a, int m) {
    long lo = 0, hi = 0;
    for (int x : a) { lo = Math.max(lo, x); hi += x; }
    while (lo < hi) {
        long cap = lo + (hi - lo) / 2;
        if (partsNeeded(a, cap) <= m) hi = cap; else lo = cap + 1;
    }
    return (int) lo;
}
int partsNeeded(int[] a, long cap) {
    int parts = 1; long cur = 0;
    for (int x : a) {
        if (cur + x > cap) { parts++; cur = x; }   // start new segment
        else cur += x;
    }
    return parts;
}
```



<Callout kind="note" title="Trace it">

`[7,2,5,10,8], m=2`. Cap 18 works: `[7,2,5] | [10,8]` = sums `14, 18`. Any smaller cap forces 3+ parts → answer **18**.

</Callout>

### Time Complexity
O(n log(sum)), where `sum` is the total array sum. Each feasibility check is O(n), and binary search spans from max element to total sum.

### Space Complexity
O(1), because the optimized algorithm uses only bounds and the current segment sum.

<Callout kind="note" title="Interview script">

"I first confirm subarrays must be contiguous and I need to minimize the maximum segment sum. I start with brute force by trying all cut placements, which is exponential in the number of gaps for variable `m`. I optimize by binary-searching the answer between max element and total sum, with an O(n) greedy feasibility check, for O(n log sum) time and O(1) space."

</Callout>


<Callout kind="trap" title="Common Trap">

Wrong feasibility semantics. *Example:* `nums=[7,2,5,10,8]`, `m=2`. `feasible(cap)` asks *"can we split into ≤ m subarrays, each with sum ≤ cap?"*. Confusing it with *"exactly m"* misclassifies boundaries and the search settles on the wrong split.

</Callout>

<Callout kind="pat" title="Pattern Connection">

"Minimize the maximum" (or "maximize the minimum") ⇒ almost always binary search on the answer with a greedy feasibility check. This is a top-5 staff-interview signal.

</Callout>

### Learning notes
- Why `lo = max(element)`? — no segment cap can be smaller than the largest single number.
- Why `hi = sum(all)`? — one segment containing the whole array is always feasible.
- Why use `long` for `lo`, `hi`, and `cap`? — sums can exceed 32-bit `int`.
- Why start `parts = 1`? — before any cut, the first segment already exists.
- Why cut when `cur + x > cap`? — that is the first moment the current segment would violate the guessed cap.
- Why `partsNeeded <= m` works? — if you can do it in fewer than `m` parts, you can split some non-empty segment further because values are non-negative.

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Capacity to Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | guess a ship capacity; feasibility = "≤ D days?" | — |
| [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | guess a speed; feasibility = "finishes within H hours?" | — |
| [Divide Chocolate / Maximize the Minimum](https://leetcode.com/problems/divide-chocolate/) | flip it — maximize the smallest piece, so `feasible(x)` = "can make ≥ k pieces each ≥ x." | — |
| [Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) | binary-search the max allowed step height; feasibility is a BFS/DFS connectivity check | — |

## Median of Two Sorted Arrays (Partition Binary Search) <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/)*

<ProgressCheck id="median-of-two-sorted-arrays-partition-binary-search" />

### Problem
Given two sorted arrays, find the **median** of their combined elements in **O(log(m+n))**.

**Constraints:** `0 ≤ m, n ≤ 1000`; combined length `≥ 1`; must be logarithmic (merging is too slow).

**Example 1:** `[1,3]` and `[2]` → `2.0`.

**Example 2:** `[1,2]` and `[3,4]` → `2.5`.

### Solution — brute force
Brute force merges the two sorted arrays until the median position, or fully merges them and reads the middle. That is O(m+n) time and O(1) space if you stop early, or O(m+n) extra space for a full merged array. The optimized solution avoids merging by binary-searching a partition of the smaller array so the combined left half and right half are ordered correctly.



```java
double findMedianSortedArraysBrute(int[] A, int[] B) {
    int total = A.length + B.length;
    int need = total / 2;
    int i = 0, j = 0, prev = 0, cur = 0;
    for (int step = 0; step <= need; step++) {
        prev = cur;
        if (j == B.length || (i < A.length && A[i] <= B[j])) cur = A[i++];
        else cur = B[j++];
    }
    if ((total & 1) == 1) return cur;
    return (prev + cur) / 2.0;
}
```



O(m+n) time, O(1) space — too slow for the required logarithmic bound.

### Solution — optimized
Binary search a *partition* of the smaller array so that left halves of both arrays form the lower half of the merged array.

<Callout kind="key" title="Key Insight">

Choose `i` in A and `j = half − i` in B so that `A[i-1] ≤ B[j]` and `B[j-1] ≤ A[i]`. That single condition means everything left ≤ everything right → the median sits at the boundary. Binary-search `i` on the shorter array for O(log min(m,n)).

</Callout>

<Callout kind="inv" title="Invariant">

`i + j = (m+n+1)/2` keeps the left partition sized for the median; adjust `i` up/down based on which cross-boundary inequality fails.

</Callout>

The optimized version does not merge values; it searches for the split point where the left side has exactly half the combined elements and every left value is ≤ every right value. Sentinels make empty partitions behave like `-∞` and `+∞`.

#### Steps
1. Ensure `nums1` is the shorter array (swap if not) — keeps the binary-search range small.
2. Binary-search `i` over `[0, m]`; set `j = (m + n + 1) / 2 - i`.
3. Boundary values: `L1 = i > 0 ? nums1[i-1] : -∞`; `R1 = i < m ? nums1[i] : +∞`. Symmetric for `L2, R2`.
4. If `L1 <= R2 && L2 <= R1` — partition is correct.
5. If `L1 > R2` — `i` is too big; shrink `hi = i - 1`. Else `lo = i + 1`.
6. Once partitioned: odd total → `max(L1, L2)`; even → `(max(L1,L2) + min(R1,R2)) / 2.0`.

The optimized Java implementation:


```java
double findMedianSortedArrays(int[] A, int[] B) {
    if (A.length > B.length) return findMedianSortedArrays(B, A);
    int m = A.length, n = B.length, half = (m + n + 1) / 2;
    int lo = 0, hi = m;
    while (lo <= hi) {
        int i = lo + (hi - lo) / 2, j = half - i;
        int aL = i == 0 ? Integer.MIN_VALUE : A[i-1];
        int aR = i == m ? Integer.MAX_VALUE : A[i];
        int bL = j == 0 ? Integer.MIN_VALUE : B[j-1];
        int bR = j == n ? Integer.MAX_VALUE : B[j];
        if (aL <= bR && bL <= aR) {                     // correct partition
            if (((m + n) & 1) == 1) return Math.max(aL, bL);
            return (Math.max(aL, bL) + Math.min(aR, bR)) / 2.0;
        } else if (aL > bR) hi = i - 1;                 // too many from A
        else                lo = i + 1;
    }
    return 0.0;
}
```



<Callout kind="note" title="Trace it">

`[1,3]` and `[2]` (total length 3, odd). The correct partition puts `{1,2}` on the left and `{3}` on the right; the median is the max of the left = **2**.

</Callout>

### Time Complexity
O(log min(m,n)), because binary search runs only over the shorter array's partition index.

### Space Complexity
O(1), because the algorithm stores boundary indices and values without building a merged array.

<Callout kind="note" title="Interview script">

"I first confirm both arrays are sorted and the combined length is at least one. I start with brute force by merging up to the median, which is O(m+n) time and O(1) space if streamed. I optimize by binary-searching the partition on the smaller array, giving O(log min(m,n)) time and O(1) space."

</Callout>


<Callout kind="trap" title="Common Trap">

Off-by-one when the total length is odd. *Example:* `A=[1]`, `B=[2,3]`. Left partition should hold `(m+n+1)/2 = 2` elements — the median is the `max` of that left side. Using `(m+n)/2` puts the median on the wrong side.

</Callout>

### Learning notes
- **Not shortening the shorter array first** — the binary search range should be the smaller of `m`, `n`.
- **Off-by-one in the left-half size** — use `(m + n + 1) / 2` so the median lives on the left when odd.
- **Missing the `±∞` sentinels** for empty halves — use `Integer.MIN/MAX_VALUE`.
- **Averaging as ints** for even-total median — divide by `2.0` (return `double`).
- Why `j = half - i`? — once A contributes `i` elements to the left, B must contribute the rest.
- Why two inequalities `aL <= bR && bL <= aR`? — together they prove every left-side value is ≤ every right-side value.
- Why `hi = i - 1` when `aL > bR`? — A contributed too many large elements to the left partition.

<Callout kind="pat" title="Pattern Connection">

Partition binary search — the most sophisticated member of the family; demonstrates that binary search operates on *structural boundaries*, not just values.

</Callout>

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Kth Element of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | the general form — binary-search a partition so `k` elements sit on the left | — |
| [Median of a Row-wise Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) | binary-search the value and count how many are ≤ mid | — |
| [Find K-th Smallest Pair Distance](https://leetcode.com/problems/find-k-th-smallest-pair-distance/) | binary-search the distance; feasibility counts pairs within it via a sliding window | — |

---

## Check your understanding

<Quiz patternId="bs-on-answer" :questions='[
  {
    "q": "A problem asks for the minimum speed that finishes within h hours. Which pattern fits?",
    "choices": [
      {
        "text": "Binary search on answer",
        "correct": true,
        "explanation": "Yes. Feasible speed is monotone: once fast enough, any higher speed also works."
      },
      {
        "text": "Merge intervals"
      },
      {
        "text": "Fast and slow pointers"
      },
      {
        "text": "Backtracking"
      }
    ]
  },
  {
    "q": "For Koko-style speed search, what should feasible(speed) mean?",
    "choices": [
      {
        "text": "True when speed is too slow",
        "explanation": "That flips the boundary and moves the search the wrong way."
      },
      {
        "text": "True when all piles finish in time",
        "correct": true,
        "explanation": "Correct. The search then finds the smallest speed on the true side."
      },
      {
        "text": "True only at the exact answer"
      },
      {
        "text": "True when piles are sorted"
      }
    ]
  },
  {
    "q": "For Split Array Largest Sum, what are tight initial bounds for capacity?",
    "choices": [
      {
        "text": "zero and array length"
      },
      {
        "text": "minimum element and maximum element"
      },
      {
        "text": "max element and total sum",
        "correct": true,
        "explanation": "Right. A part must hold the largest element; one part may hold everything."
      },
      {
        "text": "target and target squared"
      }
    ]
  }
]' />
