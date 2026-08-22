# Backtracking — Letter Case Permutation

*[↗ LeetCode: Letter Case Permutation](https://leetcode.com/problems/letter-case-permutation/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

Given a string, return every case variant of its letters (digits stay).

---

## Approach 1 — DFS with two branches per letter
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
        a[i] ^= 32;                 // flip case
        dfs(a, i + 1, out);
        a[i] ^= 32;
    }
}
```

**Complexity** — Time **O(n · 2^L)** where L = number of letters; Space **O(n)**.

---

## Approach 2 — Iterative bit-enumeration
Count L = number of letters. For mask 0..2^L - 1, apply the corresponding case flips. Same output.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| DFS with two branches per letter | O(n · 2^L) | O(n) | baseline |
| Iterative bit-enumeration | — | — | optimum |

## When to use which

- **State it for signal** → DFS with two branches per letter (O(n · 2^L)). Correct baseline; call it out then move on.
- **Ship this** → Iterative bit-enumeration (—, —). Expected optimum in interview.

## Related problems

- [Subsets](/problems/bit-manip-subsets) — same 2ⁿ enumeration
- [Permutations](/problems/permutations)
