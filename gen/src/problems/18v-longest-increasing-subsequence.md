# Dynamic Programming — Longest Increasing Subsequence

*[↗ LeetCode: Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, LinkedIn" />

Return the length of the **longest strictly increasing subsequence** of `nums`.

**Example 1** — `nums=[10,9,2,5,3,7,101,18]` → `4` (`2,3,7,101`)
**Example 2** — `nums=[0,1,0,3,2,3]` → `4`
**Example 3** — `nums=[7,7,7,7,7]` → `1`

**Constraints** — `1 ≤ n ≤ 2500`; `-10⁴ ≤ nums[i] ≤ 10⁴`.


<Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

## Approach 1 — Brute force recursion

**Intuition.** For each `i`, either include or exclude — `2^n` subsets.

**Complexity** — Time **O(2ⁿ)**; Space **O(n)**. Useless past n≈20.

---

## Approach 2 — DP (O(n²))

**Insight.** `dp[i]` = longest increasing subsequence ending at `i`. Recurrence: `dp[i] = 1 + max(dp[j] : j < i and nums[j] < nums[i])`.

```java
int lengthOfLISDp(int[] a) {
    int n = a.length, best = 1;
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++)
            if (a[j] < a[i]) dp[i] = Math.max(dp[i], dp[j] + 1);
        best = Math.max(best, dp[i]);
    }
    return best;
}
```

**Complexity** — Time **O(n²)**; Space **O(n)**.

---

## Approach 3 — Patience sort with binary search (O(n log n))

**Insight from DP.** Maintain `tails[]` where `tails[k]` = smallest tail value of any LIS of length `k+1`. `tails` stays sorted → for each new `x`, binary search for the first `tails[k] >= x` and overwrite it. Final LIS length = `tails.length`.

`tails` is *not* an actual LIS — just their length-indexed minima. But its length equals the answer.

```java
int lengthOfLIS(int[] a) {
    int[] tails = new int[a.length];
    int len = 0;
    for (int x : a) {
        int i = Arrays.binarySearch(tails, 0, len, x);
        if (i < 0) i = -(i + 1);
        tails[i] = x;
        if (i == len) len++;
    }
    return len;
}
```

<CodeTrace
  title="Patience sort — nums=[10,9,2,5,3,7,101,18]"
  :values="[10,9,2,5,3,7,101,18]"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { tails: "[10]", len: 1 }, note: "seed" },
    { pointers: { i: 1 }, vars: { tails: "[9]", len: 1 }, note: "9 lt 10 → replace" },
    { pointers: { i: 2 }, vars: { tails: "[2]", len: 1 }, note: "2 lt 9 → replace" },
    { pointers: { i: 3 }, vars: { tails: "[2,5]", len: 2 }, note: "5 gt 2 → append", added: [2,3] },
    { pointers: { i: 5 }, vars: { tails: "[2,3,7]", len: 3 }, note: "7 → append", added: [2,4,5] },
    { pointers: { i: 6 }, vars: { tails: "[2,3,7,101]", len: 4 }, note: "101 → append", added: [2,4,5,6] },
    { pointers: { i: 7 }, vars: { tails: "[2,3,7,18]", len: 4 }, note: "18 replaces 101. answer 4" }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="longest-increasing-subsequence" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute enumerate subsets | O(2ⁿ) | O(n) |
| O(n²) DP | O(n²) | O(n) |
| Patience sort + BS | **O(n log n)** | O(n) |

## When to use which

- **Just the length** → patience sort.
- **Need to reconstruct the subsequence** → O(n²) DP with `prev[i]` traceback.
- **Non-strict (≤)** → binary search for first `> x` instead of `>= x`.

<AiCompanion problem-slug="longest-increasing-subsequence" pattern-hint="dynamic programming" />

## Related problems

- [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) — 2D DP
- [Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) — LCS(s, reverse(s))
- [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) — sort by width, LIS on heights
- [Number of Longest Increasing Subsequence](https://leetcode.com/problems/number-of-longest-increasing-subsequence/) — track count alongside length

<FeedbackWidget problem-slug="longest-increasing-subsequence" />
