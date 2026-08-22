# Sliding Window — Longest Substring with At Most K Distinct

*[↗ LeetCode: Longest Substring with At Most K Distinct](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

**The one thing that changes vs the flagship for this pattern:** allow up to `K` different characters instead of zero repeats; shrink while the distinct-count exceeds `K` (track counts in a small map)

## The pattern this problem belongs to

This variation of Sliding Window shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Sliding Window](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/sliding-window) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Sliding Window](/patterns/sliding-window) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `Longest Substring with At Most K Distinct` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/sliding-window) table for the family tree.
