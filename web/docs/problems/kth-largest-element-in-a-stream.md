# Top-K / Heap — Kth Largest Element in a Stream

*[↗ LeetCode: Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/top-k-heap)

Implement `add(x)` that returns the k-th largest element among all values seen so far.

**Example** — `k=3, init=[4,5,8,2]`; `add(3)=4, add(5)=5, add(10)=5, add(9)=8, add(4)=8`.

---

## Approach 1 — Sort every call

Trivially correct but O(n log n) per call.

## Approach 2 — Min-heap of size k

**Insight.** The k-th largest = smallest of the top-k. Keep a min-heap capped at k. On `add`: offer + evict if oversize; `peek()` is the answer.



```java
class KthLargest {
    PriorityQueue<Integer> heap = new PriorityQueue<>();
    int k;
    public KthLargest(int k, int[] nums) {
        this.k = k;
        for (int x : nums) add(x);
    }
    public int add(int x) {
        heap.offer(x);
        if (heap.size() > k) heap.poll();
        return heap.peek();
    }
}
```



<CodeTrace
  title="Stream — k=3, init=[4,5,8,2], add(3), add(5)"
  :values="[4,5,8,2,3,5]"
  :windowKeys="['op']"
  :cellWidth="42"
  :steps='[
    { pointers: { op: 3 }, vars: { heap: "[4,5,8]", peek: 4 }, note: "after init: top-3 = {4,5,8}" },
    { pointers: { op: 4 }, vars: { heap: "[4,5,8]", peek: 4 }, note: "add 3: offered but 3 lt 4 → evicted. peek stays 4", added: [4] },
    { pointers: { op: 5 }, vars: { heap: "[5,5,8]", peek: 5 }, note: "add 5: replaces 4 → new peek = 5", added: [5] }
  ]'
/>

**Complexity** — Time **O(log k)** per add; Space **O(k)**. Optimal.

## Complexity summary

| Approach | Time (per add) | Space |
|---|---|---|
| Sort | O(n log n) | O(n) |
| Min-heap size k | **O(log k)** | O(k) |

## Related problems

- [Kth Largest Element in an Array](/problems/quickselect-kth-largest) — offline version
- [Top K Frequent Elements](/problems/top-k-frequent-elements) — heap or bucket
- [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) — two heaps
