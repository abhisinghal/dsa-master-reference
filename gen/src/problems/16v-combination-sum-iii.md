# Backtracking — Combination Sum III

*[↗ LeetCode: Combination Sum III](https://leetcode.com/problems/combination-sum-iii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Meta, Amazon, Google" />

`k` distinct digits from 1..9 summing to `n`.

**Example 1** — `k=3, n=7` → `[[1,2,4]]`
**Example 2** — `k=3, n=9` → `[[1,2,6],[1,3,5],[2,3,4]]`

**Constraints** — `2 ≤ k ≤ 9`; `1 ≤ n ≤ 60`.


<Hints
  hint1="You’re exploring a decision tree. What’s the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

<MarkSolved problem-slug="combination-sum-iii" />

<InterviewTimer problem-slug="combination-sum-iii" />



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

## Try it yourself

<JavaRunner problem-slug="combination-sum-iii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Backtracking | **O(C(9,k)·k)** | O(k) | canonical |

## When to use which

- **Small fixed alphabet + fixed k** → backtracking with pruning.
- **Larger alphabet** → same skeleton.
- **Count only** → replace `add(path)` with `count++`.

<AiCompanion problem-slug="combination-sum-iii" pattern-hint="backtracking" />

## Related problems

- [Combination Sum](https://leetcode.com/problems/combination-sum/)
- [Combination Sum II](/problems/combination-sum-ii)
- [Combination Sum IV](/problems/combination-sum-iv)

<FeedbackWidget problem-slug="combination-sum-iii" />

<RelatedProblems problems="subsets-ii::Subsets II|beautiful-arrangement::Beautiful Arrangement|sudoku-solver::Sudoku Solver" />
