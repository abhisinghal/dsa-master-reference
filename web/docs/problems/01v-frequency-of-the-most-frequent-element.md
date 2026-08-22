# Sliding Window — Frequency of the Most Frequent Element

*[↗ LeetCode: Frequency of the Most Frequent Element](https://leetcode.com/problems/frequency-of-the-most-frequent-element/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

**The one thing that changes vs the flagship for this pattern:** sort, then window where `windowLen·max − windowSum ≤ k` operations

## The pattern this problem belongs to

This variation of Sliding Window shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Sliding Window](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/sliding-window) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Sliding Window](/patterns/sliding-window) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `Frequency of the Most Frequent Element` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/sliding-window) table for the family tree.
