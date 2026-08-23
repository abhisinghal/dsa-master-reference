# Prefix Sum — Subarray Sum Equals K

*[↗ LeetCode: Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

&lt;CompanyTags companies="Meta, Amazon, Google, Bloomberg" /&gt;

Given an integer array `nums` (may contain negatives) and integer `k`, return the number of **contiguous subarrays** whose sum equals `k`.

**Example 1** — `nums = [1,1,1], k = 2` → `2` (the two `[1,1]` subarrays)
**Example 2** — `nums = [1,2,3], k = 3` → `2` (`[1,2]` and `[3]`)
**Example 3** — `nums = [1,-1,0], k = 0` → `3` (`[1,-1]`, `[0]`, `[1,-1,0]`)

**Constraints** — `1 ≤ n ≤ 2·10⁴`; `-10³ ≤ nums[i] ≤ 10³`.


&lt;Hints
  hint1="Ask: can I answer `sum(i, j)` in O(1) given a preprocessed structure?"
  hint2="Prefix sums let you compute range sums as `pref[j+1] - pref[i]`. For ’count subarrays with property X on sum’, use a hash-map of prefix sums."
  hint3="For ’≥ 2 length’ or ’divisible by k’ variants, store first occurrence and check remainders."
/&gt;
---

## Approach 1 — Brute force (all subarrays)

**Intuition.** Enumerate every subarray `[i..j]`; sum it; count those equal to `k`.



```java
int subarraySumBrute(int[] nums, int k) {
    int count = 0, n = nums.length;
    for (int i = 0; i < n; i++) {
        int s = 0;
        for (int j = i; j < n; j++) {
            s += nums[j];
            if (s == k) count++;
        }
    }
    return count;
}
```



<CodeTrace
  title="Brute — nums=[1,1,1], k=2: enumerate all 6 subarrays"
  :values="[1,1,1]"
  :windowKeys="['i','j']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0, j: 0 }, vars: { s: 1, count: 0 }, note: "[1] sum 1 ≠ 2" },
    { pointers: { i: 0, j: 1 }, vars: { s: 2, count: 1 }, note: "[1,1] sum 2 → +1", added: [0,1] },
    { pointers: { i: 0, j: 2 }, vars: { s: 3, count: 1 }, note: "[1,1,1] sum 3" },
    { pointers: { i: 1, j: 2 }, vars: { s: 2, count: 2 }, note: "[1,1] sum 2 → +1", added: [1,2] },
    { pointers: { i: 2, j: 2 }, vars: { s: 1, count: 2 }, note: "[1] sum 1. final = 2" }
  ]'
/>

**Complexity** — Time **O(n²)** with the running sum trick; **O(n³)** without; Space **O(1)**.

---

## Approach 2 — Prefix sums (still O(n²), but sets up the optimization)

**Insight from brute.** If `P[i]` = sum of `nums[0..i-1]`, then `sum(nums[i..j]) = P[j+1] - P[i]`. The brute-force question becomes: *how many prefix pairs `(a, b)` have `P[b] - P[a] = k`?*



```java
int subarraySumPrefix(int[] nums, int k) {
    int n = nums.length, count = 0;
    int[] P = new int[n + 1];
    for (int i = 0; i < n; i++) P[i + 1] = P[i] + nums[i];
    for (int a = 0; a <= n; a++)
        for (int b = a + 1; b <= n; b++)
            if (P[b] - P[a] == k) count++;
    return count;
}
```



Not better asymptotically, but the reframing enables Approach 3.

---

## Approach 3 — Prefix sums + hash map (one pass)

**Insight from prefix.** For each running prefix `P[j]`, the question "how many earlier prefixes `P[i]` satisfy `P[j] − P[i] = k`?" is equivalent to "how many earlier prefixes equal `P[j] − k`?" — an O(1) hash lookup.

Seed the map with `{0: 1}` so a prefix that itself equals `k` counts as one subarray (from index 0).

**Trap.** Don't return the *number of prefix values* seen — return the *count of times each prefix value was seen*, because two different starts can produce the same prefix.



```java
int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> count = new HashMap<>();
    count.put(0, 1);
    int prefix = 0, ans = 0;
    for (int x : nums) {
        prefix += x;
        ans += count.getOrDefault(prefix - k, 0);
        count.merge(prefix, 1, Integer::sum);
    }
    return ans;
}
```



<CodeTrace
  title="Prefix + hash map — nums=[1,1,1], k=2"
  :values="[1,1,1]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { prefix: 1, "need prefix-k": -1, count: 0, seen: "{0:1, 1:1}" }, note: "seen[-1]=0 miss" },
    { pointers: { i: 1 }, vars: { prefix: 2, "need prefix-k": 0, count: 1, seen: "{0:1, 1:1, 2:1}" }, note: "seen[0]=1 → +1", added: [0,1] },
    { pointers: { i: 2 }, vars: { prefix: 3, "need prefix-k": 1, count: 2, seen: "{0:1, 1:1, 2:1, 3:1}" }, note: "seen[1]=1 → +1. total = 2", added: [1,2] }
  ]'
/>

**Complexity** — Time **O(n)** amortized; Space **O(n)** for the map. Optimal.

---

## Try it yourself

<JavaRunner problem-slug="prefix-sum-subarray-sum-equals-k" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(1) |
| Prefix sum only | O(n²) | O(n) |
| Prefix + hash map | **O(n)** | O(n) |

## When to use which

- **Cold interview** → walk brute → prefix reframing → hash map.
- **Interviewer probes "what if all values are positive?"** → sliding window would work in O(n), O(1) space. But **negatives break sliding window** — this is why hash-map prefix is the general answer.

&lt;AiCompanion problem-slug="prefix-sum-subarray-sum-equals-k" pattern-hint="prefix sum" /&gt;

## Related problems (same ladder applies)

- [Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k/) — hash `prefix % k`
- [Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum/) — same but requires length ≥ 2
- [Contiguous Array](https://leetcode.com/problems/contiguous-array/) — map 0→-1, then it's "sum equals 0"
- [Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/) — same skeleton

&lt;FeedbackWidget problem-slug="prefix-sum-subarray-sum-equals-k" /&gt;
