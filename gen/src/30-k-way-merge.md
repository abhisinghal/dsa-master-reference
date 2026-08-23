# K-way Merge


<PatternVideo pattern-name="K-way Merge" duration="8–12 min" />

<PatternProgress pattern-id="k-way-merge" problems="k-way-merge-k-sorted-lists, merge-two-sorted-lists, smallest-range-covering-elements-from-k-lists, ugly-number-ii" />



## Why k-way merge exists — the story

Imagine you have three sorted logs coming from three servers:

| stream | values left |
|---|---|
| A | `1, 4, 5` |
| B | `1, 3, 4` |
| C | `2, 6` |

If you concatenate everything and sort, you get the right answer, but you throw away the one gift the input already gave you: each stream is sorted. The first element of each stream is a promise. If A starts with `1`, then A will not hide a smaller value behind it. So the global next value must be one of the `k` visible heads. That is the whole k-way merge idea: keep `k` pointers, put their current values in a min-heap, repeatedly pop the smallest head, then advance only that stream.

Trace the tiny example by hand. The heap starts with `(1,A), (1,B), (2,C)`. Pop `(1,A)`, output `1`, and push A's next value `4`; the heap is now `(1,B), (2,C), (4,A)`. Pop `(1,B)`, push `3`; then pop `2`, push `6`; then `3`, `4`, `4`, `5`, `6`. At no point did you compare every remaining element with every other element. The heap only compares the current frontier, so each of the `N` total elements costs `log k`, not `log N`.

The brute-force walk-through is concatenate everything and sort it. Can we do better? Yes, because each list already sorted itself. The only real question at any moment is: "which current head is smallest?"

> [key] **Key Insight** — The heap holds a moving *frontier* of size k, one representative per stream. Its top is always the globally smallest remaining value.

This is also why k-way merge feels like a cousin of Dijkstra's algorithm. Dijkstra keeps a heap of the best currently-known frontier nodes and expands the cheapest one next. K-way merge keeps a heap of stream fronts and expands the smallest one next. In both, the heap is not magic; it is just an efficient way to ask, again and again, "which frontier item should I process next?"

## When to use it — and when not to

### Recognize by
- "merge k sorted lists / arrays / files" — several already-ordered sources must become one ordered result.
- "smallest range covering elements from k lists" — you must keep one live value from each list.
- "kth smallest in a sorted matrix" — each row or column can be treated as a sorted stream.
- "external sort runs" — sorted chunks on disk are merged without loading everything.
- "find k pairs with smallest sums" — the candidate pairs form ordered frontiers.
- "always choose the next smallest available item among k sources" — a min-heap of fronts is likely.


<HeapAnim />


### When NOT to use it
The k streams aren't sorted individually — a heap over the current fronts is meaningless if the fronts don't represent "smallest not-yet-emitted". Sort each stream first, or use a different approach.

Also be careful when:
- you only have one unsorted collection; use sorting or quickselect instead.
- `k` is tiny and fixed, like 2; a direct two-pointer merge is simpler and faster.
- you need random access by rank after many updates; a balanced tree or indexed structure may fit better.
- the next item in a stream is expensive to fetch and you cannot prefetch; design the iterator boundary first.
- duplicate handling changes the problem, such as needing distinct values only; add that policy explicitly after popping.

## How to use it — template

```java
class Entry {
    int value, list, index;
    Entry(int value, int list, int index) {
        this.value = value; this.list = list; this.index = index;
    }
}

PriorityQueue<Entry> pq = new PriorityQueue<>((a, b) -> a.value - b.value);
for (int i = 0; i < lists.size(); i++) {
    if (!lists.get(i).isEmpty()) pq.offer(new Entry(lists.get(i).get(0), i, 0));
}
while (!pq.isEmpty()) {
    Entry cur = pq.poll();                 // global next-smallest
    output(cur.value);
    int next = cur.index + 1;
    if (next < lists.get(cur.list).size()) {
        pq.offer(new Entry(lists.get(cur.list).get(next), cur.list, next));
    }
}
```

The template has three moving pieces. The `Entry` remembers not just the value, but also where it came from, because after you pop a value you must advance the same stream. The initialization pushes the first visible value from every non-empty stream. The loop pops the global minimum, records it, and re-feeds the heap with the next value from that same list. That "same list" detail is the invariant that keeps the output sorted and prevents skipped elements.

---

## Merge Two / K Sorted Lists <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)*

<ProgressCheck id="merge-two-k-sorted-lists" />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <defs>
    <marker id="ar-kmerge-primary" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="26" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">merge k sorted lists by comparing only heads</text>

  <g text-anchor="middle">
    <g font-size="17" font-weight="700" fill="var(--dsa-ink)">
      <rect x="24" y="46" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="46" y="74">1</text>
      <rect x="72" y="46" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="94" y="74">4</text>
      <rect x="120" y="46" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="142" y="74">5</text>
      <rect x="24" y="98" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="46" y="126">1</text>
      <rect x="72" y="98" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="94" y="126">3</text>
      <rect x="120" y="98" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="142" y="126">4</text>
      <rect x="24" y="150" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="46" y="178">2</text>
      <rect x="72" y="150" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="94" y="178">6</text>
    </g>
    <g font-size="11" fill="var(--dsa-neutral)">
      <text x="12" y="73">L1</text><text x="12" y="125">L2</text><text x="12" y="177">L3</text>
    </g>
  </g>

  <line x1="178" y1="121" x2="228" y2="121" stroke="var(--dsa-primary)" stroke-width="2" marker-end="url(#ar-kmerge-primary)"/>
  <text x="203" y="108" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-primary)">heads</text>
  <line x1="291" y1="96" x2="264" y2="135" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <line x1="291" y1="96" x2="318" y2="135" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <circle cx="291" cy="78" r="20" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <circle cx="259" cy="153" r="20" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
  <circle cx="323" cy="153" r="20" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
  <g text-anchor="middle" font-size="15" font-weight="700" fill="var(--dsa-ink)">
    <text x="291" y="83">1</text><text x="259" y="158">1</text><text x="323" y="158">2</text>
  </g>
  <text x="291" y="39" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-success)">min-heap of heads</text>
  <path d="M291 178 C291 197, 244 203, 190 203" fill="none" stroke="var(--dsa-success)" stroke-width="2" marker-end="url(#ar-kmerge-primary)"/>
  <text x="259" y="218" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-success)">poll → append → refill next</text>
  <text x="200" y="237" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">min-heap of k heads; poll and refill</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> Only the current head of each sorted list can be the next output, so a min-heap chooses the smallest head and then replenishes from that same list.</div>

### Problem
Merge `k` sorted linked lists into one sorted list. (The two-list merge is the building block.)

**Constraints:** `0 ≤ k ≤ 10⁴`; total nodes up to `10⁴`; each list sorted ascending.

**Example 1:** `[[1,4,5],[1,3,4],[2,6]]` → `1→1→2→3→4→4→5→6`.

**Example 2:** `[]` → `[]`.

### Solution — brute force
The baseline is to collect every node value into an array, sort the array, then rebuild a linked list from the sorted values.

```java
// Pseudocode baseline:
// values = []
// for each list: walk nodes and append node.val to values
// sort(values)
// build a new linked list from values
```

```java
ListNode mergeKListsBrute(ListNode[] lists) {
    List<Integer> values = new ArrayList<>();
    for (ListNode head : lists) {
        for (ListNode cur = head; cur != null; cur = cur.next) {
            values.add(cur.val);
        }
    }
    Collections.sort(values);
    ListNode dummy = new ListNode(0), tail = dummy;
    for (int v : values) {
        tail.next = new ListNode(v);
        tail = tail.next;
    }
    return dummy.next;
}
```

This is easy to explain and often good enough for a warm-up, but it ignores the fact that every input list is already sorted. If there are `N` total nodes, the time is O(N log N) and the extra space is O(N). The optimized heap version keeps only one node from each list in the heap, so it improves the sort factor to O(log k).

O(N log N) time, O(N) space — too slow compared with using the sorted-list frontier.

### Solution — optimized
Dummy-head splice for two lists; min-heap for k lists.

> [inv] **Invariant** — `tail` always points at the last node of the merged prefix; appending the smaller head keeps output sorted.

The optimized version keeps one live node per list in a min-heap. Pop the smallest node, splice it onto the answer, and push that same node's successor so the frontier remains complete.

```java
ListNode mergeTwo(ListNode a, ListNode b) {
    ListNode dummy = new ListNode(0), tail = dummy;
    while (a != null && b != null) {
        if (a.val <= b.val) { tail.next = a; a = a.next; }
        else                { tail.next = b; b = b.next; }
        tail = tail.next;
    }
    tail.next = (a != null) ? a : b;        // attach remainder
    return dummy.next;
}

ListNode mergeKLists(ListNode[] lists) {
    PriorityQueue<ListNode> pq = new PriorityQueue<>((x, y) -> x.val - y.val);
    for (ListNode l : lists) if (l != null) pq.offer(l);
    ListNode dummy = new ListNode(0), tail = dummy;
    while (!pq.isEmpty()) {
        ListNode n = pq.poll();
        tail.next = n; tail = n;
        if (n.next != null) pq.offer(n.next);
    }
    return dummy.next;
}
```

> [note] **Trace it** — merge `[[1,4,5],[1,3,4],[2,6]]`.
>
> | step | heap before pop | output appended | node re-fed | merged prefix |
> |---|---|---|---|---|
> | 1 | `1A, 1B, 2C` | `1A` | `4A` | `1` |
> | 2 | `1B, 2C, 4A` | `1B` | `3B` | `1,1` |
> | 3 | `2C, 3B, 4A` | `2C` | `6C` | `1,1,2` |
> | 4 | `3B, 4A, 6C` | `3B` | `4B` | `1,1,2,3` |
> | 5 | `4A, 4B, 6C` | `4A` | `5A` | `1,1,2,3,4` |
> | 6 | `4B, 5A, 6C` | `4B` | none | `1,1,2,3,4,4` |
> | 7 | `5A, 6C` | `5A` | none | `1,1,2,3,4,4,5` |
> | 8 | `6C` | `6C` | none | `1,1,2,3,4,4,5,6` |

<CodeTrace
  title="Merge K Sorted Lists — heap-based, k=3"
  :values="[1,4,5]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { heap: "[1A, 1B, 2C]", output: "" }, note: "seed with each list head" },
    { pointers: { i: 0 }, vars: { heap: "[1B, 2C, 4A]", output: "1" }, note: "pop 1A, push 4A" },
    { pointers: { i: 0 }, vars: { heap: "[2C, 3B, 4A]", output: "1,1" }, note: "pop 1B, push 3B" },
    { pointers: { i: 0 }, vars: { heap: "[3B, 4A, 6C]", output: "1,1,2" }, note: "pop 2C, push 6C" },
    { pointers: { i: 0 }, vars: { heap: "[4A, 4B, 6C]", output: "1,1,2,3" }, note: "pop 3B, push 4B" },
    { pointers: { i: 0 }, vars: { heap: "[]", output: "1,1,2,3,4,4,5,6" }, note: "drain — final output" }
  ]'
/>
### Time Complexity
Two lists take O(n+m), because each pointer advances once. K lists take O(N log k), because each of the N total nodes is popped once and may push one successor into a heap of size at most k.

### Space Complexity
O(k) extra for the heap in the k-list solution, beyond the output links. The two-list helper uses O(1) extra space.

> [trap] **Common Trap** — Not re-feeding the heap. *Example:* three lists `[1,4],[1,3],[2,6]`. After popping `1` from list A, you must `offer(A.next)` (i.e. `4`) — otherwise list A never appears again and its remaining nodes are silently dropped.

<TrapTrace title="Not re-feeding the heap" input="[1,4],[1,3],[2,6]" bug="three lists '[1,4],[1,3],[2,6]'. After popping '1' from list A, you must 'offer(A.next)' (i.e. '4') — otherwise list A never appears again and its remaining nodes are silently dropped." fix="See the guidance in the trap description and the code snippet." />

> [note] **Interview script** — First, I'd verify that each input list is already sorted; otherwise this pattern does not apply. The brute force is to dump all `N` values, sort them, and rebuild the list in O(N log N) time. Since there are `k` sorted fronts, I can keep a min-heap of at most `k` nodes, repeatedly pop the smallest, and push that same node's successor. That gives O(N log k) time and O(k) extra space.

> [pat] **Pattern Connection** — This is the **K-way merge** pattern (heap of fronts): the same engine merges sorted arrays or external-sort runs on disk. Recognize it whenever you combine several already-sorted sequences — the linked-list version here and the array version in the Heaps chapter are literally the same algorithm with a different container.

### Learning notes
- Why a dummy head? — it removes special handling for the first appended node.
- Why `tail` moves after every append? — it must always mark the end of the merged prefix.
- Why `a.val <= b.val` in `mergeTwo`? — ties can safely come from either list; this choice keeps list A's equal nodes first.
- Why push only non-null list heads? — empty lists have no frontier item and should not enter the heap.
- Why does the heap store `ListNode`, not just `val`? — after popping, you need `n.next` from the same source list.
- Why `if (n.next != null) pq.offer(n.next)`? — re-feeding the same stream keeps one live frontier per unfinished list.
- Why not concatenate and sort? — it ignores the already-sorted structure and pays `log N` instead of `log k`.

#### Choosing between heap merge and pairwise merge
You may also see a divide-and-conquer merge strategy: merge lists in pairs, then merge the merged lists, like a tournament bracket. That also gives O(N log k) time, because each node participates in about `log k` two-list merges. The heap version is usually easier when the inputs are streams or iterators, because you do not need to materialize intermediate merged lists. The pairwise version can be attractive for linked lists because it only uses O(1) extra heap space and leans on the already-tested `mergeTwo` helper.

A good rule of thumb: if the problem says "always output the next smallest item" or "stop after the kth item," use the heap because it can stop early. If the problem says "merge all lists" and memory is tight, pairwise merging is a valid sibling solution. Both are k-way merge; they just organize the frontier differently.

#### Details that decide correctness
Duplicates are fine: if two heap entries have the same value, either can come first and the output is still sorted. Empty lists should simply be skipped during initialization. Comparator overflow is worth mentioning in production Java: `(x, y) -> x.val - y.val` is common in interview snippets, but `Integer.compare(x.val, y.val)` is safer when values can be near integer limits. Finally, remember that the heap stores nodes or `(value, list, index)` triples, not just values, because you need provenance to advance the correct stream.

---

## Merge K Sorted Lists / Smallest Range (K-way merge) <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Smallest Range Covering Elements from K Lists](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/)*

<ProgressCheck id="merge-k-sorted-lists-smallest-range-k-way-merge" />

### Problem
Merge `k` sorted sequences into one sorted stream (and, in the sibling problem, find the smallest range that covers at least one number from **each** list).

**Constraints:** `k` lists, `N` total elements; aim for O(N log k).

**Example 1:** `[[1,4,5],[1,3,4],[2,6]]` → `1,1,2,3,4,4,5,6`.

**Example 2:** for smallest range, `[[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]` → `[20,24]`.

### Solution — brute force
For the merge-only version, concatenate all arrays and sort them: O(N log N) time and O(N) space. For smallest range, the brute force is worse: try one picked value from each list, compute the min and max, and keep the smallest width. That explodes as the product of list lengths, so it is only a thought exercise.

```java
List<Integer> mergeKSortedBrute(List<List<Integer>> lists) {
    List<Integer> values = new ArrayList<>();
    for (List<Integer> list : lists) {
        values.addAll(list);
    }
    Collections.sort(values);
    return values;
}
```

A more reasonable baseline for smallest range is to flatten every value with its list id, sort by value, then run a sliding window over the flattened list until the window covers all `k` ids. That is O(N log N) for sorting plus O(N) for the window. K-way merge is the streaming version of the same idea: because each list is already sorted, the heap produces the flattened order in O(N log k) instead of O(N log N).

O(N log N) time, O(N) space for merge-only; the direct range brute force is product-of-lengths and too slow.

### Solution — optimized
Min-heap holding one candidate (the current front) from each of the k sequences.

> [inv] **Invariant** — The heap contains at most one live element per list; its root is the global next-smallest across all lists.

The optimized range version keeps a full heap frontier and a `curMax`. The current smallest range is always from the heap minimum to that running maximum; then you advance only the list that contributed the minimum.

```java
// heap entry: {value, listIndex, elemIndex}; track current max across heap tops.
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
int curMax = Integer.MIN_VALUE;
for (int i = 0; i < lists.size(); i++) {
    int v = lists.get(i).get(0);
    pq.offer(new int[]{v, i, 0});
    curMax = Math.max(curMax, v);
}
int rangeL = 0, rangeR = Integer.MAX_VALUE;
while (pq.size() == lists.size()) {                 // must cover every list
    int[] top = pq.poll();
    if (curMax - top[0] < rangeR - rangeL) { rangeL = top[0]; rangeR = curMax; }
    int i = top[1], j = top[2] + 1;
    if (j < lists.get(i).size()) {
        int nv = lists.get(i).get(j);
        pq.offer(new int[]{nv, i, j});
        curMax = Math.max(curMax, nv);              // advance only the popped list
    }
}
```

> [note] **Trace it** — smallest range for lists `[4,10,15,24,26]`, `[0,9,12,20]`, `[5,18,22,30]`.

<CodeTrace
  title="Smallest Range Covering K Lists — 3 lists"
  :values="[4,10,15,24,26]"
  :windowKeys="['i']"
  :cellWidth="38"
  :steps='[
    { pointers: { i: 0 }, vars: { heap: "min=[0,4,5]", max: 5, range: "[0,5]" }, note: "seed with each list`s first. range width 5" },
    { pointers: { i: 0 }, vars: { heap: "min=[4,5,9]", max: 9, range: "[4,9]" }, note: "advance list-1 (0→9). width 5" },
    { pointers: { i: 0 }, vars: { heap: "min=[5,9,10]", max: 10, range: "[5,10]" }, note: "advance list-0 (4→10)" },
    { pointers: { i: 0 }, vars: { heap: "min=[9,10,18]", max: 18, range: "[9,18]" }, note: "advance list-2 (5→18). too wide" },
    { pointers: { i: 0 }, vars: { heap: "min=[10,12,18]", max: 18, range: "[10,18]" }, note: "advance list-1 (9→12). still wide" },
    { pointers: { i: 0 }, vars: { heap: "min=[15,18,20]", max: 20, range: "[15,20]" }, note: "narrows to 5. final smallest [20,24]-width=5" }
  ]'
/>
### Time Complexity
O(N log k), because each element can enter and leave the heap once, and the heap has at most k live fronts.

### Space Complexity
O(k), because the heap stores one current entry per list. The output stream itself is not counted as auxiliary space.

> [key] **Key Insight** — The smallest range that includes at least one element from every list must span the current heap min and the running max of heap tops; advancing the minimum list shrinks the window.

> [trap] **Common Trap** — Popping without re-feeding the same list. *Example:* three lists — after popping `A.head`, if you push a random next instead of `A.next`, list A gets skipped ahead and its remaining values leak into another list's stream. Push `polled.list.next` from the same list you popped.

<TrapTrace title="Popping without re-feeding the same list" input="A.head" bug="three lists — after popping 'A.head', if you push a random next instead of 'A.next', list A gets skipped ahead and its remaining values leak into another list's stream" fix="Push 'polled.list.next' from the same list you popped." />

> [note] **Interview script** — First, I'd mention the brute force: flatten and sort all values, or for the range problem slide over that flattened order while tracking covered list ids. Then I'd optimize using the fact that each input list is sorted, so a heap can generate the same global order with only `k` live entries. For smallest range, I track the heap minimum and the current maximum among heap entries; every full heap gives a candidate range. The complexity is O(N log k) time and O(k) space.

> [pat] **Pattern Connection** — The shared idea is a **min-heap holding one live "front" per sorted source**, so the global next-smallest is always at the root. Recognize it whenever you must interleave *k* ordered streams: *Merge k Sorted Lists*, *Ugly Number II* (three implicit streams ×2/×3/×5), and *Kth Smallest in a Sorted Matrix* (each row is a stream). Once you see "k sorted things," reach for the heap-of-fronts rather than merging pairwise.

### Learning notes
- Why store `{value, listIndex, elemIndex}`? — after popping a value, you must know exactly which list to advance.
- Why initialize with the first element of every list? — the range problem needs one live value from each list before any candidate is valid.
- Why track `curMax` separately? — a min-heap gives the minimum quickly, but not the maximum.
- Why loop while `pq.size() == lists.size()`? — once any list is exhausted, no future range can cover every list.
- Why advance only the popped minimum list? — moving any other list cannot improve the left edge of the current range.
- Why compare `curMax - top[0]`? — every full frontier covers all lists, so min-to-max is the candidate range.
- Why not pairwise merge first? — the heap can solve streaming/range variants without materializing the full merged order.

### Same pattern, new tweaks

| Variation | The one thing that changes |
|---|---|
| [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | No heap needed; one comparison between two fronts is enough. |
| [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | A min-heap of the `k` current heads yields the global next-smallest. |
| [Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) | Treat each row as a sorted stream; pop `k-1` times, then read the heap top. |
| [Smallest Range Covering Elements from K Lists](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/) | Keep a full frontier, and compare `heapMin..curMax` before advancing the minimum stream. |
| [Ugly Number II / Super Ugly Number](https://leetcode.com/problems/ugly-number-ii/) | The streams are implicit multiples; duplicate values must be de-duped carefully. |

---

## Check your understanding

<Quiz
  pattern-id="k-way-merge"
  :questions='[{"q": "For merging k sorted lists into one, what is the heap-based complexity?", "choices": [{"text": "O(N log k) where N = total elements", "correct": true, "explanation": "Heap holds one head per list; O(log k) per pop."}, {"text": "O(N log N)", "correct": false, "explanation": "Full sort of merged; wastes existing sortedness."}, {"text": "O(k · N)", "correct": false, "explanation": "Naive round-robin merge."}, {"text": "O(N)", "correct": false}]}, {"q": "For Smallest Range Covering k Lists, what does the heap track?", "choices": [{"text": "Current-minimum across all lists (via one pointer per list)", "correct": true, "explanation": "And separately track current-max seen; range = [heapMin, currentMax]."}, {"text": "All possible ranges", "correct": false, "explanation": "Exponential; not needed."}, {"text": "Only the k smallest values", "correct": false, "explanation": "Different problem."}, {"text": "Only the k largest values", "correct": false}]}, {"q": "When does K-way Merge stop for the \"smallest range\" problem?", "choices": [{"text": "When any one list is exhausted", "correct": true, "explanation": "We can no longer cover that list; done."}, {"text": "When the heap is empty", "correct": false, "explanation": "That is total exhaustion."}, {"text": "After N iterations", "correct": false}, {"text": "Never", "correct": false}]}, {"q": "For Ugly Number II, why does the 3-pointer approach beat the min-heap?", "choices": [{"text": "It avoids duplicates and the heap overhead — pure O(n)", "correct": true, "explanation": "Three pointers into the growing ugly[] give exact sequence generation."}, {"text": "It uses less memory", "correct": false, "explanation": "Same memory."}, {"text": "Heap doesn’t work", "correct": false, "explanation": "Heap works too, but slower."}, {"text": "Randomness", "correct": false}]}, {"q": "Merging two sorted linked lists is best done with:", "choices": [{"text": "Two-pointer merge with a dummy head, in-place re-linking", "correct": true, "explanation": "O(m+n) time, O(1) space (nodes reused)."}, {"text": "Copying to array, sorting, rebuilding", "correct": false, "explanation": "Wastes existing sortedness."}, {"text": "Heap-based merge", "correct": false, "explanation": "Overkill for k=2."}, {"text": "Recursion only", "correct": false, "explanation": "Works but O(n) stack."}]}]'
/>

<PrintButton />

<RelatedPatterns pattern-id="heap" />
