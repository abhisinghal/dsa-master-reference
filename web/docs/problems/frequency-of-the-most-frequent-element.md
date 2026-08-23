# Sliding Window — Frequency of the Most Frequent Element

*[↗ LeetCode: Frequency of the Most Frequent Element](https://leetcode.com/problems/frequency-of-the-most-frequent-element/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Given nums and budget `k` (increments allowed), max frequency of any single value after operations.

**Example 1** — `nums=[1,2,4], k=5` → `3` (raise 1,2,4 to 4 → cost 3+2=5)
**Example 2** — `nums=[1,4,8,13], k=5` → `2`

**Constraints** — `1 ≤ n ≤ 10⁵`; `1 ≤ k ≤ 10⁵`.

---

## Approach — Sort + sliding window with sum budget (canonical)

**Insight.** Sort. In window `[l, r]` of sorted nums, raising every value to `nums[r]` costs `nums[r] * (r-l+1) - windowSum`. Extend r; while cost &gt; k, shrink l.



```java
int maxFrequency(int[] nums, int k) {
    Arrays.sort(nums);
    long sum = 0;
    int l = 0, best = 0;
    for (int r = 0; r < nums.length; r++) {
        sum += nums[r];
        while ((long) nums[r] * (r - l + 1) - sum > k) sum -= nums[l++];
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```



<CodeTrace
  title="Sort + budget window — nums=[1,2,4], k=5"
  :values="['1','2','4']"
  :windowKeys="['l','r']"
  :cellWidth="34"
  :steps='[
    { pointers: { l: 0, r: 0 }, vars: { sum: 1, cost: 0 }, note: "" },
    { pointers: { l: 0, r: 2 }, vars: { sum: 7, cost: 5, best: 3 }, note: "3 elems → 4·3 − 7 = 5 ≤ k → best=3" }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort + sliding budget | **O(n log n)** | O(1) | canonical |

## When to use which

- **Sorted + monotone cost function** → sliding budget.
- **Decrement instead of increment** → symmetric; sort and use different cost formula.
- **Multiple target values** → try each value as target with 2p.

## Related problems

- [Longest Repeating Character Replacement](/problems/longest-repeating-character-replacement)
- [Minimum Operations to Reduce X to Zero](https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/)
- [Max Consecutive Ones III](/problems/max-consecutive-ones-iii)
