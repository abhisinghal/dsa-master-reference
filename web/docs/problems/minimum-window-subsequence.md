# Sliding Window — Minimum Window Subsequence

*[↗ LeetCode: Minimum Window Subsequence](https://leetcode.com/problems/minimum-window-subsequence/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/sliding-window)

Smallest window in `s` such that `t` is a **subsequence** (order matters).

---

## Approach 1 — DP `dp[i][j] = latest start of match in s[..i] using t[..j]`
O(m·n) time and space.

---

## Approach 2 — Two-pointer forward + backward
**Insight.** Advance `i` in `s` matching `t` chars in order; when full match found at end index `iEnd`, walk **backward** from `iEnd` to shrink to minimal window that still contains `t` as subsequence. Repeat starting after the previous match's start.



```java
String minWindow(String s, String t) {
    int m = s.length(), n = t.length();
    int bestLen = Integer.MAX_VALUE, bestStart = -1;
    int i = 0;
    while (i < m) {
        int j = 0;
        while (i < m) {
            if (s.charAt(i) == t.charAt(j)) {
                j++;
                if (j == n) break;
            }
            i++;
        }
        if (i == m) break;
        int end = i;
        j = n - 1;
        while (j >= 0) {
            if (s.charAt(i) == t.charAt(j)) j--;
            i--;
        }
        i += 2; // start = i+1 after loop overshoot; adjust
        int start = i - 1;
        if (end - start + 1 < bestLen) { bestLen = end - start + 1; bestStart = start; }
    }
    return bestStart < 0 ? "" : s.substring(bestStart, bestStart + bestLen);
}
```



**Complexity** — Time **O(m · n)** worst case; often much faster.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| DP `dp[i][j] = latest start of match in s[… | O(m·n) | — | baseline |
| Two-pointer forward + backward | O(m · n) | — | optimum |

## When to use which

- **State it for signal** → DP `dp[i][j] = latest start of match in s[..i] using t[..j]` (O(m·n)). Correct baseline; call it out then move on.
- **Ship this** → Two-pointer forward + backward (O(m · n), —). Expected optimum in interview.

## Related problems

- [Minimum Window Substring](/problems/minimum-window-substring) — set membership, not subsequence
- [Is Subsequence](https://leetcode.com/problems/is-subsequence/) — the primitive
