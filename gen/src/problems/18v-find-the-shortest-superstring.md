# DP — Find the Shortest Superstring

*[↗ LeetCode: Find the Shortest Superstring](https://leetcode.com/problems/find-the-shortest-superstring/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Google, Amazon" />

Return shortest string containing every given word as substring.

**Constraints** — `1 ≤ n ≤ 12`.

**Example 1** — `words=["alex","loves","leetcode"]` → `"alexlovesleetcode"`
**Example 2** — `words=["catg","ctaagt","gcta","ttca","atgcatc"]` → `"gctaagttcatgcatc"`


<Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

## Approach — Bitmask TSP-style DP + overlap precompute (canonical)

**Insight.**
1. `overlap[i][j]` = max suffix of `words[i]` that is prefix of `words[j]`.
2. `dp[mask][i]` = shortest length ending at word i after using set mask.
3. Reconstruct path via predecessor tracking.

```java
String shortestSuperstring(String[] words) {
    int n = words.length;
    int[][] ov = new int[n][n];
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (i != j) ov[i][j] = computeOverlap(words[i], words[j]);
    int full = 1 << n;
    int[][] dp = new int[full][n];
    int[][] par = new int[full][n];
    for (int[] r : dp) Arrays.fill(r, Integer.MAX_VALUE / 2);
    for (int i = 0; i < n; i++) dp[1 << i][i] = words[i].length();
    for (int mask = 1; mask < full; mask++)
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) == 0) continue;
            for (int j = 0; j < n; j++) {
                if ((mask & (1 << j)) != 0) continue;
                int cand = dp[mask][i] + words[j].length() - ov[i][j];
                int nMask = mask | (1 << j);
                if (cand < dp[nMask][j]) { dp[nMask][j] = cand; par[nMask][j] = i; }
            }
        }
    int last = 0;
    for (int i = 1; i < n; i++) if (dp[full-1][i] < dp[full-1][last]) last = i;
    int[] order = new int[n];
    int mask = full - 1;
    for (int k = n - 1; k >= 0; k--) { order[k] = last; int prev = par[mask][last]; mask ^= 1 << last; last = prev; }
    StringBuilder sb = new StringBuilder(words[order[0]]);
    for (int k = 1; k < n; k++) sb.append(words[order[k]].substring(ov[order[k-1]][order[k]]));
    return sb.toString();
}
int computeOverlap(String a, String b) {
    int max = Math.min(a.length(), b.length());
    for (int k = max; k > 0; k--) if (a.endsWith(b.substring(0, k))) return k;
    return 0;
}
```

<CodeTrace
  title="Bitmask TSP-style DP + overlap precompute (canonical)"
  :values="['alex', 'loves', 'leetcode']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n² · 2ⁿ)**; Space **O(n · 2ⁿ)**.

---

## Try it yourself

<JavaRunner problem-slug="find-the-shortest-superstring" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Bitmask TSP DP | **O(n² · 2ⁿ)** | O(n · 2ⁿ) | canonical |

## When to use which

- **Small n TSP-style** → bitmask DP.
- **Approximation** → greedy longest-overlap merge.

## Related problems

- [Shortest Path Visiting All Nodes](/problems/shortest-path-visiting-all-nodes)