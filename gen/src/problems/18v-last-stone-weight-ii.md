# DP — Last Stone Weight II

*[↗ LeetCode: Last Stone Weight II](https://leetcode.com/problems/last-stone-weight-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Amazon, Google" />

Smash pairs (larger becomes diff). Minimize final remaining weight.

**Example 1** — `stones=[2,7,4,1,8,1]` → `1`
**Example 2** — `stones=[31,26,33,21,40]` → `5`

**Constraints** — `1 ≤ n ≤ 30`; `1 ≤ stones[i] ≤ 100`.


<Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/>
---

<MarkSolved problem-slug="last-stone-weight-ii" />

<InterviewTimer problem-slug="last-stone-weight-ii" />



## Approach — Reduce to subset-sum closest to total/2 (canonical)

**Insight.** Result = `|sum(+) - sum(-)| = |total - 2·subsetSum|`. Pick subset closest to `total/2`.

```java
int lastStoneWeightII(int[] stones) {
    int total = 0; for (int x : stones) total += x;
    int half = total / 2;
    boolean[] dp = new boolean[half + 1];
    dp[0] = true;
    for (int x : stones)
        for (int j = half; j >= x; j--)
            dp[j] |= dp[j - x];
    for (int j = half; j >= 0; j--) if (dp[j]) return total - 2 * j;
    return 0;
}
```

<CodeTrace
  title="Reduce to subset-sum closest to total/2 (canonical)"
  :values="['2', '7', '4', '1', '8', '1']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 3 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 5 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n · total)**; Space **O(total)**.

---

## Try it yourself

<JavaRunner problem-slug="last-stone-weight-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Reduce to subset-sum | **O(n · total)** | O(total) | canonical |

## When to use which

- **Minimize sum diff** → subset-sum close to half.
- **Return which stones on each side** → track parent choices.

<AiCompanion problem-slug="last-stone-weight-ii" pattern-hint="dynamic programming" />

## Related problems

- [Partition Equal Subset Sum](/problems/partition-equal-subset-sum)
- [Target Sum](/problems/target-sum)

<FeedbackWidget problem-slug="last-stone-weight-ii" />
