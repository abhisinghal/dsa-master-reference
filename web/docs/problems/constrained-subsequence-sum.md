# Sliding Window — Constrained Subsequence Sum

*[↗ LeetCode: Constrained Subsequence Sum](https://leetcode.com/problems/constrained-subsequence-sum/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

&lt;CompanyTags companies="Amazon, Google" /&gt;

Max sum of a subsequence where every two consecutive chosen indices differ by at most `k`.

**Example 1** — `nums=[10,2,-10,5,20], k=2` → `37`
**Example 2** — `nums=[-1,-2,-3], k=1` → `-1`
**Example 3** — `nums=[10,-2,-10,-5,20], k=2` → `23`

**Constraints** — `1 ≤ n ≤ 10⁵`; `1 ≤ k ≤ n`.


&lt;Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/&gt;
---

## Approach — DP with monotonic deque (canonical)

**Insight.** `dp[i] = nums[i] + max(0, max(dp[i-k..i-1]))`. Window-max via deque of indices with **decreasing** `dp` values → front is window max.



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



<CodeTrace
  title="Deque DP — nums=[10,2,-10,5,20], k=2"
  :values="['10','2','-10','5','20']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { dp: 10, deque: "[0]" }, note: "" },
    { pointers: { i: 1 }, vars: { dp: 12, deque: "[1]" }, note: "dp[1]=2+10=12 pops 0" },
    { pointers: { i: 3 }, vars: { dp: 17, deque: "[3]" }, note: "dp[3]=5+12=17" },
    { pointers: { i: 4 }, vars: { dp: 37, best: 37 }, note: "dp[4]=20+17=37" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(k)**.

---

## Try it yourself

<JavaRunner problem-slug="constrained-subsequence-sum" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DP + monotonic deque | **O(n)** | O(k) | canonical |

## When to use which

- **"Max/min over sliding window of DP values"** → monotonic deque.
- **Jump-game family** → same template.
- **k = 1** → same skeleton, deque may be size 1.

## Related problems

- [Jump Game VI](/problems/jump-game-vi)
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)
- [Shortest Subarray with Sum at Least K](/problems/shortest-subarray-with-sum-at-least-k)