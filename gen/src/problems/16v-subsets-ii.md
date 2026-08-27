# Backtracking — Subsets II

*[↗ LeetCode: Subsets II](https://leetcode.com/problems/subsets-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Meta, Amazon, Google, Bloomberg" />

All **unique** subsets when nums may contain duplicates.

**Example 1** — `nums=[1,2,2]` → `[[],[1],[1,2],[1,2,2],[2],[2,2]]`
**Example 2** — `nums=[0]` → `[[],[0]]`
**Example 3** — `nums=[4,4,4,1,4]` → 10 unique subsets (naive gives 32, of which 22 are duplicates)

**Constraints** — `1 ≤ n ≤ 10`. Brute enumerates 2ⁿ subsets and dedups — at n=10 with duplicates that's 10³ subsets each hashed. Sort + skip-duplicates in backtrack yields exactly distinct subsets in one pass — 10⁶ ops even for max input.
<Hints
  hint1="You're exploring a decision tree. What's the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

<MarkSolved problem-slug="subsets-ii" /> <Bookmark problem-slug="subsets-ii" />

<InterviewTimer problem-slug="subsets-ii" />



## Approach 1 — Brute force (all 2ⁿ subsets + HashSet dedup)

**Intuition.** Enumerate all 2ⁿ subsets via bitmask. Sort each and put it in a `HashSet<List<Integer>>` to dedupe.

```java
List<List<Integer>> subsetsWithDupBrute(int[] nums) {
    Arrays.sort(nums);
    Set<List<Integer>> seen = new LinkedHashSet<>();
    int n = nums.length;
    for (int mask = 0; mask < (1 << n); mask++) {
        List<Integer> sub = new ArrayList<>();
        for (int i = 0; i < n; i++)
            if ((mask & (1 << i)) != 0) sub.add(nums[i]);
        seen.add(sub);
    }
    return new ArrayList<>(seen);
}
```

**Complexity** — Time **O(n · 2ⁿ)** for enumeration + O(n) per HashSet insert; Space **O(n · 2ⁿ)**. For `n=10` that's ~10,240 candidates — fine, but generates 22 duplicates on `[4,4,4,1,4]` for every 10 uniques. *In an interview* state it, then upgrade.

---

## Approach 2 — Sort + skip equal-at-same-depth (canonical)

**Insight.** The brute force generates every ordering of every subset and dedupes at the end. If we sort first and prune duplicates at generation time, no duplicate is ever emitted.

**Rule.** In the outer loop `for i = start..n-1`: `if (i > start && nums[i] == nums[i-1]) continue`. This skips the duplicate group's second and later members at each depth level, so each duplicate group contributes to at most one subset per count.

```java
List<List<Integer>> subsetsWithDup(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> out = new ArrayList<>();
    dfs(nums, 0, new ArrayList<>(), out);
    return out;
}
void dfs(int[] a, int start, List<Integer> path, List<List<Integer>> out) {
    out.add(new ArrayList<>(path));
    for (int i = start; i < a.length; i++) {
        if (i > start && a[i] == a[i-1]) continue;
        path.add(a[i]);
        dfs(a, i + 1, path, out);
        path.remove(path.size() - 1);
    }
}
```

<CodeTrace
  title="Sort + skip equal-at-same-depth (canonical)"
  :values="['1', '2', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n · 2ⁿ)**; Space **O(n)**. *Say aloud in an interview:* "the `i > start` check — not `i > 0` — is the entire dedup mechanism. It skips duplicates at *this level* but still allows them at deeper levels."

---

## Try it yourself

<JavaRunner problem-slug="subsets-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute + HashSet dedup | O(n · 2ⁿ) | O(n · 2ⁿ) | Baseline reference |
| **Sort + skip** | **O(n · 2ⁿ)** | O(n) | **Canonical** |

## When to use which

- **Duplicates** → sort + skip.
- **Distinct** → simpler subsets bitmask.
- **Fixed size k** → cut early when `path.size() == k`.

<AiCompanion problem-slug="subsets-ii" pattern-hint="backtracking" />

## Related problems

- [Subsets](/problems/bit-manip-subsets)
- [Combination Sum II](/problems/combination-sum-ii)
- [Permutations II](/problems/permutations-ii)

<FeedbackWidget problem-slug="subsets-ii" />

<RelatedProblems problems="letter-combinations-of-a-phone-number::Letter Combinations Of A Phone Number|n-queens-ii::N Queens II|combination-sum-iii::Combination Sum III" />
