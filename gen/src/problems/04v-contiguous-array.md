# Prefix Sum — Contiguous Array

*[↗ LeetCode: Contiguous Array](https://leetcode.com/problems/contiguous-array/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

Return the length of the longest contiguous subarray with equal 0s and 1s.

**Example** — `nums=[0,1,0]` → `2`

---

## Approach 1 — Map 0→-1, then prefix sum
**Insight.** Treating 0 as -1 makes "equal 0s and 1s" equivalent to "subarray sum = 0". First occurrence of each prefix value → longest subarray with the same prefix.

```java
int findMaxLength(int[] nums) {
    Map<Integer, Integer> first = new HashMap<>();
    first.put(0, -1);
    int prefix = 0, best = 0;
    for (int i = 0; i < nums.length; i++) {
        prefix += nums[i] == 0 ? -1 : 1;
        if (first.containsKey(prefix))
            best = Math.max(best, i - first.get(prefix));
        else
            first.put(prefix, i);
    }
    return best;
}
```


<CodeTrace
  title="Map 0→-1, then prefix sum"
  :values="['0', '1', '0']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize; scan begins." },
    { pointers: { i: 0 }, vars: { phase: "midway" }, note: "Midway through the scan." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "All positions considered — return the answer." }
  ]'
/>


**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Map 0→-1, then prefix sum | O(n) | O(n) | primary |

## When to use which

- **Ship this** → Map 0→-1, then prefix sum (O(n), O(n)). The pattern's standard solution.

## Related problems

- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k)
- [Subarray Sums Divisible by K](/problems/subarray-sums-divisible-by-k)
