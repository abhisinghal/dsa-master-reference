# DP — Find the Shortest Superstring

*[↗ LeetCode: Find the Shortest Superstring](https://leetcode.com/problems/find-the-shortest-superstring/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

Given words. Return the shortest string containing every word as a substring.

## Approach — Bitmask TSP-style DP + overlap precompute

**Insight.**
1. Precompute `overlap[i][j]` = max suffix of `words[i]` that is prefix of `words[j]`.
2. `dp[mask][i]` = shortest length ending at word `i` after using set `mask`. Transition: `dp[mask | (1<<j)][j] = min(…, dp[mask][i] + len[j] - overlap[i][j])`.
3. Track predecessors to reconstruct the string.



```java
String shortestSuperstring(String[] words) {
    int n = words.length;
    int[][] ov = new int[n][n];
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (i != j)
        ov[i][j] = computeOverlap(words[i], words[j]);
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
    // find best end
    int last = 0;
    for (int i = 1; i < n; i++) if (dp[full - 1][i] < dp[full - 1][last]) last = i;
    // reconstruct order backwards
    int[] order = new int[n];
    int mask = full - 1;
    for (int k = n - 1; k >= 0; k--) {
        order[k] = last;
        int prev = par[mask][last];
        mask ^= 1 << last;
        last = prev;
    }
    StringBuilder sb = new StringBuilder(words[order[0]]);
    for (int k = 1; k < n; k++) {
        int o = ov[order[k - 1]][order[k]];
        sb.append(words[order[k]].substring(o));
    }
    return sb.toString();
}
int computeOverlap(String a, String b) {
    int max = Math.min(a.length(), b.length());
    for (int k = max; k > 0; k--) if (a.endsWith(b.substring(0, k))) return k;
    return 0;
}
```



**Complexity** — Time **O(n² · 2ⁿ)**; Space **O(n · 2ⁿ)**.

## Related problems

- [Shortest Path Visiting All Nodes](/problems/shortest-path-visiting-all-nodes) — bitmask BFS
- [Traveling Salesman] — same TSP DP
