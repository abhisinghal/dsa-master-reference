# Top-K / Heap — Kth Largest Element in a Stream

*[↗ LeetCode: Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/top-k-heap)

**The one thing that changes vs the flagship for this pattern:** keep a size-k **min**-heap alive across `add` calls; root is always the running kth largest

## The pattern this problem belongs to

This variation of Top-K / Heap shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Top-K / Heap](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/top-k-heap) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Top-K / Heap](/patterns/top-k-heap) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `Kth Largest Element in a Stream` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/top-k-heap) table for the family tree.
