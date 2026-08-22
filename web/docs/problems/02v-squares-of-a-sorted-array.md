# Two Pointers — Squares of a Sorted Array

*[↗ LeetCode: Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

Return squares of a sorted (possibly-negative) array, sorted.

## Approach 1 — Square then sort

O(n log n).

## Approach 2 — Two pointers filling from back

**Insight.** Largest square is at one of the two ends (most negative or most positive). Compare, place at `k = n-1`, decrement, repeat.



```java
int[] sortedSquares(int[] nums) {
    int n = nums.length, l = 0, r = n - 1, k = n - 1;
    int[] out = new int[n];
    while (l <= r) {
        int a = nums[l] * nums[l], b = nums[r] * nums[r];
        if (a > b) { out[k--] = a; l++; }
        else { out[k--] = b; r--; }
    }
    return out;
}
```



**Complexity** — Time **O(n)**; Space **O(n)** for output.

## Related problems

- [Merge Sorted Array](/problems/merge-sorted-array) — same fill-from-back
