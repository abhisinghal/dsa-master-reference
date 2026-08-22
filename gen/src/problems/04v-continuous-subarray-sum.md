# Prefix Sum — Continuous Subarray Sum (multiple of k)

*[↗ LeetCode: Continuous Subarray Sum (multiple of k)](https://leetcode.com/problems/continuous-subarray-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

**The one thing that changes vs the flagship for this pattern:** same `mod k` bucketing, but store the earliest index to enforce a length ≥ 2

## The pattern this problem belongs to

This variation of Prefix Sum shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Prefix Sum](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/prefix-sum) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Prefix Sum](/patterns/prefix-sum) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `Continuous Subarray Sum (multiple of k)` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/prefix-sum) table for the family tree.
