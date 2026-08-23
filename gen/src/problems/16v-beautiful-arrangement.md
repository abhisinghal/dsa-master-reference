# Backtracking — Beautiful Arrangement

*[↗ LeetCode: Beautiful Arrangement](https://leetcode.com/problems/beautiful-arrangement/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

<CompanyTags companies="Meta, Amazon, Google" />

Count permutations of 1..n where for every position `i` (1-indexed), `a[i] % i == 0` OR `i % a[i] == 0`.

**Example 1** — `n=2` → `2`
**Example 2** — `n=1` → `1`

**Constraints** — `1 ≤ n ≤ 15`.


<Hints
  hint1="You’re exploring a decision tree. What’s the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

## Approach 1 — Backtracking with used-mask

```java
int countArrangement(int n) {
    return dfs(n, 1, new boolean[n + 1]);
}
int dfs(int n, int pos, boolean[] used) {
    if (pos > n) return 1;
    int c = 0;
    for (int v = 1; v <= n; v++)
        if (!used[v] && (v % pos == 0 || pos % v == 0)) {
            used[v] = true;
            c += dfs(n, pos + 1, used);
            used[v] = false;
        }
    return c;
}
```

## Approach 2 — Bitmask DP (n ≤ 15)

`dp[mask]` = # ways to fill first `popcount(mask)` positions using selected numbers.

```java
int countArrangementBM(int n) {
    int full = 1 << n;
    int[] dp = new int[full];
    dp[0] = 1;
    for (int mask = 1; mask < full; mask++) {
        int pos = Integer.bitCount(mask);
        for (int v = 1; v <= n; v++) {
            int bit = 1 << (v - 1);
            if ((mask & bit) == 0) continue;
            if (v % pos == 0 || pos % v == 0) dp[mask] += dp[mask ^ bit];
        }
    }
    return dp[full - 1];
}
```

**Complexity** — Both **O(n · 2ⁿ)**; DP cleaner for n ≤ 15.

---

## Try it yourself

<JavaRunner problem-slug="beautiful-arrangement" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Backtracking | O(n · 2ⁿ) | O(n) | canonical |
| Bitmask DP | **O(n · 2ⁿ)** | O(2ⁿ) | iterative |

## When to use which

- **Small n** → either.
- **n ≤ 15** → bitmask DP is clean.
- **Larger n** → no polynomial algo.

<AiCompanion problem-slug="beautiful-arrangement" pattern-hint="backtracking" />

## Related problems

- [Number of Ways to Wear Different Hats](/problems/number-of-ways-to-wear-different-hats-to-each-other)
- [Partition to K Equal Sum Subsets](/problems/partition-to-k-equal-sum-subsets)