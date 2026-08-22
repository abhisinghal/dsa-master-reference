# DP — House Robber II

*[↗ LeetCode: House Robber II](https://leetcode.com/problems/house-robber-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Same as House Robber but houses are in a **circle** — first and last are adjacent.

---

## Approach 1 — Two linear runs
**Insight.** Because rob(first) forbids rob(last), the optimum is either "consider houses[0..n-2]" or "houses[1..n-1]". Both are linear house robber → max of the two.



```java
int rob(int[] nums) {
    int n = nums.length;
    if (n == 1) return nums[0];
    return Math.max(linear(nums, 0, n - 2), linear(nums, 1, n - 1));
}
int linear(int[] nums, int lo, int hi) {
    int prev = 0, curr = 0;
    for (int i = lo; i <= hi; i++) {
        int t = Math.max(curr, prev + nums[i]);
        prev = curr; curr = t;
    }
    return curr;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Two linear runs | O(n) | O(1) | primary |

## When to use which

- **Ship this** → Two linear runs (O(n), O(1)). The pattern's standard solution.

## Related problems

- [House Robber](/problems/dp-house-robber) — flagship
- [House Robber III](https://leetcode.com/problems/house-robber-iii/) — tree DP
- [Delete and Earn](/problems/delete-and-earn) — reduction to House Robber
