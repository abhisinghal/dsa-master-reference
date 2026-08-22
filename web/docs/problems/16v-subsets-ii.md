# Backtracking — Subsets II

*[↗ LeetCode: Subsets II](https://leetcode.com/problems/subsets-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

All **unique** subsets when nums may contain duplicates.

## Approach — Sort + skip equal after including

**Insight.** Sort. Standard subset backtracking, but skip duplicates in the outer loop: `if (i > start && nums[i] == nums[i-1]) continue;`. Ensures each duplicate group contributes once per "count of picks".



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
        if (i > start && a[i] == a[i - 1]) continue;
        path.add(a[i]);
        dfs(a, i + 1, path, out);
        path.remove(path.size() - 1);
    }
}
```



**Complexity** — Time **O(n · 2ⁿ)**; Space **O(n)**.

## Related problems

- [Subsets](/problems/bit-manip-subsets)
- [Combination Sum II](/problems/combination-sum-ii)
- [Permutations II](/problems/permutations-ii)
