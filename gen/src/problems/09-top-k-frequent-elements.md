# Top-K / Heap — Top K Frequent Elements

*[↗ LeetCode: Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/top-k-heap)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Uber, Bloomberg" />

Given `nums` and integer `k`, return the `k` most frequent elements (any order).

**Example 1** — `nums=[1,1,1,2,2,3], k=2` → `[1,2]`
**Example 2** — `nums=[1], k=1` → `[1]`

**Constraints** — `1 ≤ n ≤ 10⁵`; `1 ≤ k ≤ #distinct`.


<Hints
  hint1="You need the k largest/smallest. Sort is O(n log n). Can you do O(n log k)?"
  hint2="Maintain a heap of size k. Min-heap → k largest at root candidates; max-heap → k smallest."
  hint3="For ’k closest’ or ’k most frequent’, the heap’s comparator holds the distance/frequency metric."
/>
---

<MarkSolved problem-slug="top-k-frequent-elements" />


## Approach 1 — Sort by frequency

**Intuition.** Count frequencies. Sort entries by frequency desc. Take the top `k`.

```java
int[] topKFrequentSort(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    List<int[]> pairs = new ArrayList<>();
    for (var e : freq.entrySet()) pairs.add(new int[]{e.getKey(), e.getValue()});
    pairs.sort((a, b) -> b[1] - a[1]);
    int[] out = new int[k];
    for (int i = 0; i < k; i++) out[i] = pairs.get(i)[0];
    return out;
}
```

**Complexity** — Time **O(n + m log m)** where `m` = distinct count; Space **O(m)**.

---

## Approach 2 — Min-heap of size k

**Insight from sort.** We don't need all m elements sorted; just the top k. A **min-heap** of size k evicts the smallest each insert; the root is the k-th largest frequency at the end.

**Trap.** Wrong polarity — a max-heap of all m needs O(m log m). Min-heap of size k does O(m log k).

```java
int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    for (var e : freq.entrySet()) {
        heap.offer(new int[]{e.getKey(), e.getValue()});
        if (heap.size() > k) heap.poll();
    }
    int[] out = new int[k];
    for (int i = k - 1; i >= 0; i--) out[i] = heap.poll()[0];
    return out;
}
```

<CodeTrace
  title="Min-heap size k — nums=[1,1,1,2,2,3], k=2"
  :values="[1,1,1,2,2,3]"
  :windowKeys="['step']"
  :cellWidth="38"
  :steps='[
    { pointers: { step: 0 }, vars: { freq: "{1:3, 2:2, 3:1}" }, note: "count frequencies" },
    { pointers: { step: 1 }, vars: { heap: "[(3,1)]" }, note: "offer 1 (freq 3)" },
    { pointers: { step: 2 }, vars: { heap: "[(2,2),(3,1)]" }, note: "offer 2 (freq 2). size = k" },
    { pointers: { step: 3 }, vars: { heap: "[(2,2),(3,1)]" }, note: "3 has freq 1, less than min(2) → skipped (offered then popped)", added: [0,3] }
  ]'
/>

**Complexity** — Time **O(n + m log k)**; Space **O(m + k)**. Great when `k << m`.

---

## Approach 3 — Bucket sort by frequency

**Insight from heap.** Frequencies are bounded by `n`. Instead of sorting, put each element into a bucket indexed by its frequency; walk buckets from high to low.

```java
int[] topKFrequentBucket(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    List<Integer>[] buckets = new List[nums.length + 1];
    for (var e : freq.entrySet()) {
        int f = e.getValue();
        if (buckets[f] == null) buckets[f] = new ArrayList<>();
        buckets[f].add(e.getKey());
    }
    int[] out = new int[k];
    int i = 0;
    for (int f = buckets.length - 1; f >= 1 && i < k; f--)
        if (buckets[f] != null) for (int x : buckets[f]) { out[i++] = x; if (i == k) break; }
    return out;
}
```

**Complexity** — Time **O(n)**; Space **O(n)**. Optimal.

---

## Try it yourself

<JavaRunner problem-slug="top-k-frequent-elements" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Sort by freq | O(n + m log m) | O(m) |
| Min-heap of size k | O(n + m log k) | O(m + k) |
| Bucket sort | **O(n)** | O(n) |

## When to use which

- **k tiny compared to m** → heap is idiomatic and easy to defend.
- **Interviewer probes "beat log k"** → bucket sort. Trades a bit of space for O(n).

<AiCompanion problem-slug="top-k-frequent-elements" pattern-hint="top-K / heap" />

## Related problems (same ladder applies)

- [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) — same shape with distance instead of freq
- [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) — min-heap of size k over a stream
- [Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) — heap on rows
- [Reorganize String](https://leetcode.com/problems/reorganize-string/) — max-heap on char frequencies

<FeedbackWidget problem-slug="top-k-frequent-elements" />
