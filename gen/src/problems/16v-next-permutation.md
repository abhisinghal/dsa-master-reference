# Backtracking — Next Permutation

*[↗ LeetCode: Next Permutation](https://leetcode.com/problems/next-permutation/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

Rearrange nums to the next lexicographic permutation, in-place. If none, sort ascending.

> Filed near Backtracking because it's the "generate permutations in order" primitive. The algorithm itself is **not** backtracking — it's a two-step in-place swap.

## Approach — Classic algorithm

**Steps.**
1. Scan from right; find first `i` with `nums[i] < nums[i+1]` (the "pivot"). If none, reverse whole array.
2. Scan from right; find first `j` with `nums[j] > nums[i]`. Swap.
3. Reverse the suffix from `i+1` to end (it was decreasing → now increasing = smallest larger permutation).

```java
void nextPermutation(int[] nums) {
    int n = nums.length, i = n - 2;
    while (i >= 0 && nums[i] >= nums[i + 1]) i--;
    if (i >= 0) {
        int j = n - 1;
        while (nums[j] <= nums[i]) j--;
        swap(nums, i, j);
    }
    reverse(nums, i + 1, n - 1);
}
void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }
void reverse(int[] a, int l, int r) { while (l < r) swap(a, l++, r--); }
```

**Complexity** — Time **O(n)**; Space **O(1)**.

## Related problems

- [Permutations](/problems/permutations) — enumerate all
- [Permutation Sequence](https://leetcode.com/problems/permutation-sequence/) — kth permutation via factorial base
