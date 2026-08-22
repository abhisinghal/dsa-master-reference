# Sliding Window — Diet Plan Performance

*[↗ LeetCode: Diet Plan Performance](https://leetcode.com/problems/diet-plan-performance/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/sliding-window)

Fixed window of size `k` over calories. For each window: +1 if sum > upper; −1 if sum < lower; 0 otherwise. Return total.

---

## Approach 1 — Fixed-size window
**Insight.** Standard fixed-size sum window: pre-sum first k, then slide adding right and subtracting left.

```java
int dietPlanPerformance(int[] cal, int k, int lower, int upper) {
    int sum = 0;
    for (int i = 0; i < k; i++) sum += cal[i];
    int score = 0;
    if (sum > upper) score++;
    else if (sum < lower) score--;
    for (int i = k; i < cal.length; i++) {
        sum += cal[i] - cal[i - k];
        if (sum > upper) score++;
        else if (sum < lower) score--;
    }
    return score;
}
```

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Fixed-size window | O(n) | O(1) | primary |

## When to use which

- **Ship this** → Fixed-size window (O(n), O(1)). The pattern's standard solution.

## Related problems

- [Maximum Average Subarray I](/problems/maximum-average-subarray-i)
- [Minimum Size Subarray Sum](/problems/minimum-size-subarray-sum) — variable window
