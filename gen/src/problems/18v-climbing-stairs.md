# DP — Climbing Stairs

*[↗ LeetCode: Climbing Stairs](https://leetcode.com/problems/climbing-stairs/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/dp)

Steps of 1 or 2. Number of ways to reach step n.

---

## Approach 1 — Recursion + memo

---

## Approach 2 — Bottom-up DP, O(1) space
**Insight.** `dp[i] = dp[i-1] + dp[i-2]` (Fibonacci).

```java
int climbStairs(int n) {
    int a = 1, b = 1;
    for (int i = 2; i <= n; i++) { int c = a + b; a = b; b = c; }
    return b;
}
```

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Approach 3 — Matrix exponentiation
`[[1,1],[1,0]]^n` gives Fibonacci in **O(log n)**. Interview curiosity when asked "can it be sublinear".

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Recursion + memo | — | — | baseline |
| Bottom-up DP, O(1) space | O(n) | O(1) | improved |
| Matrix exponentiation | O(log n) | — | optimum |

## When to use which

- **State it for signal** → Recursion + memo (—). Correct baseline; call it out then move on.
- **Intermediate refinement** → Bottom-up DP, O(1) space (O(n)).
- **Ship this** → Matrix exponentiation (O(log n), —). Expected optimum in interview.

## Related problems

- [Min Cost Climbing Stairs](/problems/min-cost-climbing-stairs) — cost variant
- [House Robber](/problems/dp-house-robber) — same recurrence with pick/skip
- [Fibonacci Number](https://leetcode.com/problems/fibonacci-number/)
