## Concepts & Mental Models

A heap is a **shape-constrained tree** stored as an array. For a zero-indexed binary heap, node `i` has parent `(i - 1) / 2`, left child `2*i + 1`, and right child `2*i + 2`. The tree is always complete: every level is filled left-to-right except possibly the last. That structural guarantee is what makes heap operations logarithmic without pointers.

!!! key "Heap invariant"
    In a **min-heap**, every parent is `<=` its children, so the minimum lives at index 0. In a **max-heap**, every parent is `>=` its children, so the maximum lives at index 0. The heap does **not** fully sort the array; it only guarantees a local parent-child order strong enough to expose one extreme quickly.

```diagram
{"type":"array","values":[2,5,3,9,7,8],"index":true,"highlights":{"0":"green","1":"primary","2":"primary"},"brackets":[{"from":0,"to":0,"label":"root min","color":"green","row":0},{"from":1,"to":2,"label":"children of index 0","color":"primary","row":1}],"caption":"Array layout: parent i has children 2i+1 and 2i+2."}
```

```diagram
{"type":"tree","values":[2,5,3,9,7,8],"highlights":{"0":"green"},"labels":{"0":"i=0","1":"i=1","2":"i=2","3":"i=3","4":"i=4","5":"i=5"}}
```

Two primitive repairs maintain the invariant:

- **Sift-up** after insertion: append the new value at the end, then repeatedly swap it with its parent while it violates parent-child order. Cost O(log n).
- **Sift-down** after removing/replacing the root: move the last element to index 0, then repeatedly swap it with the better child until the invariant is restored. Cost O(log n).

Building a heap by inserting `n` elements costs O(n log n), but bottom-up **heapify** costs O(n): start from the last internal node and sift down each node. Most nodes are near leaves and move only a few levels, so the total work sums to linear time.

!!! pattern "Heap selection idiom"
    When a problem asks for the top/bottom `k` under a stream or one-pass constraint, keep a heap of **size at most k** containing the best candidates seen so far. The root is the *worst* kept candidate; if a new candidate is better, evict the root and insert the candidate. This yields O(n log k) time and O(k) space.

Java's `PriorityQueue` is a min-heap by default. Use `Comparator.comparingInt(...)` or `Integer.compare(...)` for custom order; never use subtraction comparators because integer overflow can reverse ordering.

---

## Kth Largest Element in an Array

!!! pattern "Pattern: Bounded min-heap · T: O(n log k) · S: O(k)"
    **Signals:** kth largest/smallest, no need to fully sort, stream-compatible, `k` much smaller than `n`.

### 1. Problem

Given an integer array `nums` and an integer `k`, return the `k`th largest element. The answer is the element that would appear at index `k - 1` if the array were sorted descending, counting duplicates as separate positions.

### 2. Intuition

You do not need all values sorted; you need only the best `k` values. Maintain a min-heap containing the current `k` largest elements. The smallest among those `k` is exactly the boundary value: all retained elements are at least as large as it, and all discarded elements are no larger than some retained boundary.

### 3. Naive

Sort descending and return `nums[k - 1]`. This is easy and often acceptable, but costs O(n log n) and does unnecessary ordering work. A max-heap of all elements followed by `k` polls also costs O(n + k log n) and stores O(n).

### 4. Key Observation

!!! key "Key observation"
    In a heap of size `k` holding the largest `k` values seen so far, the root of a **min-heap** is the current `k`th largest. Any new value larger than the root belongs in the top `k`; any value `<= root` cannot improve the answer and can be discarded immediately.

### 5. Pattern Recognition

**Signals.** kth extreme, streaming input, large `n`, duplicates allowed, and no requirement to output all top values sorted.

**Shortcut.** For kth largest, keep a min-heap of size `k`; for kth smallest, keep a max-heap of size `k`.

**Related.** Top K Frequent Elements, K Closest Points, smallest range from k lists, online leaderboard thresholds.

### 6. Invariant

After processing any prefix, the heap contains exactly `min(k, prefixLength)` largest values from that prefix. If its size is `k`, `heap.peek()` is the `k`th largest value in that prefix.

### 7. Visual Explanation

```diagram
{"type":"array","values":[3,2,1,5,6,4],"index":true,"highlights":{"3":"green","4":"green","5":"green"},"brackets":[{"from":3,"to":5,"label":"three largest values after full scan","color":"green","row":0}],"caption":"For k=2 the final heap keeps [5,6]; root 5 is the 2nd largest."}
```

```diagram
{"type":"tree","values":[5,6],"highlights":{"0":"amber","1":"green"},"labels":{"0":"kth largest","1":"larger"}}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":460,"box":270,"title":"Bounded min-heap for kth largest","steps":[{"type":"start","text":"heap = empty min-heap"},{"type":"decision","text":"next number x?","yes":"yes","branch":{"label":"no","text":"return heap.peek()","role":"green"}},{"type":"process","text":"offer x"},{"type":"decision","text":"heap.size() > k?","yes":"yes","branch":{"label":"no","text":"continue","role":"primary"}},{"type":"process","text":"poll smallest"},{"type":"process","text":"continue"}]}
```

### 9. Walkthrough

For `nums = [3,2,1,5,6,4]`, `k = 2`:

| x | heap after offer/poll | meaning |
|---|---|---|
| 3 | `[3]` | best one so far |
| 2 | `[2,3]` | best two so far |
| 1 | `[2,3]` | 1 discarded |
| 5 | `[3,5]` | 2 evicted |
| 6 | `[5,6]` | 3 evicted |
| 4 | `[5,6]` | 4 discarded |

### 10. Why It Works

Use induction on the prefix. Before any elements, the invariant is vacuous. When a new value arrives, inserting it creates a set of previous retained candidates plus the new candidate. If the heap exceeds `k`, removing the minimum discards the worst value among these `k + 1` candidates. Every value previously discarded was already no better than a retained boundary at the time it was discarded, so it cannot be needed later. Thus the heap always stores the largest `k` values seen, and its minimum is the kth largest.

### 11. Java

```java
import java.util.PriorityQueue;

class Solution {
    public int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        for (int x : nums) {
            heap.offer(x);
            if (heap.size() > k) heap.poll();
        }
        return heap.peek();
    }
}
```

### 12. Code Walkthrough

The priority queue is a min-heap, so `peek()` is the weakest retained candidate. The loop admits every value, then trims the heap back to size `k`; this compact form handles early prefixes without special cases.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n log k) because the heap never exceeds `k + 1`. **S:** O(k). Sorting is O(n log n); quickselect is expected O(n) and O(1) extra if in-place, but more delicate under adversarial pivots.

### 14. Edge Cases

- `k = 1`: heap keeps only the maximum.
- `k = nums.length`: heap eventually contains every value; root is the minimum.
- Duplicates count as separate ranks, so `[5,5,4]`, `k=2` returns 5.
- Negative values require no special handling.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Using a max-heap of size `k` for kth largest gives fast access to the largest, not the kth largest. Also avoid removing when `heap.size() == k`; trimming must happen only when the size exceeds `k`.

### 16. Optimization

If mutation is allowed and worst-case guarantees are not required, randomized quickselect partitions around a pivot and searches only the side containing index `n - k`. That is expected O(n) time, but the heap solution is deterministic, simple, and stream-friendly.

### 17. Alternatives

- Full sort: simplest, O(n log n), O(1) or O(n) depending on sort implementation.
- Quickselect: expected O(n), worst-case O(n²) without robust pivoting.
- Counting buckets: O(n + range) if the numeric range is small.

### 18. Interview Follow-Ups

What changes for kth smallest? What if elements arrive as a stream? How do you support deleting arbitrary values? How would you make quickselect worst-case linear? How do duplicates affect rank semantics?

### 19. Variations

K closest points, kth smallest in a sorted matrix, top K words, top K events by score, maintaining a rolling percentile over a bounded window.

### 20. Pattern Connection

This is the canonical **bounded heap** pattern: store the best `k`, expose the boundary through the root, and discard everything that cannot cross that boundary.

---

## Top K Frequent Elements

!!! pattern "Pattern: Frequency map + bounded min-heap · T: O(n + m log k) · S: O(m)"
    **Signals:** top K by derived score, frequency/count aggregation first, output order usually irrelevant.

### 1. Problem

Given an integer array `nums` and integer `k`, return any `k` elements with the highest frequencies. Let `m` be the number of distinct values.

### 2. Intuition

The heap should not store every occurrence; it should store **distinct values ranked by frequency**. First compress the stream into a frequency map. Then run the bounded-heap idiom over map entries: keep only the `k` most frequent values, with the least frequent retained value at the root.

### 3. Naive

Sort all distinct values by descending frequency and take the first `k`. This is O(n + m log m). It is clean but sorts more than needed when `k << m`.

### 4. Key Observation

!!! key "Key observation"
    Once frequencies are known, the problem becomes kth/top selection over `m` candidates. A min-heap ordered by frequency and capped at `k` keeps exactly the `k` highest-frequency values; the root is the lowest frequency still allowed into the answer set.

### 5. Pattern Recognition

**Signals.** "Most frequent," "top K," scoring function computed from input, and answer can be returned in any order.

**Shortcut.** Aggregate first, then select. Do not push every raw element into the heap.

**Related.** Top K words, heavy hitters, top K logs by count, top K customers by revenue.

### 6. Invariant

After processing any subset of distinct values, the heap contains `min(k, processedDistinct)` values with highest frequencies among those processed values. If the heap has size `k`, every processed value outside the heap has frequency `<= heap.peek()[1]` or lost an arbitrary tie.

### 7. Visual Explanation

```diagram
{"type":"array","values":[1,1,1,2,2,3],"index":true,"highlights":{"0":"green","1":"green","2":"green","3":"primary","4":"primary","5":"muted"},"caption":"Counts: 1→3, 2→2, 3→1. For k=2, keep values 1 and 2."}
```

```diagram
{"type":"tree","values":[2,1],"highlights":{"0":"amber","1":"green"},"labels":{"0":"value 2\nfreq 2","1":"value 1\nfreq 3"}}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":470,"box":285,"title":"Top K frequent selection","steps":[{"type":"start","text":"count frequencies"},{"type":"process","text":"heap orders entries by frequency ascending"},{"type":"decision","text":"next distinct value?","yes":"yes","branch":{"label":"no","text":"extract heap values","role":"green"}},{"type":"process","text":"offer [value, frequency]"},{"type":"decision","text":"heap.size() > k?","yes":"yes","branch":{"label":"no","text":"continue","role":"primary"}},{"type":"process","text":"poll least frequent retained"}]}
```

### 9. Walkthrough

For `[1,1,1,2,2,3]`, `k = 2`:

| candidate | frequency | heap by frequency | action |
|---|---:|---|---|
| 1 | 3 | `[(1,3)]` | keep |
| 2 | 2 | `[(2,2),(1,3)]` | keep |
| 3 | 1 | `[(2,2),(1,3)]` | insert then evict `(3,1)` |

### 10. Why It Works

The counting pass preserves all information relevant to frequency ranking. The heap pass is the same bounded selection proof as kth largest, with frequency as the ordering key. Whenever `k + 1` candidates are present, evicting the minimum frequency cannot remove a value that must be in some top-`k` answer. Ties may be resolved arbitrarily unless the problem specifies deterministic ordering.

### 11. Java

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Comparator;

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int x : nums) freq.put(x, freq.getOrDefault(x, 0) + 1);

        PriorityQueue<int[]> heap = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        for (Map.Entry<Integer, Integer> e : freq.entrySet()) {
            heap.offer(new int[] { e.getKey(), e.getValue() });
            if (heap.size() > k) heap.poll();
        }

        int[] ans = new int[k];
        for (int i = 0; i < k; i++) ans[i] = heap.poll()[0];
        return ans;
    }
}
```

### 12. Code Walkthrough

The map reduces `n` occurrences to `m` scored candidates. The heap stores pairs `[value, frequency]`, ordered only by frequency. Extracting from the min-heap returns answers from lowest retained frequency to highest, which is valid when any order is accepted.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n + m log k), where `m` is the number of distinct values. **S:** O(m) for the frequency map plus O(k) for the heap and output.

### 14. Edge Cases

- `k == m`: all distinct values are returned.
- All numbers identical: heap size remains 1.
- Negative numbers are normal map keys.
- If deterministic tie order is required, add a safe tie-breaker with `Integer.compare`.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Pushing every occurrence into the heap changes the problem and can degrade to O(n log k) without using the frequency compression. Another frequent bug is sorting or comparing by value instead of by count.

### 16. Optimization

Bucket sort by frequency gives O(n + m) time: create buckets `1..n`, place each value in the bucket for its count, then scan from high frequency down. It uses O(n + m) space and is excellent when linear time is required.

### 17. Alternatives

- Sort distinct entries by frequency: O(n + m log m), compact code.
- Quickselect on entries by frequency: expected O(n + m), but mutates an array of entries.
- Streaming heavy hitters: Misra-Gries approximates candidates with bounded memory when exact counting is impossible.

### 18. Interview Follow-Ups

How would you return results sorted by frequency descending? How do you handle ties lexicographically for strings? What if the input is a distributed stream? What if `k` changes after preprocessing?

### 19. Variations

Top K frequent words, top K URLs, most common error codes, top K by aggregate revenue rather than count, approximate top K in telemetry pipelines.

### 20. Pattern Connection

This problem composes two patterns: **hash aggregation** creates ranked candidates, then a **bounded heap** selects the best `k` without globally sorting them.

---

## Merge K Sorted Lists

!!! pattern "Pattern: K-way merge with heap of heads · T: O(N log k) · S: O(k)"
    **Signals:** multiple sorted streams/lists, repeatedly need the smallest current head, output one merged sorted sequence.

### 1. Problem

Given an array of `k` sorted linked lists, merge them into one sorted linked list and return its head. Let `N` be the total number of nodes across all lists.

### 2. Intuition

At any moment, the next output node must be the smallest among the current heads of the non-empty lists. A min-heap over those heads gives exactly that node in O(log k), and after removing a head, only that same list can contribute a new candidate: the removed node's `next`.

### 3. Naive

Repeatedly scan all `k` current heads to find the minimum, append it, and advance its list. This costs O(Nk). Pairwise merging lists one by one costs O(Nk) in the worst order, though divide-and-conquer improves it to O(N log k).

### 4. Key Observation

!!! key "Key observation"
    Because each list is individually sorted, each list contributes at most one viable candidate at a time: its current head. A heap of these `k` heads is a complete frontier of the merge.

### 5. Pattern Recognition

**Signals.** K sorted sources, next global minimum/maximum from current frontiers, output all elements in sorted order.

**Shortcut.** If each source is sorted, put only one pointer per source in the heap; never heapify every node unless memory is irrelevant.

**Related.** Merge sorted arrays, external sort runs, smallest range covering k lists, streaming log merge.

### 6. Invariant

The heap contains exactly the first unmerged node of every non-empty list. The output list is sorted and contains the globally smallest nodes already removed from the heap. Every unmerged node not in the heap is behind a heap node from the same list and is therefore not smaller than that heap node.

### 7. Visual Explanation

```diagram
{"type":"linkedlist","values":[1,4,5],"pointers":[{"name":"head A","index":0}]}
```

```diagram
{"type":"tree","values":[1,1,2],"highlights":{"0":"green"},"labels":{"0":"A:1","1":"B:1","2":"C:2"}}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":480,"box":300,"title":"Heap frontier for k-way merge","steps":[{"type":"start","text":"push each non-null list head"},{"type":"decision","text":"heap empty?","yes":"no","branch":{"label":"yes","text":"return dummy.next","role":"green"}},{"type":"process","text":"node = poll smallest head"},{"type":"process","text":"append node to output"},{"type":"decision","text":"node.next exists?","yes":"yes","branch":{"label":"no","text":"continue","role":"primary"}},{"type":"process","text":"offer node.next"}]}
```

### 9. Walkthrough

Lists: `A: 1→4→5`, `B: 1→3→4`, `C: 2→6`.

| poll | append | offer next | heap heads after step |
|---|---|---|---|
| A:1 | 1 | A:4 | B:1, C:2, A:4 |
| B:1 | 1 | B:3 | C:2, B:3, A:4 |
| C:2 | 2 | C:6 | B:3, A:4, C:6 |
| B:3 | 3 | B:4 | A:4, B:4, C:6 |

### 10. Why It Works

By the invariant, the heap contains every list's smallest unmerged node. The minimum heap node is therefore no greater than any node in its own list and no greater than the current head of every other list; since later nodes in other lists are also no smaller than their heads, the polled node is globally smallest. Appending it preserves sorted order. Advancing only its list restores the frontier invariant.

### 11. Java

```java
import java.util.Comparator;
import java.util.PriorityQueue;

class Solution {
    static class ListNode {
        int val;
        ListNode next;
        ListNode() {}
        ListNode(int val) { this.val = val; }
        ListNode(int val, ListNode next) { this.val = val; this.next = next; }
    }

    public ListNode mergeKLists(ListNode[] lists) {
        PriorityQueue<ListNode> heap = new PriorityQueue<>(Comparator.comparingInt(node -> node.val));
        for (ListNode head : lists) {
            if (head != null) heap.offer(head);
        }

        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (!heap.isEmpty()) {
            ListNode node = heap.poll();
            tail.next = node;
            tail = tail.next;
            if (node.next != null) heap.offer(node.next);
        }
        return dummy.next;
    }
}
```

### 12. Code Walkthrough

The heap stores node references, not copied values, so the result reuses existing nodes. The dummy node removes head-special-case logic. After polling a node, offering `node.next` advances exactly one input list and preserves the heap frontier.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(N log k), where each of `N` nodes is offered and polled once and the heap has at most `k` nodes. **S:** O(k) for the heap, excluding the output list nodes reused from input.

### 14. Edge Cases

- `lists` is empty or all heads are null: return null.
- Some lists are empty: skip null heads.
- Duplicate values: comparator allows equality; any stable ordering among equal nodes is valid.
- Very large node values: `Comparator.comparingInt` avoids overflow.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Comparing nodes with `a.val - b.val` can overflow. Another subtle bug is pushing all nodes at once, which works but wastes O(N) space and ignores the sorted-list structure.

### 16. Optimization

Divide-and-conquer pairwise merge also gives O(N log k) time and O(1) auxiliary space beyond recursion/iteration, often with better constants because it avoids heap operations. The heap version is superior when lists are streams or when `k` is dynamic.

### 17. Alternatives

- Sequentially merge into one list: simple but O(Nk) worst case.
- Divide-and-conquer merging: O(N log k), good for batch lists.
- Heap of all nodes: O(N log N) or O(N) heapify plus polls, but O(N) space.

### 18. Interview Follow-Ups

How would you merge iterators instead of linked lists? What if values tie and you need stable source order? How would you support infinite streams? How do you adapt this to arrays with index pointers?

### 19. Variations

Smallest range covering elements from k sorted lists, merge k sorted arrays, external merge sort, time-ordered event/log merge across shards.

### 20. Pattern Connection

This is **frontier expansion**: the heap contains the next candidate from each sorted source. It is the heap analogue of the merge step in merge sort.

---

## Find Median from Data Stream

!!! pattern "Pattern: Two heaps · T: O(log n) add, O(1) median · S: O(n)"
    **Signals:** online median, dynamic ordered prefix, need fast insert and fast middle query.

### 1. Problem

Design a data structure supporting `addNum(int num)` and `findMedian()`. The median is the middle value when the count is odd, or the average of the two middle values when the count is even.

### 2. Intuition

Split the numbers into two halves. The lower half lives in `lo`, a max-heap, so its largest value is accessible. The upper half lives in `hi`, a min-heap, so its smallest value is accessible. The median is either `lo.peek()` or the average of `lo.peek()` and `hi.peek()`.

### 3. Naive

Maintain a sorted array/list and insert each number at its sorted position. Median lookup is O(1), but insertion costs O(n) because elements shift. Sorting from scratch after every insertion is O(n log n) per update.

### 4. Key Observation

!!! key "Key observation"
    The median depends only on the maximum of the lower half and the minimum of the upper half. Two heaps maintain exactly those boundary values while avoiding full ordering inside each half.

### 5. Pattern Recognition

**Signals.** Running median, continuous inserts, percentile-like boundary, and no need to enumerate sorted order.

**Shortcut.** Use two heaps whenever a dynamic order statistic sits between a lower partition and an upper partition.

**Related.** Sliding window median, running percentile, load threshold balancing, online quantiles.

### 6. Invariant

Maintain both invariants after every insertion:

1. **Order invariant:** every value in `lo` is `<=` every value in `hi`.
2. **Balance invariant:** `lo.size() == hi.size()` or `lo.size() == hi.size() + 1`.

Thus `lo` may hold one extra value, making `lo.peek()` the median for odd counts.

### 7. Visual Explanation

```diagram
{"type":"tree","values":[5,3,2],"highlights":{"0":"green"},"labels":{"0":"lo max=5\nsize=3","1":"3","2":"2"}}
```

```diagram
{"type":"tree","values":[8,10,9],"highlights":{"0":"primary"},"labels":{"0":"hi min=8\nsize=3","1":"10","2":"9"}}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":500,"box":315,"title":"Insert while preserving order and balance","steps":[{"type":"start","text":"lo=max-heap, hi=min-heap"},{"type":"decision","text":"lo empty or x <= lo.peek()?","yes":"yes","branch":{"label":"no","text":"offer x to hi","role":"primary"}},{"type":"process","text":"offer x to lo"},{"type":"decision","text":"lo.size() > hi.size()+1?","yes":"yes","branch":{"label":"no","text":"check other side","role":"primary"}},{"type":"process","text":"hi.offer(lo.poll())"},{"type":"decision","text":"hi.size() > lo.size()?","yes":"yes","branch":{"label":"no","text":"done","role":"green"}},{"type":"process","text":"lo.offer(hi.poll())"}]}
```

### 9. Walkthrough

Insert `5, 2, 8, 10, 3`:

| add | lo (lower half) | hi (upper half) | median |
|---:|---|---|---:|
| 5 | `[5]` | `[]` | 5 |
| 2 | `[2]` | `[5]` | 3.5 |
| 8 | `[5,2]` | `[8]` | 5 |
| 10 | `[5,2]` | `[8,10]` | 6.5 |
| 3 | `[5,3,2]` | `[8,10]` | 5 |

### 10. Why It Works

The order invariant ensures all lower-half values are no larger than all upper-half values, so the only possible middle candidates are the two heap roots. The balance invariant pins the rank: if sizes are equal, the two roots straddle the middle; if `lo` has one extra, its root is exactly the middle element. Rebalancing by moving a root preserves order because the moved value is the boundary value of its old side.

### 11. Java

```java
import java.util.PriorityQueue;

class MedianFinder {
    private final PriorityQueue<Integer> lo = new PriorityQueue<>((a, b) -> Integer.compare(b, a));
    private final PriorityQueue<Integer> hi = new PriorityQueue<>();

    public void addNum(int num) {
        if (lo.isEmpty() || num <= lo.peek()) {
            lo.offer(num);
        } else {
            hi.offer(num);
        }

        if (lo.size() > hi.size() + 1) {
            hi.offer(lo.poll());
        } else if (hi.size() > lo.size()) {
            lo.offer(hi.poll());
        }
    }

    public double findMedian() {
        if (lo.size() > hi.size()) return lo.peek();
        return ((long) lo.peek() + hi.peek()) / 2.0;
    }
}
```

### 12. Code Walkthrough

`lo` is a max-heap via `Integer.compare(b, a)`, which avoids overflow. New values are routed by the current lower boundary. Rebalancing enforces that `lo` is never smaller than `hi` and never more than one larger. The median average casts to `long` before addition to avoid integer overflow.

### 13. Complexity

!!! complexity "Complexity"
    **T:** `addNum` is O(log n); `findMedian` is O(1). **S:** O(n) for storing all inserted values across the two heaps.

### 14. Edge Cases

- First insertion: goes to `lo`; median is its root.
- Even count: average the two roots using `long` before addition.
- Negative and duplicate values work naturally.
- `findMedian` is assumed to be called after at least one insertion unless an API contract says otherwise.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Letting either heap exceed the other by more than one breaks rank semantics. Also avoid a max-heap comparator like `(a, b) -> b - a`; it can overflow for extreme integers.

### 16. Optimization

For known bounded integer ranges, a Fenwick tree or counting array can answer median by rank with O(log R) or O(R) behavior. For general unbounded streams, two heaps are the interview-standard exact solution.

### 17. Alternatives

- Balanced BST/multiset with middle iterator: O(log n) insert and O(1) median, but Java lacks a built-in multiset with iterator rank maintenance.
- Sorted list: O(n) insertion.
- Approximate quantile sketches: sublinear memory but approximate medians.

### 18. Interview Follow-Ups

How do you support deletions for sliding window median? How would you handle weighted medians? Can you generalize to arbitrary percentiles? What if memory cannot grow with the stream?

### 19. Variations

Sliding Window Median, data-stream percentile dashboards, online load balancing by median, continuously tracking lower/upper quartiles with multiple heap partitions.

### 20. Pattern Connection

Two heaps model a dynamically maintained partition: one heap exposes the lower boundary, the other exposes the upper boundary. This pattern generalizes to online order statistics where only partition boundaries matter.

---

## Meeting Rooms II

### Problem

Given meeting intervals `[start, end)`, return the minimum number of rooms required so that no overlapping meetings share a room.

### Key Observation

!!! key "Key observation"
    Process meetings in ascending start time. A room becomes reusable exactly when its earliest ending meeting has `end <= currentStart`. Therefore a min-heap of active meeting end times exposes the next room that frees.

### Invariant

Before scheduling the current meeting, the heap contains end times for exactly the meetings that have started but not yet been released. After polling all end times `<= start` and offering the current `end`, `heap.size()` equals the number of rooms currently occupied. The answer is the maximum size ever reached.

### Diagram

```diagram
{"type":"flow","width":470,"box":290,"title":"Sweep starts; heap stores active end times","steps":[{"type":"start","text":"sort intervals by start"},{"type":"process","text":"for [s,e] in order"},{"type":"decision","text":"heap.peek() <= s?","yes":"yes","branch":{"label":"no","text":"room still occupied","role":"red"}},{"type":"process","text":"poll freed room(s)"},{"type":"process","text":"offer e; update max rooms"},{"type":"end","text":"return max"}]}
```

### Java

```java
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;

class Solution {
    public int minMeetingRooms(int[][] intervals) {
        if (intervals.length == 0) return 0;

        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));
        PriorityQueue<Integer> ends = new PriorityQueue<>();
        int rooms = 0;

        for (int[] meeting : intervals) {
            int start = meeting[0];
            int end = meeting[1];
            while (!ends.isEmpty() && ends.peek() <= start) {
                ends.poll();
            }
            ends.offer(end);
            rooms = Math.max(rooms, ends.size());
        }
        return rooms;
    }
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n log n) for sorting plus O(n log n) heap operations. **S:** O(n) in the worst case when all meetings overlap.

### Pattern Connection

This is a sweep-line with a heap-backed active set. Sorting gives chronological order; the min-heap answers the only active-set query required: which room frees first?

