# Backtracking — Combination Sum II

*[↗ LeetCode: Combination Sum II](https://leetcode.com/problems/combination-sum-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Meta, Amazon, Google" />

Combinations summing to target, each candidate used at most once; candidates may repeat.

**Example 1** — `candidates=[10,1,2,7,6,1,5], target=8` → `[[1,1,6],[1,2,5],[1,7],[2,6]]` (4 unique combos)
**Example 2** — `candidates=[2,5,2,1,2], target=5` → `[[1,2,2],[5]]`
**Example 3** — `candidates=[1,1,1], target=2` → `[[1,1]]`

**Constraints** — `1 ≤ n ≤ 100`; `1 ≤ target ≤ 30`.


<Hints
  hint1="You're exploring a decision tree. What's the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

<MarkSolved problem-slug="combination-sum-ii" /> <Bookmark problem-slug="combination-sum-ii" />

<InterviewTimer problem-slug="combination-sum-ii" />



## Approach 1 — Brute force (all subsets that sum + HashSet dedup)

**Intuition.** Enumerate every one of `2ⁿ` subsets. For each, check if its elements sum to `target`. Put each valid subset (sorted) in a `HashSet`.

```java
List<List<Integer>> combinationSum2Brute(int[] cand, int target) {
    Arrays.sort(cand);
    Set<List<Integer>> seen = new LinkedHashSet<>();
    int n = cand.length;
    for (int mask = 0; mask < (1 << n); mask++) {
        int sum = 0;
        List<Integer> combo = new ArrayList<>();
        for (int i = 0; i < n; i++)
            if ((mask & (1 << i)) != 0) { combo.add(cand[i]); sum += cand[i]; }
        if (sum == target) seen.add(combo);
    }
    return new ArrayList<>(seen);
}
```

**Complexity** — Time **O(n · 2ⁿ)**; Space **O(n · 2ⁿ)**. For `n=100`, `2¹⁰⁰ ≈ 10³⁰` — heat death of the universe. Even for `n=25` it's `3·10⁷` — sluggish. *In an interview* state it as the reference, then upgrade.

---

## Approach 2 — Sort + skip equal-at-same-depth + prune on sum (canonical)

**Insight.** Two prunes make this fast: (1) sort so we can break early when `cand[i] > remaining`; (2) skip duplicates at the same depth with `i > start && a[i] == a[i-1]`. Both cut the tree massively before recursion pays.

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

**Complexity** — Time exponential worst case but heavily pruned; Space **O(target)**. *Say aloud in an interview:* "the `a[i] <= rem` break is what makes this practical — without it, we'd recurse into every larger candidate for no reason."

---

## Try it yourself

<JavaRunner problem-slug="combination-sum-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute + HashSet dedup | O(n · 2ⁿ) | O(n · 2ⁿ) | Reference; dies at n>25 |
| **Sort + skip + prune** | **exponential (heavily pruned)** | O(target) | **Canonical** |

## When to use which

- **Duplicates in candidates, each used once** → sort + skip.
- **Reuse allowed** → [Combination Sum](https://leetcode.com/problems/combination-sum/).
- **Fixed k, digits 1-9** → [Combination Sum III](/problems/combination-sum-iii).

<AiCompanion problem-slug="combination-sum-ii" pattern-hint="backtracking" />

## Related problems

- [Combination Sum](https://leetcode.com/problems/combination-sum/)
- [Combination Sum III](/problems/combination-sum-iii)
- [Combination Sum IV](/problems/combination-sum-iv) — DP

<FeedbackWidget problem-slug="combination-sum-ii" />

<RelatedProblems problems="n-queens-ii::N Queens II|permutations-ii::Permutations II|subsets-ii::Subsets II" />
