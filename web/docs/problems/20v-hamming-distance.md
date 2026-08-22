# Bit Manipulation — Hamming Distance

*[↗ LeetCode: Hamming Distance](https://leetcode.com/problems/hamming-distance/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

Return number of positions where the bits of `x` and `y` differ.

## Approach — Popcount of XOR

**Insight.** `x XOR y` has 1s exactly where the bits differ. Answer = popcount.



```java
int hammingDistance(int x, int y) {
    return Integer.bitCount(x ^ y);
}
```



**Complexity** — Time **O(1)** (32 bits); Space **O(1)**.

## Related problems

- [Total Hamming Distance](https://leetcode.com/problems/total-hamming-distance/) — sum over all pairs; per-bit counting
- [Number of 1 Bits](/problems/number-of-1-bits)
