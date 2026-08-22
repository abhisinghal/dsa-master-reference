# Hashing — Two Sum II (Input Array Is Sorted)

*[↗ LeetCode: Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

Sorted array; return 1-indexed pair summing to target.

## Approach 1 — Hash map (ignores sort)

Uses O(n) extra space. Works but wastes the sort.

## Approach 2 — Opposing two-pointer

**Insight.** With a sorted array, the sum monotonically increases when `l` advances or `r` retreats. So we can move deterministically without storing anything.

```java
int[] twoSum(int[] nums, int target) {
    int l = 0, r = nums.length - 1;
    while (l < r) {
        int s = nums[l] + nums[r];
        if (s == target) return new int[]{l + 1, r + 1};
        if (s < target) l++; else r--;
    }
    return new int[]{-1, -1};
}
```

**Complexity** — Time **O(n)**; Space **O(1)**.

## Related problems

- [Two Sum](/problems/hashing-two-sum) — unsorted
- [3Sum](/problems/3sum) — outer loop + two-pointer
