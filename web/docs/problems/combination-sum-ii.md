# Backtracking — Combination Sum II

*[↗ LeetCode: Combination Sum II](https://leetcode.com/problems/combination-sum-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

&lt;CompanyTags companies="Meta, Amazon, Google" /&gt;

Combinations summing to target, each candidate used at most once; candidates may repeat.

**Example 1** — `candidates=[10,1,2,7,6,1,5], target=8` → 4 unique combos

**Constraints** — `1 ≤ n ≤ 100`.


&lt;Hints
  hint1="You’re exploring a decision tree. What’s the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/&gt;
---

&lt;MarkSolved problem-slug="combination-sum-ii" /&gt;


## Approach — Sort + skip equal-at-same-depth + prune on sum (canonical)



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
        if (i > start && a[i] == a[i-1]) continue;
        path.add(a[i]);
        dfs(a, i + 1, rem - a[i], path, out);
        path.remove(path.size() - 1);
    }
}
```



**Complexity** — Time exponential; heavily pruned.

---

## Try it yourself

<JavaRunner problem-slug="combination-sum-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort + skip + prune | **exponential** | O(target) | canonical |

## When to use which

- **Duplicates in candidates, each used once** → sort + skip.
- **Reuse allowed** → [Combination Sum](https://leetcode.com/problems/combination-sum/).
- **Fixed k, digits 1-9** → [Combination Sum III](/problems/combination-sum-iii).

&lt;AiCompanion problem-slug="combination-sum-ii" pattern-hint="backtracking" /&gt;

## Related problems

- [Combination Sum](https://leetcode.com/problems/combination-sum/)
- [Combination Sum III](/problems/combination-sum-iii)
- [Combination Sum IV](/problems/combination-sum-iv) — DP

&lt;FeedbackWidget problem-slug="combination-sum-ii" /&gt;

&lt;RelatedProblems problems="n-queens-ii::N Queens II|permutations-ii::Permutations II|subsets-ii::Subsets II" /&gt;
