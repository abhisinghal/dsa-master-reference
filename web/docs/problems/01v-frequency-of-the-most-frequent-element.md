# Sliding Window — Frequency of the Most Frequent Element

*[↗ LeetCode: Frequency of the Most Frequent Element](https://leetcode.com/problems/frequency-of-the-most-frequent-element/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Given nums and budget `k` (increments), maximize the frequency of any single value.

## Approach — Sort + sliding window with sum budget

**Insight.** Sort. In a window `[l, r]` of sorted nums, raising every value to `nums[r]` costs `nums[r] * (r - l + 1) - windowSum`. Extend r; while cost &gt; k, shrink l. Track max window size.



```java
int maxFrequency(int[] nums, int k) {
    Arrays.sort(nums);
    long sum = 0;
    int l = 0, best = 0;
    for (int r = 0; r < nums.length; r++) {
        sum += nums[r];
        while ((long) nums[r] * (r - l + 1) - sum > k) sum -= nums[l++];
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```



**Complexity** — Time **O(n log n)**; Space **O(1)**.

## Related problems

- [Minimum Operations to Reduce X to Zero](https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/) — complementary window
- [Longest Repeating Character Replacement](/problems/longest-repeating-character-replacement)
