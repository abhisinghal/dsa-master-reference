# Greedy — Jump Game III

*[↗ LeetCode: Jump Game III](https://leetcode.com/problems/jump-game-iii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/bfs)

<CompanyTags companies="Amazon, Google, Meta" />

From index `start`, you may jump `i ± arr[i]`. Return true iff you can reach any zero.

**Example 1** — `arr=[4,2,3,0,3,1,2], start=5` → `true`
**Example 2** — `arr=[4,2,3,0,3,1,2], start=0` → `true`
**Example 3** — `arr=[3,0,2,1,2], start=2` → `false`

**Constraints** — `1 ≤ n ≤ 5·10⁴`; `0 ≤ arr[i] < n`.


<Hints
  hint1="Is there a local rule that provably gives global optimum? (Exchange argument.)"
  hint2="Sort by the greedy criterion (deadline / end / cost). Iterate; make the locally best choice."
  hint3="If greedy fails, DP is likely needed. But prove greedy’s correctness before writing it."
/>
---

## Approach 1 — DFS/BFS on implicit graph (canonical)

Model each index as a node with 2 edges. BFS from start; return true on reaching a zero.

```java
boolean canReach(int[] arr, int start) {
    Queue<Integer> q = new ArrayDeque<>();
    boolean[] seen = new boolean[arr.length];
    q.add(start); seen[start] = true;
    while (!q.isEmpty()) {
        int i = q.poll();
        if (arr[i] == 0) return true;
        for (int j : new int[]{i + arr[i], i - arr[i]})
            if (j >= 0 && j < arr.length && !seen[j]) { seen[j] = true; q.add(j); }
    }
    return false;
}
```

<CodeTrace
  title="DFS/BFS on implicit graph (canonical)"
  :values="['4', '2', '3', '0', '3', '1', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 3 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 6 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="jump-game-iii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| BFS | **O(n)** | O(n) | canonical |

## When to use which

- **Reachability** → BFS/DFS.
- **Min steps to zero** → same BFS, count layers.
- **"Same-value edges"** → [Jump Game IV](https://leetcode.com/problems/jump-game-iv/).

<AiCompanion problem-slug="jump-game-iii" pattern-hint="greedy" />

## Related problems

- [Jump Game](/problems/jump-game)
- [Jump Game IV](https://leetcode.com/problems/jump-game-iv/)
- [Minimum Jumps to Reach Home](https://leetcode.com/problems/minimum-jumps-to-reach-home/)