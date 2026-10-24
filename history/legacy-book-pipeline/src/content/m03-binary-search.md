## Concepts & Mental Models

Binary search is not "look in the middle"; it is **maintaining a proof about a monotonic search space**. A search space is monotonic when every candidate can be classified so that, after some boundary, the answer to a yes/no question never flips back. In a sorted array, the predicate `nums[i] >= target` is false for a prefix and true for a suffix. In answer-space problems, `canFinish(speed)` may be false for small speeds and true for all larger speeds. Binary search works because a single midpoint test tells you which whole side is impossible.

!!! key "The mental model"
    Binary search finds a boundary between two regions: `false false false | true true true` or `true true true | false false false`. The code is correct when the loop invariant precisely states which region contains the answer and each update preserves that statement.

The safest interview convention is a **half-open interval**: `[lo, hi)`. `lo` is included, `hi` is excluded, and the interval is empty when `lo == hi`. The midpoint is always computed as `mid = lo + (hi - lo) / 2`, never `(lo + hi) / 2`, because indexes, sums, and answer bounds may overflow. For a lower-bound search (`first index with nums[i] >= target`), if `nums[mid] >= target`, the answer is at `mid` or left of it, so set `hi = mid`; otherwise set `lo = mid + 1`. Each update strictly shrinks the interval, so termination is guaranteed.

First and last occurrence are the same boundary problem with different predicates. First occurrence of `target` is the first `i` where `nums[i] >= target`; verify equality after the search. Last occurrence is `upperBound(target) - 1`, where `upperBound` is the first `i` with `nums[i] > target`. Avoid ad-hoc `while (lo <= hi)` variants unless you can state the invariant just as clearly.

The leap to **binary search on the answer** is recognizing that the candidates need not be indexes in an array. If a numeric answer has an ordered range and a monotone feasibility predicate — impossible below the answer, possible at and above it, or the reverse — the same boundary-search template applies. Koko, shipping capacity, allocation, and many scheduling problems are not "searching data"; they are searching the smallest parameter that makes a system feasible.

---

## Binary Search (the template + invariants)

!!! pattern "Pattern: Monotone boundary · T: O(log n) · S: O(1)"
    **Signals:** sorted array, first/last occurrence, lower/upper bound, phrase "smallest index/value satisfying".

### 1. The Problem

Given a sorted array `nums` and a `target`, return the index of `target` if present, otherwise `-1`. More importantly, implement the reusable boundary-search template that also supports insertion position, first occurrence, and upper bound.

### 2. The Intuition

Sorted order gives every midpoint global information. If `nums[mid] < target`, every index `<= mid` is too small. If `nums[mid] >= target`, the first possible target position is `mid` or earlier. We are not guessing where `target` is; we are proving which interval still may contain the leftmost valid position.

### 3. The Naive Approach

Scan from left to right and compare each element with `target`. This is simple and works for unsorted data, but it ignores monotonicity and costs O(n). In an interview, the sorted precondition is a signal that you should eliminate half of the candidates per comparison.

### 4. The Key Observation 🔑

!!! key "Key observation"
    In a sorted array, the predicate `nums[i] >= target` is monotone: it is false for a prefix and true for a suffix. The first true index is the lower bound. If that index exists and `nums[index] == target`, it is the answer; otherwise the target is absent.

### 5. Pattern Recognition

**Signals.** Sorted array, target lookup, insertion point, first/last occurrence, or a statement that can be phrased as "find the first index where predicate becomes true."

**Shortcut.** Define the predicate before writing code. If you can draw `F F F T T T`, use lower bound. If you need the last true, search for first false and subtract one.

**Related problems.** Search Insert Position, First Bad Version, Find First and Last Position, and every answer-space problem in this chapter.

### 6. The Invariant

Use `[lo, hi)`.

- All indexes `< lo` are known to satisfy `nums[i] < target` and cannot be the lower bound.
- All indexes `>= hi` are not needed; the lower bound, if any, is in `[lo, hi)`.
- The candidate interval strictly shrinks every iteration.

At termination, `[lo, hi)` is empty, so `lo` is the first index where `nums[i] >= target`, or `nums.length` if no such index exists.

### 7. Visual Explanation

```diagram
{"type":"searchspace","values":[1,3,5,7,9,11,13,15],"lo":0,"mid":4,"hi":8,"eliminated":[4,5,6,7],"target":7}
```

`mid = 4` has value `9`, which is `>= 7`. The lower bound could be `4`, but it could also be to the left, so the right suffix is eliminated by setting `hi = mid`.

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":460,"box":260,"title":"Lower-bound binary search","steps":[{"type":"start","text":"lo = 0, hi = n"},{"type":"decision","text":"lo < hi?","yes":"yes","branch":{"label":"no","text":"candidate = lo","role":"green"}},{"type":"process","text":"mid = lo + (hi - lo) / 2"},{"type":"decision","text":"nums[mid] >= target?","yes":"hi = mid","branch":{"label":"no","text":"lo = mid + 1","role":"primary"}},{"type":"end","text":"verify candidate in range and equal"}]}
```

### 9. Step-by-Step Walkthrough

For `nums = [1,3,5,7,9,11,13,15]`, `target = 7`:

| iteration | `[lo, hi)` | `mid` | `nums[mid]` | decision |
|---|---:|---:|---:|---|
| 1 | `[0, 8)` | 4 | 9 | `>= target`, set `hi = 4` |
| 2 | `[0, 4)` | 2 | 5 | `< target`, set `lo = 3` |
| 3 | `[3, 4)` | 3 | 7 | `>= target`, set `hi = 3` |
| end | `[3, 3)` | — | — | index 3 is lower bound |

### 10. Why It Works

The invariant is established initially: no index is known impossible, and the lower bound is somewhere in `[0, n]`. On each iteration, either `nums[mid] >= target`, so `mid` and everything to the right cannot improve on `mid`; keeping `mid` via `hi = mid` preserves the lower-bound candidate. Or `nums[mid] < target`, so every index `<= mid` is too small and `lo = mid + 1` is safe. The interval length decreases because `mid < hi` and `mid >= lo`. When `lo == hi`, the only remaining boundary is `lo`.

### 11. Java Implementation

```java
int search(int[] nums, int target) {
    int i = lowerBound(nums, target);
    return i < nums.length && nums[i] == target ? i : -1;
}

int lowerBound(int[] nums, int target) {
    int lo = 0, hi = nums.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] >= target) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}

int upperBound(int[] nums, int target) {
    int lo = 0, hi = nums.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > target) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}
```

### 12. Code Walkthrough

`lowerBound` returns an insertion position even when the target is absent. The wrapper converts that boundary into exact search by checking bounds and equality. `upperBound` changes only the predicate from `>= target` to `> target`; the loop mechanics remain identical.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(log n) — each iteration halves the candidate interval. **S:** O(1) — only three indexes are stored.

### 14. Edge Cases

- Empty array → `lo == hi == 0`, return `-1`.
- Target smaller than all values → lower bound is 0.
- Target larger than all values → lower bound is `n`, wrapper returns `-1`.
- Duplicates → lower bound returns the first equal value; `upperBound(target) - 1` gives the last.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Mixing inclusive and half-open conventions is the source of most bugs. If the loop is `while (lo < hi)`, updates must be `hi = mid` or `lo = mid + 1`; using `hi = mid - 1` can skip the answer. Also avoid `mid = (lo + hi) / 2`, which may overflow.

### 16. Optimization

The template is already optimal for comparison-based sorted search. The useful optimization is cognitive: implement one correct lower-bound helper and reuse it instead of inventing a new loop per problem.

### 17. Alternatives

`Arrays.binarySearch` is production-friendly but poor for interviews because its negative insertion-point encoding hides the invariant. Linear scan is only competitive for tiny arrays or when data is unsorted.

### 18. Interview Follow-Ups

- Return first and last position: `first = lowerBound(target)`, `last = upperBound(target) - 1`.
- Search in an unknown-size array: exponentially grow a high bound, then binary search.
- Search a monotone boolean API: the array values disappear; the predicate remains.

### 19. Variations

Lower bound, upper bound, search insert position, peak-finding variants, first bad version, and answer-space feasibility search are all boundary searches with different predicates.

### 20. Pattern Connection

This is the primitive used throughout the chapter. Rotated search modifies the predicate because sortedness is local, Koko and shipping move the interval from indexes to numeric answers, and median partition search uses binary search over how many elements are taken from one array.

---

## Search in Rotated Sorted Array

!!! pattern "Pattern: Binary search with one sorted half · T: O(log n) · S: O(1)"
    **Signals:** sorted array rotated at an unknown pivot, distinct values, target lookup.

### 1. The Problem

Given a sorted ascending array rotated at an unknown pivot, with distinct values, return the index of `target` or `-1`. Example: `[4,5,6,7,0,1,2]`, target `0` → `4`.

### 2. The Intuition

Rotation breaks global sortedness, but every midpoint still reveals structure: at least one side of the interval is sorted. If the left half is sorted, we can test whether `target` lies inside that value range. If not, the answer must be in the other half. The midpoint comparison eliminates a half by combining local sortedness with range membership.

### 3. The Naive Approach

Scan every index until `target` is found. This ignores the rotated sorted structure and costs O(n). Another approach is to find the pivot first and then run normal binary search in one side; that is valid but usually more code than necessary.

### 4. The Key Observation 🔑

!!! key "Key observation"
    For any `lo <= mid <= hi` in a rotated array with distinct values, either `nums[lo..mid]` is sorted or `nums[mid..hi]` is sorted. Once you identify the sorted half, a range check tells whether the target can be there; the other half is safely discarded.

### 5. Pattern Recognition

**Signals.** "Rotated sorted array," "distinct integers," and O(log n) required.

**Shortcut.** Ask: *Which half is sorted?* Then ask: *Can the target fit inside that half's endpoints?*

**Related problems.** Find Minimum in Rotated Sorted Array, Search in Rotated Sorted Array II with duplicates, and circular monotonic structures.

### 6. The Invariant

Use an inclusive interval `[lo, hi]` here because we return immediately on equality and discard closed halves.

- If the target exists, it is always inside `nums[lo..hi]`.
- At each step, equality is checked first.
- The selected update removes a half proven unable to contain the target.

Updates use `lo = mid + 1` or `hi = mid - 1`, so the interval strictly shrinks and cannot loop forever.

### 7. Visual Explanation

```diagram
{"type":"searchspace","values":[4,5,6,7,0,1,2],"lo":0,"mid":3,"hi":6,"eliminated":[0,1,2,3],"target":0}
```

At `mid = 3`, value `7`. The left half `[4,5,6,7]` is sorted, but target `0` is not in `[4,7]`, so that half is eliminated and the search continues right.

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":500,"box":280,"title":"Rotated search decision tree","steps":[{"type":"start","text":"lo = 0, hi = n - 1"},{"type":"decision","text":"lo <= hi?","yes":"yes","branch":{"label":"no","text":"return -1","role":"red"}},{"type":"process","text":"mid = lo + (hi - lo) / 2"},{"type":"decision","text":"nums[mid] == target?","yes":"return mid","branch":{"label":"no","text":"identify sorted half","role":"primary"}},{"type":"decision","text":"target inside sorted half?","yes":"keep sorted half","branch":{"label":"no","text":"discard sorted half","role":"primary"}}]}
```

### 9. Step-by-Step Walkthrough

For `[4,5,6,7,0,1,2]`, target `0`:

| iteration | `lo` | `mid` | `hi` | sorted half | decision |
|---|---:|---:|---:|---|---|
| 1 | 0 | 3 | 6 | left `[4..7]` | target not in left, `lo = 4` |
| 2 | 4 | 5 | 6 | left `[0..1]` | target in left, `hi = 4` |
| 3 | 4 | 4 | 4 | equal | return 4 |

### 10. Why It Works

In a rotation of a strictly increasing array, the pivot can lie in only one half of any interval. Therefore the other half is sorted. If `nums[lo] <= nums[mid]`, the left half is sorted. A target in `[nums[lo], nums[mid])` cannot appear in the right half because distinct sorted values occupy exactly that range on the left; otherwise the left half is impossible. The symmetric argument applies when the right half is sorted. Because each update discards only impossible positions, the invariant is preserved until equality is found or the interval is empty.

### 11. Java Implementation

```java
int searchRotated(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;

        if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) {
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        } else {
            if (nums[mid] < target && target <= nums[hi]) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
    }
    return -1;
}
```

### 12. Code Walkthrough

Equality is checked before half classification so singleton intervals are handled cleanly. The left-sorted branch uses `target < nums[mid]` because equality with `mid` was already handled. The right-sorted branch is symmetric: target must be strictly greater than `nums[mid]` and at most `nums[hi]`.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(log n) — one half is discarded each iteration. **S:** O(1) — only indexes are stored.

### 14. Edge Cases

- Array of length 0 → loop skipped, `-1`.
- Array of length 1 → equality check handles it.
- No rotation → left half is repeatedly detected as sorted, degenerating to normal binary search.
- Target at pivot or endpoints → equality and inclusive endpoint checks cover it.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    The duplicate-free assumption matters. With duplicates, `nums[lo] == nums[mid] == nums[hi]` may hide which half is sorted, forcing conservative boundary movement and worst-case O(n). Also be consistent with open/closed endpoint checks after equality has been handled.

### 16. Optimization

The one-pass version is concise and optimal. Pivot-first search can be easier to reason about for some candidates but requires two binary searches and more boundary cases.

### 17. Alternatives

Find the minimum index, then choose the sorted side containing the target and run ordinary binary search. Complexity remains O(log n), but the direct approach avoids a separate pivot abstraction.

### 18. Interview Follow-Ups

- Allow duplicates: when half classification is ambiguous, shrink `lo` or `hi` cautiously.
- Return insertion point in rotated order: first define the order semantics; it is no longer normal lower bound.
- Search a rotated array of strings or custom keys: comparisons generalize if the ordering is total.

### 19. Variations

Minimum in rotated array, rotated search with duplicates, searching cyclic time ranges, and binary search over piecewise-monotone domains.

### 20. Pattern Connection

This problem shows that binary search does not require the whole interval to be sorted — it requires a reason to discard a half. The invariant is still "target remains in the candidate interval," but the proof uses local sortedness rather than a global monotone predicate.

---

## Find Minimum in Rotated Sorted Array

!!! pattern "Pattern: Rotated boundary · T: O(log n) · S: O(1)"
    **Signals:** rotated sorted array, distinct values, ask for pivot/minimum rather than target.

### Problem

Given a rotated sorted array with distinct values, return its minimum element. Example: `[4,5,6,7,0,1,2]` → `0`.

### Key Observation

!!! key "Key observation"
    Compare `nums[mid]` with `nums[hi]`. If `nums[mid] > nums[hi]`, the minimum is strictly to the right of `mid`; otherwise `mid` could be the minimum, so keep it by setting `hi = mid`.

### Invariant

Use `[lo, hi]` inclusive. The minimum is always inside the interval. `hi` is never discarded when it may be the minimum; `lo` moves past `mid` only when `mid` is proven larger than the right endpoint.

### Visual Explanation

```diagram
{"type":"searchspace","values":[4,5,6,7,0,1,2],"lo":0,"mid":3,"hi":6,"eliminated":[0,1,2,3],"target":0}
```

`nums[mid] = 7 > nums[hi] = 2`, so the drop — and therefore the minimum — must be to the right.

### Java

```java
int findMin(int[] nums) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > nums[hi]) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return nums[lo];
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(log n). **S:** O(1). Each comparison with the right endpoint halves the pivot interval.

### Pattern Connection

This is lower-bound search on the rotation break. The predicate is not `nums[i] >= target`; it is whether the minimum lies to the right of `mid`. The same `hi = mid` vs `lo = mid + 1` termination discipline prevents skipping the pivot.

---

## Search a 2D Matrix

!!! pattern "Pattern: Flattened binary search · T: O(log(mn)) · S: O(1)"
    **Signals:** each row sorted and first element of each row greater than last of previous row.

### Problem

Given an `m x n` matrix whose rows are sorted and whose row ranges are globally ordered, return whether `target` exists.

### Key Observation

!!! key "Key observation"
    The matrix is a sorted one-dimensional array viewed through coordinates. Index `k` maps to `row = k / n`, `col = k % n`; binary search does not need to materialize the flattened array.

### Invariant

Search `[lo, hi)` over virtual indexes `0..m*n`. All virtual indexes `< lo` are too small; the candidate target location, if any, is in `[lo, hi)`. Termination gives the first value `>= target`.

### Visual Explanation

```diagram
{"type":"grid","col_head":["0","1","2","3"],"row_head":["0","1"],"corner":"r/c","grid":[[1,3,5,7],[10,11,16,20]],"highlights":[[0,2,"amber"],[1,0,"green"]],"arrows":[{"from":[0,2],"to":[1,0],"color":"primary"}]}
```

The virtual order is row-major: after `(0,2)` comes `(0,3)`, then `(1,0)`. Binary search moves over virtual indexes, then converts the chosen midpoint back to a cell.

### Java

```java
boolean searchMatrix(int[][] matrix, int target) {
    if (matrix.length == 0 || matrix[0].length == 0) return false;
    int m = matrix.length, n = matrix[0].length;
    long lo = 0, hi = (long) m * n;
    while (lo < hi) {
        long mid = lo + (hi - lo) / 2;
        int value = matrix[(int) (mid / n)][(int) (mid % n)];
        if (value >= target) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo < (long) m * n && matrix[(int) (lo / n)][(int) (lo % n)] == target;
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(log(mn)). **S:** O(1). The matrix is only indexed, never copied.

### Pattern Connection

This is ordinary lower bound after changing the address function. The invariant lives over virtual positions, not rows and columns. That separation avoids nested binary searches and row-boundary off-by-one bugs.

---

## Koko Eating Bananas (binary search on answer)

!!! pattern "Pattern: Answer-space feasibility · T: O(n log M) · S: O(1)"
    **Signals:** minimize an integer rate/capacity, feasibility is monotone, direct formula is hard.

### 1. The Problem

Koko has piles of bananas and `h` hours. At speed `k`, she eats up to `k` bananas from one pile per hour. Return the minimum integer `k` such that all piles can be eaten within `h` hours.

### 2. The Intuition

Higher speed never hurts. If speed `k` is enough, then every speed greater than `k` is also enough. If `k` is too slow, every smaller speed is too slow. That is the exact `false false | true true` boundary binary search needs.

### 3. The Naive Approach

Try every speed from 1 to `max(piles)` and compute the hours needed. This is O(nM), where `M` is the largest pile. If piles can be large, enumerating speeds is the bottleneck, not computing feasibility.

### 4. The Key Observation 🔑

!!! key "Key observation"
    The predicate `canEat(k) = totalHours(k) <= h` is monotone increasing with `k`: once true, it remains true for all larger speeds. Therefore the answer is the lower bound of true speeds in `[1, maxPile]`.

### 5. Pattern Recognition

**Signals.** "Minimum speed," "within h hours," integer answer range, and a check function that scans the input.

**Shortcut.** If raising the candidate makes the constraint easier, binary search the smallest feasible value.

**Related problems.** Shipping capacity, split array largest sum, minimum days to make bouquets, repair cars, machine production time.

### 6. The Invariant

Use `[lo, hi)` over speeds, with `hi = maxPile + 1` as an exclusive bound.

- Every speed `< lo` is proven infeasible.
- The smallest feasible speed is in `[lo, hi)`.
- If `canEat(mid)` is true, keep `mid` by `hi = mid`; otherwise discard it by `lo = mid + 1`.

### 7. Visual Explanation

```diagram
{"type":"searchspace","values":[1,2,3,4,5,6,7,8],"lo":0,"mid":3,"hi":8,"eliminated":[0,1,2],"target":4}
```

For piles `[3,6,7,11]` and `h = 8`, speed `4` is feasible. Since all larger speeds are also feasible, the search keeps `4` as a possible answer and tries to prove whether any slower speed can work.

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":480,"box":270,"title":"Binary search on eating speed","steps":[{"type":"start","text":"lo = 1, hi = maxPile + 1"},{"type":"decision","text":"lo < hi?","yes":"yes","branch":{"label":"no","text":"return lo","role":"green"}},{"type":"process","text":"mid = lo + (hi - lo) / 2"},{"type":"process","text":"hours = sum(ceil(pile / mid))"},{"type":"decision","text":"hours <= h?","yes":"hi = mid","branch":{"label":"no","text":"lo = mid + 1","role":"primary"}}]}
```

### 9. Step-by-Step Walkthrough

For `piles = [3,6,7,11]`, `h = 8`:

| iteration | `[lo, hi)` | `mid` | hours | decision |
|---|---:|---:|---:|---|
| 1 | `[1, 12)` | 6 | 6 | feasible, `hi = 6` |
| 2 | `[1, 6)` | 3 | 10 | infeasible, `lo = 4` |
| 3 | `[4, 6)` | 5 | 8 | feasible, `hi = 5` |
| 4 | `[4, 5)` | 4 | 8 | feasible, `hi = 4` |
| end | `[4, 4)` | — | — | answer 4 |

### 10. Why It Works

For a fixed pile `p`, `ceil(p / k)` is non-increasing as `k` grows. Summing across piles preserves monotonicity, so `totalHours(k)` is non-increasing. Thus `totalHours(k) <= h` forms a suffix of true speeds. The invariant mirrors lower-bound search: infeasible speeds are discarded from the left, feasible mids are retained as possible answers, and the interval shrinks until the first feasible speed remains.

### 11. Java Implementation

```java
int minEatingSpeed(int[] piles, int h) {
    int max = 0;
    for (int pile : piles) max = Math.max(max, pile);

    long lo = 1, hi = (long) max + 1;
    while (lo < hi) {
        long mid = lo + (hi - lo) / 2;
        if (canEatAll(piles, h, mid)) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return (int) lo;
}

boolean canEatAll(int[] piles, int h, long speed) {
    long hours = 0;
    for (int pile : piles) {
        hours += (pile + speed - 1) / speed;
        if (hours > h) return false;
    }
    return true;
}
```

### 12. Code Walkthrough

`hi = (long) max + 1` makes the interval half-open and avoids overflow when `max` is large. The feasibility check uses long arithmetic and `(pile + speed - 1) / speed` for exact ceiling division. Early exit keeps failed mids cheap when `h` is already exceeded.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n log M), where `M = max(piles)`. Each feasibility check scans all piles, and the speed range halves each iteration. **S:** O(1).

### 14. Edge Cases

- `h == piles.length` → Koko must finish each pile in one hour, answer is `maxPile`.
- One pile → answer is `ceil(pile / h)` but the binary search still works.
- Large pile values → use `long` inside ceiling-sum arithmetic.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Do not binary search indexes of piles; the search space is speed. Do not use floating-point `Math.ceil((double)pile / speed)` in interview code when integer ceiling division is exact and faster. Ensure `lo` starts at 1; speed 0 is invalid.

### 16. Optimization

A tighter lower bound is `ceil(totalBananas / h)`, but `1` is simple and still logarithmic. Early exit in `canEatAll` is the most valuable practical optimization.

### 17. Alternatives

There is no closed-form answer because each pile rounds independently. Greedy distribution also fails because Koko cannot split an hour across piles. Feasibility search is the intended abstraction.

### 18. Interview Follow-Ups

- If piles can be split across hours freely, the answer becomes `ceil(total / h)`.
- If each hour has setup cost or multiple workers, redefine feasibility and recheck monotonicity.
- For real-valued speeds, binary search with an epsilon and fixed iterations replaces integer lower bound.

### 19. Variations

Minimum ship capacity, minimum machine time, smallest divisor under threshold, bouquet days, and many scheduling problems share the "smallest feasible parameter" template.

### 20. Pattern Connection

Koko is the canonical jump from array binary search to answer-space binary search. The invariant is identical to lower bound; only the predicate changes from `nums[mid] >= target` to `canEatAll(mid)`.

---

## Capacity to Ship Packages Within D Days

!!! pattern "Pattern: Smallest feasible capacity · T: O(n log S) · S: O(1)"
    **Signals:** preserve order, split sequence into at most `D` days, minimize maximum daily load.

### Problem

Given package weights in fixed order and `days`, return the minimum ship capacity needed to deliver all packages within `days` days.

### Key Observation

!!! key "Key observation"
    If capacity `C` can ship all packages within `days`, any larger capacity can also ship them. Feasibility is computed greedily: load packages in order until the next package would exceed `C`, then start a new day.

### Invariant

Search capacities in `[maxWeight, sumWeights]`. Values below `lo` are impossible because at least one package must fit. The smallest feasible capacity remains in `[lo, hi]`; feasible mids move `hi` down, infeasible mids move `lo` up.

### Visual Explanation

```diagram
{"type":"searchspace","values":[10,11,12,13,14,15,16,17],"lo":0,"mid":3,"hi":8,"eliminated":[0,1,2],"target":15}
```

A too-small capacity creates more than `days` partitions, so the entire lower prefix is eliminated.

### Java

```java
int shipWithinDays(int[] weights, int days) {
    long lo = 0;
    long sum = 0;
    for (int w : weights) {
        lo = Math.max(lo, w);
        sum += w;
    }
    long hi = sum;
    while (lo < hi) {
        long mid = lo + (hi - lo) / 2;
        if (canShip(weights, days, mid)) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return (int) lo;
}

boolean canShip(int[] weights, int days, long capacity) {
    int usedDays = 1;
    long load = 0;
    for (int w : weights) {
        if (load + w > capacity) {
            usedDays++;
            load = 0;
        }
        load += w;
        if (usedDays > days) return false;
    }
    return true;
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n log S), where `S = sum(weights) - max(weights) + 1`. **S:** O(1).

### Pattern Connection

This is Koko with a different feasibility function. The greedy check is valid because order is fixed and delaying a package never reduces the number of days for a fixed capacity.

---

## Book Allocation / Split Array Largest Sum

!!! pattern "Pattern: Minimize maximum partition sum · T: O(n log S) · S: O(1)"
    **Signals:** split an array into `k` contiguous groups, minimize the largest group sum.

### Problem

Given `nums` and `k`, split `nums` into at most `k` non-empty contiguous subarrays while minimizing the largest subarray sum. Book Allocation uses pages and students; Split Array Largest Sum uses numbers and partitions.

### Key Observation

!!! key "Key observation"
    For a proposed maximum sum `limit`, the fewest partitions are produced greedily by extending the current partition until adding the next element would exceed `limit`. If the greedy partition count is `<= k`, the limit is feasible.

### Invariant

The answer lies between `max(nums)` and `sum(nums)`. Feasible limits form a suffix: once a maximum sum works, any larger maximum also works. Keep feasible mids with `hi = mid`; discard infeasible mids with `lo = mid + 1`.

### Visual Explanation

```diagram
{"type":"array","values":[7,2,5,10,8],"brackets":[{"from":0,"to":2,"label":"14","color":"primary","row":0},{"from":3,"to":4,"label":"18","color":"green","row":0}],"highlights":{"3":"amber"},"caption":"With limit 18 and k = 2, greedy forms [7,2,5] and [10,8]; the largest sum is feasible."}
```

### Java

```java
int splitArray(int[] nums, int k) {
    long lo = 0;
    long sum = 0;
    for (int x : nums) {
        lo = Math.max(lo, x);
        sum += x;
    }
    long hi = sum;
    while (lo < hi) {
        long mid = lo + (hi - lo) / 2;
        if (canSplit(nums, k, mid)) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return (int) lo;
}

boolean canSplit(int[] nums, int k, long limit) {
    int groups = 1;
    long current = 0;
    for (int x : nums) {
        if (current + x > limit) {
            groups++;
            current = 0;
        }
        current += x;
        if (groups > k) return false;
    }
    return true;
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n log S), where `S = sum(nums) - max(nums) + 1`. **S:** O(1).

### Pattern Connection

Shipping capacity and split array are the same monotone feasibility problem: minimize the largest bucket while preserving order. The invariant is answer-space lower bound; the check is greedy partition counting.

---

## Median of Two Sorted Arrays (partition binary search)

!!! pattern "Pattern: Partition binary search · T: O(log min(m,n)) · S: O(1)"
    **Signals:** two sorted arrays, median/ kth boundary, required logarithmic time.

### 1. The Problem

Given two sorted arrays `a` and `b`, return the median of their combined sorted order in O(log(m+n)) time. You may not merge the arrays because merging is linear.

### 2. The Intuition

The median is defined by a partition: every element on the left side is `<=` every element on the right side, and the left side contains half of the combined elements. If we choose how many elements to take from the smaller array, the number taken from the larger array is forced. Binary search adjusts that cut until the boundary values are ordered correctly.

### 3. The Naive Approach

Merge both arrays until the middle. This is O(m+n) time and either O(m+n) space for a full merge or O(1) space for a streaming merge. It is often acceptable in production, but it misses the logarithmic requirement.

### 4. The Key Observation 🔑

!!! key "Key observation"
    Let `i` be the cut in `a` and `j = half - i` the cut in `b`. The partition is valid exactly when `aLeft <= bRight` and `bLeft <= aRight`. If `aLeft > bRight`, `i` is too far right; otherwise if `bLeft > aRight`, `i` is too far left.

### 5. Pattern Recognition

**Signals.** Two sorted arrays, median, kth element, and O(log min(m,n)) target complexity.

**Shortcut.** Do not search values; search a partition count in the smaller array. The other partition count is determined by total left size.

**Related problems.** Kth element of two sorted arrays, weighted median, and partition-based selection.

### 6. The Invariant

Binary search `i` in `[0, m]`, where `m <= n`. `half = (m + n + 1) / 2` ensures the left side has one extra element for odd totals. The valid partition remains within `[lo, hi]`. If `aLeft > bRight`, every larger `i` is also too far right, so move `hi = i - 1`. If `bLeft > aRight`, every smaller `i` is too far left, so move `lo = i + 1`.

### 7. Visual Explanation

```diagram
{"type":"searchspace","values":[0,1,2,3,4],"lo":0,"mid":2,"hi":4,"eliminated":[3,4],"target":2}
```

The search space is not array values; it is possible cut counts `i` in the smaller array. A midpoint cut that takes too many elements from `a` eliminates larger cut counts.

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":520,"box":300,"title":"Median partition search","steps":[{"type":"start","text":"ensure a is smaller"},{"type":"process","text":"half = (m + n + 1) / 2"},{"type":"process","text":"choose i in a, j = half - i"},{"type":"decision","text":"aLeft <= bRight and bLeft <= aRight?","yes":"compute median","branch":{"label":"no","text":"move cut left or right","role":"primary"}},{"type":"end","text":"return maxLeft or average"}]}
```

### 9. Step-by-Step Walkthrough

For `a = [1,3]`, `b = [2]`, swap so `a = [2]`, `b = [1,3]`, total `3`, `half = 2`.

| iteration | `i` | `j` | `aLeft` | `aRight` | `bLeft` | `bRight` | decision |
|---|---:|---:|---:|---:|---:|---:|---|
| 1 | 0 | 2 | -∞ | 2 | 3 | +∞ | `bLeft > aRight`, move right |
| 2 | 1 | 1 | 2 | +∞ | 1 | 3 | valid, median `max(2,1)` |

### 10. Why It Works

For any cut `i`, the total left size is fixed by `j = half - i`. Only boundary values can violate sorted partition order because each array is internally sorted. If `aLeft > bRight`, too many elements were taken from `a`: moving `i` right would only increase or preserve `aLeft` and decrease or preserve `bRight`, so no larger cut can work. If `bLeft > aRight`, too few elements were taken from `a`, and no smaller cut can work. These monotone failures allow binary search over cut counts.

### 11. Java Implementation

```java
double findMedianSortedArrays(int[] nums1, int[] nums2) {
    int[] a = nums1, b = nums2;
    if (a.length > b.length) {
        a = nums2;
        b = nums1;
    }

    int m = a.length, n = b.length;
    int half = (m + n + 1) / 2;
    int lo = 0, hi = m;

    while (lo <= hi) {
        int i = lo + (hi - lo) / 2;
        int j = half - i;

        int aLeft = i == 0 ? Integer.MIN_VALUE : a[i - 1];
        int aRight = i == m ? Integer.MAX_VALUE : a[i];
        int bLeft = j == 0 ? Integer.MIN_VALUE : b[j - 1];
        int bRight = j == n ? Integer.MAX_VALUE : b[j];

        if (aLeft <= bRight && bLeft <= aRight) {
            int maxLeft = Math.max(aLeft, bLeft);
            if (((m + n) & 1) == 1) return maxLeft;
            int minRight = Math.min(aRight, bRight);
            return ((long) maxLeft + minRight) / 2.0;
        }
        if (aLeft > bRight) {
            hi = i - 1;
        } else {
            lo = i + 1;
        }
    }
    throw new IllegalArgumentException("Input arrays must be sorted");
}
```

### 12. Code Walkthrough

Searching the smaller array guarantees `j` stays in range for valid inputs and gives O(log min(m,n)). Sentinels remove boundary branches for empty left or right partitions. The even-length average casts through `long` to avoid overflowing when both middle values are near `Integer.MAX_VALUE`.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(log min(m,n)) — binary search over the smaller cut count. **S:** O(1) — no merge buffer.

### 14. Edge Cases

- One array empty → sentinels reduce the problem to the median of the other array.
- Odd total length → return the largest left boundary.
- Even total length → average largest-left and smallest-right with overflow-safe arithmetic.
- Duplicate values → `<=` comparisons allow equal values across the partition.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Searching the larger array can make `j` negative or greater than `n`. Another common bug is using strict `<` instead of `<=`, which rejects valid partitions with duplicates. Finally, averaging two `int` values before widening can overflow.

### 16. Optimization

The algorithm is already asymptotically optimal for comparison-based access. The main practical optimization is swapping arrays once so the loop and boundary handling stay simple.

### 17. Alternatives

A recursive kth-element elimination approach also runs in O(log(m+n)) and is excellent for general kth queries. Merge-based approaches are simpler but linear. Value-space binary search is awkward with duplicates and integer ranges and does not exploit direct indexing as cleanly.

### 18. Interview Follow-Ups

- Return the kth smallest element: set `half = k` and use similar partition validity.
- Arrays stored on disk: compare random-access cost with streaming merge.
- More than two arrays: the clean partition property no longer has one degree of freedom; heaps or value-space counting may be better.

### 19. Variations

Kth element in two sorted arrays, lower median, percentile queries, and partitioning two sorted streams all reuse the boundary-values proof.

### 20. Pattern Connection

Median partition search is the most abstract form in this module. The search variable is neither an index to inspect nor an answer value; it is a **count** chosen from one sorted source. The invariant is still monotone elimination: cuts too far left or too far right form discardable regions.
