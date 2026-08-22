# Backtracking — Combination Sum II

*[↗ LeetCode: Combination Sum II](https://leetcode.com/problems/combination-sum-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

Combinations summing to target, each candidate used at most **once**, candidates may repeat.

---

## Approach 1 — Sort + skip equal-at-same-depth + prune on sum
**Insight.** Sort → deduplicate at each recursion level with `if (i > start && cand[i] == cand[i-1]) continue`. Prune when `cand[i] > remaining`.

```java
List<List<Integer>> combinationSum2(int[] cand, int target) {
    Arrays.sort(cand);
    List<List<Integer>> out = new ArrayList<>();
    dfs(cand, 0, target, new ArrayList<>(), out);
    return out;
}
void dfs(int[] a, int start, int rem, List<Integer> path, List<List<Integer>> out) {
    if (rem == 0) { out.add(new ArrayList<>(path)); return; }
    for (int i = start; i < a.length && a[i] <= rem; i++) {
        if (i > start && a[i] == a[i - 1]) continue;
        path.add(a[i]);
        dfs(a, i + 1, rem - a[i], path, out);
        path.remove(path.size() - 1);
    }
}
```

**Complexity** — Time exponential; heavily pruned.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort + skip equal-at-same-depth + prune on… | — | — | primary |

## When to use which

- **Ship this** → Sort + skip equal-at-same-depth + prune on sum (—, —). The pattern's standard solution.

## Related problems

- [Combination Sum](https://leetcode.com/problems/combination-sum/) — reuse allowed
- [Combination Sum III](/problems/combination-sum-iii) — fixed k, digits 1..9
