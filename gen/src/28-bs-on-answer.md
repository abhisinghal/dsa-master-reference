# Binary Search on the Answer


<PatternVideo pattern-name="Binary Search on the Answer" duration="8–12 min" />

<PatternProgress pattern-id="bs-on-answer" problems="koko-bananas, capacity-to-ship-packages-within-d-days, split-array-largest-sum, median-of-two-sorted-arrays, kth-smallest-element-in-a-sorted-matrix, find-k-th-smallest-pair-distance, minimize-max-distance-to-gas-station, path-with-minimum-effort, divide-chocolate" />

<script setup>
const theTemplateCode = `int searchOnAnswer(int lo, int hi) {
    while (lo < hi) {                      // half-open convention
        int mid = lo + (hi - lo) / 2;      // Bloch overflow fix
        if (feasible(mid)) hi = mid;       // works — but maybe smaller works too
        else               lo = mid + 1;   // doesn't work — need bigger
    }
    return lo;                             // smallest feasible answer
}`

const theTemplateInvariant = {
  statement: `Every value x < lo has been proven infeasible; every value x ≥ hi is guaranteed feasible. On exit lo == hi, which is the smallest feasible answer (the first-true boundary).`,
  initialization: `Pick lo as the smallest value that could plausibly work, hi as any value you can prove is feasible. feasible(lo) may be false; feasible(hi) must be true.`,
  maintenance: `At each step mid = lo + (hi - lo) / 2 (overflow-safe). If feasible(mid), tighten hi = mid (mid might be the answer). If not, bump lo = mid + 1 (everything ≤ mid is infeasible).`,
  termination: `Each iteration halves (hi - lo). After ⌈log₂(hi - lo)⌉ iterations lo == hi, and by the invariant that value is both proven infeasible-below and feasible.`
}

const theTemplateComplexity = {
  time: `O(log(hi − lo) · f(n))  — f(n) is one feasibility check`,
  space: `O(1) for the search; feasibility may add its own`
}

const theTemplateSpecializations = [
  { slug: `capacity-to-ship-within-d-days-medium`,  title: `Capacity to Ship (medium)` },
  { slug: `koko-eating-bananas-medium`,             title: `Koko Eating Bananas (medium)` },
  { slug: `find-the-smallest-divisor-medium`,       title: `Smallest Divisor (medium)` },
  { slug: `split-array-largest-sum-hard`,           title: `Split Array Largest Sum (hard)` },
  { slug: `median-of-two-sorted-arrays-hard`,       title: `Median of Two Sorted Arrays (hard)` },
]

const theTemplateProblemShape = `Minimize/maximize a numeric answer subject to a monotone feasibility predicate — "smallest x where feasible(x) is true" or "largest x where feasible(x) is true". Each feasibility probe is a greedy or simulated O(n)/O(n log n) check.`

const capacityToShipCode = `int shipWithinDays(int[] weights, int days) {
    int lo = 0, hi = 0;
    for (int w : weights) { lo = Math.max(lo, w); hi += w; }
    while (lo < hi) {
        int cap = lo + (hi - lo) / 2;
        if (daysNeeded(weights, cap) <= days) hi = cap;
        else                                   lo = cap + 1;
    }
    return lo;
}

int daysNeeded(int[] weights, int cap) {
    int days = 1, load = 0;
    for (int w : weights) {
        if (load + w > cap) { days++; load = w; }
        else                 load += w;
    }
    return days;
}`

const smallestDivisorCode = `int smallestDivisor(int[] nums, int threshold) {
    int lo = 1, hi = 0;
    for (int x : nums) hi = Math.max(hi, x);
    while (lo < hi) {
        int d = lo + (hi - lo) / 2;
        long sum = 0;
        for (int x : nums) sum += (x + d - 1) / d;    // ceil division
        if (sum <= threshold) hi = d;                  // feasible → try smaller d
        else                  lo = d + 1;              // infeasible → bigger d
    }
    return lo;
}`

const mastery5 = [
  {
    q: `What TWO ingredients are required to apply "Binary Search on the Answer"?`,
    choices: [
      { text: `A monotonic feasibility predicate + a bounded answer range`, correct: true, explanation: `Without monotonicity you can't eliminate halves. Without bounds you can't initialize the search.` },
      { text: `A sorted input array`, correct: false, explanation: `The INPUT need not be sorted. The ANSWER space is monotone.` },
      { text: `The answer must be an integer`, correct: false, explanation: `Real-valued answers work with epsilon convergence.` },
      { text: `A recursive feasibility check`, correct: false }
    ]
  },
  {
    q: `For Koko Eating Bananas, if feasible(k) returns "is total hours ≤ h" and feasible(1) is false, feasible(max(piles)) is true, which direction tightens on feasible = true?`,
    choices: [
      { text: `hi = mid — try smaller k, because true at this k means true at every larger k`, correct: true, explanation: `We want the smallest feasible k. If k works, maybe k-1 does too.` },
      { text: `lo = mid + 1 — need faster speed`, correct: false, explanation: `That's the direction on feasible = false.` },
      { text: `lo = mid, since mid might be the answer`, correct: false, explanation: `Breaks the half-open convention and can loop forever.` },
      { text: `hi = mid - 1, excluding mid from the range`, correct: false, explanation: `Excludes a potential answer.` }
    ]
  },
  {
    q: `What's the overall complexity of binary-searching an integer answer in [1, R] where each feasibility check is O(n)?`,
    choices: [
      { text: `O(n log R)`, correct: true, explanation: `log₂ R probes × O(n) per probe.` },
      { text: `O(n R)`, correct: false, explanation: `That's "try every answer".` },
      { text: `O(log n log R)`, correct: false },
      { text: `O(n²)`, correct: false }
    ]
  },
  {
    q: `For Median of Two Sorted Arrays, which array should you binary-search the partition on?`,
    choices: [
      { text: `The SHORTER array — bounds the search range to O(log min(m,n))`, correct: true, explanation: `Also keeps j = half - i within the longer array's valid range.` },
      { text: `The LONGER array — more partition options`, correct: false, explanation: `Blows up the search range unnecessarily.` },
      { text: `Either — asymptotically identical`, correct: false, explanation: `log m vs log n differs; pick the min for a tighter bound.` },
      { text: `Whichever is sorted ascending`, correct: false, explanation: `Both are sorted.` }
    ]
  },
  {
    q: `A real-valued BS on answer (e.g. Minimize Max Distance to Gas Station). What termination condition?`,
    choices: [
      { text: `Iterate until hi - lo < ε for a chosen ε, OR fix 100 iterations (each halves)`, correct: true, explanation: `Fixed 100 iterations gives precision 2^-100 ≈ 10^-30 of the initial range — safe for doubles.` },
      { text: `while (lo < hi) — the integer loop`, correct: false, explanation: `Infinite loop on doubles.` },
      { text: `while (lo != hi) — exact equality on doubles`, correct: false, explanation: `Floating-point equality after halving is unreliable.` },
      { text: `Cast everything to int`, correct: false, explanation: `Loses precision.` }
    ]
  }
]
</script>



## Why binary search on the answer exists — the story

You are a warehouse manager. You have `n` shipments to deliver in `D` days. You must decide the **truck capacity** — every truck sends out a whole day's shipments, in order, up to the capacity. What is the *smallest* capacity that lets you deliver all `n` shipments in `D` days?

The brute honest approach: **try every capacity, one by one.** Start at capacity 1 (obviously too small — one shipment might exceed it), then 2, then 3, ... until one works. Each try runs a simulation: fill trucks day by day, count days used, compare to `D`.

For small answer ranges this works. If capacity is bounded by `50`, you run 50 simulations, each O(n). Total O(50n). Junior devs write this on the first try, it passes tests, everyone goes home.

But the interviewer says: capacity can be up to `10⁹` and `n = 10⁵`. Now brute force is `10⁹ × 10⁵ = 10¹⁴` operations — **32 years** on a laptop. Every single one of those simulations is throwing away information: if capacity `42` doesn't work, then capacity `41`, `40`, and every smaller value also don't work — you don't need to test them. And if capacity `500` *does* work, you don't need to test `501, 502, ..., 10⁹`.

The pattern is: recognize that `feasible(capacity)` is **monotonic** — a step function that is `false` up to the true answer, then `true` forever after. That means the answer space is a *sorted boolean array*, and binary search finds the boundary in `log₂(10⁹) ≈ 30` steps. **32 years → 3 milliseconds.** The full technique family is called *parametric search*, formalized by Nimrod Megiddo in 1979.

## The core idea — the answer *space* is what you binary-search

<BinarySearchAnim />

Classical binary search finds a target inside a sorted array. This variant finds the *smallest* (or largest) value in a *numeric range* satisfying a monotonic predicate. Two shifts of mindset:

1. **The array is imaginary.** You never allocate it. It exists only in the sense that `feasible(x)` for `x = lo, lo+1, ..., hi` is a boolean array — false, false, ..., false, true, true, ..., true. The boundary between the falses and trues is the answer.

2. **Each "read" is a simulation.** In classical binary search, `a[mid]` is O(1). In BS-on-answer, `feasible(mid)` is often O(n) or O(n log n) — you simulate the process (fill trucks, eat bananas, cross the ocean) for the candidate `mid` and count something to check feasibility.

Total cost: **O(log(hi − lo) × cost of one feasibility check).** For most interview problems this is `O(n log R)` where R is the answer range.

## When to use it — recognition signals

The problem statement almost always contains one of these clue phrases:

- **"Minimum X such that ..."** — Koko Eating Bananas ("min speed to finish in H hours"), Capacity to Ship Packages ("min capacity to ship in D days"), Split Array Largest Sum ("min largest subarray sum when splitting into k parts").
- **"Maximum X such that ..."** — Divide Chocolate ("max sweetness when cutting into k+1 pieces"), Magnetic Force Between Two Balls ("max minimum distance").
- **"Minimize the maximum" or "maximize the minimum"** — this "min-of-max" or "max-of-min" framing is *almost always* BS-on-answer.
- **The answer is a real number** — capacity, speed, threshold, time, distance. Not an index into an array.
- **You can build a `feasible(x)` function that runs in ≤ O(n log n).** If checking a candidate takes exponential time, this pattern doesn't help.
- **The naive "try every answer" is too slow.** If the answer range is ≤ ~1,000 and each check is O(n), maybe don't bother — plain iteration might be simpler. It's only when the answer range is 10⁶ or 10⁹ that BS-on-answer pays for the extra complexity.

## When NOT to use it

- **`feasible(x)` is not monotonic.** If some intermediate `x` fails but a smaller `x` succeeds, the boolean array is not sorted, and binary search silently returns garbage. **Verify monotonicity on paper before coding.** Common gotcha: "path with minimum effort" — is the feasibility of a max-effort threshold monotonic? Yes. Is "there exists a path of length ≥ k on a grid" monotonic in k? Also yes. But "the sum of digits equals k" is not monotonic in k.
- **The answer isn't a number** — if the answer is a subset, a path, a permutation, or a graph, you can't binary-search a *value*. Combine with another technique.
- **Feasibility itself requires solving another hard problem** — if `feasible(x)` needs an NP-hard subroutine, wrapping it in binary search doesn't rescue you.
- **The answer range is tiny** — `1 ≤ x ≤ 50` and each check is O(n)? Just iterate. Binary search adds constants and cognitive load with no asymptotic benefit at that scale.
- **You need all valid answers, not the boundary** — BS-on-answer returns one number. If the interviewer wants "all speeds that work", the pattern doesn't fit.

## THE template — one loop, two moving parts

<PatternTemplateCard
  slug="bs-on-answer"
  title="Binary Search on the Answer"
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

### The five canonical problems in this pattern

| Problem | `feasible(x)` | `lo` | `hi` |
|---|---|---|---|
| **Capacity to Ship** | packing in order at capacity `x` uses `≤ D` days | `max(weights)` | `sum(weights)` |
| Koko Bananas | eating at `x`/hr finishes in `≤ H` hrs | `1` | `max(piles)` |
| Smallest Divisor | `Σ ceilDiv(a[i], x) ≤ threshold` | `1` | `max(nums)` |
| Split Array Largest Sum | greedy splits with cap `x` produce `≤ k` groups | `max(nums)` | `sum(nums)` |
| Median of Two Sorted Arrays | count of values `≤ x` is `≥ (n+1)/2` | `min` of both | `max` of both |

Pattern: `lo` and `hi` are almost always `max(inputs)` and `sum(inputs)`, or the smallest/largest values in the input range. Get these bounds right and the rest is mechanical.

### Complexity ladder

| Approach | Time | Space | When to use |
|---|---|---|---|
| Brute try-every-answer | O(R · f(n)) | O(1) | Only if R is small (≤ 1000) |
| **Binary search on answer** | **O(log R · f(n))** | **O(1)** | **Every real interview answer** |

Where `R = hi - lo` and `f(n)` is one feasibility check — typically O(n) for pack/greedy, O(log n) for a partition BS, O(n log n) when feasibility sorts.

## When the mechanic breaks — three failure modes

<TrapTrace
  title="feasible(x) isn't monotonic"
  bug="The single most fatal mistake. Interviewers love to disguise non-monotone problems as BS-on-answer. For 'count of distinct values ≤ k that are prime' the predicate oscillates with k. The binary search returns garbage with zero runtime signal."
  fix="Before coding, evaluate feasible(lo), feasible(hi), and feasible(mid) on paper. If both lo and hi are true (or both false), the predicate isn't monotone in the direction you think. If feasible flips multiple times across the range, binary search doesn't apply — iterate or re-formulate."
/>

<TrapTrace
  title="Feasibility check has an off-by-one — the ceiling-division trap"
  bug="In Koko Bananas or Smallest Divisor, the hours (or divisions) needed for a pile of p at speed k is ceil(p / k). Writing p / k gives integer floor and underestimates hours — feasibility incorrectly returns true, and you shrink hi too aggressively, returning a speed that doesn't actually work."
  fix="Use (p + k - 1) / k or Math.ceilDiv(p, k) for positive integers. Test it: ceilDiv(10, 3) = 4, not 3. If values can be negative or zero, handle those cases explicitly before the division."
/>

<TrapTrace
  title="Wrong bounds — hi too small or lo wrong direction"
  bug="For Split Array Largest Sum with weights that overflow int, you set hi = sum(all) as int → overflow → hi comes out negative → loop exits immediately with lo = hi returning garbage. Separately: if you set lo = 1 when the true minimum is max(weights), the loop still works (just wastes 20 iterations) — but if lo > true answer, you return the wrong answer."
  fix="Use long for lo/hi/mid whenever sum(inputs) could exceed 2·10^9. Pick lo as the SMALLEST input that could make feasible true (max(weights) for shipping; 1 for divisors). Pick hi as any value you can prove is feasible (sum(weights) ships everything in one day). Overshooting hi costs one log step; undershooting it returns a value that fails feasibility."
/>


## History — Megiddo's parametric search, 1979

The technique of turning an optimization problem into a decision problem was formalized by **Nimrod Megiddo** in 1979 as **parametric search**. His paper *"Combinatorial optimization with rational objective functions"* proved that many optimization problems in computational geometry could be reduced to a sequence of feasibility tests, each solvable in polynomial time. The pattern powers the classical linear-programming and minimum-enclosing-circle algorithms.

In competitive programming, the technique was popularized on Codeforces and TopCoder in the mid-2000s under the informal name **"binary search on the answer."** LeetCode problems like Koko Eating Bananas (2019) and Capacity to Ship Packages Within D Days (2019) turned it into an interview staple.

## Sub-variations of the template

<PatternSubVariationNav pattern="bs-on-answer" />

### Capacity to Ship Within D Days <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Capacity to Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)*

The bare mechanic as a sub-variation. Packages must ship **in order** — so feasibility is a one-pass greedy count of days.

#### Problem
A conveyor belt has `weights` in a fixed order; a ship with capacity `cap` must take them in order, filling the ship each day up to `cap`. Return the minimum `cap` that finishes in `D` days.

**Constraints:** `1 ≤ weights.length ≤ 5·10^4`; `1 ≤ weights[i] ≤ 500`; `1 ≤ D ≤ weights.length`.

#### Solution — brute force

Try every capacity from `max(weights)` to `sum(weights)`, simulate for each: O(R · n) ≈ O(sum · n) ≈ 10^9 — too slow.

#### Solution — optimized

Monotone predicate: larger capacity → fewer-or-equal days. Greedy feasibility packs each day up to `cap` and counts days.

> [key] Minimum ship capacity so the packages (in order) deliver in D days.

<TemplateReveal
  slug="capacity-to-ship"
  language="java"
  :canonical="capacityToShipCode"
/>

> [inv] **Invariant** — `lo` tracks the smallest capacity that *might* work (every smaller cap proven infeasible). `hi` tracks a capacity that definitely works (`sum(weights)` ships everything in one day). After the loop, `lo == hi` is the first-true boundary.

**Why `lo = max(weights)` and not 1?** A single package must fit in one day's load. If `cap < max(weights)`, no number of days helps — the predicate is undefined, not just false. Setting `lo = max(weights)` avoids testing nonsense capacities.

**Trace** — `weights=[1,2,3,4,5,6,7,8,9,10], D=5`. `lo = 10, hi = 55`. Mid = 32: feasible with 2 days → tighten hi. Mid = 21: 2 days → tighten. Mid = 15: 3 days → tighten. Mid = 12: 4 days → tighten. Mid = 11: 5 days → tighten. Mid = 10: 10 days > 5 → loosen. Converges on **15**.

**Complexity:** O(n log(sum - max)) time, O(1) space.

**Classic variants** (same mechanic, different feasibility):
- [Aggressive Cows / Magnetic Force Between Two Balls](https://leetcode.com/problems/magnetic-force-between-two-balls/) — maximize the *minimum* gap between placed objects. Flip the search: `feasible(d) = can place ≥ k balls with every pair ≥ d apart`. Binary-search the largest `d`.
- [Boats to Save People](https://leetcode.com/problems/boats-to-save-people/) — technically a two-pointer problem; added here because the problem statement sounds identical.

### Koko Eating Bananas <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/)*

<ProgressCheck id="koko-eating-bananas-search-on-answer-rate" />

```svg
<svg role="img" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Diagram illustrating: Koko Eating Bananas (Search on Answer — rate) Medium">
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="27" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">binary search over the answer: eating rate k</text>

  <line x1="48" y1="72" x2="352" y2="72" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <circle cx="58" cy="72" r="6" fill="var(--dsa-primary)"/>
  <circle cx="342" cy="72" r="6" fill="var(--dsa-primary)"/>
  <line x1="202" y1="49" x2="202" y2="153" stroke="var(--dsa-primary)" stroke-width="2" stroke-dasharray="6 5"/>
  <text x="58" y="52" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">low=1</text>
  <text x="342" y="52" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">high=max</text>
  <text x="202" y="43" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">mid k=4</text>
  <text x="200" y="92" text-anchor="middle" font-size="11.5" fill="var(--dsa-neutral)">rate k</text>

  <g text-anchor="middle">
    <rect x="82" y="114" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <rect x="134" y="114" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <rect x="186" y="114" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
    <rect x="238" y="114" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <g font-size="17" font-weight="700" fill="var(--dsa-ink)">
      <text x="104" y="142">3</text><text x="156" y="142">6</text><text x="208" y="142">7</text><text x="260" y="142">11</text>
    </g>
    <g font-size="11" fill="var(--dsa-neutral)">
      <text x="104" y="173">1h</text><text x="156" y="173">2h</text><text x="208" y="173">2h</text><text x="260" y="173">3h</text>
    </g>
  </g>
  <rect x="100" y="186" width="200" height="28" rx="10" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <text x="200" y="205" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-success)">hours = 1+2+2+3 = 8 ≤ h=8</text>
  <text x="200" y="234" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">monotone predicate: feasible(k) is non-decreasing in k</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> Guess a rate, compute total hours with ceiling division, then use the yes/no result to keep the smallest feasible side of the search range.</div>

### Problem
Koko eats `k` bananas/hour (one pile per hour; leftovers still cost a full hour). Find the **minimum `k`** that finishes all piles within `h` hours.

**Constraints:** `1 ≤ piles.length ≤ 10⁴`; `piles.length ≤ h ≤ 10⁹`; pile sizes up to 10⁹.

**Example 1:** `piles = [3,6,7,11], h = 8` → `4`.

<ExamplePreview compact :input="['3', '6', '7', '11', '|', '8']" :output="['4']" />

**Example 2:** `piles = [30,11,23,4,20], h = 5` → `30`.

<ExamplePreview compact :input="['30', '11', '23', '4', '20', '|', '5']" :output="['30']" />

### Solution — brute force
Brute force tries every eating speed `k` from 1 up to the largest pile and simulates the total hours for each speed. The feasibility check is O(n), so this is O(n·maxPile) time and O(1) space, far too slow when pile sizes hit `10⁹`. The optimized version keeps the same feasibility check but binary-searches the monotone speed range for the first speed that works.

```java
int minEatingSpeedBrute(int[] piles, int h) {
    int max = 0;
    for (int p : piles) max = Math.max(max, p);
    for (int k = 1; k <= max; k++) {
        long hours = 0;
        for (int p : piles) hours += (p + k - 1) / k;
        if (hours <= h) return k;
    }
    return max;
}
```

O(n·maxPile) time, O(1) space — too slow when pile sizes can be 10⁹.

### Solution — optimized
Binary search the *eating speed*; feasibility "can finish within h hours at speed k" is monotone in k.

> [inv] **Invariant** — `feasible(k)` true ⇒ `feasible(k+1)` true. Find the minimum feasible k = first-true boundary over `[1, max(pile)]`.

The optimized version keeps the O(n) simulation but runs it only for O(log maxPile) guessed speeds. A feasible speed means "try slower"; an infeasible speed means "must go faster."

```java
int minEatingSpeed(int[] piles, int h) {
    int lo = 1, hi = 0;
    for (int p : piles) hi = Math.max(hi, p);
    while (lo < hi) {
        int k = lo + (hi - lo) / 2;
        long hours = 0;
        for (int p : piles) hours += (p + k - 1) / k;   // ceil division
        if (hours <= h) hi = k; else lo = k + 1;        // feasible -> go slower
    }
    return lo;
}
```

> [note] **Trace it** — `piles=[3,6,7,11], h=8`. Speed 4 takes `1+2+2+3 = 8` hours (feasible); speed 3 takes 10 (too slow). Binary search on speed lands on **4**.

<CodeTrace
  title="Koko Eating Bananas — piles=[3,6,7,11], h=8"
  :values="[3,6,7,11]"
  :windowKeys="['lo','hi']"
  :cellWidth="42"
  :steps='[
    { pointers: { lo: 1, hi: 11, mid: 6 }, vars: { hours: 6, ok: "yes" }, note: "speed 6 → 1+1+2+2=6 ≤ 8. try slower" },
    { pointers: { lo: 1, hi: 6, mid: 3 }, vars: { hours: 10, ok: "no" }, note: "speed 3 → 1+2+3+4=10. too slow" },
    { pointers: { lo: 4, hi: 6, mid: 5 }, vars: { hours: 8, ok: "yes" }, note: "speed 5 → 8 hrs. try slower" },
    { pointers: { lo: 4, hi: 5, mid: 4 }, vars: { hours: 8, ok: "yes" }, note: "speed 4 → 8 hrs. converges: answer 4" }
  ]'
/>

### Time Complexity
O(n log(maxPile)), because each feasibility check scans all piles once, and binary search performs O(log maxPile) checks.

### Space Complexity
O(1), because the search stores only bounds and the running `hours` counter.

> [note] **Interview script** — "I first confirm Koko chooses one integer speed and every partially eaten pile still costs a full hour. I start with brute force by trying every speed and simulating hours, which is O(n·maxPile) time and O(1) space. I optimize by binary-searching the first feasible speed, using the same O(n) check, for O(n log maxPile) time and O(1) space."


> [key] **Key Insight** — The moment you see "minimum speed/capacity/time such that a constraint holds," define `feasible(x)` as an O(n) check and binary-search x. The array order is irrelevant; the *answer* is what's monotone.

> [trap] **Common Trap** — Feasibility direction flipped. *Example:* `piles=[3,6,7,11]`, `h=8`. If `feasible(speed)` returns `true` when speed is too slow, binary search converges to the fastest failing speed. Sanity-check: `feasible(min)` should be `false` and `feasible(max)` should be `true`.

<CodeTrace
  title="Trap — Feasibility flipped: piles=[3,6,7,11], h=8"
  :values="[3,6,7,11]"
  :windowKeys="['lo','hi']"
  :cellWidth="46"
  :steps='[
    { pointers: { lo: 1, hi: 11, mid: 6 }, vars: { hours: 6, "flipped": "hours gt h → false" }, note: "BUG: 6 hrs ≤ 8 is fine, but flipped test says false → wrong direction" },
    { pointers: { lo: 7, hi: 11 }, vars: { direction: "wrong" }, note: "BUG: converges to some high speed like 8 or 11 instead of minimum 4" },
    { pointers: { lo: 1, hi: 6, mid: 3 }, vars: { "correct feasible": "hours ≤ h" }, note: "FIX: feasible(k) = totalHours(k) ≤ h. converges to min speed 4" }
  ]'
/>

> [pat] **Pattern Connection** — Identical structure to *Capacity to Ship Packages in D Days* (feasibility on capacity) and *Minimize Max Distance to Gas Station*.

### Learning notes
- Why `lo = 1`? — speed zero is invalid, and the slowest possible positive speed is 1 banana/hour.
- Why `hi = max(pile)`? — at that speed, every pile finishes in one hour, so it is always feasible.
- Why `(p + k - 1) / k`? — integer ceil division counts a partially eaten pile as a full hour.
- Why `long hours`? — total hours can exceed `int` while summing many large piles.
- Why `hi = k` on feasible? — `k` might be the minimum working speed, so keep it in the search range.
- Why `lo = k + 1` on infeasible? — if speed `k` is too slow, every smaller speed is also too slow.

### Same pattern, new tweaks

"Guess an answer, check feasibility in O(n), binary-search the threshold" — only the feasibility test changes:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Capacity to Ship Packages in D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | guess a ship capacity; feasibility = "can we finish in ≤ D days at this capacity?" | — |
| [Split Array Largest Sum / Book Allocation](https://leetcode.com/problems/split-array-largest-sum/) | guess a max segment sum; feasibility = "≤ m parts needed?" | — |
| [Minimize Max Distance to Gas Station](https://leetcode.com/problems/minimize-max-distance-to-gas-station/) | guess a distance; feasibility counts how many stations you'd have to add (works on real numbers, so fix an iteration count or epsilon) | — |

### Find the Smallest Divisor <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Find the Smallest Divisor Given a Threshold](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/)*

#### Problem
Given an integer array `nums` and `threshold`, find the smallest **positive integer divisor** `d` such that `Σ ⌈nums[i] / d⌉ ≤ threshold`.

**Constraints:** `1 ≤ nums.length ≤ 5·10^4`; `nums[i] ≤ 10^6`; `nums.length ≤ threshold ≤ 10^6`.

**Example:** `nums=[1,2,5,9], threshold=6` → `5` (sum = ⌈1/5⌉ + ⌈2/5⌉ + ⌈5/5⌉ + ⌈9/5⌉ = 1+1+1+2 = 5 ≤ 6).

#### Why this is a BS-on-answer problem

The feasibility `Σ⌈nums[i]/d⌉ ≤ threshold` is monotone in `d`: larger `d` → smaller (or equal) sum, since each `⌈nums[i]/d⌉` is non-increasing in `d`. The answer space `[1, max(nums)]` is bounded and finite.

> [key] Smallest positive integer d so the sum of ceilDiv(nums[i], d) is ≤ threshold.

<TemplateReveal
  slug="smallest-divisor"
  language="java"
  :canonical="smallestDivisorCode"
/>

> [inv] **Invariant** — `lo` is the smallest divisor that *might* work (every smaller d has `Σ⌈nums[i]/d⌉ > threshold`). `hi` is a divisor that definitely works (at `d = max(nums)` every term is 1, sum = n ≤ threshold by constraint). Loop maintains the half-open window.

**Why `lo = 1`, not `max(nums)`?** Here the problem accepts any positive integer; small `d` is meaningful (just makes the sum big). Contrast with Capacity to Ship: there `lo = max(weights)` because smaller caps are *undefined*. The lower bound depends on whether sub-range values make feasibility well-defined.

**Why `hi = max(nums)` and not `sum(nums)`?** At `d = max(nums)` every `⌈nums[i]/d⌉ = 1`, so sum = `n ≤ threshold` by the problem's constraint. Any larger `d` gives the same answer. No need to extend `hi` further.

**Complexity:** O(n log(max(nums))) time, O(1) space. For `n = 5·10^4` and `max = 10^6`, that's ~`10^6` ops — microseconds.

**Variations** (same monotone sum, different operation):
- [Nth Magical Number](https://leetcode.com/problems/nth-magical-number/) — binary-search the value whose count of multiples hits N.
- [Minimum Time to Complete Trips](https://leetcode.com/problems/minimum-time-to-complete-trips/) — binary-search the time; feasibility is `Σ ⌊t / time[i]⌋ ≥ totalTrips`.

### Split Array Largest Sum <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/)*

<ProgressCheck id="split-array-largest-sum-book-allocation-search-on-answer-partition" />

### Problem
Split the array into `m` **contiguous** subarrays so as to **minimize the largest** subarray sum.

**Constraints:** `1 ≤ n ≤ 1000`; `1 ≤ m ≤ n`; values `≥ 0`, sums up to ~10⁹.

**Example 1:** `[7,2,5,10,8], m = 2` → `18` (split `[7,2,5] | [10,8]`).

<ExamplePreview compact :input="['7', '2', '5', '10', '8', '|', '2']" :output="['18']" />

**Example 2:** `[1,2,3,4,5], m = 2` → `9` (split `[1,2,3] | [4,5]`).

<ExamplePreview compact :input="['1', '2', '3', '4', '5', '|', '2']" :output="['9']" />

### Solution — brute force
Brute force enumerates every way to place `m-1` cuts between elements, computes the largest segment sum for that partition, and keeps the minimum. There are exponentially many cut patterns (or combinatorially many for fixed `m`), so it is correct but not scalable. The optimized view guesses the largest allowed segment sum and greedily counts how many parts are needed, then binary-searches the smallest feasible cap.

```java
int splitArrayBrute(int[] a, int m) {
    return splitDfs(a, 0, m);
}
int splitDfs(int[] a, int start, int parts) {
    if (parts == 1) {
        int sum = 0;
        for (int i = start; i < a.length; i++) sum += a[i];
        return sum;
    }
    int best = Integer.MAX_VALUE, cur = 0;
    for (int cut = start; cut <= a.length - parts; cut++) {
        cur += a[cut];
        best = Math.min(best, Math.max(cur, splitDfs(a, cut + 1, parts - 1)));
    }
    return best;
}
```

Exponential time over cut placements, O(m) recursion space — too slow beyond small n.

### Solution — optimized
Binary search the *maximum allowed segment sum*; feasibility "can partition into ≤ m parts with each part ≤ cap" is monotone in cap and checked greedily.

> [key] **Key Insight** — Larger cap ⇒ fewer required parts (monotone). `lo = max(element)` (a part must hold its largest element), `hi = sum(all)`. Answer = smallest cap needing ≤ m parts.

The optimized version guesses the largest allowed subarray sum. For a fixed cap, the greedy scan starts a new segment only when adding the next value would exceed the cap; if that needs at most `m` parts, try a smaller cap.

```java
int splitArray(int[] a, int m) {
    long lo = 0, hi = 0;
    for (int x : a) { lo = Math.max(lo, x); hi += x; }
    while (lo < hi) {
        long cap = lo + (hi - lo) / 2;
        if (partsNeeded(a, cap) <= m) hi = cap; else lo = cap + 1;
    }
    return (int) lo;
}
int partsNeeded(int[] a, long cap) {
    int parts = 1; long cur = 0;
    for (int x : a) {
        if (cur + x > cap) { parts++; cur = x; }   // start new segment
        else cur += x;
    }
    return parts;
}
```

> [note] **Trace it** — `[7,2,5,10,8], m=2`. Cap 18 works: `[7,2,5] | [10,8]` = sums `14, 18`. Any smaller cap forces 3+ parts → answer **18**.

<CodeTrace
  title="Split Array Largest Sum — nums=[7,2,5,10,8], m=2 parts"
  :values="[7,2,5,10,8]"
  :windowKeys="['lo','hi']"
  :cellWidth="42"
  :steps='[
    { pointers: { lo: 10, hi: 32, mid: 21 }, vars: { parts: 2, ok: "yes" }, note: "cap 21: [7,2,5]/[10,8]. tighten" },
    { pointers: { lo: 10, hi: 21, mid: 15 }, vars: { parts: 3, ok: "no" }, note: "cap 15: [7,2,5]/[10]/[8] — 3 parts. loosen" },
    { pointers: { lo: 16, hi: 21, mid: 18 }, vars: { parts: 2, ok: "yes" }, note: "cap 18: [7,2,5]/[10,8]. tighten" },
    { pointers: { lo: 16, hi: 18, mid: 17 }, vars: { parts: 3, ok: "no" }, note: "cap 17: cannot 2-partition. loosen" },
    { pointers: { lo: 18, hi: 18 }, vars: { answer: 18 }, note: "converges: min cap = 18" }
  ]'
/>

### Time Complexity
O(n log(sum)), where `sum` is the total array sum. Each feasibility check is O(n), and binary search spans from max element to total sum.

### Space Complexity
O(1), because the optimized algorithm uses only bounds and the current segment sum.

> [note] **Interview script** — "I first confirm subarrays must be contiguous and I need to minimize the maximum segment sum. I start with brute force by trying all cut placements, which is exponential in the number of gaps for variable `m`. I optimize by binary-searching the answer between max element and total sum, with an O(n) greedy feasibility check, for O(n log sum) time and O(1) space."


> [trap] **Common Trap** — Wrong feasibility semantics. *Example:* `nums=[7,2,5,10,8]`, `m=2`. `feasible(cap)` asks *"can we split into ≤ m subarrays, each with sum ≤ cap?"*. Confusing it with *"exactly m"* misclassifies boundaries and the search settles on the wrong split.

<TrapTrace title="Wrong feasibility semantics" input="nums=[7,2,5,10,8]" bug="'nums=[7,2,5,10,8]', 'm=2'. 'feasible(cap)' asks *'can we split into ≤ m subarrays, each with sum ≤ cap?'*. Confusing it with *'exactly m'* misclassifies boundaries and the search settles on the wrong split." fix="See the guidance in the trap description and the code snippet." />

> [pat] **Pattern Connection** — "Minimize the maximum" (or "maximize the minimum") ⇒ almost always binary search on the answer with a greedy feasibility check. This is a top-5 staff-interview signal.

### Learning notes
- Why `lo = max(element)`? — no segment cap can be smaller than the largest single number.
- Why `hi = sum(all)`? — one segment containing the whole array is always feasible.
- Why use `long` for `lo`, `hi`, and `cap`? — sums can exceed 32-bit `int`.
- Why start `parts = 1`? — before any cut, the first segment already exists.
- Why cut when `cur + x > cap`? — that is the first moment the current segment would violate the guessed cap.
- Why `partsNeeded <= m` works? — if you can do it in fewer than `m` parts, you can split some non-empty segment further because values are non-negative.

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Capacity to Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | guess a ship capacity; feasibility = "≤ D days?" | — |
| [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | guess a speed; feasibility = "finishes within H hours?" | — |
| [Divide Chocolate / Maximize the Minimum](https://leetcode.com/problems/divide-chocolate/) | flip it — maximize the smallest piece, so `feasible(x)` = "can make ≥ k pieces each ≥ x." | — |
| [Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) | binary-search the max allowed step height; feasibility is a BFS/DFS connectivity check | — |

### Median of Two Sorted Arrays <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/)*

<ProgressCheck id="median-of-two-sorted-arrays-partition-binary-search" />

### Problem
Given two sorted arrays, find the **median** of their combined elements in **O(log(m+n))**.

**Constraints:** `0 ≤ m, n ≤ 1000`; combined length `≥ 1`; must be logarithmic (merging is too slow).

**Example 1:** `[1,3]` and `[2]` → `2.0`.

<ExamplePreview compact :input="['1', '3']" :output="['2']" />

**Example 2:** `[1,2]` and `[3,4]` → `2.5`.

<ExamplePreview compact :input="['1', '2']" :output="['3', '4']" />

### Solution — brute force
Brute force merges the two sorted arrays until the median position, or fully merges them and reads the middle. That is O(m+n) time and O(1) space if you stop early, or O(m+n) extra space for a full merged array. The optimized solution avoids merging by binary-searching a partition of the smaller array so the combined left half and right half are ordered correctly.

```java
double findMedianSortedArraysBrute(int[] A, int[] B) {
    int total = A.length + B.length;
    int need = total / 2;
    int i = 0, j = 0, prev = 0, cur = 0;
    for (int step = 0; step <= need; step++) {
        prev = cur;
        if (j == B.length || (i < A.length && A[i] <= B[j])) cur = A[i++];
        else cur = B[j++];
    }
    if ((total & 1) == 1) return cur;
    return (prev + cur) / 2.0;
}
```

O(m+n) time, O(1) space — too slow for the required logarithmic bound.

### Solution — optimized
Binary search a *partition* of the smaller array so that left halves of both arrays form the lower half of the merged array.

> [key] **Key Insight** — Choose `i` in A and `j = half − i` in B so that `A[i-1] ≤ B[j]` and `B[j-1] ≤ A[i]`. That single condition means everything left ≤ everything right → the median sits at the boundary. Binary-search `i` on the shorter array for O(log min(m,n)).

> [inv] **Invariant** — `i + j = (m+n+1)/2` keeps the left partition sized for the median; adjust `i` up/down based on which cross-boundary inequality fails.

The optimized version does not merge values; it searches for the split point where the left side has exactly half the combined elements and every left value is ≤ every right value. Sentinels make empty partitions behave like `-∞` and `+∞`.

#### Steps
1. Ensure `nums1` is the shorter array (swap if not) — keeps the binary-search range small.
2. Binary-search `i` over `[0, m]`; set `j = (m + n + 1) / 2 - i`.
3. Boundary values: `L1 = i > 0 ? nums1[i-1] : -∞`; `R1 = i < m ? nums1[i] : +∞`. Symmetric for `L2, R2`.
4. If `L1 <= R2 && L2 <= R1` — partition is correct.
5. If `L1 > R2` — `i` is too big; shrink `hi = i - 1`. Else `lo = i + 1`.
6. Once partitioned: odd total → `max(L1, L2)`; even → `(max(L1,L2) + min(R1,R2)) / 2.0`.

The optimized Java implementation:
```java
double findMedianSortedArrays(int[] A, int[] B) {
    if (A.length > B.length) return findMedianSortedArrays(B, A);
    int m = A.length, n = B.length, half = (m + n + 1) / 2;
    int lo = 0, hi = m;
    while (lo <= hi) {
        int i = lo + (hi - lo) / 2, j = half - i;
        int aL = i == 0 ? Integer.MIN_VALUE : A[i-1];
        int aR = i == m ? Integer.MAX_VALUE : A[i];
        int bL = j == 0 ? Integer.MIN_VALUE : B[j-1];
        int bR = j == n ? Integer.MAX_VALUE : B[j];
        if (aL <= bR && bL <= aR) {                     // correct partition
            if (((m + n) & 1) == 1) return Math.max(aL, bL);
            return (Math.max(aL, bL) + Math.min(aR, bR)) / 2.0;
        } else if (aL > bR) hi = i - 1;                 // too many from A
        else                lo = i + 1;
    }
    return 0.0;
}
```

> [note] **Trace it** — `[1,3]` and `[2]` (total length 3, odd). The correct partition puts `{1,2}` on the left and `{3}` on the right; the median is the max of the left = **2**.

<CodeTrace
  title="Median of Two Sorted Arrays — A=[1,3], B=[2]"
  :values="[1,3]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 1, "j (implied)": 1 }, vars: { L1: 1, R1: 3, L2: 2, R2: "∞", ok: "R1gt=L2 but L1ltL2?" }, note: "partition A after idx 0; B after idx 0" },
    { pointers: { i: 2, "j (implied)": 0 }, vars: { L1: 3, R1: "∞", L2: "-∞", R2: 2, ok: "no: L1gtR2" }, note: "wrong. move i left" },
    { pointers: { i: 1, "j (implied)": 1 }, vars: { L1: 1, R1: 3, L2: 2, R2: "∞", ok: "yes: L1≤R2 & L2≤R1" }, note: "valid partition. left has {1,2}. odd total → median=max(L1,L2)=2" }
  ]'
/>

### Time Complexity
O(log min(m,n)), because binary search runs only over the shorter array's partition index.

### Space Complexity
O(1), because the algorithm stores boundary indices and values without building a merged array.

> [note] **Interview script** — "I first confirm both arrays are sorted and the combined length is at least one. I start with brute force by merging up to the median, which is O(m+n) time and O(1) space if streamed. I optimize by binary-searching the partition on the smaller array, giving O(log min(m,n)) time and O(1) space."


> [trap] **Common Trap** — Off-by-one when the total length is odd. *Example:* `A=[1]`, `B=[2,3]`. Left partition should hold `(m+n+1)/2 = 2` elements — the median is the `max` of that left side. Using `(m+n)/2` puts the median on the wrong side.

<TrapTrace title="Off-by-one when the total length is odd" input="A=[1]" bug="'A=[1]', 'B=[2,3]'. Left partition should hold '(m+n+1)/2 = 2' elements — the median is the 'max' of that left side. Using '(m+n)/2' puts the median on the wrong side." fix="See the guidance in the trap description and the code snippet." />

### Learning notes
- **Not shortening the shorter array first** — the binary search range should be the smaller of `m`, `n`.
- **Off-by-one in the left-half size** — use `(m + n + 1) / 2` so the median lives on the left when odd.
- **Missing the `±∞` sentinels** for empty halves — use `Integer.MIN/MAX_VALUE`.
- **Averaging as ints** for even-total median — divide by `2.0` (return `double`).
- Why `j = half - i`? — once A contributes `i` elements to the left, B must contribute the rest.
- Why two inequalities `aL <= bR && bL <= aR`? — together they prove every left-side value is ≤ every right-side value.
- Why `hi = i - 1` when `aL > bR`? — A contributed too many large elements to the left partition.

> [pat] **Pattern Connection** — Partition binary search — the most sophisticated member of the family; demonstrates that binary search operates on *structural boundaries*, not just values.

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Kth Element of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | the general form — binary-search a partition so `k` elements sit on the left | — |
| [Median of a Row-wise Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) | binary-search the value and count how many are ≤ mid | — |
| [Find K-th Smallest Pair Distance](https://leetcode.com/problems/find-k-th-smallest-pair-distance/) | binary-search the distance; feasibility counts pairs within it via a sliding window | — |

## In the wild — Kubernetes bin-packing feasibility

The Kubernetes scheduler must decide, at pod-admission time, whether a new pod with a resource request fits onto some node. For **cluster autoscaler**, the question flips to: *"What's the minimum number of nodes of type T we need to add so this pending workload fits?"* The scheduler's `ClusterAutoscaler.estimateNodeCount()` runs a monotone bin-packing feasibility and binary-searches the node count:

```go
// kubernetes/autoscaler/cluster-autoscaler/estimator/binpacking_estimator.go (paraphrased)
func (e *BinpackingEstimator) Estimate(pods []*v1.Pod, nodeTemplate *schedulerframework.NodeInfo) int {
    lo, hi := 1, len(pods)                             // bounds: 1 node ≤ answer ≤ one node per pod
    for lo < hi {
        mid := lo + (hi-lo)/2
        if canFit(pods, nodeTemplate, mid) {           // feasibility: first-fit-decreasing packing
            hi = mid                                    // mid works — can we do fewer?
        } else {
            lo = mid + 1                                // mid doesn't fit — need more
        }
    }
    return lo
}
```

The `canFit` feasibility check is a **first-fit-decreasing** bin-pack simulation: sort pods by resource request, assign greedily to the mid-count virtual nodes. If every pod fits, mid is feasible. Monotonicity holds because adding a node can never make a feasible packing infeasible.

**Why BS-on-answer here instead of a greedy single-pass count?** Because resources are multi-dimensional (CPU, memory, GPU, pods-per-node), first-fit-decreasing can leave gaps a second pass can't recover. BS on the node count treats each feasibility probe as an independent repack.

**Other production uses of the same mechanic:**
1. **PostgreSQL's `pg_bulkload`** — binary-searches the optimal `buffer_size` for streaming inserts; feasibility = "did the load complete without disk flush during this window?"
2. **Linux kernel `tcp_bbr`** congestion control — binary-searches the sending rate; feasibility = "did RTT stay under probe target during this interval?"
3. **TensorFlow's `tf.config.experimental.set_memory_growth`** on GPU allocators — binary-searches the initial `block_size`; feasibility = "no OOM during the first N allocations?"
4. **Spark's `DAGScheduler.shuffleWriteBufferSize`** — binary-searches the per-partition write buffer; feasibility = "did the shuffle complete within the deadline?"

## Recognition drill

<RecognitionDrill pattern="bs-on-answer" :count="10" />

## Advanced — follow-ups and failure modes

<details>
<summary><strong>What if the answer is a real number?</strong></summary>

Switch from `while (lo < hi)` to one of:
- **Epsilon convergence** — `while (hi - lo > 1e-7)`, where `1e-7` matches the problem's tolerance.
- **Fixed-iteration halving** — `for (int i = 0; i < 100; i++)` → precision `2^-100 ≈ 10^-30` of initial range. Preferred for competitive programming — no `while` termination to prove.

Rewrite the loop body:

```java
double lo = ..., hi = ...;
for (int it = 0; it < 100; it++) {
    double mid = lo + (hi - lo) / 2;      // never (lo + hi) / 2 — overflow on doubles too (close to MAX_VALUE)
    if (feasible(mid)) hi = mid;
    else                lo = mid;
}
return lo;
```

Example: *Median of a sorted matrix with real values*, *Minimize Max Distance to Gas Station*.
</details>

<details>
<summary><strong>What if feasible is non-monotone but has a known shape?</strong></summary>

If `feasible` is **unimodal** (one peak or one valley), ternary search works in O(log n) with twice the probes per step. Each iteration splits into thirds, discards the end farthest from the current best. Used for continuous convex optimization in low dimensions.

If `feasible` has `k` monotone intervals, each ≥ `n/k` wide, binary-search each interval separately. If `k` is unknown, this doesn't help.
</details>

<details>
<summary><strong>What if the feasibility check itself is a BS?</strong></summary>

You get **nested BS** — common when the inner search is on a value and the outer is on a count. Example: *Kth Smallest Pair Distance*: outer BS on the pair-distance answer; inner is a sorted-array two-pointer that counts pairs within a given distance. Total: O(n log(max_pair_distance)) because the inner is linear, not log.

If both layers are BS, you'd get O(log² ...). Try to flatten by replacing one with a greedy count.
</details>

<details>
<summary><strong>What if the answer space is a 2D parameter (e.g., choose x AND y)?</strong></summary>

Binary search doesn't generalize to 2D. Reach for:
- **Lagrangian relaxation** — binary-search the dual multiplier (one dimension) and solve the primal (other dimension) exactly for each probe.
- **Grid search → gradient-free optimization** (CMA-ES, Nelder-Mead) when the surface is smooth.
- **Direct DP** when the parameters are small-integer.

Example: *Allocate k items to m bins minimizing max load, with per-bin capacity limits* — Lagrangian on the capacity shadow price.
</details>

<details>
<summary><strong>What if monotonicity breaks only at a few points (floating-point artifacts)?</strong></summary>

Common with real-valued feasibility: `feasible(x)` is a Monte-Carlo simulation whose output flickers near the boundary. Fixes:

- **Hysteresis** — treat a flip as "feasible" only if 3 consecutive probes agree.
- **Decrease epsilon** — probe at `mid ± δ` and require both to agree.
- **Deterministic feasibility** — swap the stochastic check for a conservative upper bound that's deterministic even if looser.

Example: *Optimal GPU batch size by binary-searching OOM risk* — feasibility is stochastic because of fragmentation; use a conservative headroom instead.
</details>

### Breaking point

Binary search on the answer **stops being optimal** when:
- `feasible` isn't monotone — single most-common failure mode.
- Each feasibility check costs more than O(n log n) — the log factor from BS might not amortize.
- The answer is a structure, not a scalar.
- The answer range is small (`≤ 1000`) and each check is cheap — simple iteration is simpler.
- The problem has a closed-form solution — e.g. median of a sorted array is `a[n/2]`, don't BS.

### Three cross-pattern problems

- [Allocate Mailboxes](https://leetcode.com/problems/allocate-mailboxes/) — looks like BS on answer; actually a DP (the feasibility isn't monotone in a useful way).
- [Minimum Cost to Hire K Workers](https://leetcode.com/problems/minimum-cost-to-hire-k-workers/) — BS on quality ratio paired with a priority queue; demonstrates nested feasibility.
- [Erect the Fence](https://leetcode.com/problems/erect-the-fence/) — convex hull, NOT a BS problem; included because the "minimize enclosing area" phrasing sounds BS-shaped.

---

## Check your understanding

<Quiz pattern-id="bs-on-answer" :questions="mastery5" />

<PrintButton />

<RelatedPatterns pattern-id="binary-search" />
