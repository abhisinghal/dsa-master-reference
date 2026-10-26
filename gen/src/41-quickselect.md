# Quickselect

<script setup>
const quickselectTemplate = `int findKthSmallest(int[] a, int k) {
  int target = k - 1;                   // 0-based target index
  int lo = 0, hi = a.length - 1;
  Random rnd = new Random();
  while (lo < hi) {
    int p = partition(a, lo, hi, lo + rnd.nextInt(hi - lo + 1));
    if (p == target) return a[p];
    else if (p < target) lo = p + 1;
    else hi = p - 1;
  }
  return a[lo];
}

int partition(int[] a, int lo, int hi, int pivotIdx) {
  int pivot = a[pivotIdx];
  swap(a, pivotIdx, hi);                // stash pivot at end
  int store = lo;
  for (int i = lo; i < hi; i++)
    if (a[i] < pivot) swap(a, store++, i);
  swap(a, store, hi);                   // pivot to final place
  return store;
}

void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }`

const quickselectInvariant = {
  statement: `At the start of each outer-loop iteration, the search interval [lo, hi] contains the target rank; 0 ≤ lo ≤ target ≤ hi ≤ n-1. After a partition at index p, exactly one side still contains target, and that side becomes the new [lo, hi].`,
  initialization: `Before the loop: lo = 0, hi = n-1. The full array is the search interval, which trivially contains any valid target.`,
  maintenance: `Each iteration picks a random pivot in [lo, hi], partitions the subarray, and gets p = pivot's final sorted position. If p == target, return. If p < target, lo = p+1 (left side cannot contain target). If p > target, hi = p-1 (right side cannot contain target). The new [lo, hi] still contains target.`,
  termination: `The interval shrinks by at least 1 per iteration (the pivot itself is removed from consideration). Expected shrink is ~n/2 per step for a random pivot. Loop ends when lo == hi (interval of size 1) or when p == target (early return).`
}

const quickselectComplexity = {
  time: 'O(n) expected, O(n²) worst',
  space: 'O(1)'
}

const quickselectSpecializations = [
  { slug: 'kth-smallest-lomuto-partition-bare-mechanic-medium', title: 'kth-smallest-lomuto' },
  { slug: 'median-via-quickselect-two-calls-for-even-n-medium', title: 'median-via-quickselect' },
  { slug: 'top-k-via-quickselect-vs-heap-of-k-medium', title: 'top-k-quickselect' },
  { slug: 'hoare-vs-lomuto-pivot-invariants-compared-medium', title: 'hoare-vs-lomuto' }
]

const amortizedWorkedExample = `n = 16, expected (random pivot splits ~half):

  step 1: partition 16 elements  → 16 ops, keep ~8
  step 2: partition  8 elements  →  8 ops, keep ~4
  step 3: partition  4 elements  →  4 ops, keep ~2
  step 4: partition  2 elements  →  2 ops, keep ~1
  step 5: return

  Total: 16 + 8 + 4 + 2 = 30 ≈ 2·16 = O(n).

Worst case (pivot always smallest or largest):
  step 1: 16 ops, keep 15
  step 2: 15 ops, keep 14
  ...
  Total: 16+15+...+1 = n(n+1)/2 = O(n²). This is why we RANDOMIZE the pivot.`

const bareMechCode = `int[] a = {7, 1, 5, 3, 9, 2};     // find the 3rd smallest (target index 2)
int lo = 0, hi = 5;
int pivot = a[hi];                 // Lomuto: pivot = last element = 2
int store = lo;                    // index where next "< pivot" lands

for (int i = lo; i < hi; i++) {
  if (a[i] < pivot) {
    swap(a, store, i);
    store++;
  }
}
swap(a, store, hi);                // pivot to its final place: store
// a is now [1, 7, 5, 3, 9, 2] with pivot 2 at index store=1
// pivot's final sorted rank p = 1; target = 2, so p < target → recurse right`

const bareMechInvariant = {
  statement: `After the scan, every element in [lo, store) is strictly less than pivot, and every element in [store, i) is ≥ pivot. The final swap places pivot at index store — its correct sorted rank.`,
  initialization: `store = lo. [lo, store) and [store, lo) are both empty. Invariant vacuously holds.`,
  maintenance: `For each i in [lo, hi): if a[i] < pivot, swap into store and increment store; else leave in place. After the step, the partition invariant still holds.`,
  termination: `When i reaches hi, [lo, store) < pivot and [store, hi) ≥ pivot. Final swap moves pivot to store; now a[store] = pivot and is at its final sorted index.`
}

const bareMechComplexity = { time: 'O(n) per partition', space: 'O(1)' }

const subv1Code = `int findKthSmallest(int[] a, int k) {
  int target = k - 1;
  int lo = 0, hi = a.length - 1;
  Random rnd = new Random();
  while (lo < hi) {
    int p = partition(a, lo, hi, lo + rnd.nextInt(hi - lo + 1));
    if (p == target) return a[p];
    else if (p < target) lo = p + 1;
    else hi = p - 1;
  }
  return a[lo];
}

int partition(int[] a, int lo, int hi, int pivotIdx) {
  int pivot = a[pivotIdx];
  swap(a, pivotIdx, hi);
  int store = lo;
  for (int i = lo; i < hi; i++)
    if (a[i] < pivot) swap(a, store++, i);
  swap(a, store, hi);
  return store;
}`

const subv1Invariant = {
  statement: `[lo, hi] always contains the target rank. The pivot's final sorted position p splits the array into "all < pivot | pivot | all ≥ pivot"; the half not containing target is discarded.`,
  initialization: `lo = 0, hi = n-1, target = k-1 (for kth smallest) or n-k (for kth largest). Target is trivially inside [0, n-1].`,
  maintenance: `Each iteration partitions [lo, hi] and gets p. If p == target → done. If p < target → lo = p+1 (left half can't contain target). If p > target → hi = p-1.`,
  termination: `Loop ends when lo == hi (interval collapses to one element containing target) or when p == target.`
}

const subv2Code = `double findMedian(int[] a) {
  int n = a.length;
  if (n % 2 == 1) {
    return quickselect(a, n / 2);         // odd: single middle element
  }
  // even: average of two middle ranks
  int lo = quickselect(a, n / 2 - 1);
  int hi = quickselect(a, n / 2);         // array may be re-partitioned; this is correct
  return (lo + hi) / 2.0;
}

int quickselect(int[] a, int target) {
  int lo = 0, hi = a.length - 1;
  Random rnd = new Random();
  while (lo < hi) {
    int p = partition(a, lo, hi, lo + rnd.nextInt(hi - lo + 1));
    if (p == target) return a[p];
    else if (p < target) lo = p + 1;
    else hi = p - 1;
  }
  return a[lo];
}`

const subv2Invariant = {
  statement: `For odd n, the median is the element at rank ⌊n/2⌋. For even n, the median is the average of ranks n/2-1 and n/2. Two separate quickselect calls locate these two ranks in O(n) + O(n) = O(n) expected total.`,
  initialization: `n is given; parity determines whether one or two quickselect calls are needed.`,
  maintenance: `Each quickselect call runs the standard loop. The second call may re-partition the array (quickselect mutates); that's fine because we only need the value at the target index.`,
  termination: `Both calls terminate when their respective target indices are reached. Final result is the average (or single value).`
}

const subv3Code = `int[][] kClosest(int[][] points, int k) {
  // partition points by squared distance; after one quickselect, the first k slots
  // hold the k closest in any order (not necessarily sorted)
  int lo = 0, hi = points.length - 1;
  int target = k - 1;
  Random rnd = new Random();
  while (lo < hi) {
    int p = partition(points, lo, hi, lo + rnd.nextInt(hi - lo + 1));
    if (p == target) break;
    else if (p < target) lo = p + 1;
    else hi = p - 1;
  }
  return Arrays.copyOfRange(points, 0, k);
}

int partition(int[][] a, int lo, int hi, int pivotIdx) {
  int pivot = dist(a[pivotIdx]);
  swap(a, pivotIdx, hi);
  int store = lo;
  for (int i = lo; i < hi; i++)
    if (dist(a[i]) < pivot) swap(a, store++, i);
  swap(a, store, hi);
  return store;
}

int dist(int[] p) { return p[0] * p[0] + p[1] * p[1]; }`

const subv3Invariant = {
  statement: `After one quickselect to rank k-1, every element at index < k has distance ≤ a[k-1], and every element at index ≥ k has distance ≥ a[k-1]. The prefix [0, k) is the top-K (unsorted).`,
  initialization: `Target = k - 1. The partition routine compares by distance, not by raw value.`,
  maintenance: `Standard quickselect loop; the comparator is "squared distance to origin" instead of value.`,
  termination: `Loop ends at p == target. Return the first k slots.`
}

const subv4HoareCode = `int hoarePartition(int[] a, int lo, int hi) {
  int pivot = a[lo + (hi - lo) / 2];
  int i = lo - 1, j = hi + 1;
  while (true) {
    do { i++; } while (a[i] < pivot);
    do { j--; } while (a[j] > pivot);
    if (i >= j) return j;              // Hoare returns a position where [lo, j] ≤ pivot and [j+1, hi] ≥ pivot
    swap(a, i, j);
  }
}`

const subv4LomutoCode = `int lomutoPartition(int[] a, int lo, int hi, int pivotIdx) {
  int pivot = a[pivotIdx];
  swap(a, pivotIdx, hi);
  int store = lo;
  for (int i = lo; i < hi; i++)
    if (a[i] < pivot) swap(a, store++, i);
  swap(a, store, hi);
  return store;                        // Lomuto returns pivot's FINAL sorted index
}`

const subv4Invariant = {
  statement: `Hoare: after return, [lo, j] has values ≤ pivot and [j+1, hi] has values ≥ pivot — the pivot is NOT guaranteed to be at index j. Lomuto: after return, a[store] = pivot and is at its final sorted rank.`,
  initialization: `Both start by choosing a pivot. Hoare uses i=lo-1, j=hi+1 and advances with do-while. Lomuto moves the pivot to hi, uses store = lo.`,
  maintenance: `Hoare advances i until a[i] ≥ pivot, j until a[j] ≤ pivot, then swaps — three times fewer swaps on average than Lomuto. Lomuto advances i through [lo, hi); every time a[i] < pivot it swaps into store and increments store.`,
  termination: `Hoare: i ≥ j → return j. Lomuto: i = hi → final swap puts pivot at store, return store.`
}

const inTheWildCode = `# NumPy np.partition — same quickselect pattern, written in C.
# From numpy/core/src/npysort/quickselect.cpp (abridged):

def partition_kth(a, k):
    """Rearrange a in-place so a[k] holds the k-th order statistic."""
    lo, hi = 0, len(a) - 1
    while lo < hi:
        pivot = median_of_three(a, lo, (lo + hi) >> 1, hi)
        p = three_way_partition(a, lo, hi, pivot)
        if p == k:
            return
        elif p < k:
            lo = p + 1
        else:
            hi = p - 1

# np.partition(a, k) is EXACTLY this, plus:
#   - three-way partition (handles duplicate-heavy inputs)
#   - median-of-three pivot (avoids adversarial O(n²))
#   - introselect fallback to heap-select when recursion depth > 2*log2(n)`

const trap1Bug = `Deterministic pivots on adversarial input:

  a = [1, 2, 3, 4, 5, 6, 7, 8]  (already sorted)
  Pick a[hi] as pivot EVERY iteration.
  Round 1: pivot = 8 → partition → p = 7. Keep [0, 6].
  Round 2: pivot = 7 → p = 6. Keep [0, 5].
  Round 3: pivot = 6 → p = 5. Keep [0, 4].
  ...
  Total: O(n²) time, not O(n). On n = 10^5 this is 10^10 ops — minutes vs microseconds.`

const trap1Fix = `Pivot = \`lo + rnd.nextInt(hi - lo + 1)\`. Randomization makes the adversarial-input case probabilistically rare — expected O(n) holds. For deterministic worst-case guarantee, use median-of-medians (BFPRT 1973), but the constant is 10× worse, so random pivot wins in practice. Say "expected O(n) with randomized pivot" out loud in interviews.`

const trap2Bug = `Rank-conversion bugs between "k-th largest" and "k-th smallest":

  Input: a = [3, 2, 1, 5, 6, 4], k = 2
  "2nd LARGEST" means target index n - k = 6 - 2 = 4 (ascending)
  "2nd SMALLEST" means target index k - 1 = 1 (ascending)

  Writing target = k - 1 when the problem asked for k-th largest returns 2 (the 2nd smallest), not 5.
  The code is correct; the index conversion is wrong, and the test case passes if sorted(a) matches at that index.`

const trap2Fix = `State the rank conversion before writing the loop:
  • k-th SMALLEST → target = k - 1
  • k-th LARGEST  → target = n - k
Both are 0-based. For an input of length n, the extremes map to:
  • 1st smallest = index 0 = a[0] after sort
  • 1st largest  = index n-1 = a[n-1] after sort
Writing it as a comment above the loop head catches this immediately.`

const trap3Bug = `Partition comparator \`a[i] <= pivot\` (should be \`<\`) on duplicate-heavy inputs:

  a = [5, 5, 5, 5, 5], target = 2
  With <= pivot: every element gets swapped forward; store advances for all n.
  Partition returns store = n, which is out of bounds / wrong rank.
  More subtly: with <= and random pivot = a[k], the partition "accepts" the pivot itself
  as "< pivot," which is nonsensical.`

const trap3Fix = `Use strict \`a[i] < pivot\` in the scan. This correctly partitions:
  [< pivot] [pivot and duplicates] [> pivot]
Pivot and its duplicates end up on the right side of the "< pivot" region.
For truly duplicate-heavy inputs, upgrade to three-way partition (<, ==, >);
if target falls inside the equal band, return immediately in O(n).`

const advanced1 = `What if the input is adversarial and quickselect degenerates to O(n²)?

Use median-of-medians (BFPRT 1973) for deterministic O(n). The pivot is chosen by:
  1. Split the array into groups of 5.
  2. Compute the median of each group (O(1) per group).
  3. Recursively quickselect the median of medians.
This pivot is guaranteed to reject at least 30% of elements per step, giving T(n) = T(n/5) + T(7n/10) + O(n) → O(n).
But: the constant factor is ~10× worse than randomized quickselect, so it's rarely used in practice. C++ std::nth_element and NumPy np.partition both use RANDOMIZED quickselect with a worst-case heap-select fallback (introselect), not median-of-medians.`

const advanced2 = `What if you need the top-K and the stream is unbounded?

Quickselect requires random access to the whole array — won't work on a stream. Use a min-heap of size k instead:
  for each incoming value v:
    if heap.size() < k: heap.offer(v);
    else if (v > heap.peek()): heap.poll(); heap.offer(v);
Time: O(n log k), space: O(k). Worse asymptotically than quickselect's O(n), but STREAMING-COMPATIBLE and bounded memory. The two patterns divide cleanly: quickselect for in-memory one-shot, heap for streams or repeated queries.`

const advanced3 = `What if the array must remain in original order?

Quickselect mutates in-place. Options:
  1. Copy the array first (O(n) extra memory, then standard quickselect).
  2. Build an index array [0, 1, 2, ..., n-1] and quickselect over the indices
     (comparing a[indices[i]] instead of indices[i]). The original array is untouched.
Option 2 is what databases do for "TOP N" queries where the underlying rows must stay in insertion order.`

const advanced4 = `What if you need the top-K VALUES SORTED (not just in any order)?

Quickselect alone gives you the k-th rank; the first k slots are the top-K but UNSORTED. Two choices:
  1. Sort just those k slots: O(k log k) extra, total O(n + k log k).
  2. Build a heap-of-K from the start: O(n log k) throughout.
If k << n, option 1 wins; if k ~ n, they're equivalent. The classic trap: assuming
quickselect "gives you top-K sorted" — it doesn't. Always ask the interviewer whether
output must be sorted.`

const advanced5 = `Breaking point — quickselect has no advantage when:
  • The data is a stream: use heap-of-K.
  • The data must stay in order: use heap or index-array trick.
  • You need all k values sorted (not just the k-th): heap is simpler and comparable.
  • You need DETERMINISTIC worst-case O(n): use median-of-medians (constants are bad).
  • The input is in a BST: in-order traversal is O(h + k), typically much faster.
Diagnostic: can you mutate the array and do one in-memory pass? If no — different pattern.`

const advancedCrossProblems = [
  {
    title: 'Wiggle Sort II (quickselect + Dutch flag + virtual index)',
    hint: 'Quickselect the median; then use three-way partition with virtual index mapping i -> (2i+1) % (n|1) to interleave larger/smaller halves in O(n) time, O(1) extra space.',
    reveal: 'Three composed patterns: quickselect (median), Dutch flag (three-way partition), index arithmetic. The virtual index trick makes the output nums[0] < nums[1] > nums[2] without an auxiliary array.'
  },
  {
    title: 'Kth Smallest Element in a BST (NOT quickselect)',
    hint: 'A BST already encodes rank in its in-order traversal. Iterative in-order with early termination gives O(h + k) time, O(h) stack — completely different mechanism.',
    reveal: 'Recognition drill: when the input is a BST, quickselect\'s partition idea doesn\'t apply. The TREE is already partitioned by sort order; walk it in-order and stop at the k-th node. If the BST stores subtree sizes at each node, you can even get O(h) worst-case.'
  },
  {
    title: 'Median Filter in image processing',
    hint: 'For each pixel, compute the median of a 3x3 neighborhood (9 pixels). Naive: sort 9 pixels → O(n·k·log k) for an n-pixel image with k-sized window. Quickselect: O(n·k) expected, 2-3× faster in practice.',
    reveal: 'Composed with sliding window: as the 3x3 window slides, you can update the partial sort incrementally. Production median-filter implementations (OpenCV, Pillow) use a histogram-based O(n) algorithm (Huang 1979), which is tangentially related but a different pattern.'
  }
]

const quizQuestions = [
  {
    q: 'Expected time complexity of Quickselect for the k-th element?',
    choices: [
      { text: 'O(n)', correct: true, explanation: 'Each partition eliminates a constant fraction of candidates on average, giving the geometric sum n + n/2 + n/4 + ... = 2n.' },
      { text: 'O(n log n)', correct: false, explanation: 'That is full quicksort.' },
      { text: 'O(log n)', correct: false },
      { text: 'O(k)', correct: false }
    ]
  },
  {
    q: 'Worst-case complexity of Quickselect without randomization?',
    choices: [
      { text: 'O(n²)', correct: true, explanation: 'On adversarial inputs (e.g., sorted input with last-element pivot), each partition shrinks by 1 → quadratic.' },
      { text: 'O(n log n)', correct: false },
      { text: 'O(n)', correct: false, explanation: 'Only with median-of-medians pivot (BFPRT 1973).' },
      { text: 'O(log n)', correct: false }
    ]
  },
  {
    q: 'For k-th LARGEST via quickselect, how do you compute the target index?',
    choices: [
      { text: 'target = n - k (in ascending-sorted order)', correct: true, explanation: 'k-th largest is the element at position n-k when sorted ascending.' },
      { text: 'target = k', correct: false, explanation: 'That is the (k+1)-th smallest.' },
      { text: 'target = k - 1', correct: false, explanation: 'That is k-th smallest.' },
      { text: 'target = random', correct: false }
    ]
  },
  {
    q: 'What is the Hoare vs Lomuto key difference?',
    choices: [
      { text: 'Hoare uses two pointers from both ends; Lomuto uses one pointer and a store index', correct: true, explanation: 'Hoare does ~3× fewer swaps on average and handles duplicates better; Lomuto is simpler to explain and more commonly taught.' },
      { text: 'They have different asymptotic complexity', correct: false, explanation: 'Both are O(n) per partition; the difference is in constant factor and duplicate handling.' },
      { text: 'Hoare is deterministic O(n) worst case', correct: false },
      { text: 'Lomuto cannot handle duplicates', correct: false, explanation: 'Lomuto CAN handle duplicates with strict `< pivot`; it is just less efficient.' }
    ]
  },
  {
    q: 'What is the "Wiggle Sort II" O(n) trick using quickselect?',
    choices: [
      { text: 'Quickselect the median, then three-way partition with virtual index mapping (2i+1) % (n|1)', correct: true, explanation: 'Virtual indexing interleaves the ranked halves to produce the wiggle pattern in-place.' },
      { text: 'Just sort', correct: false, explanation: 'That is O(n log n), not O(n).' },
      { text: 'Random shuffle until wiggle', correct: false },
      { text: 'BFS', correct: false }
    ]
  }
]
</script>

<PatternVideo pattern-name="Quickselect" duration="8–12 min" />

<PatternProgress pattern-id="quickselect" problems="kth-largest, k-closest-points-to-origin, top-k-frequent-elements, wiggle-sort-ii, kth-smallest-in-sorted-matrix" />



## Why Quickselect exists — the story

You're an engineer at Netflix. The Recommendation Systems team asks: *"For each user, return the top 10 movies from our catalog of 100,000 titles."*

The obvious approach: sort all 100,000 movies by predicted rating, return the first 10. `O(n log n)` — for 200 million users, ~`2·10¹²` sort operations. **Manageable, but wasteful.** You spent effort ranking movie 50,000 vs movie 60,000 when you only care about the top 10.

You could argue: *"sort is O(n log n), that's fine."* And it is — for one query. But Netflix does this **per user, per day**, for 200 million users. And the *interesting* question isn't sort; it's **"why did I spend cycles ordering movies I'll never return?"** After finding the top 10, you don't care whether movie 50,000 or 60,000 is better. That's pure waste.

The pattern is **Quickselect**: return the k-th smallest (or largest) element in **O(n) expected time** without fully sorting. Pick a pivot, partition the array around it. The pivot lands in its final sorted position `p`. If `p == k`, you're done. If `p < k`, the answer is in the right half — throw away the left half and recurse. If `p > k`, symmetric. **You never recurse into both halves.** For finding top-10-of-100,000, Quickselect averages ~200,000 ops vs. sort's `100,000 · log₂(100,000) = 1,700,000` — an **8.5× speedup** for the same answer. Scaled to Netflix: from 2·10¹² to 2·10¹¹ ops per day. Ships hit datacenter power budgets.

```svg
<svg role="img" width="720" height="240" viewBox="0 0 720 240" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif" aria-label="one partition step decides which side can contain rank k">
  <defs>
    <marker id="qs-ar-blue" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/></marker>
    <marker id="qs-ar-grn" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-success)"/></marker>
    <marker id="qs-ar-red" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-danger)"/></marker>
  </defs>
  <rect x="0" y="0" width="720" height="240" fill="var(--dsa-bg)"/>
  <text x="360" y="24" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-ink)">one partition step decides which side can contain rank k</text>
  <text x="48" y="70" text-anchor="end" font-size="12" font-weight="700" fill="var(--dsa-neutral)">before</text>
  <g>
    <rect x="70" y="48" width="46" height="38" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><rect x="122" y="48" width="46" height="38" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/>
    <rect x="174" y="48" width="46" height="38" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.7"/><rect x="226" y="48" width="46" height="38" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/>
    <rect x="278" y="48" width="46" height="38" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><rect x="330" y="48" width="46" height="38" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/>
  </g>
  <g font-size="17" font-weight="700" fill="var(--dsa-ink)" text-anchor="middle">
    <text x="93" y="73">7</text><text x="145" y="73">1</text><text x="197" y="73">5</text><text x="249" y="73">3</text><text x="301" y="73">9</text><text x="353" y="73">2</text>
  </g>
  <text x="197" y="100" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-primary)">pivot = 5</text>
  <text x="48" y="170" text-anchor="end" font-size="12" font-weight="700" fill="var(--dsa-neutral)">after</text>
  <g>
    <rect x="70" y="148" width="46" height="38" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><rect x="122" y="148" width="46" height="38" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/>
    <rect x="174" y="148" width="46" height="38" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><rect x="226" y="148" width="46" height="38" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.7"/>
    <rect x="278" y="148" width="46" height="38" rx="7" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)"/><rect x="330" y="148" width="46" height="38" rx="7" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)"/>
  </g>
  <g font-size="17" font-weight="700" fill="var(--dsa-ink)" text-anchor="middle">
    <text x="93" y="173">1</text><text x="145" y="173">3</text><text x="197" y="173">2</text><text x="249" y="173">5</text><text x="301" y="173">9</text><text x="353" y="173">7</text>
  </g>
  <text x="145" y="204" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-success)">&lt; pivot</text>
  <text x="249" y="204" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-primary)">final rank p = 3</text>
  <text x="327" y="204" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-danger)">≥ pivot</text>
  <rect x="432" y="48" width="248" height="78" rx="9" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/>
  <text x="556" y="72" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">compare p with target rank k</text>
  <text x="556" y="94" text-anchor="middle" font-size="12" fill="var(--dsa-neutral)">if p == k, done</text>
  <text x="556" y="114" text-anchor="middle" font-size="12" fill="var(--dsa-neutral)">else recurse only into k's side</text>
</svg>
```
<div class="readfig"><b>How to read it:</b> Partition moves values smaller than the pivot to the green left side and values greater than or equal to it to the red right side. The pivot <b>5</b> lands at its final sorted rank <b>p</b>. Quickselect compares <b>p</b> with the target rank <b>k</b> and discards the side that cannot contain the answer.</div>

> [key] **Key Insight** — Quickselect is expected O(n) *because* it discards half the array on each step. Total work: `n + n/2 + n/4 + ... = 2n = O(n)`. Say "expected linear" out loud in interviews — the word "expected" acknowledges the worst-case O(n²).

## The bare mechanic — simplest working example

Before randomized pivots, before median-of-medians, before all four sub-variations, here's the Lomuto partition on a 6-element array in one pass. **Target: find the 3rd smallest in `[7, 1, 5, 3, 9, 2]`.**

Target index = `k - 1 = 2` (0-based). Pick pivot = `a[hi] = 2` (last element). Walk `i` from `0` to `hi-1`; whenever `a[i] < pivot`, swap into `store` and increment `store`:

| step | i | a[i] | pivot | action | store | array |
|---|---|---|---|---|---|---|
| 0 | — | — | 2 | pivot = a[5] = 2; swap a[5]↔a[5] (no-op) | 0 | `[7,1,5,3,9,2]` |
| 1 | 0 | 7 | 2 | 7 ≥ 2 → skip | 0 | `[7,1,5,3,9,2]` |
| 2 | 1 | 1 | 2 | 1 < 2 → swap a[0]↔a[1], store++ | 1 | `[1,7,5,3,9,2]` |
| 3 | 2 | 5 | 2 | 5 ≥ 2 → skip | 1 | `[1,7,5,3,9,2]` |
| 4 | 3 | 3 | 2 | 3 ≥ 2 → skip | 1 | `[1,7,5,3,9,2]` |
| 5 | 4 | 9 | 2 | 9 ≥ 2 → skip | 1 | `[1,7,5,3,9,2]` |
| end | — | — | 2 | swap a[store]↔a[hi] → pivot to final place | — | `[1,2,5,3,9,7]` |

Pivot `2` is now at index `store = 1`, which is its correct sorted rank. Target `k-1 = 2` is to the right of `1`, so **recurse into `[2, 5]`** — the sub-array `[5, 3, 9, 7]` — and find rank `2 - 1 - 1 = 0` of that slice (the smallest, which is `3`).

Four more operations and quickselect returns `3`. **Total work:** 6 + 4 ≈ 10 ops to find the 3rd smallest — much less than fully sorting (18 ops minimum for quicksort on 6 elements).

<PatternTemplateCard
  slug="quickselect-bare-mechanic"
  :code="bareMechCode"
  language="java"
  :invariant="bareMechInvariant"
  :complexity="bareMechComplexity"
  title="Bare mechanic — one Lomuto partition pass"
/>

> [key] **The single move.** Partition rearranges the array so a[store] = pivot sits at its final sorted rank, and everything left of store is strictly smaller. The pivot's rank is now KNOWN; recurse only into the side containing the target index. Everything in this chapter — median, top-k, Hoare partition — is this move plus a different "what to do with the two halves."

## When to use it — one-shot rank selection

### Recognize by
- "find the kth smallest" or "find the kth largest" in an unsorted array
- "find the median" when you do not need the full sorted array
- "return the kth order statistic" or "element at rank r"
- "top k" when returning the k items in any order is okay and mutating/partitioning is allowed
- constraints where O(n log n) sort is acceptable but the interviewer asks for better average time
- array is available in memory, so random access and in-place swaps are allowed

### When NOT to use it
You need k-th in a **stream** (no random access) — use a heap. You need the k boundary items in order — use a heap or partial sort. Adversarial inputs with the same pivot every time degrade to O(n²) — always pick a **random** pivot or use median-of-medians.

Do not reach for Quickselect when the input must remain in original order and mutation is forbidden unless you are willing to copy the array. Do not use it for repeated queries on the same data; sorting once or building an order-statistics structure may win. And if the problem requires stable ordering, tie-aware output, or all top-k values sorted, Quickselect alone only gets you the boundary; you still need post-processing.

<QuickselectAnim />

## THE template

Every quickselect problem is a specialization of the two-step loop: pick a pivot, partition, compare `p` to the target, discard the half that cannot contain `target`. The template below is Lomuto partition inside a while loop with randomized pivot — the standard interview form.

<PatternTemplateCard
  slug="quickselect-template"
  :code="quickselectTemplate"
  language="java"
  :invariant="quickselectInvariant"
  :complexity="quickselectComplexity"
  :specializations="quickselectSpecializations"
  title="THE quickselect template — randomized Lomuto"
/>

### Why it's O(n) expected — the amortized argument

The outer `while` seems to loop up to `n` times, and each partition is `O(n)` — a naive reader would guess `O(n²)` worst case. The crucial observation is that each iteration **shrinks the active range by roughly half** on average, giving a geometric sum.

<AmortizedPanel
  method="aggregate"
  bound="O(n) expected"
  statement="Each partition scans the current range in O(range), and the range halves (in expectation) per iteration. Total work ≈ n + n/2 + n/4 + ... = 2n = O(n)."
  :workedExample="amortizedWorkedExample"
>

Partition at step i costs O(r_i) where r_i is the current range size. With a random pivot, E[r_{i+1}] = r_i / 2 (because a uniformly random pivot splits a range of size r into expected halves of r/2 each; we keep only one).

Total expected work:

E[T(n)] = n + n/2 + n/4 + ... = 2n = **O(n)**

Worst case (pivot always extreme): r shrinks by 1 per step → T(n) = n + (n-1) + ... + 1 = n(n+1)/2 = O(n²). Randomization makes this adversarial case probabilistically rare — the probability of hitting worst-case over 10^5 iterations is < 10^-10000.

This same aggregate argument powers [§22 two-pointers](/patterns/two-pointers) (sum of advances ≤ 2n) and [§21 sliding-window](/patterns/sliding-window) (each index pushed/popped once). The pattern is "monotone counter bounds total work" — the signature of amortized O(1) per step.

</AmortizedPanel>

> [key] **Where the "expected" matters.** In a system where an adversary can craft inputs (web server receiving user queries), always use randomized or median-of-three pivot. In a system with trusted input (sorting a database page), deterministic first-element pivot is fine and avoids the RNG cost. Say which assumption you're making out loud.

## History — Hoare 1961, Blum-Floyd-Pratt-Rivest-Tarjan 1973

Quickselect was invented by **Sir Charles Antony Richard Hoare** in **1961** — the same year and the same paper (*"Algorithm 65: FIND"*, Communications of the ACM 4(7):321-322) that introduced **quicksort**. Hoare was 27 years old, working on a Russian-English translation dictionary at Elliott Brothers Ltd; sorting Russian words prompted him to invent the partition technique. He got the Turing Award in 1980 for both algorithms.

Hoare's quickselect had a randomized average of O(n) but worst-case O(n²) on adversarial input. This worst case was unacceptable in system code (adversaries could craft slow requests to DoS a server). The question of *"can we achieve deterministic linear-time selection?"* stayed open for 12 years.

**Blum, Floyd, Pratt, Rivest, and Tarjan** answered in **1973** with the **median-of-medians algorithm** — a deterministic O(n) selection algorithm. Their trick: recursively find a *"good enough"* pivot by taking the median of medians of groups of 5. This guarantees the pivot rejects at least 30% of the elements per step, giving O(n) with a large constant. The paper *"Time bounds for selection"* is one of the most cited results in theoretical computer science.

**Real-world adoption:**

- **C++ `std::nth_element`** — introselect (Musser 1997), a hybrid of Hoare's quickselect and heapsort-fallback for worst-case protection.
- **NumPy's `np.partition`** — uses the same introselect hybrid.
- **Netflix's recommendation top-K** — the scene we opened with; production code uses quickselect for O(n) expected instead of O(n log n) sort.
- **Databases** — every "TOP N" query optimizer uses partial partitioning under the hood, not full sort.
- **Median filters** in image processing (used for denoising every phone photo) — quickselect over pixel windows.
- **Java's Dual-Pivot Quicksort** (Yaroslavskiy 2009), the algorithm behind `Arrays.sort` on primitives, uses two pivots per partition; quickselect variants adapt the same idea.

Bloch's 2006 blog post on the Binary Search bug also revealed that Java's original `Arrays.sort` had subtle quickselect-related bugs — even the JDK's sort spec-authors weren't immune. That story reinforces the Chapter 27 point: partition-based algorithms *look* simple but are among the most bug-prone code in a standard library.

## Sub-variations of the template

Each sub-variation below swaps **what gets compared** and/or **how the partition is done** but keeps the "pivot + partition + narrow" skeleton. Reading these in order (bare mechanic → median → top-K → Hoare vs Lomuto) traces the capability growth from one rank to many ranks to pivot-scheme-level choice.

<PatternSubVariationNav pattern="quickselect" />

### Kth smallest (Lomuto partition — bare mechanic) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/)*

<ProgressCheck id="quickselect-kth-largest-element" />

The canonical quickselect problem: find the k-th order statistic. The code is simplest when "k-th smallest" is primary; "k-th largest" is just `target = n - k`.

<InvariantProof :statement="subv1Invariant.statement" :initialization="subv1Invariant.initialization" :maintenance="subv1Invariant.maintenance" :termination="subv1Invariant.termination" />

> [key] **Blind-solve prompt** — on `nums=[3,2,1,5,6,4], k=2` (2nd largest = 5). Convert to target = `n - k = 4`, then run the while loop. Try it, then reveal.

<TemplateReveal :canonical="subv1Code" language="java" slug="quickselect-kth" />

#### Problem
Find the **kth largest** element in an unsorted array (a one-shot query) — faster than fully sorting.

**Constraints:** `1 ≤ k ≤ n ≤ 10⁵`; expected O(n) average via partitioning.

**Example 1:** `[3,2,1,5,6,4], k = 2` → `5`.

<ExamplePreview compact :input="['3', '2', '1', '5', '6', '4', '|', '2']" :output="['5']" />

**Example 2:** `[3,2,3,1,2,4,5,5,6], k = 4` → `4`.

<ExamplePreview compact :input="['3', '2', '3', '1', '2', '4', '5', '5', '6', '|', '4']" :output="['4']" />

#### Solution — brute force
The baseline is to sort the array and index into the sorted result.

```text
sort nums ascending
return nums[nums.length - k]
```

That is O(n log n) time and O(1) or O(n) extra space depending on the language and whether you can mutate the input. It is also the best first sentence in an interview because it proves you understand that "kth largest" means a rank, not necessarily a distinct value. Quickselect improves the average runtime by avoiding the side of the partition that cannot contain that rank.

A heap baseline is also possible: keep a min-heap of size k and return its root after scanning all values. That costs O(n log k) and works for streams. Quickselect is usually preferred for one in-memory one-shot query because expected O(n) is better.

**Baseline complexity:** O(n log n) time; O(1) or O(n) extra space depending on sorting/copying.

#### Solution — optimized

The optimized solution partitions around a (randomized) pivot; recurse only into the side that contains rank k.

```java
int findKthLargest(int[] a, int k) {
  int target = a.length - k;                 // kth largest = index n-k ascending
  int lo = 0, hi = a.length - 1;
  Random rnd = new Random();
  while (lo < hi) {
    int p = partition(a, lo, hi, lo + rnd.nextInt(hi - lo + 1));
    if (p == target) break;
    else if (p < target) lo = p + 1;
    else hi = p - 1;
  }
  return a[target];
}
int partition(int[] a, int lo, int hi, int pivotIdx) {
  int pivot = a[pivotIdx];
  swap(a, pivotIdx, hi);                      // stash pivot at end
  int store = lo;
  for (int i = lo; i < hi; i++)
    if (a[i] < pivot) swap(a, store++, i);
  swap(a, store, hi);                         // pivot to final place
  return store;
}
void swap(int[] a, int i, int j){ int t=a[i]; a[i]=a[j]; a[j]=t; }
```

<CodeTrace
  title="Quickselect Kth Largest — nums=[3,2,1,5,6,4], k=2 (target idx=4)"
  :values="[3,2,1,5,6,4]"
  :windowKeys="['lo','hi']"
  :cellWidth="42"
  :steps='[
    { pointers: { lo: 0, hi: 5, pivot: 4 }, vars: { array: "[3,2,1,4,6,5]" }, note: "pick pivot 6 → partition puts 6 at end. after: [3,2,1,5,4,6]" },
    { pointers: { lo: 0, hi: 4, pivot: 3 }, vars: { array: "[3,2,1,4,5]" }, note: "pivot 5 → partitions to [3,2,1,4] | 5. idx 4 == k → found 5", added: [4] }
  ]'
/>

#### Rank conversion: kth largest vs kth smallest

Most bugs here are off-by-one rank bugs. If the array were sorted ascending, the 1st smallest is index `0`, so kth smallest is `k - 1`. The 1st largest is the final index `n - 1`, so kth largest is `n - k`. For `[1,2,3,4,5,6]`, the 2nd largest is `5`, which sits at index `4`; `n-k = 6-2 = 4`. Say this conversion out loud before writing the loop.

Duplicates do not change the formula. In `[3,2,3,1,2,4,5,5,6]`, sorted ascending is `[1,2,2,3,3,4,5,5,6]`. The 4th largest is index `9-4=5`, value `4`. You are selecting by position after sorting, not by distinct value.

#### Mutability and output shape

Quickselect **mutates** the array. In an interview, mention this trade-off if the prompt says "do not modify the input" — the fix is to copy the array first (O(n) extra space). Also distinguish between returning the **kth value** and the **top k values**: the code above returns one integer. If the prompt asks for the k largest in any order, after `partition` places the k-th at index `n-k`, the suffix `[n-k, n)` contains the k largest unsorted. For "k largest sorted," sort just that suffix or use a heap.

> [note] **Interview script** — First, I'd translate kth largest into an ascending target index: `n-k`, so duplicates are handled naturally by rank. The brute force is sorting in O(n log n), and a heap gives O(n log k), especially for streams. Since this is a one-shot array query, I'll use Quickselect: partition around a randomized pivot and continue only on the side containing the target index. The expected time is O(n), worst-case O(n²) with unlucky pivots, and space is O(1) in-place.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **The one commitment**: after partition returns pivot index `p`, recurse into ONLY the side containing the target index. That's why quickselect is O(n) expected — the work halves each level (vs. quicksort's full-tree O(n log n)).
- **Target index conversion**: for "k-th largest in ascending-sorted order," target = `n - k`. For "k-th smallest," target = `k - 1`. Pick ONE convention and stick with it; mixing is the #1 bug.
- **Pivot MUST be randomized** (or median-of-three) — a last-element pivot on sorted input is O(n²). `Random.nextInt(hi - lo + 1) + lo` before swapping to the end is one line that gives O(n) expected regardless of input.
- **Comparator MUST be strict `<` not `<=`** in Lomuto. On `[5,5,5,5,5]` with `<=`, every element goes to the "less than" side and pivot ends at index 0 regardless — recursion never makes progress on duplicates.
- **O(n) expected, O(n²) worst case, O(1) space in-place** (ignoring recursion stack). Beats sort (O(n log n)) and heap-of-k (O(n log k)) when `k` is close to `n/2` and the array fits in memory.
- **Mutates input.** If the problem says "do not modify the input," copy first (O(n) extra space) and quickselect on the copy.
- **Siblings: Kth Largest Element in a Stream (heap, not quickselect — streams aren't quickselect-compatible), Wiggle Sort II (quickselect to find the median, then 3-way partition).**

</details>

### Median via quickselect (two calls for even n) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Find Median from Data Stream (array variant)](https://leetcode.com/problems/kth-largest-element-in-an-array/)*

The median of an unsorted array is the k-th rank at `k = n/2` (odd) or the average of ranks `n/2 - 1` and `n/2` (even). Each quickselect call is O(n) expected; two calls total O(n) — not O(n log n) like a sort.

<InvariantProof :statement="subv2Invariant.statement" :initialization="subv2Invariant.initialization" :maintenance="subv2Invariant.maintenance" :termination="subv2Invariant.termination" />

> [key] **Blind-solve prompt** — on `[7, 1, 5, 3, 9, 2]` (n=6, even). Target ranks: n/2-1=2 and n/2=3. First quickselect returns the 3rd smallest = 3; second returns the 4th smallest = 5. Median = (3+5)/2 = 4. Try it, then reveal.

<TemplateReveal :canonical="subv2Code" language="java" slug="quickselect-median" />

**Why two calls, not one?** For even n, you need two adjacent ranks. The second call runs after the array is already partially partitioned by the first, but since quickselect's output is just the value at target (and both target indices still fit in `[0, n-1]`), the second call is still O(n) expected. Total: O(n) + O(n) = O(n).

**Alternative — one quickselect, then scan.** After `quickselect(a, n/2)`, the n/2-th position holds the upper median; everything in `[0, n/2)` is ≤ it. Scan `[0, n/2)` once to find the max — that's the lower median. One quickselect + O(n) scan = O(n) + O(n/2) = O(n). This saves one quickselect call in half the cases.

**Production use: median filters in image processing.** For each pixel of an image, compute the median of its 3×3 neighborhood (9 pixels). Naive sort: O(k log k) per pixel = O(n·k·log k) total. Quickselect per pixel: O(n·k) total — 2-3× faster, used in every denoising pipeline in OpenCV and Pillow.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Odd `n`**: median = `quickselect(a, n/2)`. **Even `n`**: median = `(quickselect(a, n/2 - 1) + quickselect(a, n/2)) / 2.0`. Two calls for even case; still O(n) + O(n) = O(n) total.
- **Optimization: one call + scan**. After `quickselect(a, n/2)` on even n, everything in `[0, n/2)` is ≤ the upper median. Max of that prefix is the lower median — O(n/2) scan instead of a second quickselect call.
- **Watch the integer-overflow trap for even case**: `(a + b) / 2` can overflow if `a + b > Integer.MAX_VALUE`. Use `(a + b) / 2.0` to force double arithmetic, or `a / 2.0 + b / 2.0`.
- **The second quickselect runs on the ALREADY-PARTIALLY-PARTITIONED array** (from the first call). Still O(n) expected because quickselect's analysis doesn't assume starting-from-random order — it averages over pivot choices, not input permutations.
- **Streaming median is a different problem** — use two heaps (max-heap for lower half, min-heap for upper half), balance after each insert, median = top of max-heap or average of tops. Quickselect doesn't support streams.
- **Production use**: median filters in image processing (3×3 kernels, 9-element median per pixel, used in every denoising pipeline).
- **Siblings: Find Median from Data Stream (two heaps), Sliding Window Median (two heaps with lazy deletion or a multiset), Majority Element (Boyer-Moore voting, not median).**

</details>

### Top-K via quickselect vs heap-of-K <span class="diff diff-m">Medium</span>

*[↗ LeetCode: K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/)*

For "find the top-K elements in any order," you have a choice: quickselect (O(n) expected, mutates) or heap-of-K (O(n log k), streaming-compatible). The decision depends on constraints you should check first.

<InvariantProof :statement="subv3Invariant.statement" :initialization="subv3Invariant.initialization" :maintenance="subv3Invariant.maintenance" :termination="subv3Invariant.termination" />

> [key] **Blind-solve prompt** — on `points = [[1,3],[-2,2],[2,-2]], k = 2`. Partition by `x² + y²`; the first 2 slots should hold the closest 2 points. Try the quickselect approach, then reveal.

<TemplateReveal :canonical="subv3Code" language="java" slug="quickselect-top-k" />

#### Decision table — quickselect vs heap-of-K

| Dimension | Quickselect | Heap-of-K |
|---|---|---|
| **Time (expected)** | O(n) | O(n log k) |
| **Time (worst)** | O(n²) | O(n log k) |
| **Space** | O(1) (in-place) | O(k) |
| **Streaming** | NO (requires full array) | YES |
| **Mutates input** | YES | NO |
| **Repeated queries on same data** | re-run every time | heap can be amortized |
| **k << n** | fast (small constant) | fast (log k is small) |
| **k ~ n/2** | fast (O(n)) | slow (O(n log n) effectively) |
| **k = n** | O(n) but pointless | O(n log n) full sort |

**Rule of thumb:** quickselect for one-shot in-memory queries where mutation is OK; heap for streams, repeated queries, or when the input must stay in-order.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Quickselect for top-K**: after `partition(a, 0, n-1, target = n-k)`, the suffix `a[n-k, n)` contains the k largest in any order. Just return that slice (or those indices).
- **"Any order" is the critical qualifier.** If the problem wants the k largest **sorted**, you add O(k log k) sort after the quickselect — total O(n + k log k). Still beats heap-of-K's O(n log k) when k ≪ n.
- **Decision rule**: use quickselect for one-shot in-memory queries where mutation is OK; use heap-of-K for streams, repeated queries, or when the input must stay in order.
- **Streaming kills quickselect.** It needs random access to the full array; a true stream can't be partitioned. Heap-of-K is the only streaming option — it keeps a running min-heap of size k, popping when size exceeds k.
- **k close to n/2 is where quickselect dominates**: O(n) vs. heap's O(n log k) with k ≈ n/2 → O(n log n). Factor-of-log-n speedup matters at scale.
- **For `K Closest Points`**: partition by squared distance (never sqrt — monotonic for non-negative values, saves O(n) sqrt calls). Target = `k - 1` (closest k are the smallest k, so indices `[0, k)` after quickselect).
- **Siblings: K Closest Points to Origin (quickselect by distance²), Top K Frequent Elements (hash counts, then heap or quickselect), Kth Largest Element in a Stream (heap only — stream).**

</details>

### Hoare vs Lomuto pivot (invariants compared) <span class="diff diff-m">Medium</span>

The two canonical partition schemes have different invariants, different swap counts, and different behavior on duplicate-heavy inputs. Interviews rarely ask about this, but production code (std::nth_element, np.partition) uses Hoare because it's measurably faster.

<InvariantProof :statement="subv4Invariant.statement" :initialization="subv4Invariant.initialization" :maintenance="subv4Invariant.maintenance" :termination="subv4Invariant.termination" />

**Lomuto partition** (what we've been using throughout the chapter — simplest to explain):

```java
int lomutoPartition(int[] a, int lo, int hi, int pivotIdx) {
  int pivot = a[pivotIdx];
  swap(a, pivotIdx, hi);
  int store = lo;
  for (int i = lo; i < hi; i++)
    if (a[i] < pivot) swap(a, store++, i);
  swap(a, store, hi);
  return store;                        // pivot's final sorted index
}
```

**Hoare partition:**

```java
int hoarePartition(int[] a, int lo, int hi) {
  int pivot = a[lo + (hi - lo) / 2];
  int i = lo - 1, j = hi + 1;
  while (true) {
    do { i++; } while (a[i] < pivot);
    do { j--; } while (a[j] > pivot);
    if (i >= j) return j;              // partition index (NOT pivot's final rank!)
    swap(a, i, j);
  }
}
```

#### The decision

| Dimension | Lomuto | Hoare |
|---|---|---|
| **Returns** | pivot's final sorted index | partition index (`[lo, j]` ≤ pivot, `[j+1, hi]` ≥ pivot) |
| **Swaps on average** | ~2n/3 | ~n/4 (3× fewer) |
| **Duplicate-heavy input** | O(n²) possible | handles well |
| **Easier to explain** | yes (one write pointer) | no (two-pointer dance) |
| **Interview default** | yes | no (unless asked) |
| **Production default** | no | yes (std::nth_element, np.partition) |

**Why Hoare is faster.** Lomuto writes every "< pivot" element to its new location, even if it was already there — ~2n/3 swaps on random input. Hoare only swaps the "wrong-side" elements it finds from both ends — ~n/4 swaps. On modern CPUs where swap cost dominates, Hoare is measurably 2-3× faster per partition.

**The subtle gotcha with Hoare.** Hoare does NOT return the pivot's final sorted index. It returns a partition index `j` where `[lo, j]` ≤ pivot and `[j+1, hi]` ≥ pivot. In the quickselect loop, you have to compare `target ≤ j` (recurse left on `[lo, j]`) vs `target > j` (recurse right on `[j+1, hi]`) — slightly different from the Lomuto `target < p` vs `target > p` three-way comparison. Mix them up and you get an infinite loop or wrong answer.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Lomuto returns the PIVOT'S FINAL SORTED INDEX**; Hoare returns a PARTITION INDEX (not necessarily the pivot's position). This changes how the recursion branches: Lomuto compares `target < p` / `target > p` (two cases); Hoare uses `target ≤ j` / `target > j`.
- **Lomuto does ~2n/3 swaps on random input**; Hoare does ~n/4. Hoare is measurably 2-3× faster per partition on modern CPUs where swap cost dominates. Production (std::nth_element, numpy.partition) uses Hoare.
- **Hoare handles duplicate-heavy input gracefully** because it stops at equal-to-pivot elements; both sides take their share. Lomuto with `<` can push all duplicates to one side → O(n²) blowup.
- **The Hoare two-pointer dance**: `do { i++; } while (a[i] < pivot); do { j--; } while (a[j] > pivot);` — walks from both ends until a wrong-side pair is found, swaps, repeats. The `do-while` (not `while`) ensures progress even on the pivot value itself.
- **Pivot CANNOT be the first or last element in Hoare without extra care** — picking `a[lo + (hi - lo) / 2]` (middle) is the standard safe choice. First-element pivot can cause infinite recursion when the pivot is also the min of the range.
- **Interview default: Lomuto** (clearer invariant, one write pointer, easy to explain). **Production default: Hoare.** Know both.
- **Siblings: 3-way (Dutch National Flag) partition for duplicate-heavy inputs (returns two indices, groups into <, =, > buckets), BFPRT median-of-medians for guaranteed O(n) worst case.**

</details>

## Traps & gotchas

Three traps every quickselect problem can hit. Each sub-variation above calls out its own specific bugs; these three are the ones that cross problem boundaries.

### Trap 1 — deterministic pivot on adversarial input

<TrapTrace title="Last-element pivot on sorted input degenerates to O(n²)" input="a = [1,2,3,4,5,6,7,8]" :bug="trap1Bug" :fix="trap1Fix" />

### Trap 2 — k-th largest vs k-th smallest rank conversion

<TrapTrace title="Target index off-by-one between smallest and largest conventions" input="a = [3,2,1,5,6,4], k = 2 (2nd largest = 5, 2nd smallest = 2)" :bug="trap2Bug" :fix="trap2Fix" />

### Trap 3 — partition comparator `<=` instead of `<` on duplicate-heavy input

<TrapTrace title="Including the pivot in the 'less than pivot' side breaks the partition" input="a = [5,5,5,5,5], target = 2" :bug="trap3Bug" :fix="trap3Fix" />

> [trap] **The 10-second trap-check.** Before shipping any quickselect solution: (1) is the pivot RANDOMIZED or median-of-three? (2) is the target-index conversion stated for the specific "k-th X" the problem wants? (3) is the comparator STRICT (`<` not `<=`)? All three must be yes.

## In the wild — quickselect in real systems

Quickselect runs at the bottom of every scientific-computing stack, every "TOP N" database query, every image-processing median filter.

```python
# NumPy np.partition — same quickselect pattern, written in C.
# From numpy/core/src/npysort/quickselect.cpp (abridged):

def partition_kth(a, k):
    """Rearrange a in-place so a[k] holds the k-th order statistic."""
    lo, hi = 0, len(a) - 1
    while lo < hi:
        pivot = median_of_three(a, lo, (lo + hi) >> 1, hi)
        p = three_way_partition(a, lo, hi, pivot)
        if p == k:
            return
        elif p < k:
            lo = p + 1
        else:
            hi = p - 1

# np.partition(a, k) is EXACTLY this, plus:
#   - three-way partition (handles duplicate-heavy inputs)
#   - median-of-three pivot (avoids adversarial O(n²))
#   - introselect fallback to heap-select when recursion depth > 2*log2(n)
```

The pattern:
- **NumPy `np.partition`** — introselect (Musser 1997) hybrid; the engine behind `np.median`, `np.percentile`, `scipy.stats.scoreatpercentile`.
- **C++ `std::nth_element`** — same hybrid; part of the STL since 1998.
- **Pandas `.quantile`** — delegates to NumPy; every data-science pipeline that computes p99 latency uses this.
- **PostgreSQL `TOP N` queries** — the query planner emits quickselect-style partial sort when `LIMIT N` is small vs. table size.
- **OpenCV `cv2.medianBlur`** — median filter for image denoising; quickselect per 3×3 or 5×5 window.
- **Java's `java.util.Arrays.parallelSort`** (JDK 8+) — Yaroslavskiy's dual-pivot quicksort, which shares the partition scheme.

The code above is 10 lines of pseudocode. The *idea* is "partition + narrow + recurse." The complexity in production comes from pivot-selection heuristics (median-of-three, median-of-medians fallback), three-way partition for duplicate heaviness, and recursion-depth tracking for the heap-select fallback.

## Recognition drill

Each problem below is phrased without the pattern tag. Your task: name the sub-variation. The drill randomizes order each session and tracks your running score.

<RecognitionDrill pattern="quickselect" :count="10" />

> [key] **How to use.** Aim for ≥ 8/10 before considering cold-solving fluency the next bottleneck. The common confusion is quickselect vs heap-of-K vs sorting — the distractors in this drill are specifically those three. If you keep picking "heap" when the answer is "quickselect," the recognition cue to internalize is: "ONE-shot IN-memory array query with mutation allowed" → quickselect.

## Advanced — follow-ups and failure modes

The sub-variations above are the shapes you're expected to recognize cold. The questions below are the ones that come **after** you write a correct quickselect — "what if we change this one constraint?" — and separate pattern-fluent from pattern-mastered.

### What if the input is adversarial and quickselect degenerates to O(n²)?

<details>
<summary>Click to reveal</summary>

{{ advanced1 }}

</details>

### What if you need the top-K and the stream is unbounded?

<details>
<summary>Click to reveal</summary>

{{ advanced2 }}

</details>

### What if the array must stay in original order?

<details>
<summary>Click to reveal</summary>

{{ advanced3 }}

</details>

### What if you need the top-K VALUES SORTED?

<details>
<summary>Click to reveal</summary>

{{ advanced4 }}

</details>

### Breaking point — when quickselect has no advantage

<details>
<summary>Click to reveal</summary>

{{ advanced5 }}

</details>

### Cross-pattern problems

Three problems where quickselect composes with another pattern. Each is a diagnostic — if you can identify the composition and solve each, you've transferred the recognition skill beyond this chapter.

<div v-for="(p, i) in advancedCrossProblems" :key="i" style="border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 14px 16px; margin: 12px 0; background: var(--vp-c-bg-soft);">
  <div style="font-weight: 700; margin-bottom: 6px;">{{ p.title }}</div>
  <div style="font-size: 0.92em; color: var(--vp-c-text-2); margin-bottom: 8px;">{{ p.hint }}</div>
  <details>
    <summary style="font-size: 0.85em; cursor: pointer; color: var(--vp-c-brand-1);">Reveal answer sketch</summary>
    <div style="padding-top: 8px; font-size: 0.9em;">{{ p.reveal }}</div>
  </details>
</div>

## Related patterns + Check your understanding

<RelatedPatterns pattern-id="quickselect" />

<Quiz
  pattern-id="quickselect"
  :questions="quizQuestions"
/>

<PrintButton />
