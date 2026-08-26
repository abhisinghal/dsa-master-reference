# Divide &amp; Conquer


<PatternVideo pattern-name="Divide & Conquer" duration="8–12 min" />

<PatternProgress pattern-id="divide-conquer" problems="inversions, count-of-range-sum, reverse-pairs, global-and-local-inversions, sort-list" />



## Why divide and conquer exists — the story

You're a game engine developer at Riot. Every frame you must sort the visible entities by depth to correctly render transparent water effects. **50,000 entities. 60 frames per second. That's 3 million sorts per second per player.**

The obvious approach: bubble sort, insertion sort, or any O(n²) sort. For 50,000 entities that's `2.5·10⁹` comparisons per frame — **40 seconds per frame** on a modern CPU. Frame budget is 16 milliseconds. You are **2,500× over budget.** Water flickers, players uninstall.

You could try to be clever with domain tricks: bucket the entities by depth ranges, sort each bucket. But entities are moving; buckets constantly rebalance. You could try to sort incrementally frame-over-frame, but a single teleport ruins the assumption.

The right answer is a **general-purpose O(n log n) sort** — and the one used by every game engine, JVM, and database on Earth is **merge sort** (or a hybrid like Timsort). The insight is: sort of `[5, 2, 6, 1]` is hard. Sort of `[5, 2]` is easy. Sort of `[6, 1]` is easy. Once both halves are sorted, **merging** them in one linear pass produces the final sorted result. `T(n) = 2·T(n/2) + O(n) = O(n log n)`. For 50,000 entities: `50,000 · log₂(50,000) ≈ 800,000` comparisons per frame — **50,000× faster than bubble sort**. Frame budget met. Water renders correctly.

That's **divide and conquer**: split the input, solve each half recursively, then combine. The split is the easy part; the *combine* is where the cleverness lives. Merge sort combines by merging two sorted halves. Quicksort combines by picking a pivot and letting the recursion handle everything. Fast Fourier Transform combines by "twisting" two half-spectra with roots of unity. Karatsuba's multiplication combines by reusing three product results instead of four. Every one is the same shape: **T(n) = a·T(n/b) + f(n)**.

**Grokking arc:** The motivating problem is counting cross-boundary relationships that brute force checks pair by pair. Brute force compares every pair. **Can we do better?** Split the input, solve organized halves, then let the combine step count many relationships at once.

Divide and conquer is what you reach for when solving the whole input directly feels messy, but solving smaller pieces feels natural. You split the input, solve the left half, solve the right half, and then combine the two answers. The split is usually the easy part. The combine step is where the cleverness lives.

Merge sort is the cleanest example. Sorting `[5,2,6,1]` directly is noisy, but sorting `[5,2]` and `[6,1]` is smaller, and sorting single elements is trivial. The merge step then combines two sorted halves in linear time. That same merge step can do more than sort. When merging `[2,5]` and `[1,6]`, the value `1` from the right half jumps before both `2` and `5` from the left half, so you discover two inversions at once: `(5,1)` and `(2,1)`.

> [key] **Key Insight** — The base case must be a size-1 or size-0 subarray that returns its own trivial answer. Every layer of the recursion tree above it does work proportional to n, and the tree is `log n` deep -> total O(n log n) if the combine is O(n).

That is the mental upgrade from "recursion" to "divide and conquer." Recursion is just a control-flow tool. Divide and conquer is a performance strategy: do the expensive cross-boundary work while the halves are already organized. In count-inversions problems, the halves being sorted lets one comparison stand for many pairs. In closest-pair-of-points, the halves being solved lets you only inspect a narrow strip across the boundary. The combine step pays for the insight.

```svg
<svg width="720" height="260" viewBox="0 0 720 260" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <defs>
    <marker id="dc-ar-blue" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/></marker>
    <filter id="dc-s1" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="var(--dsa-neutral)" flood-opacity="0.5"/></filter>
  </defs>
  <rect x="0" y="0" width="720" height="260" fill="var(--dsa-bg)"/>
  <text x="360" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-ink)">merge sort recursion tree: split down, combine up</text>
  <g stroke="var(--dsa-primary)" stroke-width="1.6" marker-end="url(#dc-ar-blue)">
    <line x1="360" y1="52" x2="220" y2="82"/><line x1="360" y1="52" x2="500" y2="82"/>
    <line x1="220" y1="104" x2="130" y2="132"/><line x1="220" y1="104" x2="288" y2="132"/>
    <line x1="500" y1="104" x2="432" y2="132"/><line x1="500" y1="104" x2="590" y2="132"/>
    <line x1="130" y1="152" x2="74" y2="184"/><line x1="130" y1="152" x2="130" y2="184"/>
    <line x1="288" y1="152" x2="250" y2="184"/><line x1="288" y1="152" x2="306" y2="184"/>
    <line x1="432" y1="152" x2="414" y2="184"/><line x1="432" y1="152" x2="470" y2="184"/>
    <line x1="590" y1="152" x2="590" y2="184"/><line x1="590" y1="152" x2="646" y2="184"/>
  </g>
  <g filter="url(#dc-s1)" text-anchor="middle" font-weight="700">
    <rect x="244" y="32" width="232" height="30" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary-line)"/><text x="360" y="52" font-size="12" fill="var(--dsa-ink)">[3,1,4,1,5,9,2,6]</text>
    <rect x="152" y="82" width="136" height="28" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><text x="220" y="101" font-size="12" fill="var(--dsa-ink)">[3,1,4,1]</text>
    <rect x="432" y="82" width="136" height="28" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><text x="500" y="101" font-size="12" fill="var(--dsa-ink)">[5,9,2,6]</text>
    <rect x="96" y="132" width="68" height="26" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><text x="130" y="150" font-size="11" fill="var(--dsa-ink)">[3,1]</text>
    <rect x="254" y="132" width="68" height="26" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><text x="288" y="150" font-size="11" fill="var(--dsa-ink)">[4,1]</text>
    <rect x="398" y="132" width="68" height="26" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><text x="432" y="150" font-size="11" fill="var(--dsa-ink)">[5,9]</text>
    <rect x="556" y="132" width="68" height="26" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><text x="590" y="150" font-size="11" fill="var(--dsa-ink)">[2,6]</text>
    <rect x="55" y="184" width="38" height="26" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="74" y="202" font-size="11" fill="var(--dsa-ink)">[3]</text>
    <rect x="111" y="184" width="38" height="26" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="130" y="202" font-size="11" fill="var(--dsa-ink)">[1]</text>
    <rect x="231" y="184" width="38" height="26" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="250" y="202" font-size="11" fill="var(--dsa-ink)">[4]</text>
    <rect x="287" y="184" width="38" height="26" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="306" y="202" font-size="11" fill="var(--dsa-ink)">[1]</text>
    <rect x="395" y="184" width="38" height="26" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="414" y="202" font-size="11" fill="var(--dsa-ink)">[5]</text>
    <rect x="451" y="184" width="38" height="26" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="470" y="202" font-size="11" fill="var(--dsa-ink)">[9]</text>
    <rect x="571" y="184" width="38" height="26" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="590" y="202" font-size="11" fill="var(--dsa-ink)">[2]</text>
    <rect x="627" y="184" width="38" height="26" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="646" y="202" font-size="11" fill="var(--dsa-ink)">[6]</text>
  </g>
  <g font-size="11" fill="var(--dsa-neutral)" font-weight="700">
    <text x="586" y="51">combine level: O(n)</text>
    <text x="586" y="101">combine level: O(n)</text>
    <text x="586" y="150">combine level: O(n)</text>
    <text x="54" y="232" fill="var(--dsa-primary)">height = log n</text>
  </g>
  <rect x="470" y="218" width="206" height="30" rx="9" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/>
  <text x="573" y="238" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">O(n) × log n = O(n log n)</text>
</svg>
```
<div class="readfig"><b>How to read it:</b> The input splits until every leaf is size 1. On the way back up, each merge level touches all <b>n</b> elements total, even though the work is spread across many small merges. There are <b>log n</b> levels, so merge-sort-shaped divide and conquer costs <b>O(n log n)</b> when combine is linear.</div>

## When to use it — and when not to

### Recognize by
- "solve the halves, combine" — merge sort family.
- "count inversions" / "count of smaller after self" / "reverse pairs".
- "cross-boundary pairs" where left-half and right-half relationships matter.
- "closest pair of points", "maximum subarray via D&C" (Kadane's O(n) beats it but D&C teaches the shape).
- constraints around `10^5` where O(n²) pair checking is too slow but O(n log n) fits.
- input can be split into independent subproblems after you define the right combine information.


<DivideConquerAnim />


### When NOT to use it
The two halves *depend on each other* (state flows across the split). Then you can't recurse independently — reach for DP with a state that captures the cross-half interaction. Also, if the combine step is O(n log n), your total becomes O(n log² n) — check if a single-pass approach exists.

Also avoid it when:
- a simple linear scan exists, such as Kadane for maximum subarray.
- the split creates highly unbalanced recursion; you may fall toward O(n²).
- the combine step has to re-scan too much hidden state from both halves.
- the problem needs online updates; segment trees or Fenwick trees may be better.
- recursion depth could exceed limits and an iterative structure is simpler.

## How to use it — template

```java
Result solve(int[] a, int lo, int hi, Scratch scratch) {
    if (lo >= hi) return baseResult(a, lo);
    int mid = lo + (hi - lo) / 2;
    Result left = solve(a, lo, mid, scratch);
    Result right = solve(a, mid + 1, hi, scratch);
    Result cross = combine(a, lo, mid, hi, scratch);
    return mergeResults(left, right, cross);
}
```

The recursive calls should solve independent halves. The `combine` function is the heart: it counts cross pairs, merges sorted runs, picks a crossing maximum, or builds whatever information the parent needs. The `Scratch` parameter is optional but important in Java; passing one reusable temp array avoids allocating a new array at every recursion level. Finally, `mergeResults` packages the answer for the parent.

A useful interview sentence is: "I need each recursive call to return not only the answer inside its half, but also enough structure to combine with the other half." For merge-sort counting, that structure is sorted order. Without sorted order, you would still be stuck comparing every left item to every right item.

## The recursion tree intuition

For merge-sort-shaped divide and conquer, each level of recursion touches every element once in the combine step. At the bottom, there are many size-1 problems. One level up, you merge pairs into size-2 sorted runs. Then size 4, size 8, and so on. There are about `log n` levels, and each level does O(n) total merge work, so the total is O(n log n). This is the same reason merge sort is predictable even on already-sorted or reverse-sorted input.

The warning is that the combine step sets the cost. If you split in half but then compare every left element to every right element during combine, that level costs O(n²), and divide and conquer did not save you. The art is to make each recursive answer return structure that makes combine cheap: sorted order, prefix/suffix summaries, bounding boxes, or whatever the parent needs.

### What the combine step can carry
For inversion count, combine carries sorted order and a count. For maximum subarray via divide and conquer, each node carries four values: total sum, best prefix sum, best suffix sum, and best subarray sum. For closest pair of points, each half carries its closest distance, and combine checks only points near the vertical split. The pattern is not "always merge arrays"; the pattern is "design a summary that makes cross-boundary work small."

## Designing the combine step — a checklist

Before writing code, ask three questions. First, what does each half return? It might be a sorted range, a count, a best prefix/suffix summary, or a distance. Second, what relationships cross the middle and are not counted inside either half? Those are the only things combine must handle. Third, can the returned structure make those cross relationships cheaper than checking all pairs? If the answer to the third question is no, your divide-and-conquer idea is probably just brute force with recursion.

For inversion count, the answers are crisp: each half returns sorted order plus its internal inversion count; cross relationships are pairs with left index in the left half and right index in the right half; sorted order lets one comparison count many such pairs. This checklist keeps the solution grounded instead of turning into vague recursion.

---

## Merge Sort &amp; Count of Smaller Numbers After Self <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)*

<ProgressCheck id="merge-sort-amp-count-of-smaller-numbers-after-self" />

### Problem
For each element, count how many elements **to its right are smaller** — the "count smaller after self" problem.

**Constraints:** `1 ≤ n ≤ 10⁵`; values fit in `int`; needs O(n log n).

**Example 1:** `[5,2,6,1]` → `[2,1,1,0]`.

<ExamplePreview compact :input="['5', '2', '6', '1']" :output="['2', '1', '1', '0']" />

**Example 2:** `[2,4,1,3,5]` has inversions `(2,1)`, `(4,1)`, `(4,3)` → total `3`.

<ExamplePreview compact :input="['2', '4', '1', '3', '5']" :output="['(2,1)']" />

### Solution — brute force
The obvious baseline checks every pair `(i,j)` with `i < j` and counts when `a[i] > a[j]`.

```java
// Pseudocode baseline:
// count = 0
// for i in 0..n-1:
//     for j in i+1..n-1:
//         if a[i] > a[j]: count++
```

For `[5,2,6,1]`, the inversion pairs are `(5,2)`, `(5,1)`, `(2,1)`, and `(6,1)`, so the total inversion count is `4`. This is O(n²), which is too slow for `n = 100000`. Divide and conquer improves it by counting many cross pairs at once during merge.

**Baseline complexity:** O(n²) time and O(1) extra space for total inversion count.

### Solution — optimized
The optimized solution keeps the original Java intact and explains the pattern that removes the brute-force bottleneck.

#### Pattern
Stable merge sort whose merge step *counts* cross-pair relationships (inversions, smaller-to-the-right).

> [key] **Key Insight** — During merge, when you take an element from the right half before some remaining left-half elements, you've discovered order relationships between them for free. Piggyback the count on the sort.

> [inv] **Invariant** — Each half is fully sorted before merge; the combine step sees a clean cross-boundary comparison.

#### Why sorting helps counting
Before the merge, the left and right halves are individually sorted. That means comparisons become bulk statements. If the current left value is `2` and current right value is `1`, then not only is `2 > 1`, every later value in the sorted left half is also greater than `1`. One comparison just counted multiple original pairs. That is the exact reason the optimized solution beats brute force.

Do not lose sight of original positions in variants. Sorting changes order, but questions like Count of Smaller After Self need answers attached to original indices. The usual trick is to sort small records like `(value, originalIndex)` rather than raw integers. The array becomes sorted by value for merge logic, while `originalIndex` tells you where to add the discovered count.

#### Java (inversion count)
```java
long countInversions(int[] a) { return sort(a, 0, a.length - 1, new int[a.length]); }
long sort(int[] a, int lo, int hi, int[] tmp) {
    if (lo >= hi) return 0;
    int mid = (lo + hi) >>> 1;
    long inv = sort(a, lo, mid, tmp) + sort(a, mid + 1, hi, tmp);
    int i = lo, j = mid + 1, k = lo;
    while (i <= mid && j <= hi) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];
        else { inv += (mid - i + 1); tmp[k++] = a[j++]; }   // a[i..mid] all > a[j]
    }
    while (i <= mid) tmp[k++] = a[i++];
    while (j <= hi)  tmp[k++] = a[j++];
    System.arraycopy(tmp, lo, a, lo, hi - lo + 1);
    return inv;
}
```

> [note] **Trace it** — inversion count for `[5,2,6,1]`.

<CodeTrace
  title="Count Inversions via merge sort — nums=[5,2,6,1]"
  :values="[5,2,6,1]"
  :windowKeys="['i','j']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0, j: 1 }, vars: { subarray: "[5,2]", split: 1 }, note: "merge halves [5]/[2]. 5 gt 2 → 1 inversion", added: [0,1] },
    { pointers: { i: 2, j: 3 }, vars: { subarray: "[6,1]", split: 1 }, note: "merge halves [6]/[1]. 6 gt 1 → 1 inversion", added: [2,3] },
    { pointers: { i: 0, j: 2 }, vars: { L: "[2,5]", R: "[1,6]", inv: 2 }, note: "merge: L[0]=2 vs R[0]=1 → R first (+2 inv from L)" },
    { pointers: { i: 0, j: 3 }, vars: { L: "[2,5]", R: "[6]", inv: 2 }, note: "L[0]=2 lt R[0]=6 → take 2" },
    { pointers: { i: 1, j: 3 }, vars: { L: "[5]", R: "[6]", inv: 2 }, note: "5 lt 6 → take 5, then 6. total = 1+1+2 = 4" }
  ]'
/>
#### How this differs from quicksort-style divide and conquer
Quicksort also divides and conquers, but its combine step is almost empty after partitioning; the clever work happens before the recursive calls. Merge-sort counting is the opposite: the split is mechanical, and the merge is where you count. In interviews, naming where the cleverness lives helps you choose the right invariant. For inversion counting, you want the postcondition "this range is sorted and its internal inversions are counted" after every recursive call.

#### Overflow and stability details
The inversion total can be as large as `n * (n - 1) / 2`, which exceeds `int` when `n` is large, so the return type is `long`. Stability matters when equal values appear: equal numbers are not inversions, so the merge uses `<=` to take the left value first. If you accidentally use `<`, duplicates may be pulled from the right first and can corrupt per-index counting variants even when the total inversion count looks close.

> [pat] **Pattern Connection** — The "count while sorting" trick answers *Count of Smaller After Self*, *Reverse Pairs*, and *Count Range Sum* (merge sort over prefix sums) — a recurring staff-level technique. A BIT/segment tree is the alternative.

#### Extending from inversion count to per-index counts
The shown code counts total inversions. For LeetCode's per-index "count smaller after self," you keep pairs `(value, originalIndex)` instead of raw values, and when left elements move after right elements, you add the number of already-taken right elements to that original index's answer. The skeleton is identical: split, sort pairs by value, and do all cross-boundary accounting inside merge. This is why interviewers often ask the simpler inversion count first; it teaches the combine step without the original-index bookkeeping.

#### Mini trace: recursion shape
For `[5,2,6,1]`, the call tree splits into `[5,2]` and `[6,1]`, then into singletons. The first merge returns sorted `[2,5]` with one inversion. The second returns `[1,6]` with one inversion. The final merge counts two cross inversions caused by `1`, then returns `[1,2,5,6]`. The final answer is not computed at one magic line; it accumulates as `leftAnswer + rightAnswer + crossAnswer` at every parent.

#### Reverse pairs as the same combine idea
Reverse Pairs asks for `i < j` and `a[i] > 2 * a[j]`. The merge itself still sorts normally, but many implementations do a separate two-pointer counting pass before merging. For each left index `i`, advance a right pointer while the condition holds; because both halves are sorted, the right pointer never moves backward. Then merge the halves. The lesson is important: the combine step does not have to count only inside the merge loop. It can perform any linear cross-boundary pass as long as the halves' sorted structure makes it safe.

#### Count Range Sum as prefix-sum divide and conquer
Count Range Sum looks unrelated until you convert the array to prefix sums. A subarray sum from `i` to `j-1` is `prefix[j] - prefix[i]`. Now the question becomes: for each prefix on the left, how many prefixes on the right fall into `[prefix[i] + lower, prefix[i] + upper]`? Merge sort over prefix sums keeps each half sorted, so two moving pointers count the valid range in linear time per level. Same shape, different thing being counted.

#### Iterative alternative
If recursion makes you nervous in Java, merge sort can be written bottom-up: merge runs of length 1, then 2, then 4, then 8. The counting logic inside each merge range is the same. Interviewers usually prefer the recursive version because it shows the divide-and-conquer idea directly, but recognizing the bottom-up form helps when stack depth, allocation strategy, or performance tuning matters.

#### Same pattern, new tweaks
"Piggyback a count onto the merge step" answers a family of cross-pair questions:

| Variation | The one thing that changes |
|---|---|
| [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | Carry original indices and accumulate how many right-half values moved before each left value. |
| [Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) | Before merging, count pairs with `a[i] > 2·a[j]`, using `long` to avoid overflow. |
| [Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/) | Run merge sort over prefix sums and count prefix differences in `[lower, upper]`. |
| [Global and Local Inversions](https://leetcode.com/problems/global-and-local-inversions/) | Compare total inversions with local adjacent inversions; the count idea explains the distinction. |
| [Sort List](https://leetcode.com/problems/sort-list/) | Same divide/merge shape, but the split is fast/slow pointers and the merge relinks nodes. |

> [trap] **Common Trap** — Adding the inversion count `mid - i + 1` on the wrong branch (it belongs to the *right-element-taken* case, where all remaining left elements exceed it) or using `int` for a count that can reach ~n²/2 — use `long`.

> [note] **Interview script** — First, I'd present the brute force: compare every pair `i < j`, which is O(n²). To optimize, I use merge sort because after each half is sorted, cross-half comparisons become bulk counts. During merge, when a right value is smaller than `a[i]` in the left half, it is smaller than all remaining left values, so I add `mid - i + 1`. This gives O(n log n) time and O(n) extra space.

### Time Complexity
Time O(n log n) · Space O(n). The recursion has `log n` levels, and each level performs O(n) merge work.

O(n log n): `log n` merge-sort levels, each doing O(n) total merge/count work.


### Space Complexity
O(n) for the reusable temp array, plus O(log n) recursion stack.

### Learning notes
- Why `lo >= hi`? — a range of size 0 or 1 is already sorted and has no inversions.
- Why allocate `tmp` once outside recursion? — one reusable buffer avoids per-frame array allocation.
- Why `a[i] <= a[j]` takes from the left? — equal values are not inversions, and stable merging protects per-index variants.
- Why add `mid - i + 1`? — if sorted-left `a[i] > a[j]`, every remaining left value is also greater than that right value.
- Why `System.arraycopy` back? — parent calls rely on this range being sorted after the child returns.
- Why `long inv`? — inversion counts can grow near n²/2 and overflow `int`.

---

## Check your understanding

<Quiz
  pattern-id="divide-conquer"
  :questions='[{"q": "Merge sort merges two halves in O(n). Total complexity?", "choices": [{"text": "O(n log n)", "correct": true, "explanation": "By Master Theorem: T(n) = 2T(n/2) + O(n)."}, {"text": "O(n²)", "correct": false}, {"text": "O(log n)", "correct": false}, {"text": "O(n)", "correct": false}]}, {"q": "For Count Inversions during merge sort, when is the count added?", "choices": [{"text": "When taking from the right half: add (leftRemaining) to the count", "correct": true, "explanation": "Each such take crosses `leftRemaining` inversions."}, {"text": "At start of merge", "correct": false}, {"text": "At end of merge", "correct": false, "explanation": "Batch-counting works too but the per-take is standard."}, {"text": "Never — count separately", "correct": false}]}, {"q": "For Reverse Pairs (i < j with nums[i] > 2*nums[j]), why long?", "choices": [{"text": "2 * nums[j] can overflow int", "correct": true, "explanation": "Cast to long before comparison."}, {"text": "For readability", "correct": false}, {"text": "Faster than int", "correct": false, "explanation": "Usually slower."}, {"text": "Not needed", "correct": false, "explanation": "Overflow bug otherwise."}]}, {"q": "For Sort List (linked list mergesort), how do you split in O(1) space?", "choices": [{"text": "Fast/slow pointers to find middle; cut the link", "correct": true, "explanation": "Middle split via fast/slow, then merge."}, {"text": "Copy to array", "correct": false, "explanation": "O(n) space."}, {"text": "Random split", "correct": false}, {"text": "Not possible", "correct": false}]}, {"q": "When would you NOT use divide & conquer?", "choices": [{"text": "When the subproblems aren’t independent (need shared state)", "correct": true, "explanation": "Then DP or shared-memoization is better."}, {"text": "When n is large", "correct": false, "explanation": "D&C shines for large n."}, {"text": "When recursion is banned", "correct": false, "explanation": "You can iterate; possible but ugly."}, {"text": "Never — always use D&C", "correct": false}]}]'
/>

<PrintButton />

<RelatedPatterns pattern-id="divide-conquer" />
