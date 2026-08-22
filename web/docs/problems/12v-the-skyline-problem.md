# Sweep Line — The Skyline Problem

*[↗ LeetCode: The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sweep-line)

**The one thing that changes vs the flagship for this pattern:** Events add/remove building heights; the swept state is a max-heap or multiset, not a count.

## The pattern this problem belongs to

This variation of Sweep Line shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Sweep Line](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/sweep-line) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Sweep Line](/patterns/sweep-line) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `The Skyline Problem` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/sweep-line) table for the family tree.
