# Sliding Window — Max Consecutive Ones III

*[↗ LeetCode: Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Longest subarray of 1s where at most `k` zeros can be flipped.

---

## Approach 1 — Variable window bounded by zero count
**Insight.** Window is valid iff it contains ≤ k zeros. Extend r; when zero count exceeds k, shrink from l.



```java
int longestOnes(int[] nums, int k) {
    int l = 0, zeros = 0, best = 0;
    for (int r = 0; r < nums.length; r++) {
        if (nums[r] == 0) zeros++;
        while (zeros > k) {
            if (nums[l++] == 0) zeros--;
        }
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```



**"Never shrink" variant.** For a *maximum-length* answer, we can replace the `while` with an `if`: window never shrinks below its best; `best` = size of the window at the end. Same `O(n)`, simpler.

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Variable window bounded by zero count | O(n) | O(1) | primary |

## When to use which

- **Ship this** → Variable window bounded by zero count (O(n), O(1)). The pattern's standard solution.

## Related problems

- [Longest Subarray of 1's After Deleting One Element](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/) — k=1 with deletion
- [Fruit Into Baskets](/problems/fruit-into-baskets)
