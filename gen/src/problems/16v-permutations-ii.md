# Backtracking — Permutations II

*[↗ LeetCode: Permutations II](https://leetcode.com/problems/permutations-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

All **unique** permutations of nums (may contain duplicates).

## Approach — Sort + `used[]` + skip equal-and-unused

**Insight.** Sort. When picking the next element, skip any `nums[i]` such that `nums[i] == nums[i-1]` AND `!used[i-1]` — this enforces a canonical order among duplicates.

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
        if (i > 0 && a[i] == a[i - 1] && !used[i - 1]) continue;
        used[i] = true;
        path.add(a[i]);
        dfs(a, used, path, out);
        path.remove(path.size() - 1);
        used[i] = false;
    }
}
```

**Why `!used[i-1]`.** Enforces that among duplicates, we pick "left-to-right" order — if the previous duplicate is unused, skipping now avoids a mirror choice already explored.

**Complexity** — Time **O(n · n!)** worst case; Space **O(n)**.

## Related problems

- [Permutations](/problems/permutations) — no duplicates
- [Subsets II](/problems/subsets-ii) — same dedup idea for subsets
