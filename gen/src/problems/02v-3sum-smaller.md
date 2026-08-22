# Two Pointers — 3Sum Smaller

*[↗ LeetCode: 3Sum Smaller](https://leetcode.com/problems/3sum-smaller/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

Count triplets `(i, j, k)` with `i < j < k` and `nums[i] + nums[j] + nums[k] < target`.

## Approach — Sort + counting two-pointer

**Insight.** After sorting, for each `i` and left pointer `l`, if `nums[i]+nums[l]+nums[r] < target`, then **every** `k` in `(l, r]` also satisfies it — add `r - l` and advance `l`. Otherwise, decrement `r`.

```java
int threeSumSmaller(int[] nums, int target) {
    Arrays.sort(nums);
    int count = 0;
    for (int i = 0; i < nums.length - 2; i++) {
        int l = i + 1, r = nums.length - 1;
        while (l < r) {
            if (nums[i] + nums[l] + nums[r] < target) { count += r - l; l++; }
            else r--;
        }
    }
    return count;
}
```

**Complexity** — Time **O(n²)**; Space **O(1)**.

## Related problems

- [3Sum](/problems/3sum)
- [3Sum Closest](/problems/3sum-closest)
