# Sliding Window — Maximum Average Subarray I

*[↗ LeetCode: Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/sliding-window)

Max average of any contiguous subarray of length `k`.

---

## Approach 1 — Fixed-window running sum
Max sum ÷ k; sliding sum of window k.



```java
double findMaxAverage(int[] nums, int k) {
    int sum = 0;
    for (int i = 0; i < k; i++) sum += nums[i];
    int best = sum;
    for (int i = k; i < nums.length; i++) {
        sum += nums[i] - nums[i - k];
        best = Math.max(best, sum);
    }
    return best / (double) k;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Fixed-window running sum | O(n) | O(1) | primary |

## When to use which

- **Ship this** → Fixed-window running sum (O(n), O(1)). The pattern's standard solution.

## Related problems

- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) — deque
- [Diet Plan Performance](/problems/diet-plan-performance)
