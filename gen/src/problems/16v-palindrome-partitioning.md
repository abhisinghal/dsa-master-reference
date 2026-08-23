# Backtracking — Palindrome Partitioning

*[↗ LeetCode: Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Meta, Amazon, Google, Bloomberg" />

All partitions of `s` where every part is a palindrome.

**Example 1** — `s="aab"` → `[["a","a","b"],["aa","b"]]`
**Example 2** — `s="a"` → `[["a"]]`

**Constraints** — `1 ≤ n ≤ 16`.


<Hints
  hint1="You’re exploring a decision tree. What’s the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

<MarkSolved problem-slug="palindrome-partitioning" />


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

<CodeTrace
  title="DFS + palindrome check on the fly (canonical)"
  :values="['a', 'a', 'b']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

## Approach 2 — Precompute `pal[i][j]` DP
O(n²) precompute; O(1) checks during recursion.

**Complexity** — Time exponential (~2ⁿ · n); Space **O(n²)** with DP.

---

## Try it yourself

<JavaRunner problem-slug="palindrome-partitioning" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DFS + check | exponential | O(n) | canonical |
| DFS + pal DP | exponential | O(n²) | faster |

## When to use which

- **Partition into palindromes** → DFS + check.
- **Min cuts** → different problem (see [II](/problems/palindrome-partitioning-ii)).
- **Count partitions** → same skeleton; replace add with count.

<AiCompanion problem-slug="palindrome-partitioning" pattern-hint="backtracking" />

## Related problems

- [Palindrome Partitioning II](/problems/palindrome-partitioning-ii)
- [Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses/)
- [Word Break II](https://leetcode.com/problems/word-break-ii/)

<FeedbackWidget problem-slug="palindrome-partitioning" />

<RelatedProblems problems="n-queens-ii::N Queens II|sudoku-solver::Sudoku Solver|combination-sum-iii::Combination Sum III" />
