# Two Pointers — Merge Sorted Array

*[↗ LeetCode: Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

Merge `nums2` into `nums1` in-place; `nums1` has `m + n` slots (last `n` empty).

## Approach 1 — Naïve merge into buffer

Copy nums1 first m into a temp, then two-pointer merge into nums1. O(m+n) time, O(m) space.

## Approach 2 — Backward two-pointer

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

**Why safe.** Any element we overwrite at index `k` has already been read (its original position `≤ k` was consumed earlier).

**Complexity** — Time **O(m+n)**; Space **O(1)**.

## Related problems

- [Merge Two Sorted Lists](/problems/merge-two-sorted-lists) — linked-list variant
- [Squares of a Sorted Array](/problems/squares-of-a-sorted-array) — fill-from-back
