# Dynamic Programming — House Robber

*[↗ LeetCode: House Robber](https://leetcode.com/problems/house-robber/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, LinkedIn, Bloomberg" />

Given `nums[i]` = value at house `i`, return the max total value you can rob given you can't rob two adjacent houses.

**Example 1** — `[2,7,9,3,1]` → `12` (rob 2 + 9 + 1)
**Example 2** — `[2,1,1,2]` → `4` (rob 2 + 2)

**Constraints** — `1 ≤ n ≤ 100`; `0 ≤ nums[i] ≤ 400`.


<Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="dp-house-robber" />

<InterviewTimer problem-slug="dp-house-robber" />



## Approach 1 — Brute force recursion

**Intuition.** At each house: either **rob** it (skip next) or **skip** it. Return the max.

```java
int robBrute(int[] a) { return rec(a, 0); }
int rec(int[] a, int i) {
    if (i >= a.length) return 0;
    int rob = a[i] + rec(a, i + 2);
    int skip = rec(a, i + 1);
    return Math.max(rob, skip);
}
```

**Complexity** — Time **O(2ⁿ)**; Space **O(n)** recursion. TLE at n=100.

---

## Approach 2 — Memoized recursion (top-down DP)

**Insight from brute.** The recursion revisits `rec(a, i)` exponentially many times. Cache it.

```java
int robMemo(int[] a) {
    Integer[] memo = new Integer[a.length];
    return rec(a, 0, memo);
}
int rec(int[] a, int i, Integer[] memo) {
    if (i >= a.length) return 0;
    if (memo[i] != null) return memo[i];
    return memo[i] = Math.max(a[i] + rec(a, i + 2, memo), rec(a, i + 1, memo));
}
```

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Approach 3 — Bottom-up DP (tabulation)

**Insight from memo.** Compute `dp[i]` = max value from `i..n-1` iteratively.

```java
int robTable(int[] a) {
    int n = a.length;
    int[] dp = new int[n + 2];
    for (int i = n - 1; i >= 0; i--)
        dp[i] = Math.max(a[i] + dp[i + 2], dp[i + 1]);
    return dp[0];
}
```

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Approach 4 — Rolling variables (O(1) space)

**Insight from tabulation.** We only ever read `dp[i+1]` and `dp[i+2]` — two variables suffice.

```java
int rob(int[] a) {
    int prev2 = 0, prev1 = 0;
    for (int x : a) {
        int cur = Math.max(prev1, prev2 + x);
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
```

<CodeTrace
  title="O(1)-space DP — nums=[2,7,9,3,1]"
  :values="[2,7,9,3,1]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { prev2: 0, prev1: 2, choice: "rob" }, note: "max(0, 0+2)=2", added: [0] },
    { pointers: { i: 1 }, vars: { prev2: 2, prev1: 7, choice: "rob" }, note: "max(2, 0+7)=7", added: [1] },
    { pointers: { i: 2 }, vars: { prev2: 7, prev1: 11, choice: "rob" }, note: "max(7, 2+9)=11", added: [2] },
    { pointers: { i: 3 }, vars: { prev2: 11, prev1: 11, choice: "skip" }, note: "max(11, 7+3)=11" },
    { pointers: { i: 4 }, vars: { prev2: 11, prev1: 12, choice: "rob" }, note: "max(11, 11+1)=12. answer 12", added: [4] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. Optimal.

---

## Try it yourself

<JavaRunner problem-slug="dp-house-robber" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute recursion | O(2ⁿ) | O(n) |
| Memoized | O(n) | O(n) |
| Tabulated | O(n) | O(n) |
| Rolling variables | **O(n)** | **O(1)** |

## When to use which

- **Cold interview** → walk brute → memo → table → rolled. This ladder shows the full DP thought process.
- **Interviewer probes "why rolled?"** → we only need dp[i-1] and dp[i-2].

<AiCompanion problem-slug="dp-house-robber" pattern-hint="dynamic programming" />

## Related problems (same ladder applies)

- [House Robber II](https://leetcode.com/problems/house-robber-ii/) — circle: run twice, exclude first vs exclude last
- [Delete and Earn](https://leetcode.com/problems/delete-and-earn/) — bucket by value, then House Robber
- [Paint House](https://leetcode.com/problems/paint-house/) — 3-state variant
- [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) — same recurrence shape (Fibonacci)

<FeedbackWidget problem-slug="dp-house-robber" />
