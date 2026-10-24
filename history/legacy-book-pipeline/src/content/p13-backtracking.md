## The Pattern

Backtracking is disciplined DFS over a decision tree: **choose → explore → un-choose**. Each stack frame owns one partial candidate, extends it with one legal choice, and restores state before trying the next sibling. The power is not recursion itself; it is expressing the search space so invalid branches are cut before they expand.

!!! pattern "Recognition signals"
    You need all feasible configurations, one valid configuration, or an optimum over combinatorial choices; constraints are local enough to reject a partial state early; the input size is small because the worst case is exponential.

```diagram
{"type":"recursion","nodes":[{"id":"root","label":"[]","x":3,"y":0,"role":"primary"},{"id":"a","label":"[1]","x":1,"y":1,"role":"panel"},{"id":"b","label":"[2]","x":3,"y":1,"role":"panel"},{"id":"c","label":"[3]","x":5,"y":1,"role":"panel"},{"id":"a1","label":"[1,1]","x":0,"y":2,"role":"red"},{"id":"a2","label":"[1,2]","x":2,"y":2,"role":"green"},{"id":"b1","label":"[2,1]","x":3,"y":2,"role":"red"},{"id":"c1","label":"[3,1]","x":5,"y":2,"role":"red"}],"edges":[{"from":"root","to":"a","label":"choose 1","color":"primary","dash":false},{"from":"root","to":"b","label":"choose 2","color":"primary","dash":false},{"from":"root","to":"c","label":"choose 3","color":"primary","dash":false},{"from":"a","to":"a1","label":"prune","color":"red","dash":true},{"from":"a","to":"a2","label":"accept","color":"green","dash":false},{"from":"b","to":"b1","label":"prune","color":"red","dash":true},{"from":"c","to":"c1","label":"prune","color":"red","dash":true}]}
```

## The Invariant

At entry to `dfs(state)`, `state` is a valid partial solution and all mutable bookkeeping exactly matches it. At exit, every extension under that prefix has been considered, and the caller's state has been restored byte-for-byte. Pruning is safe only when no completion of the current prefix can satisfy the problem.

## Template

```java
void dfs(int start, List<Integer> path, List<List<Integer>> ans, int[] nums) {
    if (isSolution(path)) {
        ans.add(new ArrayList<>(path));
        return;
    }

    for (int i = start; i < nums.length; i++) {
        if (!isCandidateAllowed(i, path, nums)) continue;

        path.add(nums[i]);          // choose
        dfs(nextStart(i), path, ans, nums); // explore
        path.remove(path.size() - 1);       // un-choose
    }
}
```

For grids, "state" usually includes `(r, c)` plus a visited mark; for permutations, it is `used[]`; for constraint boards, it is compact sets such as occupied columns and diagonals.

## Worked Recognition

- **Combination Sum (Module 6)**: decisions are "take candidate `i` again or move forward." The invariant is `remaining >= 0`; prune when `remaining < 0`, accept at `remaining == 0`.
- **N-Queens (Module 6)**: one row per depth, one column choice per row. Column and diagonal sets make `isCandidateAllowed` O(1), turning board validation from repeated scans into state maintenance.
- **Word Search and Permutations II (Module 6)**: both are DFS with reversible state. Word Search mutates/marks cells and restores them; Permutations II sorts first and skips equal unused siblings so duplicate leaves are never generated.

## Complexity

!!! complexity "Complexity"
    **T:** O(branching^depth) in the raw tree, reduced by pruning and duplicate skipping but still exponential in the worst case. **S:** O(depth) auxiliary stack/state, plus output size. Be explicit whether output storage is counted.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Forgetting to unmark state on every path, copying the path too late, pruning on a condition that excludes valid completions, or using global mutable collections whose contents leak across sibling branches.

## When NOT to use it

Do not backtrack when the problem has optimal substructure and overlapping subproblems better handled by DP, when a greedy invariant proves one pass is enough, or when `n` is large and the search space cannot be aggressively pruned.
