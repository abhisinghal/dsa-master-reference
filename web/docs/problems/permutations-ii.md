# Backtracking — Permutations II

*[↗ LeetCode: Permutations II](https://leetcode.com/problems/permutations-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft" /&gt;

All **unique** permutations of nums (may contain duplicates).

**Example 1** — `nums=[1,1,2]` → 3 unique perms

**Constraints** — `1 ≤ n ≤ 8`.


&lt;Hints
  hint1="You’re exploring a decision tree. What’s the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/&gt;
---

## Approach — Sort + used[] + skip equal-and-unused (canonical)

**Insight.** Sort. Skip `nums[i]` iff `nums[i] == nums[i-1] AND !used[i-1]` — enforces canonical order among duplicates.



```java
List<List<Integer>> permuteUnique(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> out = new ArrayList<>();
    boolean[] used = new boolean[nums.length];
    dfs(nums, used, new ArrayList<>(), out);
    return out;
}
void dfs(int[] a, boolean[] used, List<Integer> path, List<List<Integer>> out) {
    if (path.size() == a.length) { out.add(new ArrayList<>(path)); return; }
    for (int i = 0; i < a.length; i++) {
        if (used[i]) continue;
        if (i > 0 && a[i] == a[i-1] && !used[i-1]) continue;
        used[i] = true;
        path.add(a[i]);
        dfs(a, used, path, out);
        path.remove(path.size() - 1);
        used[i] = false;
    }
}
```



**Complexity** — Time **O(n · n!)** worst; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="permutations-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort + used-mask dedup | **O(n · n!)** | O(n) | canonical |

## When to use which

- **Duplicates** → sort + skip.
- **Distinct** → simpler swap-in-place.
- **Return count only** → multinomial `n! / Π(k_i!)`.

&lt;AiCompanion problem-slug="permutations-ii" pattern-hint="backtracking" /&gt;

## Related problems

- [Permutations](/problems/permutations)
- [Subsets II](/problems/subsets-ii)
- [Combination Sum II](/problems/combination-sum-ii)

&lt;FeedbackWidget problem-slug="permutations-ii" /&gt;
