# Two Pointers — Sort Array By Parity

*[↗ LeetCode: Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

Rearrange so all even values come before all odd. Any valid partition accepted.

---

## Approach 1 — Opposing pointers, swap on mismatch
**Insight.** `l` from left seeks first odd; `r` from right seeks first even; swap; repeat.



```java
int[] sortArrayByParity(int[] nums) {
    int l = 0, r = nums.length - 1;
    while (l < r) {
        if (nums[l] % 2 == 0) l++;
        else if (nums[r] % 2 == 1) r--;
        else { int t = nums[l]; nums[l++] = nums[r]; nums[r--] = t; }
    }
    return nums;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

**Trap.** For stable ordering (preserve original relative order within each group) → use a slow/fast writer, not opposing pointers.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Opposing pointers, swap on mismatch | O(n) | O(1) | primary |

## When to use which

- **Ship this** → Opposing pointers, swap on mismatch (O(n), O(1)). The pattern's standard solution.

## Related problems

- [Sort Colors (Dutch flag)](https://leetcode.com/problems/sort-colors/) — 3-way partition
- [Move Zeroes](/problems/move-zeroes)
