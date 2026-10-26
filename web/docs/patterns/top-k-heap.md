# Top-K / Heap


<PatternVideo pattern-name="Top-K / Heap" duration="8–12 min" />

<PatternProgress pattern-id="top-k-heap" problems="top-k-frequent-elements, k-closest-points-to-origin, kth-largest-element-in-a-stream, reorganize-string" />

<script setup>
const theTemplateSpecializations = [
  { slug: `top-k-smallest-heap-of-k-bare-mechanic-medium`, title: `Top-K Smallest (heap-of-K bare mechanic)` },
  { slug: `top-k-frequent-elements-medium`, title: `Top K Frequent Elements` },
  { slug: `k-closest-points-to-origin-medium`, title: `K Closest Points to Origin` },
  { slug: `kth-largest-in-array-medium`, title: `Kth Largest in Array` },
  { slug: `find-median-from-data-stream-two-heap-hard`, title: `Find Median from Data Stream (two-heap)` },
  { slug: `task-scheduler-max-heap-greedy-medium`, title: `Task Scheduler (max-heap greedy)` },
]

const theTemplateCode = `// Top-K via size-k heap of the OPPOSITE polarity:
//   k LARGEST  -&gt; MIN-heap (root = weakest-of-winners, cheap to evict).
//   k SMALLEST -&gt; MAX-heap (root = largest-of-winners).
// Each item is offered once; the heap stays bounded at size k.
&lt;Item&gt; List&lt;Item&gt; topK(Iterable&lt;Item&gt; items, int k, Comparator&lt;Item&gt; worstFirst) {
    PriorityQueue&lt;Item&gt; heap = new PriorityQueue&lt;&gt;(worstFirst);
    for (Item item : items) {
        heap.offer(item);
        if (heap.size() &gt; k) {
            heap.poll();                         // evict the worst-of-winners
        }
    }
    List&lt;Item&gt; out = new ArrayList&lt;&gt;();
    while (!heap.isEmpty()) out.add(heap.poll());
    return out;                                   // worst-to-best order
}`

const topKSmallestCode = `// Top-K Smallest — MAX-heap of size k; root = largest kept = next to evict.
int[] topKSmallest(int[] nums, int k) {
    PriorityQueue&lt;Integer&gt; maxHeap = new PriorityQueue&lt;&gt;((a, b) -&gt; b - a);
    for (int x : nums) {
        maxHeap.offer(x);
        if (maxHeap.size() &gt; k) maxHeap.poll();  // drop the largest kept
    }
    int[] out = new int[k];
    for (int i = k - 1; i &gt;= 0; i--) out[i] = maxHeap.poll();
    return out;
}`

const topKFrequentCode = `// Top K Frequent Elements — MIN-heap of size k keyed on frequency.
int[] topKFrequent(int[] nums, int k) {
    Map&lt;Integer, Integer&gt; freq = new HashMap&lt;&gt;();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    PriorityQueue&lt;Integer&gt; pq = new PriorityQueue&lt;&gt;(
        (a, b) -&gt; Integer.compare(freq.get(a), freq.get(b)));
    for (int key : freq.keySet()) {
        pq.offer(key);
        if (pq.size() &gt; k) pq.poll();            // drop least-frequent kept
    }
    int[] res = new int[k];
    for (int i = k - 1; i &gt;= 0; i--) res[i] = pq.poll();
    return res;
}`

const kClosestPointsCode = `// K Closest Points to Origin — MAX-heap of size k keyed on squared distance.
// sqrt is monotone so compare on squared distance to avoid floating-point.
int[][] kClosest(int[][] points, int k) {
    PriorityQueue&lt;int[]&gt; heap = new PriorityQueue&lt;&gt;((a, b) -&gt; {
        int da = a[0]*a[0] + a[1]*a[1], db = b[0]*b[0] + b[1]*b[1];
        return Integer.compare(db, da);           // farthest at root
    });
    for (int[] p : points) {
        heap.offer(p);
        if (heap.size() &gt; k) heap.poll();         // evict the farthest
    }
    int[][] res = new int[k][2];
    for (int i = 0; i &lt; k; i++) res[i] = heap.poll();
    return res;
}`

const kthLargestStreamCode = `// Kth Largest in a Stream — size-k MIN-heap kept alive across add() calls.
class KthLargest {
    private final int k;
    private final PriorityQueue&lt;Integer&gt; pq = new PriorityQueue&lt;&gt;();

    public KthLargest(int k, int[] nums) {
        this.k = k;
        for (int x : nums) add(x);
    }

    public int add(int val) {
        pq.offer(val);
        if (pq.size() &gt; k) pq.poll();
        return pq.peek();                         // root of min-heap = k-th largest
    }
}`

const medianStreamCode = `// Find Median from Data Stream — TWO heaps:
//   low  = max-heap of the smaller half (root = largest of the small half)
//   high = min-heap of the larger half (root = smallest of the large half)
// Invariant: size(low) == size(high) or size(low) == size(high)+1.
class MedianFinder {
    private final PriorityQueue&lt;Integer&gt; low  = new PriorityQueue&lt;&gt;((a, b) -&gt; b - a);
    private final PriorityQueue&lt;Integer&gt; high = new PriorityQueue&lt;&gt;();

    public void addNum(int num) {
        low.offer(num);                           // tentative add to low half
        high.offer(low.poll());                   // move its max to high
        if (high.size() &gt; low.size()) {
            low.offer(high.poll());               // rebalance so low has ceil(n/2)
        }
    }

    public double findMedian() {
        return low.size() == high.size()
            ? (low.peek() + high.peek()) / 2.0
            : low.peek();
    }
}`

const taskSchedulerCode = `// Task Scheduler — greedy max-heap: pick the most-frequent runnable task.
// Cooldown enforced by a holding queue that releases tasks back when cooldown expires.
int leastInterval(char[] tasks, int n) {
    int[] counts = new int[26];
    for (char c : tasks) counts[c - 'A']++;
    PriorityQueue&lt;Integer&gt; heap = new PriorityQueue&lt;&gt;((a, b) -&gt; b - a);
    for (int c : counts) if (c &gt; 0) heap.offer(c);
    Deque&lt;int[]&gt; cooldown = new ArrayDeque&lt;&gt;();   // (releaseAt, remainingCount)
    int time = 0;
    while (!heap.isEmpty() || !cooldown.isEmpty()) {
        time++;
        if (!heap.isEmpty()) {
            int c = heap.poll() - 1;
            if (c &gt; 0) cooldown.offer(new int[]{time + n, c});
        }
        if (!cooldown.isEmpty() && cooldown.peek()[0] == time) {
            heap.offer(cooldown.poll()[1]);
        }
    }
    return time;
}`

const topKInvariant = {
  statement: `After processing any prefix of the input, the heap contains EXACTLY the best min(k, prefix_size) elements seen so far. The root is the worst-of-the-winners — the next candidate to evict if a better one arrives.`,
  initialization: `Before iteration 0: heap is empty. The invariant holds vacuously (prefix size is 0, no winners yet).`,
  maintenance: `Each iteration offers the new item (heap size temporarily becomes previous_best + 1). If this exceeds k, poll the root — which, by heap ordering, is the worst-of-the-winners under the current comparator. Correctness: either (a) the new item was better than the root and now kicks out the old-root as planned, or (b) the new item IS the current worst and gets kicked out immediately. In both cases, the heap holds exactly the best k.`,
  termination: `After processing all n items, the heap contains the globally-best k items. Successive polls yield them in worst-to-best order (reverse this if the caller wants best-to-worst).`,
}

const topKComplexity = { time: `O(n log k) — n insertions each O(log k) on a bounded heap`, space: `O(k) for the heap plus any extra bookkeeping (freq map for Top-K Frequent)` }

const mastery5 = [
  {
    q: `For "k LARGEST" with the heap-of-k template, which polarity do you use?`,
    choices: [
      { text: `MIN-heap — the root is the smallest of the current top-k, cheap to evict`, correct: true, explanation: `Opposite-polarity rule: the root should be "the next thing I would throw away." For k largest, that's the smallest kept.` },
      { text: `MAX-heap — put the largest at the root`, correct: false, explanation: `That gives you k SMALLEST, not k largest.` },
      { text: `MIN-heap of size n`, correct: false, explanation: `Wasteful — defeats the point of heap-of-k.` },
      { text: `A BST`, correct: false, explanation: `Also works but with worse constants and more code.` },
    ],
  },
  {
    q: `Time complexity of maintaining top-k over n elements with the heap-of-k template?`,
    choices: [
      { text: `O(n log k) — n insertions each on a bounded size-k heap`, correct: true, explanation: `Each offer/poll is O(log(current_size)) which stays ≤ O(log k). Beats O(n log n) full sort when k ≪ n.` },
      { text: `O(n log n)`, correct: false, explanation: `That's full sort — wasteful when k ≪ n.` },
      { text: `O(k log n)`, correct: false },
      { text: `O(n + k)`, correct: false },
    ],
  },
  {
    q: `For Find Median from Data Stream, why TWO heaps?`,
    choices: [
      { text: `A max-heap on the smaller half + min-heap on the larger half; the roots give O(1) median access`, correct: true, explanation: `Each addNum rebalances both heaps so their sizes differ by at most 1. Median is low.peek() (odd total) or (low.peek() + high.peek()) / 2 (even total).` },
      { text: `For redundancy — one validates the other`, correct: false },
      { text: `One for even positions, one for odd`, correct: false },
      { text: `To support concurrent reads`, correct: false },
    ],
  },
  {
    q: `For streaming "Kth Largest Element in a Stream", what does the heap root hold at any point?`,
    choices: [
      { text: `The current k-th largest value — the min of the k best seen so far`, correct: true, explanation: `Min-heap root is the smallest of the k winners, which is exactly the k-th largest overall.` },
      { text: `The largest value ever seen`, correct: false, explanation: `That's the 1st largest, not k-th.` },
      { text: `The newest value`, correct: false },
      { text: `A sentinel`, correct: false },
    ],
  },
  {
    q: `Quickselect vs size-k Heap for OFFLINE top-k (order irrelevant, k ~ n/2): which is better on average?`,
    choices: [
      { text: `Quickselect, O(n) average — avoids the O(log k) heap factor`, correct: true, explanation: `When k ≈ n/2, O(n log k) ≈ O(n log n), losing the heap advantage. Quickselect's expected O(n) wins. Heap remains the safer worst-case choice.` },
      { text: `Heap, always`, correct: false, explanation: `Heap is bounded worst-case but slower on average when k is not small.` },
      { text: `Both equal`, correct: false },
      { text: `Merge sort`, correct: false, explanation: `Full sort is strictly worse than both.` },
    ],
  },
]
</script>

## Why top-k heaps exist — the story

Imagine you are watching a live scoreboard with millions of scores, but the product manager only cares about the top 10. Sorting every score every time would be silly: rank 11 through rank 1,000,000 do not matter. The Top-K heap pattern exists because you can keep a tiny "VIP room" of size `k` instead of arranging the whole crowd. Every new candidate enters the room briefly; if the room is too full, you kick out the worst person currently inside. At the end, the room contains exactly the best `k` candidates.

<HeapAnim />

Use a concrete example: find the 3 largest numbers in `[7, 1, 9, 3, 10, 2, 8]`. Keep a min-heap of size 3. Read `7,1,9` → heap has `{1,7,9}`. Read `3` → heap becomes `{1,3,7,9}`, too large, so remove the smallest `1`; room is `{3,7,9}`. Read `10` → remove `3`; room is `{7,9,10}`. Read `2` → remove `2` immediately. Read `8` → remove `7`; final room is `{8,9,10}`. Notice the heap root is not the answer to "largest"; it is the weakest of the winners, the one easiest to evict.

The brute-force walk-through is full sorting: arrange everyone, then take the first `k`. Can we do better? Yes, because the exact order of the rejected `n-k` items does not matter. Keep only the current boundary set.

That opposite-polarity idea is the whole trick. For k largest, use a min-heap. For k smallest, use a max-heap. For k most frequent, use a min-heap ordered by frequency. The heap is not there to sort everything; it is there to maintain a moving boundary between "still in the top k" and "not good enough."

<Callout kind="key" title="Key Insight">

For k *largest*, use a **min**-heap (its root is the worst-of-the-best, cheap to evict). For k *smallest*, use a **max**-heap. Polarity is always the opposite of the goal.

</Callout>

## When to use it — boundary items without sorting

Top-K heap is the interview pattern for "I need a small elite set from a large input." It is especially strong when `k` is much smaller than `n`, when the input is streaming, or when the final order of the selected items does not matter.

### Recognize by
- "k largest", "k smallest", "top k", "bottom k"
- "k most frequent", "k least frequent", "most common words"
- "k closest to origin" or "nearest k elements" where the ranking key is computed from each item
- "kth largest in a stream" where values arrive over time and you must answer after each add
- "return any order" or "relative order among the top k does not matter"
- constraints like `n = 10^5` and `k` small enough that O(n log k) is attractive

### When NOT to use it
You need the k-th value **once** and don't care about the other k−1 boundary items. **Quickselect** is O(n) average and beats the heap's O(n log k). Use a heap when the input arrives as a **stream** (you can't Quickselect it) or when you need *all* k boundary items.

Also avoid a heap when you need the complete sorted order of all values; then sorting is simpler and honest. If the key range is tiny or bounded, bucket sort can beat the heap: for frequencies from 0 to n, buckets often give O(n). If `k` is close to `n`, O(n log k) becomes close to O(n log n), so the benefit shrinks.

## THE template

Every Top-K-heap problem is a specialization of **"maintain a size-k heap of the OPPOSITE polarity to the goal; the root is the worst-of-the-winners, cheap to evict."** Four parameters distinguish the sub-variations: what's being ranked (value, frequency, distance), what the ranking key is derived from (direct, aux map), whether the heap stays alive across queries (streaming), and whether you need two heaps (median).

<PatternTemplateCard
  slug="top-k-heap-template"
  title="Size-k heap with opposite-polarity root"
  language="java"
  :code="theTemplateCode"
  :invariant="topKInvariant"
  :complexity="topKComplexity"
  :specializations="theTemplateSpecializations"
/>

## Traps & gotchas

<TrapTrace
  title="Trap 1 — Wrong heap polarity"
  bug="For 'k LARGEST', instinct says 'max-heap'. nums=[3,1,5,2,4], k=2 with a MAX-heap of all 5: builds then pops 2 times to extract {5,4} — that's O(n log n) work. Also, with the opposite polarity used as a size-k heap, the algorithm silently returns the WRONG values (keeps the smallest instead of the largest)."
  fix="Rule: 'the root is the next thing I would throw away.' k largest → smallest kept is next to go → MIN-heap. k smallest → MAX-heap. Say the polarity aloud before writing the comparator. Size-k heap stays O(n log k)."
/>

<TrapTrace
  title="Trap 2 — Subtraction comparator overflow on int keys"
  bug="PriorityQueue<Integer> pq = new PriorityQueue<>((a, b) -> b - a); — looks correct for max-heap. But when a = Integer.MIN_VALUE and b = 1, b - a overflows to Integer.MIN_VALUE + 1 (negative), inverting the comparison. On adversarial inputs the heap order is corrupted and the top-k result is wrong."
  fix="Always use Integer.compare(b, a) for max-heap or Integer.compare(a, b) for min-heap. The compare method handles the full int range correctly. Same rule for Long.compare, Double.compare."
/>

<TrapTrace
  title="Trap 3 — Streaming add() after batch-filling misses the heap-size invariant"
  bug="class KthLargest { PriorityQueue<Integer> pq = new PriorityQueue<>(); public KthLargest(int k, int[] nums) { for (int x : nums) pq.offer(x); } public int add(int v) { pq.offer(v); return pq.peek(); } } — if the initial array has 10 items and k=3, the heap holds 10 (not 3), and the root is the OVERALL min, not the 3rd largest. Returns the wrong answer."
  fix="Trim to k during BOTH the constructor and add(): after every offer, if (pq.size() > k) pq.poll(). The invariant 'size == min(k, items_seen)' must hold at all times, not just steady-state."
/>

## History — Williams's heap, 1964

The binary heap was invented by **J.W.J. Williams** in 1964 as the core data structure of **heapsort**. Williams's paper introduced both the heap-invariant maintenance operations (sift-up, sift-down) and the array-based tree representation using index arithmetic — parent at `(i-1)/2`, children at `2i+1` and `2i+2`. That representation lets a heap live entirely in a contiguous `int[]` with zero pointer overhead, which is why every language's standard library ships a heap-backed `PriorityQueue`.

The **k-way merge** algorithm — used in every external sort since von Neumann's 1945 tape-sort memo — is built on the same heap idea, with the heap holding one live iterator per input stream. Modern implementations include Lucene's segment merging, DuckDB's external sort, and Kafka's log compaction.

The specific Top-K-on-a-stream pattern was formalized in the **NIST Text REtrieval Conference (TREC)** benchmarks in the late 1990s as *"top-K retrieval,"* and later applied to trending / recommendation systems at Google, Facebook, and Twitter. Every "top trending topic" list you see is a Top-K heap in disguise.

## Sub-variations of the template

<PatternSubVariationNav pattern="top-k-heap" />

The sub-variations below walk the template through six canonical uses — bare mechanic (top-k smallest with max-heap), frequency-keyed selection, geometry-keyed selection, streaming kth-largest, two-heap median, and max-heap greedy for scheduling. Each uses the opposite-polarity-root rule; what changes is the ranking key and whether the heap persists across queries.

### Top-K Smallest (heap-of-K bare mechanic) <span class="diff diff-m">Medium</span>

The simplest instance of the template. Given `nums[]` and `k`, return the `k` smallest values in any order. Keep a size-`k` **max-heap**: the root is the largest kept — if a new item is smaller, evict the root; otherwise discard the new item.

<Callout kind="inv" title="Invariant">

After processing each new element, the max-heap holds exactly the `min(k, elements_seen)` smallest values seen so far. Its root is the largest among the kept, which is the next candidate for eviction.

</Callout>

<InvariantProof
  statement="At the end of any iteration i, the heap contains the k smallest values from nums[0..i], and the root is the largest among them (the worst-of-winners)."
  initialization="Before iteration 0: heap is empty. The invariant holds vacuously (no winners yet)."
  maintenance="Iteration i offers nums[i]. If the heap size exceeds k, poll the root (max-heap root = largest kept). Correctness: either (a) nums[i] was smaller than the previous root and the previous root is now correctly evicted, or (b) nums[i] IS the current worst and is immediately evicted. In both cases the heap holds the k smallest of nums[0..i]."
  termination="After iteration n-1, the heap holds the k smallest values of nums[]. Successive polls yield them in largest-to-smallest order."
/>

<Callout kind="key" title="Blind-solve prompt">

*Before revealing:* given `nums=[3,2,1,5,6,4]` and `k=3`, return the 3 smallest. Trace the heap state after each insertion. Why does the opposite-polarity rule mean "max-heap for k smallest"?

</Callout>

<TemplateReveal
  slug="top-k-smallest"
  language="java"
  :canonical="topKSmallestCode"
/>

**Trace** on `nums=[3,2,1,5,6,4]`, `k=3`:

| i | nums[i] | after offer | after poll (if size&gt;k) | heap holds |
|---|---|---|---|---|
| 0 | 3 | `[3]` | — | `{3}` |
| 1 | 2 | `[3,2]` | — | `{3,2}` |
| 2 | 1 | `[3,2,1]` | — | `{3,2,1}` |
| 3 | 5 | `[5,3,1,2]` | pop 5 | `{3,2,1}` |
| 4 | 6 | `[6,3,1,2]` wait — root was 3, offer(6) → `[6,3,1,2,...]`. Actually: after step 3 heap = `{3,2,1}` (root=3). offer(6): heap=`[6,3,1,2]`. poll: pop 6 | `{3,2,1}` |
| 5 | 4 | `[4,3,1,2]` | pop 4 | `{3,2,1}` |

Final: `{3,2,1}` ✓ — the 3 smallest.

### Top K Frequent Elements <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)*

Return the `k` most frequent values. First count frequencies, then keep a size-`k` **min-heap** keyed on frequency: the root is the least frequent kept — a candidate with higher frequency arrives, evict the root.

<Callout kind="inv" title="Invariant">

After processing each distinct key, the heap holds the `k` highest-frequency keys seen so far; its root is the least-frequent survivor.

</Callout>

<TemplateReveal
  slug="top-k-frequent"
  language="java"
  :canonical="topKFrequentCode"
/>

**Alternative — bucket sort for O(n)**: since frequencies are integers in `[1, n]`, create buckets where `bucket[f]` = list of values with frequency `f`. Walk `f` from `n` down to `1`, collecting until you've gathered `k` values. Beats the heap when frequencies span a bounded range.

### K Closest Points to Origin <span class="diff diff-m">Medium</span>

*[↗ LeetCode: K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/)*

Return the `k` points closest to `(0,0)`. Keep a size-`k` **max-heap** keyed on **squared** Euclidean distance (`x² + y²`) — `sqrt` is monotone, so comparing squared distances preserves the ordering while avoiding floating-point.

<TemplateReveal
  slug="k-closest-points"
  language="java"
  :canonical="kClosestPointsCode"
/>

<details>
<summary><strong>Pedagogical: the 3-approach ladder for K Closest Points (sort → heap → quickselect)</strong></summary>

**Problem** ([↗ LeetCode](https://leetcode.com/problems/k-closest-points-to-origin/)): Given an array of points on a 2D plane, return the `k` closest points to the origin. Distance is Euclidean; the order of the returned points doesn't matter.

#### Approach 1 — Full sort by distance



```java
int[][] kClosestSort(int[][] points, int k) {
    Arrays.sort(points, (a, b) -> (a[0]*a[0] + a[1]*a[1]) - (b[0]*b[0] + b[1]*b[1]));
    return Arrays.copyOf(points, k);
}
```



**Complexity:** O(n log n) time, O(1) extra space (in-place sort).
Correct, one line, but does more work than needed when `k << n`.

### Approach 2 — Max-heap of size k

Keep a heap of size `k` where the root is the *farthest* point currently in the top-k. Each new point that's closer than the root evicts it.



```java
int[][] kClosest(int[][] points, int k) {
    // Max-heap by squared distance (avoid sqrt — it's monotonic so it doesn't change order).
    PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> {
        int da = a[0]*a[0] + a[1]*a[1], db = b[0]*b[0] + b[1]*b[1];
        return db - da;                              // farthest at root
    });
    for (int[] p : points) {
        heap.offer(p);
        if (heap.size() > k) heap.poll();            // evict the farthest
    }
    int[][] res = new int[k][2];
    for (int i = 0; i < k; i++) res[i] = heap.poll();
    return res;
}
```



**Complexity:** O(n log k) time, O(k) space.

**Why this is faster when k is small:** each of the `n` iterations does O(log k) work instead of the O(log n) of full sort. For `n = 10⁵`, `k = 10`: sort is ~1.7·10⁶ ops, heap is ~3.3·10⁵ ops — 5× faster. The gap widens as `k` shrinks.

### Approach 3 — Quickselect (Hoare partition)

Partition the array around a pivot's distance; recurse on the side that contains rank `k`. Average O(n).



```java
int[][] kClosestQuickselect(int[][] points, int k) {
    quickselect(points, 0, points.length - 1, k);
    return Arrays.copyOf(points, k);
}

void quickselect(int[][] a, int lo, int hi, int k) {
    if (lo >= hi) return;
    int pivotIdx = lo + (int)(Math.random() * (hi - lo + 1));
    int pivotDist = dist(a[pivotIdx]);
    swap(a, pivotIdx, hi);
    int store = lo;
    for (int i = lo; i < hi; i++)
        if (dist(a[i]) < pivotDist) swap(a, i, store++);
    swap(a, store, hi);
    if      (store == k) return;
    else if (store < k)  quickselect(a, store + 1, hi, k);
    else                 quickselect(a, lo, store - 1, k);
}

int dist(int[] p) { return p[0]*p[0] + p[1]*p[1]; }
void swap(int[][] a, int i, int j) { int[] t = a[i]; a[i] = a[j]; a[j] = t; }
```



**Complexity:** O(n) *average*, O(n²) worst case (defended by random pivot).

**When to reach for it:** contest programming or when you know `k` is close to `n/2`. Interview trade-off — quickselect is faster asymptotically but more code, and interviewers occasionally distrust the "expected O(n)" claim.

#### Complexity ladder

| Approach | Time | Space | When |
|---|---|---|---|
| Sort by distance | O(n log n) | O(1) | Simplest; equally good when k ~ n |
| **Max-heap of size k** | **O(n log k)** | **O(k)** | **Interview default when k ≪ n** |
| Quickselect | O(n) avg / O(n²) worst | O(1) in-place | Contest / follow-up "make it O(n)" |

</details>

### Kth Largest in Array <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/)* / *[↗ Kth Largest in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/)*

Return the `k`-th largest value. The size-`k` **min-heap** approach stays alive across stream `add()` calls: `pq.peek()` is always the current `k`-th largest. For the one-shot array version, Quickselect's O(n) average is faster when input is batch, but the heap wins on streams.

<Callout kind="key" title="Why min-heap root = k-th largest?">

The heap holds the `k` largest values seen so far. The smallest of those `k` is at the root — which is the `k`-th largest overall.

</Callout>

<TemplateReveal
  slug="kth-largest-stream"
  language="java"
  :canonical="kthLargestStreamCode"
/>

**Example sequence:** `KthLargest(3, [4, 5, 8, 2])` then `add(3), add(5), add(10), add(9), add(4)`:

| op | heap (size ≤ 3) | peek (k-th largest) |
|---|---|---|
| init | `{4, 5, 8}` (pushed and polled to size 3) | 4 |
| add(3) | `{4, 5, 8}` (3 pushed, polled) | 4 |
| add(5) | `{5, 5, 8}` | 5 |
| add(10) | `{5, 8, 10}` | 5 |
| add(9) | `{8, 9, 10}` | 8 |
| add(4) | `{8, 9, 10}` (4 pushed, polled) | 8 |

### Find Median from Data Stream (two-heap) <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)*

Design a data structure that supports `addNum(x)` and `findMedian()` on a growing stream. The two-heap trick: a **max-heap** `low` holding the smaller half + a **min-heap** `high` holding the larger half. Keep sizes balanced (differ by at most 1); the median is `low.peek()` (odd count) or `(low.peek() + high.peek()) / 2` (even count).

<Callout kind="inv" title="Invariant">

`size(low) == size(high) || size(low) == size(high) + 1`. Every element in `low` is ≤ every element in `high`.

</Callout>

<TemplateReveal
  slug="median-from-stream"
  language="java"
  :canonical="medianStreamCode"
/>

**Why the "offer-to-low, move-max-to-high, rebalance" dance?** Just offering to the right heap based on comparison is tempting but subtle — the comparison breaks when heaps are empty, and the balance can drift. The 3-line canonical move is **always correct**: it's a sort-through-the-middle operation that guarantees both invariants.

**Trace** `addNum(1), addNum(2), findMedian(), addNum(3), findMedian()`:

| op | low (max-heap) | high (min-heap) | median |
|---|---|---|---|
| add(1) | `{1}` | `{}` | — |
| add(2) | `{1}` | `{2}` | — |
| findMedian() | — | — | 1.5 |
| add(3) | `{1, 2}` | `{3}` | — |
| findMedian() | — | — | 2 |

### Task Scheduler (max-heap greedy) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Task Scheduler](https://leetcode.com/problems/task-scheduler/)*

Given task counts and a cooldown `n` (same task can't repeat within `n` ticks), return the minimum time to run everything. The greedy insight: **at each tick, run the most-frequent runnable task** — this prevents the highest-count task from piling up at the end. Use a **max-heap** of counts, with a cooldown queue to re-enqueue tasks when their cooldown expires.

<Callout kind="key" title="Why greedy on max-count works">

if we don't drain the most-frequent task first, its tail will create idle gaps larger than `n`. Formal lower bound: `(max_count - 1) × (n + 1) + ties_at_max`.

</Callout>

<TemplateReveal
  slug="task-scheduler-heap"
  language="java"
  :canonical="taskSchedulerCode"
/>

### Kth Largest / Top K Frequent — walkthrough deep dive <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)*

<ProgressCheck id="kth-largest-top-k-frequent" />





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" role="img" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Diagram illustrating: Kth Largest / Top K Frequent Medium">
  <defs>
    <marker id="ar-topk-success" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-success)"/>
    </marker>
    <marker id="ar-topk-danger" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-danger)"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="28" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">keep only the current top k boundary</text>
  <rect x="31" y="92" width="44" height="44" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <text x="53" y="120" text-anchor="middle" font-size="17" font-weight="700" fill="var(--dsa-ink)">12</text>
  <text x="53" y="153" text-anchor="middle" font-size="11.5" fill="var(--dsa-success)">incoming</text>
  <line x1="80" y1="114" x2="137" y2="114" stroke="var(--dsa-success)" stroke-width="2" marker-end="url(#ar-topk-success)"/>
  <text x="105" y="101" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-success)">larger</text>
  <line x1="200" y1="95" x2="164" y2="138" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <line x1="200" y1="95" x2="236" y2="138" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <circle cx="200" cy="76" r="22" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="1.6"/>
  <circle cx="158" cy="158" r="22" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
  <circle cx="242" cy="158" r="22" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
  <g text-anchor="middle" font-size="17" font-weight="700" fill="var(--dsa-ink)">
    <text x="200" y="82">5</text><text x="158" y="164">8</text><text x="242" y="164">10</text>
  </g>
  <text x="200" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-danger)">root = smallest kept</text>
  <path d="M200 104 C206 121, 220 124, 258 105" fill="none" stroke="var(--dsa-danger)" stroke-width="2" marker-end="url(#ar-topk-danger)"/>
  <text x="294" y="108" font-size="11.5" font-weight="700" fill="var(--dsa-danger)">evict root</text>
  <text x="200" y="210" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">size-k min-heap keeps k largest at O(n log k)</text>
</svg>
</div>




<div class="readfig"><b>How to read it:</b> The heap stores only k candidates; its root is the weakest kept item, so a stronger incoming value replaces it and everything smaller can be ignored.</div>

### Problem
Return the **k most frequent** elements of an array (or, in the sibling, the kth largest). The order among the top-k doesn't matter.

**Constraints:** `1 ≤ n ≤ 10⁵`; `1 ≤ k ≤ #distinct`; beat a full O(n log n) sort.

**Example 1:** `nums = [1,1,1,2,2,3], k = 2` → `[1,2]`.

<ExamplePreview compact :input="['1', '1', '1', '2', '2', '3', '|', '2']" :output="['1', '2']" />

**Example 2:** `nums = [1], k = 1` → `[1]`.

<ExamplePreview compact :input="['1', '|', '1']" :output="['1']" />

### Solution — brute force
First count frequencies. The brute-force way is then to sort all distinct values by decreasing frequency and take the first `k`.



```text
freq = count each number
items = all distinct numbers
sort items by freq descending
return first k items
```





```java
int[] topKFrequentBrute(int[] nums, int k) {
    Map<Integer,Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    List<Integer> keys = new ArrayList<>(freq.keySet());
    keys.sort((a, b) -> freq.get(b) - freq.get(a));
    int[] res = new int[k];
    for (int i = 0; i < k; i++) res[i] = keys.get(i);
    return res;
}
```



This is perfectly acceptable as a baseline: O(n) to count, O(m log m) to sort `m` distinct values, and O(m) space. It becomes wasteful when `m` is large and `k` is small, because sorting rank 5000 versus rank 5001 does not help you return the top 10. The heap version avoids fully ordering the losers.

O(n + m log m) time, O(m) space, where `m` is the number of distinct values — wasteful when k is tiny.

### Solution — optimized
Size-k min-heap; evict the smallest whenever the heap exceeds k.

The heap stores distinct numbers, not array indices and not `(number, frequency)` pairs. The comparator looks up each number's count in the frequency map. Because this is a min-heap by frequency, `poll()` removes the least frequent number among the currently kept candidates. After all distinct values have been processed, only the k most frequent can survive.

<Callout kind="inv" title="Invariant">

After each key from `freq.keySet()` is processed, `pq` contains the k highest-frequency keys seen so far. If more than k keys have been offered, the lowest-frequency survivor has already been evicted.

</Callout>

The optimized Java counts once, then keeps a heap of only `k` surviving keys. The root is deliberately the weakest survivor, so overflow beyond size `k` evicts the least useful candidate immediately.



```java
int[] topKFrequent(int[] nums, int k) {
    Map<Integer,Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    PriorityQueue<Integer> pq =                    // min-heap by frequency
        new PriorityQueue<>((a, b) -> freq.get(a) - freq.get(b));
    for (int key : freq.keySet()) {
        pq.offer(key);
        if (pq.size() > k) pq.poll();              // drop least frequent
    }
    int[] res = new int[k];
    for (int i = k - 1; i >= 0; i--) res[i] = pq.poll();
    return res;
}
```



<Callout kind="note" title="Trace it">

`nums=[1,1,1,2,2,3], k=2`.

</Callout>

<CodeTrace
  title="Top K Frequent — nums=[1,1,1,2,2,3], k=2"
  :values="[1,1,1,2,2,3]"
  :windowKeys="['i']"
  :cellWidth="38"
  :steps='[
    { pointers: { i: 5 }, vars: { freq: "{1:3, 2:2, 3:1}", heap: "[]" }, note: "count all frequencies" },
    { pointers: { i: 0 }, vars: { heap: "[(3,1)]" }, note: "push 1 (freq 3)" },
    { pointers: { i: 0 }, vars: { heap: "[(2,2),(3,1)]" }, note: "push 2 (freq 2). heap size = k=2" },
    { pointers: { i: 0 }, vars: { heap: "[(2,2),(3,1)]" }, note: "3 has freq 1 lt min(2) → skip. result [1,2]", added: [0,3] }
  ]'
/>
### Time Complexity
O(n + m log k), often written O(n log k) when `m ≤ n`. Counting scans all n values, and each of the `m` distinct keys costs O(log k) in the heap.

### Space Complexity
O(n), because the frequency map may store all n values when every value is distinct; the heap itself stores only O(k).

More precisely, counting costs O(n), and heap operations cost O(m log k), where `m` is the number of distinct values. The frequency map can hold up to O(n) entries. The heap itself holds O(k) entries, but the total auxiliary space is still O(n) because of the map.

<Callout kind="trap" title="Common Trap">

Wrong heap polarity. *Example:* the *k-th largest* with a **max**-heap of all n elements costs O(n log n) — wasteful. A **min**-heap of size k evicts the smallest; the root is your answer in O(n log k).

</Callout>

<CodeTrace
  title="Trap — Heap polarity: k-th largest of nums=[3,1,5,2,4], k=2"
  :values="[3,1,5,2,4]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 4 }, vars: { max_heap: "[5,4,3,2,1]", cost: "O(n log n)" }, note: "BUG: max-heap of all 5 → build + pop 2 for 2nd largest = 4. wasteful" },
    { pointers: { i: 4 }, vars: { min_heap: "[4,5]", size: 2, cost: "O(n log k)" }, note: "FIX: min-heap capped at k=2. root=4 = 2nd largest", added: [4] }
  ]'
/>

<Callout kind="note" title="Interview script">

First, I'd count each number because frequency is the ranking key. The brute force is to sort all distinct numbers by frequency and take the first k, which is O(n + m log m). Since we only need k winners, I'll keep a min-heap of size k ordered by frequency and evict the least frequent whenever the heap grows too large. That gives O(n + m log k) time and O(n) space, and the output order can be arbitrary because the problem allows it.

</Callout>

<Callout kind="pat" title="Pattern Connection">

*K Closest Points to Origin* is identical with a max-heap of size k keyed on distance; bucket sort by frequency gives O(n) when the key range is bounded.

</Callout>

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- Why count first? — frequency is the ranking key, so the heap cannot compare numbers until counts exist.
- Why store just the key in the heap? — the `freq` map already holds the count; duplicating pairs is unnecessary here.
- Why a **min-heap** for "most frequent"? — the least frequent survivor is the next one to evict.
- Why `if (pq.size() > k) pq.poll()`? — allowing one temporary extra item lets each candidate compete before eviction.
- Why fill `res` from right to left? — repeated `poll()` returns lower-frequency survivors first.
- Why not sort all keys? — sorting orders every loser too; the heap only maintains the top-k boundary.
- Why mention `Integer.compare`? — subtraction comparators can overflow when values or counts are extreme.

</details>

#### Choosing between heap, sort, bucket, and quickselect
A useful interview move is to name the trade-off instead of pretending the heap is always best. Full sorting is shortest to code and good when `n` is small or when the final order matters. A size-k heap is best when k is small, the stream may not fit in memory, or you need to update answers incrementally. Bucket sort is excellent for frequencies because frequency is an integer from 1 to n; create buckets where bucket `f` stores all values with frequency `f`, then read from high frequency down until k values are collected. Quickselect is attractive for one-shot selection when you can mutate the array of candidates and do not need streaming behavior.

For Top K Frequent specifically, the heap solution is a reliable general answer because it does not depend on a small value range and is easy to adapt to words, points, pairs, or custom objects. If the interviewer asks for strict O(n), discuss buckets after presenting the heap.

#### Comparator details in Java
Java's `PriorityQueue` is a min-heap according to the comparator. That means the "smallest" item by comparator comes out first. For top-k largest, you intentionally define "smallest" as the item you are most willing to discard. In the existing code, `(a, b) -> freq.get(a) - freq.get(b)` puts lower-frequency numbers first.

In production code, `Integer.compare(freq.get(a), freq.get(b))` avoids overflow. The chapter keeps the compile-tested solution unchanged, but in an interview you can mention `Integer.compare` if counts or values can be extreme. For tie-breaking, add a secondary comparison only if the problem requires deterministic ordering; otherwise, extra tie logic is unnecessary.

#### Heap polarity exercises

When you are under interview pressure, decide heap polarity with one sentence: **the root should be the next thing I would throw away.** If you want k largest numbers, the smallest kept number is the next thing to throw away, so the root must be small: min-heap. If you want k smallest numbers, the largest kept number is the next thing to throw away, so the root must be large: max-heap. If you want k closest points, the farthest kept point is the next thing to throw away, so use a max-heap by distance. If you want k most frequent words, the least frequent kept word is the next thing to throw away, so use a min-heap by frequency.

Try this quick table before coding:

| Goal | Worst survivor | Heap at root |
|---|---|---|
| k largest values | smallest value among the kept k | min-heap |
| k smallest values | largest value among the kept k | max-heap |
| k closest points | largest distance among the kept k | max-heap |
| k most frequent | smallest frequency among the kept k | min-heap |
| k least frequent | largest frequency among the kept k | max-heap |

This table prevents the most common reversal bug. The heap is not a trophy case where the best item sits on top. It is a door guard; the root is the easiest item to remove when a better candidate arrives.

#### Streaming vs batch thinking

Top-K heap is the natural streaming answer because it never needs to see the future. After processing the first 100 numbers, the heap already contains the top k among those 100. After the 101st number, one `offer` and maybe one `poll` restores the same invariant. That is why *Kth Largest Element in a Stream* stores the heap as object state and returns `pq.peek()` after each `add`.

Quickselect cannot do that. Quickselect needs a closed array to partition; when a new number arrives, the previous partition work may no longer line up with the new rank. If an interviewer asks, \"What if numbers arrive continuously?\" switch from Quickselect to heap immediately. If they ask, \"What if this is one offline query and k is large?\" Quickselect becomes attractive.

#### Tie handling and output order

Many top-k problems say \"return the answer in any order.\" That permission matters. The heap output order is usually from worst survivor to best survivor because repeated `poll()` removes the comparator-minimum. The existing solution fills the result from right to left so higher-frequency values tend to appear earlier, but the LeetCode problem does not require a sorted top-k list.

If a problem requires deterministic ties, bake the tie-breaker into the comparator. For words, you might sort by frequency ascending but reverse lexicographic order for the min-heap so that the lexicographically worse word is evicted first. For points, equal distances might not need tie-breaking at all. Never add tie rules that the prompt does not ask for; they make comparators harder to reason about and can accidentally evict the wrong item.

#### Testing checklist

Run these small cases mentally before trusting the code:

| Case | Expected lesson |
|---|---|
| `nums=[1], k=1` | heap and result handle the smallest input |
| `nums=[1,2,3], k=3` | no distinct key should be evicted permanently |
| `nums=[1,1,2,2], k=1` | ties are acceptable unless prompt specifies order |
| `nums=[1,1,1,2,3], k=2` | a low-frequency late key should be offered then immediately evicted |
| all values distinct | any k values are valid for top-k frequent because all frequencies tie |

### Same pattern, new tweaks

"Keep only the best `k` in a size-`k` heap of the opposite polarity" transfers straight across:

| Variation | The one thing that changes | Time |
|---|---|---|
| [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | a **max**-heap of size k keyed on squared distance; the farthest current winner is easiest to evict | O(n log k) |
| [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | heap keyed on frequency, or bucket by frequency for O(n) when you want the linear variant | O(n log k) |
| [Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) | treat each row as a sorted stream and use a min-heap for k-way merge | O(k log n) |
| [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | keep a size-k **min**-heap alive across `add` calls; root is always the running kth largest | O(log k) per add |
| [Reorganize String](https://leetcode.com/problems/reorganize-string/) | use a max-heap because you repeatedly need the currently most frequent remaining character, not a bounded top-k set | O(n log alphabet) |

## In the wild — Elasticsearch top-N aggregation & Java's `PriorityQueue`

**Elasticsearch's top-N bucket aggregation** uses a size-N min-heap per shard to compute the top documents by some ordering (score, timestamp, custom field). Each shard returns its local top-N heap; the coordinator does a k-way merge over the shard heaps to produce the global top-N. This is the opposite-polarity rule applied at distributed scale.



```java
/* elasticsearch/search/aggregations/bucket/terms/BucketPriorityQueue.java — paraphrased */
public class BucketPriorityQueue extends PriorityQueue<Bucket> {
    public BucketPriorityQueue(int size, Comparator<Bucket> comparator) {
        super(size, comparator);                 // size = N (the top-N count)
    }
    /* insertWithOverflow(bucket): if heap full and bucket > root, replaces root.
       Classic size-k heap-of-opposite-polarity. The comparator defines "worst at root"
       based on the aggregation ordering (count asc, score desc, etc.). */
}
```



**Four more real-world top-k-heap sightings:**

1. **Kafka's log-compaction** uses a min-heap of per-partition offsets to find the next segment to compact — bounded by compaction concurrency, not partition count.
2. **Linux kernel's `CFS` (Completely Fair Scheduler)** uses a red-black tree (not quite a heap) keyed on virtual runtime; the smallest-runtime task is "most behind" and picked next. Same opposite-polarity idea.
3. **Dijkstra's shortest path** uses a min-heap keyed on tentative distance — pop the vertex with smallest tentative distance, relax its edges, push updated neighbors. Classic in-the-wild heap.
4. **Twitter's trending topics** maintains a sliding-window top-N heap of topic frequencies; new tweets update the heap in O(log N), coordinator aggregates across shards.

## False friends — when "top-k" doesn't need a heap

The phrase "top-k" draws a lot of problems to the heap pattern, but the specific access pattern decides whether the heap is actually the right tool.

- **Quickselect** is strictly better when you need **one** k-th value offline and don't care about the other k-1 boundary items. O(n) average vs. O(n log k).
- **Bucket sort** beats heap when the ranking key has a small bounded range (e.g., frequency buckets 1..n for Top-K Frequent). O(n) time.
- **TreeSet / sorted multiset** when you need **ordered** access to the entire top-k (not just the boundary). O(log k) per op, but with sorted iteration.
- **Reservoir sampling** for streaming "k random items from an infinite stream" — a heap would require seeing all items, reservoir doesn't.
- **Count-min sketch / top-k approximation** for streaming top-k on massive data (10^12+ items) where exact answers aren't needed. The heap approach needs enough memory for k winners.
- **Plain scalar tracking** for k = 1 — just a `max` variable. No heap needed.

### Visual 1: quickselect beats heap for one offline k-th value

For "find the k-th largest" when the full array fits in memory and you don't need the other winners:



```text
   n = 10⁷ random integers, k = 1000

   Heap approach (min-heap of size k):
     for each of 10⁷ elements:  add to heap, if size > k pop min
     cost: 10⁷ × log₂ 1000 ≈ 10⁷ × 10 = 10⁸ ops
     bonus: heap at end gives you ALL top k, sorted by extraction

   Quickselect approach (partition until the k-th position is fixed):
     expected cost: O(n) = 10⁷ ops
     bonus: NONE — only the k-th value is placed; everything else is just partitioned
     downside: in-place mutation of input; worst case O(n²) without careful pivot

   10× fewer ops in exchange for giving up the other k−1 values.
```



The decision: do you need **all top-k** values or just **the k-th**? Heap gives you all of them; quickselect gives you only the one, in less time. For streaming or online data you can't rewind, quickselect doesn't apply at all — the heap is forced. For an offline file you can read once, quickselect wins.

### Visual 2: bucket sort beats heap on bounded frequency keys

For `Top-K Frequent Elements`, the frequency `f` is bounded by `n`. That means you can bucket by frequency:



```text
   nums = [1,1,1,2,2,3,3,3,3,4,5,5],  n = 12,  k = 2 most frequent

   Heap approach:
     count freqs:    map = {1:3, 2:2, 3:4, 4:1, 5:2}       O(n)
     min-heap of size k:                                     O(n log k)
     for each (val, freq) in map:
       heap.offer((val, freq)); if size > k, poll
     result: [1, 3]                                          total: O(n log k) ≈ n · 10 for k=1024

   Bucket-sort approach:
     count freqs:    map = {1:3, 2:2, 3:4, 4:1, 5:2}       O(n)
     bucket by freq: buckets[3]=[1], buckets[2]=[2,5], buckets[4]=[3], buckets[1]=[4]
                                                             O(n)
     walk buckets from high freq to low, collect top k:      O(n)
     result: [3, 1]                                          total: O(n)
```



The trick: there are at most `n` possible frequency values, so you can index into a `bucket[]` of size `n+1` directly. No log factor. On problems where the "ranking key" is bounded by `n` or something small, bucket sort beats heap. Watch for this pattern — it comes up in "sort characters by frequency", "top-k frequent", "sort array by rank" problems.

### Visual 3: streaming with no space budget → reservoir, not heap

Problem: pick k uniformly random items from a stream of unknown length. A heap can't do this:



```text
   Stream: emit 10¹² items, we must choose k=100 uniformly at random

   Heap approach (max-heap by random priority):
     for each item x: give x a random priority p; heap.add((p,x)); if size>k poll
     cost: 10¹² × log₂(100) ≈ 7 × 10¹² ops
     memory: k = 100 items in the heap ✓ feasible
     BUT: requires knowing we are "comparing by random priority" — essentially recreating reservoir
          with heap overhead

   Reservoir sampling (Algorithm R):
     fill reservoir[0..k-1] with first k items
     for each item i ≥ k:
       j = random int in [0, i]
       if j < k: reservoir[j] = item i
     cost: 10¹² ops, no log factor
     memory: k = 100 ✓
     correctness: proved uniform over any stream prefix of length ≥ k
```



Both work, but reservoir is a 5-line loop with no heap and no log factor. The heap is extra machinery that doesn't earn its complexity for this access pattern. Reach for reservoir sampling specifically when you need **random k from a stream of unknown length**; use the heap when you need **top-k by rank from a stream**, where the comparison is a value, not a random priority.

## Recognition drill

<RecognitionDrill pattern="top-k-heap" :count="10" />

## Advanced — follow-ups and failure modes

<details>
<summary><strong>What if the input is massive and doesn't fit in memory?</strong></summary>

**Streaming with external merge.** Chunk the input, compute top-k per chunk with a size-k heap, then merge the chunk heaps with k-way merge (another min-heap of chunk iterators). Memory: O(k + #chunks). This is exactly how external sort and MapReduce's top-k implementations work.

For **approximate** top-k on massive streams, use **Count-Min Sketch + heap** (Metwally et al., 2005). Each incoming item updates sketch counters; a size-k heap tracks the current top candidates. Error bounded by ε·N with probability 1-δ, using O(log(1/δ)/ε) memory — independent of stream length.
</details>

<details>
<summary><strong>What if the heap must support arbitrary deletes (not just root)?</strong></summary>

Plain binary heap can't do this in O(log n) — deleting a specific element requires finding it first. Three approaches:
1. **Indexed heap** — maintain `pos[element] = index` alongside the heap array, allowing O(log n) delete-by-element. More code; used in Dijkstra when you want to "update priority" of a specific vertex.
2. **Lazy deletion** — tag the element as deleted; skip it when it bubbles to the root. Simple but wastes space proportional to deleted-but-not-popped elements.
3. **TreeSet / sorted multiset** — O(log n) for any op, including remove, successor, predecessor. Slower constants than heap, but strictly more capable.
</details>

<details>
<summary><strong>What if k is NOT fixed — queries arrive with different k values?</strong></summary>

**One-shot batch**: sort the input once in O(n log n); every query is O(k) slice.

**Online queries**: maintain a **sorted structure** (TreeSet, skip list, order-statistic tree). Each insertion O(log n), each "give me top k" is O(k) iteration from the top.

A heap is the wrong tool here — it only knows about the k winners, not the broader structure.
</details>

<details>
<summary><strong>What if ties in the key matter (and the heap doesn't guarantee stable order)?</strong></summary>

Java's `PriorityQueue` is **not stable** — equal-key items may be popped in any order. If the problem requires FIFO on ties (e.g., "oldest tied document wins"), augment the comparator with a secondary key: `(key, insertion_timestamp)`, breaking ties by timestamp ascending.

For custom tie-breaking (lex order, ID), pass the secondary comparator explicitly. Never rely on the heap's internal "default" tie behavior.
</details>

<details>
<summary><strong>What if the "ranking function" is expensive to compute?</strong></summary>

**Cache the key per item** by wrapping into a `(key, item)` tuple, computing the key once at offer time. Avoids recomputing during every bubble-up/bubble-down.

For geometric top-k ("nearest neighbors"), **KD-trees** (static) or **ball trees** (dynamic) answer top-k queries in average O(k log n), beating the O(n log k) heap approach when n is large and the dimensionality is low (≤ 20).
</details>

### Breaking point

Top-K heap **stops being optimal** when:
- `k` is close to `n` (O(n log k) ≈ O(n log n), just sort).
- The ranking key has a small bounded range (bucket sort wins at O(n)).
- You need arbitrary-element delete (indexed heap or TreeSet).
- You need the top-k internally sorted (TreeSet or sort-then-slice).
- The input is a known, static array and you need just the k-th value (Quickselect wins at O(n) average).
- The stream is massive and exact answers aren't needed (sketch-based approximation).

### Three cross-pattern problems

- [Sliding Window Median (480)](https://leetcode.com/problems/sliding-window-median/) — two-heap median + lazy deletion to handle elements leaving the window. Bridges heap with sliding-window.
- [Merge k Sorted Lists (23)](https://leetcode.com/problems/merge-k-sorted-lists/) — min-heap of head pointers; classic k-way merge. Heap meets linked-list.
- [Design Twitter (355)](https://leetcode.com/problems/design-twitter/) — merge the top-10 tweets of each followee using a min-heap; combines heap with hash-map user-follower bookkeeping.

---

## Check your understanding

<Quiz pattern-id="top-k-heap" :questions="mastery5" />

<PrintButton />

<RelatedPatterns pattern-id="heap" />
