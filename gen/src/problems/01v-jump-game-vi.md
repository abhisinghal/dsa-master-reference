# Sliding Window — Jump Game VI

*[↗ LeetCode: Jump Game VI](https://leetcode.com/problems/jump-game-vi/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google" />

Start at 0. At index `i`, jump 1..k steps. Max total score reaching last index.

**Example 1** — `nums=[1,-1,-2,4,-7,3], k=2` → `7`
**Example 2** — `nums=[10,-5,-2,4,0,3], k=3` → `17`
**Example 3** — `nums=[1,-5,-20,4,-1,3,-6,-3], k=2` → `0`

**Constraints** — `1 ≤ n ≤ 10⁵`; `1 ≤ k ≤ n`. Naive DP is O(nk) — at n=k=10⁵ that's 10¹⁰ ops (~5 min). Deque brings it to O(n).


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it's restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

<MarkSolved problem-slug="jump-game-vi" /> <Bookmark problem-slug="jump-game-vi" />

<InterviewTimer problem-slug="jump-game-vi" />



## Approach 1 — Brute DP with inner window scan

**Intuition.** `dp[i] = nums[i] + max(dp[i-k..i-1])`. For each `i`, scan back `k` positions.

```java
int maxResultBrute(int[] nums, int k) {
    int n = nums.length;
    int[] dp = new int[n];
    dp[0] = nums[0];
    for (int i = 1; i < n; i++) {
        int mx = Integer.MIN_VALUE;
        for (int j = Math.max(0, i - k); j < i; j++) mx = Math.max(mx, dp[j]);
        dp[i] = nums[i] + mx;
    }
    return dp[n - 1];
}
```

**Complexity** — Time **O(nk)**; Space **O(n)**. TLE at 10⁵. *In an interview* say "sliding max = monotonic deque, one canonical template."

---

## Approach 2 — DP + monotonic deque (canonical)

**Insight.** The inner scan is a window-max. Maintain a deque of indices with **decreasing** `dp` values; front is always the current window max.

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

<CodeTrace
  title="Deque DP — nums=[1,-1,-2,4,-7,3], k=2"
  :values="['1','-1','-2','4','-7','3']"
  :windowKeys="['i']"
  :cellWidth="30"
  :steps='[
    { pointers: { i: 0 }, vars: { dp: 1 }, note: "" },
    { pointers: { i: 3 }, vars: { dp: 4 }, note: "dp[3]=4+0=4" },
    { pointers: { i: 5 }, vars: { dp: 7 }, note: "dp[5]=3+4=7" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)**. *Say aloud in an interview:* "same monotonic-deque template as Sliding Window Maximum and Constrained Subsequence Sum."

---

## Try it yourself

<JavaRunner problem-slug="jump-game-vi" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute DP (window scan) | O(nk) | O(n) | Reference; TLE at 10⁵ |
| **Deque DP** | **O(n)** | O(n) | **Canonical** |

## When to use which

- **DP with window-max transition** → monotonic deque.
- **"Min steps"** → BFS layers instead.
- **k=∞ (unbounded)** → prefix max is enough.

<AiCompanion problem-slug="jump-game-vi" pattern-hint="sliding window" />

## Related problems

- [Constrained Subsequence Sum](/problems/constrained-subsequence-sum)
- [Jump Game II](/problems/greedy-jump-game-ii)
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)

<FeedbackWidget problem-slug="jump-game-vi" />
