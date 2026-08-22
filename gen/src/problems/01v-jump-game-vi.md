# Sliding Window — Jump Game VI

*[↗ LeetCode: Jump Game VI](https://leetcode.com/problems/jump-game-vi/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Start at 0. At index i, jump 1..k steps. Max total score.

---

## Approach 1 — DP + monotonic deque (sliding window max)
**Insight.** `dp[i] = nums[i] + max(dp[i-k..i-1])`. Window max via deque of indices with decreasing `dp`.

```java
int maxResult(int[] nums, int k) {
    int n = nums.length;
    int[] dp = new int[n];
    dp[0] = nums[0];
    Deque<Integer> dq = new ArrayDeque<>();
    dq.offerLast(0);
    for (int i = 1; i < n; i++) {
        if (dq.peekFirst() < i - k) dq.pollFirst();
        dp[i] = nums[i] + dp[dq.peekFirst()];
        while (!dq.isEmpty() && dp[dq.peekLast()] <= dp[i]) dq.pollLast();
        dq.offerLast(i);
    }
    return dp[n - 1];
}
```

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| DP + monotonic deque (sliding window max) | O(n) | O(n) | primary |

## When to use which

- **Ship this** → DP + monotonic deque (sliding window max) (O(n), O(n)). The pattern's standard solution.

## Related problems

- [Constrained Subsequence Sum](/problems/constrained-subsequence-sum) — same deque idea
- [Jump Game II](/problems/greedy-jump-game-ii)
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) — the primitive
