# Two Pointers — Move Zeroes

*[↗ LeetCode: Move Zeroes](https://leetcode.com/problems/move-zeroes/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

Move all zeros to end, preserving order of non-zeros. In-place.

## Approach — Slow/fast write pointer

**Insight.** `write` points to the next slot for a non-zero; `read` scans. Copy non-zeros forward, then zero-fill the tail. Alternatively, swap on the fly.

```java
void moveZeroes(int[] nums) {
    int write = 0;
    for (int read = 0; read < nums.length; read++)
        if (nums[read] != 0) nums[write++] = nums[read];
    while (write < nums.length) nums[write++] = 0;
}
```

**One-pass swap variant** (fewer writes when array is mostly zeros):

```java
void moveZeroes2(int[] nums) {
    int write = 0;
    for (int read = 0; read < nums.length; read++)
        if (nums[read] != 0) { int t = nums[read]; nums[read] = nums[write]; nums[write++] = t; }
}
```

**Complexity** — Time **O(n)**; Space **O(1)**.

## Related problems

- [Remove Element](https://leetcode.com/problems/remove-element/) — same slow/fast pattern
- [Sort Array By Parity](/problems/sort-array-by-parity)
