# Sliding Window — Longest Palindromic Substring

*[↗ LeetCode: Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

Longest palindromic substring of `s`.

&gt; Filed under Sliding Window in the curriculum, but the O(n²) solution is "expand around center" (two pointers), and the O(n) solution is Manacher's.

---

## Approach 1 — Try every substring O(n³)

---

## Approach 2 — DP `pal[i][j]`
O(n²) time and space.

---

## Approach 3 — Expand around each center
**Insight.** A palindrome has either an odd (single) center or an even (double) center — 2n-1 centers total.



```java
String longestPalindrome(String s) {
    int start = 0, end = 0;
    for (int i = 0; i < s.length(); i++) {
        int l1 = expand(s, i, i);
        int l2 = expand(s, i, i + 1);
        int len = Math.max(l1, l2);
        if (len > end - start) {
            start = i - (len - 1) / 2;
            end = i + len / 2;
        }
    }
    return s.substring(start, end + 1);
}
int expand(String s, int l, int r) {
    while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; }
    return r - l - 1;
}
```



**Complexity** — Time **O(n²)**; Space **O(1)**.

---

## Approach 4 — Manacher's algorithm
Insert sentinels; maintain palindrome-radius array with reuse across mirrored centers. **O(n)**. Beautiful but rarely required in interviews unless asked "can you go faster than n²".

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Try every substring O(n³) | — | — | baseline |
| DP `pal[i][j]` | O(n²) | — | improved |
| Expand around each center | O(n²) | O(1) | improved |
| Manacher's algorithm | O(n) | — | optimum |

## When to use which

- **State it for signal** → Try every substring O(n³) (—). Correct baseline; call it out then move on.
- **Intermediate refinement** → DP `pal[i][j]` (O(n²)).
- **Intermediate refinement** → Expand around each center (O(n²)).
- **Ship this** → Manacher's algorithm (O(n), —). Expected optimum in interview.

## Related problems

- [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) — count all
- [Longest Palindromic Subsequence](/problems/longest-palindromic-subsequence) — DP
