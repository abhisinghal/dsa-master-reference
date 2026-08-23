# Sliding Window — Subarrays with K Different Integers

*[↗ LeetCode: Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/sliding-window)

<CompanyTags companies="Google, Amazon" />

Given an integer array `nums` and integer `k`, return the number of contiguous subarrays containing **exactly** `k` distinct integers.

**Example 1** — `nums = [1,2,1,2,3], k = 2` → `7` (subarrays: `[1,2]`, `[2,1]`, `[1,2]`, `[2,1,2]`, `[1,2,1]`, `[1,2,1,2]`, `[2,1,2,1]`… actually 7 with exactly 2 distinct)
**Example 2** — `nums = [1,2,1,3,4], k = 3` → `3`
**Example 3** — `nums = [1,1,1], k = 1` → `6` (each of `[1]`, `[1]`, `[1]`, `[1,1]`, `[1,1]`, `[1,1,1]`)

**Constraints** — `1 ≤ n ≤ 2 · 10⁴`; `1 ≤ nums[i] ≤ n`; `1 ≤ k ≤ n`.


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

<MarkSolved problem-slug="subarrays-with-k-different-integers" />

<InterviewTimer problem-slug="subarrays-with-k-different-integers" />



## Approach 1 — Enumerate every subarray

**Intuition.** Count distinct in each `[i, j]`; if exactly `k`, increment.

```java
int subarraysWithKDistinctBrute(int[] nums, int k) {
    int n = nums.length, count = 0;
    for (int i = 0; i < n; i++) {
        Set<Integer> d = new HashSet<>();
        for (int j = i; j < n; j++) {
            d.add(nums[j]);
            if (d.size() == k) count++;
            else if (d.size() > k) break;
        }
    }
    return count;
}
```

**Complexity** — Time **O(n²)**; Space **O(n)**.

---

## Approach 2 — Two windows: `atMost(k) − atMost(k−1)`

**Insight from brute.** "Exactly k" is hard to slide directly. But `exactly(k) = atMost(k) - atMost(k-1)`. Each `atMost` is a standard sliding window with a distinct counter.

**Why it works.** Every subarray with ≤ k distinct is counted by `atMost(k)`. Subtract those with ≤ k−1 distinct — what remains is exactly k distinct.

```java
int subarraysWithKDistinct(int[] nums, int k) {
    return atMost(nums, k) - atMost(nums, k - 1);
}
int atMost(int[] nums, int k) {
    if (k < 0) return 0;
    Map<Integer, Integer> cnt = new HashMap<>();
    int left = 0, res = 0;
    for (int right = 0; right < nums.length; right++) {
        cnt.merge(nums[right], 1, Integer::sum);
        while (cnt.size() > k) {
            cnt.merge(nums[left], -1, Integer::sum);
            if (cnt.get(nums[left]) == 0) cnt.remove(nums[left]);
            left++;
        }
        res += right - left + 1; // # of subarrays ending at `right`
    }
    return res;
}
```

<CodeTrace
  title="atMost(k=2) — nums=[1,2,1,2,3]"
  :values="['1','2','1','2','3']"
  :windowKeys="['left','right']"
  :cellWidth="36"
  :steps='[
    { pointers: { left: 0, right: 0 }, vars: { cnt: "{1:1}", res: 1 }, note: "1 subarray ending at 0" },
    { pointers: { left: 0, right: 1 }, vars: { cnt: "{1:1,2:1}", res: 3 }, note: "2 subarrays end at 1 — total 3" },
    { pointers: { left: 0, right: 3 }, vars: { cnt: "{1:2,2:2}", res: 10 }, note: "at each step add right-left+1" },
    { pointers: { left: 2, right: 4 }, vars: { cnt: "{1:1,2:1,3:1}", size: 3 }, note: "shrink until size ≤ 2" },
    { pointers: { left: 3, right: 4 }, vars: { cnt: "{2:1,3:1}", res: 12 }, note: "final atMost(2) = 12" }
  ]'
/>

Then `atMost(2) - atMost(1) = 12 - 5 = 7`.

**Complexity** — Time **O(n)** — two O(n) sweeps; Space **O(k)**.

---

## Try it yourself

<JavaRunner problem-slug="subarrays-with-k-different-integers" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Every subarray | O(n²) | O(n) | baseline |
| Two `atMost` windows | **O(n)** | O(k) | expected optimum |

## When to use which

- **"Exactly k" phrasing** → immediately go to `atMost(k) - atMost(k-1)`.
- **"At most k"** → single sliding window.
- **"At least k"** → count total `n·(n+1)/2` minus `atMost(k-1)`.
- **"Return the subarrays themselves"** → change the counting to enumeration; loses O(n).

<AiCompanion problem-slug="subarrays-with-k-different-integers" pattern-hint="sliding window" />

## Related problems

- [Binary Subarrays With Sum](/problems/binary-subarrays-with-sum) — same at-most trick with sums
- [Count Number of Nice Subarrays](/problems/count-number-of-nice-subarrays) — same trick, k odd numbers
- [Longest Substring with At Most K Distinct Characters](/problems/longest-substring-with-at-most-k-distinct-characters) — length variant
- [Subarray Product Less Than K](/problems/subarray-product-less-than-k)

<FeedbackWidget problem-slug="subarrays-with-k-different-integers" />

<RelatedProblems problems="number-of-substrings-containing-all-three-characters::Number Of Substrings Containing All Three Characters|minimum-window-substring::Minimum Window Substring|count-number-of-nice-subarrays::Count Number Of Nice Subarrays" />
