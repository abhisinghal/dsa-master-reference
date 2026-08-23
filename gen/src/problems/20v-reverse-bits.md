# Bit Manipulation — Reverse Bits

*[↗ LeetCode: Reverse Bits](https://leetcode.com/problems/reverse-bits/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

<CompanyTags companies="Meta, Amazon, Google, Apple, Microsoft, Adobe" />

Reverse the bits of a 32-bit unsigned integer.

**Example 1** — `n = 0000...1010 (43261596)` → `0011...1001 (964176192)`

**Constraints** — 32 bits.


<Hints
  hint1="Is there a bit-level trick? XOR cancels duplicates, `n & (n-1)` clears the lowest bit, `n | (1 << k)` sets bit k."
  hint2="For subset problems: iterate `mask` from 0 to 2ⁿ−1; bit `i` set means element `i` chosen."
  hint3="For ’find the unique/missing’: XOR the whole array with 0..n; pairs cancel, missing survives."
/>
---

## Approach 1 — Bit-by-bit

```java
int reverseBits1(int n) {
    int r = 0;
    for (int i = 0; i < 32; i++) {
        r = (r << 1) | (n & 1);
        n >>>= 1;
    }
    return r;
}
```

O(32).

## Approach 2 — SWAR parallel bit swap

**Insight.** Swap adjacent 1-bit groups; then 2-bit; then 4-bit; then 8-bit; then 16-bit halves. Each step is O(1) via bit masks.

```java
int reverseBits(int n) {
    n = (n >>> 1 & 0x55555555) | (n & 0x55555555) << 1;
    n = (n >>> 2 & 0x33333333) | (n & 0x33333333) << 2;
    n = (n >>> 4 & 0x0f0f0f0f) | (n & 0x0f0f0f0f) << 4;
    n = (n >>> 8 & 0x00ff00ff) | (n & 0x00ff00ff) << 8;
    return n >>> 16 | n << 16;
}
```

**Complexity** — Time **O(1)**; Space **O(1)**.

## Approach 3 — Cache 8-bit chunks

For repeated calls, precompute an int[256] table of reversed bytes.

---

## Try it yourself

<JavaRunner problem-slug="reverse-bits" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Bit-by-bit | O(32) | O(1) | baseline |
| SWAR parallel | **O(1)** | O(1) | canonical |
| Byte cache | O(1) w/ table | O(256) | production |

## When to use which

- **Interview** — SWAR shows constant-time mastery.
- **Production** — table cache if called in tight loop.

<AiCompanion problem-slug="reverse-bits" pattern-hint="bit manipulation" />

## Related problems

- [Number of 1 Bits](/problems/number-of-1-bits) — SWAR popcount
- [Reverse Integer](https://leetcode.com/problems/reverse-integer/)

<FeedbackWidget problem-slug="reverse-bits" />
