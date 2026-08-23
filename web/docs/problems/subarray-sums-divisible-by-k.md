# Prefix Sum — Subarray Sums Divisible by K

*[↗ LeetCode: Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

<CompanyTags companies="Google, Amazon" />

Count subarrays whose sum is divisible by `k`.

**Example 1** — `nums = [4,5,0,-2,-3,1], k = 5` → `7`
**Example 2** — `nums = [5], k = 9` → `0`
**Example 3** — `nums = [-1,2,9], k = 2` → `2`

**Constraints** — `1 ≤ n ≤ 3·10⁴`; `2 ≤ k ≤ 10⁴`.


<Hints
  hint1="Ask: can I answer `sum(i, j)` in O(1) given a preprocessed structure?"
  hint2="Prefix sums let you compute range sums as `pref[j+1] - pref[i]`. For ’count subarrays with property X on sum’, use a hash-map of prefix sums."
  hint3="For ’≥ 2 length’ or ’divisible by k’ variants, store first occurrence and check remainders."
/>
---

<MarkSolved problem-slug="subarray-sums-divisible-by-k" /> <Bookmark problem-slug="subarray-sums-divisible-by-k" />

<InterviewTimer problem-slug="subarray-sums-divisible-by-k" />



## Approach 1 — Every subarray

O(n²) sums. Baseline.

## Approach 2 — Prefix sum modulo k with hash map

**Insight.** Two prefix sums with the same remainder mod k → their difference is divisible by k. Count pairs of prefixes sharing each remainder.

**Trap** — Java `%` can be negative. Use `((sum % k) + k) % k`.



```java
int subarraysDivByK(int[] nums, int k) {
    Map<Integer, Integer> cnt = new HashMap<>();
    cnt.put(0, 1);
    int pref = 0, res = 0;
    for (int x : nums) {
        pref += x;
        int m = ((pref % k) + k) % k;
        res += cnt.getOrDefault(m, 0);
        cnt.merge(m, 1, Integer::sum);
    }
    return res;
}
```



<CodeTrace
  title="Prefix mod k — nums=[4,5,0,-2,-3,1], k=5"
  :values="['4','5','0','-2','-3','1']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { pref: 4, m: 4, cnt: "{0:1,4:1}", res: 0 }, note: "first prefix" },
    { pointers: { i: 1 }, vars: { pref: 9, m: 4, res: 1 }, note: "same m=4 → +1 pair" },
    { pointers: { i: 4 }, vars: { pref: 4, m: 4, res: 5 }, note: "several matches accumulate" },
    { pointers: { i: 5 }, vars: { pref: 5, m: 0, res: 7 }, note: "final 7" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(k)**.

---

## Try it yourself

<JavaRunner problem-slug="subarray-sums-divisible-by-k" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute | O(n²) | O(1) | baseline |
| Prefix mod + map | **O(n)** | O(k) | optimum |

## When to use which

- **"Sum divisible by k"** → prefix mod + hash map (initialise with `{0:1}`).
- **Negatives possible** → the `((% + k) % k)` normalization is required.
- **"Longest / shortest such subarray"** → change map to store first-index; take max/min index difference.

<AiCompanion problem-slug="subarray-sums-divisible-by-k" pattern-hint="prefix sum" />

## Related problems

- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k)
- [Continuous Subarray Sum](/problems/continuous-subarray-sum) — sum multiple of k with length ≥ 2
- [Contiguous Array](/problems/contiguous-array) — same modulo trick with +1/−1

<FeedbackWidget problem-slug="subarray-sums-divisible-by-k" />

<RelatedProblems problems="prefix-sum-subarray-sum-equals-k::Prefix Sum Subarray Sum Equals K|continuous-subarray-sum::Continuous Subarray Sum|car-pooling::Car Pooling" />
