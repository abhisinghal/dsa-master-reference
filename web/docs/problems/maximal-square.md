# DP — Maximal Square

*[↗ LeetCode: Maximal Square](https://leetcode.com/problems/maximal-square/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google, Meta, Uber" />

Largest square of `1`s in binary matrix. Return area.

**Example 1** — Standard binary matrix → `4`

**Constraints** — `1 ≤ m, n ≤ 300`.


<Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="maximal-square" /> <Bookmark problem-slug="maximal-square" />

<InterviewTimer problem-slug="maximal-square" />



## Approach — DP `side[i][j]` = largest square ending at (i, j) (canonical)

**Insight.** `mat[i][j] == '1'` → `side[i][j] = 1 + min(side[i-1][j], side[i][j-1], side[i-1][j-1])`.



```java
int maximalSquare(char[][] mat) {
    int m = mat.length, n = mat[0].length, best = 0;
    int[] dp = new int[n + 1];
    int prev = 0;
    for (int i = 1; i <= m; i++) {
        prev = 0;
        for (int j = 1; j <= n; j++) {
            int tmp = dp[j];
            if (mat[i-1][j-1] == '1') {
                dp[j] = 1 + Math.min(dp[j], Math.min(dp[j-1], prev));
                best = Math.max(best, dp[j]);
            } else dp[j] = 0;
            prev = tmp;
        }
    }
    return best * best;
}
```



**Complexity** — Time **O(mn)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="maximal-square" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DP min-of-3 | **O(mn)** | O(n) | canonical |

## When to use which

- **Only squares** → this DP.
- **Rectangles** → [Maximal Rectangle](/problems/maximal-rectangle) — row heights + stack.
- **Count all squares** → sum of `side[i][j]`.

<AiCompanion problem-slug="maximal-square" pattern-hint="dynamic programming" />

## Related problems

- [Maximal Rectangle](/problems/maximal-rectangle)
- [Count Square Submatrices](https://leetcode.com/problems/count-square-submatrices-with-all-ones/)

<FeedbackWidget problem-slug="maximal-square" />

<RelatedProblems problems="delete-and-earn::Delete And Earn|climbing-stairs::Climbing Stairs|regular-expression-matching::Regular Expression Matching" />
