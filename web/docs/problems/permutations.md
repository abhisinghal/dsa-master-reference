# Backtracking — Permutations

*[↗ LeetCode: Permutations](https://leetcode.com/problems/permutations/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

Return all permutations of distinct integers.

---

## Approach 1 — Insert into every position
Recursively insert `nums[i]` into every position of every partial permutation of `nums[0..i-1]`. O(n! · n).

---

## Approach 2 — Swap-in-place
**Insight.** At depth `k`, swap each remaining candidate into position `k`, recurse, swap back.



```java
List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> out = new ArrayList<>();
    dfs(nums, 0, out);
    return out;
}
void dfs(int[] a, int k, List<List<Integer>> out) {
    if (k == a.length) {
        List<Integer> perm = new ArrayList<>();
        for (int x : a) perm.add(x);
        out.add(perm);
        return;
    }
    for (int i = k; i < a.length; i++) {
        swap(a, k, i);
        dfs(a, k + 1, out);
        swap(a, k, i);
    }
}
void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }
```



**Complexity** — Time **O(n · n!)**; Space **O(n)** recursion.

---

## Approach 3 — Used-set + build
Cleaner when duplicates exist (see Permutations II).

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Insert into every position | O(n! · n) | — | baseline |
| Swap-in-place | O(n · n!) | O(n) | improved |
| Used-set + build | — | — | optimum |

## When to use which

- **State it for signal** → Insert into every position (O(n! · n)). Correct baseline; call it out then move on.
- **Intermediate refinement** → Swap-in-place (O(n · n!)).
- **Ship this** → Used-set + build (—, —). Expected optimum in interview.

## Related problems

- [Permutations II](/problems/permutations-ii) — duplicate handling
- [Next Permutation](/problems/next-permutation)
- [Letter Case Permutation](/problems/letter-case-permutation)
