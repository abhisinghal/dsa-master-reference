# Sliding Window — Maximum Average Subarray I

*[↗ LeetCode: Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/sliding-window)

Return the max average of any contiguous subarray of length exactly `k`.

**Example 1** — `nums=[1,12,-5,-6,50,3], k=4` → `12.75`
**Example 2** — `nums=[5], k=1` → `5.0`

**Constraints** — `1 ≤ k ≤ n ≤ 10⁵`.

---

## Approach — Fixed-window running sum (canonical)

**Insight.** Max avg = max sum ÷ k over any size-k window.

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

<CodeTrace
  title="Fixed window — nums=[1,12,-5,-6,50,3], k=4"
  :values="['1','12','-5','-6','50','3']"
  :windowKeys="['left','right']"
  :cellWidth="30"
  :steps='[
    { pointers: { left: 0, right: 3 }, vars: { sum: 2, best: 2 }, note: "first window" },
    { pointers: { left: 1, right: 4 }, vars: { sum: 51, best: 51 }, note: "slide right → biggest sum" },
    { pointers: { left: 2, right: 5 }, vars: { sum: 42, best: 51 }, note: "final; avg = 51/4 = 12.75" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Fixed window | **O(n)** | O(1) | canonical |

## When to use which

- **Fixed size k, sum-based metric** → sliding sum.
- **Variable size** → constrained window (see [Minimum Size Subarray Sum](/problems/minimum-size-subarray-sum)).
- **Max avg with size ≥ k** → binary search on answer.

## Related problems

- [Diet Plan Performance](/problems/diet-plan-performance)
- [Maximum Average Subarray II](https://leetcode.com/problems/maximum-average-subarray-ii/)
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)
