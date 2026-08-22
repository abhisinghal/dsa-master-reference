# Backtracking — Permutations

*[↗ LeetCode: Permutations](https://leetcode.com/problems/permutations/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

Return all permutations of distinct integers.

**Example 1** — `nums=[1,2,3]` → 6 permutations
**Example 2** — `nums=[1]` → `[[1]]`

**Constraints** — `1 ≤ n ≤ 6`.

---

## Approach 1 — Insert-at-every-position recursion

Build permutations of length k+1 by inserting the (k+1)-th element into every position of length-k perms.

## Approach 2 — Swap-in-place (canonical)

**Insight.** At depth `k`, swap each remaining candidate into position `k`, recurse, swap back.

```java
List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> out = new ArrayList<>();
    dfs(nums, 0, out);
    return out;
}
void dfs(int[] a, int k, List<List<Integer>> out) {
    if (k == a.length) {
        List<Integer> p = new ArrayList<>();
        for (int x : a) p.add(x);
        out.add(p); return;
    }
    for (int i = k; i < a.length; i++) {
        swap(a, k, i);
        dfs(a, k + 1, out);
        swap(a, k, i);
    }
}
void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }
```

**Complexity** — Time **O(n · n!)**; Space **O(n)**.

## Approach 3 — Used-set + build (extensible to duplicates)

Cleaner when duplicates exist — see [Permutations II](/problems/permutations-ii).

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Insert-at-position | O(n · n!) | O(n · n!) | works |
| Swap-in-place | **O(n · n!)** | O(n) | canonical |
| Used set | O(n · n!) | O(n) | dup-friendly |

## When to use which

- **Standard interview** → swap-in-place.
- **Duplicates** → used-set variant.
- **Kth permutation** → factorial-number system, no enumeration.

## Related problems

- [Permutations II](/problems/permutations-ii)
- [Next Permutation](/problems/next-permutation)
- [Letter Case Permutation](/problems/letter-case-permutation)
