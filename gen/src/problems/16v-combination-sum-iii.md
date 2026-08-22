# Backtracking — Combination Sum III

*[↗ LeetCode: Combination Sum III](https://leetcode.com/problems/combination-sum-iii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

`k` distinct digits from 1..9 summing to `n`.

**Example 1** — `k=3, n=7` → `[[1,2,4]]`
**Example 2** — `k=3, n=9` → `[[1,2,6],[1,3,5],[2,3,4]]`

**Constraints** — `2 ≤ k ≤ 9`; `1 ≤ n ≤ 60`.

---

## Approach — Backtracking with pruning (canonical)

**Prunes:** `path.size() == k`, `rem < 0`, `i > rem`.

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

| Approach | Time | Space | Grade |
|---|---|---|---|
| Backtracking | **O(C(9,k)·k)** | O(k) | canonical |

## When to use which

- **Small fixed alphabet + fixed k** → backtracking with pruning.
- **Larger alphabet** → same skeleton.
- **Count only** → replace `add(path)` with `count++`.

## Related problems

- [Combination Sum](https://leetcode.com/problems/combination-sum/)
- [Combination Sum II](/problems/combination-sum-ii)
- [Combination Sum IV](/problems/combination-sum-iv)
