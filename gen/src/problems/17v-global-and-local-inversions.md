# Divide & Conquer — Global and Local Inversions

*[↗ LeetCode: Global and Local Inversions](https://leetcode.com/problems/global-and-local-inversions/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/divide-conquer)

Return `true` iff **number of global inversions == number of local inversions**. A local inversion is `nums[i] > nums[i+1]`; global is any `i < j` with `nums[i] > nums[j]`.

**Example 1** — `nums=[1,0,2]` → `true`
**Example 2** — `nums=[1,2,0]` → `false` (2 global: (1,0),(2,0); 1 local: (2,0))

**Constraints** — `1 ≤ n ≤ 10⁵`; `0 ≤ nums[i] ≤ n − 1` (permutation).


<Hints
  hint1="Can I split the input in half, solve each half, then combine? Combine step is the trick."
  hint2="Merge sort framework: recurse left, recurse right, then merge with the counting/comparison logic on the boundary."
  hint3="For count-of-X-across-boundary, two-pointer walk during the merge step."
/>
---

<MarkSolved problem-slug="global-and-local-inversions" />


## Approach 1 — Count both explicitly

O(n²) for global. Baseline.

## Approach 2 — Merge sort inversions count vs O(n) locals

O(n log n). Works but heavy.

## Approach 3 — Direct observation (canonical)

**Insight.** Every local inversion IS a global inversion. So equality holds iff no non-adjacent global inversion exists → for every `i`, `nums[i]` must not exceed `i + 1` (values can differ from index by at most 1). Check `|nums[i] - i| ≤ 1` for all `i`.

Even simpler: track running max at `i - 2`; if it exceeds `nums[i]`, non-adjacent inversion exists.

```java
boolean isIdealPermutation(int[] nums) {
    int maxSoFar = 0;
    for (int i = 0; i < nums.length - 2; i++) {
        maxSoFar = Math.max(maxSoFar, nums[i]);
        if (maxSoFar > nums[i + 2]) return false;
    }
    return true;
}
```

<CodeTrace
  title="Count both explicitly"
  :values="['1', '0', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="global-and-local-inversions" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Explicit both | O(n²) | O(1) | baseline |
| Merge sort | O(n log n) | O(n) | works |
| Direct scan | **O(n)** | **O(1)** | canonical |

## When to use which

- **"Are global and local equal?"** → single O(n) scan.
- **"Count both separately"** → merge sort for global; O(n) for local.
- **"Are they within k?"** → merge sort remains most general.

<AiCompanion problem-slug="global-and-local-inversions" pattern-hint="divide & conquer" />

## Related problems

- [Reverse Pairs](/problems/reverse-pairs)
- [Count Inversions](/problems/divide-conquer-inversions)
- [Number of Reverse Pairs in Array](https://leetcode.com/problems/number-of-reverse-pairs-in-array/)

<FeedbackWidget problem-slug="global-and-local-inversions" />
