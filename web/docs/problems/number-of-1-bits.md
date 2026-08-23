# Bit Manipulation — Number of 1 Bits

*[↗ LeetCode: Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

&lt;CompanyTags companies="Meta, Amazon, Apple, Google, Microsoft" /&gt;

Return the popcount (number of set bits) of an unsigned 32-bit integer.

**Example 1** — `n=00000000000000000000000000001011` → `3`
**Example 2** — `n=11111111111111111111111111111101` → `31`

**Constraints** — 32-bit unsigned.


&lt;Hints
  hint1="Is there a bit-level trick? XOR cancels duplicates, `n & (n-1)` clears the lowest bit, `n | (1 << k)` sets bit k."
  hint2="For subset problems: iterate `mask` from 0 to 2ⁿ−1; bit `i` set means element `i` chosen."
  hint3="For ’find the unique/missing’: XOR the whole array with 0..n; pairs cancel, missing survives."
/&gt;
---

## Approach 1 — Loop all 32 bits



```java
int hammingWeight1(int n) {
    int c = 0;
    for (int i = 0; i < 32; i++) if ((n & (1 << i)) != 0) c++;
    return c;
}
```



O(32) always.

## Approach 2 — Kernighan's trick (clear lowest set bit)

**Insight.** `n & (n-1)` clears the lowest set bit. Iterate until 0; count iterations.



```java
int hammingWeight(int n) {
    int c = 0;
    while (n != 0) { n &= n - 1; c++; }
    return c;
}
```



**Complexity** — Time **O(# set bits)**; Space **O(1)**.

## Approach 3 — Built-in



```java
int hammingWeight3(int n) { return Integer.bitCount(n); }
```



Uses hardware popcount when available.

---

## Try it yourself

<JavaRunner problem-slug="number-of-1-bits" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| 32-bit scan | O(32) | O(1) | baseline |
| Kernighan | O(#set bits) | O(1) | canonical |
| `Integer.bitCount` | O(1) HW | O(1) | production |

## When to use which

- **Interview** → Kernighan for the "aha".
- **Production** → `Integer.bitCount`.
- **Popcount many ints** → SWAR parallel popcount for batches.

&lt;AiCompanion problem-slug="number-of-1-bits" pattern-hint="bit manipulation" /&gt;

## Related problems

- [Counting Bits](/problems/counting-bits) — 0..n via Kernighan DP
- [Hamming Distance](/problems/hamming-distance)
- [Reverse Bits](/problems/reverse-bits)