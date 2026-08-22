# Backtracking — Combination Sum IV

*[↗ LeetCode: Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

**The one thing that changes vs the flagship for this pattern:** it *counts ordered* ways → drop backtracking for a 1-D DP (`dp[t] += dp[t-num]`)

## The pattern this problem belongs to

This variation of Backtracking shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Backtracking](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/backtracking) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Backtracking](/patterns/backtracking) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `Combination Sum IV` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/backtracking) table for the family tree.
