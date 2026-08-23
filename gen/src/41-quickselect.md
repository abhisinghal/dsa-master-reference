# Quickselect


<PatternVideo pattern-name="Quickselect" duration="8–12 min" />
<PatternProgress pattern-id="quickselect" problems="kth-largest" />



**Grokking arc:** The motivating problem is finding one rank without needing the whole sorted order. Brute force sorts everything. **Can we do better?** Partition once, compare the pivot's final index with the target rank, and discard the side that cannot contain the answer.

## Why Quickselect exists — the story

Sorting is a powerful habit, but sometimes it is too much. If someone asks for the 2nd largest number in `[3,2,1,5,6,4]`, a full sort gives `[1,2,3,4,5,6]` and then returns `5`. Correct, but notice how much extra information you computed: you learned the full order of every value even though only one rank mattered. Quickselect exists for the moment you say, "I only need the element that would land at one index if the array were sorted."

Quickselect borrows the partition step from quicksort. Pick a pivot, move smaller values to the left and larger values to the right, then the pivot lands in its final sorted position. If that position is the target rank, you are done. If it is too small, the target is on the right; if it is too large, the target is on the left. Unlike quicksort, you never recursively sort both sides. You throw away the side that cannot contain the answer.

Trace a tiny example by hand. For `[7, 1, 5, 3, 9, 2]`, the 2nd largest is index `n-k = 4` in ascending order. Suppose pivot `5` partitions to `[1,3,2,5,9,7]`, so pivot index is `3`. Target `4` is to the right, so ignore indices `0..3`. Now partition `[9,7]`; if pivot `7` lands at index `4`, return `7`. You selected the answer without sorting `[1,3,2]` at all.

> [key] **Key Insight** — After partitioning around a pivot, the pivot sits at its final sorted index p. If p == k you're done. If p < k, the answer is in the right half; else the left. You never touch the side that doesn't contain rank k.

```svg
<svg width="720" height="240" viewBox="0 0 720 240" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <defs>
    <marker id="qs-ar-blue" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/></marker>
    <marker id="qs-ar-grn" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-success)"/></marker>
    <marker id="qs-ar-red" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-danger)"/></marker>
    <filter id="qs-s1" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="var(--dsa-neutral)" flood-opacity="0.5"/></filter>
  </defs>
  <rect x="0" y="0" width="720" height="240" fill="var(--dsa-bg)"/>
  <text x="360" y="24" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-ink)">one partition step decides which side can contain rank k</text>
  <text x="48" y="70" text-anchor="end" font-size="12" font-weight="700" fill="var(--dsa-neutral)">before</text>
  <g filter="url(#qs-s1)">
    <rect x="70" y="48" width="46" height="38" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><rect x="122" y="48" width="46" height="38" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/>
    <rect x="174" y="48" width="46" height="38" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.7"/><rect x="226" y="48" width="46" height="38" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/>
    <rect x="278" y="48" width="46" height="38" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><rect x="330" y="48" width="46" height="38" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/>
  </g>
  <g font-size="17" font-weight="700" fill="var(--dsa-ink)" text-anchor="middle">
    <text x="93" y="73">7</text><text x="145" y="73">1</text><text x="197" y="73">5</text><text x="249" y="73">3</text><text x="301" y="73">9</text><text x="353" y="73">2</text>
  </g>
  <text x="197" y="100" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-primary)">pivot = 5</text>
  <path d="M150,96 C126,122 112,132 102,146" fill="none" stroke="var(--dsa-success)" stroke-width="2" marker-end="url(#qs-ar-grn)"/>
  <path d="M250,96 C222,122 192,134 156,146" fill="none" stroke="var(--dsa-success)" stroke-width="2" marker-end="url(#qs-ar-grn)"/>
  <path d="M354,96 C294,122 246,134 210,146" fill="none" stroke="var(--dsa-success)" stroke-width="2" marker-end="url(#qs-ar-grn)"/>
  <path d="M92,96 C316,118 418,132 470,146" fill="none" stroke="var(--dsa-danger)" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#qs-ar-red)"/>
  <path d="M300,96 C388,118 476,132 522,146" fill="none" stroke="var(--dsa-danger)" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#qs-ar-red)"/>
  <line x1="218" y1="68" x2="315" y2="150" stroke="var(--dsa-primary)" stroke-width="2" marker-end="url(#qs-ar-blue)"/>
  <text x="48" y="170" text-anchor="end" font-size="12" font-weight="700" fill="var(--dsa-neutral)">after</text>
  <g filter="url(#qs-s1)">
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

## When to use it — one-shot rank selection

### Recognize by
- "find the kth smallest" or "find the kth largest" in an unsorted array
- "find the median" when you do not need the full sorted array
- "return the kth order statistic" or "element at rank r"
- "top k" when returning the k items in any order is okay and mutating/partitioning is allowed
- constraints where O(n log n) sort is acceptable but the interviewer asks for better average time
- array is available in memory, so random access and in-place swaps are allowed


<QuickselectAnim />


### When NOT to use it
You need k-th in a **stream** (no random access) — use a heap. You need the k boundary items in order — use a heap or partial sort. Adversarial inputs with the same pivot every time degrade to O(n²) — always pick a **random** pivot or use median-of-medians.

Do not reach for Quickselect when the input must remain in original order and mutation is forbidden unless you are willing to copy the array. Do not use it for repeated queries on the same data; sorting once or building an order-statistics structure may win. And if the problem requires stable ordering, tie-aware output, or all top-k values sorted, Quickselect alone only gets you the boundary; you still need post-processing.

## How to use it — template

```java
int target = rankIndex;                 // 0-based index in sorted order
int lo = 0, hi = a.length - 1;
while (lo < hi) {
    int pivotIdx = choosePivot(lo, hi);
    int p = partition(a, lo, hi, pivotIdx);
    if (p == target) {
        return a[p];
    } else if (p < target) {
        lo = p + 1;
    } else {
        hi = p - 1;
    }
}
return a[lo];
```

The template is a narrowing search over ranks, not values. `partition` gives you one value in its final sorted position. Comparing that position with `target` tells you which half can still contain the answer. `choosePivot` should be randomized or at least not always the same bad endpoint. For kth largest, convert to an ascending rank with `target = n - k`; for kth smallest, use `target = k - 1`.

---

## Quickselect (Kth Largest Element) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/)*

<ProgressCheck id="quickselect-kth-largest-element" />

### Problem
Find the **kth largest** element in an unsorted array (a one-shot query) — faster than fully sorting.

**Constraints:** `1 ≤ k ≤ n ≤ 10⁵`; expected O(n) average via partitioning.

**Example 1:** `[3,2,1,5,6,4], k = 2` → `5`.

<ExamplePreview compact :input="['3', '2', '1', '5', '6', '4', '|', '2']" :output="['5']" />

**Example 2:** `[3,2,3,1,2,4,5,5,6], k = 4` → `4`.

<ExamplePreview compact :input="['3', '2', '3', '1', '2', '4', '5', '5', '6', '|', '4']" :output="['4']" />

### Solution — brute force
The baseline is to sort the array and index into the sorted result.

```text
sort nums ascending
return nums[nums.length - k]
```

That is O(n log n) time and O(1) or O(n) extra space depending on the language and whether you can mutate the input. It is also the best first sentence in an interview because it proves you understand that "kth largest" means a rank, not necessarily a distinct value. Quickselect improves the average runtime by avoiding the side of the partition that cannot contain that rank.

A heap baseline is also possible: keep a min-heap of size k and return its root after scanning all values. That costs O(n log k) and works for streams. Quickselect is usually preferred for one in-memory one-shot query because expected O(n) is better.

**Baseline complexity:** O(n log n) time; O(1) or O(n) extra space depending on sorting/copying.

### Solution — optimized
The optimized solution keeps the original Java intact and explains the pattern that removes the brute-force bottleneck.

#### Pattern
Partition around a (randomized) pivot; recurse only into the side that contains rank k.

> [inv] **Invariant** — After partition, the pivot rests at its final sorted position `p`; everything left ≤ pivot ≤ everything right. Compare `p` to the target index to pick the side.

#### Java
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

> [note] **Trace it** — One possible randomized run for `[3,2,1,5,6,4], k=2`; target index is `6-2=4` in ascending order.

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
>
> | Round | Active range | Chosen pivot | Array shape after partition | Pivot index | Next move |
> |---|---|---|---|---|---|
> | 1 | `0..5` | `4` | values `<4`, then `4`, then values `>4` | `3` | `3 < 4`, search right |
> | 2 | `4..5` | `6` | value `5`, then `6` | `5` | `5 > 4`, search left |
> | stop | `4..4` | — | `a[4]` is fixed enough | `4` | return `5` |
>
> The whole left side below index 4 never needs to be sorted. It only needs to be known as "too small to contain the 2nd largest."

#### Rank conversion: kth largest vs kth smallest
Most bugs in this problem are off-by-one rank bugs. If the array were sorted ascending, the 1st smallest is index `0`, so kth smallest is `k - 1`. The 1st largest is the final index `n - 1`, so kth largest is `n - k`. For `[1,2,3,4,5,6]`, the 2nd largest is `5`, which sits at index `4`; `n-k = 6-2 = 4`. Say this conversion out loud before writing the loop.

Duplicates do not change the formula. In `[3,2,3,1,2,4,5,5,6]`, sorted ascending is `[1,2,2,3,3,4,5,5,6]`. The 4th largest is index `9-4=5`, value `4`. You are selecting by position after sorting, not by distinct value.

#### Partition mechanics in plain English
The partition helper temporarily moves the pivot to the end. `store` marks the first index where a value `>= pivot` may belong. As you scan from `lo` to `hi-1`, every value smaller than pivot gets swapped to `store`, and `store` advances. At the end, swapping the pivot into `store` places it after all smaller values and before all larger-or-equal values. That is enough for selection; the left side does not need to be internally sorted.

Using `< pivot` instead of `<= pivot` means duplicates equal to the pivot collect on the right side. That is valid for selection because the pivot still lands at one sorted-compatible position. On arrays with many equal values, three-way partitioning (`<`, `=`, `>`) can be faster, but the two-way version is the standard compact interview solution.

#### Mutability and return shape
Quickselect rearranges the array. It does not sort it, but it absolutely mutates it. That is fine for most LeetCode problems because the input array is not reused after the call. In a production API, you should either document the mutation or copy the array first. Copying preserves the caller's data but changes the space complexity to O(n). In an interview, mention this trade-off if the prompt says \"do not modify the input.\"

Also distinguish between returning the **kth value** and returning the **top k values**. The provided code returns one integer. If the prompt asks for the k largest elements in any order, Quickselect can partition until index `n-k` is in place, and then the suffix from `n-k` to `n-1` contains the k largest elements, not necessarily sorted. If the prompt asks for those k elements sorted, you either sort just that suffix or use a heap / full sort depending on constraints.

#### Pivot quality and randomness
The partition logic is deterministic once a pivot index is chosen. The randomness is only there to protect you from consistently bad pivots. On already sorted input, always choosing the last element is disastrous for kth largest: the pivot lands at the end, then the next end, then the next, shrinking by one each time. Random choice makes that pattern extremely unlikely.

If randomization is not allowed, median-of-three is a practical compromise: compare the first, middle, and last values and use their median as the pivot. The theoretical worst-case linear solution is median-of-medians, but it is longer and rarely expected in a standard interview unless the prompt explicitly demands deterministic O(n). Most interviewers are satisfied when you name the worst case and use randomized pivoting.

#### Duplicates and three-way partitioning
The two-way partition above works with duplicates, but it may do extra work when the array contains many values equal to the pivot. For example, if every value is `5`, a two-way partition may place the pivot at the start of the active range repeatedly. A three-way partition groups values into `< pivot`, `== pivot`, and `> pivot`. Then if the target rank falls inside the equal band, you can return immediately.

You do not need to implement three-way partitioning unless the interviewer pushes on duplicate-heavy inputs. The key is to understand that duplicates do not make the answer ambiguous: kth largest is still a position in sorted order. If several equal values occupy that region, returning that value is correct.

#### Testing checklist
Use these mental tests to catch rank and partition mistakes:

| Input | k | Expected | Lesson |
|---|---:|---:|---|
| `[3,2,1,5,6,4]` | 2 | 5 | target is `n-k`, not `k` |
| `[1]` | 1 | 1 | loop may never run; return target value |
| `[3,3,3,3]` | 2 | 3 | duplicates are ranks too |
| `[2,1]` | 1 | 2 | kth largest means largest when k is 1 |
| `[2,1]` | 2 | 1 | smallest is also kth largest when k equals n |

#### How to narrate partition during a dry run
When tracing Quickselect, do not try to fully sort the active range on paper. Say which pivot you chose, draw a vertical bar at its final index after partition, and compare that index to the target. Everything left of the bar is \"small enough,\" everything right is \"large enough,\" but their internal order is irrelevant. This keeps the trace short and reinforces the reason Quickselect is faster than quicksort.

For the example `[3,2,1,5,6,4]`, if pivot `4` lands at index `3`, you can immediately say: \"The target is index 4, so every value at index 0 through 3 is too low-ranked to matter now.\" That is the core optimization. Each round should delete a range from consideration.

#### Same pattern, new tweaks
"Partition around a pivot and recurse into only one side" selects without fully sorting:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Kth Largest Element](https://leetcode.com/problems/kth-largest-element-in-an-array/) | the target index is `n-k` in ascending order | O(n) avg |
| [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | partition by squared distance; after selection, the first k positions hold the closest points in any order | O(n) avg |
| [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | quickselect over distinct values using frequency as the partition key | O(n) avg |
| [Wiggle Sort II](https://leetcode.com/problems/wiggle-sort-ii/) | quickselect the median, then place larger/smaller halves into virtual indices | O(n) avg |
| [Median of an Unsorted Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | select index `n/2` (and maybe `n/2 - 1` for even length) instead of sorting | O(n) avg |

> [trap] **Common Trap** — Bad pivots. *Example:* `nums=[1,2,3,4,5]`, k=1, picking the *last* element as pivot every time → each partition shrinks by only 1 → O(n²). Random pivot (or median-of-three) keeps average O(n).

<TrapTrace title="Bad pivots" input="nums=[1,2,3,4,5]" bug="'nums=[1,2,3,4,5]', k=1, picking the *last* element as pivot every time → each partition shrinks by only 1 → O(n²). Random pivot (or median-of-three) keeps average O(n)." fix="See the guidance in the trap description and the code snippet." />

> [note] **Interview script** — First, I'd translate kth largest into an ascending target index: `n-k`, so duplicates are handled naturally by rank. The brute force is sorting in O(n log n), and a heap gives O(n log k), especially for streams. Since this is a one-shot array query, I'll use Quickselect: partition around a randomized pivot and continue only on the side containing the target index. The expected time is O(n), worst-case O(n²) with unlucky pivots, and space is O(1) in-place.

> [pat] **Pattern Connection** — For a *stream* or repeated queries, a size-k heap (O(n log k)) beats one-shot Quickselect. Quickselect also drives *Wiggle Sort II* and median-of-medians selection.

### Time Complexity
Time O(n) average, O(n²) worst · Space O(1).

The average is linear because a random pivot tends to discard a meaningful fraction of the remaining range. The worst case happens when each pivot is the smallest or largest remaining element, so the active range shrinks by only one each time. This implementation is iterative, so it avoids recursion stack space.

O(n) expected with randomized pivots; O(n²) worst case if pivots are consistently bad.


### Space Complexity
O(1) extra because the selection loop partitions in place.

### Learning notes
- Why `target = a.length - k`? — kth largest is the `n-k` index in ascending sorted order.
- Why choose a random pivot? — it avoids repeatedly picking the smallest/largest element on sorted or adversarial inputs.
- Why move the pivot to `hi`? — it frees the scan range and makes the final swap simple.
- Why `store` advances only for `< pivot`? — it partitions smaller values to the left and leaves greater/equal values to the right.
- Why discard one side after partition? — the pivot's final rank tells which side can still contain the target.
- Why return `a[target]`? — once the loop narrows or hits the target, that index holds the selected rank.

---

## Check your understanding

<Quiz
  pattern-id="quickselect"
  :questions='[{"q": "Average complexity of Quickselect for k-th element?", "choices": [{"text": "O(n)", "correct": true, "explanation": "Each partition eliminates a constant fraction of remaining candidates on average."}, {"text": "O(n log n)", "correct": false, "explanation": "That is full quicksort."}, {"text": "O(log n)", "correct": false}, {"text": "O(k)", "correct": false}]}, {"q": "Worst-case complexity of Quickselect (without randomization)?", "choices": [{"text": "O(n²)", "correct": true, "explanation": "On adversarial inputs / sorted-with-first-pivot."}, {"text": "O(n log n)", "correct": false}, {"text": "O(n)", "correct": false, "explanation": "Only with median-of-medians pivot."}, {"text": "O(log n)", "correct": false}]}, {"q": "For k-th LARGEST via Quickselect, how do you compute the index?", "choices": [{"text": "Look for index n - k in ascending-sorted order", "correct": true, "explanation": "k-th largest = element at position n-k when sorted ascending."}, {"text": "Look for index k", "correct": false, "explanation": "That is k-th smallest."}, {"text": "Random", "correct": false}, {"text": "Nothing; use max-heap", "correct": false, "explanation": "Works but heavier."}]}, {"q": "What is Wiggle Sort II’s O(n) trick using Quickselect?", "choices": [{"text": "Quickselect median, then Dutch flag partition using virtual index mapping", "correct": true, "explanation": "Virtual index `(2i+1) % (n|1)` interleaves ranks correctly."}, {"text": "Just sort", "correct": false, "explanation": "That is O(n log n)."}, {"text": "Random shuffle", "correct": false}, {"text": "BFS", "correct": false}]}, {"q": "What guarantees Quickselect terminates?", "choices": [{"text": "The partition strictly reduces the search size by at least 1 each step", "correct": true, "explanation": "The pivot itself is placed correctly and excluded."}, {"text": "Random luck", "correct": false}, {"text": "Recursion depth bound", "correct": false}, {"text": "Sorted input", "correct": false}]}]'
/>

<RelatedPatterns pattern-id="quickselect" />
