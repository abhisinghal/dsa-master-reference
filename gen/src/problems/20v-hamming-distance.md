# Bit Manipulation — Hamming Distance

*[↗ LeetCode: Hamming Distance](https://leetcode.com/problems/hamming-distance/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

Return number of positions where the bits of `x` and `y` differ.

---

## Approach 1 — Popcount of XOR
**Insight.** `x XOR y` has 1s exactly where the bits differ. Answer = popcount.

```java
int hammingDistance(int x, int y) {
    return Integer.bitCount(x ^ y);
}
```

**Complexity** — Time **O(1)** (32 bits); Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Popcount of XOR | O(1) | O(1) | primary |

## When to use which

- **Ship this** → Popcount of XOR (O(1), O(1)). The pattern's standard solution.

## Related problems

- [Total Hamming Distance](https://leetcode.com/problems/total-hamming-distance/) — sum over all pairs; per-bit counting
- [Number of 1 Bits](/problems/number-of-1-bits)
