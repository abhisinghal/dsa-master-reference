# Top-K / Heap — K Closest Points to Origin

*[↗ LeetCode: K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/top-k-heap)

**The one thing that changes vs the flagship for this pattern:** a **max**-heap of size k keyed on squared distance; the farthest current winner is easiest to evict

## The pattern this problem belongs to

This variation of Top-K / Heap shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Top-K / Heap](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/top-k-heap) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Top-K / Heap](/patterns/top-k-heap) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `K Closest Points to Origin` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/top-k-heap) table for the family tree.
