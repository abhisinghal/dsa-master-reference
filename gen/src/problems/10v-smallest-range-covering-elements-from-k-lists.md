# K-way Merge — Smallest Range Covering Elements from K Lists

*[↗ LeetCode: Smallest Range Covering Elements from K Lists](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/k-way-merge)

**The one thing that changes vs the flagship for this pattern:** Keep a full frontier, and compare `heapMin..curMax` before advancing the minimum stream.

## The pattern this problem belongs to

This variation of K-way Merge shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for K-way Merge](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/k-way-merge) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [K-way Merge](/patterns/k-way-merge) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `Smallest Range Covering Elements from K Lists` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/k-way-merge) table for the family tree.
