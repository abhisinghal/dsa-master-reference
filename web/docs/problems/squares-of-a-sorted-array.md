# Two Pointers — Squares of a Sorted Array

*[↗ LeetCode: Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

Return squares of a sorted (possibly-negative) array, sorted.

**Example 1** — `nums=[-4,-1,0,3,10]` → `[0,1,9,16,100]`
**Example 2** — `nums=[-7,-3,2,3,11]` → `[4,9,9,49,121]`

**Constraints** — `1 ≤ n ≤ 10⁴`; sorted ascending.

---

## Approach 1 — Square then sort

O(n log n).

## Approach 2 — Two pointers filling from back (canonical)

**Insight.** Largest square is at one of the two ends. Compare, place at `k = n-1`, decrement, repeat.



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

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort | O(n log n) | O(n) | baseline |
| Fill from back | **O(n)** | O(n) | canonical |

## When to use which

- **"Sorted array with monotone-transform"** → fill-from-ends technique.
- **In-place mutation** → different — see [Merge Sorted Array](/problems/merge-sorted-array).

## Related problems

- [Merge Sorted Array](/problems/merge-sorted-array)
- [Sort Colors](https://leetcode.com/problems/sort-colors/)
