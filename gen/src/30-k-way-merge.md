# K-way Merge


<PatternVideo pattern-name="K-way Merge" duration="8–12 min" />

<PatternProgress pattern-id="k-way-merge" problems="k-way-merge-k-sorted-lists, merge-two-sorted-lists, smallest-range-covering-elements-from-k-lists, find-k-pairs-with-smallest-sums, find-median-from-data-stream, ugly-number-ii" />

<script setup>
const bareTemplateCode = `# python — min-heap of (value, source, index-into-source)
import heapq
def kway_merge(sorted_lists):
    heap = []
    for i, lst in enumerate(sorted_lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    out = []
    while heap:
        value, i, j = heapq.heappop(heap)
        out.append(value)
        if j + 1 < len(sorted_lists[i]):
            heapq.heappush(heap, (sorted_lists[i][j+1], i, j+1))  # re-feed SAME list
    return out`

const bareInvariant = {
  statement: `At every iteration, the heap contains at most one live element per sorted source, and its root is the globally smallest element not yet emitted.`,
  initialization: `Seed with each source's first element. One element per non-empty source; the heap root is the smallest of these — which equals the smallest unemitted element overall (each source is already sorted, so the first element is each source's minimum).`,
  maintenance: `When we pop \`(v, i, j)\`, \`v\` is emitted (it's the global minimum). Then we push \`(sorted_lists[i][j+1], i, j+1)\` — same source, next position. This preserves "at most one per source" and "the root is the global minimum of unemitted elements": the only new element being considered is from source \`i\` (every other source's unemitted frontier is unchanged), and \`sorted_lists[i][j+1] >= v\` since source \`i\` is sorted.`,
  termination: `The heap drains when every source is exhausted. The sequence of emitted values is sorted (each is the global minimum at its pop time) and contains every element exactly once (we re-fed after each pop until each source ran out).`
}

const bareComplexity = {
  time: `O(N log k) — each of N elements is pushed and popped once; heap ops are O(log k).`,
  space: `O(k) for the heap (one representative per live source).`
}

const templateSpecializations = [
  { slug: `merge-k-sorted-lists-hard`, title: `Merge K Sorted Lists` },
  { slug: `find-k-pairs-with-smallest-sums-medium`, title: `K Pairs Smallest Sums` },
  { slug: `find-median-from-data-stream-hard`, title: `Median from Stream` }
]

const kPairsCode = `# python — Cartesian k-way, lazy frontier
import heapq
def kSmallestPairs(nums1, nums2, k):
    if not nums1 or not nums2: return []
    heap = [(nums1[0] + nums2[0], 0, 0)]       # seed only (0,0)
    seen = {(0, 0)}
    out = []
    while heap and len(out) < k:
        s, i, j = heapq.heappop(heap)
        out.append([nums1[i], nums2[j]])
        for ni, nj in [(i+1, j), (i, j+1)]:   # grow frontier right/down
            if ni < len(nums1) and nj < len(nums2) and (ni, nj) not in seen:
                heapq.heappush(heap, (nums1[ni] + nums2[nj], ni, nj))
                seen.add((ni, nj))
    return out`

const kPairsInvariant = {
  statement: `The heap contains all unvisited (i, j) frontier cells adjacent to visited cells, and its root is always the smallest-sum unvisited pair.`,
  initialization: `Seed with \`(nums1[0] + nums2[0], 0, 0)\`. Since both arrays are sorted ascending, \`(0, 0)\` is the smallest possible sum.`,
  maintenance: `After popping the smallest \`(s, i, j)\`, we add its two downward/rightward neighbors \`(i+1, j)\` and \`(i, j+1)\` (if unseen). The next smallest unvisited pair cannot lie in a cell whose dominator \`(i', j') ≤ (i, j)\` component-wise is unvisited — those were already popped. So the frontier is always complete, and the heap root is still the smallest unvisited sum.`,
  termination: `We stop after emitting k pairs, which is the problem's request. The remaining frontier is discarded.`
}

const medianCode = `# python — two heaps: max-heap for lower half, min-heap for upper half
import heapq
class MedianFinder:
    def __init__(self):
        self.lo = []    # max-heap (store negatives)
        self.hi = []    # min-heap
    def addNum(self, num):
        heapq.heappush(self.lo, -num)             # tentatively add to lo
        heapq.heappush(self.hi, -heapq.heappop(self.lo))  # move lo-max to hi
        if len(self.hi) > len(self.lo):           # keep sizes balanced
            heapq.heappush(self.lo, -heapq.heappop(self.hi))
    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0`

const medianInvariant = {
  statement: `After every \`addNum\`, \`lo\` holds the smaller half (max-heap) and \`hi\` holds the larger half (min-heap); \`|lo| \in \{|hi|, |hi|+1\}\` and \`max(lo) <= min(hi)\`.`,
  initialization: `Before any inserts, both heaps are empty — the invariant holds vacuously.`,
  maintenance: `Each insert does: (1) push to \`lo\`, (2) move \`lo\`'s max to \`hi\` (so the two heaps are "almost split" by magnitude), (3) rebalance by moving \`hi\`'s min back to \`lo\` if \`|hi| > |lo|\`. After step 2, \`max(lo) <= min(hi)\` (we just moved the previous \`lo\`-max into \`hi\`, so it stays the min of \`hi\` or gets displaced by something smaller). After step 3, sizes satisfy the constraint.`,
  termination: `For a stream, the invariant is maintained after every call; the median is read from the invariant: if \`|lo| > |hi|\`, it's \`lo\`'s top; else the average of the two tops.`
}

const trapAcode = {
  statement: `Not re-feeding the heap from the SAME source after a pop.`,
  bug: `On three lists \`[1,4], [1,3], [2,6]\`, after popping \`1\` from list A, if you forget to push \`A.next\`, list A disappears from the heap and its remaining \`4\` is silently dropped from the output.`,
  fix: `The pop + push happen together: after \`(v, i, j) = heappop()\`, immediately \`heappush((sorted_lists[i][j+1], i, j+1))\` if \`j+1\` is in range. Always push from the same source index \`i\`.`
}

const trapBcode = {
  statement: `Comparator overflow on int subtraction in Java/C++.`,
  bug: `A comparator like \`(a, b) -> a.val - b.val\` returns the wrong sign when \`a.val\` and \`b.val\` straddle \`Integer.MIN_VALUE\` or \`MAX_VALUE\`; the heap silently violates its ordering and the merged output is non-decreasing.`,
  fix: `Use \`Integer.compare(a.val, b.val)\` in Java or an explicit comparison (\`<\`, \`>\`) rather than subtraction. Python's tuples compare naturally; this trap applies only to typed languages.`
}

const trapCcode = {
  statement: `Visiting duplicate frontier cells in Cartesian / Ugly Number k-way variants.`,
  bug: `In K Smallest Pairs, when you expand \`(i, j)\` to both \`(i+1, j)\` and \`(i, j+1)\`, cell \`(1, 1)\` is reachable from \`(0, 1)\` AND from \`(1, 0)\`. Without a \`seen\` set, you push it twice and the heap pops it twice — the output contains the same pair repeated.`,
  fix: `Maintain a \`seen\` set keyed by cell coordinates. Push only if the cell hasn't been added. Alternative: seed the heap with the entire first column \`(0, j)\` and only expand rightward — this gives each pair exactly one entry path.`
}

const quizQuestions = [
  {q: "For merging k sorted lists into one, what is the heap-based complexity?", choices: [{text: "O(N log k) where N = total elements", correct: true, explanation: "Heap holds one head per list; O(log k) per pop."}, {text: "O(N log N)", correct: false, explanation: "Full sort of merged; wastes existing sortedness."}, {text: "O(k · N)", correct: false, explanation: "Naive round-robin merge."}, {text: "O(N)", correct: false}]},
  {q: "For Smallest Range Covering k Lists, what does the heap track?", choices: [{text: "Current-minimum across all lists (via one pointer per list)", correct: true, explanation: "And separately track current-max seen; range = [heapMin, currentMax]."}, {text: "All possible ranges", correct: false, explanation: "Exponential; not needed."}, {text: "Only the k smallest values", correct: false, explanation: "Different problem."}, {text: "Only the k largest values", correct: false}]},
  {q: "For K Pairs with Smallest Sums, why do we need a seen set when expanding (i,j) in both directions?", choices: [{text: "Cell (i+1, j+1) is reachable from two directions — without deduping, the same pair is emitted twice", correct: true, explanation: "The Cartesian grid has multiple paths to each cell; the seen set prevents double-counting."}, {text: "Memory optimization only", correct: false, explanation: "It is correctness, not just memory."}, {text: "To speed up the heap", correct: false}, {text: "It's not needed", correct: false}]},
  {q: "In the two-heap Median-from-Stream pattern, why do we move the lo-max to hi before rebalancing?", choices: [{text: "It enforces max(lo) ≤ min(hi) regardless of insertion order", correct: true, explanation: "Direct push to lo could leave a value in lo that's bigger than hi's min; routing through hi fixes it."}, {text: "It saves memory", correct: false}, {text: "It avoids heap overflow", correct: false}, {text: "It's not necessary", correct: false, explanation: "It is necessary for correctness."}]},
  {q: "Merging two sorted linked lists is best done with:", choices: [{text: "Two-pointer merge with a dummy head, in-place re-linking", correct: true, explanation: "O(m+n) time, O(1) space (nodes reused)."}, {text: "Copying to array, sorting, rebuilding", correct: false, explanation: "Wastes existing sortedness."}, {text: "Heap-based merge", correct: false, explanation: "Overkill for k=2."}, {text: "Recursion only", correct: false, explanation: "Works but O(n) stack."}]}
]

const mergeKSolvePrompt = `Merge \`k\` sorted linked lists into one sorted list. Example: \`[[1,4,5],[1,3,4],[2,6]]\` → \`1→1→2→3→4→4→5→6\`.`

const kPairsSolvePrompt = `Given two sorted arrays \`nums1\` and \`nums2\` and integer \`k\`, return the \`k\` pairs \`(nums1[i], nums2[j])\` with the smallest sums.`

const medianSolvePrompt = `Design a data stream median finder: \`addNum(x)\` inserts \`x\`; \`findMedian()\` returns the current median. Both must be sub-O(n).`

const mergeKJavaCode = `// mergeTwo (k=2 special case):
ListNode mergeTwo(ListNode a, ListNode b) {
    ListNode dummy = new ListNode(0), tail = dummy;
    while (a != null && b != null) {
        if (a.val <= b.val) { tail.next = a; a = a.next; }
        else                { tail.next = b; b = b.next; }
        tail = tail.next;
    }
    tail.next = (a != null) ? a : b;
    return dummy.next;
}

// mergeKLists:
ListNode mergeKLists(ListNode[] lists) {
    PriorityQueue<ListNode> pq = new PriorityQueue<>((x, y) -> Integer.compare(x.val, y.val));
    for (ListNode l : lists) if (l != null) pq.offer(l);
    ListNode dummy = new ListNode(0), tail = dummy;
    while (!pq.isEmpty()) {
        ListNode n = pq.poll();
        tail.next = n; tail = n;
        if (n.next != null) pq.offer(n.next);
    }
    return dummy.next;
}`

const smallestRangeCode = `PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
int curMax = Integer.MIN_VALUE;
for (int i = 0; i < lists.size(); i++) {
    int v = lists.get(i).get(0);
    pq.offer(new int[]{v, i, 0});
    curMax = Math.max(curMax, v);
}
int rangeL = 0, rangeR = Integer.MAX_VALUE;
while (pq.size() == lists.size()) {
    int[] top = pq.poll();
    if (curMax - top[0] < rangeR - rangeL) { rangeL = top[0]; rangeR = curMax; }
    int i = top[1], j = top[2] + 1;
    if (j < lists.get(i).size()) {
        int nv = lists.get(i).get(j);
        pq.offer(new int[]{nv, i, j});
        curMax = Math.max(curMax, nv);
    }
}`
</script>

## Why k-way merge exists — the story

You're an infrastructure engineer at Snowflake. A user submits a query that scans 200 columnar files, each already sorted by timestamp. To answer the query, you need one *globally* sorted stream of rows. And the total data is **1.4 TB** — you cannot load it all into memory.

The obvious approach: concatenate all 200 files and sort. Correct — for a small `n`. But you have 1.4 TB and 128 GB of RAM. External sort passes over disk multiple times, at ~500 MB/s. Result: **50 minutes per query.** Your users churn. This is why every early database, from the 1960s tape drives to MySQL circa 2005, felt slow on aggregations: they used naive merge-sort-then-scan.

But look at the input. Every file is **already sorted**. That's the gift the data model gave you — and full sorting throws it away. If the head of file A is `t=1000` and the head of file B is `t=999`, then B's next row is guaranteed to be the globally-smallest remaining row. You never need to compare it against the tails of A, B, ..., F. **You only need to compare the heads.**

That's k-way merge: maintain `k` cursors, one per input file. Put the current head value of each into a min-heap of size `k`. Repeatedly `pop` the smallest head, emit it, and `push` the next value from that same file. Each of the total `N` rows costs `log k`, not `log N`. For 200 files of 1B rows each: `2·10¹¹ · log₂(200) ≈ 1.5·10¹²` ops — but no disk re-reads, no memory blow-up. Snowflake, BigQuery, DuckDB, Spark — every columnar OLAP engine on Earth is doing this at the bottom of its query plan.

> [key] **Key Insight** — The heap holds a moving *frontier* of size k, one representative per stream. Its top is always the globally smallest remaining value.

This is also why k-way merge feels like a cousin of Dijkstra's algorithm. Dijkstra keeps a heap of the best currently-known frontier nodes and expands the cheapest one next. K-way merge keeps a heap of stream fronts and expands the smallest one next. In both, the heap is not magic; it is just an efficient way to ask, again and again, "which frontier item should I process next?"

## The bare mechanic — simplest working example

Three sorted lists: `[1,4,5]`, `[1,3,4]`, `[2,6]`. Seed the heap with their heads, then pop + re-feed from the same list until empty.

| step | heap before pop | pop | re-feed | output |
|---|---|---|---|---|
| 1 | `(1,A,0), (1,B,0), (2,C,0)` | `(1,A,0)` | `(4,A,1)` | `1` |
| 2 | `(1,B,0), (2,C,0), (4,A,1)` | `(1,B,0)` | `(3,B,1)` | `1,1` |
| 3 | `(2,C,0), (3,B,1), (4,A,1)` | `(2,C,0)` | `(6,C,1)` | `1,1,2` |
| 4 | `(3,B,1), (4,A,1), (6,C,1)` | `(3,B,1)` | `(4,B,2)` | `1,1,2,3` |
| 5 | `(4,A,1), (4,B,2), (6,C,1)` | `(4,A,1)` | `(5,A,2)` | `1,1,2,3,4` |
| 6 | `(4,B,2), (5,A,2), (6,C,1)` | `(4,B,2)` | — | `1,1,2,3,4,4` |
| 7 | `(5,A,2), (6,C,1)` | `(5,A,2)` | — | `1,1,2,3,4,4,5` |
| 8 | `(6,C,1)` | `(6,C,1)` | — | `1,1,2,3,4,4,5,6` |

```svg
<svg role="img" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="K-way merge bare mechanic">
  <rect x="0" y="0" width="400" height="200" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">heap of 3 heads, pop + re-feed same source</text>
  <g text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">
    <rect x="30" y="46" width="30" height="30" rx="6" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/><text x="45" y="66">1</text>
    <rect x="62" y="46" width="30" height="30" rx="6" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/><text x="77" y="66">4</text>
    <rect x="94" y="46" width="30" height="30" rx="6" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/><text x="109" y="66">5</text>
    <rect x="30" y="88" width="30" height="30" rx="6" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/><text x="45" y="108">1</text>
    <rect x="62" y="88" width="30" height="30" rx="6" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/><text x="77" y="108">3</text>
    <rect x="94" y="88" width="30" height="30" rx="6" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/><text x="109" y="108">4</text>
    <rect x="30" y="130" width="30" height="30" rx="6" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/><text x="45" y="150">2</text>
    <rect x="62" y="130" width="30" height="30" rx="6" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/><text x="77" y="150">6</text>
  </g>
  <g font-size="10" fill="var(--dsa-neutral)">
    <text x="12" y="66">A</text><text x="12" y="108">B</text><text x="12" y="150">C</text>
  </g>
  <text x="230" y="60" font-size="11" font-weight="700" fill="var(--dsa-success)">min-heap</text>
  <circle cx="265" cy="80" r="18" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <circle cx="235" cy="118" r="18" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/>
  <circle cx="295" cy="118" r="18" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/>
  <g text-anchor="middle" font-size="14" font-weight="700" fill="var(--dsa-ink)">
    <text x="265" y="85">1</text><text x="235" y="123">1</text><text x="295" y="123">2</text>
  </g>
  <text x="365" y="110" font-size="10" font-weight="700" text-anchor="end" fill="var(--dsa-neutral)">output stream</text>
  <text x="365" y="145" text-anchor="end" font-size="13" font-weight="700" fill="var(--dsa-ink)">1 → 1 → 2 → …</text>
  <text x="200" y="185" text-anchor="middle" font-size="11" font-style="italic" fill="var(--dsa-neutral)">each pop re-feeds from the SAME source — this is the invariant</text>
</svg>
```

<PatternTemplateCard
  slug="kway-bare"
  language="python"
  :code="bareTemplateCode"
  :invariant="bareInvariant"
  :complexity="bareComplexity"
  problemShape="k sorted sequences → one sorted stream via min-heap of fronts"
  defaultRevealed />

## When to use it — and when not to

### Recognize by
- "merge k sorted lists / arrays / files" — several already-ordered sources must become one ordered result.
- "smallest range covering elements from k lists" — you must keep one live value from each list.
- "kth smallest in a sorted matrix" — each row or column can be treated as a sorted stream.
- "external sort runs" — sorted chunks on disk are merged without loading everything.
- "find k pairs with smallest sums" — the candidate pairs form ordered frontiers.
- "always choose the next smallest available item among k sources" — a min-heap of fronts is likely.

### When NOT to use it
The k streams aren't sorted individually — a heap over the current fronts is meaningless if the fronts don't represent "smallest not-yet-emitted". Sort each stream first, or use a different approach.

Also be careful when:
- you only have one unsorted collection; use sorting or quickselect instead.
- `k` is tiny and fixed, like 2; a direct two-pointer merge is simpler and faster.
- you need random access by rank after many updates; a balanced tree or indexed structure may fit better.
- the next item in a stream is expensive to fetch and you cannot prefetch; design the iterator boundary first.
- duplicate handling changes the problem, such as needing distinct values only; add that policy explicitly after popping.

## History — von Neumann's tape sort, 1945

The k-way merge originated in **John von Neumann's 1945 draft *"First Draft of a Report on the EDVAC"***, the founding document of stored-program computing. Von Neumann's motivating problem: sort a data set too large to fit in the machine's memory. His answer was **external merge sort** — split the input into runs that fit in memory, sort each, then merge the sorted runs back with a k-way merge. His original paper used **magnetic tape drives** as the "streams" and had `k = 4` (four tape decks common on IBM 704 systems).

The **loser tree** (a compact heap variant) was introduced by Knuth in *TAOCP Vol 3* (1973) as the specific data structure for the merge step; it uses `k − 1` comparisons per output element instead of the plain heap's `log₂ k`, which matters when disk I/O time is comparable to CPU time. When you tell an interviewer "the k-way merge with a heap is O(N log k)," you're citing an algorithm the entire OLAP industry runs on.

## THE template

<PatternTemplateCard
  slug="kway-canonical"
  title="K-way merge canonical template"
  language="python"
  :code="bareTemplateCode"
  :invariant="bareInvariant"
  :complexity="bareComplexity"
  :specializations="templateSpecializations"
  problemShape="k sorted sources → min-heap of fronts → pop + re-feed from popped source" />

## Interactive diagram

<HeapAnim />

## Sub-variations of the template

<PatternSubVariationNav pattern="k-way-merge" />

### Merge K Sorted Lists <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)*

<ProgressCheck id="merge-k-sorted-lists-hard" />

> [key] **The twist:** linked lists instead of arrays — each entry in the heap is a node, and the next pointer serves as the "next element of the same source" we re-feed.

<InvariantProof
  :statement="bareInvariant.statement"
  :initialization="bareInvariant.initialization"
  :maintenance="bareInvariant.maintenance"
  :termination="bareInvariant.termination" />

```svg
<svg role="img" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Diagram illustrating: Merge Two / K Sorted Lists Hard">
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
</svg>
```

> [key] **Blind-solve first:** {{ mergeKSolvePrompt }}

<TemplateReveal
  slug="merge-k-sorted-lists"
  language="java"
  :canonical="mergeKJavaCode"
  problemShape="k sorted linked lists → min-heap of head nodes → O(N log k)" />

**Trace** on `[[1,4,5],[1,3,4],[2,6]]`:

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

#### Related sibling: Smallest Range Covering Elements from K Lists

Same engine, different stopping condition. Keep a full-frontier heap (one live element per list), track the max of heap tops separately. The current candidate range is `[heap.min, curMax]`. On each pop, update best, then advance only the popped list. Stop when any list is exhausted (future ranges cannot cover all lists).

```java
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
int curMax = Integer.MIN_VALUE;
for (int i = 0; i < lists.size(); i++) {
    int v = lists.get(i).get(0);
    pq.offer(new int[]{v, i, 0});
    curMax = Math.max(curMax, v);
}
int rangeL = 0, rangeR = Integer.MAX_VALUE;
while (pq.size() == lists.size()) {
    int[] top = pq.poll();
    if (curMax - top[0] < rangeR - rangeL) { rangeL = top[0]; rangeR = curMax; }
    int i = top[1], j = top[2] + 1;
    if (j < lists.get(i).size()) {
        int nv = lists.get(i).get(j);
        pq.offer(new int[]{nv, i, j});
        curMax = Math.max(curMax, nv);
    }
}
```

Also same engine: **Kth Smallest in a Sorted Matrix** — treat each row as a stream, pop `k-1` times, read the top.

#### Choosing between heap merge and pairwise merge

A divide-and-conquer merge strategy also works: merge lists in pairs, then merge the merged lists, like a tournament bracket — also O(N log k). The heap version is easier when inputs are streams or iterators (no intermediate materialization). The pairwise version uses O(1) extra space on linked lists and leans on `mergeTwo` as a helper. Both are k-way merge, just organizing the frontier differently.

---

### Find K Pairs with Smallest Sums <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Find K Pairs with Smallest Sums](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/)*

> [key] **The twist:** the k "sources" are an *implicit grid* `nums1 × nums2`. Each cell `(i, j)` has sum `nums1[i] + nums2[j]`. The k-way frontier isn't given — it's generated lazily by expanding from `(0, 0)` outward. Watch the duplicate-cell trap.

<InvariantProof
  :statement="kPairsInvariant.statement"
  :initialization="kPairsInvariant.initialization"
  :maintenance="kPairsInvariant.maintenance"
  :termination="kPairsInvariant.termination" />

```svg
<svg role="img" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="K-pairs Cartesian frontier">
  <rect x="0" y="0" width="400" height="200" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">lazy frontier on nums1 × nums2 grid</text>
  <g font-size="12" fill="var(--dsa-ink)" text-anchor="middle">
    <rect x="60" y="46" width="40" height="30" rx="5" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="2"/><text x="80" y="66">(0,0)=2</text>
    <rect x="110" y="46" width="40" height="30" rx="5" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/><text x="130" y="66">(0,1)=4</text>
    <rect x="160" y="46" width="40" height="30" rx="5" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/><text x="180" y="66">(0,2)=6</text>
    <rect x="60" y="86" width="40" height="30" rx="5" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/><text x="80" y="106">(1,0)=4</text>
    <rect x="110" y="86" width="40" height="30" rx="5" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/><text x="130" y="106">(1,1)=6</text>
    <rect x="60" y="126" width="40" height="30" rx="5" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/><text x="80" y="146">(2,0)=6</text>
  </g>
  <text x="280" y="80" font-size="11" fill="var(--dsa-ink)">nums1 = [1, 3, 5]</text>
  <text x="280" y="100" font-size="11" fill="var(--dsa-ink)">nums2 = [1, 3, 5]</text>
  <text x="280" y="135" font-size="11" font-weight="700" fill="var(--dsa-success)">heap top: (0,0) sum=2</text>
  <text x="200" y="185" text-anchor="middle" font-size="10" font-style="italic" fill="var(--dsa-neutral)">cell (1,1) reachable from (0,1) OR (1,0) — need seen set</text>
</svg>
```

> [key] **Blind-solve first:** {{ kPairsSolvePrompt }}

<TemplateReveal
  slug="find-k-pairs-with-smallest-sums"
  language="python"
  :canonical="kPairsCode"
  problemShape="implicit grid; heap on frontier of (i, j) cells; seen-set dedup" />

**Trace** on `nums1 = [1, 3, 5]`, `nums2 = [1, 3, 5]`, `k = 4`:
- Seed heap: `(2, 0, 0)`.
- Pop `(2, 0, 0)` → emit `[1,1]`. Push `(4, 1, 0)` and `(4, 0, 1)`. Heap: `[(4,0,1), (4,1,0)]`.
- Pop `(4, 0, 1)` → emit `[1,3]`. Push `(6, 1, 1)` and `(6, 0, 2)`. Heap: `[(4,1,0), (6,0,2), (6,1,1)]`.
- Pop `(4, 1, 0)` → emit `[3,1]`. Push `(6, 2, 0)` and `(6, 1, 1)` is already seen → skip. Heap: `[(6,0,2), (6,1,1), (6,2,0)]`.
- Pop `(6, 0, 2)` → emit `[1,5]`. (`k = 4` reached.)
- **Result:** `[[1,1], [1,3], [3,1], [1,5]]`.

**Alternative seeding:** push the entire first column `(0, 0), (0, 1), (0, 2), ...` upfront, then only expand `(i, j)` to `(i+1, j)` — each cell has exactly one entry path and no `seen` set is needed. Trade-off: upfront `O(min(k, n2))` pushes vs. lazy.

**Also same engine:** *Ugly Number II* is a k-way merge over three implicit streams (×2, ×3, ×5). The classic 3-pointer solution is strictly better than a heap because it does pure O(n) with no duplicates — a sign that for *very* structured implicit streams, direct pointer management beats heap overhead.

---

### Find Median from Data Stream <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)*

> [key] **The twist:** two heaps balancing against each other act as "two sorted sources" we're virtually merging. The median lives on the boundary between them. This is k-way merge with `k = 2` but running online, insert by insert.

<InvariantProof
  :statement="medianInvariant.statement"
  :initialization="medianInvariant.initialization"
  :maintenance="medianInvariant.maintenance"
  :termination="medianInvariant.termination" />

```svg
<svg role="img" viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Two-heap median finder">
  <rect x="0" y="0" width="400" height="180" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">lo = max-heap (smaller half) · hi = min-heap (larger half)</text>
  <rect x="40" y="52" width="150" height="90" rx="8" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <text x="115" y="72" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-success)">lo (max-heap)</text>
  <text x="115" y="105" text-anchor="middle" font-size="22" font-weight="700" fill="var(--dsa-ink)">[5, 3, 1]</text>
  <text x="115" y="132" text-anchor="middle" font-size="10" fill="var(--dsa-neutral)">top = 5</text>
  <rect x="210" y="52" width="150" height="90" rx="8" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
  <text x="285" y="72" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-primary)">hi (min-heap)</text>
  <text x="285" y="105" text-anchor="middle" font-size="22" font-weight="700" fill="var(--dsa-ink)">[6, 8, 10]</text>
  <text x="285" y="132" text-anchor="middle" font-size="10" fill="var(--dsa-neutral)">top = 6</text>
  <text x="200" y="165" text-anchor="middle" font-size="11" font-style="italic" fill="var(--dsa-neutral)">median = (5 + 6) / 2 = 5.5 (even count) · 5 if odd and |lo| > |hi|</text>
</svg>
```

> [key] **Blind-solve first:** {{ medianSolvePrompt }}

<TemplateReveal
  slug="find-median-from-data-stream"
  language="python"
  :canonical="medianCode"
  problemShape="online stream → two heaps balanced at the median boundary" />

**Trace** on `addNum(1), addNum(2), addNum(3)`:
- `add(1)`: push to lo `[-1]`. Move lo-max to hi: hi `[1]`, lo `[]`. Rebalance: move hi-min to lo. lo `[-1]`, hi `[]`. Median = 1.
- `add(2)`: push to lo `[-2, -1]`. Move lo-max to hi: hi `[2]`, lo `[-1]`. Sizes equal. Median = (1 + 2)/2 = 1.5.
- `add(3)`: push to lo `[-3, -1]`. Move lo-max to hi: hi `[2, 3]`, lo `[-1]`. |hi| > |lo| → move hi-min to lo: lo `[-2, -1]`, hi `[3]`. Median = 2.

**Why "k-way merge"?** Because `addNum` is doing a tiny merge-step between two sorted sources (lo and hi) every insert — it routes the new value through the heap boundary. The structural idea — two heaps with controlled sizes anchored at a boundary — generalizes to **sliding-window median** (chapter 25) and **median-of-k-streams** in distributed OLAP engines.

---

## Traps & gotchas

<TrapTrace
  :title="trapAcode.statement"
  :bug="trapAcode.bug"
  :fix="trapAcode.fix" />

<TrapTrace
  :title="trapBcode.statement"
  :bug="trapBcode.bug"
  :fix="trapBcode.fix" />

<TrapTrace
  :title="trapCcode.statement"
  :bug="trapCcode.bug"
  :fix="trapCcode.fix" />

## In the wild — PostgreSQL's external sort (`tuplesort.c`)

When a PostgreSQL query needs `ORDER BY` on a result set bigger than `work_mem`, the planner calls into `src/backend/utils/sort/tuplesort.c`. The algorithm:

1. **Phase 1 (run generation)**: read `work_mem` worth of tuples, sort them in RAM with introsort, flush as a sorted "run" to a temp file. Repeat until all input is consumed.
2. **Phase 2 (merge)**: open all runs as `k` sorted streams and k-way merge them with a **replacement selection heap** (a loser-tree variant from Knuth TAOCP Vol 3). The replacement selection reduces disk I/O by producing a smaller number of longer runs, which merge faster in phase 2.
3. **Multi-pass merge**: if `k > ioMergeOrder` (typically ~500), merge in multiple passes, writing intermediate runs to disk, until the final pass merges ≤ `k` runs into the output stream.

`tuplesort.c` has been battle-tested across every major database since Postgres95 (1996). The code specifically credits **Knuth's TAOCP Volume 3, Algorithm 5.4.1R**, as the implementation reference.

Other named production uses:
- **Apache Spark** `ShuffleExternalSorter`: runs produced per task, merged by `TaskMemoryManager` with a k-way merge in the reduce stage.
- **DuckDB `ExternalSort`**: the standard analytical-DB external sort over Parquet files.
- **Google Logs 'cat **/log.*.gz | sort'** idioms: multi-file sorted log merge for serving monitoring queries.
- **ClickHouse `MergeTree`**: on-disk sorted data parts; background merges run k-way across parts.
- **git log** (across packed revs): k-way merge of several commit date streams in `git/revision.c`.

## Recognition drill

<RecognitionDrill pattern="k-way-merge" :count="10" />

## Advanced — follow-ups and failure modes

<details>
<summary><b>What if the streams are infinite (true online k-way merge)?</b></summary>

The heap-based template still works — iterator-based rather than array-indexed. In Java, use `Iterator<Integer>` per source; push the first value, then after each pop advance the iterator and push `.next()` if it has more. Spark, Flink, and Kafka Streams all use this pattern for merging multiple ordered partitioned streams.
</details>

<details>
<summary><b>What if N is huge and log k is a bottleneck — loser trees.</b></summary>

Knuth's **loser tree** (TAOCP Vol 3, 5.4.1) uses `k - 1` comparisons per output element but with a lower constant factor than a plain heap because each push doesn't require a sift. For CPU-cache-bound external sorts (where disk I/O dominates), the loser tree saves perhaps 15-25% CPU vs. a plain binary heap. Postgres' `tuplesort.c` uses it in phase 2.
</details>

<details>
<summary><b>What if elements have equal values and you need a stable merge?</b></summary>

A plain min-heap breaks ties arbitrarily. For a stable merge (ties resolved by source order), include the source index as a tie-breaker in the heap key: `(value, source_index)` instead of just `value`. Python's tuple comparison handles this naturally.

Where it matters: SQL `ORDER BY stable_column, tie_breaker`, external sort when the input ordering must be preserved on ties, event-sourced logs where "when" matters more than "what" when timestamps collide.
</details>

<details>
<summary><b>What if streams are very wide (k = 10,000) and n per stream is small?</b></summary>

The heap of size k loses its edge; `O(N log k)` approaches `O(N log N)`. Reach for a **tournament tree** (special loser-tree variant) which keeps the comparison depth exactly `log k` and amortizes better than a heap when k is large. For k > ~10^6, you fall off the end of practical in-memory merging and need a disk-based multi-pass merge like Postgres does.
</details>

<details>
<summary><b>Breaking point — when k-way merge stops being the right pattern.</b></summary>

- **Single unsorted collection**: no sorted sources → use sorting / quickselect (chapter 41).
- **k = 2 with linked lists**: use direct two-pointer merge; the heap overhead is unnecessary.
- **Random-access needed on the merged result**: materialize into an array; the streaming heap pattern doesn't support jumping around.
- **Streams have strong structure** (geometric progressions, arithmetic series): direct pointer management (3-pointer Ugly Number) beats the heap.
</details>

### Cross-pattern problems

| Problem | Primary pattern | What k-way merge contributes |
|---|---|---|
| [Super Ugly Number](https://leetcode.com/problems/super-ugly-number/) | k-way merge | heap of k implicit prime-multiple streams |
| [Smallest Range Covering Elements from K Lists](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/) | k-way merge + sliding window | heap maintains the min; separately track max |
| [Sort a Nearly Sorted (K-Sorted) Array](https://leetcode.com/problems/sort-nearly-sorted-array/) | heap sort | min-heap of size k slides across the array; each pop is the next output |

## Related patterns + Check your understanding

<RelatedPatterns pattern-id="heap" />

<Quiz
  pattern-id="k-way-merge"
  :questions="quizQuestions" />

<PrintButton />
