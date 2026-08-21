## Concepts & Mental Models

Divide and conquer turns one problem on `n` items into smaller independent problems, then pays a controlled combine cost:

1. **Split** into subproblems.
2. **Solve** subproblems recursively.
3. **Combine** their answers into the parent answer.

The senior engineer's question is not "can I recurse?" but: *how many subproblems, how fast do they shrink, and what is the non-recursive work?* That gives a recurrence.

!!! key "The recurrence lens"
    Most divide-and-conquer algorithms fit `T(n) = aT(n / b) + f(n)`: `a` subproblems, shrink factor `b`, and split/combine cost `f(n)`. Name all three before discussing complexity.

### Master Theorem summary

For `T(n) = aT(n / b) + f(n)`, compare `f(n)` with `n^{log_b a}`.

| Case | Condition | Meaning | Result | Example |
|---|---|---|---|---|
| 1 | `f(n) = O(n^{log_b a - ε})` | leaves dominate | `Θ(n^{log_b a})` | `T(n)=8T(n/2)+n²` → `Θ(n³)` |
| 2 | `f(n) = Θ(n^{log_b a} log^k n)` | levels tie | `Θ(n^{log_b a} log^{k+1} n)` | `T(n)=2T(n/2)+n` → `Θ(n log n)` |
| 3 | `f(n) = Ω(n^{log_b a + ε})` with regularity | root dominates | `Θ(f(n))` | `T(n)=2T(n/2)+n²` → `Θ(n²)` |

`ε > 0`; Case 3's regularity condition is `a f(n/b) ≤ c f(n)` for some constant `c < 1` and sufficiently large `n`.

### Sorting versus selection

Divide-and-conquer sorting solves **both** halves because the final sorted order depends on every element. Merge sort has `T(n)=2T(n/2)+Θ(n)=Θ(n log n)`. Selection is different: after partitioning around a pivot, the pivot's final rank tells us which side can contain the k-th element, so the other side is discarded. Quickselect's expected recurrence is `T(n)=T(n/2)+Θ(n)=Θ(n)`, while unlucky extreme pivots degrade to `Θ(n²)`; randomization makes that sequence unlikely.

!!! pattern "Pattern: Divide, discard, or merge"
    **Signals:** independent halves, ordered combine, rank-based pruning, or pair counting across a split. Sorting keeps both sides; selection throws one side away.

---

## Merge Sort

!!! pattern "Pattern: Divide & Conquer Sort · T: O(n log n) · S: O(n)"
    **Signals:** need guaranteed `O(n log n)`, stable ordering of equal keys, or a predictable comparison sort.

### 1. The Problem

Sort an integer array in nondecreasing order with deterministic worst-case `O(n log n)` time. The important points are the recurrence, the stable merge, and the `O(n)` auxiliary array.

### 2. The Intuition

Merging two sorted arrays is easy. Merge sort recursively creates sorted halves, then combines them linearly. Each recursion level touches every element once during merge.

### 3. The Naive Approach

Selection sort or insertion sort repeatedly grows a sorted prefix, but both are `O(n²)` in the worst case. They do not exploit the linear merge available once halves are sorted.

### 4. The Key Observation 🔑

!!! key "Key observation"
    If `a[lo..mid]` and `a[mid+1..hi]` are sorted, `a[lo..hi]` can be sorted in `Θ(hi-lo+1)` by two pointers. Thus `T(n)=2T(n/2)+Θ(n)`, Master Theorem Case 2, so `T(n)=Θ(n log n)`.

### 5. Pattern Recognition

**Signals.** Stable sort, worst-case guarantee, or a need to aggregate cross-half information.

**Recognition shortcut.** Ask: *"If both halves were solved, could I combine in linear time?"*

**Related problems.** Count Inversions, linked-list sort, external sorting, multiway merge.

### 6. The Invariant

For every `sort(a, aux, lo, hi)`, on return `a[lo..hi]` is sorted and contains exactly the original multiset. During merge, after writing `a[lo..k-1]`, that prefix contains the smallest `k-lo` values from `aux[lo..mid]` and `aux[mid+1..hi]`, in stable order.

### 7. Visual Explanation

```diagram
{"type":"recursion","nodes":[{"id":"n8","label":"8 elems\nmerge O(n)","x":3,"y":0,"role":"primary"},{"id":"n4l","label":"4\nO(n/2)","x":1,"y":1,"role":"panel"},{"id":"n4r","label":"4\nO(n/2)","x":5,"y":1,"role":"panel"},{"id":"n2a","label":"2","x":0,"y":2,"role":"muted"},{"id":"n2b","label":"2","x":2,"y":2,"role":"muted"},{"id":"n2c","label":"2","x":4,"y":2,"role":"muted"},{"id":"n2d","label":"2","x":6,"y":2,"role":"muted"},{"id":"n1a","label":"1","x":0,"y":3,"role":"green"},{"id":"n1b","label":"1","x":1,"y":3,"role":"green"},{"id":"n1c","label":"1","x":2,"y":3,"role":"green"},{"id":"n1d","label":"1","x":3,"y":3,"role":"green"}],"edges":[{"from":"n8","to":"n4l","label":"split","color":"primary"},{"from":"n8","to":"n4r","label":"split","color":"primary"},{"from":"n4l","to":"n2a","label":"","color":"muted"},{"from":"n4l","to":"n2b","label":"","color":"muted"},{"from":"n4r","to":"n2c","label":"","color":"muted"},{"from":"n4r","to":"n2d","label":"","color":"muted"},{"from":"n2a","to":"n1a","label":"","color":"green"},{"from":"n2a","to":"n1b","label":"","color":"green"},{"from":"n2b","to":"n1c","label":"","color":"green"},{"from":"n2b","to":"n1d","label":"","color":"green"}]}
```

Each level performs total merge work `Θ(n)`: one node of size `n`, two of size `n/2`, four of size `n/4`, for `log₂ n` levels.

```diagram
{"type":"array","values":[1,4,7,2,3,6],"highlights":{"0":"green","3":"amber"},"pointers":[{"name":"i","index":0,"color":"green","side":"top"},{"name":"j","index":3,"color":"amber","side":"top"},{"name":"k","index":0,"color":"primary","side":"bottom"}],"brackets":[{"from":0,"to":2,"label":"left sorted","color":"green","row":0},{"from":3,"to":5,"label":"right sorted","color":"amber","row":0}],"caption":"Compare aux[i] and aux[j]; write the smaller to a[k]. Equal values choose left first for stability."}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":460,"box":260,"title":"Merge sort control flow","steps":[{"type":"start","text":"sort(lo, hi)"},{"type":"decision","text":"lo >= hi?","yes":"no","branch":{"label":"yes","text":"single element is sorted","role":"green"}},{"type":"process","text":"mid = lo + (hi - lo) / 2"},{"type":"process","text":"sort(lo, mid)"},{"type":"process","text":"sort(mid + 1, hi)"},{"type":"process","text":"merge(lo, mid, hi)"},{"type":"end","text":"range sorted"}]}
```
### 9. Step-by-Step Walkthrough

For `[4, 1, 7, 2, 6, 3]`:

| phase | left run | right run | merged result |
|---|---|---|---|
| base merges | `[4]` | `[1]` | `[1,4]` |
| base merges | `[2]` | `[6,3] → [3,6]` | `[2,3,6]` |
| final merge | `[1,4,7]` | `[2,3,6]` | `[1,2,3,4,6,7]` |

The array becomes sorted only on the way back up the recursion tree.

### 10. Why It Works

By strong induction on range length. Length `0` or `1` is sorted. For a larger range, recursive calls sort both halves by induction. The merge invariant always writes the next-smallest remaining value, so the result is sorted and preserves the multiset. Stability follows from choosing the left element when keys compare equal.

### 11. Java Implementation

```java
import java.util.Arrays;

class MergeSortSolution {
    public void sort(int[] nums) {
        if (nums == null || nums.length < 2) return;
        int[] aux = Arrays.copyOf(nums, nums.length);
        sort(nums, aux, 0, nums.length - 1);
    }

    private void sort(int[] nums, int[] aux, int lo, int hi) {
        if (lo >= hi) return;
        int mid = lo + (hi - lo) / 2;
        sort(nums, aux, lo, mid);
        sort(nums, aux, mid + 1, hi);
        merge(nums, aux, lo, mid, hi);
    }

    private void merge(int[] nums, int[] aux, int lo, int mid, int hi) {
        for (int p = lo; p <= hi; p++) aux[p] = nums[p];

        int i = lo;
        int j = mid + 1;
        for (int k = lo; k <= hi; k++) {
            if (i > mid) nums[k] = aux[j++];
            else if (j > hi) nums[k] = aux[i++];
            else if (aux[i] <= aux[j]) nums[k] = aux[i++]; // left-first tie keeps stability
            else nums[k] = aux[j++];
        }
    }
}
```

### 12. Code Walkthrough

`aux` is allocated once and reused. Each merge copies only the active range before overwriting `nums`. The comparison uses `<=`, not `<`, so equal elements from the left half remain before equal elements from the right half.

### 13. Complexity

!!! complexity "Complexity"
    **T:** `Θ(n log n)` in best, average, and worst cases: `Θ(log n)` levels × `Θ(n)` merge work per level. **S:** `Θ(n)` auxiliary array plus `Θ(log n)` recursion stack; dominant extra space is `Θ(n)`.

### 14. Edge Cases

- Empty or one-element arrays are already sorted.
- Duplicate values test stability.
- Already sorted arrays still cost `Θ(n log n)` unless a skip-merge optimization is added.
- Large arrays should not allocate a fresh helper at every recursive call.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Using `<` instead of `<=` makes the sort unstable. Allocating a new helper array inside every merge creates unnecessary allocation churn and can obscure the intended `O(n)` auxiliary-space design.

### 16. Optimization

If `nums[mid] <= nums[mid + 1]`, the halves are already globally ordered and merge can be skipped. Small ranges can switch to insertion sort for constants; neither changes the worst-case bound.

### 17. Alternatives

Quicksort is often faster in-place on arrays but is not stable and has a bad worst case without safeguards. Heap sort is in-place and worst-case `O(n log n)` but not stable. TimSort exploits existing runs and is stable for Java object arrays.

### 18. Interview Follow-Ups

- Sort a linked list in `O(n log n)`.
- Count inversions while sorting.
- External sort files too large for memory.
- Make the implementation generic with `Comparator<T>`.

### 19. Variations

- Bottom-up iterative merge sort.
- Natural merge sort over detected runs.
- Multiway merge for `k` sorted streams.

### 20. Pattern Connection

Merge sort is the canonical split/solve/combine algorithm. It also enables cross-boundary counting: if a right value beats a block of remaining left values, a single comparison can certify many pairs.

---

## Count Inversions

!!! pattern "Pattern: Merge-Augmented Counting · T: O(n log n) · S: O(n)"
    **Signals:** count pairs `(i, j)` with `i < j` and `nums[i] > nums[j]`; brute force is `O(n²)` but sorted halves would expose batches.

### 1. The Problem

Count inversions in an array: pairs `(i, j)` such that `i < j` and `nums[i] > nums[j]`. The answer can be `n(n-1)/2`, so return `long`.

### 2. The Intuition

An inversion is left-only, right-only, or crosses the midpoint. Recursion counts the first two. During merge, if the current right value is smaller than the current left value, it is smaller than every remaining value in the sorted left half.

### 3. The Naive Approach

Check every pair with nested loops. It is direct and correct, but `O(n²)`.

### 4. The Key Observation 🔑

!!! key "Key observation"
    In merge, if `aux[i] > aux[j]`, then `aux[i..mid]` are all greater than `aux[j]`. Add `mid - i + 1` cross inversions immediately, then move `aux[j]`.

### 5. Pattern Recognition

**Signals.** Count ordered pairs, compare earlier and later elements, and sorted halves would let one comparison represent many pairs.

**Recognition shortcut.** Ask: *"When a right-half element wins during merge, does it certify a batch of cross pairs?"*

**Related problems.** Reverse pairs, count smaller after self, range-sum count.

### 6. The Invariant

`countAndSort(lo, hi)` returns the exact number of inversions with both indices in `lo..hi` and leaves `nums[lo..hi]` sorted. During merge, before writing `k`, the count includes all cross inversions involving right-half elements already emitted.

### 7. Visual Explanation

```diagram
{"type":"recursion","nodes":[{"id":"all","label":"[5,3,2,4,1]\ncount + sort","x":3,"y":0,"role":"primary"},{"id":"left","label":"left half\nlocal inversions","x":1,"y":1,"role":"panel"},{"id":"right","label":"right half\nlocal inversions","x":5,"y":1,"role":"panel"},{"id":"cross","label":"merge sorted halves\ncount cross pairs","x":3,"y":2,"role":"amber"},{"id":"done","label":"sorted range\n+ total count","x":3,"y":3,"role":"green"}],"edges":[{"from":"all","to":"left","label":"solve","color":"primary"},{"from":"all","to":"right","label":"solve","color":"primary"},{"from":"left","to":"cross","label":"sorted left","color":"muted"},{"from":"right","to":"cross","label":"sorted right","color":"muted"},{"from":"cross","to":"done","label":"combine","color":"green"}]}
```

Suppose the merge sees left `[2,3,5]` and right `[1,4]`.

```diagram
{"type":"array","values":[2,3,5,1,4],"highlights":{"0":"green","1":"green","2":"green","3":"red"},"pointers":[{"name":"i","index":0,"color":"green","side":"top"},{"name":"j","index":3,"color":"red","side":"top"},{"name":"k","index":0,"color":"primary","side":"bottom"}],"brackets":[{"from":0,"to":2,"label":"remaining left: 3 items","color":"green","row":0},{"from":3,"to":4,"label":"right","color":"red","row":0}],"caption":"Because 1 < 2, count (2,1), (3,1), and (5,1): add mid - i + 1 = 3."}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":470,"box":270,"title":"Count inversions with merge","steps":[{"type":"start","text":"countAndSort(lo, hi)"},{"type":"decision","text":"lo >= hi?","yes":"no","branch":{"label":"yes","text":"return 0","role":"green"}},{"type":"process","text":"left = countAndSort(lo, mid)"},{"type":"process","text":"right = countAndSort(mid + 1, hi)"},{"type":"process","text":"cross = mergeAndCount(lo, mid, hi)"},{"type":"end","text":"return left + right + cross"}]}
```
### 9. Step-by-Step Walkthrough

For `[5, 3, 2, 4, 1]`:

| merge | sorted left | sorted right | cross additions |
|---|---|---|---|
| `[5] + [3]` | `[5]` | `[3]` | `3` beats `[5]` → `+1` |
| `[3,5] + [2]` | `[3,5]` | `[2]` | `2` beats `[3,5]` → `+2` |
| `[4] + [1]` | `[4]` | `[1]` | `1` beats `[4]` → `+1` |
| `[2,3,5] + [1,4]` | `[2,3,5]` | `[1,4]` | `1` beats `[2,3,5]` → `+3`; `4` beats `[5]` → `+1` |

Total inversions: `8`.

### 10. Why It Works

Every inversion belongs to exactly one disjoint set: left-only, right-only, or cross-midpoint. Recursive calls count and sort the first two sets. For a cross pair, sorted left order means when `aux[j] < aux[i]`, all remaining left values are greater than `aux[j]`; each such pair is counted once when that right value is emitted.

### 11. Java Implementation

```java
class CountInversionsSolution {
    public long countInversions(int[] nums) {
        if (nums == null || nums.length < 2) return 0L;
        int[] aux = new int[nums.length];
        return countAndSort(nums, aux, 0, nums.length - 1);
    }

    private long countAndSort(int[] nums, int[] aux, int lo, int hi) {
        if (lo >= hi) return 0L;
        int mid = lo + (hi - lo) / 2;
        long count = countAndSort(nums, aux, lo, mid);
        count += countAndSort(nums, aux, mid + 1, hi);
        count += mergeAndCount(nums, aux, lo, mid, hi);
        return count;
    }

    private long mergeAndCount(int[] nums, int[] aux, int lo, int mid, int hi) {
        for (int p = lo; p <= hi; p++) aux[p] = nums[p];

        long inversions = 0L;
        int i = lo;
        int j = mid + 1;
        for (int k = lo; k <= hi; k++) {
            if (i > mid) nums[k] = aux[j++];
            else if (j > hi) nums[k] = aux[i++];
            else if (aux[i] <= aux[j]) nums[k] = aux[i++];
            else {
                inversions += mid - i + 1L;
                nums[k] = aux[j++];
            }
        }
        return inversions;
    }
}
```

### 12. Code Walkthrough

The recursive method returns a count and mutates the range into sorted order. The `<=` branch prevents equal values from being counted; inversion requires strict `>`. `mid - i + 1L` widens the batch count before accumulation.

### 13. Complexity

!!! complexity "Complexity"
    **T:** `Θ(n log n)` from `T(n)=2T(n/2)+Θ(n)`. Counting adds O(1) work per merged element. **S:** `Θ(n)` auxiliary array plus `Θ(log n)` stack.

### 14. Edge Cases

- Sorted input → `0`.
- Reverse-sorted input → `n(n-1)/2`.
- Equal values are not inversions.
- Negative values require no special handling.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Adding only `1` when the right value wins gives a wrong count. Using `<` in the left-choice branch counts equal values as inversions, violating the strict definition.

### 16. Optimization

If `nums[mid] <= nums[mid + 1]`, there are no cross inversions and the merge can be skipped because the range is already sorted.

### 17. Alternatives

A Fenwick tree with coordinate compression also counts inversions in `O(n log n)` and is useful for online scans. Balanced BST approaches work but are more duplicate-prone in Java. Merge augmentation is usually the clearest interview solution.

### 18. Interview Follow-Ups

- Count reverse pairs where `nums[i] > 2 * nums[j]`.
- Count smaller elements after each index.
- Count inversions modulo a prime.
- Count swaps needed to transform one permutation into another.

### 19. Variations

- Linked-list inversion counting via merge sort.
- Iterative bottom-up merge to avoid recursion.
- Count cross-boundary violations for custom comparators.

### 20. Pattern Connection

This is merge sort plus an aggregate. Recursively solve local facts, sort as a side effect, and compute cross facts during linear combine.

---

## Quickselect

!!! pattern "Pattern: Partition-Based Selection · T: expected O(n) · S: O(1) iterative"
    **Signals:** k-th smallest/largest, median, order statistic, or top-k threshold without needing a fully sorted array.

### 1. The Problem

Given an unsorted array and zero-based rank `k`, return the k-th smallest element. `k = 0` is the minimum; `k = n - 1` is the maximum.

### 2. The Intuition

Partitioning around a pivot puts the pivot into its final sorted position. If that position is `k`, return it. If it is smaller than `k`, search right; if larger, search left. Only one side can still contain the answer.

### 3. The Naive Approach

Sort and return `nums[k]`. This is `O(n log n)` and orders every element. A heap may be `O(n log k)`, but a single offline order statistic can be found in expected linear time.

### 4. The Key Observation 🔑

!!! key "Key observation"
    Partition gives the pivot's exact rank in the current segment. With Lomuto partition, values left of `p` are `<= pivot` and values right of `p` are `> pivot`; therefore rank `k` can lie on only one side unless `p == k`.

### 5. Pattern Recognition

**Signals.** "k-th," "median," "order statistic," "threshold," and no requirement to output sorted order.

**Recognition shortcut.** Ask: *"After one partition, can I prove one side cannot contain the target rank?"*

**Related problems.** Kth Largest Element, median selection, top-k thresholding, wiggle sort.

### 6. The Invariant

At loop start, target rank `k` lies in active interval `[lo, hi]`. After `partition(nums, lo, hi)` returns `p`, `nums[p]` has final sorted rank `p`; all indices `< p` hold values `<= nums[p]`, and all indices `> p` hold values `> nums[p]`. Updating `hi = p - 1` or `lo = p + 1` preserves the invariant.

### 7. Visual Explanation

```diagram
{"type":"recursion","nodes":[{"id":"n","label":"n items\npartition O(n)","x":3,"y":0,"role":"primary"},{"id":"discard1","label":"discard side\nrank impossible","x":1,"y":1,"role":"muted"},{"id":"keep1","label":"keep target side\nexpected n/2","x":5,"y":1,"role":"amber"},{"id":"discard2","label":"discard","x":4,"y":2,"role":"muted"},{"id":"keep2","label":"keep\nexpected n/4","x":6,"y":2,"role":"amber"},{"id":"ans","label":"pivot rank = k","x":6,"y":3,"role":"green"}],"edges":[{"from":"n","to":"discard1","label":"not recursed","color":"muted","dash":true},{"from":"n","to":"keep1","label":"recurse","color":"primary"},{"from":"keep1","to":"discard2","label":"not recursed","color":"muted","dash":true},{"from":"keep1","to":"keep2","label":"recurse","color":"primary"},{"from":"keep2","to":"ans","label":"found","color":"green"}]}
```

Expected work is `n + n/2 + n/4 + ... = O(n)` because only the target side continues.

```diagram
{"type":"array","values":[7,2,9,4,1,6],"highlights":{"5":"purple","0":"amber","1":"green","3":"green","4":"green"},"pointers":[{"name":"lo","index":0,"color":"primary","side":"bottom"},{"name":"i","index":3,"color":"green","side":"top"},{"name":"j","index":4,"color":"amber","side":"top"},{"name":"pivot","index":5,"color":"purple","side":"bottom"},{"name":"hi","index":5,"color":"primary","side":"bottom"}],"brackets":[{"from":0,"to":3,"label":"<= pivot after swaps","color":"green","row":0},{"from":4,"to":4,"label":"> pivot scan","color":"amber","row":0}],"caption":"Lomuto invariant: nums[lo..i] <= pivot, nums[i+1..j-1] > pivot, nums[j..hi-1] unknown."}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":470,"box":275,"title":"Quickselect loop","steps":[{"type":"start","text":"target rank k"},{"type":"process","text":"random pivot\npartition [lo, hi]"},{"type":"decision","text":"p == k?","yes":"yes","branch":{"label":"yes","text":"return nums[p]","role":"green"}},{"type":"decision","text":"p < k?","yes":"yes","branch":{"label":"no","text":"hi = p - 1","role":"primary"}},{"type":"process","text":"lo = p + 1"},{"type":"process","text":"continue"}]}
```
### 9. Step-by-Step Walkthrough

Find rank `k = 2` in `[7,2,9,4,1,6]`.

| step | pivot final index | array shape | decision |
|---|---:|---|---|
| pivot `6` | `3` | `[2,4,1,6,9,7]` | `3 > 2`, keep left |
| pivot `1` | `0` | `[1,4,2,6,9,7]` | `0 < 2`, keep right |
| pivot `4` | `2` | `[1,2,4,6,9,7]` | `2 == k`, return `4` |

The array is only partially ordered; rank is certified without full sorting.

### 10. Why It Works

Partition correctness is a rank certificate. If the pivot lands at `p`, every index left has value `<= nums[p]` and every index right has value `> nums[p]`, so the pivot is at final ascending rank `p`. If `k < p`, ranks `p..hi` are too large; if `k > p`, ranks `lo..p` are too small. The invariant ensures the target is never discarded.

### 11. Java Implementation

```java
import java.util.concurrent.ThreadLocalRandom;

class QuickselectSolution {
    public int kthSmallest(int[] nums, int k) {
        if (nums == null || nums.length == 0) {
            throw new IllegalArgumentException("nums must be non-empty");
        }
        if (k < 0 || k >= nums.length) {
            throw new IllegalArgumentException("k is zero-based and must be in [0, n)");
        }

        int lo = 0;
        int hi = nums.length - 1;
        while (lo <= hi) {
            int pivotIndex = ThreadLocalRandom.current().nextInt(lo, hi + 1);
            swap(nums, pivotIndex, hi);
            int p = partition(nums, lo, hi);
            if (p == k) return nums[p];
            if (p < k) lo = p + 1;
            else hi = p - 1;
        }
        throw new AssertionError("unreachable when k is valid");
    }

    private int partition(int[] nums, int lo, int hi) {
        int pivot = nums[hi];
        int i = lo - 1;
        for (int j = lo; j < hi; j++) {
            if (nums[j] <= pivot) {
                swap(nums, ++i, j);
            }
        }
        swap(nums, i + 1, hi);
        return i + 1;
    }

    private void swap(int[] nums, int i, int j) {
        int tmp = nums[i];
        nums[i] = nums[j];
        nums[j] = tmp;
    }
}
```

### 12. Code Walkthrough

`k` is zero-based. A random pivot is swapped to `hi`, then Lomuto partition places it at `p`. The loop narrows only the side containing `k`, which is the difference between Quickselect and quicksort.

### 13. Complexity

!!! complexity "Complexity"
    **T:** expected `Θ(n)` with randomized pivots; worst-case `Θ(n²)` if partitions are repeatedly extreme. **S:** `Θ(1)` for the iterative implementation.

### 14. Edge Cases

- `k = 0` returns minimum; `k = n - 1` returns maximum.
- Duplicates are valid; equal values occupy a range of ranks.
- Input is mutated.
- Invalid `k` should throw.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Confusing one-based `k` with zero-based rank causes off-by-one errors. Recursing into both sides accidentally writes quicksort and loses expected linear selection.

### 16. Optimization

Three-way partitioning is better for duplicate-heavy arrays because it stops when `k` falls inside the equal band. Median-of-three improves constants; randomization is the simpler adversarial-order defense.

### 17. Alternatives

Sorting costs `O(n log n)` but is simplest. A size-`k` heap costs `O(n log k)` and supports streaming/top-k. Median-of-medians gives deterministic `O(n)` but is rarely required in interviews.

### 18. Interview Follow-Ups

- Convert to k-th largest.
- Select median.
- Return top k elements after finding the threshold.
- Handle duplicates with Dutch National Flag partition.

### 19. Variations

- Hoare partition with careful return semantics.
- Recursive randomized Quickselect.
- Deterministic median-of-medians selection.

### 20. Pattern Connection

Quickselect is the selection sibling of quicksort: both partition, but selection discards one side. The core pattern is rank pruning.

---

## Kth Largest Element

!!! pattern "Pattern: Quickselect Rank Conversion · T: expected O(n) · S: O(1)"
    **Signals:** k-th largest in an unsorted array, single order statistic, and mutation allowed.

### 1. Problem

Given `int[] nums` and one-based `k`, return the k-th largest value. In ascending sorted order, the k-th largest sits at zero-based rank `nums.length - k`.

### 2. Key Observation

!!! key "Key observation"
    Kth largest is Quickselect with rank conversion: `target = n - k`. Keep the partition written for ascending ranks; only the target index changes.

### 3. Invariant

The active interval `[lo, hi]` always contains ascending rank `target`. After partition returns `p`, `nums[p]` has final ascending rank `p`; if `p < target`, discard the left side, otherwise discard the right side. Duplicates are handled as rank positions, not distinct values.

### 4. Diagram

```diagram
{"type":"array","values":[3,2,1,5,6,4],"highlights":{"4":"green"},"pointers":[{"name":"target = n - k = 4","index":4,"color":"green","side":"bottom"}],"brackets":[{"from":0,"to":5,"label":"ascending ranks 0..5; k=2 largest maps to rank 4","color":"primary","row":0}],"caption":"The second largest value is the element that would land at ascending index 4."}
```

### 5. Java

```java
import java.util.concurrent.ThreadLocalRandom;

class KthLargestSolution {
    public int findKthLargest(int[] nums, int k) {
        if (nums == null || nums.length == 0) {
            throw new IllegalArgumentException("nums must be non-empty");
        }
        if (k < 1 || k > nums.length) {
            throw new IllegalArgumentException("k is one-based and must be in [1, n]");
        }

        int target = nums.length - k;
        int lo = 0;
        int hi = nums.length - 1;
        while (lo <= hi) {
            int pivotIndex = ThreadLocalRandom.current().nextInt(lo, hi + 1);
            swap(nums, pivotIndex, hi);
            int p = partition(nums, lo, hi);
            if (p == target) return nums[p];
            if (p < target) lo = p + 1;
            else hi = p - 1;
        }
        throw new AssertionError("unreachable when k is valid");
    }

    private int partition(int[] nums, int lo, int hi) {
        int pivot = nums[hi];
        int i = lo - 1;
        for (int j = lo; j < hi; j++) {
            if (nums[j] <= pivot) {
                swap(nums, ++i, j);
            }
        }
        swap(nums, i + 1, hi);
        return i + 1;
    }

    private void swap(int[] nums, int i, int j) {
        int tmp = nums[i];
        nums[i] = nums[j];
        nums[j] = tmp;
    }
}
```

### 6. Complexity

!!! complexity "Complexity"
    **T:** expected `Θ(n)` with randomized pivots; worst-case `Θ(n²)` under repeatedly extreme partitions. **S:** `Θ(1)` extra space because partitioning is in-place and iterative.

### 7. Implementation Notes

Validate `k` as one-based. Convert once to `target = n - k`, then reason only in zero-based ascending ranks. The input array is mutated; copy first if callers require preservation.

### 8. Pattern Connection

This is Quickselect with a rank transform. Cross-reference **Module 10 — Heaps**: a min-heap of size `k` gives `O(n log k)` time and is preferable for streaming data or when mutation is forbidden; randomized Quickselect is better for one offline array when expected linear time and in-place mutation are acceptable.
