# Divide & Conquer — Reverse Pairs

*[↗ LeetCode: Reverse Pairs](https://leetcode.com/problems/reverse-pairs/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/divide-conquer)

<CompanyTags companies="Google, Amazon" />

Count pairs `(i, j)` with `i < j` and `nums[i] > 2 · nums[j]`.

**Example 1** — `nums=[1,3,2,3,1]` → `2`
**Example 2** — `nums=[2,4,3,5,1]` → `3`

**Constraints** — `1 ≤ n ≤ 5·10⁴`; `-2³¹ ≤ nums[i] ≤ 2³¹−1`.


<Hints
  hint1="Can I split the input in half, solve each half, then combine? Combine step is the trick."
  hint2="Merge sort framework: recurse left, recurse right, then merge with the counting/comparison logic on the boundary."
  hint3="For count-of-X-across-boundary, two-pointer walk during the merge step."
/>
---

## Approach 1 — All pairs

O(n²). TLE.

## Approach 2 — Merge sort with reverse-pair counting (canonical)

**Insight.** During merge sort, before merging two sorted halves, count pairs `(i, j)` with `i` in left, `j` in right, and `nums[i] > 2 · nums[j]`. Use two pointers on the two sorted halves.

**Trap** — use `long` for `2 * nums[j]` to avoid overflow.

```java
int reversePairs(int[] nums) {
    return mergeSort(nums, 0, nums.length - 1);
}
int mergeSort(int[] a, int lo, int hi) {
    if (lo >= hi) return 0;
    int mid = (lo + hi) / 2;
    int count = mergeSort(a, lo, mid) + mergeSort(a, mid + 1, hi);
    int j = mid + 1;
    for (int i = lo; i <= mid; i++) {
        while (j <= hi && a[i] > 2L * a[j]) j++;
        count += j - mid - 1;
    }
    int[] merged = new int[hi - lo + 1];
    int p = lo, q = mid + 1, w = 0;
    while (p <= mid && q <= hi) merged[w++] = a[p] <= a[q] ? a[p++] : a[q++];
    while (p <= mid) merged[w++] = a[p++];
    while (q <= hi) merged[w++] = a[q++];
    System.arraycopy(merged, 0, a, lo, merged.length);
    return count;
}
```

<CodeTrace
  title="Merge — nums=[2,4,3,5,1]"
  :values="['2','4','3','5','1']"
  :windowKeys="['step']"
  :cellWidth="34"
  :steps='[
    { pointers: { step: 0 }, vars: { left: "[2,4]", right: "[3,5,1]" }, note: "" },
    { pointers: { step: 1 }, vars: { count: 3 }, note: "pairs across" }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="reverse-pairs" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| All pairs | O(n²) | O(1) | baseline |
| Merge sort count | **O(n log n)** | O(n) | canonical |

## When to use which

- **Standard inversion / reverse pair counting** → merge sort.
- **BIT alternative** → compress values; sweep left-to-right; BIT counts smaller / larger.
- **k times threshold** → same skeleton with different pointer logic.

<AiCompanion problem-slug="reverse-pairs" pattern-hint="divide & conquer" />

## Related problems

- [Count of Range Sum](/problems/count-of-range-sum)
- [Global and Local Inversions](/problems/global-and-local-inversions)
- [Count Inversions](/problems/divide-conquer-inversions)

<FeedbackWidget problem-slug="reverse-pairs" />
