## The Pattern

Quickselect finds the kth order statistic by partitioning around a pivot, placing that pivot at its final sorted index, and recursing into only the side that can contain the target. It borrows quicksort's partition but discards half the search space instead of sorting both halves.

!!! pattern "Recognition signals"
    **Signals:** kth smallest/largest, median, percentile, threshold value, array may be mutated, and full sorted order is unnecessary. If the interviewer asks for average O(n), think randomized quickselect; if they require streaming or deterministic bounds, consider a heap or median-of-medians.

```diagram
{"type":"array","title":"Partition narrows the kth search to one side","values":[9,1,7,3,6,5,8],"index":["lo",1,"i",3,"j","pivot","hi"],"highlights":{"0":"amber","1":"green","3":"green","4":"purple","5":"primary","6":"amber"},"pointers":[{"name":"lo","index":0,"color":"amber","side":"top"},{"name":"i","index":2,"color":"green","side":"bottom"},{"name":"j","index":4,"color":"purple","side":"bottom"},{"name":"pivot","index":5,"color":"primary","side":"top"},{"name":"hi","index":6,"color":"amber","side":"top"}],"caption":"Partition moves values less than the pivot left and greater values right; once pivot lands at p, compare p with the target index k."}
```

## The Invariant

During partition, elements before the store pointer are strictly less than the pivot under the chosen ordering, and scanned elements after it are greater than or equal until proven otherwise. After the final swap, the pivot index `p` is exactly its sorted position: every index `< p` is no larger for kth-smallest, and every index `> p` is no smaller. Therefore only one side can contain `k`.

## Template

```java
int kthLargest(int[] nums, int k) {
    int target = nums.length - k; // kth largest == sorted index n-k
    Random random = new Random();
    int lo = 0, hi = nums.length - 1;

    while (lo <= hi) {
        int pivotIndex = lo + random.nextInt(hi - lo + 1);
        int p = partition(nums, lo, hi, pivotIndex);
        if (p == target) return nums[p];
        if (p < target) lo = p + 1;
        else hi = p - 1;
    }
    throw new IllegalArgumentException("k is out of range");
}

int partition(int[] a, int lo, int hi, int pivotIndex) {
    int pivot = a[pivotIndex];
    swap(a, pivotIndex, hi);
    int store = lo;
    for (int i = lo; i < hi; i++) {
        if (a[i] < pivot) {
            swap(a, store, i);
            store++;
        }
    }
    swap(a, store, hi);
    return store;
}

void swap(int[] a, int i, int j) {
    int tmp = a[i];
    a[i] = a[j];
    a[j] = tmp;
}
```

Duplicates are fine: strict `< pivot` puts equals on the right, still giving a valid pivot position. For many duplicates, a three-way partition can shrink faster.

## Worked Recognition

- **Kth Largest Element** (Modules 10/15): convert to target sorted index `n - k`, partition, and recurse/iterate into one side. This is the canonical quickselect use case.
- Median of an unsorted array: select index `n / 2` without sorting all values; for even `n`, select both middle indices if the exact statistical median is required.
- Contrast with **Top-K / Heap** (Module 10): a size-`k` heap is O(n log k), deterministic, and stream-friendly; quickselect is expected O(n), in-place, but mutates the array and has randomized performance.

## Complexity

!!! complexity "Complexity"
    **T:** Expected O(n) because each random pivot discards a constant fraction in expectation; worst-case O(n²) if pivots are repeatedly extreme. Randomizing the pivot prevents adversarial sorted-input behavior in normal interviews. **S:** O(1) for the iterative version, excluding the random generator.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Recursing into both sides like quicksort; confusing kth largest with sorted index `k - 1` instead of `n - k`; failing to randomize pivots; writing partition code that loses the pivot; ignoring duplicate-heavy arrays; or using subtraction comparators in object variants.

## When NOT to use it

Do not use quickselect when the input must remain unmodified, when values arrive as a stream, when you need all top `k` values sorted, or when worst-case O(n) is contractually required. Prefer a heap, full sort, copy-before-select, or median-of-medians depending on the constraint.
