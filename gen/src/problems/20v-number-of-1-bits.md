# Bit Manipulation — Number of 1 Bits

*[↗ LeetCode: Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

Return the popcount (number of set bits) of an unsigned integer.

---

## Approach 1 — Loop bits
```java
int hammingWeight(int n) {
    int count = 0;
    for (int i = 0; i < 32; i++) if ((n & (1 << i)) != 0) count++;
    return count;
}
```

---

## Approach 2 — Kernighan's trick (clear lowest set bit)
**Insight.** `n & (n-1)` clears the lowest set bit. Iterate until 0 → number of iterations = popcount.

```java
int hammingWeight2(int n) {
    int count = 0;
    while (n != 0) { n &= n - 1; count++; }
    return count;
}
```

---

## Approach 3 — Built-in
```java
int hammingWeight3(int n) { return Integer.bitCount(n); }
```

**Complexity** — All **O(#set bits)** at most; Approach 1 always O(32).

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Loop bits | — | — | baseline |
| Kernighan's trick (clear lowest set bit) | — | — | improved |
| Built-in | O(#set bits) | O(32) | optimum |

## When to use which

- **State it for signal** → Loop bits (—). Correct baseline; call it out then move on.
- **Intermediate refinement** → Kernighan's trick (clear lowest set bit) (—).
- **Ship this** → Built-in (O(#set bits), O(32)). Expected optimum in interview.

## Related problems

- [Counting Bits](/problems/counting-bits) — 0..n via Kernighan DP
- [Hamming Distance](/problems/hamming-distance) — popcount of XOR
- [Reverse Bits](/problems/reverse-bits)
