# BS on Answer — Capacity To Ship Packages Within D Days

*[↗ LeetCode: Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/bs-on-answer)

<CompanyTags companies="Amazon, Google, Meta" />

Given package weights and `days`, find the minimum ship capacity that ships all in `days` days.

**Example** — `weights=[1,2,3,4,5,6,7,8,9,10], days=5` → `15`

**Constraints** — `1 ≤ days ≤ n ≤ 5·10⁴`; `1 ≤ weights[i] ≤ 500`.


<Hints
  hint1="Can I write a `feasible(x)` check that returns true iff answer ≤ x (or ≥ x)?"
  hint2="If `feasible` is monotonic in x, binary search over the answer space `[lo, hi]`. Range: min possible value to max possible value."
  hint3="The feasibility check is O(n); total complexity is O(n log range)."
/>
---

<MarkSolved problem-slug="capacity-to-ship-packages-within-d-days" />


## Approach 1 — Try every capacity

O(max·n). TLE.

## Approach 2 — Binary search on capacity

**Insight.** `feasible(cap)` = can we ship in ≤ days days with this cap? Monotonic. Range: `lo = max(weights)` (must fit heaviest), `hi = sum(weights)`.

```java
int shipWithinDays(int[] w, int days) {
    int lo = 0, hi = 0;
    for (int x : w) { lo = Math.max(lo, x); hi += x; }
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        int used = 1, load = 0;
        for (int x : w) {
            if (load + x > mid) { used++; load = 0; }
            load += x;
        }
        if (used <= days) hi = mid;
        else              lo = mid + 1;
    }
    return lo;
}
```

<CodeTrace
  title="BS — weights=[1..10], days=5"
  :values="[1,2,3,4,5,6,7,8,9,10]"
  :windowKeys="['lo','hi']"
  :cellWidth="30"
  :steps='[
    { pointers: { lo: 10, hi: 55, mid: 32 }, vars: { used: 2 }, note: "cap 32 fits in 2 days" },
    { pointers: { lo: 10, hi: 32, mid: 21 }, vars: { used: 3 }, note: "cap 21 fits in 3 days" },
    { pointers: { lo: 10, hi: 21, mid: 15 }, vars: { used: 5 }, note: "cap 15 fits in 5 days" },
    { pointers: { lo: 10, hi: 15, mid: 12 }, vars: { used: 6 }, note: "cap 12 needs 6 days → too small" },
    { pointers: { lo: 13, hi: 15, mid: 14 }, vars: { used: 6 }, note: "14 → 6. still too small" },
    { pointers: { lo: 15, hi: 15 }, vars: { answer: 15 }, note: "converged → 15", added: [4,5] }
  ]'
/>

**Complexity** — Time **O(n log sum)**; Space **O(1)**.

## Try it yourself

<JavaRunner problem-slug="capacity-to-ship-packages-within-d-days" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Linear scan on cap | O(max · n) | O(1) |
| BS on answer | **O(n log sum)** | O(1) |

## When to use which

- **"Min feasible X with monotone predicate"** → BS on answer.
- **Return the split itself** → after BS converges, re-simulate to record boundaries.
- **Very large sums** → use `long` for hi bound.

<AiCompanion problem-slug="capacity-to-ship-packages-within-d-days" pattern-hint="binary search on answer" />

## Related problems

- [Koko Eating Bananas](/problems/bs-on-answer-koko-bananas)
- [Split Array Largest Sum](/problems/split-array-largest-sum) — same skeleton
- [Divide Chocolate](/problems/divide-chocolate) — maximise the minimum

<FeedbackWidget problem-slug="capacity-to-ship-packages-within-d-days" />

<RelatedProblems problems="koko-bananas::Koko Bananas|find-peak-element::Find Peak Element|median-of-two-sorted-arrays::Median Of Two Sorted Arrays" />
