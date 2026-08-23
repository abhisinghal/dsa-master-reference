# Sliding Window — Minimum Window Subsequence

*[↗ LeetCode: Minimum Window Subsequence](https://leetcode.com/problems/minimum-window-subsequence/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/sliding-window)

Find the min window in `s1` such that `s2` is a subsequence.

**Example 1** — `s1="abcdebdde", s2="bde"` → `"bcde"`
**Example 2** — `s1="jmeqksfrsdcmsiwvaovztaqenprpvnbstl", s2="k"` → `"k"`

**Constraints** — `1 ≤ |s1| ≤ 2·10⁴`; `1 ≤ |s2| ≤ 100`.


&lt;Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/&gt;
---

## Approach 1 — DP `dp[i][j]` = latest start of match

O(m·n) time and space.

## Approach 2 — Two-pointer forward + backward (canonical)

**Insight.** Advance `i` in `s1` matching `s2` chars in order. On full match, walk backward from end index to shrink to minimal window that still contains `s2` as subsequence. Repeat.



```java
String minWindow(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    int bestLen = Integer.MAX_VALUE, bestStart = -1;
    int i = 0;
    while (i < m) {
        int j = 0;
        while (i < m) {
            if (s1.charAt(i) == s2.charAt(j)) {
                j++;
                if (j == n) break;
            }
            i++;
        }
        if (i == m) break;
        int end = i;
        j = n - 1;
        while (j >= 0) {
            if (s1.charAt(i) == s2.charAt(j)) j--;
            i--;
        }
        i += 2;
        int start = i - 1;
        if (end - start + 1 < bestLen) { bestLen = end - start + 1; bestStart = start; }
    }
    return bestStart < 0 ? "" : s1.substring(bestStart, bestStart + bestLen);
}
```



<CodeTrace
  title="Forward + backward — s1='abcdebdde', s2='bde'"
  :values="['a','b','c','d','e','b','d','d','e']"
  :windowKeys="['i','j']"
  :cellWidth="26"
  :steps='[
    { pointers: { i: 4, j: 3 }, vars: { end: 4 }, note: "forward: full match at idx 4 (a-b-c-d-e)" },
    { pointers: { i: 1, j: -1 }, vars: { start: 1 }, note: "backward: minimal start at idx 1" },
    { pointers: {}, vars: { window: "bcde", len: 4 }, note: "record best; continue" }
  ]'
/>

**Complexity** — Time **O(m · n)** worst; often much faster.

---

## Try it yourself

<JavaRunner problem-slug="minimum-window-subsequence" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DP | O(m·n) | O(m·n) | works |
| 2p forward+backward | **O(m·n)** worst | O(1) | canonical |

## When to use which

- **Subsequence** (order matters) → this pattern.
- **Substring** (set membership) → [Minimum Window Substring](/problems/minimum-window-substring).
- **"Any window containing s2"** → forward sweep only.

&lt;AiCompanion problem-slug="minimum-window-subsequence" pattern-hint="sliding window" /&gt;

## Related problems

- [Minimum Window Substring](/problems/minimum-window-substring)
- [Is Subsequence](https://leetcode.com/problems/is-subsequence/)
- [Longest Common Subsequence](/problems/longest-common-subsequence)

&lt;FeedbackWidget problem-slug="minimum-window-subsequence" /&gt;
