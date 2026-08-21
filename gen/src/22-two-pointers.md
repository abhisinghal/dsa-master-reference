# Two Pointers

Instead of checking every pair with two nested loops (that's O(n²)), you keep **two indices** and move them cleverly so each step rules out a whole batch of pairs at once. The trick almost always leans on the array being **sorted** — that order is what tells you *which* pointer to move.

Say the array is sorted and you want two numbers that add up to a target. Put one pointer at each end and look at their sum:

- too **big**? the large end is the culprit — move the right pointer **left** to a smaller value.
- too **small**? move the left pointer **right** to a bigger value.
- **just right**? you found the pair.

Every move discards a number you've *proven* can't help, so you sweep the array once — O(n) instead of O(n²).

```svg
<svg width="720" height="200" viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <defs>
    <marker id="tp-g" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#16a34a"/></marker>
    <marker id="tp-r" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#dc2626"/></marker>
    <filter id="tp-s" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.5"/></filter>
  </defs>
  <rect x="0" y="0" width="720" height="200" fill="#fbfcfe"/>
  <text x="20" y="28" font-size="13" font-weight="700" fill="#2563eb">sorted array — find two numbers summing to 9</text>

  <g filter="url(#tp-s)">
    <rect x="18"  y="54" width="54" height="42" rx="7" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.6"/>
    <rect x="82"  y="54" width="54" height="42" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="146" y="54" width="54" height="42" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="210" y="54" width="54" height="42" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="274" y="54" width="54" height="42" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="338" y="54" width="54" height="42" rx="7" fill="#fef2f2" stroke="#dc2626" stroke-width="1.6"/>
  </g>
  <g font-size="19" font-weight="700" fill="#0b1220" text-anchor="middle">
    <text x="45"  y="82">1</text><text x="109" y="82">3</text><text x="173" y="82">5</text>
    <text x="237" y="82">6</text><text x="301" y="82">8</text><text x="365" y="82">11</text>
  </g>
  <g font-size="11" fill="#94a3b8" text-anchor="middle">
    <text x="45" y="112">0</text><text x="109" y="112">1</text><text x="173" y="112">2</text>
    <text x="237" y="112">3</text><text x="301" y="112">4</text><text x="365" y="112">5</text>
  </g>

  <line x1="45"  y1="150" x2="45"  y2="100" stroke="#16a34a" stroke-width="2" marker-end="url(#tp-g)"/>
  <text x="45"  y="168" text-anchor="middle" font-size="12" font-weight="700" fill="#16a34a">lo</text>
  <line x1="365" y1="150" x2="365" y2="100" stroke="#dc2626" stroke-width="2" marker-end="url(#tp-r)"/>
  <text x="365" y="168" text-anchor="middle" font-size="12" font-weight="700" fill="#dc2626">hi</text>

  <rect x="440" y="52" width="264" height="92" rx="9" fill="#f6f8fb" stroke="#d9dee7"/>
  <text x="456" y="76" font-size="13" font-weight="700" fill="#0b1220">a[lo] + a[hi] = 1 + 11 = 12</text>
  <text x="456" y="100" font-size="13" fill="#dc2626">12 &gt; 9  →  too big, move hi ◀ left</text>
  <text x="456" y="124" font-size="12" fill="#334155">(now 1 + 8 = 9  ✓  found it)</text>
</svg>
```
<div class="readfig"><b>How to read it:</b> The green <b>lo</b> pointer starts at the smallest value, the red <b>hi</b> at the largest. Their sum here is 12, which overshoots 9 — and since everything to the left of <b>hi</b> is smaller, the only way to shrink the sum is to pull <b>hi</b> inward. One step later, <code>1 + 8 = 9</code>. Each move permanently eliminates one number, so the two pointers meet in the middle after a single O(n) sweep.</div>

There are three flavours of this idea: **converging** (from both ends, like above), **same-direction** (a fast reader and a slow writer, for in-place compaction), and **partition** (the Dutch-flag three-way split).

> [key] **Key Insight** — On a *sorted* array, if `a[lo]+a[hi]` is too big, no pair using `hi` can be smaller, so `hi--` discards a whole column safely. Each step eliminates one row or column of the pair matrix ⇒ O(n).

### Recognize by
- sorted array + "find pair / triplet summing to X"
- "partition" / "in-place two-value split" — Dutch National Flag, Sort Colors
- palindrome check, container-with-most-water, trapping rain water (two-pointer variant)

### When NOT to use it
The array **isn't sorted** and you can't afford to sort it (O(n log n) prep) — try a hash-map approach instead. Or the problem needs a *contiguous window* rather than a boundary discard — that's [Sliding Window](#sliding-window).

---

## 3Sum
*[↗ LeetCode: 3Sum](https://leetcode.com/problems/3sum/)*

### Problem
Find **all unique triplets** `(a, b, c)` in the array with `a + b + c = 0`. The output must contain no duplicate triplets.

**Constraints:** `3 ≤ n ≤ 3000`; values fit in `int`; the array is unsorted (you'll sort it first).

**Example:** `[-1,0,1,2,-1,-4]` → `[[-1,-1,2],[-1,0,1]]`.

### Brute force
Brute force is three nested loops over `i < j < k`, checking every triplet and putting sorted triplets into a set to avoid duplicates. That is O(n³) time plus output/dedup space, and it times out quickly at `n = 3000`. Sorting first lets us fix one value and replace the inner pair scan with two pointers, cutting the search to O(n²) while still skipping duplicates deterministically.

### Pattern
Sort, fix one element, converge two pointers for the remaining pair; skip duplicates at every level.

> [inv] **Invariant** — For fixed `i`, `[lo,hi]` brackets all unexplored pairs summing toward `-a[i]`; sortedness makes each move monotone.

### Steps
1. Sort the array — sortedness lets us prune and two-pointer.
2. Loop `i` over each element as the outer pivot. Skip duplicate pivots: `if (i > 0 && a[i] == a[i-1]) continue;`.
3. For each pivot, set `lo = i+1`, `hi = n-1`; hunt pairs summing to `-a[i]`.
4. If `s < 0` → `lo++`; if `s > 0` → `hi--`; if `s == 0` → record the triplet.
5. After a hit, skip duplicates on **both** pointers before advancing: `while (a[lo]==a[lo+1]) lo++;` and mirror for `hi`.
6. Break early when `a[i] > 0` — no positive triple sums to zero.

### Java
```java
List<List<Integer>> threeSum(int[] a) {
    Arrays.sort(a);
    List<List<Integer>> res = new ArrayList<>();
    for (int i = 0; i < a.length - 2; i++) {
        if (i > 0 && a[i] == a[i-1]) continue;               // skip dup pivot
        if (a[i] > 0) break;                                  // smallest already positive
        int lo = i + 1, hi = a.length - 1;
        while (lo < hi) {
            int s = a[i] + a[lo] + a[hi];
            if (s == 0) {
                res.add(List.of(a[i], a[lo], a[hi]));
                while (lo < hi && a[lo] == a[lo+1]) lo++;      // skip dup
                while (lo < hi && a[hi] == a[hi-1]) hi--;
                lo++; hi--;
            } else if (s < 0) lo++;
            else hi--;
        }
    }
    return res;
}
```

> [note] **Trace it** — `[-1,0,1,2,-1,-4]` sorts to `[-4,-1,-1,0,1,2]`. Fix `-1`, then two pointers on the rest find `0+1` and `-1+2` → triplets `[-1,0,1]` and `[-1,-1,2]`.

### Complexity
Time O(n²) · Space O(1) (excluding output/sort).

> [note] **Interview script** — "I first confirm the output needs unique triplets and the input is unsorted, so sorting is allowed. I start with brute force by checking all triples and deduping them, which is O(n³) time and too slow. I optimize by sorting, fixing one pivot, and two-pointering the remaining pair with duplicate skips for O(n²) time and O(1) extra space excluding output."


> [trap] **Common Trap** — Missing any of the three duplicate-skips yields repeated triplets. *Example:* `nums=[-1,-1,-1,2]`. Without skipping duplicate pivots you emit `[-1,-1,2]` twice (once per `-1` as pivot); without skipping `lo`/`hi` after a hit, `[0,0,0,0]` emits `[0,0,0]` multiple times.

### Common Mistakes
- **Missing any of the three duplicate-skips** — pivot, `lo`, `hi`. All three are required.
- **Advancing `lo`/`hi` before skipping duplicates** — do the skip on the value you just consumed, then advance.
- **Using `long` for the sum** unnecessary here (constraints keep it within `int`), but confirm when values approach `10⁹`.
- **Not sorting first** breaks the two-pointer discard argument — the whole approach collapses to O(n³).

> [pat] **Pattern Connection** — Generalizes to k-Sum by recursion (fix outer indices, two-pointer the base case). 4Sum = one more loop.

### Same pattern, new tweaks

Sort once, then let two converging pointers do the work — the target and the counting change, the skeleton doesn't:

| Variation | The one thing that changes | Time |
|---|---|---|
| [3Sum Closest](https://leetcode.com/problems/3sum-closest/) | instead of hunting for exactly 0, track the sum closest to `target` as the pointers move | — |
| [3Sum Smaller](https://leetcode.com/problems/3sum-smaller/) | count triplets with sum `< target`; when `a[lo]+a[hi] < target`, *all* `hi−lo` pairs qualify at once, so add them in one shot | — |
| [4Sum](https://leetcode.com/problems/4sum/) | add one more outer loop, then two-pointer the inner pair (skip duplicates at every level) | — |
| [Triplets with Smaller Sum](https://leetcode.com/problems/3sum-smaller/) | same batch-counting trick as 3Sum Smaller | — |

## Container With Most Water
*[↗ LeetCode: Container With Most Water](https://leetcode.com/problems/container-with-most-water/)*

### Problem
Each element is the height of a vertical wall. Pick the two walls that (with the x-axis) hold the **most water** — area `= min(h[i], h[j]) × (j − i)`.

**Constraints:** `2 ≤ n ≤ 10⁵`; heights `≥ 0`.

**Example:** `[1,8,6,2,5,4,8,3,7]` → `49`.

### Brute force
Brute force checks every pair of walls `(i, j)`, computes `min(h[i], h[j]) * (j - i)`, and keeps the largest area. It is easy to reason about and uses O(1) space, but it is O(n²) time because there are all-pairs choices. The optimized two-pointer version keeps the widest container first and moves only the shorter wall, because moving the taller wall cannot raise the limiting height.

### Pattern
Converging pointers; move the **shorter** wall — the only move that can increase area.

> [key] **Key Insight** — Area = `min(h[l],h[r]) × (r−l)`. Width shrinks each step, so only raising the limiting height can help; moving the taller wall can never improve.

### Java
```java
int maxArea(int[] h) {
    int l = 0, r = h.length - 1, best = 0;
    while (l < r) {
        best = Math.max(best, Math.min(h[l], h[r]) * (r - l));
        if (h[l] < h[r]) l++; else r--;
    }
    return best;
}
```

> [note] **Trace it** — `[1,8,6,2,5,4,8,3,7]`. Widest pair `8@idx1` and `7@idx8` give `min(8,7)×7 = 49` — the max. Moving the taller side could only shrink width without raising the limiting height.

### Complexity
Time O(n) · Space O(1).

> [note] **Interview script** — "I first confirm we need the maximum area from two vertical lines and width is index distance. I start with brute force by testing every pair, which is O(n²) time and O(1) space. I optimize with two pointers at the ends, moving the shorter wall each step, for O(n) time and O(1) space."


> [trap] **Common Trap** — Moving the taller wall can never help. *Example:* `heights=[1,8,6,2,5,4,8,3,7]`, `lo=0(h=1), hi=8(h=7)`. Moving `hi` inward shrinks width and can't raise the min (already `1`). Move the shorter wall — the only move that can improve area.

> [pat] **Pattern Connection** — Greedy converging pointers. Contrast with Trapping Rain Water, which *accumulates* water rather than maximizing a single span.

### Same pattern, new tweaks

Two pointers closing in from the ends, always moving the one that can't hurt you:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | instead of maximizing one span, accumulate water per bar using the smaller of the two running maxes | — |
| [Valid Palindrome / Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/) | compare from both ends inward; II allows one mismatch (try skipping either side) | — |
| [Boats to Save People](https://leetcode.com/problems/boats-to-save-people/) | sort, then pair the lightest with the heaviest that still fits — a converging-pointer greedy | — |

## Squaring a Sorted Array
*[↗ LeetCode: Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/)*

### Problem
Given a **sorted** array that may contain negatives, return the squares of every number, also in **sorted** order — in O(n).

**Constraints:** `1 ≤ n ≤ 10⁴`; input sorted ascending; negatives allowed (their squares can be the largest).

**Example:** `[-4,-1,0,3,10]` → `[0,1,9,16,100]`.

### Brute force
Brute force squares every element, then sorts the squared values. That is correct because sorting restores the lost order after negatives become positive, but it costs O(n log n) time and O(n) output space. The sorted input still gives structure: the largest remaining square must be at the left or right end, so the optimized method fills the output array from back to front in one pass.

### Pattern
A sorted array may contain negatives, whose squares are large. Merge from **both ends inward** — the biggest square is always at one of the two ends.

> [key] **Key Insight** — After squaring, the array is no longer sorted (e.g. `[-4,-1,0,3]` → `[16,1,0,9]`). But the largest square must come from the most-negative or most-positive value — i.e. an **end**. So compare the two ends, take the larger square, and fill the result **back to front**.

> [inv] **Invariant** — `[left, right]` still spans every element whose square hasn't been placed; `pos` marks the next slot to fill from the right, so the output is built in descending square order.

### Java
```java
int[] sortedSquares(int[] a) {
    int n = a.length, left = 0, right = n - 1;
    int[] res = new int[n];
    for (int pos = n - 1; pos >= 0; pos--) {   // fill largest-first, back to front
        int ls = a[left] * a[left], rs = a[right] * a[right];
        if (ls > rs) { res[pos] = ls; left++; }
        else         { res[pos] = rs; right--; }
    }
    return res;
}
```

> [note] **Trace it** — `[-4,-1,0,3,10]`. Compare ends: `(-4)²=16` vs `10²=100` → take 100, then 16, 9, 1, 0; fill the output back-to-front → `[0,1,9,16,100]`.

### Complexity
Time O(n) · Space O(n) (output).

> [note] **Interview script** — "I first confirm the input is already sorted but may contain negatives, so squared order can break. I start with brute force by squaring everything and sorting, which is O(n log n) time and O(n) space. I optimize by comparing absolute extremes with two pointers and filling from the end, giving O(n) time and O(n) output space."


> [trap] **Common Trap** — Squaring in place, then sorting. *Example:* `nums=[-4,-1,0,3,10]` → squared `[16,1,0,9,100]` still needs a sort (O(n log n)). Two pointers from the ends fill an output array from the back in O(n).

> [pat] **Pattern Connection** — "Merge from both ends because the extreme is at an end" is the same converging-pointer idea as Container With Most Water, and mirrors the merge step of merge sort operating on a fold-point.

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Sort Transformed Array](https://leetcode.com/problems/squares-of-a-sorted-array/) | after applying `ax²+bx+c` the extremes are at the ends (if `a>0`) or middle (if `a<0`); merge accordingly | — |
| [Merge Sorted Array (in place, from the back)](https://leetcode.com/problems/merge-sorted-array/) | fill from the largest end so you never overwrite unmerged values | — |
| [Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii/) | sort both, then two pointers advancing the smaller side | — |

## Sort Colors (Dutch National Flag)
*[↗ LeetCode: Sort Colors](https://leetcode.com/problems/sort-colors/)*

### Problem
Sort an array of `0`s, `1`s, and `2`s **in place** in a single pass (the Dutch-national-flag problem) — no library sort.

**Constraints:** `1 ≤ n ≤ 300`; values ∈ {0,1,2}; O(1) extra space, one pass.

**Example:** `[2,0,2,1,1,0]` → `[0,0,1,1,2,2]`.

### Brute force
Brute force can count how many `0`s, `1`s, and `2`s appear, then overwrite the array with that many of each value. That is O(n) time and O(1) space, but it uses two passes; a comparison sort would be O(n log n) and unnecessary. The Dutch National Flag optimization keeps three regions and partitions in one pass, which is the version to present when the interviewer asks for one-pass in-place sorting.

### Pattern
Three-way partition in one pass with three pointers `low, mid, high`.

> [inv] **Invariant** — `[0,low)`=0s, `[low,mid)`=1s, `(high,n)`=2s; `[mid,high]` unprocessed. The three regions only grow.

### Java
```java
void sortColors(int[] a) {
    int low = 0, mid = 0, high = a.length - 1;
    while (mid <= high) {
        if (a[mid] == 0)      swap(a, low++, mid++);
        else if (a[mid] == 1) mid++;
        else                  swap(a, mid, high--);   // 2: don't advance mid
    }
}
void swap(int[] a, int i, int j){ int t=a[i]; a[i]=a[j]; a[j]=t; }
```

> [note] **Trace it** — `[2,0,2,1,1,0]`. `mid` walks forward: 0s swap down to `low`, 2s swap up to `high`, 1s stay → `[0,0,1,1,2,2]` in a single sweep.

### Complexity
Time O(n) · Space O(1).

> [note] **Interview script** — "I first confirm the only values are 0, 1, and 2 and the array must be sorted in place. I start with brute force as counting buckets or library sort, which is O(n) in two passes or O(n log n) with sort. I optimize with `low`, `mid`, and `high` regions so one scan partitions the array in O(n) time and O(1) space."


> [trap] **Common Trap** — Advancing `mid` after swapping with `high` skips an unexamined value. *Example:* `[2,0,2]`, `mid=1`. Swap `a[mid]` with `a[high]` → `[2,0,2]` (a `2` moves in at `mid`). If you `mid++`, you miss re-evaluating that new value. Advance `mid` only when you swapped with `low` or saw a `1`.

> [pat] **Pattern Connection** — Partitioning is the core of Quickselect/quicksort; the same 3-way scheme handles duplicate-heavy pivots (3-way quicksort).

### Same pattern, new tweaks

"Sweep once, swapping items into buckets by category" generalizes the Dutch-flag idea:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Move Zeroes](https://leetcode.com/problems/move-zeroes/) | two categories (nonzero vs zero); a single write-pointer packs nonzeros to the front | — |
| [Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/) | partition into evens then odds with two pointers | — |
| [Wiggle Sort](https://leetcode.com/problems/wiggle-sort-ii/) | partition around the median, then interleave the two halves | — |
| [Partition (Quicksort step)](https://leetcode.com/problems/kth-largest-element-in-an-array/) | the same in-place split around a pivot that powers Quickselect | — |

## Trapping Rain Water
*[↗ LeetCode: Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)*

### Problem
Each bar has width 1; compute how much **rain water** is trapped between the bars after it rains.

**Constraints:** `1 ≤ n ≤ 2·10⁴`; heights `≥ 0`; target O(n) time, O(1) space.

**Example:** `[0,1,0,2,1,0,1,3,2,1,2,1]` → `6`.

### Brute force
Brute force computes water at each index by scanning left for the tallest wall and scanning right for the tallest wall, then adding `min(leftMax, rightMax) - height[i]`. That is correct but costs O(n²) time and O(1) space. Precomputing prefix/suffix maxima gives O(n) time with O(n) space; the shown two-pointer version compresses those maxima into two running values for O(1) extra space.

### Pattern
Two pointers tracking `leftMax`/`rightMax`; water over a bar is bounded by the smaller side's running max.

> [key] **Key Insight** — Water above `i` = `min(maxLeft, maxRight) − h[i]`. Advance from the side with the smaller max, because that side's bound is fixed regardless of what lies beyond.

> [inv] **Invariant** — If `leftMax ≤ rightMax`, the water at `left` depends only on `leftMax` (a taller-or-equal wall is guaranteed on the right).

### Steps
1. Two pointers `lo=0, hi=n-1`; carry `leftMax = 0`, `rightMax = 0`.
2. At each step, compare `heights[lo]` vs `heights[hi]`. The **shorter** side bounds the water.
3. If `heights[lo] < heights[hi]`: if `heights[lo] >= leftMax`, update `leftMax`; else add `leftMax - heights[lo]` to the answer. Advance `lo++`.
4. Symmetric on the right side: advance `hi--`.
5. Loop until `lo >= hi`. Every cell contributes at most once — O(n) time, O(1) space.

### Java
```java
int trap(int[] h) {
    int l = 0, r = h.length - 1, lMax = 0, rMax = 0, water = 0;
    while (l < r) {
        if (h[l] < h[r]) {
            lMax = Math.max(lMax, h[l]);
            water += lMax - h[l];
            l++;
        } else {
            rMax = Math.max(rMax, h[r]);
            water += rMax - h[r];
            r--;
        }
    }
    return water;
}
```

> [note] **Trace it** — `[0,1,0,2,1,0,1,3,2,1,2,1]` traps **6** units. Over the `0` at index 2, water rises to `min(leftMax=1, rightMax=3)=1`, so 1 unit sits there; summing every bar gives 6.

### Complexity
Time O(n) · Space O(1).

> [note] **Interview script** — "I first confirm each bar has width one and water over a bar depends on the smaller boundary wall. I start with brute force by scanning left and right from every index, which is O(n²) time and O(1) space. I optimize by carrying `leftMax` and `rightMax` with two pointers, so each bar is processed once in O(n) time and O(1) space."


> [trap] **Common Trap** — Local vs global boundaries. *Example:* `heights=[4,2,0,3,2,5]`. Water above index 3 (h=3) is bounded by the global `4` on the left and `5` on the right — not by 3. Track running max from each side (or the shorter side with two pointers).

### Common Mistakes
- **Local maxima vs global**: water above a cell depends on the global bounding walls, not on the nearest peak.
- **Wrong side advances**: only move the pointer on the shorter side — that's the one whose water level is determined.
- **Missing the `>= leftMax` check**: without it, you subtract on `leftMax = heights[lo]` and get negative contributions.
- **Stack-based alternative**: also O(n) but uses O(n) space; two-pointer is O(1).

> [pat] **Pattern Connection** — Also solvable with a monotonic (decreasing) stack that resolves trapped basins between bars — a good cross-check of the two viewpoints.

### Same pattern, new tweaks

"Water/area is bounded by the smaller enclosing wall" shows up in a few disguises:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | maximize a single span instead of summing trapped water; move the shorter wall | — |
| [Trapping Rain Water II (2D)](https://leetcode.com/problems/trapping-rain-water-ii/) | the "walls" are a whole grid boundary, so process cells outward from the lowest border using a min-heap | — |
| [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | the dual "peak" view — a monotonic stack finds how far each bar extends | — |
