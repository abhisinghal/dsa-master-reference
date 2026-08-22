# Prefix Sum — Subarray Sums Divisible by K

*[↗ LeetCode: Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

Count contiguous subarrays whose sum is divisible by `k`.

**Example** — `nums=[4,5,0,-2,-3,1], k=5` → `7`

---

## Approach 1 — Prefix mod + hash map
**Insight.** Subarray sum divisible by k iff `P[j] ≡ P[i] (mod k)`. Count prefix-remainders; matches with each other = valid subarrays.

**Trap.** For negatives, use `((prefix % k) + k) % k` for positive modulo.



```java
int subarraysDivByK(int[] nums, int k) {
    Map<Integer, Integer> cnt = new HashMap<>();
    cnt.put(0, 1);
    int prefix = 0, ans = 0;
    for (int x : nums) {
        prefix = ((prefix + x) % k + k) % k;
        ans += cnt.getOrDefault(prefix, 0);
        cnt.merge(prefix, 1, Integer::sum);
    }
    return ans;
}
```




<CodeTrace
  title="Prefix mod + hash map"
  :values="['4', '5', '0', '-2', '-3', '1']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize; scan begins." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through the scan." },
    { pointers: { i: 5 }, vars: { phase: "done" }, note: "All positions considered — return the answer." }
  ]'
/>


<CodeTrace
  title="Prefix mod — nums=[4,5,0,-2,-3,1], k=5"
  :values="[4,5,0,-2,-3,1]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { prefix: 4, ans: 0, cnt: "{0:1,4:1}" }, note: "prefix mod 5 = 4" },
    { pointers: { i: 1 }, vars: { prefix: 4, ans: 1, cnt: "{0:1,4:2}" }, note: "seen 4 already → +1" },
    { pointers: { i: 4 }, vars: { prefix: 4, ans: 4, cnt: "{...4:3}" }, note: "3 pairs so far", added: [1,3,4] },
    { pointers: { i: 5 }, vars: { prefix: 0, ans: 7 }, note: "seen[0]=1+more → final 7" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(k)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Prefix mod + hash map | O(n) | O(k) | primary |

## When to use which

- **Ship this** → Prefix mod + hash map (O(n), O(k)). The pattern's standard solution.

## Related problems

- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k) — sibling with exact match
- [Continuous Subarray Sum](/problems/continuous-subarray-sum)
- [Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/)
