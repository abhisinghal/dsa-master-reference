# Hashing — Two Sum Less Than K

*[↗ LeetCode: Two Sum Less Than K](https://leetcode.com/problems/two-sum-less-than-k/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

Return the max sum `< k` from any pair, or `-1`.

## Approach — Sort + two pointer

**Insight.** Sort. `l` and `r` from ends: if `sum < k`, record and advance `l`; else retreat `r`.



```java
int twoSumLessThanK(int[] nums, int k) {
    Arrays.sort(nums);
    int l = 0, r = nums.length - 1, best = -1;
    while (l < r) {
        int s = nums[l] + nums[r];
        if (s < k) { best = Math.max(best, s); l++; }
        else r--;
    }
    return best;
}
```



**Complexity** — Time **O(n log n)**; Space **O(1)**.

**Bucket alternative.** Since values are bounded (1..1000), we can bucket-count then two-pointer over buckets → O(n + max) time.

## Related problems

- [Two Sum II](/problems/two-sum-ii-input-array-is-sorted)
- [3Sum Smaller](/problems/3sum-smaller)
