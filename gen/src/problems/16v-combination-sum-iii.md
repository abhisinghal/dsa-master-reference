# Backtracking — Combination Sum III

*[↗ LeetCode: Combination Sum III](https://leetcode.com/problems/combination-sum-iii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Meta, Amazon, Google" />

`k` distinct digits from 1..9 summing to `n`.

**Example 1** — `k=3, n=7` → `[[1,2,4]]`
**Example 2** — `k=3, n=9` → `[[1,2,6],[1,3,5],[2,3,4]]`
**Example 3** — `k=4, n=1` → `[]` (need k=4 distinct digits >= 1+2+3+4 = 10, so no way to sum to 1)

**Constraints** — `2 ≤ k ≤ 9`; `1 ≤ n ≤ 60`. Brute enumerate all `C(9, k)` subsets is at most `C(9, 4) = 126`. Backtracking with pruning is asymptotically the same but much faster in practice — dead-ends cut early. Brute enumerates C(9, k) subsets and checks sum — trivial (C(9,4)=126) but scales badly if we generalise. Backtracking with early-terminate on sum > target is O(2⁹) = 512 leaves, ~10⁶ ops for related enumerations.
<Hints
  hint1="You're exploring a decision tree. What's the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

<MarkSolved problem-slug="combination-sum-iii" /> <Bookmark problem-slug="combination-sum-iii" />

<InterviewTimer problem-slug="combination-sum-iii" />



## Approach 1 — Brute enumerate all `C(9, k)` combinations

**Intuition.** For each of the C(9, k) choices of k distinct digits, sum them; if equal to n, add.

```java
List<List<Integer>> combinationSum3Brute(int k, int n) {
    List<List<Integer>> out = new ArrayList<>();
    for (int mask = 0; mask < (1 << 9); mask++) {
        if (Integer.bitCount(mask) != k) continue;
        int sum = 0;
        List<Integer> combo = new ArrayList<>();
        for (int i = 0; i < 9; i++)
            if ((mask & (1 << i)) != 0) { combo.add(i + 1); sum += i + 1; }
        if (sum == n) out.add(combo);
    }
    return out;
}
```

**Complexity** — Time **O(2⁹ · 9)** = 4608 ops; Space **O(k · #combos)**. Perfectly fine for this tiny domain. *In an interview* say "for the small fixed alphabet, brute is O(1) constant. Backtracking with pruning is faster in practice because dead-ends are cut early."

---

## Approach 2 — Backtracking with pruning (canonical)

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

**Complexity** — Time **O(C(9, k) · k)**; Space **O(k)**. *Say aloud in an interview:* "backtracking with early-termination prunes on `sum > n` and `remaining_slots < needed`. Same skeleton as Combination Sum, N-Queens, Subsets."

---

## Try it yourself

<JavaRunner problem-slug="combination-sum-iii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Enumerate all masks | O(2⁹ · 9) | O(k · #combos) | Baseline for fixed alphabet |
| **Backtracking** | **O(C(9,k)·k)** | O(k) | **Canonical** |

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
