# DP — Perfect Squares

*[↗ LeetCode: Perfect Squares](https://leetcode.com/problems/perfect-squares/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

&lt;CompanyTags companies="Amazon, Google, Meta" /&gt;

Min count of perfect squares summing to `n`.

**Example 1** — `n=12` → `3` (`4+4+4`)
**Example 2** — `n=13` → `2` (`4+9`)

**Constraints** — `1 ≤ n ≤ 10⁴`.


&lt;Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/&gt;
---

&lt;MarkSolved problem-slug="perfect-squares" /&gt; &lt;Bookmark problem-slug="perfect-squares" /&gt;

&lt;InterviewTimer problem-slug="perfect-squares" /&gt;



## Approach 1 — DP (min coin change with square coins)

`dp[i] = 1 + min(dp[i - k²])` over `k² ≤ i`.



```java
int numSquares(int n) {
    int[] dp = new int[n + 1];
    Arrays.fill(dp, Integer.MAX_VALUE);
    dp[0] = 0;
    for (int i = 1; i <= n; i++)
        for (int k = 1; k * k <= i; k++)
            if (dp[i - k*k] != Integer.MAX_VALUE)
                dp[i] = Math.min(dp[i], dp[i - k*k] + 1);
    return dp[n];
}
```



**Complexity** — Time **O(n · √n)**; Space **O(n)**.

## Approach 2 — Lagrange's four-square theorem
Every positive integer = sum of ≤ 4 squares. Result ∈ {1,2,3,4}.
- 1 iff n is perfect square.
- 4 iff `n = 4^k · (8m + 7)`.
- Else check if `n = a² + b²` → 2; else 3.

**O(√n).** Beat the DP.

---

## Try it yourself

<JavaRunner problem-slug="perfect-squares" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DP | O(n · √n) | O(n) | canonical |
| Lagrange | **O(√n)** | O(1) | polish |

## When to use which

- **Interview** → DP first.
- **"Fast bound"** → Lagrange trick.
- **Return the squares** → DP with parent pointers.

&lt;AiCompanion problem-slug="perfect-squares" pattern-hint="dynamic programming" /&gt;

## Related problems

- [Coin Change](/problems/coin-change)
- [Word Break](https://leetcode.com/problems/word-break/)

&lt;FeedbackWidget problem-slug="perfect-squares" /&gt;
