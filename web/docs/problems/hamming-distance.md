# Bit Manipulation — Hamming Distance

*[↗ LeetCode: Hamming Distance](https://leetcode.com/problems/hamming-distance/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

&lt;CompanyTags companies="Meta, Amazon, Google, Adobe" /&gt;

Return the number of positions where the bits of `x` and `y` differ.

**Example 1** — `x=1, y=4` → `2`
**Example 2** — `x=3, y=1` → `1`

**Constraints** — `0 ≤ x, y ≤ 2³¹−1`.


&lt;Hints
  hint1="Is there a bit-level trick? XOR cancels duplicates, `n & (n-1)` clears the lowest bit, `n | (1 << k)` sets bit k."
  hint2="For subset problems: iterate `mask` from 0 to 2ⁿ−1; bit `i` set means element `i` chosen."
  hint3="For ’find the unique/missing’: XOR the whole array with 0..n; pairs cancel, missing survives."
/&gt;
---

## Approach — Popcount of XOR

**Insight.** `x XOR y` has 1s exactly at differing positions → answer is popcount(x^y).



```java
int hammingDistance(int x, int y) {
    return Integer.bitCount(x ^ y);
}
```



**Complexity** — Time **O(1)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="hamming-distance" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Popcount of XOR | **O(1)** | O(1) | optimum |

## When to use which

- **"Sum of pairwise Hamming distances"** → per-bit counting; see [Total Hamming Distance](https://leetcode.com/problems/total-hamming-distance/).
- **Manhattan-like "min flips to reach y"** → same popcount.

## Related problems

- [Total Hamming Distance](https://leetcode.com/problems/total-hamming-distance/)
- [Number of 1 Bits](/problems/number-of-1-bits)
- [XOR Sum problems]