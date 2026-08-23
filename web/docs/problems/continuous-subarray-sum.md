# Prefix Sum — Continuous Subarray Sum

*[↗ LeetCode: Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

&lt;CompanyTags companies="Meta, Amazon, Google" /&gt;

Return true iff there is a subarray of length **≥ 2** whose sum is a multiple of `k`.

**Example 1** — `nums = [23,2,4,6,7], k = 6` → `true` (subarray `[2,4]`)
**Example 2** — `nums = [23,2,6,4,7], k = 6` → `true`
**Example 3** — `nums = [1,0], k = 2` → `false`

**Constraints** — `1 ≤ n ≤ 10⁵`; `0 ≤ nums[i] ≤ 10⁹`; `1 ≤ k ≤ 2³¹−1`.


&lt;Hints
  hint1="Ask: can I answer `sum(i, j)` in O(1) given a preprocessed structure?"
  hint2="Prefix sums let you compute range sums as `pref[j+1] - pref[i]`. For ’count subarrays with property X on sum’, use a hash-map of prefix sums."
  hint3="For ’≥ 2 length’ or ’divisible by k’ variants, store first occurrence and check remainders."
/&gt;
---

&lt;MarkSolved problem-slug="continuous-subarray-sum" /&gt;

&lt;InterviewTimer problem-slug="continuous-subarray-sum" /&gt;



## Approach 1 — Every subarray

O(n²). Baseline.

## Approach 2 — Prefix mod + first-index map (with length guard)

**Insight.** If two prefix sums have same remainder mod k AND the distance is ≥ 2, we win. Store first index of each remainder.

**Trap** — treat prefix at index `-1` as `0` (multiple of k). Also handle `k = 0` (subarray must sum to 0).



```java
boolean checkSubarraySum(int[] nums, int k) {
    Map<Integer, Integer> first = new HashMap<>();
    first.put(0, -1);
    int pref = 0;
    for (int i = 0; i < nums.length; i++) {
        pref += nums[i];
        int m = k == 0 ? pref : pref % k;
        if (first.containsKey(m)) {
            if (i - first.get(m) >= 2) return true;
        } else first.put(m, i);
    }
    return false;
}
```



<CodeTrace
  title="Prefix mod — nums=[23,2,4,6,7], k=6"
  :values="['23','2','4','6','7']"
  :windowKeys="['i']"
  :cellWidth="30"
  :steps='[
    { pointers: { i: 0 }, vars: { pref: 23, m: 5, first: "{5:0}" }, note: "" },
    { pointers: { i: 1 }, vars: { pref: 25, m: 1, first: "{5:0,1:1}" }, note: "new remainder" },
    { pointers: { i: 2 }, vars: { pref: 29, m: 5 }, note: "m=5 first at 0; distance=2 → return true" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(k)**.

---

## Try it yourself

<JavaRunner problem-slug="continuous-subarray-sum" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute | O(n²) | O(1) | baseline |
| Prefix mod + first-index | **O(n)** | O(k) | optimum |

## When to use which

- **"Length ≥ 2" constraint** → keep **first** index (not most recent) to maximize gap.
- **"Length ≥ L"** → same, check `i - first ≥ L`.
- **"Any sum divisible by k" (no length)** → simpler [Subarray Sums Divisible by K](/problems/subarray-sums-divisible-by-k).

&lt;AiCompanion problem-slug="continuous-subarray-sum" pattern-hint="prefix sum" /&gt;

## Related problems

- [Subarray Sums Divisible by K](/problems/subarray-sums-divisible-by-k)
- [Contiguous Array](/problems/contiguous-array)
- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k)

&lt;FeedbackWidget problem-slug="continuous-subarray-sum" /&gt;

&lt;RelatedProblems problems="contiguous-array::Contiguous Array|car-pooling::Car Pooling|range-addition::Range Addition" /&gt;
