# Backtracking — Letter Combinations of a Phone Number

*[↗ LeetCode: Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Uber, Bloomberg" />

Given digits 2-9, return all letter combinations.

**Example 1** — `digits="23"` → `["ad","ae","af","bd","be","bf","cd","ce","cf"]`
**Example 2** — `digits=""` → `[]`

**Constraints** — `0 ≤ len ≤ 4`.


<Hints
  hint1="You’re exploring a decision tree. What’s the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

<MarkSolved problem-slug="letter-combinations-of-a-phone-number" /> <Bookmark problem-slug="letter-combinations-of-a-phone-number" />

<InterviewTimer problem-slug="letter-combinations-of-a-phone-number" />



## Approach 1 — DFS enumeration (canonical)

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

<CodeTrace
  title="DFS enumeration (canonical)"
  :values="['2', '3']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

## Approach 2 — Iterative BFS
Extend all combinations by next digit's letters; same complexity, no recursion.

**Complexity** — Time **O(4ⁿ · n)** worst; Space **O(n)** recursion.

---

## Try it yourself

<JavaRunner problem-slug="letter-combinations-of-a-phone-number" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DFS | O(4ⁿ · n) | O(n) | canonical |
| BFS | O(4ⁿ · n) | O(4ⁿ) | iterative |

## When to use which

- **Small n** → either.
- **Very deep** → BFS to avoid stack.
- **First combination only** → early return in DFS.

<AiCompanion problem-slug="letter-combinations-of-a-phone-number" pattern-hint="backtracking" />

## Related problems

- [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/)
- [Palindrome Partitioning](/problems/palindrome-partitioning)

<FeedbackWidget problem-slug="letter-combinations-of-a-phone-number" />

<RelatedProblems problems="permutations::Permutations|palindrome-partitioning::Palindrome Partitioning|n-queens-ii::N Queens II" />
