# Prefix Sum — Continuous Subarray Sum

*[↗ LeetCode: Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

Return `true` iff there's a subarray of size ≥ 2 with sum divisible by `k`.

**Example** — `nums=[23,2,4,6,7], k=6` → `true` (`[2,4]`)

---

## Approach 1 — Prefix mod, track FIRST index
**Insight.** `sum(i..j) % k == 0 ↔ prefix[j] ≡ prefix[i-1] (mod k)`. Store the first index a remainder appeared; if seen again with `j - i ≥ 2`, return true.

**Trap.** Store index of FIRST occurrence (not last) so subarray length is maximized.



```java
boolean checkSubarraySum(int[] nums, int k) {
    Map<Integer, Integer> first = new HashMap<>();
    first.put(0, -1);
    int prefix = 0;
    for (int i = 0; i < nums.length; i++) {
        prefix = (prefix + nums[i]) % k;
        if (first.containsKey(prefix)) {
            if (i - first.get(prefix) >= 2) return true;
        } else first.put(prefix, i);
    }
    return false;
}
```




<CodeTrace
  title="Prefix mod, track FIRST index"
  :values="['23', '2', '4', '6', '7']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize; scan begins." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through the scan." },
    { pointers: { i: 4 }, vars: { phase: "done" }, note: "All positions considered — return the answer." }
  ]'
/>


**Complexity** — Time **O(n)**; Space **O(k)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Prefix mod, track FIRST index | O(n) | O(k) | primary |

## When to use which

- **Ship this** → Prefix mod, track FIRST index (O(n), O(k)). The pattern's standard solution.

## Related problems

- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k)
- [Subarray Sums Divisible by K](/problems/subarray-sums-divisible-by-k)
- [Contiguous Array](/problems/contiguous-array)
