# Greedy — Jump Game

*[↗ LeetCode: Jump Game](https://leetcode.com/problems/jump-game/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

`nums[i]` = max jump length from `i`. Can we reach the last index?

## Approach 1 — DP reachable[i]

O(n²). Too slow for large inputs.

## Approach 2 — Greedy farthest reachable

**Insight.** Track `maxReach`. At index `i`, if `i > maxReach` we're stuck. Else update `maxReach = max(maxReach, i + nums[i])`.

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

**Complexity** — Time **O(n)**; Space **O(1)**.

## Related problems

- [Jump Game II](/problems/greedy-jump-game-ii) — minimum jumps (BFS layers)
- [Jump Game III](/problems/jump-game-iii) — arbitrary graph BFS
- [Jump Game VI](/problems/jump-game-vi) — DP with deque
