# BS on Answer — Divide Chocolate

*[↗ LeetCode: Divide Chocolate](https://leetcode.com/problems/divide-chocolate/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/bs-on-answer)

<CompanyTags companies="Google, Amazon" />

Divide `sweetness[]` into `k+1` contiguous pieces (you take the piece with the smallest sum). Maximize your piece's sweetness.

**Example** — `sweetness=[1,2,3,4,5,6,7,8,9], k=5` → `6`

**Constraints** — `1 ≤ k+1 ≤ n ≤ 10⁴`; `1 ≤ sweetness[i] ≤ 10⁵`.


<Hints
  hint1="Can I write a `feasible(x)` check that returns true iff answer ≤ x (or ≥ x)?"
  hint2="If `feasible` is monotonic in x, binary search over the answer space `[lo, hi]`. Range: min possible value to max possible value."
  hint3="The feasibility check is O(n); total complexity is O(n log range)."
/>
---

<MarkSolved problem-slug="divide-chocolate" /> <Bookmark problem-slug="divide-chocolate" />

<InterviewTimer problem-slug="divide-chocolate" />



## Approach — Binary search on the minimum

**Insight.** `feasible(cap)` = can we cut into ≥ k+1 pieces each with sum ≥ cap? Monotonic (bigger cap → fewer possible cuts). Range: `lo = 1`, `hi = sum / (k+1)` (or `sum`).

```java
int maximizeSweetness(int[] sweetness, int k) {
    int lo = Integer.MAX_VALUE, hi = 0;
    for (int x : sweetness) { lo = Math.min(lo, x); hi += x; }
    while (lo < hi) {
        int mid = lo + (hi - lo + 1) / 2;                     // upper mid for max-answer BS
        int cuts = 0, sum = 0;
        for (int x : sweetness) {
            sum += x;
            if (sum >= mid) { cuts++; sum = 0; }
        }
        if (cuts >= k + 1) lo = mid;                          // feasible → try larger
        else               hi = mid - 1;
    }
    return lo;
}
```

<CodeTrace
  title="BS on min — sweetness=[1..9], k=5 (6 pieces)"
  :values="[1,2,3,4,5,6,7,8,9]"
  :windowKeys="['lo','hi']"
  :cellWidth="30"
  :steps='[
    { pointers: { lo: 1, hi: 45, mid: 23 }, vars: { cuts: 1 }, note: "min 23 → only 1 piece → too big → hi=22" },
    { pointers: { lo: 1, hi: 22, mid: 12 }, vars: { cuts: 3 }, note: "min 12 → 3 pieces → too big → hi=11" },
    { pointers: { lo: 1, hi: 11, mid: 6 }, vars: { cuts: 6 }, note: "min 6 → 6 pieces ✓ → lo=6" },
    { pointers: { lo: 6, hi: 11, mid: 9 }, vars: { cuts: 4 }, note: "min 9 → 4 pieces → too big → hi=8" },
    { pointers: { lo: 6, hi: 8, mid: 7 }, vars: { cuts: 5 }, note: "min 7 → 5 pieces → too big → hi=6" },
    { pointers: { lo: 6, hi: 6 }, vars: { answer: 6 }, note: "converged → 6" }
  ]'
/>

**Complexity** — Time **O(n log sum)**; Space **O(1)**.

## Try it yourself

<JavaRunner problem-slug="divide-chocolate" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| BS on min | **O(n log sum)** | O(1) |

**Watch the mid formula.** For *maximize-feasible* BS, use `lo + (hi - lo + 1) / 2` (upper mid) to avoid infinite loops.

## When to use which

- **"Max feasible X with monotone predicate"** → BS on answer with `≥ target` check.
- **Return the splits** → re-simulate after convergence.
- **Bounded values** → tight `[lo, hi]` speeds up.

<AiCompanion problem-slug="divide-chocolate" pattern-hint="binary search on answer" />

## Related problems

- [Split Array Largest Sum](/problems/split-array-largest-sum) — minimize the maximum (sibling)
- [Koko Eating Bananas](/problems/bs-on-answer-koko-bananas)
- [Minimize Max Distance to Gas Station](/problems/minimize-max-distance-to-gas-station)

<FeedbackWidget problem-slug="divide-chocolate" />
