# Prefix Sum — Contiguous Array

*[↗ LeetCode: Contiguous Array](https://leetcode.com/problems/contiguous-array/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

<CompanyTags companies="Meta, Amazon, Google" />

Given binary array `nums`, return the length of the longest subarray with equal numbers of 0s and 1s.

**Example 1** — `nums = [0,1]` → `2`
**Example 2** — `nums = [0,1,0]` → `2`
**Example 3** — `nums = [0,0,1,1,0]` → `4`

**Constraints** — `1 ≤ n ≤ 10⁵`; `nums[i] ∈ {0,1}`. Brute is O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Rewrite as prefix-sum with 0/1→−1/+1, hashmap of first-seen index → O(n) = 10⁵ ops.
<Hints
  hint1="Ask: can I answer `sum(i, j)` in O(1) given a preprocessed structure?"
  hint2="Prefix sums let you compute range sums as `pref[j+1] - pref[i]`. For ’count subarrays with property X on sum’, use a hash-map of prefix sums."
  hint3="For ’≥ 2 length’ or ’divisible by k’ variants, store first occurrence and check remainders."
/>
---

<MarkSolved problem-slug="contiguous-array" /> <Bookmark problem-slug="contiguous-array" />

<InterviewTimer problem-slug="contiguous-array" />



## Approach 1 — Every subarray

O(n²). Baseline.

## Approach 2 — Map 0 → −1; prefix-sum with earliest-index map

**Insight.** Replace 0 with −1. Equal counts of 0/1 iff running sum returns to a prior value. Store **first occurrence** of each prefix sum; on revisit, subarray length = `i - firstIndex`.

```java
int findMaxLength(int[] nums) {
    Map<Integer, Integer> first = new HashMap<>();
    first.put(0, -1);
    int sum = 0, best = 0;
    for (int i = 0; i < nums.length; i++) {
        sum += (nums[i] == 0) ? -1 : 1;
        if (first.containsKey(sum)) best = Math.max(best, i - first.get(sum));
        else first.put(sum, i);
    }
    return best;
}
```

<CodeTrace
  title="Prefix — nums=[0,0,1,1,0]"
  :values="['0','0','1','1','0']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { sum: -1, first: "{-1:0}" }, note: "first -1 at 0" },
    { pointers: { i: 1 }, vars: { sum: -2, first: "{-2:1}" }, note: "new min sum" },
    { pointers: { i: 3 }, vars: { sum: 0, best: 4 }, note: "sum=0 first at -1 → length 4" },
    { pointers: { i: 4 }, vars: { sum: -1, best: 4 }, note: "sum=-1 first at 0 → length 4; unchanged" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="contiguous-array" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute | O(n²) | O(1) | baseline |
| Prefix + first-index map | **O(n)** | O(n) | optimum |

## When to use which

- **Equal count of two labels** → 0→−1 mapping + first-index.
- **Longest subarray with sum S** → same skeleton, store first prefix by value.
- **k different labels equal counts** → k-dimensional signature as hash key.

<AiCompanion problem-slug="contiguous-array" pattern-hint="prefix sum" />

## Related problems

- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k)
- [Subarray Sums Divisible by K](/problems/subarray-sums-divisible-by-k)
- [Continuous Subarray Sum](/problems/continuous-subarray-sum)

<FeedbackWidget problem-slug="contiguous-array" />

<RelatedProblems problems="subarray-sums-divisible-by-k::Subarray Sums Divisible By K|range-addition::Range Addition|prefix-sum-subarray-sum-equals-k::Prefix Sum Subarray Sum Equals K" />
