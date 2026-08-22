# Sliding Window — Longest Substring with **exactly** K distinct

*[↗ LeetCode: Longest Substring with **exactly** K distinct](https://leetcode.com/problems/subarrays-with-k-different-integers/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

**The one thing that changes vs the flagship for this pattern:** Exactly-K validity isn't monotone: a window with 3 distinct isn't "valid" for K=2 nor for K=4.

## The pattern this problem belongs to

This variation of Sliding Window shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Sliding Window](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/sliding-window) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Sliding Window](/patterns/sliding-window) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `Longest Substring with **exactly** K distinct` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/sliding-window) table for the family tree.
