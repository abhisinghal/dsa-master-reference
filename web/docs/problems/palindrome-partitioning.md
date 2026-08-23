# Backtracking — Palindrome Partitioning

*[↗ LeetCode: Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

All partitions of `s` where every part is a palindrome.

**Example 1** — `s="aab"` → `[["a","a","b"],["aa","b"]]`
**Example 2** — `s="a"` → `[["a"]]`

**Constraints** — `1 ≤ n ≤ 16`.

---

## Approach 1 — DFS + palindrome check on the fly (canonical)



```java
List<List<String>> partition(String s) {
    List<List<String>> out = new ArrayList<>();
    dfs(s, 0, new ArrayList<>(), out);
    return out;
}
void dfs(String s, int start, List<String> path, List<List<String>> out) {
    if (start == s.length()) { out.add(new ArrayList<>(path)); return; }
    for (int end = start + 1; end <= s.length(); end++) {
        if (isPali(s, start, end - 1)) {
            path.add(s.substring(start, end));
            dfs(s, end, path, out);
            path.remove(path.size() - 1);
        }
    }
}
boolean isPali(String s, int l, int r) {
    while (l < r) if (s.charAt(l++) != s.charAt(r--)) return false;
    return true;
}
```



## Approach 2 — Precompute `pal[i][j]` DP
O(n²) precompute; O(1) checks during recursion.

**Complexity** — Time exponential (~2ⁿ · n); Space **O(n²)** with DP.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DFS + check | exponential | O(n) | canonical |
| DFS + pal DP | exponential | O(n²) | faster |

## When to use which

- **Partition into palindromes** → DFS + check.
- **Min cuts** → different problem (see [II](/problems/palindrome-partitioning-ii)).
- **Count partitions** → same skeleton; replace add with count.

## Related problems

- [Palindrome Partitioning II](/problems/palindrome-partitioning-ii)
- [Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/)
- [Word Break II](https://leetcode.com/problems/word-break-ii/)
