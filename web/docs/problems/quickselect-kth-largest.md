# Quickselect — Kth Largest Element in an Array

*[↗ LeetCode: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/quickselect)

Given `nums` and integer `k`, return the k-th **largest** element (1-indexed). O(n) average time expected.

**Example 1** — `nums=[3,2,1,5,6,4], k=2` → `5`
**Example 2** — `nums=[3,2,3,1,2,4,5,5,6], k=4` → `4`

**Constraints** — `1 ≤ k ≤ n ≤ 10⁵`; `-10⁴ ≤ nums[i] ≤ 10⁴`.

---

## Approach 1 — Sort + index

**Intuition.** Sort ascending; return `nums[n - k]`.



```java
int findKthLargestSort(int[] nums, int k) {
    Arrays.sort(nums);
    return nums[nums.length - k];
}
```



**Complexity** — Time **O(n log n)**; Space **O(1)** (Timsort in-place).

---

## Approach 2 — Min-heap of size k

**Insight from sort.** We don't need all n sorted — just the top k. Push each; if heap &gt; k, evict smallest. Root is the k-th largest.



```java
int findKthLargestHeap(int[] nums, int k) {
    PriorityQueue<Integer> heap = new PriorityQueue<>();
    for (int x : nums) { heap.offer(x); if (heap.size() > k) heap.poll(); }
    return heap.peek();
}
```



**Complexity** — Time **O(n log k)**; Space **O(k)**. Good when `k << n`.

---

## Approach 3 — Quickselect (Hoare's partition, average O(n))

**Insight from heap.** We only need one k-th boundary. Quickselect partitions around a pivot and recurses into only the side containing k → linear expected time.

**Trap.** A bad pivot (e.g. always last element on sorted input) blows up to O(n²). Randomize.



```java
int findKthLargest(int[] nums, int k) {
    int target = nums.length - k;                        // index in ascending order
    Random rng = new Random();
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int p = partition(nums, lo, hi, rng);
        if (p == target) return nums[p];
        else if (p < target) lo = p + 1;
        else                 hi = p - 1;
    }
    return nums[lo];
}
int partition(int[] a, int lo, int hi, Random rng) {
    int pivotIdx = lo + rng.nextInt(hi - lo + 1);
    int pivot = a[pivotIdx];
    swap(a, pivotIdx, hi);
    int store = lo;
    for (int i = lo; i < hi; i++) if (a[i] < pivot) swap(a, store++, i);
    swap(a, store, hi);
    return store;
}
void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }
```



<CodeTrace
  title="Quickselect — nums=[3,2,1,5,6,4], k=2 (target idx=4)"
  :values="[3,2,1,5,6,4]"
  :windowKeys="['lo','hi']"
  :cellWidth="42"
  :steps='[
    { pointers: { lo: 0, hi: 5, pivotIdx: 5 }, vars: { pivot: 4 }, note: "pick pivot 4; partition → [3,2,1,4,6,5]. store=3" },
    { pointers: { lo: 4, hi: 5, pivotIdx: 5 }, vars: { pivot: 5, target: 4 }, note: "3 lt 4 → search right. partition [6,5] → store=4", added: [4] },
    { pointers: { lo: 4, hi: 4 }, vars: { answer: 5 }, note: "store == target → return 5" }
  ]'
/>

**Complexity** — Time **O(n)** expected, **O(n²)** worst; Space **O(1)**. Optimal on average.

---

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Sort | O(n log n) | O(1) |
| Min-heap size k | O(n log k) | O(k) |
| Quickselect | **O(n) avg** | **O(1)** |

## When to use which

- **Interviewer wants "expected O(n)"** → quickselect.
- **Streaming input** → min-heap size k (quickselect needs the whole array).
- **k = 1** → linear scan is enough.

## Related problems (same ladder applies)

- [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) — quickselect by distance
- [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) — quickselect by frequency
- [Wiggle Sort II](https://leetcode.com/problems/wiggle-sort-ii/) — quickselect to find median, then three-way partition
- [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) — two heaps (streaming counterpart)
