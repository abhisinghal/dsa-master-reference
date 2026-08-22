# Two Pointers — 3Sum Smaller

*[↗ LeetCode: 3Sum Smaller](https://leetcode.com/problems/3sum-smaller/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

**The one thing that changes vs the flagship for this pattern:** count triplets with sum `< target`; when `a[lo]+a[hi] < target`, *all* `hi−lo` pairs qualify at once, so add them in one shot

## The pattern this problem belongs to

This variation of Two Pointers shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Two Pointers](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/two-pointers) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Two Pointers](/patterns/two-pointers) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `3Sum Smaller` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/two-pointers) table for the family tree.
