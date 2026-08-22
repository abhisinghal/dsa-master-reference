# Bit Manipulation — Reverse Bits

*[↗ LeetCode: Reverse Bits](https://leetcode.com/problems/reverse-bits/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

Reverse the bits of a 32-bit unsigned integer.

## Approach 1 — Bit-by-bit



```java
int reverseBits(int n) {
    int result = 0;
    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1);
        n >>>= 1;
    }
    return result;
}
```



## Approach 2 — Byte swap + cache (interview follow-up)

If called many times, cache the reversal of each 8-bit chunk in a size-256 table; assemble result in 4 lookups.

## Approach 3 — SWAR (parallel bit swap)

**Insight.** Swap adjacent 1-bit groups, then 2-bit, 4-bit, 8-bit, 16-bit.



```java
int reverseBits3(int n) {
    n = (n >>> 1 & 0x55555555) | (n & 0x55555555) << 1;
    n = (n >>> 2 & 0x33333333) | (n & 0x33333333) << 2;
    n = (n >>> 4 & 0x0f0f0f0f) | (n & 0x0f0f0f0f) << 4;
    n = (n >>> 8 & 0x00ff00ff) | (n & 0x00ff00ff) << 8;
    return n >>> 16 | n << 16;
}
```



**Complexity** — All **O(1)**; SWAR is fastest constant.

## Related problems

- [Number of 1 Bits](/problems/number-of-1-bits) — same SWAR pattern for popcount
