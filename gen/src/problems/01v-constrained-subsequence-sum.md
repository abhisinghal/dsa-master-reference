# Sliding Window — Constrained Subsequence Sum

*[↗ LeetCode: Constrained Subsequence Sum](https://leetcode.com/problems/constrained-subsequence-sum/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

Max sum of a subsequence where every two consecutive chosen indices differ by at most `k`.

---

## Approach 1 — DP with monotonic deque
**Insight.** `dp[i] = nums[i] + max(0, max(dp[i-k..i-1]))`. Window-max query on a sliding window → monotonic deque (like Sliding Window Maximum).

```java
int constrainedSubsetSum(int[] nums, int k) {
    int n = nums.length;
    int[] dp = new int[n];
    Deque<Integer> dq = new ArrayDeque<>();
    int best = Integer.MIN_VALUE;
    for (int i = 0; i < n; i++) {
        dp[i] = nums[i] + (dq.isEmpty() ? 0 : Math.max(0, dp[dq.peekFirst()]));
        while (!dq.isEmpty() && dp[dq.peekLast()] <= dp[i]) dq.pollLast();
        dq.offerLast(i);
        if (dq.peekFirst() == i - k) dq.pollFirst();
        best = Math.max(best, dp[i]);
    }
    return best;
}
```

**Invariant.** Deque holds indices in the current k-window, with `dp` values strictly decreasing → front is the window max.

**Complexity** — Time **O(n)**; Space **O(k)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| DP with monotonic deque | O(n) | O(k) | primary |

## When to use which

- **Ship this** → DP with monotonic deque (O(n), O(k)). The pattern's standard solution.

## Related problems

- [Jump Game VI](/problems/jump-game-vi) — same deque template
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)
- [Shortest Subarray with Sum at Least K](/problems/shortest-subarray-with-sum-at-least-k)
