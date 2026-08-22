# Two Pointers — Move Zeroes

*[↗ LeetCode: Move Zeroes](https://leetcode.com/problems/move-zeroes/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

Move all zeros to end preserving order of non-zeros. In-place.

**Example 1** — `nums=[0,1,0,3,12]` → `[1,3,12,0,0]`
**Example 2** — `nums=[0]` → `[0]`

**Constraints** — `1 ≤ n ≤ 10⁴`.

---

## Approach 1 — Two-pass write

Copy non-zeros forward; zero-fill tail.

## Approach 2 — Slow/fast write pointer (canonical)

**Insight.** One pointer for read, one for the next slot to write.

```java
void moveZeroes(int[] nums) {
    int w = 0;
    for (int r = 0; r < nums.length; r++)
        if (nums[r] != 0) nums[w++] = nums[r];
    while (w < nums.length) nums[w++] = 0;
}
```

## Approach 3 — Swap on the fly (fewer writes)

Use when array is mostly zeros — each non-zero causes one swap.

```java
void moveZeroesSwap(int[] nums) {
    int w = 0;
    for (int r = 0; r < nums.length; r++)
        if (nums[r] != 0) { int t = nums[r]; nums[r] = nums[w]; nums[w++] = t; }
}
```

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Two-pass | O(n) | O(1) | baseline |
| Slow/fast writer | **O(n)** | O(1) | canonical |
| Swap-in-place | O(n) | O(1) | fewer writes |

## When to use which

- **Standard** → slow/fast.
- **Minimize writes** (SSD wear, etc.) → swap variant.
- **Removes / partition** → same template family.

## Related problems

- [Remove Element](https://leetcode.com/problems/remove-element/)
- [Sort Array By Parity](/problems/sort-array-by-parity)
