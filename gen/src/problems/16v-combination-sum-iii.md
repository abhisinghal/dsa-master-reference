# Backtracking — Combination Sum III

*[↗ LeetCode: Combination Sum III](https://leetcode.com/problems/combination-sum-iii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

`k` distinct digits from 1..9 summing to `n`.

---

## Approach 1 — Backtracking with pruning
**Prunes:** `path.size() == k`, `rem < 0`, `i > rem` (further digits too big).

```java
List<List<Integer>> combinationSum3(int k, int n) {
    List<List<Integer>> out = new ArrayList<>();
    dfs(1, k, n, new ArrayList<>(), out);
    return out;
}
void dfs(int start, int k, int rem, List<Integer> path, List<List<Integer>> out) {
    if (path.size() == k) { if (rem == 0) out.add(new ArrayList<>(path)); return; }
    for (int i = start; i <= 9 && i <= rem; i++) {
        path.add(i);
        dfs(i + 1, k, rem - i, path, out);
        path.remove(path.size() - 1);
    }
}
```

**Complexity** — Time **O(C(9, k) · k)**; Space **O(k)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Backtracking with pruning | O(C(9, k) · k) | O(k) | primary |

## When to use which

- **Ship this** → Backtracking with pruning (O(C(9, k) · k), O(k)). The pattern's standard solution.

## Related problems

- [Combination Sum](https://leetcode.com/problems/combination-sum/)
- [Combination Sum II](/problems/combination-sum-ii)
- [Combination Sum IV](/problems/combination-sum-iv) — **DP** (unbounded, order matters)
