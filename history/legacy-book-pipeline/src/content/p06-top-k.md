## The Pattern

Top-K problems ask for the largest, smallest, or most frequent `k` items without necessarily requiring full ordering. The default senior-level move is a **size-k heap**: keep only the best `k` candidates seen so far, ejecting the current worst inside that kept set.

!!! pattern "Recognition signals"
    **Signals:** "k largest/smallest", "top k frequent", "kth largest", stream-like input, or output size much smaller than input size. If you do not need all `n` elements sorted, full sort is usually overkill.

```diagram
{"type":"tree","title":"Size-k min-heap for k largest","values":[7,10,9],"highlights":{"0":"amber"},"labels":{"0":"root = smallest kept","1":"kept","2":"kept"},"caption":"For k largest, the min-heap root is the cutoff. A new value larger than 7 replaces it; smaller values are ignored."}
```

## The Invariant

After processing any prefix, the heap contains exactly the best `min(k, prefixLength)` elements under the desired ranking. For k-largest, that means the heap is a min-heap and `peek()` is the smallest among the kept winners; anything not in the heap is no better than `peek()`.

## Template

```java
List<Integer> topKLargest(int[] nums, int k) {
    PriorityQueue<Integer> heap = new PriorityQueue<>(); // min-heap
    for (int x : nums) {
        heap.offer(x);
        if (heap.size() > k) heap.poll();
    }
    List<Integer> ans = new ArrayList<>(heap);
    ans.sort(Comparator.reverseOrder());
    return ans;
}
```

For custom records, use safe comparators:

```java
PriorityQueue<int[]> heap = new PriorityQueue<>(
    (a, b) -> Integer.compare(a[1], b[1]) // frequency ascending
);
```

Use **quickselect** when you only need the kth threshold in an array and average O(n) is acceptable; use a heap when data is streaming, `k` is small, or deterministic behavior is easier to explain.

## Worked Recognition

- **Kth Largest Element** (Module 10): a size-`k` min-heap leaves the kth largest at `peek()`. Quickselect is the faster average-time alternative when mutation is allowed.
- **Top K Frequent Elements** (Module 10): count frequencies, then keep a size-`k` heap ordered by frequency. Avoid sorting all distinct values unless `k` is close to `m`.
- **Merge K Sorted Lists** (Module 10): the heap stores one current node per list. This is a "top one repeated" variant: repeatedly poll the smallest head and push its successor.

## Complexity

!!! complexity "Complexity"
    **T:** O(n log k) for a size-k heap, plus optional O(k log k) output ordering. Full sort is O(n log n). Quickselect is O(n) average and O(n²) worst without robust pivoting. **S:** O(k), or O(m) extra when a frequency map over `m` distinct keys is required.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Using a max-heap for k-largest and accidentally storing all `n` elements; returning heap iteration order as sorted order; writing `b - a` comparators that overflow; ignoring tie-breaking requirements; or choosing quickselect when the input is a stream.

## When NOT to use it

Do not use a heap if the problem requires a total sorted order of all elements, if `k` is essentially `n`, or if a bounded counting/bucket strategy gives linear time with simpler ordering guarantees.
