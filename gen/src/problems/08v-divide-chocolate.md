# BS on Answer — Divide Chocolate

*[↗ LeetCode: Divide Chocolate](https://leetcode.com/problems/divide-chocolate/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/bs-on-answer)

<CompanyTags companies="Google, Amazon" />

Divide `sweetness[]` into `k+1` contiguous pieces (you take the piece with the smallest sum). Maximize your piece's sweetness.

**Example 1** — `sweetness=[1,2,3,4,5,6,7,8,9], k=5` → `6`
**Example 2** — `sweetness=[5,6,7,8,9,1,2,3,4], k=8` → `1` (9 pieces, 1 each — you take min = 1)
**Example 3** — `sweetness=[1,2,2,1,2,2,1,2,2], k=2` → `5` (3 pieces of sums [5, 5, 5])

**Constraints** — `1 ≤ k+1 ≤ n ≤ 10⁴`; `1 ≤ sweetness[i] ≤ 10⁵`. Answer range `[1, 10⁹]`. Brute enumeration of `C(n,k)` cuts is impossibly large; BS-on-answer is O(n log range) ≈ 3·10⁵ ops.


<Hints
  hint1="Can I write a `feasible(x)` check that returns true iff answer ≤ x (or ≥ x)?"
  hint2="If `feasible` is monotonic in x, binary search over the answer space `[lo, hi]`. Range: min possible value to max possible value."
  hint3="The feasibility check is O(n); total complexity is O(n log range)."
/>
---

<MarkSolved problem-slug="divide-chocolate" /> <Bookmark problem-slug="divide-chocolate" />

<InterviewTimer problem-slug="divide-chocolate" />



## Approach 1 — Brute force: try every partition

**Intuition.** For each of the `C(n-1, k)` ways to place `k` cuts among `n-1` gaps, compute the minimum piece sum, keep the max.

```java
int maximizeSweetnessBrute(int[] a, int k) {
    return tryPartition(a, k, 0, 0);
}
int tryPartition(int[] a, int k, int start, int cutsPlaced) {
    if (cutsPlaced == k) return sumRange(a, start, a.length - 1);
    int best = 0;
    for (int end = start; end < a.length - (k - cutsPlaced); end++) {
        int firstPiece = sumRange(a, start, end);
        int rest = tryPartition(a, k, end + 1, cutsPlaced + 1);
        best = Math.max(best, Math.min(firstPiece, rest));
    }
    return best;
}
```

**Complexity** — Time **O(C(n-1, k))** which blows up; Space **O(k)** recursion. For `n=100, k=50`, `C(99,50) ≈ 10²⁹`. *In an interview* state this then flip to binary search on the answer.

---

## Approach 2 — Binary search on the minimum (canonical)

**Insight.** `feasible(cap)` = can we cut into ≥ `k+1` pieces each with sum ≥ `cap`? **Monotone** — bigger `cap` → fewer possible cuts → harder. Find the largest `cap` where `feasible(cap)` still holds.

Range: `lo = min(sweetness)` (a piece must contain at least one item), `hi = sum(sweetness)` (one giant piece).

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

**Complexity** — Time **O(n log sum)**; Space **O(1)**. *Say aloud in an interview:* "for maximize-feasible, use the *upper* mid (`lo + (hi - lo + 1) / 2`) to avoid infinite loops. For minimize-feasible, use lower mid."

## Try it yourself

<JavaRunner problem-slug="divide-chocolate" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute enumeration | O(C(n-1, k)) | O(k) |
| **BS on min** | **O(n log sum)** | O(1) |

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
