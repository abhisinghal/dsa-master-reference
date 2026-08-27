# Backtracking — Permutations II

*[↗ LeetCode: Permutations II](https://leetcode.com/problems/permutations-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Meta, Amazon, Google, Microsoft" />

All **unique** permutations of nums (may contain duplicates).

**Example 1** — `nums=[1,1,2]` → `[[1,1,2],[1,2,1],[2,1,1]]` (3 unique perms)
**Example 2** — `nums=[1,2,3]` → 6 permutations (all distinct)
**Example 3** — `nums=[2,2,2]` → `[[2,2,2]]` (only 1 unique)

**Constraints** — `1 ≤ n ≤ 8`.


<Hints
  hint1="You're exploring a decision tree. What's the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

<MarkSolved problem-slug="permutations-ii" /> <Bookmark problem-slug="permutations-ii" />

<InterviewTimer problem-slug="permutations-ii" />



## Approach 1 — Brute force (all perms + HashSet dedup)

**Intuition.** Generate every one of the n! permutations. Deduplicate by putting each into a `HashSet<List<Integer>>`.



```java
List<List<Integer>> permuteUniqueBrute(int[] nums) {
    Set<List<Integer>> seen = new LinkedHashSet<>();
    boolean[] used = new boolean[nums.length];
    dfsBrute(nums, used, new ArrayList<>(), seen);
    return new ArrayList<>(seen);
}
void dfsBrute(int[] a, boolean[] used, List<Integer> path, Set<List<Integer>> seen) {
    if (path.size() == a.length) { seen.add(new ArrayList<>(path)); return; }
    for (int i = 0; i < a.length; i++) {
        if (used[i]) continue;
        used[i] = true; path.add(a[i]);
        dfsBrute(a, used, path, seen);
        path.remove(path.size() - 1); used[i] = false;
    }
}
```



**Complexity** — Time **O(n · n!)** for the generation + **O(n)** per hash insertion; Space **O(n · n!)** for the set. For `n=8` that's ~40,320 perms — still fine but generates all duplicates only to throw them away. *In an interview* state this as the reference then move on.

---

## Approach 2 — Sort + used[] + skip equal-and-unused (canonical)

**Insight.** The brute force wastes work generating duplicates. If we sort first and enforce a canonical order among identical values, every duplicate branch is pruned *at generation time* — never emitted.

**Rule.** Skip `nums[i]` iff `nums[i] == nums[i-1] AND !used[i-1]`. Reading in English: *"if the previous duplicate hasn't been used at this level, this duplicate must not be used first."* That forces every group of identical values to be picked in a fixed left-to-right order.



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



**Complexity** — Time **O(n · n!)** worst but with strict pruning; Space **O(n)**. *Say aloud in an interview:* "sort turns 'anywhere in the array is fine' into a canonical order — the `!used[i-1]` guard is the entire dedup mechanism."

---

## Try it yourself

<JavaRunner problem-slug="permutations-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute + HashSet dedup | O(n · n!) | O(n · n!) | Baseline reference |
| **Sort + used-mask dedup** | **O(n · n!)** | O(n) | **Canonical** |

## When to use which

- **Duplicates** → sort + skip.
- **Distinct** → simpler swap-in-place.
- **Return count only** → multinomial `n! / Π(k_i!)`.

<AiCompanion problem-slug="permutations-ii" pattern-hint="backtracking" />

## Related problems

- [Permutations](/problems/permutations)
- [Subsets II](/problems/subsets-ii)
- [Combination Sum II](/problems/combination-sum-ii)

<FeedbackWidget problem-slug="permutations-ii" />

<RelatedProblems problems="letter-combinations-of-a-phone-number::Letter Combinations Of A Phone Number|combination-sum-iv::Combination Sum IV|n-queens::N Queens" />
