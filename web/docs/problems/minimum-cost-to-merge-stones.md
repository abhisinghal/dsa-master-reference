# DP — Minimum Cost to Merge Stones

*[↗ LeetCode: Minimum Cost to Merge Stones](https://leetcode.com/problems/minimum-cost-to-merge-stones/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Google, Amazon" />

Merge exactly k consecutive piles at a time; cost = sum. Min total to merge all into one. `-1` if impossible.

**Example 1** — `stones=[3,2,4,1], k=2` → `20`
**Example 2** — `stones=[3,2,4,1], k=3` → `-1` (impossible — `(n-1)%(k-1) = 3%2 = 1 ≠ 0`)
**Example 3** — `stones=[3,5,1,2,6], k=3` → `25`

**Constraints** — `1 ≤ n ≤ 30`; `2 ≤ k ≤ 30`. Brute enumeration of merge orders is n! — at n=15 is 10¹² ops. Interval DP is O(n³/k) ≈ 27,000/2 = 13,500 ops at n=30.


<Hints
  hint1="What is the state? What are the transitions? What's the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="minimum-cost-to-merge-stones" /> <Bookmark problem-slug="minimum-cost-to-merge-stones" />

<InterviewTimer problem-slug="minimum-cost-to-merge-stones" />



## Approach 1 — Brute: try every merge sequence

**Intuition.** At each step, pick any consecutive `k` piles and merge them. Recurse on the resulting sequence. Return the min over all orderings.



```java
int mergeStonesBrute(int[] stones, int k) {
    List<Integer> piles = new ArrayList<>();
    for (int x : stones) piles.add(x);
    if ((piles.size() - 1) % (k - 1) != 0) return -1;
    return dfsBrute(piles, k);
}
int dfsBrute(List<Integer> piles, int k) {
    if (piles.size() == 1) return 0;
    int best = Integer.MAX_VALUE;
    for (int i = 0; i + k <= piles.size(); i++) {
        int sum = 0;
        for (int j = i; j < i + k; j++) sum += piles.get(j);
        List<Integer> next = new ArrayList<>(piles.subList(0, i));
        next.add(sum);
        next.addAll(piles.subList(i + k, piles.size()));
        best = Math.min(best, sum + dfsBrute(next, k));
    }
    return best;
}
```



**Complexity** — Time **O(n!)**; Space **O(n)** stack. TLE past n=12. *In an interview* state this then flip to interval DP.

---

## Approach 2 — Interval DP with residue trick (canonical)

**Insight.** Feasible iff `(n-1) % (k-1) == 0` (each merge reduces pile count by `k-1`, so to reach 1 pile the *reduction* `n-1` must be divisible by `k-1`).

Define `dp[i][j]` = min cost to reduce range `[i, j]` to `((j-i) mod (k-1)) + 1` piles. Split at every valid `m` (respecting the residue). Add the total sum at merge points.



```java
int mergeStones(int[] stones, int k) {
    int n = stones.length;
    if ((n - 1) % (k - 1) != 0) return -1;
    int[] pref = new int[n + 1];
    for (int i = 0; i < n; i++) pref[i+1] = pref[i] + stones[i];
    int[][] dp = new int[n][n];
    for (int len = k; len <= n; len++)
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            dp[i][j] = Integer.MAX_VALUE;
            for (int m = i; m < j; m += k - 1)
                dp[i][j] = Math.min(dp[i][j], dp[i][m] + dp[m+1][j]);
            if ((j - i) % (k - 1) == 0) dp[i][j] += pref[j+1] - pref[i];
        }
    return dp[0][n-1];
}
```



<CodeTrace
  title="Interval DP with residue trick (canonical)"
  :values="['3', '2', '4', '1']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n³ / k)**; Space **O(n²)**. *Say aloud in an interview:* "same interval-DP shape as Matrix Chain Multiplication and Burst Balloons — the residue trick generalises k-way merging to arbitrary k."

---

## Try it yourself

<JavaRunner problem-slug="minimum-cost-to-merge-stones" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute merge sequences | O(n!) | O(n) | Reference; TLE past n=12 |
| **Interval DP + residue** | **O(n³/k)** | O(n²) | **Canonical** |

## When to use which

- **Merge k at a time** → residue trick.
- **k=2** → merge sort merging pattern.
- **Optimal binary search tree** — similar interval DP.

<AiCompanion problem-slug="minimum-cost-to-merge-stones" pattern-hint="dynamic programming" />

## Related problems

- [Burst Balloons](/problems/burst-balloons)

<FeedbackWidget problem-slug="minimum-cost-to-merge-stones" />
