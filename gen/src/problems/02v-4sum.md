# Two Pointers — 4Sum

*[↗ LeetCode: 4Sum](https://leetcode.com/problems/4sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

Return all unique quadruplets summing to `target`.

## Approach 1 — Quadruple loop O(n⁴)

## Approach 2 — Sort + two nested loops + two-pointer

**Insight.** Fix `i` and `j`, then two-pointer over the rest. Skip duplicates at each of the four levels. Use `long` for the sum to avoid overflow on adversarial inputs.

```java
List<List<Integer>> fourSum(int[] nums, int target) {
    Arrays.sort(nums);
    List<List<Integer>> out = new ArrayList<>();
    int n = nums.length;
    for (int i = 0; i < n - 3; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        for (int j = i + 1; j < n - 2; j++) {
            if (j > i + 1 && nums[j] == nums[j - 1]) continue;
            int l = j + 1, r = n - 1;
            while (l < r) {
                long s = (long) nums[i] + nums[j] + nums[l] + nums[r];
                if (s == target) {
                    out.add(Arrays.asList(nums[i], nums[j], nums[l], nums[r]));
                    while (l < r && nums[l] == nums[l + 1]) l++;
                    while (l < r && nums[r] == nums[r - 1]) r--;
                    l++; r--;
                } else if (s < target) l++;
                else r--;
            }
        }
    }
    return out;
}
```

**Complexity** — Time **O(n³)**; Space **O(1)** extra.

**Generalization.** kSum → recursion + 2Sum base case gives O(n^(k-1)).

## Related problems

- [3Sum](/problems/3sum)
- [4Sum II](https://leetcode.com/problems/4sum-ii/) — hash-based, splits into two halves
