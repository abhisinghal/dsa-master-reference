# Sliding Window — Subarrays With K Different Integers

*[↗ LeetCode: Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/sliding-window)

Count subarrays with **exactly** K distinct integers.

---

## Approach 1 — At-most-K minus at-most-(K-1)
**Insight.** Direct "exactly K" is hard to slide. But `exactly(K) = atMost(K) - atMost(K-1)`. Each `atMost` is standard sliding window (distinct counter).

```java
int subarraysWithKDistinct(int[] nums, int k) {
    return atMost(nums, k) - atMost(nums, k - 1);
}
int atMost(int[] nums, int k) {
    if (k < 0) return 0;
    Map<Integer, Integer> cnt = new HashMap<>();
    int l = 0, res = 0;
    for (int r = 0; r < nums.length; r++) {
        cnt.merge(nums[r], 1, Integer::sum);
        while (cnt.size() > k) {
            cnt.merge(nums[l], -1, Integer::sum);
            if (cnt.get(nums[l]) == 0) cnt.remove(nums[l]);
            l++;
        }
        res += r - l + 1;
    }
    return res;
}
```

**Complexity** — Time **O(n)**; Space **O(k)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| At-most-K minus at-most-(K-1) | O(n) | O(k) | primary |

## When to use which

- **Ship this** → At-most-K minus at-most-(K-1) (O(n), O(k)). The pattern's standard solution.

## Related problems

- [Binary Subarrays With Sum](/problems/binary-subarrays-with-sum) — same at-most trick with sums
- [Count Number of Nice Subarrays](/problems/count-number-of-nice-subarrays) — at-most on odd count
- [Longest Substring With At Most K Distinct](/problems/longest-substring-with-at-most-k-distinct)
