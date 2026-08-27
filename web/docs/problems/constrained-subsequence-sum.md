# Sliding Window — Constrained Subsequence Sum

*[↗ LeetCode: Constrained Subsequence Sum](https://leetcode.com/problems/constrained-subsequence-sum/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google" />

Max sum of a subsequence where every two consecutive chosen indices differ by at most `k`.

**Example 1** — `nums=[10,2,-10,5,20], k=2` → `37`
**Example 2** — `nums=[-1,-2,-3], k=1` → `-1`
**Example 3** — `nums=[10,-2,-10,-5,20], k=2` → `23`

**Constraints** — `1 ≤ n ≤ 10⁵`; `1 ≤ k ≤ n`. Naive DP is O(nk) — at n=k=10⁵ that's 10¹⁰ ops (~5 minutes). Deque trick is O(n).


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it's restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

<MarkSolved problem-slug="constrained-subsequence-sum" /> <Bookmark problem-slug="constrained-subsequence-sum" />

<InterviewTimer problem-slug="constrained-subsequence-sum" />



## Approach 1 — Brute DP with inner window scan

**Intuition.** `dp[i] = nums[i] + max(0, max(dp[i-k..i-1]))`. For each `i`, scan back `k` positions.



```java
int constrainedSubsetSumBrute(int[] nums, int k) {
    int n = nums.length;
    int[] dp = new int[n];
    int best = Integer.MIN_VALUE;
    for (int i = 0; i < n; i++) {
        int maxPrev = 0;
        for (int j = Math.max(0, i - k); j < i; j++)
            maxPrev = Math.max(maxPrev, dp[j]);
        dp[i] = nums[i] + maxPrev;
        best = Math.max(best, dp[i]);
    }
    return best;
}
```



**Complexity** — Time **O(nk)**; Space **O(n)**. For n=k=10⁵: 10¹⁰ ops = TLE. *In an interview* state this then reach for a monotonic deque.

---

## Approach 2 — DP with monotonic deque (canonical)

**Insight.** The inner scan is a sliding-window max. Replace it with a monotonic deque of indices with **decreasing** `dp` values — the front is always the current window max in O(1) amortised.



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

**Complexity** — Time **O(n)**; Space **O(k)**. *Say aloud in an interview:* "same monotonic-deque pattern as Sliding Window Maximum and Jump Game VI — reusable across every 'DP with window max/min' problem."

---

## Try it yourself

<JavaRunner problem-slug="constrained-subsequence-sum" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute DP (window scan) | O(nk) | O(n) | Reference; TLE at 10⁵ |
| **DP + monotonic deque** | **O(n)** | O(k) | **Canonical** |

## When to use which

- **"Max/min over sliding window of DP values"** → monotonic deque.
- **Jump-game family** → same template.
- **k = 1** → same skeleton, deque may be size 1.

<AiCompanion problem-slug="constrained-subsequence-sum" pattern-hint="sliding window" />

## Related problems

- [Jump Game VI](/problems/jump-game-vi)
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)
- [Shortest Subarray with Sum at Least K](/problems/shortest-subarray-with-sum-at-least-k)

<FeedbackWidget problem-slug="constrained-subsequence-sum" />
