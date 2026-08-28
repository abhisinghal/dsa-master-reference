# Bit Manipulation — Power of Two

*[↗ LeetCode: Power of Two](https://leetcode.com/problems/power-of-two/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

<CompanyTags companies="Meta, Amazon, Google, Microsoft" />

Return true iff `n` is a positive power of two.

**Example 1** — `n=1` → `true` (2⁰)
**Example 2** — `n=16` → `true`
**Example 3** — `n=3` → `false`

**Constraints** — `-2³¹ ≤ n ≤ 2³¹−1`. Brute divide-by-2 loop is O(log n) = 30 iters at n=2³¹. Bit trick `n>0 && (n&(n-1))==0` is 2 ops = <1 ns — 10⁹ checks/sec.
<Hints
  hint1="Is there a bit-level trick? XOR cancels duplicates, `n & (n-1)` clears the lowest bit, `n | (1 << k)` sets bit k."
  hint2="For subset problems: iterate `mask` from 0 to 2ⁿ−1; bit `i` set means element `i` chosen."
  hint3="For ’find the unique/missing’: XOR the whole array with 0..n; pairs cancel, missing survives."
/>
---

<MarkSolved problem-slug="power-of-two" /> <Bookmark problem-slug="power-of-two" />

<InterviewTimer problem-slug="power-of-two" />



## Approach 1 — Divide by 2

O(log n).

## Approach 2 — `n & (n-1) == 0` (canonical)

**Insight.** A positive power of two has exactly one bit set. `n & (n-1)` clears the lowest set bit → 0 iff there was only one.

**Trap** — guard `n > 0`. For `n = 0`, `0 & -1 == 0` would falsely return true.

```java
boolean isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
```

**Complexity** — Time **O(1)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="power-of-two" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Divide by 2 | O(log n) | O(1) | works |
| `n & (n-1) == 0` | **O(1)** | O(1) | canonical |

## When to use which

- **"Power of 2"** → bit trick.
- **"Power of 4"** → also check `n & 0x55555555 != 0` (bit at even position).
- **"Power of 3"** → no clean bit trick — `1162261467 % n == 0` (largest power of 3 ≤ INT_MAX).

<AiCompanion problem-slug="power-of-two" pattern-hint="bit manipulation" />

## Related problems

- [Power of Three](https://leetcode.com/problems/power-of-three/)
- [Power of Four](https://leetcode.com/problems/power-of-four/)
- [Number of 1 Bits](/problems/number-of-1-bits)

<FeedbackWidget problem-slug="power-of-two" />

<RelatedProblems problems="single-number::Single Number|hamming-distance::Hamming Distance|find-the-difference::Find The Difference" />
