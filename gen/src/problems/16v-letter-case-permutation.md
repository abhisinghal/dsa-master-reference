# Backtracking — Letter Case Permutation

*[↗ LeetCode: Letter Case Permutation](https://leetcode.com/problems/letter-case-permutation/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Meta, Amazon, Google" />

Return every case variant of letters (digits stay).

**Example 1** — `s="a1b2"` → `["a1b2","a1B2","A1b2","A1B2"]`
**Example 2** — `s="3z4"` → `["3z4","3Z4"]`
**Example 3** — `s="12345"` → `["12345"]` (no letters — one variant)

**Constraints** — `1 ≤ n ≤ 12`. That constraint gives `2¹² = 4096` upper bound on output size — trivially fast.


<Hints
  hint1="You're exploring a decision tree. What's the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

<MarkSolved problem-slug="letter-case-permutation" /> <Bookmark problem-slug="letter-case-permutation" />

<InterviewTimer problem-slug="letter-case-permutation" />



## Approach 1 — DFS with two branches per letter (canonical)

```java
List<String> letterCasePermutation(String s) {
    List<String> out = new ArrayList<>();
    dfs(s.toCharArray(), 0, out);
    return out;
}
void dfs(char[] a, int i, List<String> out) {
    if (i == a.length) { out.add(new String(a)); return; }
    dfs(a, i + 1, out);
    if (Character.isLetter(a[i])) {
        a[i] ^= 32;
        dfs(a, i + 1, out);
        a[i] ^= 32;
    }
}
```

<CodeTrace
  title="DFS with two branches per letter (canonical)"
  :values="['a', '1', 'b', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

## Approach 2 — Iterative bit-enumeration
Count L letters; for mask 0..2^L-1 flip corresponding cases.

**Complexity** — Time **O(n · 2^L)**; Space **O(n)** recursion.

---

## Try it yourself

<JavaRunner problem-slug="letter-case-permutation" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DFS | O(n · 2^L) | O(n) | canonical |
| Bit enumeration | O(n · 2^L) | O(1) | iterative |

## When to use which

- **Small L** → either.
- **Case with constraints** → DFS + prune.

<AiCompanion problem-slug="letter-case-permutation" pattern-hint="backtracking" />

## Related problems

- [Subsets](/problems/bit-manip-subsets)
- [Permutations](/problems/permutations)

<FeedbackWidget problem-slug="letter-case-permutation" />
