# Monotonic Stack — Sum of Subarray Minimums

*[↗ LeetCode: Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/monotonic-stack)

**The one thing that changes vs the flagship for this pattern:** each element contributes `min × (countLeft × countRight)`; the monotonic stack gives those boundary counts

## The pattern this problem belongs to

This variation of Monotonic Stack shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Monotonic Stack](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/monotonic-stack) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Monotonic Stack](/patterns/monotonic-stack) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `Sum of Subarray Minimums` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/monotonic-stack) table for the family tree.
