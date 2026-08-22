# Backtracking — Palindrome Partitioning

*[↗ LeetCode: Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

All partitions of `s` where every part is a palindrome.

## Approach 1 — DFS + palindrome check on the fly

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

`pal[i][j]` = whether `s[i..j]` is palindrome — DP in O(n²) time / space. Then O(1) checks during recursion.

**Complexity** — Time exponential (~2ⁿ · n); Space **O(n²)** for DP + recursion depth.

## Related problems

- [Palindrome Partitioning II](/problems/palindrome-partitioning-ii) — min cuts, DP not backtracking
- [Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/) — same partition template
- [Word Break II](https://leetcode.com/problems/word-break-ii/)
