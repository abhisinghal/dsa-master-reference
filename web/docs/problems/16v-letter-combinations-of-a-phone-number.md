# Backtracking — Letter Combinations of a Phone Number

*[↗ LeetCode: Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

Given digits 2-9, return all letter combinations.

## Approach — DFS enumeration



```java
List<String> letterCombinations(String digits) {
    List<String> out = new ArrayList<>();
    if (digits.isEmpty()) return out;
    String[] map = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
    dfs(digits, 0, map, new StringBuilder(), out);
    return out;
}
void dfs(String d, int i, String[] map, StringBuilder sb, List<String> out) {
    if (i == d.length()) { out.add(sb.toString()); return; }
    for (char c : map[d.charAt(i) - '0'].toCharArray()) {
        sb.append(c);
        dfs(d, i + 1, map, sb, out);
        sb.deleteCharAt(sb.length() - 1);
    }
}
```



**Complexity** — Time **O(4ⁿ · n)** worst case (digits 7, 9); Space **O(n)** recursion.

## Approach 2 — Iterative BFS

Repeatedly extend all combinations by the next digit's letters — same complexity, no recursion.

## Related problems

- [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) — same recursion shape with constraint
- [Palindrome Partitioning](/problems/palindrome-partitioning)
