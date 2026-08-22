# Greedy — Jump Game III

*[↗ LeetCode: Jump Game III](https://leetcode.com/problems/jump-game-iii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/bfs)

From index `start`, you may jump `i ± arr[i]`. Can you reach any zero?

&gt; Filed under Greedy in the curriculum, but the natural solution is BFS/DFS on an implicit graph — there's nothing "greedy" to exploit.

## Approach — BFS from start



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



**Complexity** — Time **O(n)**; Space **O(n)**.

## Related problems

- [Jump Game IV](https://leetcode.com/problems/jump-game-iv/) — same-value edges → BFS with "process all same-value neighbors and clear"
- [Minimum Jumps to Reach Home](https://leetcode.com/problems/minimum-jumps-to-reach-home/) — bounded BFS
