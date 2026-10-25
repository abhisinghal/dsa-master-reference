# Binary Search

<script setup>
const canonicalCode = `// Find the smallest index i in [0, n) such that P(a[i]) is true.
// For plain lookup, P(x) = (x >= target).
int lowerBound(int[] a, int target) {
    int lo = 0, hi = a.length;          // half-open [lo, hi)
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;   // overflow-safe
        if (a[mid] < target) lo = mid + 1;  // P(a[mid]) false: answer is strictly right
        else                 hi = mid;      // P(a[mid]) true : mid may be the answer; keep it
    }
    return lo;                           // lo == hi == first i with P(a[i]) true, or a.length
}`

const canonicalInvariant = {
  statement: 'The first index i with P(a[i]) true (if any) lies in the half-open range [lo, hi).',
  initialization: 'At entry lo=0, hi=a.length, so [lo, hi) covers the whole array. Any index with P true is inside — including the sentinel a.length when no such index exists.',
  maintenance: 'Each iteration either sets lo := mid+1 (ruling out indices up to mid because P(a[mid]) is false) or hi := mid (ruling out indices beyond mid while keeping mid, because P(a[mid]) is true). Either branch strictly shrinks hi - lo and preserves the invariant.',
  termination: 'When lo == hi the interval is empty. lo is now the first index with P true, or a.length if no such index exists. The loop always terminates because hi - lo strictly decreases on every iteration.'
}

const canonicalSpecs = [
  { slug: 'lower-upper-bound', title: 'Lower / upper bound' },
  { slug: 'rotated', title: 'Rotated sorted array' },
  { slug: 'peak-bitonic', title: 'Peak in bitonic array' },
  { slug: '2d-matrix', title: 'Search 2D matrix' },
  { slug: 'first-last-position', title: 'First and last position' }
]

const canonicalComplexity = { time: 'O(log n)', space: 'O(1)' }

const lowerUpperCode = `int lowerBound(int[] a, int target) {
    int lo = 0, hi = a.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < target) lo = mid + 1;   // strict < for lower bound
        else                 hi = mid;
    }
    return lo;
}

int upperBound(int[] a, int target) {
    int lo = 0, hi = a.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] <= target) lo = mid + 1;  // <= for upper bound
        else                   hi = mid;
    }
    return lo;
}

int indexOf(int[] a, int target) {
    int i = lowerBound(a, target);
    return (i < a.length && a[i] == target) ? i : -1;
}`

const rotatedCode = `int searchRotated(int[] a, int target) {
    int lo = 0, hi = a.length - 1;              // closed interval here — we return on exact match
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;

        if (a[lo] <= a[mid]) {                  // left half [lo..mid] is sorted
            if (a[lo] <= target && target < a[mid]) hi = mid - 1;
            else                                     lo = mid + 1;
        } else {                                 // right half [mid..hi] is sorted
            if (a[mid] < target && target <= a[hi]) lo = mid + 1;
            else                                     hi = mid - 1;
        }
    }
    return -1;
}`

const peakCode = `int findPeak(int[] a) {
    int lo = 0, hi = a.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < a[mid + 1]) lo = mid + 1;  // rising → peak is to the right
        else                     hi = mid;      // falling or at peak → peak is at mid or left
    }
    return lo;                                   // lo == hi is a peak
}`

const matrixCode = `boolean searchMatrix(int[][] mat, int target) {
    int m = mat.length, n = mat[0].length;
    int lo = 0, hi = m * n;              // half-open on the flattened index
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        int v = mat[mid / n][mid % n];   // the flat-to-2D projection
        if (v < target) lo = mid + 1;
        else            hi = mid;
    }
    return lo < m * n && mat[lo / n][lo % n] == target;
}`

const firstLastCode = `int[] searchRange(int[] a, int target) {
    int first = lowerBound(a, target);
    if (first == a.length || a[first] != target) return new int[]{-1, -1};
    int last = lowerBound(a, target + 1) - 1;
    return new int[]{first, last};
}

int lowerBound(int[] a, int t) {
    int lo = 0, hi = a.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < t) lo = mid + 1;
        else            hi = mid;
    }
    return lo;
}`

const bareMechFrames = [
  { lo: 0, hi: 5, mid: 2, verdict: 'go-right', caption: 'Step 1 — lo=0, hi=6 (past end). mid=2, a[2]=5 < 7. lo := 3.' },
  { lo: 3, hi: 5, mid: 4, verdict: 'go-left',  caption: 'Step 2 — lo=3, hi=6. mid=4, a[4]=9 ≥ 7. hi := 4.' },
  { lo: 3, hi: 3, mid: 3, verdict: 'found',    caption: 'Step 3 — lo=3, hi=4. mid=3, a[3]=7 ≥ 7. hi := 3. Loop ends: lo==hi==3. a[3]==7. Return 3.' }
]

const lowerBoundFrames = [
  { lo: 0, hi: 4, mid: 2, verdict: 'go-left',  caption: 'Step 1 — lo=0, hi=5. mid=2, a[2]=2 is NOT < 2. hi := 2.' },
  { lo: 0, hi: 2, mid: 1, verdict: 'go-left',  caption: 'Step 2 — lo=0, hi=2. mid=1, a[1]=2 is NOT < 2. hi := 1.' },
  { lo: 0, hi: 1, mid: 0, verdict: 'go-right', caption: 'Step 3 — lo=0, hi=1. mid=0, a[0]=1 IS < 2. lo := 1.' },
  { lo: 1, hi: 1, mid: 1, verdict: 'found',    caption: 'Step 4 — lo==hi==1. First index with a[i] >= 2 is index 1. Return 1.' }
]

const rotatedFrames = [
  { lo: 0, hi: 6, mid: 3, verdict: 'go-right', caption: 'Step 1 — a[mid=3]=7. Left half [4,5,6,7] is sorted (a[lo]=4 ≤ a[mid]=7). target=0 is not in [4, 7). Go right: lo := 4.' },
  { lo: 4, hi: 6, mid: 5, verdict: 'go-left',  caption: 'Step 2 — a[mid=5]=1. Left [a[4]=0 .. a[5]=1] is sorted (0 ≤ 1). target=0 IS in [0, 1). Go left: hi := 4.' },
  { lo: 4, hi: 4, mid: 4, verdict: 'found',    caption: 'Step 3 — mid=4, a[4]=0 == target. Return 4.' }
]

const peakFrames = [
  { lo: 0, hi: 3, mid: 1, verdict: 'go-right', caption: 'Step 1 — a[1]=2 < a[2]=3 (rising). lo := 2.' },
  { lo: 2, hi: 3, mid: 2, verdict: 'go-left',  caption: 'Step 2 — a[2]=3 > a[3]=1 (falling). hi := 2.' },
  { lo: 2, hi: 2, mid: 2, verdict: 'found',    caption: 'Step 3 — lo == hi == 2. a[2]=3 is a peak. Return 2.' }
]

const firstLastFrames = [
  { lo: 0, hi: 5, mid: 2, verdict: 'go-right', caption: 'Pass 1 (lower bound of 8). mid=2, a[2]=7 < 8. lo := 3.' },
  { lo: 3, hi: 5, mid: 4, verdict: 'go-left',  caption: 'mid=4, a[4]=8 NOT < 8. hi := 4.' },
  { lo: 3, hi: 3, mid: 3, verdict: 'found',    caption: 'lo == hi == 3. first = 3. Second pass finds lower bound of 9 at index 5; last = 4. Return [3, 4].' }
]

const trap1Bug = 'int mid = (lo + hi) / 2; computes 3.5·10⁹ which exceeds Integer.MAX_VALUE (2.1·10⁹), wraps to a negative number, and a[mid] throws ArrayIndexOutOfBoundsException. Every JDK Arrays.binarySearch had this bug for 9 years until Josh Bloch\'s 2006 fix. In an interview, writing (lo + hi) / 2 is a visible tell that you\'ve only ever used binary search on toy inputs.'
const trap1Fix = 'int mid = lo + (hi - lo) / 2;  — compute the half-distance first, then add to lo. Mathematically identical for positive lo, hi; immune to the overflow. Say the words "Bloch overflow fix" as you write it.'

const trap2Bug = 'You start writing the half-open template with while (lo < hi), then on the shrink branch write hi = mid - 1 (closed convention). Now when target lives at index mid, you have just thrown it away — the loop may still terminate but return the wrong index. Or symmetrically: closed-interval loop condition lo <= hi with hi = mid (half-open update). When lo == hi == mid you never shrink the interval; infinite loop.'
const trap2Fix = 'Pick ONE convention and let the loop condition dictate the update. Half-open: while (lo < hi) with hi = mid and lo = mid + 1. Closed: while (lo <= hi) with hi = mid - 1 and lo = mid + 1. The one-sentence rule: "if the mid IS a candidate answer, keep it; use hi = mid in the half-open template." Write it on scratch paper before you touch the loop.'

const trap3Bug = 'You start with the vanilla binary search and bolt on three if-conditions for rotation handling. The branches multiply (which half is sorted? is the target in it? what if mid IS the pivot?) and the invariant becomes undefined. Code compiles, passes 3 test cases, fails on [3, 1] or [1] or any single-pivot edge.'
const trap3Fix = 'Two options, both cleaner than one messy loop: (a) first find the pivot with a bitonic-style binary search, then plain-binary-search the correct half; two 10-line functions beat one 25-line tangle. (b) if you insist on one pass, write a[lo] <= a[mid] test FIRST, inside the loop, then handle "which half contains target" inside the sorted-half branch. Either way, state the invariant above the loop in English before writing the first if.'

const quizQuestions = [
  {
    q: 'For the half-open template with the invariant "every index less than lo satisfies P false; every index at or past hi satisfies P true," what update is correct when P(a[mid]) is TRUE?',
    choices: ['lo = mid + 1', 'hi = mid', 'hi = mid - 1', 'lo = mid'],
    correct: 1,
    why: 'When P is true at mid, the first true-index could BE mid or lie to its left — so we keep mid in the interval by setting hi = mid. Using hi = mid - 1 would discard mid even though it may be the answer.'
  },
  {
    q: 'Which problem does NOT reduce to this binary-search template?',
    choices: [
      'Find the smallest ship capacity to deliver within D days',
      'Find the index of a target in a sorted array',
      'Find the longest substring with at most K distinct characters',
      'Find a peak in a bitonic array'
    ],
    correct: 2,
    why: 'Longest-substring-with-K-distinct is sliding window — the window grows and shrinks per character and there is no monotone predicate on an index or an answer value. The other three admit a monotone boundary and reduce to lowerBound.'
  },
  {
    q: 'Why is int mid = (lo + hi) / 2 a bug?',
    choices: [
      'It rounds down for negative values',
      'For large lo and hi it overflows a 32-bit signed int and wraps negative',
      'It can produce the wrong parity when the array length is odd',
      'It makes the loop asymmetric and biases toward the left half'
    ],
    correct: 1,
    why: 'When lo + hi exceeds Integer.MAX_VALUE (about 2.1 × 10^9), the sum wraps negative and mid becomes a negative array index. The fix lo + (hi - lo) / 2 computes the gap first — immune to overflow for any positive lo, hi.'
  },
  {
    q: 'In the rotated-sorted-array search, you first check if a[lo] is at-most a[mid]. If TRUE, which half is sorted?',
    choices: ['Left half [lo..mid]', 'Right half [mid..hi]', 'Both halves', 'Neither half'],
    correct: 0,
    why: 'If a[lo] <= a[mid], the pivot (where the rotation happened) is NOT in the left half, so the left is monotonically non-decreasing. Then a standard range check on [a[lo], a[mid]] tells us if the target lives in that sorted half.'
  },
  {
    q: 'You wrote a half-open binary search and the loop never terminates. What is the most likely cause?',
    choices: [
      'The input array is not actually sorted',
      'You wrote hi = mid - 1 instead of hi = mid in the shrink branch',
      'You wrote lo = mid instead of lo = mid + 1 when the predicate is false',
      'The target is smaller than every array element'
    ],
    correct: 2,
    why: 'With while (lo < hi) and lo = mid, the case lo == mid == hi - 1 never shrinks the interval — lo stays, hi stays, mid stays — infinite loop. The correct half-open rule is lo = mid + 1 on the false branch, hi = mid on the true branch.'
  }
]
</script>

<PatternVideo pattern-name="Binary Search" duration="8–12 min" />

<PatternProgress pattern-id="binary-search" problems="binary-search-rotated-sorted, binary-search, find-minimum-in-rotated-sorted-array, find-peak-element, search-in-rotated-sorted-array-ii" />

<PatternSubVariationNav pattern="binary-search" />

<DueForReview />

## Why binary search exists — the story

You get an on-call ping at 3 AM: the payments service is misbehaving on a specific `order_id`. Your logs are sorted by `order_id`. There are **50 million rows**. You need to find one.

The honest first attempt is linear scan: read each row, compare, move on. It's a `while` loop and a print statement. Correct. And for a small file — say, the last hour's traffic, 100,000 rows — you're done in a second. That is the *reason* linear scan survived so long as an interview answer: it works, it's easy to prove correct, and for small n it's actually the fastest thing (branch predictors love it).

But at 50 million rows, linear scan takes about **half a second** — and 20 alerts fire in parallel while you wait. At 5 *billion* rows, you're waiting a minute. Every one of those comparisons is throwing away the fact that your logs are *sorted*: after checking row 500 and seeing `order_id = 42_000`, you've just proven every row before 500 has a smaller id. Ignoring that fact is what makes linear scan wasteful.

Binary search is the fix. Look at the *middle* row. If its `order_id` matches, you're done. If it's too big, the target must be in the left half — throw the right half away. Too small? Symmetric. Each step **halves** the search space, so 50 million rows collapse to `log₂(5·10⁷) ≈ 25` steps. **Half a second → 25 nanoseconds.** A 20-million-times speedup for four lines of code.

## The bare mechanic — simplest working example

Before any clever template, see the shape work on a trivial input. Six sorted integers, look up a value, return its index.

```java
int firstBinarySearch(int[] a, int target) {
    int lo = 0, hi = a.length;        // half-open [lo, hi): hi is PAST the last valid index
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2; // avoid overflow (see Trap 1 below)
        if (a[mid] < target) lo = mid + 1;   // target is strictly to the right
        else                 hi = mid;        // mid itself might be the answer; keep it
    }
    // lo == hi == first index i with a[i] >= target
    return (lo < a.length && a[lo] == target) ? lo : -1;
}
```

Trace it on `a = [1, 3, 5, 7, 9, 11]`, target `7`:

<BinarySearchStepStrip
  title="firstBinarySearch([1, 3, 5, 7, 9, 11], target = 7)"
  :input="[1, 3, 5, 7, 9, 11]"
  :target="7"
  :frames="bareMechFrames"
/>

That is the ground floor. **Every binary search in this chapter — rotated, bitonic, 2D, answer-space — is a specialization of this exact loop.** The template never changes. What changes is the *predicate* ("is `a[mid]` strictly less than the target?") and sometimes the search space ("is this answer feasible?"). Memorize this and the specializations become one-line diffs.

> [key] **Why `[lo, hi)` not `[lo, hi]`?** The half-open convention has one invariant and two update rules; the closed-interval convention has two invariants (one for `lo`, one for `hi`) and four update rules — twice the surface area for bugs. The JDK, C++ STL, Python's `bisect`, and Rust's `slice::partition_point` all converged on half-open for the same reason. If you only remember one template, let it be this one.

## When to use it — recognition signals

Binary search applies when your input has any of these shapes:

- **Sorted or monotonic data** — the classic. Sorted array, sorted list of files, sorted rows in a DB index.
- **Monotonic predicate on an unsorted-looking domain** — the "search on answer" pattern. If you can define `feasible(x)` that is `false` for `x < answer` and `true` for `x ≥ answer`, binary-search `x`. (That full topic has its own chapter: [BS on answer](/bs-on-answer).)
- **Rotated sorted array** — at least one half around `mid` is still sorted; detect which and shrink into it.
- **Boundary problems** — "first index with `a[i] ≥ target`" or "last index with `a[i] ≤ target`." These are *lower_bound* / *upper_bound* variants.
- **A function has a valley or peak** — bitonic arrays, unimodal functions. Compare `a[mid]` to `a[mid+1]` and shrink into the rising/falling side.
- **Constants that make O(log n) matter** — DB indexes, geometric algorithms with tight n·log n bounds, streaming median with sorted multiset.

If the problem statement contains *"sorted"*, *"monotonic"*, *"minimum X such that ..."*, or *"maximum X such that ..."*, binary search is your first hypothesis.

## THE template

One canonical loop. Every sub-variation below is a specialization of this exact shape.

<PatternTemplateCard
  slug="binary-search-canonical"
  title="Half-open [lo, hi) binary search"
  language="java"
  problem-shape="Find the smallest index i such that P(i) is true. If P never holds, lo == a.length."
  :code="canonicalCode"
  :invariant="canonicalInvariant"
  :complexity="canonicalComplexity"
  :specializations="canonicalSpecs"
/>

> [key] **What the predicate P is doing.** `P` partitions the index space into a `false` prefix and a `true` suffix. The loop finds the boundary. For plain lookup, `P(x) = (x >= target)`; the first index where P flips is where `target` would appear (lower bound). Every §Sub-variations H3 below differs ONLY in what `P` is.

## Sub-variations of the template

Five flavors, each a one-line diff from THE template above. Each sub-variation also carries a `<MarkSolved>` button so returning here from the [spaced-review schedule](/review) is one click.

### Lower / upper bound {#lower-upper-bound}

**Problem.** Given a sorted array (possibly with duplicates) and a target, return the first index where `a[i] ≥ target` (lower bound) or the first where `a[i] > target` (upper bound). Example: `a = [1, 2, 2, 2, 5]`, target `2`. Lower-bound returns 1 (first `≥ 2`). Upper-bound returns 4 (first `> 2`). Range `[1, 4)` is "all 2s."

**Template diff.** Only the predicate inside the `if` changes:

- Lower bound: `if (a[mid] < target)` ← strict less-than
- Upper bound: `if (a[mid] <= target)` ← less-than-or-equal
- Equality search: run lower bound, then check `a[lo] == target` at the end.

<TemplateReveal
  slug="binary-search/lower-upper-bound"
  language="java"
  problem-shape="First index with a[i] >= target (lower) or a[i] > target (upper)."
  :canonical="lowerUpperCode"
/>

<InvariantProof
  statement="All indices before lo have a[i] < target; all indices from hi onward have a[i] >= target. On exit lo == hi is the lower-bound boundary."
  initialization="At entry [lo, hi) = [0, n). The empty prefix [0, 0) vacuously satisfies 'all < target'; the suffix [n, n) vacuously satisfies 'all >= target'."
  maintenance="Each iteration either extends the 'all < target' prefix one past mid (when a[mid] < target), or extends the '>= target' suffix down to mid. The split moves but never crosses itself."
  termination="lo == hi means the two sides meet. The index lo is the first with a[i] >= target, or n if every element is less. Add one equality check at the end to upgrade this to exact-match search."
/>

<BinarySearchStepStrip
  title="lowerBound([1, 2, 2, 2, 5], target = 2) — returns 1"
  :input="[1, 2, 2, 2, 5]"
  :target="2"
  :frames="lowerBoundFrames"
/>

**Complexity.** O(log n) time, O(1) space.

**When to pick this variant.** Any "where would `x` fit in a sorted array" question. Range-count queries (`upper(hi) − lower(lo)`), insertion points, deduplication cursors, `java.util.TreeMap.floorKey/ceilingKey` under the hood.

<MarkSolved problem-slug="binary-search:lower-upper-bound" />

### Rotated sorted array {#rotated}

**Problem.** A sorted array of distinct integers was rotated at an unknown pivot — e.g., `[4, 5, 6, 7, 0, 1, 2]` originated from `[0..7]` rotated. Given a target, return its index or -1. Must be O(log n). [↗ LeetCode 33](https://leetcode.com/problems/search-in-rotated-sorted-array/).

**Template diff.** Keep the canonical loop. The predicate becomes "is the target in the sorted half that contains `mid`?" — one `if` chooses which half is sorted, a nested `if` chooses which side of `mid` to shrink into.

<TemplateReveal
  slug="binary-search/rotated"
  language="java"
  problem-shape="Find target in a rotated sorted array of distinct values. O(log n)."
  :canonical="rotatedCode"
/>

<InvariantProof
  statement="At every iteration, if target is in a, it lies in [lo, hi]. At least one of [lo..mid] and [mid..hi] is sorted (because the input is sorted everywhere except at one pivot)."
  initialization="At entry [lo, hi] = [0, n-1] covers the whole array. Whichever half of [0..mid] / [mid..n-1] does not contain the pivot is sorted — at least one always does."
  maintenance="The 'which half is sorted' check compares a[lo] to a[mid]. If a[lo] <= a[mid], the left half is sorted; otherwise the right. Inside the sorted half, standard range check (lo-value, hi-value) tells us if target is there; we shrink into it. The invariant 'target in [lo, hi]' is preserved on both branches."
  termination="hi - lo strictly decreases each iteration (either lo := mid+1 or hi := mid-1). When lo > hi the interval is empty and we return -1."
/>

<BinarySearchStepStrip
  title="searchRotated([4, 5, 6, 7, 0, 1, 2], target = 0) — returns 4"
  :input="[4, 5, 6, 7, 0, 1, 2]"
  :target="0"
  :frames="rotatedFrames"
/>

**Complexity.** O(log n) time, O(1) space.

**When to pick this variant.** Any variant of rotated / shifted sorted arrays. Also the mental template for "the array is sorted along ONE axis but you don't know which half" — comes up with ring buffers and log replay windows.

<MarkSolved problem-slug="binary-search:rotated" />

### Peak in bitonic array {#peak-bitonic}

**Problem.** Given an array where `a[i] != a[i+1]` for all i, find any peak (an index `i` with `a[i] > a[i-1]` and `a[i] > a[i+1]`; boundaries treated as -∞). Multiple peaks may exist; return any index in O(log n). [↗ LeetCode 162 Find Peak Element](https://leetcode.com/problems/find-peak-element/).

**Template diff.** Compare `a[mid]` to `a[mid+1]`. If rising, a peak lies in `[mid+1, hi]` (the sequence must come down eventually, since the right-end is -∞). If falling, a peak lies in `[lo, mid]`. The predicate is "is the sequence still rising at mid?"

<TemplateReveal
  slug="binary-search/peak-bitonic"
  language="java"
  problem-shape="Find any peak in an array of distinct consecutive values. O(log n)."
  :canonical="peakCode"
/>

<InvariantProof
  statement="A peak exists in the closed range [lo, hi] at every iteration."
  initialization="At entry [lo, hi] = [0, n-1]. The two boundary sentinels are -∞, so the max of the array (a peak) lies somewhere inside. The invariant holds trivially."
  maintenance="If a[mid] < a[mid+1] the function is rising at mid. Since the right boundary is -∞, the sequence must come back down past mid+1, so a peak lies in (mid, hi]. Set lo := mid+1. Otherwise a[mid] >= a[mid+1]: either mid is a peak or the function is falling, so a peak lies in [lo, mid]. Set hi := mid."
  termination="lo < hi guarantees mid+1 ≤ hi, so a[mid+1] is in bounds. Each branch shrinks hi - lo by at least 1. When lo == hi the invariant forces that single index to be a peak."
/>

<BinarySearchStepStrip
  title="findPeak([1, 2, 3, 1]) — returns 2"
  :input="[1, 2, 3, 1]"
  :target="'peak'"
  :frames="peakFrames"
/>

**Complexity.** O(log n) time, O(1) space.

**When to pick this variant.** Bitonic arrays, finding minimum in rotated sorted (dual — look for the inflection point). Also any unimodal function (max of a concave sequence, min of a convex sequence) when you can evaluate `f(mid)` and `f(mid+1)`.

<MarkSolved problem-slug="binary-search:peak-bitonic" />

### Search 2D matrix {#2d-matrix}

**Problem.** An `m × n` matrix is sorted row-major: every row is sorted left-to-right, AND the first element of each row is greater than the last of the previous row. Search for a target in O(log(mn)). [↗ LeetCode 74](https://leetcode.com/problems/search-a-2d-matrix/).

**Template diff.** Treat the matrix as a flat sorted array of length `m·n`. The flat index `k` maps to `(k / n, k % n)`. Everything else is the canonical loop.

<TemplateReveal
  slug="binary-search/2d-matrix"
  language="java"
  problem-shape="Search target in a row-major-sorted m×n matrix. O(log(mn))."
  :canonical="matrixCode"
/>

<InvariantProof
  statement="If target is in the matrix, its flat index lies in [lo, hi). Row-major sortedness guarantees the flat sequence is sorted."
  initialization="[lo, hi) = [0, m*n). Covers every (row, col) cell exactly once."
  maintenance="v := mat[mid/n][mid%n] reads the k-th cell in row-major order. Because the row's end is strictly less than the next row's start, the flattened sequence is sorted; the standard lower-bound shrink works unchanged."
  termination="hi - lo strictly decreases. On exit lo is the lower bound in the flat sequence; one equality check finishes."
/>

**Complexity.** O(log(m·n)) time, O(1) space. Note this is identical to O(log m + log n) for standard sizes, but one unified loop is cleaner than nested searches.

**When to pick this variant.** Fully-sorted matrices. For the *staircase*-sorted case (rows and columns sorted independently, like LeetCode 240), binary search doesn't give log — use the top-right walk in O(m + n) instead.

<MarkSolved problem-slug="binary-search:2d-matrix" />

### First and last position {#first-last-position}

**Problem.** Sorted array with duplicates, find the leftmost and rightmost indices of a target. Return `[-1, -1]` if absent. [↗ LeetCode 34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/).

**Template diff.** Two calls: `lowerBound(target)` for the leftmost index, `lowerBound(target + 1) - 1` for the rightmost. (That second form, "lower bound of `target+1` then minus one," is the trick that keeps the code symmetric.)

<TemplateReveal
  slug="binary-search/first-last-position"
  language="java"
  problem-shape="Return [first, last] indices of target in a sorted array with duplicates."
  :canonical="firstLastCode"
/>

<InvariantProof
  statement="searchRange returns [first, last] such that a[first..last] contains exactly the occurrences of target."
  initialization="lowerBound(target) finds the first index with a[i] >= target; if that element is not target, no occurrence exists."
  maintenance="lowerBound(target + 1) finds the first index with a[i] >= target + 1. Everything before it with value target is a target cell. Subtract 1 to get the last target index."
  termination="Both lowerBound calls terminate in O(log n). Final arithmetic is O(1)."
/>

<BinarySearchStepStrip
  title="searchRange([5, 7, 7, 8, 8, 10], target = 8) — returns [3, 4]"
  :input="[5, 7, 7, 8, 8, 10]"
  :target="8"
  :frames="firstLastFrames"
/>

**Complexity.** 2 × O(log n) = O(log n) time, O(1) space.

**When to pick this variant.** Any "count how many" or "range of equal values" problem. Count-of-X with `upper(X) − lower(X)`. Deduplication cursors. Streaming histogram bucket boundaries.

<MarkSolved problem-slug="binary-search:first-last-position" />

## Traps & gotchas

Three traps show up in interviews often enough to deserve walked-through bug/fix pairs. Two more live as callouts.

<TrapTrace
  title="Trap 1 — mid overflow with (lo + hi) / 2"
  input="lo = 1_500_000_000, hi = 2_000_000_000"
  :bug="trap1Bug"
  :fix="trap1Fix"
/>

<TrapTrace
  title="Trap 2 — mixing comparison operators between templates"
  input="half-open condition with closed-convention update (or vice versa)"
  :bug="trap2Bug"
  :fix="trap2Fix"
/>

<TrapTrace
  title="Trap 3 — rotated-array template contamination"
  input="searchRotated with the plain binary-search template as a starting point"
  :bug="trap3Bug"
  :fix="trap3Fix"
/>

> [trap] **Trap 4 — Off-by-one on the return.** After the loop exits, is `lo` the answer, `lo - 1`, or `-1`? The invariant tells you. **Interview move:** write a comment above the `return` stating what `lo` means in your invariant language. If you cannot name it, your loop is wrong.

> [trap] **Trap 5 — Floating-point without an iteration cap.** `while (hi - lo > 1e-9)` can loop forever on inputs where floating-point precision stops halving. Bound by `for (int iter = 0; iter < 100; iter++)` as well; 100 iterations halves the interval by `2^100 ≈ 10^30` — orders of magnitude more precision than any real problem needs.

## History

Binary search was first formally described by **John Mauchly in 1946**, one of the earliest algorithms to receive formal analysis. Yet in 2006, Josh Bloch published *"Nearly All Binary Searches and Mergesorts are Broken"* on the Google Research blog, revealing that essentially every JDK implementation (Java 1.0 through Java 5) contained the `mid = (lo + hi) / 2` overflow bug — for arrays larger than about a billion elements, the answer was wrong. Bloch had co-authored *Effective Java*; he found the bug while reading the code of his own book's `Arrays.binarySearch`. His takeaway: *"even careful programmers make horrible mistakes."* Mention this in an interview and the seasoned interviewer smiles — you've just signaled that you know binary search is deceptively simple and dangerously bug-prone.

Nimrod Megiddo formalized the full technique family — including search-on-answer — in 1979 as **parametric search**. His paper on optimization by binary-searching the answer space became the template for a generation of geometric algorithms (nearest-neighbor, minimum-enclosing-circle).

### In the wild

OpenJDK 21's `java.util.Arrays.binarySearch(int[], int)` is a near-canonical half-open loop with the Bloch overflow fix:

```java
// java.base/java/util/Arrays.java (openjdk-21, lightly condensed)
public static int binarySearch(int[] a, int key) {
    int low = 0;
    int high = a.length - 1;             // closed convention here
    while (low <= high) {
        int mid = (low + high) >>> 1;    // >>> instead of / 2 — unsigned shift,
                                         // also overflow-safe for positive low+high
        int midVal = a[mid];
        if      (midVal < key) low  = mid + 1;
        else if (midVal > key) high = mid - 1;
        else                   return mid;         // key found
    }
    return -(low + 1);                   // key not found; -(insertion point) - 1
}
```

Two choices worth noting. The JDK uses the **closed-interval** convention (we chose half-open above) — both are fine, same complexity. And it returns `-(insertionPoint + 1)` on a miss instead of `-1`, so a caller gets the insertion point *and* the found/not-found signal in one return value. The `>>> 1` is the Bloch fix in its most compact form — unsigned right shift divides by 2 without the sign-bit overflow.

Source: [openjdk/jdk `src/java.base/share/classes/java/util/Arrays.java`](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/Arrays.java). Every half-decent language stdlib has an equivalent — Python `bisect`, C++ `std::lower_bound`, Rust `slice::binary_search`, Go `sort.Search` — all converge on the same template with cosmetic differences.

## Interactive diagram

<BinarySearchAnim />

The animation shows the half-open loop on a sorted array. Watch the `[lo, hi)` window shrink; note that at every step the candidate answer (if any) lies inside the yellow range. Try: a value in the array (watch it converge in `log₂ n` steps), a value smaller than all elements (lo stays at 0, hi walks down to 0), a value larger than all (lo walks up to n). The three cases cover the full behavior.

## When NOT to use it

You've now worked through the half-open loop in all its common shapes. Here's where it silently fails — the three structural failure modes beneath the six bullets.

- **Unsorted data with no monotonic predicate** — sorting to enable binary search costs O(n log n), worse than O(n) hash-map lookup. Only sort-then-search if you'll do many queries.
- **You need every match, not the first** — plain iteration, or `lower_bound` + `upper_bound`, is simpler.
- **The array is small (`n ≤ 32`)** — linear scan wins in practice: branch predictor loves it, cache-friendly, `log₂ 32 = 5` comparisons plus overhead loses to a straight loop.
- **Duplicates and you want *all* occurrences** — do lower-bound + linear expansion, or two binary searches (lower + upper). Don't hack it inside one loop.
- **Non-monotone feasibility** — e.g., "smallest `x` such that some bitonic metric is minimized." Binary search silently returns the wrong answer; verify monotonicity on paper first.
- **Floating-point ranges without a stopping criterion** — the loop never terminates. Fix an ε tolerance or an iteration cap.

### Visual 1: non-monotone feasibility on a bitonic array `[1, 3, 7, 5, 2]`, target 5

A plain binary search on this array for value 5 silently commits to one half and returns "not found":

```text
   idx    0    1    2    3    4
   val    1    3    7    5    2
                                                        found?
   [lo=0, hi=5)  mid=2  arr[2]=7  7 > 5  → go left     no
   [lo=0, hi=2)  mid=1  arr[1]=3  3 < 5  → go right    no
   [lo=2, hi=2)                   loop ends            no (returns -1)
```

The real answer sits at index 3. Binary search *assumes* that `arr[mid] > target` means "the match must be to the left" — true only if the array is monotone. On a bitonic array that assumption holds for the ascending half and fails for the descending half, so the search commits to the wrong direction and never recovers. The fix: either run two binary searches (one per monotone region, after finding the peak via another binary search) or just scan linearly for n < 100.

### Visual 2: floating-point without a stopping criterion on `sqrt(2)`

A naive `while (lo < hi)` on floats never terminates because real numbers aren't representable exactly:

```text
   target: sqrt(2) ≈ 1.4142135623730951

   Iteration     lo                  hi                  mid
   0             1.0000000000000000  2.0000000000000000  1.5000000000000000
   1             1.0000000000000000  1.5000000000000000  1.2500000000000000
   2             1.2500000000000000  1.5000000000000000  1.3750000000000000
   …             …                   …                   …
   52            1.4142135623730949  1.4142135623730951  1.4142135623730951
   53            1.4142135623730949  1.4142135623730951  1.4142135623730951  ← SAME mid, hi doesn't shrink
   54            1.4142135623730949  1.4142135623730951  1.4142135623730951
   …
```

Beyond ~52 iterations the subdivision step drops below one ULP (unit in the last place), so `(lo+hi)/2` floors to one of the endpoints — the interval stops shrinking and the loop runs forever. The fix: pick a tolerance (`while (hi - lo > 1e-9)`) OR cap iterations at 100 (double precision has ~52 bits of mantissa; 100 is comfortably past convergence).

### Visual 3: small `n` where linear scan wins

For `n ≤ 32`, branch misprediction + cache lines + loop overhead make a straight scan beat `log₂ n` with constants:

```text
   Linear scan on n=16:                     Binary search on n=16:
   16 compares                              log₂ 16 = 4 compares
   16 sequential loads (prefetch friendly)  4 random-access loads (jump around)
   ~1 branch per compare, mostly correct    4 branches, half mispredicted on average
   total: 16 × 1 ns ≈ 16 ns                 total: 4 × ~6 ns ≈ 24 ns
                                            (branch miss + cache line change per step)
```

The crossover for sorted integers in L1 cache is around n=64 on modern CPUs. Below that, `log n` is "theoretically faster" but practically slower because the hidden constant is a branch mispredict, not an array compare. The fix: use linear scan for `n < 32`, binary search for larger; the standard library's `std::lower_bound` does something similar under the hood.

## Recognition drill

Reading the chapter trains comprehension. Drilling recognition trains the thing an interviewer actually tests: given a cold problem with no pattern tag, can you spot that it reduces to a half-open loop?

<RecognitionDrill pattern="binary-search" :count="10" />

Then come back to [the mixed drill](/mixed-drill) once you've worked a few other chapters — mixed is where interleaved recognition becomes a reflex instead of a chapter-local skill.

## Advanced — follow-ups and failure modes

Five interview "what if…" follow-ups and a breaking point. If you can answer these cold, you have mastered binary search as a tool, not just as a template.

### What if the sorted array has duplicates and we must find the FIRST occurrence?

Use `lowerBound(target)`, then verify `a[lo] == target`. Do NOT try to make the vanilla equality-check loop return the first; it'll return any occurrence. The lower-bound predicate `a[mid] < target` (strict less-than) is the key — on an equality match it still shrinks hi down to mid, never resting on a later occurrence.

### What if the predicate is "is this `k` feasible?" and feasibility is monotone?

That's the entire [binary search on the answer](/bs-on-answer) chapter. The template above is unchanged; only the search space changes from array indices to the answer range `[lo, hi]`, and `a[mid] < target` becomes `!feasible(mid)`. Classic examples: minimum eating speed (Koko), minimum capacity to ship, split array largest sum. If you've mastered this chapter, you've already mastered 80% of that one.

### What if the array is on disk and random access costs 10ms?

Pure binary search still works (25 disk reads for `n = 10^7`, well under a second), but you can do better by exploiting the fact that distant reads are no more expensive than near reads: **interpolation search** probes at a position *proportional to the target's value* in `[a[lo], a[hi]]`, not at the midpoint. On uniformly-distributed data it drops to `log(log n)` reads — ~4-5 instead of 25. On adversarial data (geometric distribution), it degrades to O(n), so pair it with a plain-binary-search fallback after a few bad iterations.

### What if the sorted sequence is coming in through a stream and you can only random-access the last N elements?

Binary search is impossible on a stream — you can't rewind. Switch to a `TreeMap` (RB-tree) that supports `ceilingKey` / `floorKey` in O(log n) with incremental insertion. Or if the stream is huge and the query is "top-K", switch to a bounded heap. Pattern recognition: streaming + sorted + boundary query → BBST or bounded heap, not binary search.

### What if the array is nearly-sorted (bounded disorder of ±k)?

Plain binary search is wrong — the target you expect at index `i` might be at `i ± k`. Two fixes: (a) check `[i-k, i+k]` linearly after the binary search lands, giving O(log n + k) — fine if `k` is small; (b) if `k` is comparable to `n`, give up on sort-order assumptions and use hashing.

### Breaking point: when the "feasibility" predicate is NOT monotone

Binary search silently returns the wrong answer on a non-monotone predicate — the loop still terminates, but the invariant doesn't hold, so the final `lo` has no meaning. **Verification before you code:** compute `feasible(lo)` and `feasible(hi)` and sanity-check: one must be true and one false. If both agree, you have a boundary problem (not a feasibility problem). If feasibility flips back and forth, binary search doesn't apply at all; switch to a linear scan or (if the function is unimodal) ternary search.

### Cross-pattern problems

- **Median of Two Sorted Arrays** ([↗ LeetCode 4](https://leetcode.com/problems/median-of-two-sorted-arrays/)). O(log(min(m, n))) via binary search on the partition index — one of the hardest classical results you'll see in interviews. The predicate: "do these two partitions produce left-max ≤ right-min?" This is binary search where the "array" being searched is the partition cursor, not element values. Pattern mix: binary search + two-pointer thinking.
- **Capacity to Ship Packages Within D Days** ([↗ LeetCode 1011](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)). Binary search over the answer space `[max(weight), sum(weights)]` with feasibility = "can we ship in ≤ D days at this capacity?" Full write-up in [BS on answer](/bs-on-answer). Recognition drill: when the problem says "minimum X such that Y holds" and Y is checkable in O(n), the predicate is monotone and this template applies.
- **Count of Range Sum** ([↗ LeetCode 327](https://leetcode.com/problems/count-of-range-sum/)). O(n log n) via merge sort + binary search inside the merge step: for each prefix sum, binary-search the window of valid partners. Pattern mix: binary search + divide-and-conquer. The binary search here is `lowerBound` / `upperBound` on a sorted buffer during the merge.

## Related patterns + Check your understanding

<RelatedPatterns pattern-id="binary-search" />

<Quiz pattern-id="binary-search" :questions="quizQuestions" />

<PrintButton />
