# Backtracking — Permutations II

*[↗ LeetCode: Permutations II](https://leetcode.com/problems/permutations-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

All **unique** permutations of nums (may contain duplicates).

**Example 1** — `nums=[1,1,2]` → 3 unique perms

**Constraints** — `1 ≤ n ≤ 8`.

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

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort + used-mask dedup | **O(n · n!)** | O(n) | canonical |

## When to use which

- **Duplicates** → sort + skip.
- **Distinct** → simpler swap-in-place.
- **Return count only** → multinomial `n! / Π(k_i!)`.

## Related problems

- [Permutations](/problems/permutations)
- [Subsets II](/problems/subsets-ii)
- [Combination Sum II](/problems/combination-sum-ii)
