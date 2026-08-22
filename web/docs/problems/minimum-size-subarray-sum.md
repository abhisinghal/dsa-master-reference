# Sliding Window — Minimum Size Subarray Sum

*[↗ LeetCode: Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Smallest contiguous subarray with sum ≥ `target`. (Positive integers.)

## Approach 1 — O(n²) brute force

## Approach 2 — Sliding window

**Insight.** With **positive** values, `sum` is monotone in window size. Extend r; while sum ≥ target, shrink from l tracking min length.



```java
int minSubArrayLen(int target, int[] nums) {
    int l = 0, sum = 0, best = Integer.MAX_VALUE;
    for (int r = 0; r < nums.length; r++) {
        sum += nums[r];
        while (sum >= target) {
            best = Math.min(best, r - l + 1);
            sum -= nums[l++];
        }
    }
    return best == Integer.MAX_VALUE ? 0 : best;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

## Approach 3 — Prefix sum + binary search

Compute prefix sums; for each `i`, binary-search the smallest `j ≥ i` with `prefix[j] - prefix[i] ≥ target`. O(n log n). Necessary when the array has **negatives** (window fails); see Shortest Subarray with Sum at Least K.

## Related problems

- [Shortest Subarray with Sum at Least K](/problems/shortest-subarray-with-sum-at-least-k) — with negatives → monotonic deque
- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k) — count, not length
