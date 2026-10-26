# Divide &amp; Conquer


<PatternVideo pattern-name="Divide & Conquer" duration="8–12 min" />

<PatternProgress pattern-id="divide-conquer" problems="inversions, count-of-range-sum, reverse-pairs, global-and-local-inversions, sort-list, pow-x-n, majority-element" />

<script setup>
const bareTemplateCode = `# python — generic D&C skeleton
def solve(a, lo, hi, scratch):
    if hi - lo <= 1:
        return base_result(a, lo, hi)         # size-0 or size-1 base case
    mid = (lo + hi) // 2
    left  = solve(a, lo, mid, scratch)
    right = solve(a, mid, hi, scratch)
    return combine(a, lo, mid, hi, left, right, scratch)`

const bareInvariant = {
  statement: `After \`solve(a, lo, hi, scratch)\` returns, (a) \`a[lo:hi]\` carries the postcondition the combine step requires (sorted order, best prefix-sum, closest-pair distance, etc.), and (b) the returned object fully describes that range for the parent's combine step.`,
  initialization: `When \`hi - lo <= 1\`, the range is size 0 or 1 — the base case returns the trivially correct answer. For merge sort, a single element is already sorted; for max subarray, a single element is its own best prefix/suffix/sum.`,
  maintenance: `Each recursive call establishes the postcondition on its half. The combine step uses both halves' postconditions and performs O(f(n)) work on the current range to produce the parent's postcondition. If both halves are correctly solved and combine is correctly defined, the parent is too.`,
  termination: `Each call reduces \`hi - lo\` by roughly half (b = 2 for most variants), so depth is \`log_b n\`. Base case triggers at every leaf; the tree has finite depth; recursion terminates. Total cost by the Master Theorem is determined by (\`a\`, \`b\`, \`f(n)\`).`
}

const bareComplexity = {
  time: `O(f(n) · log_b n) when a = b (merge sort: O(n log n)); more generally decided by the Master Theorem on \`T(n) = a·T(n/b) + f(n)\`.`,
  space: `O(n) scratch + O(log n) recursion stack for merge sort; variants vary.`
}

const templateSpecializations = [
  { slug: `merge-sort-medium`, title: `Merge Sort` },
  { slug: `pow-x-n-medium`, title: `Pow(x, n)` },
  { slug: `count-of-smaller-numbers-after-self-hard`, title: `Count Smaller After Self` },
  { slug: `majority-element-easy`, title: `Majority Element` }
]

const mergeSortCode = `# python — in-place merge sort with reusable scratch
def merge_sort(a):
    scratch = [0] * len(a)
    _ms(a, 0, len(a), scratch)
def _ms(a, lo, hi, scratch):
    if hi - lo <= 1: return
    mid = (lo + hi) // 2
    _ms(a, lo, mid, scratch)
    _ms(a, mid, hi, scratch)
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if a[i] <= a[j]:            # stable: left wins on ties
            scratch[k] = a[i]; i += 1
        else:
            scratch[k] = a[j]; j += 1
        k += 1
    while i < mid: scratch[k] = a[i]; i += 1; k += 1
    while j < hi:  scratch[k] = a[j]; j += 1; k += 1
    a[lo:hi] = scratch[lo:hi]`

const mergeSortInvariant = {
  statement: `After \`_ms(a, lo, hi, scratch)\`, the subarray \`a[lo:hi]\` is sorted ascending and contains the same multiset of values as before the call.`,
  initialization: `When \`hi - lo <= 1\` the range is trivially sorted and the multiset is preserved — nothing is written.`,
  maintenance: `Each recursive call sorts its half (invariant holds inductively). The merge step reads two sorted halves and writes to \`scratch[lo:hi]\` in sorted order (two-pointer merge with left-takes-tie preserves stability and sortedness). The final copy-back preserves the multiset and the sort order.`,
  termination: `All recursion returns; the top call sorts \`a[0:n]\`. Depth is \`log n\`; each level does O(n) work; total O(n log n).`
}

const powCode = `# python — binary exponentiation (fast power)
def my_pow(x, n):
    if n < 0:
        x, n = 1 / x, -n
    result = 1.0
    while n > 0:
        if n & 1:                    # odd bit → multiply current x into result
            result *= x
        x *= x                       # square the base
        n >>= 1                      # shift to the next bit
    return result`

const powInvariant = {
  statement: `At each iteration, the loop maintains \`result * x^n == x_initial^n_initial\`.`,
  initialization: `Before the loop, \`result = 1\`, \`x = x_initial\`, \`n = n_initial\` (after sign-flip). So \`1 * x_initial^n_initial == x_initial^n_initial\`.`,
  maintenance: `When n is odd: we multiply \`result\` by \`x\` and squeeze one factor of \`x\` out of the exponent — then \`n & 1\` effectively becomes zero because we'll \`n >>= 1\`. The product \`result * x^n\` is unchanged after accounting for the squaring. When we square \`x\` and right-shift \`n\`, \`x^n\` becomes \`(x^2)^(n>>1)\` which equals the original \`x^n\` for even \`n\` (and we've already extracted the odd bit).`,
  termination: `When \`n\` reaches 0, \`x^0 = 1\` so \`result * 1 = result = x_initial^n_initial\`. The loop runs \`O(log n)\` times because each iteration halves \`n\`.`
}

const countSmallerCode = `# python — merge sort with per-index "right-smaller" counting
def countSmaller(nums):
    n = len(nums)
    result = [0] * n
    indices = list(range(n))
    scratch = [0] * n
    def ms(lo, hi):
        if hi - lo <= 1: return
        mid = (lo + hi) // 2
        ms(lo, mid)
        ms(mid, hi)
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            if nums[indices[i]] <= nums[indices[j]]:
                # for indices[i], (j - mid) right-half elements have already
                # been placed BEFORE it — each was strictly smaller
                result[indices[i]] += (j - mid)
                scratch[k] = indices[i]; i += 1
            else:
                scratch[k] = indices[j]; j += 1
            k += 1
        while i < mid:
            result[indices[i]] += (j - mid)
            scratch[k] = indices[i]; i += 1; k += 1
        while j < hi:
            scratch[k] = indices[j]; j += 1; k += 1
        indices[lo:hi] = scratch[lo:hi]
    ms(0, n)
    return result`

const countSmallerInvariant = {
  statement: `After \`ms(lo, hi)\` returns, \`indices[lo:hi]\` is sorted by \`nums[]\` value, and for every original index \`idx\` originally inside \`[lo, hi)\`, \`result[idx]\` is incremented by exactly the number of smaller elements that were originally to its right within \`[lo, hi)\`.`,
  initialization: `A size-1 range is trivially sorted and has no right-of-self elements; result stays 0.`,
  maintenance: `By induction, left-half sort and counting is correct; right-half same. The merge step then handles cross pairs: when we move left \`indices[i]\` into position, \`(j - mid)\` right-half elements with original index > \`indices[i]\` (they were on the right) and smaller value (they were placed before this left element) are *strictly smaller elements to the right of indices[i]* — add that to \`result[indices[i]]\`. Combined with the recursive counts, this gives the exact right-smaller count for every original index in \`[lo, hi)\`.`,
  termination: `All recursion returns; the top call has processed every original pair \`(i, j)\` where \`i < j\` as either a within-half pair (counted recursively) or a cross-boundary pair (counted during merge).`
}

const majorityCode = `# python — Boyer-Moore via divide and conquer
def majorityElement(nums):
    def helper(lo, hi):
        if hi - lo == 1:
            return nums[lo]
        mid = (lo + hi) // 2
        left  = helper(lo, mid)
        right = helper(mid, hi)
        if left == right:
            return left
        # count each in [lo, hi) and return the one with higher count
        lc = sum(1 for x in nums[lo:hi] if x == left)
        rc = sum(1 for x in nums[lo:hi] if x == right)
        return left if lc > rc else right
    return helper(0, len(nums))`

const majorityInvariant = {
  statement: `Claim: in any array where some value \`m\` appears > n/2 times, \`m\` must be the majority element in at least one half when the array is split in half.`,
  initialization: `Size-1 range: the single element is trivially the majority.`,
  maintenance: `Suppose \`m\` appears > n/2 times in \`[lo, hi)\` of length \`n\`. If \`m\` is NOT majority in the left half (appearing ≤ \`n_l/2\` times there) AND NOT majority in the right half (appearing ≤ \`n_r/2\` times there), then total \`m\` count is ≤ \`n_l/2 + n_r/2 = n/2\` — contradiction. So \`m\` is majority of at least one half. The algorithm returns the two half-candidates and resolves by counting; the true \`m\` is one of them.`,
  termination: `Recursion depth \`log n\`; combine step is O(n); total O(n log n). Space O(log n) stack. This is slower than Boyer-Moore's O(n) linear pass but shows the D&C framing.`
}

const trapAcode = {
  statement: `Treating D&C as a synonym for recursion.`,
  bug: `Writing \`fib(n) = fib(n-1) + fib(n-2)\` and calling it D&C is wrong. The subproblems are NOT independent (\`fib(n-2)\` is used by \`fib(n-1)\` too), so there's no clean split-and-combine. Interviewers who hear "divide and conquer" expect balanced splits with independent subproblems; naming the pattern wrong undercuts your explanation.`,
  fix: `D&C specifically means: split into roughly equal halves → solve halves independently → combine. If subproblems overlap or depend on each other, you have recursion with memoization (DP), not D&C. Fibonacci, DFS, and tree traversal are recursion but not D&C.`
}

const trapBcode = {
  statement: `Copying subarrays instead of passing indices.`,
  bug: `\`def ms(a): if len(a)<=1: return a; return merge(ms(a[:mid]), ms(a[mid:]))\` creates \`O(n log n)\` new arrays with \`O(n log n)\` total allocation — far worse than the O(n log n) comparison count. GC thrashes; actual wall-clock is 3-5x slower than the in-place version.`,
  fix: `Pass \`lo, hi\` indices and a pre-allocated scratch buffer. Allocate scratch ONCE outside the recursion; reuse at every level. For languages without GC (Rust, C++), this is also safer — no accidental copies.`
}

const trapCcode = {
  statement: `Combine step accidentally doing O(n log n) or O(n²), breaking the Master Theorem optimum.`,
  bug: `If combine does \`sorted(a[lo:hi])\` on each call, the recurrence becomes \`T(n) = 2T(n/2) + O(n log n)\` → O(n log² n), not O(n log n). More subtly: comparing every left element to every right element during combine gives \`T(n) = 2T(n/2) + O(n²) = O(n²)\` — same as brute force; D&C bought you nothing.`,
  fix: `Combine should be strictly O(n) (or O(n log k) if that's where cleverness lives). Design the "returned structure" so cross-boundary work is linear: sorted order, prefix/suffix sums, bounding boxes, closest-pair distance. If combine seems to need O(n log n), the structure is wrong.`
}

const quizQuestions = [
  {q: "Merge sort merges two halves in O(n). Total complexity?", choices: [{text: "O(n log n)", correct: true, explanation: "By Master Theorem: T(n) = 2T(n/2) + O(n)."}, {text: "O(n²)", correct: false}, {text: "O(log n)", correct: false}, {text: "O(n)", correct: false}]},
  {q: "For Count Inversions during merge sort, when is the count added?", choices: [{text: "When taking from the right half: add (leftRemaining) to the count", correct: true, explanation: "Each such take crosses `leftRemaining` inversions."}, {text: "At start of merge", correct: false}, {text: "At end of merge", correct: false, explanation: "Batch-counting works too but the per-take is standard."}, {text: "Never — count separately", correct: false}]},
  {q: "For Pow(x, n) by binary exponentiation, what's the key invariant maintained each loop iteration?", choices: [{text: "result * x^n equals the original x^n (reinterpreted as x grows and n shrinks)", correct: true, explanation: "Odd-bit extraction into result, square x, right-shift n — all preserve the product."}, {text: "x stays constant", correct: false, explanation: "x squares every iteration."}, {text: "n stays positive", correct: false, explanation: "True but not the point."}, {text: "result stays 1", correct: false}]},
  {q: "The D&C Majority Element solution is O(n log n). Boyer-Moore's linear-scan version is O(n). Why learn the D&C variant?", choices: [{text: "It teaches the general pattern 'majority must survive in at least one half' which generalizes to other problems", correct: true, explanation: "The structural insight is reusable across problems; the linear Boyer-Moore specializes a particular case."}, {text: "D&C is always faster", correct: false, explanation: "Here it's slower."}, {text: "Boyer-Moore is wrong", correct: false, explanation: "It's correct."}, {text: "D&C uses less memory", correct: false, explanation: "More stack."}]},
  {q: "When would you NOT use divide & conquer?", choices: [{text: "When the subproblems aren't independent (need shared state)", correct: true, explanation: "Then DP or shared-memoization is better."}, {text: "When n is large", correct: false, explanation: "D&C shines for large n."}, {text: "When recursion is banned", correct: false, explanation: "You can iterate; possible but ugly."}, {text: "Never — always use D&C", correct: false}]}
]

const mergeSortSolvePrompt = `Sort an array of n integers in O(n log n) worst case using merge sort — stable, with O(n) auxiliary space.`

const powSolvePrompt = `Implement \`pow(x, n)\` for real \`x\` and integer \`n\` (positive or negative) in O(log |n|) multiplications.`

const countSmallerSolvePrompt = `For each element, return how many elements to its right are strictly smaller. Example: \`[5,2,6,1]\` → \`[2,1,1,0]\`.`

const majoritySolvePrompt = `Given an array where some element appears more than n/2 times, return that element. Use divide and conquer (not Boyer-Moore).`
</script>

## Why divide and conquer exists — the story

You're a game engine developer at Riot. Every frame you must sort the visible entities by depth to correctly render transparent water effects. **50,000 entities. 60 frames per second. That's 3 million sorts per second per player.**

The obvious approach: bubble sort, insertion sort, or any O(n²) sort. For 50,000 entities that's `2.5·10⁹` comparisons per frame — **40 seconds per frame** on a modern CPU. Frame budget is 16 milliseconds. You are **2,500× over budget.** Water flickers, players uninstall.

You could try to be clever with domain tricks: bucket the entities by depth ranges, sort each bucket. But entities are moving; buckets constantly rebalance. You could try to sort incrementally frame-over-frame, but a single teleport ruins the assumption.

The right answer is a **general-purpose O(n log n) sort** — and the one used by every game engine, JVM, and database on Earth is **merge sort** (or a hybrid like Timsort). The insight is: sort of `[5, 2, 6, 1]` is hard. Sort of `[5, 2]` is easy. Sort of `[6, 1]` is easy. Once both halves are sorted, **merging** them in one linear pass produces the final sorted result. `T(n) = 2·T(n/2) + O(n) = O(n log n)`. For 50,000 entities: `50,000 · log₂(50,000) ≈ 800,000` comparisons per frame — **50,000× faster than bubble sort**. Frame budget met. Water renders correctly.

That's **divide and conquer**: split the input, solve each half recursively, then combine. The split is the easy part; the *combine* is where the cleverness lives. Merge sort combines by merging two sorted halves. Quicksort combines by picking a pivot and letting the recursion handle everything. Fast Fourier Transform combines by "twisting" two half-spectra with roots of unity. Karatsuba's multiplication combines by reusing three product results instead of four. Every one is the same shape: **T(n) = a·T(n/b) + f(n)**.

> [key] **Key Insight — the Master Theorem gives the total cost from `T(n) = a·T(n/b) + f(n)`.** For merge sort: `a=2, b=2, f(n)=O(n)` → O(n log n). For binary search: `a=1, b=2, f(n)=O(1)` → O(log n). For Strassen matrix mult: `a=7, b=2, f(n)=O(n²)` → O(n^{log₂7}) ≈ O(n^2.81). **Say the phrase "Master Theorem" out loud in an interview when justifying complexity — it signals recursion literacy.**

## The bare mechanic — simplest working example

Divide `[5,2,6,1]` into `[5,2]` and `[6,1]`. Sort each recursively — size-1 is trivially sorted, then merge pairs. Finally merge `[2,5]` with `[1,6]` to get `[1,2,5,6]`.

| level | halves | combine | output |
|---|---|---|---|
| 2 (leaves) | `[5], [2]` and `[6], [1]` | merge pairs | `[2,5]`, `[1,6]` |
| 1 | `[2,5], [1,6]` | merge sorted halves | `[1,2,5,6]` |
| 0 (root) | — | — | `[1,2,5,6]` |

Each level does O(n) total merge work; there are `log₂ n` levels; total O(n log n).

```svg
<svg role="img" width="400" height="200" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="merge sort recursion tree">
  <rect x="0" y="0" width="400" height="200" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">split down, combine up</text>
  <g stroke="var(--dsa-neutral)" stroke-width="1.4">
    <line x1="200" y1="46" x2="130" y2="80"/><line x1="200" y1="46" x2="270" y2="80"/>
    <line x1="130" y1="100" x2="90" y2="130"/><line x1="130" y1="100" x2="170" y2="130"/>
    <line x1="270" y1="100" x2="230" y2="130"/><line x1="270" y1="100" x2="310" y2="130"/>
  </g>
  <g text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">
    <rect x="150" y="30" width="100" height="26" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/><text x="200" y="48">[5,2,6,1]</text>
    <rect x="90" y="80" width="80" height="24" rx="6" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/><text x="130" y="97">[5,2]</text>
    <rect x="230" y="80" width="80" height="24" rx="6" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/><text x="270" y="97">[6,1]</text>
    <rect x="70" y="130" width="40" height="24" rx="6" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="90" y="147">[5]</text>
    <rect x="150" y="130" width="40" height="24" rx="6" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="170" y="147">[2]</text>
    <rect x="210" y="130" width="40" height="24" rx="6" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="230" y="147">[6]</text>
    <rect x="290" y="130" width="40" height="24" rx="6" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="310" y="147">[1]</text>
  </g>
  <text x="200" y="185" text-anchor="middle" font-size="10" font-style="italic" fill="var(--dsa-neutral)">height = log₂ n · each level merges all n elements · total O(n log n)</text>
</svg>
```

<PatternTemplateCard
  slug="dc-bare"
  language="python"
  :code="bareTemplateCode"
  :invariant="bareInvariant"
  :complexity="bareComplexity"
  problemShape="split array into halves → solve independently → combine with a cheap O(n) step"
  defaultRevealed />

## When to use it — recognition signals

- "solve the halves, combine" — merge sort family.
- "count inversions" / "count of smaller after self" / "reverse pairs".
- "cross-boundary pairs" where left-half and right-half relationships matter.
- "closest pair of points", "maximum subarray via D&C" (Kadane's O(n) beats it but D&C teaches the shape).
- "x^n in O(log n)", "a mod b^e" via binary exponentiation.
- constraints around `10^5` where O(n²) pair checking is too slow but O(n log n) fits.
- input can be split into independent subproblems after you define the right combine information.

## History — von Neumann 1945, Karatsuba 1962, Strassen 1969

**John von Neumann** wrote the first published divide-and-conquer algorithm in **1945**: merge sort, in his *"First Draft of a Report on the EDVAC."* He described splitting an array in half, sorting each half, and merging — every element of the pattern was there. Von Neumann was designing algorithms for a computer that didn't exist yet (EDVAC wouldn't run until 1949), so merge sort predates its own hardware by 4 years.

**Anatoly Karatsuba** applied divide-and-conquer to integer multiplication in **1962**. Grade-school multiplication of two `n`-digit numbers is O(n²). Karatsuba noticed that `(a·10^k + b)(c·10^k + d) = ac·10^{2k} + (ad+bc)·10^k + bd`, but the middle term `(ad+bc)` can be computed as `(a+b)(c+d) - ac - bd` — reducing 4 multiplications to 3. Recursion gives `T(n) = 3·T(n/2) + O(n) = O(n^{log₂3}) ≈ O(n^{1.585})`. GMP, Java's BigInteger, Python's int — all use Karatsuba for large-integer multiplication.

**Volker Strassen** did the same for matrix multiplication in **1969**: reduced the 8 recursive multiplications in a 2×2 divide-and-conquer scheme to 7, giving O(n^{log₂7}) ≈ O(n^2.81). His paper stunned the community — everyone believed matrix multiplication was Ω(n³). The current best-known bound (Coppersmith-Winograd, refined by Le Gall 2014) is O(n^2.373), and every improvement uses the divide-and-conquer skeleton Strassen introduced.

**Master Theorem** (Bentley-Haken-Saxe 1980) formalized the analysis: `T(n) = a·T(n/b) + f(n)` has a closed-form solution based on `log_b(a)` vs. `f(n)`. Every complexity analysis you'll write in an interview uses this theorem, even if you don't cite it by name.

## THE template

Four flavors share one shape. The split is mechanical; the **combine** is where the cleverness lives — it decides whether you achieve O(n log n), O(n²), or something in between.

<PatternTemplateCard
  slug="dc-canonical"
  title="Divide & Conquer canonical skeleton"
  language="python"
  :code="bareTemplateCode"
  :invariant="bareInvariant"
  :complexity="bareComplexity"
  :specializations="templateSpecializations"
  problemShape="any D&C: split, solve halves, combine with O(f(n)) step" />

## Interactive diagram

<DivideConquerAnim />

## Sub-variations of the template

<PatternSubVariationNav pattern="divide-conquer" />

### Merge Sort <span class="diff diff-m">Medium</span>

The **bare mechanic**: sort an array by splitting, recursing, and merging two sorted halves in O(n). The ancestor of every "piggyback on merge" trick that follows.

<InvariantProof
  :statement="mergeSortInvariant.statement"
  :initialization="mergeSortInvariant.initialization"
  :maintenance="mergeSortInvariant.maintenance"
  :termination="mergeSortInvariant.termination" />

> [key] **Blind-solve first:** {{ mergeSortSolvePrompt }}

<TemplateReveal
  slug="merge-sort"
  language="python"
  :canonical="mergeSortCode"
  problemShape="split in half → recurse → merge two sorted halves with two pointers" />

**Trace** on `[5, 2, 6, 1]`:
- `_ms(a, 0, 4)` splits into `_ms(a, 0, 2)` + `_ms(a, 2, 4)`.
- `_ms(a, 0, 2)` sorts `[5, 2]` → `[2, 5]`. `_ms(a, 2, 4)` sorts `[6, 1]` → `[1, 6]`.
- Merge `[2, 5]` + `[1, 6]`: scratch becomes `[1, 2, 5, 6]`; copy back.

**Why stable (left-takes-tie):** when values are equal, taking the LEFT element first preserves original relative order among equals. This matters for stable-sort guarantees downstream (SQL `ORDER BY tiebreaker`, variants that carry original indices).

**Why one scratch buffer, not many:** allocating a fresh `scratch` at each recursive level balloons to `O(n log n)` total allocation — same work as the comparisons, but with GC pressure. One pre-allocated buffer at the top makes allocation O(n) once.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Guaranteed O(n log n), stable, predictable** — the only general-purpose comparison sort that stays n log n in the WORST case; quicksort is O(n²) worst-case on adversarial input.
- **O(n) extra space is the price for stability and predictability.** In-place merge sort exists but is tricky and rarely worth it for the memory it saves.
- **The two-finger merge IS the crux.** Both halves are sorted, so walk `i` through left and `j` through right, picking the smaller — O(n) per merge, O(log n) merge levels → O(n log n) total.
- **Prefer merge sort over quicksort when** data is on disk (external sort), inputs are linked lists (no random access needed), or stability matters (secondary sort keys must be preserved).
- **One pre-allocated scratch buffer, not one per level.** Fresh allocations at every recursion level cost O(n log n) total allocation + GC pressure; a single top-level buffer makes it O(n) once.
- **The pattern template for Count-of-Smaller, Count Range Sum, Reverse Pairs** — any "count inversions" problem IS merge sort with a counting hook in the merge step.

</details>

---

### Pow(x, n) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Pow(x, n)](https://leetcode.com/problems/powx-n/)*

> [key] **The twist:** the "split" is on the EXPONENT, not the array. `x^n = x^(n/2) · x^(n/2)` (even n) or `x · x^(n-1)` (odd n). Each halving step is O(1), so `log n` steps give O(log n) multiplications instead of O(n). This is **binary exponentiation**; the same trick works for `a^n mod m` in cryptography (RSA, Diffie-Hellman).

<InvariantProof
  :statement="powInvariant.statement"
  :initialization="powInvariant.initialization"
  :maintenance="powInvariant.maintenance"
  :termination="powInvariant.termination" />

```svg
<svg role="img" viewBox="0 0 400 160" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Binary exponentiation">
  <rect x="0" y="0" width="400" height="160" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">x^13 = x^(1101₂) = x^8 · x^4 · x^1</text>
  <g font-size="12" fill="var(--dsa-ink)" text-anchor="middle">
    <rect x="40" y="50" width="60" height="30" rx="6" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/><text x="70" y="70">x</text>
    <rect x="110" y="50" width="60" height="30" rx="6" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/><text x="140" y="70">x²</text>
    <rect x="180" y="50" width="60" height="30" rx="6" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/><text x="210" y="70">x⁴</text>
    <rect x="250" y="50" width="60" height="30" rx="6" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/><text x="280" y="70">x⁸</text>
  </g>
  <g font-size="10" fill="var(--dsa-success)" text-anchor="middle">
    <text x="70" y="95">bit 0: on → use</text>
    <text x="210" y="95">bit 2: on → use</text>
    <text x="280" y="95">bit 3: on → use</text>
  </g>
  <text x="200" y="130" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-success)">result = x · x⁴ · x⁸ = x¹³ (4 multiplications instead of 12)</text>
</svg>
```

> [key] **Blind-solve first:** {{ powSolvePrompt }}

<TemplateReveal
  slug="pow-x-n"
  language="python"
  :canonical="powCode"
  problemShape="iterate bits of n → square x each step; multiply result on odd bits" />

**Trace** `my_pow(2, 10)`:
- n=10 (`1010₂`), x=2, result=1.
- Bit 0: n is even → result stays 1; x becomes 4; n = 5.
- Bit 1: n is odd → result = 1·4 = 4; x becomes 16; n = 2.
- Bit 2: n is even → result stays 4; x becomes 256; n = 1.
- Bit 3: n is odd → result = 4·256 = 1024; x becomes 65536; n = 0. Done.
- **Result:** 1024 = 2^10. 4 multiplications, not 10.

**Recursive form is natural too:** `pow(x, n) = pow(x·x, n/2)` for even n, else `x · pow(x, n-1)`. The iterative version shown above saves stack space.

**Where this shows up:** modular exponentiation for RSA key generation (`a^d mod n` with `d` on the order of 2048 bits — binary exp is the only way), matrix exponentiation for linear recurrences (Fibonacci in O(log n)), polynomial evaluation at a point via Horner-like doubling.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Exponentiation by squaring**: `pow(x, n) = pow(x·x, n/2)` for even n, `x · pow(x·x, (n-1)/2)` for odd — halves n at every level, O(log n) multiplications instead of O(n).
- **Handle `n < 0` by computing `pow(1/x, -n)`.** Beware `n = INT_MIN`: `-n` overflows `int`; widen to `long` or special-case before recursion.
- **Iterative beats recursive on stack use.** Both are O(log n) time; iterative walks the bits of `n` and is O(1) space; recursive is O(log n) stack. Interview grading rarely cares, but tight-stack production code might.
- **The pattern generalizes beyond multiplication** — any associative operation (matrix multiply, modular multiply, function composition) uses the same O(log n) trick. This is why "matrix power" and "Fibonacci in O(log n)" exist.
- **Modular variant drops into cryptography unchanged.** `a^d mod m` with `d` on the order of 2048 bits is the arithmetic core of RSA key generation and ECDHE — binary exponentiation is the ONLY way to make that tractable.
- **Floating-point `pow` can lose precision for very large `n`.** Within the LC-50 constraints the double stays exact enough; your own extra decimals may still mismatch the judge's rounded answer.

</details>

---

### Count of Smaller Numbers After Self <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)*

<ProgressCheck id="count-of-smaller-numbers-after-self-hard" />

> [key] **The twist:** piggyback counting onto merge sort's merge step. During merge, when we place a left-half element into position, every right-half element already placed before it is smaller — count them. Carrying original indices (`indices[]` sorted by value) lets us attribute the count to the right output slot.

<InvariantProof
  :statement="countSmallerInvariant.statement"
  :initialization="countSmallerInvariant.initialization"
  :maintenance="countSmallerInvariant.maintenance"
  :termination="countSmallerInvariant.termination" />

> [key] **Blind-solve first:** {{ countSmallerSolvePrompt }}

<TemplateReveal
  slug="count-of-smaller-numbers-after-self"
  language="python"
  :canonical="countSmallerCode"
  problemShape="merge sort on indices (by value) → add (j - mid) to result[indices[i]] whenever a left element is taken" />

**Trace** on `[5, 2, 6, 1]`:
- indices start `[0, 1, 2, 3]`.
- Sort left half `[0, 1]` (values `[5, 2]`) → merge: 2 (idx 1) < 5 (idx 0) → right wins; then move left. Left (idx 0, val 5) now has 1 already-moved right element → result[0] += 1. indices → `[1, 0]`.
- Sort right half `[2, 3]` (values `[6, 1]`) → merge: right (idx 3, val 1) wins; left (idx 2, val 6) has 1 right already placed → result[2] += 1. indices → `[3, 2]`.
- Final merge: left `[1, 0]` (values `[2, 5]`), right `[3, 2]` (values `[1, 6]`).
  - 2 (idx 1) vs 1 (idx 3) → right wins. j=3.
  - 2 (idx 1) vs 6 (idx 2) → left wins. j - mid = 3 - 2 = 1 → result[1] += 1. i=1.
  - 5 (idx 0) vs 6 (idx 2) → left wins. result[0] += 1. i=2.
  - Drain right. Done.
- **result:** `[2, 1, 1, 0]`. ✓

**Related sibling: Count Inversions** — simpler version returning only the total. Add `(mid - i)` on the right-element-taken branch and sum across recursion.

**Related sibling: Reverse Pairs** — pairs with `a[i] > 2·a[j]` for `i < j`. Before the standard merge, do a separate two-pointer pass counting valid pairs; because both halves are sorted, the right pointer never moves backward → O(n) per level. Use `long` since `2 * a[j]` can overflow `int`.

**Alternative solution: Fenwick tree.** Iterate right-to-left; for each `nums[i]`, Fenwick-query "how many smaller than nums[i] seen so far?" then Fenwick-insert nums[i]. Also O(n log n). More "data-structure flavored" than "D&C flavored" — pick merge sort for interviews that specifically ask about D&C.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Merge sort with a counting hook.** During the merge step, every time a RIGHT-half element is placed before a LEFT-half element, that's an inversion against the left element — accumulate it into `result[original_index_of_left]`.
- **Index tracking is the subtlety.** The output must line up with ORIGINAL positions, not sorted positions. Carry an `indices[]` array alongside values through the recursion and update `result[indices[i]]`.
- **O(n log n) time, O(n) space** — exactly merge sort's cost, plus a tiny constant per element for the counter.
- **Fenwick tree is an equally valid O(n log n) alternative.** Coordinate-compress values, scan right-to-left, `BIT.query(v - 1)` then `BIT.update(v)`. Pick merge-sort when the interviewer asks about D&C; pick Fenwick when the values are dense ints and the DS angle fits better.
- **Tie-break with `left <= right`, not `left < right`.** On equal values, the right-half element should NOT advance before the left-half element — strict `<` would over-count inversions on duplicates.
- **Siblings reuse the same template:** Count Inversions (total only — add `mid - i` on right-wins), Reverse Pairs (`a[i] > 2·a[j]` — separate two-pointer pass before the merge), Count Range Sum (merge on prefix sums).

</details>

---

### Majority Element <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Majority Element](https://leetcode.com/problems/majority-element/)*

> [key] **The twist:** split in half, recursively find each half's majority candidate, then check which is the global majority by counting both in `[lo, hi)`. Key lemma: if `m` has strict majority in the whole array, it must have strict majority in at least ONE of the two halves (pigeonhole). O(n log n) time — slower than linear Boyer-Moore but teaches the "majority survives in a half" idea that generalizes.

<InvariantProof
  :statement="majorityInvariant.statement"
  :initialization="majorityInvariant.initialization"
  :maintenance="majorityInvariant.maintenance"
  :termination="majorityInvariant.termination" />

```svg
<svg role="img" viewBox="0 0 400 160" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Majority split lemma">
  <rect x="0" y="0" width="400" height="160" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">if m is majority of a[0..n), it is majority of at least one half</text>
  <rect x="30" y="46" width="150" height="30" rx="6" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/>
  <text x="105" y="66" text-anchor="middle" font-size="11" fill="var(--dsa-ink)">left: n/2 slots</text>
  <rect x="220" y="46" width="150" height="30" rx="6" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/>
  <text x="295" y="66" text-anchor="middle" font-size="11" fill="var(--dsa-ink)">right: n/2 slots</text>
  <text x="200" y="100" text-anchor="middle" font-size="11" fill="var(--dsa-ink)">if m ≤ n/4 in left AND m ≤ n/4 in right → total ≤ n/2 — contradiction</text>
  <text x="200" y="130" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-success)">so m survives as majority in at least one half ✓</text>
</svg>
```

> [key] **Blind-solve first:** {{ majoritySolvePrompt }}

<TemplateReveal
  slug="majority-element"
  language="python"
  :canonical="majorityCode"
  problemShape="split in half → recursive candidates → count both in [lo, hi) to pick the winner" />

**Trace** on `[3, 2, 3]`:
- `helper(0, 3)` splits at mid=1 into `[3]` and `[2, 3]`.
- Left: `helper(0, 1)` returns 3.
- Right: `helper(1, 3)` splits at mid=2 into `[2]` and `[3]`. Both candidates differ → count in `[1, 3)`: 2 appears 1x, 3 appears 1x → tie, returns whichever comes first (2 in some impls; disambiguate as needed).
- Back at `helper(0, 3)`: candidates 3 and 2 differ → count in `[0, 3)`: 3 appears 2x, 2 appears 1x → return 3. ✓

**Why learn this if Boyer-Moore is O(n)?** The "majority survives in at least one half" lemma generalizes to:
- **1/3-majority (LC Majority Element II)**: at most 2 elements can appear > n/3 times; the "survive in halves" argument extends.
- **Distributed count** at MapReduce scale: each shard reports its local majority candidates; the reducer counts globally.
- **Robust tournament election**: proofs of correctness in Byzantine fault-tolerance papers invoke this lemma.

**When to prefer Boyer-Moore (O(n), O(1) space):** always, in production. The D&C variant is a teaching tool and a stepping stone to the generalizations above.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **The lemma: a strict majority in the whole array must be a strict majority in at least ONE half.** By pigeonhole: if `m` appears `≤ n/4` in both halves, total `≤ n/2` — contradiction. This is why D&C works at all here.
- **Compare two candidates by counting both in the current window.** When the left and right halves disagree, scan `[lo, hi)` counting each candidate's occurrences and pick the winner — O(n) per level, O(log n) levels → O(n log n) total.
- **Boyer-Moore Majority Vote is O(n), O(1) space.** Candidate ← first element, counter counts matches, decrements on mismatches, resets with new candidate on zero. For LC-169 (strict majority guaranteed), the final candidate IS the answer.
- **Boyer-Moore does NOT verify.** If majority is not guaranteed, run a verification pass (count the candidate's occurrences, check `> n/2`). LC-229 (`> n/3` majority) extends to TWO candidates + verification.
- **The lemma generalizes.** `> n/3` majority admits at most 2 candidates (same proof pattern); distributed count at MapReduce scale uses it to collapse shard-local candidates to a global one.
- **Three valid approaches, know all three:** Boyer-Moore (O(n) time, O(1) space — production), HashMap counting (O(n) time, O(n) space — easiest to explain), sort then take middle (O(n log n) time, O(1) space in-place or O(log n) stack — one-liner).

</details>

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

## In the wild — NumPy FFT (Cooley-Tukey)

`numpy.fft.fft` and `scipy.fft.fft` implement the **Cooley-Tukey 1965 FFT**, divide-and-conquer on complex exponentials. The algorithm splits an N-point DFT into two N/2-point DFTs (on the even-indexed and odd-indexed samples), then combines them with "twiddle factors" (complex roots of unity). Recurrence `T(N) = 2·T(N/2) + O(N) = O(N log N)` — the same shape as merge sort.

What runs on top of this FFT:
- **MP3, AAC, Vorbis audio encoding** — DCT (a cosine-only variant of FFT) compresses frequency bands.
- **JPEG, HEIC image encoding** — 8×8 2D DCT turns pixel blocks into frequency coefficients, then quantizes.
- **5G cellular modulation (OFDM)** — IFFT at the transmitter, FFT at the receiver, run per OFDM symbol at ~15 kHz rate on every phone.
- **Radio astronomy** — Very Long Baseline Interferometry correlators run FFT on telescope sample streams to produce sky-brightness maps.
- **Protein folding (AlphaFold inference)** — electrostatic interactions are evaluated in Fourier space via FFT because O(N log N) beats the O(N²) direct sum.

Jon Bentley called the Cooley-Tukey FFT "the most important algorithm of the 20th century" in *Programming Pearls*, exactly because its divide-and-conquer structure is reused everywhere.

Other named production uses of divide-and-conquer:
- **Timsort** (Python's `sorted`, Java's `Arrays.sort`) is merge-sort + insertion-sort hybrid: run detection in O(n), merge runs with D&C merge.
- **Rust's `slice::sort`** uses Timsort-flavored stable merge sort.
- **Postgres btree page split** on insertion: when a page overflows, split it in half and promote a separator key up — a D&C on the index tree.
- **Hadoop/Spark `sortByKey`** uses external merge sort (D&C with k-way merge in the reduce phase, chapter 30).

## When NOT to use it

Having walked the four D&C flavors, here's where "split, solve halves, combine" is the wrong frame.

- **The two halves depend on each other** (state flows across the split) — you can't recurse independently; reach for DP with a state that captures the cross-half interaction.
- **The combine step is O(n log n)** — your total becomes O(n log² n); check if a single-pass approach exists.
- **A simple linear scan exists** — Kadane for maximum subarray is O(n), D&C variant is O(n log n).
- **The split creates highly unbalanced recursion** — you may fall toward O(n²).
- **The combine step has to re-scan too much hidden state from both halves.**
- **The problem needs online updates** — segment trees or Fenwick trees may be better.
- **Recursion depth could exceed limits** and an iterative structure is simpler.

### Visual 1: cross-half dependencies — D&C can't recurse independently

Longest Increasing Subsequence (LIS) looks like it could D&C, but the halves share information:

```text
   nums = [3, 1, 4, 1, 5, 9, 2, 6]

   Split: [3, 1, 4, 1]  |  [5, 9, 2, 6]
                        ↑
              LIS of left half = 3  (1, 4, ...)   missing: ends at what?
              LIS of right half = 3 (2, 6, ...)   starts at what?

   Can we combine? To know if a left-LIS can EXTEND into the right half,
   we need to know the LAST value of every possible left-LIS. There are
   many such LISs with different endings — the combine step would have
   to track all of them.

   Also: the LIS might not cross the boundary at all, OR it might reuse
   a prefix of one left-LIS and a suffix of a specific right-LIS whose
   first value exceeds the left-LIS's last value. The combine isn't
   additive — it's a combinatorial match on endpoints.

   The right algorithm: DP with dp[i] = LIS ending at i, or the
   patience-sort variant with a `tails[]` array binary-searched for each
   new element. Neither has D&C structure.
```

The D&C smell test: can you solve each half with a bounded summary (one number, a count, a boundary pair) and combine without re-examining the raw halves? Merge sort's answer is yes — the summary is "the sorted half". Inversion count's answer is yes — "count of inversions within + a merge-time cross-count". LIS says no — the summary would need to be the full set of per-endpoint LISs, which defeats the point.

### Visual 2: unbalanced split degrades to O(n²)

D&C's O(n log n) depends on the split being balanced. If the pivot is near the extreme every time, you get O(n²):

```text
   Quicksort on an already-sorted array, pivot = last element:

     [1, 2, 3, 4, 5, 6, 7, 8]            pivot = 8   → partition: [1..7] | [8]
     [1, 2, 3, 4, 5, 6, 7]               pivot = 7   → partition: [1..6] | [7]
     [1, 2, 3, 4, 5, 6]                  pivot = 6   → partition: [1..5] | [6]
     ...

   Recursion depth: n (not log n)
   Work per level: n, n-1, n-2, ..., 1  → total O(n²)

   Balanced split would be:
     [1..8]          split at 4-5         → O(1) partition
     [1..4] [5..8]   split at 2-3, 6-7    → 2 subproblems
     [1,2][3,4][5,6][7,8]                 → 4 subproblems
     ...
   Recursion depth: log n, total O(n log n)
```

The master theorem's `T(n) = aT(n/b) + f(n)` assumes `b > 1`. An unbalanced split has effective `b = 1 + ε/n`, which collapses `log_b n` to O(n). The fixes: randomize the pivot (median-of-three sampling), or switch to a different algorithm (merge sort has guaranteed O(n log n) because the split is positional, not value-dependent).

## Recognition drill

<RecognitionDrill pattern="divide-conquer" :count="10" />

## Advanced — follow-ups and failure modes

<details>
<summary><b>What if combine would be O(n log n) and total would be O(n log² n)?</b></summary>

**Closest Pair of Points** has this risk. Naive combine sorts the "strip near the dividing vertical line" by y — O(n log n) per combine → O(n log² n) total. The trick: maintain BOTH an x-sorted and a y-sorted version of each half; combine merges the y-sorted strips in O(n). Then total is O(n log n). The lesson: when combine wants to re-sort, pre-maintain the needed order up the tree.
</details>

<details>
<summary><b>What if the input is a linked list, not an array?</b></summary>

**Sort List (LC 148)**: can't random-access the middle. Find it with fast/slow pointers (chapter 23) in O(n), then recurse. Merge two sorted linked lists in O(m+n) with pointer re-linking. Overall O(n log n) time, O(log n) stack (no array scratch — nodes are reused in-place). This is the standard reference implementation of merge sort for singly-linked lists.
</details>

<details>
<summary><b>What if subproblems overlap — can D&C still help?</b></summary>

Vanilla D&C fails: solving two halves and combining doesn't account for pairs that need both halves simultaneously. BUT: **memoize subproblem results** and you get **top-down DP**. The split pattern becomes a memoized recursion. The transition from "D&C with independent subproblems" to "DP with overlapping subproblems" is a key skill shift — same recursion shape, add a memoization layer.

Examples: Longest Common Subsequence (D&C recurrence has overlap → memoize → O(mn) DP), Matrix Chain Multiplication, Burst Balloons.
</details>

<details>
<summary><b>What if the array doesn't split cleanly in half?</b></summary>

Quicksort splits by *pivot* instead of *midpoint* — the partition can be anywhere from 1:(n-1) to n/2:n/2. Worst case is O(n²); expected is O(n log n) with random pivots. See chapter 41 (Quickselect) for the amortized argument. The lesson: not every D&C splits at the midpoint; some split by a value-based criterion. Tune the split strategy to the problem.
</details>

<details>
<summary><b>Breaking point — when D&C stops being enough.</b></summary>

- **Non-decomposable state** (next element depends on all previous): switch to DP.
- **Online updates with queries**: switch to segment tree or Fenwick tree.
- **Very unbalanced splits** (e.g. recursion on `n-1` instead of `n/2`): the recurrence degrades to O(n²) or worse.
- **Combine step too expensive**: redesign the returned summary to make combine O(n) or O(log n).
- **Stack-depth limits** on very large n (>10⁶): rewrite D&C iteratively (bottom-up merge, iterative FFT).
</details>

### Cross-pattern problems

| Problem | Primary pattern | What D&C contributes |
|---|---|---|
| [Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) | merge sort piggyback | pre-merge counting pass with two sorted halves |
| [Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/) | merge sort on prefix sums | each level counts valid cross-pair ranges in O(n) |
| [Sort List](https://leetcode.com/problems/sort-list/) | fast-slow + merge | fast-slow finds the midpoint; D&C orchestrates the sort |

## Related patterns + Check your understanding

<RelatedPatterns pattern-id="divide-conquer" />

<Quiz
  pattern-id="divide-conquer"
  :questions="quizQuestions" />

<PrintButton />
