# Two Pointers — Sort Array By Parity

*[↗ LeetCode: Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

Rearrange so all even values come before all odd. Any valid partition accepted.

**Example 1** — `nums=[3,1,2,4]` → `[2,4,3,1]` or `[4,2,3,1]` etc.
**Example 2** — `nums=[0]` → `[0]`

**Constraints** — `1 ≤ n ≤ 5000`.

---

## Approach — Opposing pointers + swap (canonical)

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

**Trap** — for stable ordering (preserving relative order), use slow/fast writer instead.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Opposing 2p | **O(n)** | O(1) | canonical |

## When to use which

- **"Any valid partition"** → opposing 2p.
- **"Stable ordering"** → slow/fast writer + zero-fill (order-preserving).
- **Three-way partition** → Dutch national flag.

## Related problems

- [Sort Colors](https://leetcode.com/problems/sort-colors/) — 3-way
- [Move Zeroes](/problems/move-zeroes)
