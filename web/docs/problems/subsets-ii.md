# Backtracking — Subsets II

*[↗ LeetCode: Subsets II](https://leetcode.com/problems/subsets-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

All **unique** subsets when nums may contain duplicates.

**Example 1** — `nums=[1,2,2]` → `[[],[1],[1,2],[1,2,2],[2],[2,2]]`

**Constraints** — `1 ≤ n ≤ 10`.

---

## Approach — Sort + skip equal-at-same-depth (canonical)

**Insight.** Sort. Standard subset backtracking, but skip duplicates in the outer loop: `if (i > start && nums[i] == nums[i-1]) continue`. Ensures each duplicate group contributes once per count.



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

**Complexity** — Time **O(n · 2ⁿ)**; Space **O(n)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort + skip | **O(n · 2ⁿ)** | O(n) | canonical |

## When to use which

- **Duplicates** → sort + skip.
- **Distinct** → simpler subsets bitmask.
- **Fixed size k** → cut early when `path.size() == k`.

## Related problems

- [Subsets](/problems/bit-manip-subsets)
- [Combination Sum II](/problems/combination-sum-ii)
- [Permutations II](/problems/permutations-ii)
