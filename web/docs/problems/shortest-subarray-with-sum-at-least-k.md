# Sliding Window — Shortest Subarray With Sum at Least K

*[↗ LeetCode: Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/monotonic-stack)

Smallest subarray sum ≥ `k`. **Array may contain negatives.**

## Approach 1 — Sliding window fails

With negatives, sum is not monotone in window size — can't shrink safely.

## Approach 2 — Prefix sums + monotonic deque

**Insight.** Define `P[i]` = prefix sum. Answer = min `j - i` with `P[j] - P[i] ≥ k`. For each `j`, we want the earliest `i < j` with `P[i] ≤ P[j] - k`.

Maintain a deque of candidate `i` indices where `P` is **increasing**. On processing `j`:
- **Pop front** while `P[deque.front] ≤ P[j] - k` — those `i` yield candidates (record length) and can be discarded (any later `j'` picking them would give a longer subarray).
- **Pop back** while `P[deque.back] ≥ P[j]` — a smaller-or-equal prefix at later index dominates.



```java
int shortestSubarray(int[] nums, int k) {
    int n = nums.length;
    long[] P = new long[n + 1];
    for (int i = 0; i < n; i++) P[i + 1] = P[i] + nums[i];
    Deque<Integer> dq = new ArrayDeque<>();
    int best = Integer.MAX_VALUE;
    for (int j = 0; j <= n; j++) {
        while (!dq.isEmpty() && P[j] - P[dq.peekFirst()] >= k)
            best = Math.min(best, j - dq.pollFirst());
        while (!dq.isEmpty() && P[dq.peekLast()] >= P[j]) dq.pollLast();
        dq.offerLast(j);
    }
    return best == Integer.MAX_VALUE ? -1 : best;
}
```



**Complexity** — Time **O(n)**; Space **O(n)**.

## Related problems

- [Minimum Size Subarray Sum](/problems/minimum-size-subarray-sum) — positives only, plain window
- [Constrained Subsequence Sum](/problems/constrained-subsequence-sum) — DP with monotonic deque
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) — deque template
