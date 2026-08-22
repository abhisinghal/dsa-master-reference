# Backtracking — Permutations II (with duplicates)

*[↗ LeetCode: Permutations II (with duplicates)](https://leetcode.com/problems/permutations-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

**The one thing that changes vs the flagship for this pattern:** sort, then skip `i>0 && a[i]==a[i-1] && !used[i-1]` to avoid duplicate orderings

## The pattern this problem belongs to

This variation of Backtracking shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Backtracking](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/backtracking) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Backtracking](/patterns/backtracking) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `Permutations II (with duplicates)` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/backtracking) table for the family tree.
