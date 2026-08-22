# Sliding Window — Minimum Window Substring

*[↗ LeetCode: Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/sliding-window)

Smallest window in `s` containing every char of `t` (with multiplicity).

---

## Approach 1 — Enumerate all substrings
O(n²·|t|).

---

## Approach 2 — Sliding window + need/have counter
**Insight.** Track `need = Σ counts in t`. Maintain a window; extend `r`; whenever a character reduces the "deficit", decrement `have`. Once `have == need`, shrink from `l` while the window still satisfies. Record min.

```java
String minWindow(String s, String t) {
    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;
    int required = t.length(), have = 0;
    int bestL = 0, bestLen = Integer.MAX_VALUE;
    int l = 0;
    for (int r = 0; r < s.length(); r++) {
        char c = s.charAt(r);
        if (need[c]-- > 0) have++;
        while (have == required) {
            if (r - l + 1 < bestLen) { bestLen = r - l + 1; bestL = l; }
            char lc = s.charAt(l++);
            if (++need[lc] > 0) have--;
        }
    }
    return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestL, bestL + bestLen);
}
```

**Invariant.** `need[c]` may go negative for chars over-represented in the window — that's fine; only positive values count toward deficit.

**Complexity** — Time **O(n)**; Space **O(σ)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Enumerate all substrings | O(n²·|t|) | — | baseline |
| Sliding window + need/have counter | O(n) | O(σ) | optimum |

## When to use which

- **State it for signal** → Enumerate all substrings (O(n²·|t|)). Correct baseline; call it out then move on.
- **Ship this** → Sliding window + need/have counter (O(n), O(σ)). Expected optimum in interview.

## Related problems

- [Minimum Window Subsequence](/problems/minimum-window-subsequence) — order matters
- [Substring with Concatenation of All Words](/problems/substring-with-concatenation-of-all-words)
- [Permutation in String](/problems/permutation-in-string)
