# Bit Manipulation — Number of 1 Bits

*[↗ LeetCode: Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/bit-manip)

**The one thing that changes vs the flagship for this pattern:** Brian Kernighan's `x &= x - 1` clears the lowest set bit each step

## The pattern this problem belongs to

This variation of Bit Manipulation shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Bit Manipulation](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/bit-manip) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Bit Manipulation](/patterns/bit-manip) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `Number of 1 Bits` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/bit-manip) table for the family tree.
