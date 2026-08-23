# Divide & Conquer — Count of Range Sum

*[↗ LeetCode: Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/divide-conquer)

&lt;CompanyTags companies="Google, Amazon" /&gt;

Count subarrays whose sum lies in `[lower, upper]` (inclusive).

**Example 1** — `nums=[-2,5,-1], lower=-2, upper=2` → `3`
**Example 2** — `nums=[0], lower=0, upper=0` → `1`

**Constraints** — `1 ≤ n ≤ 10⁵`; `-2³¹ ≤ nums[i] ≤ 2³¹−1`.


&lt;Hints
  hint1="Can I split the input in half, solve each half, then combine? Combine step is the trick."
  hint2="Merge sort framework: recurse left, recurse right, then merge with the counting/comparison logic on the boundary."
  hint3="For count-of-X-across-boundary, two-pointer walk during the merge step."
/&gt;
---

&lt;MarkSolved problem-slug="count-of-range-sum" /&gt;

&lt;InterviewTimer problem-slug="count-of-range-sum" /&gt;



## Approach 1 — All subarrays

O(n²). Baseline.

## Approach 2 — Merge sort on prefix sums (canonical)

**Insight.** Sum of `[i, j]` = `pref[j+1] - pref[i]`. Count pairs `(i, j)` with `lower ≤ pref[j] - pref[i] ≤ upper` and `i < j`. During merge sort of `pref`, whenever left half's element `L` and right half's element `R` maintain `L < R` in the original sequence, count valid `L, R`s via two pointers.



```java
int countRangeSum(int[] nums, int lower, int upper) {
    long[] pref = new long[nums.length + 1];
    for (int i = 0; i < nums.length; i++) pref[i + 1] = pref[i] + nums[i];
    return mergeCount(pref, 0, pref.length, lower, upper);
}
int mergeCount(long[] p, int lo, int hi, int lower, int upper) {
    if (hi - lo <= 1) return 0;
    int mid = (lo + hi) / 2;
    int count = mergeCount(p, lo, mid, lower, upper) + mergeCount(p, mid, hi, lower, upper);
    int i = mid, j = mid;
    for (int k = lo; k < mid; k++) {
        while (i < hi && p[i] - p[k] < lower) i++;
        while (j < hi && p[j] - p[k] <= upper) j++;
        count += j - i;
    }
    long[] merged = new long[hi - lo];
    int a = lo, b = mid, w = 0;
    while (a < mid && b < hi) merged[w++] = p[a] <= p[b] ? p[a++] : p[b++];
    while (a < mid) merged[w++] = p[a++];
    while (b < hi) merged[w++] = p[b++];
    System.arraycopy(merged, 0, p, lo, merged.length);
    return count;
}
```



<CodeTrace
  title="Merge — nums=[-2,5,-1], pref=[0,-2,3,2]"
  :values="['0','-2','3','2']"
  :windowKeys="['step']"
  :cellWidth="34"
  :steps='[
    { pointers: { step: 0 }, vars: { pref: "[0,-2,3,2]" }, note: "" },
    { pointers: { step: 1 }, vars: { left: "[-2,0]", right: "[2,3]" }, note: "count valid pairs across" },
    { pointers: { step: 2 }, vars: { total: 3 }, note: "" }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="count-of-range-sum" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| All subarrays | O(n²) | O(n) | baseline |
| Merge sort | **O(n log n)** | O(n) | canonical |

## When to use which

- **Count pairs with range constraint on transformed values** → merge sort.
- **Fenwick/BIT alternative** → compress prefix values; count during single sweep.
- **Segment tree** → same asymptotics; different implementation.

&lt;AiCompanion problem-slug="count-of-range-sum" pattern-hint="divide & conquer" /&gt;

## Related problems

- [Reverse Pairs](/problems/reverse-pairs)
- [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)
- [Global and Local Inversions](/problems/global-and-local-inversions)

&lt;FeedbackWidget problem-slug="count-of-range-sum" /&gt;

&lt;RelatedProblems problems="reverse-pairs::Reverse Pairs|sort-list::Sort List|inversions::Inversions" /&gt;
