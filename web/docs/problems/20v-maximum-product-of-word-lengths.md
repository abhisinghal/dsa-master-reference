# Bit Manipulation — Maximum Product of Word Lengths

*[↗ LeetCode: Maximum Product of Word Lengths](https://leetcode.com/problems/maximum-product-of-word-lengths/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/bit-manip)

**The one thing that changes vs the flagship for this pattern:** encode each word's letters as a 26-bit mask; two words share no letter iff `maskA & maskB == 0`

## The pattern this problem belongs to

This variation of Bit Manipulation shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Bit Manipulation](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/bit-manip) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Bit Manipulation](/patterns/bit-manip) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `Maximum Product of Word Lengths` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/bit-manip) table for the family tree.
