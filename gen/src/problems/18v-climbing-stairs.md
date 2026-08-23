# DP — Climbing Stairs

*[↗ LeetCode: Climbing Stairs](https://leetcode.com/problems/climbing-stairs/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Meta, Amazon, Google, Adobe, Bloomberg" />

Steps of 1 or 2. Number of ways to reach step `n`.

**Example 1** — `n=2` → `2`
**Example 2** — `n=3` → `3`

**Constraints** — `1 ≤ n ≤ 45`.


<Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="climbing-stairs" />


## Approach 1 — Recursion + memo
O(n).

## Approach 2 — Bottom-up DP O(1) space (canonical)

**Insight.** `dp[i] = dp[i-1] + dp[i-2]` — Fibonacci.

```java
int climbStairs(int n) {
    int a = 1, b = 1;
    for (int i = 2; i <= n; i++) { int c = a + b; a = b; b = c; }
    return b;
}
```

## Approach 3 — Matrix exponentiation
`[[1,1],[1,0]]^n` → **O(log n)**. Interview curiosity.

**Complexity** — Time **O(n)** DP; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="climbing-stairs" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Memo | O(n) | O(n) | correct |
| Rolling DP | **O(n)** | **O(1)** | canonical |
| Matrix expo | O(log n) | O(1) | polish |

## When to use which

- **Standard** → rolling DP.
- **Very large n** → matrix expo or closed-form Binet.
- **Steps of {1..k}** → same recurrence extended.

<AiCompanion problem-slug="climbing-stairs" pattern-hint="dynamic programming" />

## Related problems

- [Min Cost Climbing Stairs](/problems/min-cost-climbing-stairs)
- [House Robber](/problems/dp-house-robber)
- [Fibonacci Number](https://leetcode.com/problems/fibonacci-number/)

<FeedbackWidget problem-slug="climbing-stairs" />

<RelatedProblems problems="coin-change::Coin Change|target-sum::Target Sum|min-cost-climbing-stairs::Min Cost Climbing Stairs" />
