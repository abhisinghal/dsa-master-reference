# Divide & Conquer — Count of Range Sum

*[↗ LeetCode: Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/divide-conquer)

**The one thing that changes vs the flagship for this pattern:** Run merge sort over prefix sums and count prefix differences in `[lower, upper]`.

## The pattern this problem belongs to

This variation of Divide & Conquer shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Divide & Conquer](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/divide-conquer) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Divide & Conquer](/patterns/divide-conquer) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `Count of Range Sum` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/divide-conquer) table for the family tree.
