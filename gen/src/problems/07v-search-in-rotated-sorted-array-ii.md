# Binary Search — Search in Rotated Array II (with duplicates)

*[↗ LeetCode: Search in Rotated Array II (with duplicates)](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/binary-search)

**The one thing that changes vs the flagship for this pattern:** when `a[lo] == a[mid] == a[hi]` you can't tell which half is sorted, so shrink both ends by one (worst case degrades to O(n))

## The pattern this problem belongs to

This variation of Binary Search shares the flagship's skeleton — see the pattern's canonical multi-approach walkthrough for the full brute-force → optimized ladder, then apply the tweak above.

- [→ Flagship problem for Binary Search](/problems/) — see the multi-approach walkthrough
- [→ Pattern chapter (theory + all variations in context)](/patterns/binary-search) — includes this problem's approach + code + trace + traps

## Solution sketch

The pattern chapter's [Binary Search](/patterns/binary-search) walks the brute → optimized ladder for this problem inline; a dedicated multi-approach page is planned. In the meantime:

1. **Read the pattern chapter's `Search in Rotated Array II (with duplicates)` section** — brute force, Java code, and Execution Trace are already there.
2. **Read the flagship problem's multi-approach walkthrough** — the *shape* of the reasoning is identical.
3. **Apply the tweak above** — that's what distinguishes this variation.

## Related problems in the same pattern

See the pattern chapter's ["Same pattern, new tweaks"](/patterns/binary-search) table for the family tree.
