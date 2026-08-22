# Sliding Window — Count Number of Nice Subarrays

*[↗ LeetCode: Count Number of Nice Subarrays](https://leetcode.com/problems/count-number-of-nice-subarrays/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Count subarrays containing exactly `k` odd numbers.

---

## Approach 1 — Treat odd = 1, even = 0 → Binary Subarrays With Sum
**Insight.** Same trick: `atMost(k) - atMost(k-1)`.

```java
int numberOfSubarrays(int[] nums, int k) {
    return atMost(nums, k) - atMost(nums, k - 1);
}
int atMost(int[] nums, int k) {
    if (k < 0) return 0;
    int l = 0, odd = 0, res = 0;
    for (int r = 0; r < nums.length; r++) {
        if (nums[r] % 2 == 1) odd++;
        while (odd > k) if (nums[l++] % 2 == 1) odd--;
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
| Treat odd = 1, even = 0 → Binary Subarrays… | O(n) | O(1) | primary |

## When to use which

- **Ship this** → Treat odd = 1, even = 0 → Binary Subarrays With Sum (O(n), O(1)). The pattern's standard solution.

## Related problems

- [Binary Subarrays With Sum](/problems/binary-subarrays-with-sum) — identical mechanics
- [Subarrays with K Different Integers](/problems/subarrays-with-k-different-integers)
