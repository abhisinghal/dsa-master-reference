# Two Pointers — Merge Sorted Array

*[↗ LeetCode: Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Meta, Amazon, Microsoft, Google, Bloomberg" />

Merge `nums2` into `nums1` in-place; `nums1` has size `m+n` with last `n` slots empty.

**Example 1** — `nums1=[1,2,3,0,0,0], m=3, nums2=[2,5,6], n=3` → `[1,2,2,3,5,6]`
**Example 2** — `nums1=[1], m=1, nums2=[], n=0` → `[1]`

**Constraints** — `nums1.length == m + n`. Brute concat + sort is O((m+n) log(m+n)) — fine for 10² inputs, misses the point. In-place from-the-back three-pointer is O(m+n) = ~10⁶ pointer ops on real payload sizes.
<Hints
  hint1="Sort first if the input isn’t already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/>
---

<MarkSolved problem-slug="merge-sorted-array" /> <Bookmark problem-slug="merge-sorted-array" />

<InterviewTimer problem-slug="merge-sorted-array" />



## Approach 1 — Copy then sort

O((m+n) log(m+n)). Baseline.

## Approach 2 — Backward two-pointer (canonical)

**Insight.** Fill from the back so we never overwrite an unread element.



```java
void merge(int[] nums1, int m, int[] nums2, int n) {
    int i = m - 1, j = n - 1, k = m + n - 1;
    while (j >= 0) {
        if (i >= 0 && nums1[i] > nums2[j]) nums1[k--] = nums1[i--];
        else nums1[k--] = nums2[j--];
    }
}
```



<CodeTrace
  title="Fill-from-back — nums1=[1,2,3,0,0,0], nums2=[2,5,6]"
  :values="['1','2','3','·','·','·']"
  :windowKeys="['i','j','k']"
  :cellWidth="30"
  :steps='[
    { pointers: { i: 2, j: 2, k: 5 }, vars: { pick: 6 }, note: "" },
    { pointers: { i: 2, j: 1, k: 4 }, vars: { pick: 5 }, note: "" },
    { pointers: { i: 1, j: 0, k: 2 }, vars: { done: true }, note: "" }
  ]'
/>

**Complexity** — Time **O(m+n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="merge-sorted-array" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Copy + sort | O((m+n) log) | O(m+n) | baseline |
| Fill from back | **O(m+n)** | O(1) | canonical |

## When to use which

- **In-place merge with buffer at back** → fill from back.
- **No buffer** → allocate new array.
- **Linked lists** → same idea; see [Merge Two Sorted Lists](/problems/merge-two-sorted-lists).

<AiCompanion problem-slug="merge-sorted-array" pattern-hint="two pointers" />

## Related problems

- [Merge Two Sorted Lists](/problems/merge-two-sorted-lists)
- [Squares of a Sorted Array](/problems/squares-of-a-sorted-array)
- [Sort Colors](https://leetcode.com/problems/sort-colors/)

<FeedbackWidget problem-slug="merge-sorted-array" />

<RelatedProblems problems="4sum::4sum|squares-of-a-sorted-array::Squares Of A Sorted Array|move-zeroes::Move Zeroes" />
