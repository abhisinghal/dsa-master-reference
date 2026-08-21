# Heaps (Priority Queues)

## Why heaps exist — the story

A heap is what you use when the full order is overkill but the next extreme matters a lot. Sorting a changing collection after every insert would be like alphabetizing your whole bookshelf every time you buy one book. A heap keeps just enough order so the smallest (or largest, with a reversed comparator) is always at the root, while the rest of the array is only partially ordered. That weaker promise is exactly why updates are cheap.

The array layout is the trick. Store a binary tree level-by-level: for index `i`, the parent is `(i - 1) / 2`, and the children are `2*i + 1` and `2*i + 2`. Insert `4` into a min-heap `[2,5,8]`: append it as `[2,5,8,4]`, then compare with its parent `5` and swap to get `[2,4,8,5]`. It stops because parent `2` is smaller. That is **sift-up**. Removing the root does the reverse: move the last item to the root, then repeatedly swap it with the smaller child until the heap property returns. That is **sift-down**. Each move climbs or descends one tree level, so the cost is O(log n).

This Part III chapter focuses on heap internals and streaming problems. The Top-K pattern chapter covers the interview recipe of "keep a size-k heap of the opposite polarity." Here, the goal is to understand what Java's `PriorityQueue` is doing under the hood, why median needs **two** heaps, and which heap gotchas cause bugs in production code.

<Callout kind="key" title="Key Insight">

A heap is a partially ordered array-backed tree. It gives O(1) access to one extreme and O(log n) insert/remove-extreme, but it does not keep every element sorted.

</Callout>

### Recognize by
- "current smallest/largest" after many inserts or removals
- "streaming median," "running percentile," or "middle value as data arrives"
- "merge k sorted lists/streams" where the next output is the smallest head
- scheduling by earliest time/deadline/priority
- graph algorithms that repeatedly pick the cheapest frontier state
- memory limit hints where sorting the entire changing set is too expensive

### When to use it — practical flavors

| Flavor | Typical wording | Heap shape |
|---|---|---|
| Repeated minimum/maximum | "process next earliest", "always pick cheapest" | one min-heap or max-heap |
| Streaming boundary | "running kth", "data stream" | fixed-size heap or two heaps |
| Merge sorted sources | "k sorted lists", "smallest head among streams" | min-heap of current heads |
| Median / percentile | "middle after each insert" | max-heap lower half + min-heap upper half |
| Lazy update algorithms | Dijkstra, Prim, cancellations | push new entries; skip stale roots |

The shared idea is that you do not care where every item ranks. You care which item should be processed next. If the problem asks for repeated "next best" decisions and the set changes between decisions, a heap is usually the first structure to test.

### When NOT to use it
- You need full sorted iteration; heap iteration is not sorted.
- You need fast search for arbitrary values; a heap only exposes the root.
- You need O(log n) arbitrary delete or update by key; Java `PriorityQueue` does not support decrease-key.
- You need order statistics like "10th smallest" under many deletes; consider balanced trees or indexed heaps.
- You only need one kth value once; Quickselect can be O(n) average and simpler than maintaining a heap.

## How to use it — two-heap streaming median template

Median is not a top-k problem. You need the middle boundary from both sides, so split the stream into two halves: `low` is a max-heap containing the smaller half; `high` is a min-heap containing the larger half.



```java
PriorityQueue<Integer> low = new PriorityQueue<>(Collections.reverseOrder());
PriorityQueue<Integer> high = new PriorityQueue<>();

void add(int x) {
    low.offer(x);
    high.offer(low.poll());
    if (high.size() > low.size()) low.offer(high.poll());
}

double median() {
    if (low.size() > high.size()) return low.peek();
    return (low.peek() + high.peek()) / 2.0;
}
```



<Callout kind="inv" title="Two-heap invariant">

`low.size()` is either equal to `high.size()` or one larger, and every value in `low` is `<=` every value in `high`. Therefore the median is either `low.peek()` or the average of both peeks.

</Callout>

## Heap internals in one page

Java's `PriorityQueue` is backed by an array, not linked nodes. For a min-heap, every parent is `<=` its children. That does **not** mean the left child is less than the right child, or that a level is sorted. The only guaranteed global fact is that the minimum is at index 0.



```text
index:  0  1  2  3  4  5
heap:  [2, 4, 8, 9, 7, 10]
parent of 4(index 1) = 0 -> 2
children of 4(index 1) = 3,4 -> 9,7
```



Insert appends to the end and sifts up. Poll removes root, moves the last element to root, and sifts down. Building a heap from an existing array can be O(n), because bottom-up heapify sifts down only where needed; inserting n items one by one is O(n log n).

<Callout kind="trap" title="Heap-order misconception">

Printing or iterating a `PriorityQueue` does not produce sorted order. Only repeated `poll()` returns values in priority order, and that destroys the heap.

</Callout>

### Sift-up and sift-down by hand

For a min-heap, insert always starts at the next open array slot. Suppose the heap is `[3, 6, 8, 10, 7]` and you insert `2`. Append first: `[3, 6, 8, 10, 7, 2]`. The new item is at index 5, parent `(5-1)/2 = 2`, value 8, so swap: `[3, 6, 2, 10, 7, 8]`. Now index 2's parent is index 0, value 3, so swap again: `[2, 6, 3, 10, 7, 8]`. The item reached the root in two swaps because the tree height is logarithmic.

Polling is symmetric. Remove root `2`, move last `8` to root: `[8, 6, 3, 10, 7]`. Compare children `6` and `3`; swap with smaller child `3`: `[3, 6, 8, 10, 7]`. Now `8` has no smaller child, so stop. This is why heap operations are predictable even when the internal array looks only half-sorted.

### Java `PriorityQueue` operation costs

| Operation | Cost | Notes |
|---|---|---|
| `offer(x)` | O(log n) | append then sift up |
| `peek()` | O(1) | read root; returns `null` when empty |
| `poll()` | O(log n) | remove root, move tail to root, sift down |
| constructor from collection | O(n) | heapifies bottom-up |
| `contains(x)` | O(n) | scans the backing array |
| `remove(x)` | O(n) | finds arbitrary item by scan, then fixes heap |

That table explains many interview tradeoffs. If the prompt says "cancel task id 42 in O(log n)," a plain `PriorityQueue` is not enough because it cannot find id 42 quickly. You either add a map from id to heap index and implement your own indexed heap, or you use lazy deletion and accept that cancelled tasks disappear only when they rise to the root.

### K-way merge as the internals warm-up

Merging sorted streams is the purest heap use case: each stream already has local order, so the only question is which stream head is globally smallest right now. Push the first node from each list into a min-heap keyed by value. Repeatedly poll the smallest node, append it to the answer, and push that node's successor from the same list. The heap size is at most `k`, so the merge is O(totalNodes · log k). This is not the Top-K pattern; you are not discarding candidates. You are using the heap as a live tournament among k frontiers.

---

## Find Median from Data Stream (Two Heaps) <span class="diff diff-h">Hard</span>


*[↗ LeetCode: Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)*

<ProgressCheck id="find-median-from-data-stream-two-heaps" />

### Problem

Support `addNum(x)` on a growing stream and `findMedian()` returning the current median — both efficiently.

**Constraints:** up to `5·10⁴` calls; `addNum` O(log n), `findMedian` O(1).

**Example:** add `1, 2` → median `1.5`; then add `3` → median `2`.

**Example 1:** add 1, add 2 -&gt; median 1.5; add 3 -&gt; median 2.

**Example 2:** add 5,15,1,3 -&gt; medians 5,10,5,4.

### Solution — brute force

The simplest design stores every value in a list. On each `findMedian`, sort a copy and read the middle.



```java
class MedianFinderBrute {
    List<Integer> nums = new ArrayList<>();
    void addNum(int x) { nums.add(x); }
    double findMedian() {
        List<Integer> copy = new ArrayList<>(nums);
        Collections.sort(copy);
        int n = copy.size();
        if (n % 2 == 1) return copy.get(n / 2);
        return (copy.get(n / 2 - 1) + copy.get(n / 2)) / 2.0;
    }
}
```



That makes `addNum` O(1), but `findMedian` O(n log n). Keeping a sorted list improves median lookup but makes insertion O(n) because elements must shift. Two heaps split the work: insertion is O(log n), median is O(1).

There is also a `TreeMap<Integer, count>` approach: insert in O(log n), keep two counters or iterators around the middle, and answer median in O(1) or O(log n) depending on how much machinery you maintain. It is valid, but in Java interviews the two-heap version is shorter and easier to reason about.

### Solution — optimized

**Pattern:**
A **max-heap** for the lower half and a **min-heap** for the upper half, balanced in size. The median is a heap top (or the average of two).

<Callout kind="inv" title="Invariant">

Every element in `low` (max-heap) ≤ every element in `high` (min-heap); sizes differ by at most 1. The medians sit at the two roots.

</Callout>

<div class="figcap">Two-heap median — funnel through <code>high</code>, rebalance by size; ordering across the two roots is preserved.</div>
<div class="readfig"><b>How to read it:</b> Split the numbers into a smaller half and a larger half. The smaller half sits in a max-heap (so its biggest is on top) and the larger half in a min-heap (so its smallest is on top) — which means the two tops are exactly the middle values. Every new number is passed through <code>high</code> and then the halves are rebalanced so their sizes differ by at most one. The median is then just the top of the bigger half, or the average of the two tops when they're equal in size.</div>

**Java:**


```java
class MedianFinder {
    private final PriorityQueue<Integer> low  = new PriorityQueue<>(Collections.reverseOrder()); // max-heap
    private final PriorityQueue<Integer> high = new PriorityQueue<>();                            // min-heap
    public void addNum(int num) {
        low.offer(num);
        high.offer(low.poll());                 // funnel largest of low into high
        if (high.size() > low.size()) low.offer(high.poll());  // rebalance
    }
    public double findMedian() {
        if (low.size() > high.size()) return low.peek();
        return (low.peek() + high.peek()) / 2.0;
    }
}
```



<Callout kind="note" title="Trace it">

Stream `1,2,3,4`. Add `1`: `low=[1]`, `high=[]`, median `1`. Add `2`: push through `low` into `high`, then sizes are equal: `low=[1]`, `high=[2]`, median `(1+2)/2 = 1.5`. Add `3`: `3` moves to `high`, then `2` rebalances back to `low`, so roots are `2 | 3`, median `2`. Add `4`: halves become `low=[2,1]`, `high=[3,4]`, median `2.5`.

</Callout>

### Time Complexity

O(log n) per addNum and O(1) per findMedian.

Original summary: `addNum` O(log n) · `findMedian` O(1) · Space O(n).

### Space Complexity

O(n) across the two heaps.

<Callout kind="trap" title="Common Trap">

Skipping the rebalance. *Example:* insert 1,2,3,4. Without rebalancing, all four might land in the low-heap → median unreadable. After every insert: push to `low`, move `low.top` to `high`; if `high.size() > low.size()` move one back. Two peeks give the median.

</Callout>

<Callout kind="trap" title="Overflow Trap">

`low.peek() + high.peek()` can overflow `int` before division. If constraints allow values near `Integer.MAX_VALUE`, cast first: `((long) low.peek() + high.peek()) / 2.0`.

</Callout>

<Callout kind="note" title="Interview script">

"The median is the boundary between the lower half and upper half. I keep the lower half in a max-heap and the upper half in a min-heap, so the boundary values are at the roots. On insert, I funnel through one heap to preserve ordering, then rebalance sizes. `findMedian` only peeks at one or two roots, so it is O(1)."

</Callout>

<Callout kind="pat" title="Pattern Connection">

Two balanced heaps also solve *Sliding Window Median* (add lazy deletion) and *IPO / maximize capital* (one heap to unlock projects, another to pick the most profitable). This complements the Top-K chapter: top-k keeps one boundary heap; median keeps two opposing boundary heaps.

</Callout>

### Learning notes

- Why two heaps? They hold lower and upper halves.
- Why max-heap lower? The lower middle must be O(1).
- Why rebalance? Median formula needs size difference &lt;= 1.
- Why double division? Avoids integer truncation.
- Why PriorityQueue&lt;Integer&gt;? No extra metadata is needed.

#### Same pattern, new tweaks

"Keep the data split into two heaps whose tops meet in the middle" transfers to:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Sliding Window Median](https://leetcode.com/problems/sliding-window-median/) | add lazy deletion so the element leaving the window is discarded from whichever heap holds it | O(n log k) |
| [IPO / Maximize Capital](https://leetcode.com/problems/ipo/) | a min-heap unlocks projects you can afford, a max-heap picks the most profitable of those | O(n log n) |
| [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | the base case — balance the two heaps on every insert | O(log n) add |
| [Meeting Rooms III](https://leetcode.com/problems/meeting-rooms-iii/) | one heap tracks free room ids, another tracks rooms by next end time | O(n log rooms) |

## Heap essentials &amp; gotchas
<p class="secgoal"><b>What & why:</b> the practical rules and traps of `PriorityQueue`. Goal — avoid the classic mistakes (iteration isn't sorted, no decrease-key, O(n) arbitrary removal) and choose the right heap size and direction.</p>

- **Min-heap by default.** `new PriorityQueue<>()` returns the smallest item first. Use `Collections.reverseOrder()` or a comparator for max-heap behavior.
- **Build-heap** from an array is O(n) (bottom-up sift-down), not O(n log n).
- **No decrease-key** in Java's `PriorityQueue`: for Dijkstra/Prim, push duplicates and skip stale entries on pop (lazy deletion).
- **Custom order** via comparator; for objects avoid `a - b` on large ints (overflow) — use `Integer.compare` / `Long.compare`.
- **Arbitrary removal** is O(n); if you need it, pair the heap with a hash "removed" set and lazy-delete on pop.
- **The heap is not sorted.** `peek()` is meaningful; iteration order is an implementation detail.

<Callout kind="key" title="Key Insight">

A heap is the right tool when you need *an* extreme repeatedly but never a full ordering. If you need the full sorted order or arbitrary-position access, use a `TreeMap`/`TreeSet` instead.

</Callout>

### Choosing heap polarity

Say the goal out loud: "Which item should be easiest to throw away?" For top-k largest, the worst of your kept set is the smallest, so use a min-heap. For top-k smallest, use a max-heap. For median, neither single polarity is enough because you need both sides of the middle.

For object comparators, prefer explicit comparison:



```java
PriorityQueue<int[]> pq = new PriorityQueue<>(
    (a, b) -> Integer.compare(a[0], b[0])
);
```



Avoid `(a, b) -> a[0] - b[0]`; large values can overflow and reverse the intended order. If two entries can tie, add a deterministic tie-breaker such as `Integer.compare(a[1], b[1])` so tests do not depend on incidental ordering.

### Lazy deletion in one minute

Java heaps cannot remove an arbitrary stale element in O(log n). The common workaround is to leave stale entries inside the heap and skip them when they reach the root. Maintain a `Map<Value, countToDelete>` or store `(value, id)` pairs. Before every `peek` or `poll`, repeatedly pop while the root is marked stale. This is the key upgrade for sliding-window median, Dijkstra with updated distances, and task schedulers with cancellations.

<Callout kind="note" title="Interview script">

"I will not rely on iterating the heap or removing arbitrary values from it. A heap only promises the root. If I need updates or deletions, I either push a newer entry and skip stale ones later, or I choose a balanced tree. That keeps the complexity honest."

</Callout>
