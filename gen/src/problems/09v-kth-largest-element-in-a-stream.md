# Top-K / Heap — Kth Largest Element in a Stream

*[↗ LeetCode: Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/top-k-heap)

<CompanyTags companies="Meta, Amazon, Google, Bloomberg" />

Design a class `KthLargest`. Constructor takes `k` and an initial array; `add(val)` returns the k-th largest element after inserting `val` into the stream.

**Example 1** —
```
KthLargest kthLargest = new KthLargest(3, [4,5,8,2]);
kthLargest.add(3);   // returns 4
kthLargest.add(5);   // returns 5
kthLargest.add(10);  // returns 5
kthLargest.add(9);   // returns 8
kthLargest.add(4);   // returns 8
```

**Constraints** — `1 ≤ k ≤ 10⁴`; `0 ≤ nums.length ≤ 10⁴`; `-10⁴ ≤ vals ≤ 10⁴`; at most `10⁴` `add` calls.


<Hints
  hint1="You need the k largest/smallest. Sort is O(n log n). Can you do O(n log k)?"
  hint2="Maintain a heap of size k. Min-heap → k largest at root candidates; max-heap → k smallest."
  hint3="For ’k closest’ or ’k most frequent’, the heap’s comparator holds the distance/frequency metric."
/>
---

<MarkSolved problem-slug="kth-largest-element-in-a-stream" /> <Bookmark problem-slug="kth-largest-element-in-a-stream" />

<InterviewTimer problem-slug="kth-largest-element-in-a-stream" />



## Approach 1 — Re-sort on every add

**Intuition.** Store all values; sort on each `add`; return `arr[n - k]`.

**Complexity** — Time **O(n log n)** per add; too slow.

---

## Approach 2 — Min-heap of size k

**Insight from re-sort.** We only ever care about the k largest values seen so far. A **min-heap of size k** whose root is the k-th largest.

- On `add(val)`: push. If heap size > k, poll the smallest. The root is now the k-th largest.

```java
class KthLargest {
    PriorityQueue<Integer> pq;
    int k;
    KthLargest(int k, int[] nums) {
        this.k = k;
        pq = new PriorityQueue<>();
        for (int x : nums) add(x);
    }
    public int add(int val) {
        pq.offer(val);
        if (pq.size() > k) pq.poll();
        return pq.peek();
    }
}
```

<CodeTrace
  title="Min-heap k=3, init=[4,5,8,2]"
  :values="['4','5','8','2','3','5','10','9','4']"
  :windowKeys="['idx']"
  :cellWidth="30"
  :steps='[
    { pointers: { idx: 3 }, vars: { heap: "[4,5,8]" }, note: "init: after 4 vals size>k, dropped smallest(2)" },
    { pointers: { idx: 4 }, vars: { heap: "[4,5,8]", ret: 4 }, note: "add(3): push, size=4, poll 3 → heap [4,5,8], root=4" },
    { pointers: { idx: 6 }, vars: { heap: "[5,8,10]", ret: 5 }, note: "add(5) → [5,4,5,8]→pop 4 → [5,5,8]; add(10) → drop 5 → [5,8,10]; root=5" },
    { pointers: { idx: 8 }, vars: { heap: "[8,9,10]", ret: 8 }, note: "add(9): drop 5; add(4): push then drop 4; root=8" }
  ]'
/>

**Complexity** — Time **O(log k)** per `add`; Space **O(k)**.

---

## Approach 3 — Sorted TreeMap (with counts if duplicates allowed)

**Insight from heap.** A `TreeMap<Integer, Integer>` (value → count) also supports "kth largest" in O(log k). Not simpler than a heap, but useful if you need range queries too.

**Complexity** — Same as heap.

---

## Try it yourself

<JavaRunner problem-slug="kth-largest-element-in-a-stream" />

## Complexity summary

| Approach | Time per add | Space | Interview grade |
|---|---|---|---|
| Re-sort | O(n log n) | O(n) | baseline; TLE at 10⁴ adds |
| Min-heap of size k | **O(log k)** | **O(k)** | canonical |
| TreeMap | O(log k) | O(n) | overkill unless range queries needed |

## When to use which

- **Streaming k-th largest** → min-heap of size k.
- **Streaming k-th smallest** → max-heap of size k.
- **Both k-th largest AND range queries** → TreeMap.
- **`k` very large (close to n)** → maintain running sort; heap advantage vanishes.

<AiCompanion problem-slug="kth-largest-element-in-a-stream" pattern-hint="top-K / heap" />

## Related problems

- [Top K Frequent Elements](/problems/top-k-frequent-elements)
- [K Closest Points to Origin](/problems/k-closest-points-to-origin)
- [Kth Largest Element in an Array](/problems/quickselect-kth-largest) — offline sibling
- [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) — two-heap for streaming median

<FeedbackWidget problem-slug="kth-largest-element-in-a-stream" />

<RelatedProblems problems="k-way-merge-k-sorted-lists::K Way Merge K Sorted Lists|ugly-number-ii::Ugly Number II|k-closest-points-to-origin::K Closest Points To Origin" />
