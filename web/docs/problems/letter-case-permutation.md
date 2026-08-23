# Backtracking — Letter Case Permutation

*[↗ LeetCode: Letter Case Permutation](https://leetcode.com/problems/letter-case-permutation/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

Return every case variant of letters (digits stay).

**Example 1** — `s="a1b2"` → `["a1b2","a1B2","A1b2","A1B2"]`

**Constraints** — `1 ≤ n ≤ 12`.

---

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



## Approach 2 — Iterative bit-enumeration
Count L letters; for mask 0..2^L-1 flip corresponding cases.

**Complexity** — Time **O(n · 2^L)**; Space **O(n)** recursion.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DFS | O(n · 2^L) | O(n) | canonical |
| Bit enumeration | O(n · 2^L) | O(1) | iterative |

## When to use which

- **Small L** → either.
- **Case with constraints** → DFS + prune.

## Related problems

- [Subsets](/problems/bit-manip-subsets)
- [Permutations](/problems/permutations)
