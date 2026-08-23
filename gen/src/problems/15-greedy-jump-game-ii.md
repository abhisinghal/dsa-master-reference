# Greedy — Jump Game II

*[↗ LeetCode: Jump Game II](https://leetcode.com/problems/jump-game-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg" />

Given `nums[i]` = max jump length from index `i`, return the **minimum jumps** to reach the last index. Guaranteed reachable.

**Example 1** — `[2,3,1,1,4]` → `2` (`0 → 1 → 4`)
**Example 2** — `[2,3,0,1,4]` → `2`

**Constraints** — `1 ≤ n ≤ 10⁴`; `0 ≤ nums[i] ≤ 1000`.


<Hints
  hint1="Is there a local rule that provably gives global optimum? (Exchange argument.)"
  hint2="Sort by the greedy criterion (deadline / end / cost). Iterate; make the locally best choice."
  hint3="If greedy fails, DP is likely needed. But prove greedy’s correctness before writing it."
/>
---

<MarkSolved problem-slug="greedy-jump-game-ii" /> <Bookmark problem-slug="greedy-jump-game-ii" />

<InterviewTimer problem-slug="greedy-jump-game-ii" />



## Approach 1 — BFS (level = jump count)

**Intuition.** Model the problem as BFS: each index is a node with edges to `[i+1, i+nums[i]]`. Level of last index = min jumps.

```java
int jumpBFS(int[] a) {
    int n = a.length;
    if (n <= 1) return 0;
    boolean[] seen = new boolean[n];
    Deque<Integer> q = new ArrayDeque<>();
    q.offer(0); seen[0] = true;
    int level = 0;
    while (!q.isEmpty()) {
        level++;
        for (int i = q.size(); i > 0; i--) {
            int u = q.poll();
            for (int v = u + 1; v <= Math.min(u + a[u], n - 1); v++) {
                if (v == n - 1) return level;
                if (!seen[v]) { seen[v] = true; q.offer(v); }
            }
        }
    }
    return -1;
}
```

**Complexity** — Time **O(n²)** worst-case; Space **O(n)**.

---

## Approach 2 — DP (min jumps from each index)

**Intuition.** `dp[i]` = min jumps to reach `n-1` from `i`. `dp[n-1] = 0`; `dp[i] = 1 + min(dp[i+1..i+a[i]])`. Fill right to left.

```java
int jumpDP(int[] a) {
    int n = a.length;
    int[] dp = new int[n];
    Arrays.fill(dp, Integer.MAX_VALUE);
    dp[n - 1] = 0;
    for (int i = n - 2; i >= 0; i--)
        for (int j = i + 1; j <= Math.min(i + a[i], n - 1); j++)
            if (dp[j] != Integer.MAX_VALUE) dp[i] = Math.min(dp[i], dp[j] + 1);
    return dp[0];
}
```

**Complexity** — Time **O(n²)**; Space **O(n)**.

---

## Approach 3 — Greedy (frontier expansion)

**Insight from DP.** Because all edges have weight 1, BFS's "levels" have a very simple shape — we just need to know **how far each level reaches**. Track `farthest` (best reach considering all indices in the current level). When we hit `end` (level boundary), commit a jump and set `end = farthest`.

**Trap.** Commit `jumps++` when `i == end`, not on every scan step.

```java
int jump(int[] a) {
    int end = 0, farthest = 0, jumps = 0;
    for (int i = 0; i < a.length - 1; i++) {
        farthest = Math.max(farthest, i + a[i]);
        if (i == end) { jumps++; end = farthest; }
    }
    return jumps;
}
```

<CodeTrace
  title="Greedy frontier — nums=[2,3,1,1,4]"
  :values="[2,3,1,1,4]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { end: 0, farthest: 2, jumps: 0 }, note: "start. reach from 0 is 2" },
    { pointers: { i: 1 }, vars: { end: 2, farthest: 4, jumps: 1 }, note: "i==end → commit; window [1,2] best reach=4", added: [1] },
    { pointers: { i: 2 }, vars: { end: 2, farthest: 4, jumps: 1 }, note: "no better" },
    { pointers: { i: 3 }, vars: { end: 4, farthest: 4, jumps: 2 }, note: "i==end → commit → reach idx 4. return 2", added: [4] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. Optimal.

---

## Try it yourself

<JavaRunner problem-slug="greedy-jump-game-ii" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| BFS | O(n²) | O(n) |
| DP right-to-left | O(n²) | O(n) |
| Greedy frontier | **O(n)** | O(1) |

## When to use which

- **Cold interview** → walk BFS → greedy. Show the "levels shape enables O(1)" insight.
- **Interviewer wants a proof** → BFS gives you the shortest-path guarantee; greedy is a tighter special case.

<AiCompanion problem-slug="greedy-jump-game-ii" pattern-hint="greedy" />

## Related problems (same ladder applies)

- [Jump Game I](https://leetcode.com/problems/jump-game/) — reachability instead of min jumps
- [Jump Game III](https://leetcode.com/problems/jump-game-iii/) — BFS with two edges per node
- [Video Stitching](https://leetcode.com/problems/video-stitching/) — same greedy frontier expansion
- [Minimum Number of Taps to Open](https://leetcode.com/problems/minimum-number-of-taps-to-open-to-water-a-garden/) — reframe intervals → same greedy

<FeedbackWidget problem-slug="greedy-jump-game-ii" />
