# DP — House Robber II

*[↗ LeetCode: House Robber II](https://leetcode.com/problems/house-robber-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

Houses in a **circle** — first and last adjacent. Max rob without adjacent.

**Example 1** — `nums=[2,3,2]` → `3`
**Example 2** — `nums=[1,2,3,1]` → `4`

**Constraints** — `1 ≤ n ≤ 100`.

---

## Approach — Two linear runs (canonical)

**Insight.** rob(first) forbids rob(last). Optimum = max of two subarrays: `[0..n-2]` and `[1..n-1]`.

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

| Approach | Time | Space | Grade |
|---|---|---|---|
| Two linear runs | **O(n)** | O(1) | canonical |

## When to use which

- **Circular house robber** → this.
- **Linear** → [House Robber](/problems/dp-house-robber).
- **Tree** → [House Robber III](https://leetcode.com/problems/house-robber-iii/).

## Related problems

- [House Robber](/problems/dp-house-robber)
- [Delete and Earn](/problems/delete-and-earn)
