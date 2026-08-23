# DP — Regular Expression Matching

*[↗ LeetCode: Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Uber" />

Match `s` against `p` with `.` (any char) and `*` (0+ of prev char).

**Example 1** — `s="aa", p="a"` → `false`
**Example 2** — `s="aa", p="a*"` → `true`
**Example 3** — `s="ab", p=".*"` → `true`

**Constraints** — `1 ≤ |s|, |p| ≤ 20`.


<Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

## Approach — 2D DP (canonical)

**Insight.** `dp[i][j]` = whether `s[..i]` matches `p[..j]`.
- `p[j-1] == '*'`:
  - Zero: `dp[i][j-2]`.
  - One+: if `s[i-1]` matches `p[j-2]`, also `dp[i-1][j]`.
- Else if match: `dp[i-1][j-1]`.

```java
boolean isMatch(String s, String p) {
    int m = s.length(), n = p.length();
    boolean[][] dp = new boolean[m + 1][n + 1];
    dp[0][0] = true;
    for (int j = 2; j <= n; j++)
        if (p.charAt(j-1) == '*') dp[0][j] = dp[0][j-2];
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++) {
            if (p.charAt(j-1) == '*') {
                dp[i][j] = dp[i][j-2];
                if (matches(s, p, i, j-1)) dp[i][j] |= dp[i-1][j];
            } else if (matches(s, p, i, j)) dp[i][j] = dp[i-1][j-1];
        }
    return dp[m][n];
}
boolean matches(String s, String p, int i, int j) {
    char sc = s.charAt(i-1), pc = p.charAt(j-1);
    return pc == '.' || pc == sc;
}
```

<CodeTrace
  title="2D DP (canonical)"
  :values="['a', 'a']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(mn)**; Space **O(mn)** (compressible).

---

## Try it yourself

<JavaRunner problem-slug="regular-expression-matching" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| 2D DP | **O(mn)** | O(mn) | canonical |

## When to use which

- **`.` and `*`** → this DP.
- **`?` and `*`** → [Wildcard Matching](https://leetcode.com/problems/wildcard-matching/).
- **Full regex** → NFA/DFA.

## Related problems

- [Wildcard Matching](https://leetcode.com/problems/wildcard-matching/)
- [Edit Distance](/problems/edit-distance)