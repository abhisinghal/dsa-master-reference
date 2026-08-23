# Greedy — Jump Game

*[↗ LeetCode: Jump Game](https://leetcode.com/problems/jump-game/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg" />

`nums[i]` = max jump length from `i`. Return `true` iff we can reach the last index starting from index 0.

**Example 1** — `nums=[2,3,1,1,4]` → `true`
**Example 2** — `nums=[3,2,1,0,4]` → `false`
**Example 3** — `nums=[0]` → `true`

**Constraints** — `1 ≤ n ≤ 10⁴`.


<Hints
  hint1="Is there a local rule that provably gives global optimum? (Exchange argument.)"
  hint2="Sort by the greedy criterion (deadline / end / cost). Iterate; make the locally best choice."
  hint3="If greedy fails, DP is likely needed. But prove greedy’s correctness before writing it."
/>
---

<MarkSolved problem-slug="jump-game" /> <Bookmark problem-slug="jump-game" />

<InterviewTimer problem-slug="jump-game" />



## Approach 1 — DP `reachable[i]`

O(n²). Baseline.

## Approach 2 — Greedy farthest reach (canonical)

**Insight.** Track `maxReach = max(i + nums[i])`. At index `i`, if `i > maxReach`, we're stuck. Update as we go.



```java
boolean canJump(int[] nums) {
    int maxReach = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > maxReach) return false;
        maxReach = Math.max(maxReach, i + nums[i]);
        if (maxReach >= nums.length - 1) return true;
    }
    return true;
}
```



<CodeTrace
  title="Farthest reach — nums=[3,2,1,0,4]"
  :values="['3','2','1','0','4']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { maxReach: 3 }, note: "" },
    { pointers: { i: 3 }, vars: { maxReach: 3 }, note: "still 3" },
    { pointers: { i: 4 }, vars: { blocked: true }, note: "4 > 3 → false" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="jump-game" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DP reachable | O(n²) | O(n) | baseline |
| Greedy | **O(n)** | O(1) | canonical |

## When to use which

- **Reachability only** → greedy.
- **Min jumps** → [Jump Game II](/problems/greedy-jump-game-ii) — BFS layers.
- **Arbitrary graph jumps** → [Jump Game III](/problems/jump-game-iii) — BFS.

<AiCompanion problem-slug="jump-game" pattern-hint="greedy" />

## Related problems

- [Jump Game II](/problems/greedy-jump-game-ii)
- [Jump Game III](/problems/jump-game-iii)
- [Jump Game VI](/problems/jump-game-vi)

<FeedbackWidget problem-slug="jump-game" />

<RelatedProblems problems="non-overlapping-intervals::Non Overlapping Intervals|gas-station::Gas Station|best-time-to-buy-and-sell-stock::Best Time To Buy And Sell Stock" />
