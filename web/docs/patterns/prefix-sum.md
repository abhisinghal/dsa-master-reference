# Prefix Sum &amp; Difference Arrays


<PatternVideo pattern-name="Prefix Sum" duration="8–12 min" />

<PatternProgress pattern-id="prefix-sum" problems="prefix-sum-subarray-sum-equals-k, subarray-sums-divisible-by-k, contiguous-array, continuous-subarray-sum, corporate-flight-bookings, car-pooling, range-addition, matrix-block-sum, count-submatrices-with-target-sum, maximal-rectangle" />

<script setup>
const bareMechanicCode = `int[] a = {3, 1, 4, 1, 5};
long[] pre = new long[a.length + 1];       // length n+1; pre[0]=0 by default
for (int i = 0; i &lt; a.length; i++)
    pre[i + 1] = pre[i] + a[i];            // running total

// Range sum of a[l..r] inclusive, in O(1):
long sum = pre[r + 1] - pre[l];`

const theTemplateCode = `class PrefixSum {
    long[] pre;                            // length n+1; pre[0]=0

    PrefixSum(int[] a) {
        pre = new long[a.length + 1];
        for (int i = 0; i &lt; a.length; i++)
            pre[i + 1] = pre[i] + a[i];    // one accumulate per element
    }

    long sum(int l, int r) {               // inclusive range [l, r]
        return pre[r + 1] - pre[l];        // one subtraction per query
    }
}`

const theTemplateInvariant = {
  statement: `pre[i] equals a[0] + a[1] + ... + a[i-1]. Length is n+1. pre[0]=0 is the sum of the empty prefix. Any contiguous range sum is one subtraction of two prefixes.`,
  initialization: `pre[0] = 0 — the empty prefix sums to zero, no elements consumed.`,
  maintenance: `After processing index i, pre[i+1] = pre[i] + a[i]. By induction pre[i+1] equals a[0..i].`,
  termination: `After the build loop, pre[n] holds Σa and sum(l,r) = pre[r+1] - pre[l] is well-defined for every 0 ≤ l ≤ r < n.`
}

const theTemplateComplexity = {
  time: `O(n) build · O(1) per range-sum query`,
  space: `O(n) for the prefix array`
}

const theTemplateSpecializations = [
  { slug: `range-sum-1d-easy`, title: `Range Sum 1D (easy)` },
  { slug: `subarray-sum-equals-k-medium`, title: `Subarray Sum Equals K (medium)` },
  { slug: `difference-array-medium`, title: `Difference Array (medium)` },
  { slug: `_2d-prefix-sum-medium`, title: `2D Prefix Sum (medium)` },
  { slug: `prefix-xor-medium`, title: `Prefix XOR (medium)` },
  { slug: `prefix-mod-medium`, title: `Prefix Mod (medium)` },
]

const theTemplateProblemShape = `Many queries over a static array where each query reduces to a difference of two running aggregates (sum, XOR, mod-residue count, 2D rectangle inclusion-exclusion).`

const prefixXorCode = `int subarrayXorEqualsK(int[] a, int k) {
    Map&lt;Integer, Integer&gt; count = new HashMap&lt;&gt;();
    count.put(0, 1);                       // empty prefix has XOR 0
    int running = 0, answer = 0;
    for (int x : a) {
        running ^= x;                      // XOR, not plus
        // A prior prefix p satisfies running ^ p = k iff p = running ^ k.
        answer += count.getOrDefault(running ^ k, 0);
        count.merge(running, 1, Integer::sum);
    }
    return answer;
}`

const prefixModCode = `int subarraysDivByK(int[] a, int k) {
    int[] countByResidue = new int[k];
    countByResidue[0] = 1;                 // empty prefix has residue 0
    int running = 0, answer = 0;
    for (int x : a) {
        running = ((running + x) % k + k) % k;   // handle negatives
        answer += countByResidue[running];       // every earlier same-residue → divisible subarray
        countByResidue[running]++;
    }
    return answer;
}`

const prefixXorQuote = `Count the contiguous subarrays whose XOR equals k.`
const prefixModQuote = `Count the contiguous subarrays whose sum is divisible by k.`

const advancedWhatIfs = [
  {
    title: `What if the array has point updates between queries?`,
    body: `Prefix sum becomes O(n) per update — unacceptable at Q = 10^5. Switch to a Fenwick tree (BIT) for O(log n) update + O(log n) prefix. The invariant mutates from "snapshot" to "incrementally maintained running total."`
  },
  {
    title: `What if the queries are on a 1D sliding window of fixed size k?`,
    body: `You don't need a full prefix array. A single running sum with a window of length k (add a[r], subtract a[r-k]) runs in O(1) extra space. Prefix sum works too but allocates O(n).`
  },
  {
    title: `What if values are reals and precision matters?`,
    body: `Naive accumulation accumulates error. Use Kahan summation (compensated accumulation) or pairwise summation (what NumPy's reduceat uses). The algorithmic skeleton is the same; the inner update changes from one add to four.`
  },
  {
    title: `What if the matrix is sparse but queries are dense?`,
    body: `A dense 2D prefix table costs O(RC) build and O(RC) space even when most cells are 0. If the matrix has K ≪ RC non-zero cells, a Fenwick tree on coordinates or a CDQ divide-and-conquer scan over events gives O((K + Q) log K).`
  },
  {
    title: `What if the array is distributed across GPU threads?`,
    body: `This is where Blelloch's parallel prefix (section "History" below) wins — the sequential O(n) loop becomes an O(log n)-depth tree scan. Thrust's inclusive_scan and TensorFlow's XLA scan both implement this.`
  }
]

const crossPatternProblems = [
  { href: `https://leetcode.com/problems/sliding-window-maximum/`, title: `Sliding Window Maximum — monotonic deque, not prefix sum (operation isn't invertible)` },
  { href: `https://leetcode.com/problems/range-sum-query-mutable/`, title: `Range Sum Query — Mutable (307) — bridges prefix sum → Fenwick tree` },
  { href: `https://leetcode.com/problems/number-of-ways-to-split-array-into-good-subarrays/`, title: `Number of Good Subarrays — combine prefix count of 1s with combinatorics` }
]

const mastery5 = [
  {
    q: `An array supports 10^5 range-sum queries and 10^5 point updates interleaved. Which structure wins?`,
    choices: [
      { text: `Prefix sum (rebuild on each update)`, correct: false, explanation: `Rebuild is O(n) → 10^10 ops total.` },
      { text: `Fenwick tree`, correct: true, explanation: `O(log n) per update AND per prefix query → 10^5 · 17 ≈ 2·10^6 ops total.` },
      { text: `Hash map`, correct: false, explanation: `Doesn't support range sum directly.` },
      { text: `Difference array`, correct: false, explanation: `Only works when all updates precede all queries.` }
    ]
  },
  {
    q: `For "count subarrays whose sum is divisible by k", why can we bucket prefix sums by (pre mod k)?`,
    choices: [
      { text: `Two prefixes in the same residue bucket differ by a multiple of k`, correct: true, explanation: `(pre_r - pre_l) ≡ 0 (mod k) iff pre_r ≡ pre_l (mod k).` },
      { text: `The modulo distributes over addition in the standard way`, correct: false, explanation: `True but not the direct justification.` },
      { text: `Hash maps are O(1) lookup`, correct: false },
      { text: `Negative numbers wrap around correctly`, correct: false, explanation: `Only if you canonicalize with ((x % k) + k) % k.` }
    ]
  },
  {
    q: `Why does prefix XOR with a hash map count "subarrays with XOR = k" in O(n), the same way prefix sum counts "subarrays with sum = k"?`,
    choices: [
      { text: `XOR is its own inverse — pre_r ^ pre_l = k ⟺ pre_l = pre_r ^ k`, correct: true, explanation: `This is the exact algebraic property that lets the hash-map trick transfer.` },
      { text: `XOR is commutative`, correct: false, explanation: `True but not sufficient.` },
      { text: `XOR distributes over the hash function`, correct: false },
      { text: `By coincidence; the two problems are unrelated`, correct: false }
    ]
  },
  {
    q: `A difference array solves 10^5 range updates on a length-10^6 array in O(n + Q). What's the single prefix pass at the end doing?`,
    choices: [
      { text: `Converting endpoint deltas into per-index net totals`, correct: true, explanation: `diff is the difference-sequence representation; one prefix pass inverts it.` },
      { text: `Sorting the updates by starting index`, correct: false },
      { text: `Deduplicating overlapping ranges`, correct: false },
      { text: `Converting from 0-indexed to 1-indexed`, correct: false }
    ]
  },
  {
    q: `You discover prefix sums are overflowing int on an array where every a[i] ≤ 10^9 and n = 10^5. Minimum fix?`,
    choices: [
      { text: `Use long[] for the prefix array`, correct: true, explanation: `Max prefix ≈ 10^14 which fits in long (max ~9·10^18) but not int (max ~2·10^9).` },
      { text: `Take modulo 10^9+7 of every prefix`, correct: false, explanation: `Changes the problem — now differences don't equal subarray sums.` },
      { text: `Switch to a Fenwick tree`, correct: false, explanation: `Doesn't fix overflow; just moves it.` },
      { text: `Add a saturation check on every write`, correct: false, explanation: `Over-engineering; use the right type.` }
    ]
  }
]
</script>



## Why prefix sum exists — the story

You built a dashboard for a stock trading desk. Traders keep asking the same question in different forms: *"How much revenue did we book between March 3rd and March 17th?"* *"What's the total volume from tick 200 to tick 800?"* Every question is a **range sum** over the same underlying array.

The obvious answer: sum the range. A `for` loop from `l` to `r`, accumulate, return. It's five lines. For one query on 1,000 elements it's instant. For a hundred queries it's a hundred loops — still fine.

But the desk sends **50,000 queries per second** and the array has **10⁶ elements**. Now every query averages `5·10⁵` operations; total workload is `2.5·10¹⁰` per second. The CPU has 10⁹ cycles per second. **You are 25× slower than realtime.** Traders are getting stale numbers; the manager is asking questions in Slack. Every query is redoing work — array element `a[500]` gets added into every range that includes it, over and over.

The pattern is to trade one-time prep for permanently cheap queries. Compute a **running total** array `pre[]` once: `pre[i]` = sum of everything strictly before index `i`. Now every range sum becomes **one subtraction**: `sum(l..r) = pre[r+1] - pre[l]`. **O(n) prep + O(1) per query.** For the trading desk: prep once (10⁶ ops), then every query is a single subtraction — the CPU handles 50K queries per second with time to spare.

The mirror image — the **difference array** — makes range *updates* cheap: instead of adding `+5` to every element in `[l, r]`, you flag `+5` at `l` and `-5` at `r+1`, then run a prefix sum at the end to materialize the final array. Range-update problems that would be O(nQ) become O(n + Q).

And the party trick: pair prefix sums with a hash map to count subarrays with a target sum — even with negative numbers, where a sliding window silently fails. That's the pattern behind Subarray Sum Equals K, one of the top-10 most-asked LeetCode problems in FAANG interviews.

## The core idea — precompute once, query in O(1) forever

<PrefixSumAnim />



```text
a      =   3   1   4   1   5
pre    = 0   3   4   8   9  14      pre[i] = sum of a[0..i-1]
sum(l..r) = pre[r+1] - pre[l]       e.g. sum(1..3)=pre[4]-pre[1]=9-3=6
```



Read that carefully. `pre[]` has **length n+1**, not `n`. The extra slot at `pre[0] = 0` is not a mistake — it lets you query `sum(0..r) = pre[r+1] - pre[0]` without special-casing the left edge. Every off-by-one bug in prefix sum comes from getting `pre[]`'s length wrong.

<Callout kind="key" title="Key Insight">

"Sum over a range" ⇒ prefix sums. "Count subarrays whose sum = k" ⇒ prefix sums **as keys in a hash map**: a subarray `(l,r]` has sum k iff `pre[r]-pre[l]=k`, i.e. `pre[l]=pre[r]-k` was seen before.

</Callout>

## When to use it — recognition signals

Reach for prefix sum (or its variants) when:

- **Many range-sum queries on a static array** — build once, answer each in O(1).
- **Count subarrays with sum = k** (or divisible by k, or in a range) — combine prefix sum with a HashMap of `pre -> count`.
- **Range updates on an array** followed by a materialization pass — difference array turns O(nQ) into O(n+Q). Classic examples: Corporate Flight Bookings, Car Pooling, Range Addition.
- **2D range-sum queries** — extend to 2D prefix sum (a.k.a. summed-area tables). Answers rectangle-sum queries in O(1) with O(nm) prep. Used by image-processing algorithms.
- **Contiguous subarray with equal 0s and 1s** — remap `0 → -1`, then a subarray sums to 0 iff `pre[l] == pre[r]`. This is the *equal-partition* trick.
- **Sliding window doesn't work because values can be negative** — a window can't reliably shrink when the sum can go up or down. Prefix sums + hashing is the escape hatch.

## The bare mechanic — Range Sum 1D

Before any variation, see the mechanic naked. One array, one running total, one subtraction per query:



```java
int[] a = {3, 1, 4, 1, 5};
long[] pre = new long[a.length + 1];       // pre[0]=0 (sentinel)
for (int i = 0; i < a.length; i++)
    pre[i + 1] = pre[i] + a[i];            // 0, 3, 4, 8, 9, 14

long sum = pre[r + 1] - pre[l];            // range [l, r] inclusive — O(1)
```





```text
a      =   3   1   4   1   5
pre    = 0   3   4   8   9  14      pre[i] = sum of a[0..i-1]
sum(1..3) = pre[4] - pre[1] = 9 - 3 = 6   // just three cells away
```



**Why the extra `pre[0] = 0`?** Without it, `sum(0..r)` needs a special case for the left edge. With it, every range becomes one uniform subtraction. **Every off-by-one in prefix sum traces back to omitting this sentinel.**

<Callout kind="key" title="The one move">

compute a running total once, then every range sum is one subtraction. The variations swap "sum" for XOR, mod-residue counting, 2D inclusion-exclusion, or endpoint deltas — but the mechanic is always "snapshot the running aggregate, difference two snapshots."

</Callout>

## THE template — build once, query in O(1)

<PatternTemplateCard
  slug="prefix-sum"
  title="Prefix Sum"
  language="java"
  :code="theTemplateCode"
  :invariant="theTemplateInvariant"
  :complexity="theTemplateComplexity"
  :specializations="theTemplateSpecializations"
  :problemShape="theTemplateProblemShape"
/>

<InvariantProof
  :statement="theTemplateInvariant.statement"
  :initialization="theTemplateInvariant.initialization"
  :maintenance="theTemplateInvariant.maintenance"
  :termination="theTemplateInvariant.termination"
/>

### What the chips above open

The six specialization chips on the card link to the H3 sub-variations below. Each one keeps the same skeleton — a running aggregate maintained in O(1) per step, a difference of two aggregates at query time — and swaps a single operation. Hover each chip to see the one thing that changes.

### Complexity ladder (comparison vs. the alternatives)

| Approach | Build | Query | Update | Space |
|---|---|---|---|---|
| Naive range sum | 0 | O(n) | O(1) | O(n) |
| **1D prefix sum** | **O(n)** | **O(1)** | **O(n) rebuild** | **O(n)** |
| Fenwick tree | O(n log n) | O(log n) | O(log n) | O(n) |
| Segment tree | O(n) | O(log n) | O(log n) | O(n) |
| **2D prefix sum** | **O(rc)** | **O(1)** | **O(rc) rebuild** | **O(rc)** |
| **Difference array** | **O(n+Q)** | **O(1) after materialize** | **O(1)** | **O(n)** |

Rule of thumb: **prefix sum when array is static; Fenwick/segment tree when updates are frequent.**

## When the mechanic breaks — three failure modes

<TrapTrace
  title="Off-by-one on pre[] length"
  bug="You size `pre = new long[n]` and query `pre[r+1] - pre[l]`. Now `r = n-1` reads out of bounds. Also, `sum(0..r) = pre[r+1] - pre[0]` has no `pre[0]` sentinel, so you special-case the left edge and the special case is wrong half the time."
  fix="Size `pre = new long[n+1]` with `pre[0] = 0` as the sentinel. Every range query becomes `pre[r+1] - pre[l]` uniformly. The sentinel costs 8 bytes and eliminates the entire class of off-by-one at the left boundary."
/>

<TrapTrace
  title="Forgetting the empty-prefix seed in the hash-map variant"
  bug="Subarray Sum Equals K with `nums=[3,4], k=3`: you expect `1` (the subarray `[3]`) but return `0`. The subarray starts at index 0, so there's no earlier prefix to pair with — and your map never seeded `{0: 1}` to represent the empty prefix."
  fix="Always `count.put(0, 1)` before the loop. The empty prefix sums to zero, has been 'seen once' trivially. The same seed is required for Prefix XOR (`count.put(0, 1)`) and Prefix Mod (`countByResidue[0] = 1`)."
/>

<TrapTrace
  title="Integer overflow in prefix sums"
  bug="`n = 10^5` elements, each up to `10^9`, so Σa reaches `10^14` — well outside `int` (max ~2·10^9). `pre[i]` silently wraps to negative garbage, and every subsequent range query returns a wrong answer with no runtime signal. Same bug class as Bloch's binary-search overflow."
  fix="Declare `pre` as `long[]`. Max cumulative prefix for the worst case is ~9·10^18 which fits comfortably. If you're also doing XOR, int is fine — XOR doesn't grow. If values are reals, see Kahan/pairwise summation in Advanced below."
/>

## History — Blelloch's parallel prefix, 1990

The prefix-sum operation was formalized by **Guy Blelloch** at CMU in his 1990 paper *"Prefix Sums and Their Applications."* The paper proved that prefix sum — despite looking inherently sequential — could be **parallelized** to O(log n) depth using `n` processors via a "work-efficient" tree-reduction pattern. That algorithm became the foundation of **CUDA's `thrust::inclusive_scan`** and every modern GPU primitive for reductions, sorting, and histogram-building.

Every time you `git diff` and see a fast enumeration of changed lines, or your ML framework runs an `argmax` reduction across 10⁴ GPU cores, you're seeing Blelloch's algorithm in action. In interviews, dropping the phrase *"the parallel-prefix-scan variant"* signals depth beyond LeetCode.

The difference-array trick appears informally in Knuth's *Art of Computer Programming* Vol 1 (1968), but the modern interview form — turning `Q` range updates into a single O(n) pass — was popularized on TopCoder and Codeforces in the mid-2000s.

## Sub-variations of the template

<PatternSubVariationNav pattern="prefix-sum" />

### Range Sum 1D <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Range Sum Query — Immutable](https://leetcode.com/problems/range-sum-query-immutable/)*

The bare mechanic as a sub-variation. Build once, serve many queries in O(1).



```java
class NumArray {
    private final long[] pre;
    public NumArray(int[] nums) {
        pre = new long[nums.length + 1];
        for (int i = 0; i < nums.length; i++)
            pre[i + 1] = pre[i] + nums[i];
    }
    public int sumRange(int l, int r) {
        return (int)(pre[r + 1] - pre[l]);
    }
}
```



<Callout kind="key" title="Interview answer">

*"I build a running-total array `pre` of length `n+1` with `pre[0] = 0` as a sentinel. Each query is one subtraction. O(n) build, O(1) per query."*

</Callout>

**When this is NOT enough** — if the problem adds *point updates* between queries, prefix sum degrades to O(n) per update. Reach for a Fenwick tree. If the problem adds *range updates* then one final query, use the Difference Array sub-variation below.

### Subarray Sum Equals K <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/)*

<ProgressCheck id="subarray-sum-equals-k" />





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" role="img" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Diagram illustrating: Subarray Sum Equals K Medium">
  <defs>
    <marker id="ar-ps-primary" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/></marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-primary)">Subarray sum = difference between two prefixes</text>
  <text x="44" y="86" text-anchor="end" font-size="12" font-weight="700" fill="var(--dsa-neutral)">nums</text>
  <text x="44" y="158" text-anchor="end" font-size="12" font-weight="700" fill="var(--dsa-neutral)">prefix</text>
  <g text-anchor="middle">
    <rect x="70" y="58" width="44" height="44" rx="7" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="122" y="58" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="174" y="58" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="226" y="58" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <g font-size="17" font-weight="700" fill="var(--dsa-ink)">
      <text x="92" y="86">1</text><text x="144" y="86">2</text><text x="196" y="86">3</text><text x="248" y="86">4</text>
    </g>
    <rect x="118" y="50" width="104" height="60" rx="10" fill="none" stroke="var(--dsa-primary)" stroke-width="var(--dsa-outline-stroke)"/>
    <text x="170" y="45" font-size="12" font-weight="700" fill="var(--dsa-primary)">subarray [2,3]</text>
    <rect x="70" y="130" width="44" height="44" rx="7" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="122" y="130" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="174" y="130" width="44" height="44" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="226" y="130" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <g font-size="17" font-weight="700" fill="var(--dsa-ink)">
      <text x="92" y="158">1</text><text x="144" y="158">3</text><text x="196" y="158">6</text><text x="248" y="158">10</text>
    </g>
  </g>
  <path d="M94 180 C110 210 180 210 196 180" fill="none" stroke="var(--dsa-primary)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-ps-primary)"/>
  <rect x="286" y="86" width="92" height="74" rx="9" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
  <text x="332" y="109" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">k = 5</text>
  <text x="332" y="130" text-anchor="middle" font-size="12" fill="var(--dsa-success)">6 - 1 = 5</text>
  <text x="332" y="150" text-anchor="middle" font-size="11" fill="var(--dsa-neutral)">pre[3]-pre[0]</text>
  <text x="200" y="228" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">at each prefix, ask how many earlier prefixes equal current - k</text>
</svg>
</div>




<div class="readfig"><b>How to read it:</b> The subarray <b>[2,3]</b> is found by subtracting an earlier prefix from the current prefix; the hashmap version counts how often <code>prefix - k</code> has appeared.</div>

### Problem
Count how many **contiguous subarrays** sum exactly to `k`. The array may contain **negative** numbers — which is what rules out a sliding window.

**Constraints:** `1 ≤ n ≤ 2·10⁴`; values and `k` fit in `int`; negatives allowed.

**Example 1:** `nums = [1,2,1,2,1], k = 3` → `4`.

<ExamplePreview compact :input="['1', '2', '1', '2', '1', '|', '3']" :output="['4']" />

**Example 2:** `nums = [1,-1,0], k = 0` → `3` (`[1,-1]`, `[1,-1,0]`, and `[0]`).

<ExamplePreview compact :input="['1', '-1', '0', '|', '0']" :output="['3']" />

### Solution — brute force
Start with the direct baseline: enumerate every candidate and compute the answer from scratch. It is correct, but it repeats the exact work that the pattern is meant to reuse.



```java
int subarraySumBrute(int[] a, int k) {
    int ans = 0;
    for (int left = 0; left < a.length; left++) {
        int sum = 0;
        for (int right = left; right < a.length; right++) {
            sum += a[right];
            if (sum == k) ans++;
        }
    }
    return ans;
}
```



**Brute-force cost:** O(n²) time, O(1) space — too slow for n ≥ 10⁴.

### Solution — optimized
The optimized idea counts prefix pairs. At running prefix `pre`, every earlier prefix equal to `pre - k` forms a subarray ending here with sum `k`, so a frequency map gives the answer immediately.

**Pattern.**
Prefix sum + hash map of prefix frequencies. Handles negatives (sliding window cannot).

**Java.**


```java
int subarraySum(int[] a, int k) {
    Map<Long,Integer> count = new HashMap<>();
    count.put(0L, 1);                 // empty prefix
    long pre = 0; int ans = 0;
    for (int x : a) {
        pre += x;
        ans += count.getOrDefault(pre - k, 0);
        count.merge(pre, 1, Integer::sum);
    }
    return ans;
}
```



### Time Complexity
Existing summary: Time O(n) · Space O(n).

The scan is O(n) because each array value updates one running prefix and performs two expected-O(1) hash-map operations.

### Space Complexity
Space is O(n) in the worst case because every prefix sum can be distinct and stored in the map.

### Learning notes
- Why `Map<Long,Integer>`? — prefix sums can exceed int range.
- Why `count.put(0L, 1)`? — it represents the empty prefix before index 0.
- Why add `count.getOrDefault(pre - k, 0)`? — those prior prefixes make subarrays summing to k.
- Why merge `pre` after counting? — the current prefix should be available only to future endings.
- Why frequencies, not one index? — multiple prior prefixes can create multiple valid subarrays.

<Callout kind="inv" title="Invariant">

`count` maps each prefix-sum value to how many indices produced it among the processed prefix. At index `r`, the number of valid `l` is `count[pre - k]`.

</Callout>

<Callout kind="note" title="Trace it">

`a=[1,2,1,2,1], k=3`. Running prefixes `0,1,3,4,6,7`. Each time `pre−3` was seen before, you found a subarray: pairs give `[1,2],[2,1],[1,2],[2,1]` → **4**.

</Callout>

<Callout kind="trap" title="Common Trap">

Forgetting the `count.put(0,1)` seed drops subarrays that start at index 0. Do **not** use a sliding window here — negatives destroy the monotonic shrink.

</Callout>


<CodeTrace
  title="Subarray Sum Equals K — a=[1,2,1,2,1], k=3"
  :values="[1,2,1,2,1]"
  :windowKeys="['i']"
  :cellWidth="38"
  :steps='[
    { pointers: { i: 0 }, vars: { pre: 1, "need pre-k": -2, count: 0, "seen": "{0:1}" }, note: "map miss. seen[1]=1" },
    { pointers: { i: 1 }, vars: { pre: 3, "need pre-k": 0, count: 1, "seen": "{0:1,1:1}" }, note: "seen[0]=1 → +1. seen[3]=1", added: [0,1] },
    { pointers: { i: 2 }, vars: { pre: 4, "need pre-k": 1, count: 2, "seen": "{0:1,1:1,3:1}" }, note: "seen[1]=1 → +1. seen[4]=1", added: [1,2] },
    { pointers: { i: 3 }, vars: { pre: 6, "need pre-k": 3, count: 3, "seen": "{0:1,1:1,3:1,4:1}" }, note: "seen[3]=1 → +1. seen[6]=1", added: [2,3] },
    { pointers: { i: 4 }, vars: { pre: 7, "need pre-k": 4, count: 4, "seen": "{...,4:1,6:1}" }, note: "seen[4]=1 → +1. final count=4", added: [3,4] }
  ]'
/>

<Callout kind="pat" title="Pattern Connection">

The shared idea is **charge a subarray-with-a-target-property to its prefix**: a subarray `(l,r]` has the property iff two prefixes differ by the target, so you store seen prefixes in a map. Recognize it in *Contiguous Array* (map a 0/1 array's ±1 running sum to the first index it appeared — a balanced subarray means equal prefixes) and *Subarray Sums Divisible by K* (bucket prefixes by `pre mod k`; two prefixes in the same bucket bound a divisible subarray). The transfer trick: rephrase "count subarrays where X" as "count prefix pairs that differ by X."

</Callout>

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k/) | key the map on `pre mod k` instead of the raw prefix | — |
| [Contiguous Array (equal 0s and 1s)](https://leetcode.com/problems/contiguous-array/) | treat 0 as −1; a subarray is balanced when two prefixes are equal | — |
| [Continuous Subarray Sum (multiple of k)](https://leetcode.com/problems/continuous-subarray-sum/) | same `mod k` bucketing, but store the earliest index to enforce a length ≥ 2 | — |
| [Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/) | count prefixes equal to `pre − goal` | — |

### Difference Array <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/)*

<ProgressCheck id="difference-array-range-update" />

### Problem
You're given many **range updates** — each adds `v` to every element in `[l, r]` — and you only need the final array *after* all updates. Do it in O(n + m), not O(n·m).

**Constraints:** `n` slots, `m` updates, each `1 ≤ l ≤ r ≤ n`; running totals can exceed int → use `long`.

**Example 1:** `n = 5`, bookings `[1,2,10], [2,3,20], [2,5,25]` → `[10,55,45,25,25]`.

**Example 2:** `n = 3`, bookings `[1,1,5]` → `[5,0,0]` (single-point range closes immediately after index 0).

<ExamplePreview compact :input="['3']" :output="['1', '1', '5']" />

### Solution — brute force
Start with the direct baseline: enumerate every candidate and compute the answer from scratch. It is correct, but it repeats the exact work that the pattern is meant to reuse.



```java
int[] corpFlightBookingsBrute(int[][] bookings, int n) {
    int[] res = new int[n];
    for (int[] b : bookings)
        for (int i = b[0] - 1; i <= b[1] - 1; i++) res[i] += b[2];
    return res;
}
```



**Brute-force cost:** O(n·m) time, O(n) output space — too slow when both flights and bookings are large.

### Solution — optimized
A range add can be represented by two endpoint marks: start adding at `l`, stop adding after `r`. One final prefix pass turns those marks into the actual per-index totals.

**Pattern.**
Invert prefix sum: to add `v` to `[l, r]`, do `diff[l] += v; diff[r+1] -= v`. One final prefix sum materializes all updates.

**Java.**


```java
// Corporate Flight Bookings: bookings[i] = {first, last, seats} (1-indexed)
int[] corpFlightBookings(int[][] bookings, int n) {
    long[] diff = new long[n + 1];
    for (int[] b : bookings) {
        diff[b[0] - 1] += b[2];
        diff[b[1]]     -= b[2];
    }
    int[] res = new int[n];
    long run = 0;
    for (int i = 0; i < n; i++) { run += diff[i]; res[i] = (int) run; }
    return res;
}
```



### Time Complexity
Existing summary: Time O(n + m) · Space O(n).

Processing m bookings is O(m) because each update writes two diff cells; reconstructing n flights is O(n), so total time is O(n + m).

### Space Complexity
Space is O(n) for the difference array and output array. The extra `+1` slot is a boundary sentinel for closing ranges at the end.

### Learning notes
- Why `long[] diff`? — many bookings can accumulate beyond int during reconstruction.
- Why `b[0] - 1`? — bookings are 1-indexed, Java arrays are 0-indexed.
- Why `diff[b[1]] -= b[2]`? — `b[1]` is the first index after the inclusive range.
- Why length `n + 1`? — ranges ending at flight n need a safe closing decrement.
- Why one prefix pass? — the running sum materializes all active increments.

<Callout kind="key" title="Key Insight">

Batch many range increments in O(1) each, then reconstruct in O(n). Ideal when all updates precede all queries.

</Callout>

<Callout kind="inv" title="Invariant">

After processing, `prefix(diff)[i]` equals the net of all increments covering index `i`.

</Callout>

<Callout kind="note" title="Trace it">

`n=5`, bookings `[1,2,10],[2,3,20],[2,5,25]`. Endpoint marks then one prefix pass → per-flight seats `[10,55,45,25,25]` — three range adds settled in one sweep.

</Callout>

<Callout kind="trap" title="Common Trap">

Off-by-one at `r+1`; size the array `n+1` so the closing decrement never overflows the bounds.

</Callout>


<CodeTrace
  title="Corporate Flight Bookings — n=5, three bookings"
  :values="[0,0,0,0,0]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { diff: "[10,0,-10,0,0,0]" }, note: "booking [1,2,10] → diff[0]+=10, diff[2]-=10" },
    { pointers: { i: 1 }, vars: { diff: "[10,20,-10,-20,0,0]" }, note: "[2,3,20] → diff[1]+=20, diff[3]-=20" },
    { pointers: { i: 2 }, vars: { diff: "[10,45,-10,-20,0,-25]" }, note: "[2,5,25] → diff[1]+=25, diff[5]-=25" },
    { pointers: { i: 0 }, vars: { seats: "[10,_,_,_,_]" }, note: "prefix pass: seats[0]=10", added: [0] },
    { pointers: { i: 1 }, vars: { seats: "[10,55,_,_,_]" }, note: "seats[1]=10+45=55", added: [1] },
    { pointers: { i: 2 }, vars: { seats: "[10,55,45,_,_]" }, note: "seats[2]=55−10=45", added: [2] },
    { pointers: { i: 3 }, vars: { seats: "[10,55,45,25,_]" }, note: "seats[3]=45−20=25", added: [3] },
    { pointers: { i: 4 }, vars: { seats: "[10,55,45,25,25]" }, note: "seats[4]=25+0=25 — final", added: [4] }
  ]'
/>

<Callout kind="pat" title="Pattern Connection">

2D difference arrays handle sub-rectangle increments; combined with a 2D prefix sum they answer *Range Sum Query 2D* in O(1) per query.

</Callout>

### Same pattern, new tweaks

"Mark the endpoints of each range, then one prefix pass materializes all updates" scales across dimensions:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/) | +seats at `first`, −seats after `last`; one sweep gives per-flight totals | — |
| [Car Pooling](https://leetcode.com/problems/car-pooling/) | a difference array over the *timeline* of pick-ups (+) and drop-offs (−); check capacity never overflows | — |
| [Range Addition](https://leetcode.com/problems/range-addition/) | the canonical form — apply many `[l, r] += v` in O(1) each, reconstruct once | O(1) |
| [2D — Range Addition II / stamping a grid](https://leetcode.com/problems/range-addition-ii/) | a 2D difference array marks the four corners of each rectangle | — |

### 2D Prefix Sum <span class="diff diff-m">Medium</span>
*[↗ LeetCode: Range Sum Query 2D](https://leetcode.com/problems/range-sum-query-2d-immutable/)*

### Problem
Preprocess an **immutable** matrix so each query *"sum of the sub-rectangle from (r1,c1) to (r2,c2)"* answers in O(1).

**Constraints:** grid up to ~200×200; many queries → build once, then O(1) each.

**Example 1:** on `[[3,1],[2,4]]`, `sumRegion(0,0,1,1) = 10` (the whole grid); `sumRegion(1,1,1,1) = 4`.

**Example 2:** on `[[5]]`, `sumRegion(0,0,0,0) = 5` (padding handles the smallest rectangle).

<ExamplePreview compact :input="['[[5]]']" :output="['5']" />

### Solution — brute force
Start with the direct baseline: enumerate every candidate and compute the answer from scratch. It is correct, but it repeats the exact work that the pattern is meant to reuse.



```java
class NumMatrixBrute {
    private final int[][] m;
    NumMatrixBrute(int[][] matrix) { m = matrix; }
    int sumRegion(int r1, int c1, int r2, int c2) {
        int sum = 0;
        for (int r = r1; r <= r2; r++)
            for (int c = c1; c <= c2; c++) sum += m[r][c];
        return sum;
    }
}
```



**Brute-force cost:** O(R·C) per query in the worst case, O(1) extra space — too slow when many queries arrive.

### Solution — optimized
The optimized class pays one preprocessing pass to build a padded 2D prefix table. Every query then becomes four table lookups using inclusion–exclusion.

**Java.**


```java
class NumMatrix {
    private final long[][] P;
    NumMatrix(int[][] m) {
        int R = m.length, C = m[0].length;
        P = new long[R + 1][C + 1];
        for (int i = 0; i < R; i++)
            for (int j = 0; j < C; j++)
                P[i+1][j+1] = m[i][j] + P[i][j+1] + P[i+1][j] - P[i][j];
    }
    int sumRegion(int r1, int c1, int r2, int c2) {
        return (int)(P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]);
    }
}
```



Time: O(RC) build, O(1) query.

### Time Complexity
Building `P` is O(RC) because each matrix cell contributes to one prefix-table cell. Each `sumRegion` call is O(1) because it reads four precomputed corners.

### Space Complexity
Space is O(RC) for the padded prefix table `P`; the extra top row and left column simplify boundary math.

### Learning notes
- Why `long[][] P`? — rectangle sums can be larger than one cell value.
- Why size `R + 1` by `C + 1`? — padding makes boundary queries safe.
- Why write `P[i+1][j+1]`? — prefix indices mean sum before this row/col boundary.
- Why subtract `P[i][j]` while building? — the top-left rectangle was added twice.
- Why the query has `- - +` terms? — subtract top/left strips, then add back their overlap.

<Callout kind="key" title="Key Insight">

Inclusion–exclusion: `sum(r1,c1,r2,c2) = P[r2+1][c2+1] − P[r1][c2+1] − P[r2+1][c1] + P[r1][c1]`.

</Callout>

<Callout kind="note" title="Trace it">

`m=[[3,1],[2,4]]`. The padded prefix table gives `sumRegion(0,0,1,1) = P[2][2] − P[0][2] − P[2][0] + P[0][0] = 10 − 0 − 0 + 0 = 10` (the whole grid), and `sumRegion(1,1,1,1)=4` (just the corner).

</Callout>

<CodeTrace
  title="2D Range Sum — matrix [[3,1],[2,4]], query sumRegion(1,1,1,1)"
  :values="[3,1,2,4]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { P: "[[0,0,0],[0,3,4],[0,5,10]]" }, note: "build prefix P with 1-row/col padding" },
    { pointers: { i: 3 }, vars: { r1: 1, c1: 1, r2: 1, c2: 1 }, note: "query (1,1)-(1,1) → single cell", added: [3] },
    { pointers: { i: 0 }, vars: { formula: "P[2][2] − P[1][2] − P[2][1] + P[1][1]" }, note: "10 − 4 − 5 + 3 = 4 ✓" }
  ]'
/>

<Callout kind="inv" title="Invariant">

`P[i][j]` holds the sum of the sub-rectangle from `(0,0)` to `(i-1,j-1)`; the padding row/column of zeros makes every query boundary-safe.

</Callout>

<Callout kind="trap" title="Common Trap">

Sign/index errors in the four-term formula, or omitting the `+1` padding — then corner queries read out of bounds. Add back the double-subtracted corner (`+ P[r1][c1]`).

</Callout>

<Callout kind="pat" title="Pattern Connection">

The +/−/− /+ inclusion–exclusion pattern reappears in *Maximal Rectangle* accounting and 2D sweep problems.

</Callout>

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Matrix Block Sum](https://leetcode.com/problems/matrix-block-sum/) | answer each cell as the sum of a `k`-radius block using the same four-corner formula | — |
| [Count Submatrices With Target Sum](https://leetcode.com/problems/count-submatrices-with-target-sum/) | fix a pair of rows, collapse columns to 1D prefix sums, then reuse the "subarray sum = k" hash-map count | — |
| [Maximal Square / Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | combine per-row prefix counts with a histogram/DP to bound the largest all-ones region | — |

### Prefix XOR <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Count Triplets That Can Form Two Arrays of Equal XOR](https://leetcode.com/problems/count-triplets-that-can-form-two-arrays-of-equal-xor/)*

#### Problem
Count contiguous subarrays whose XOR equals `k`. Values are non-negative, up to ~`10^9`; `n ≤ 10^5`.

**Why not a sliding window?** XOR is **not monotone** as the window grows — adding an element can either raise or lower the running XOR depending on bit patterns. The sliding-window shrink step is undefined.

#### Solution — brute force



```java
int subarrayXorBrute(int[] a, int k) {
    int ans = 0;
    for (int l = 0; l < a.length; l++) {
        int x = 0;
        for (int r = l; r < a.length; r++) {
            x ^= a[r];
            if (x == k) ans++;
        }
    }
    return ans;
}
```



O(n²) time, O(1) space.

#### Solution — optimized

The exact same trick as "subarray sum = k", with the sole substitution `+` → `^`. The algebraic property that makes it work: **XOR is its own inverse** — `pre_r ^ pre_l = k` iff `pre_l = pre_r ^ k`. So lookup `(running ^ k)` in a hash map at each step.

<Callout kind="key">

Count the contiguous subarrays whose XOR equals k.

</Callout>

<TemplateReveal
  slug="prefix-xor"
  language="java"
  :canonical="prefixXorCode"
/>

<Callout kind="inv" title="Invariant">

`count[v]` holds the number of indices `i` for which `a[0] ^ a[1] ^ … ^ a[i-1] = v`. At each new index, we read how many earlier prefixes satisfy `pre_l = running ^ k`.

</Callout>

**Complexity:** O(n) time, O(n) space.

**Classic application — Contiguous Array (equal 0s and 1s):** map `0 → -1, 1 → +1` (so the running sum tracks "excess of 1s over 0s"). The longest subarray with equal 0s and 1s is the longest span where the same running value appears twice — a hash map of first-seen indices does it in O(n).

### Prefix Mod <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k/)*

#### Problem
Count contiguous subarrays whose sum is divisible by `k`. Values can be negative; `n ≤ 3·10^4`, `|a[i]| ≤ 10^4`, `2 ≤ k ≤ 10^4`.

#### The move — bucket prefixes by residue

A subarray `(l, r]` has `(pre_r - pre_l) ≡ 0 (mod k)` **iff** `pre_r ≡ pre_l (mod k)`. So keep a histogram of running residues: every pair of prefixes in the same bucket is a divisible subarray.

For `k = 5` and residues `[0, 2, 1, 2, 0, 2]`, bucket 0 has two indices (gives `C(2,2) + 1 = 1` subarray starting at empty prefix × 2 others), bucket 2 has three (`C(3,2) = 3`), bucket 1 has one. Total divisible subarrays = `C(2,2)·… + …`.

<Callout kind="key">

Count the contiguous subarrays whose sum is divisible by k.

</Callout>

<TemplateReveal
  slug="prefix-mod"
  language="java"
  :canonical="prefixModCode"
/>

<Callout kind="inv" title="Invariant">

`countByResidue[r]` holds the number of processed prefixes with `pre ≡ r (mod k)`. The answer increments by `countByResidue[running]` at each step, then we record the current prefix.

</Callout>

**Negative-aware canonicalization.** `((x % k) + k) % k` turns Java's symmetric mod (`-1 % 5 = -1`) into the mathematical residue (`4`). Without this line, every negative value corrupts the residue bucketing and the count comes out wrong by a factor of ~2.

**Complexity:** O(n + k) time, O(k) space — the residue table has exactly `k` cells. If `k ≤ n`, this is strictly better than the hash-map variant (array indexing beats hashing in constants).

**Variation — [Continuous Subarray Sum (523)](https://leetcode.com/problems/continuous-subarray-sum/):** instead of the count, you want *whether any such subarray of length ≥ 2 exists*. Store the **first** index each residue was seen at (not the count) and check `r - firstIndex[running] ≥ 2`.

## In the wild — NumPy cumsum & TF XLA scan

**NumPy's `np.cumsum`** is a one-line user API over a C-level in-place loop:



```c
/* numpy/core/src/multiarray/calculation.c — slight simplification */
PyObject* PyArray_CumSum(PyArrayObject *self, int axis, int rtype, PyArrayObject *out) {
    PyArrayObject *ret = /* alloc or alias out */;
    /* reduceat implements the running fold via BLAS/looping; for float64 it dispatches
       to a pairwise summation ladder to keep rounding error at O(log n) instead of O(n). */
    return PyArray_GenericAccumulateFunction(self, n_ops.add, axis, rtype, ret);
}
```



The pairwise-summation detour is why `np.cumsum([1e20, 1, -1e20])` returns a different last value than a naive left-fold on `float64` — numerical stability matters once prefixes run over million-element inputs.

**TensorFlow's `tf.cumsum` compiled through XLA** emits an `HloInstruction::Scan` node that, on GPU, becomes a **Blelloch exclusive scan** (section "History" above):

```c++
// tensorflow/compiler/xla/service/gpu/scan_thunk.cc — paraphrased
// Launch (n / block_size) blocks of block_size threads.
// Phase 1 (up-sweep):  each block computes its local scan in shared memory in O(log block_size) depth.
// Phase 2 (down-sweep): a second kernel propagates block prefixes to get the global scan.
// Total depth: O(log n). Total work: O(n). Memory bandwidth bound in practice.


```

The exact code was the subject of Harris, Sengupta & Owens' GPU Gems 3 chapter — the first widely-cited GPU implementation of Blelloch's algorithm.

**Real production uses of prefix sum / difference array:**
1. **FFmpeg's `AVFrame` SAD computation** uses summed-area tables (2D prefix sum) to score motion-estimation candidates in constant time per block.
2. **PostgreSQL's `width_bucket` on sorted histogram boundaries** is a prefix-sum lookup over bucket counts.
3. **Linux kernel's `__percpu` counter batching** uses the difference-array trick: each CPU accumulates deltas locally; a periodic prefix-reduce updates the global counter without cross-CPU locks on every write.
4. **Pandas' `rolling().sum()` fast path** on numeric columns picks between a running-sum loop and a prefix-sum table based on `window / len` ratio; XLA's codegen for `jnp.cumsum` is the same algorithm applied one dimension at a time.

## When NOT to use it

- **You need range operations other than sum** — prefix sum extends to prefix-max only for immutable arrays; prefix-min/max with updates is a **segment tree**, not prefix sum.
- **The array is dynamic (values change between queries)** — prefix sum recomputes from scratch after every update. If you have thousands of updates interleaved with queries, use a **Fenwick tree (BIT)** or **segment tree** for O(log n) both.
- **Just one query on the whole array** — prefix sum's prep cost equals the query cost. Just accumulate in a single loop.
- **Multi-dimensional ranges beyond 2D** — 3D prefix sum works but memory is O(nmp) and inclusion-exclusion has 8 terms. Consider whether the problem really needs that dimensionality.
- **The subarray-sum target is 0 and the array is all zeros** — degenerate case; the count blows up quadratically. Handle explicitly.

## Recognition drill

<RecognitionDrill pattern="prefix-sum" :count="10" />

## Advanced — follow-ups and failure modes

<details>
<summary><strong>What if the array has point updates between queries?</strong></summary>

Prefix sum becomes O(n) per update — unacceptable at `Q = 10^5`. Switch to a **Fenwick tree (BIT)** for `O(log n)` update + `O(log n)` prefix. The invariant mutates from "snapshot" to "incrementally maintained running total":

```java
void update(int i, long delta) {           // 1-indexed
    for (; i <= n; i += i & -i) bit[i] += delta;
}
long prefix(int i) {
    long s = 0;
    for (; i > 0; i -= i & -i) s += bit[i];
    return s;
}
```



Range sum: `prefix(r) - prefix(l-1)`. Same mental model, log-factor cost.
</details>

<details>
<summary><strong>What if queries are on a 1D sliding window of fixed size k?</strong></summary>

You don't need a full prefix array — a single running sum with `add(a[r]) + subtract(a[r-k])` gives O(1) extra space:



```java
long sum = 0;
for (int i = 0; i < a.length; i++) {
    sum += a[i];
    if (i >= k) sum -= a[i - k];
    if (i >= k - 1) emitWindowSum(i, sum);
}
```



Prefix sum works too but allocates O(n) when O(1) was free.
</details>

<details>
<summary><strong>What if values are reals and precision matters?</strong></summary>

Naive accumulation accumulates error at O(n) in the worst case. Fixes:

- **Kahan summation** — compensated accumulation; one extra `float` tracks the lost low-order bits. Reduces error to O(1).
- **Pairwise summation** — recursive halving (what NumPy's `reduceat` uses). O(log n) error with the same asymptotics as the naive loop.

The algorithmic skeleton stays the same; the inner update changes from one add to four. For financial accounting problems, use fixed-point integers instead — different world, same lesson.
</details>

<details>
<summary><strong>What if the matrix is sparse but queries are dense?</strong></summary>

A dense 2D prefix table costs O(RC) build and O(RC) space even when most cells are 0. If the matrix has `K ≪ RC` non-zero cells and you need `Q` rectangle queries:

- `K · Q` ≤ RC → naive scan wins.
- `K + Q log K ≪ RC` → Fenwick tree on coordinates, or offline CDQ divide-and-conquer over events.

The win: avoid materializing the full prefix table. Also the pattern used by competitive-programming problems like SPOJ MATSUM in sparse mode.
</details>

<details>
<summary><strong>What if the array is distributed across GPU threads?</strong></summary>

The sequential O(n) build loop is now the bottleneck — 10^8 elements on one GPU core is slow. Blelloch's **parallel prefix (scan)** gives O(log n) depth with O(n) total work:

1. **Up-sweep** — build a reduction tree where each node holds the sum of its subtree.
2. **Down-sweep** — propagate exclusive prefixes top-down.

Thrust's `inclusive_scan` and TensorFlow's XLA scan both implement this. The same primitive underlies parallel sort, parallel compaction, and histogram-building on GPUs.
</details>

### Breaking point

Prefix sum **stops being optimal** when:
- Updates interleave with queries → Fenwick tree (O(log n) both).
- The aggregation operation is not invertible (max, min) → segment tree or sparse table.
- You need the *k*-th smallest in a range, not a sum → wavelet tree or merge-sort tree.
- Dimensions &gt; 2 and queries are rectangles → inclusion-exclusion has `2^d` terms; usually re-formulate.
- Updates are range-add AND queries are range-sum interleaved → BIT with difference-array trick (two Fenwicks).

### Three cross-pattern problems

- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) — a trap problem: looks like it wants prefix sum, actually wants a **monotonic deque** (max isn't invertible).
- [Range Sum Query — Mutable (307)](https://leetcode.com/problems/range-sum-query-mutable/) — the natural bridge from prefix sum to **Fenwick tree**.
- [Count Vowel Strings in Ranges](https://leetcode.com/problems/count-vowel-strings-in-ranges/) — prefix-count over a bitmap; stripped-down demonstration of the pattern on a boolean sequence.

---

## Check your understanding

<Quiz pattern-id="prefix-sum" :questions="mastery5" />

<PrintButton />

<RelatedPatterns pattern-id="prefix-sum" />
