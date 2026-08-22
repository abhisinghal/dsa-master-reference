# Prefix Sum — Contiguous Array

*[↗ LeetCode: Contiguous Array](https://leetcode.com/problems/contiguous-array/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

Return the length of the longest contiguous subarray with equal 0s and 1s.

**Example** — `nums=[0,1,0]` → `2`

## Approach — Map 0→-1, then prefix sum

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



**Complexity** — Time **O(n)**; Space **O(n)**.

## Related problems

- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k)
- [Subarray Sums Divisible by K](/problems/subarray-sums-divisible-by-k)
