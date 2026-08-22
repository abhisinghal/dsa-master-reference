# Sliding Window — Binary Subarrays With Sum

*[↗ LeetCode: Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

Count binary subarrays with sum exactly `goal`.

---

## Approach 1 — Prefix-sum hash (works for any integers)
`count[preSum - goal]` accumulated as we sweep. See [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k).

---

## Approach 2 — At-most-goal minus at-most-(goal-1)
**Insight.** With nonneg integers, `atMost(goal)` slides cleanly: extend r; shrink from l while sum &gt; goal; add `r - l + 1`. Then subtract.



```java
int numSubarraysWithSum(int[] nums, int goal) {
    return atMost(nums, goal) - atMost(nums, goal - 1);
}
int atMost(int[] nums, int goal) {
    if (goal < 0) return 0;
    int l = 0, sum = 0, res = 0;
    for (int r = 0; r < nums.length; r++) {
        sum += nums[r];
        while (sum > goal) sum -= nums[l++];
        res += r - l + 1;
    }
    return res;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Prefix-sum hash (works for any integers) | — | — | baseline |
| At-most-goal minus at-most-(goal-1) | O(n) | O(1) | optimum |

## When to use which

- **State it for signal** → Prefix-sum hash (works for any integers) (—). Correct baseline; call it out then move on.
- **Ship this** → At-most-goal minus at-most-(goal-1) (O(n), O(1)). Expected optimum in interview.

## Related problems

- [Subarrays with K Different Integers](/problems/subarrays-with-k-different-integers)
- [Count Number of Nice Subarrays](/problems/count-number-of-nice-subarrays)
- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k)
