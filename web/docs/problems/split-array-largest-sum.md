# BS on Answer — Split Array Largest Sum

*[↗ LeetCode: Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/bs-on-answer)

<CompanyTags companies="Meta, Google, Amazon, Bloomberg" />

Split `nums` into `m` non-empty contiguous subarrays to minimize the largest sum among the subarrays. Return that min largest sum.

**Example** — `nums=[7,2,5,10,8], m=2` → `18`

**Constraints** — `1 ≤ m ≤ n ≤ 1000`; `0 ≤ nums[i] ≤ 10⁶`.


<Hints
  hint1="Can I write a `feasible(x)` check that returns true iff answer ≤ x (or ≥ x)?"
  hint2="If `feasible` is monotonic in x, binary search over the answer space `[lo, hi]`. Range: min possible value to max possible value."
  hint3="The feasibility check is O(n); total complexity is O(n log range)."
/>
---

<MarkSolved problem-slug="split-array-largest-sum" /> <Bookmark problem-slug="split-array-largest-sum" />

<InterviewTimer problem-slug="split-array-largest-sum" />



## Approach 1 — Interval DP

`dp[i][k]` = min largest sum for `nums[0..i-1]` split into k parts. O(n²·m).

## Approach 2 — Binary search on the answer

**Insight.** `feasible(cap)` = can we split into ≤ m parts each with sum ≤ cap? Monotonic. Range: `lo = max(nums)`, `hi = sum(nums)`.



```java
int splitArray(int[] nums, int m) {
    int lo = 0, hi = 0;
    for (int x : nums) { lo = Math.max(lo, x); hi += x; }
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        int parts = 1, sum = 0;
        for (int x : nums) {
            if (sum + x > mid) { parts++; sum = 0; }
            sum += x;
        }
        if (parts <= m) hi = mid;
        else            lo = mid + 1;
    }
    return lo;
}
```



<CodeTrace
  title="BS on answer — nums=[7,2,5,10,8], m=2"
  :values="[7,2,5,10,8]"
  :windowKeys="['lo','hi']"
  :cellWidth="42"
  :steps='[
    { pointers: { lo: 10, hi: 32, mid: 21 }, vars: { parts: 2 }, note: "cap 21 → 2 parts ≤ 2 → hi=21" },
    { pointers: { lo: 10, hi: 21, mid: 15 }, vars: { parts: 3 }, note: "cap 15 → 3 parts too many → lo=16" },
    { pointers: { lo: 16, hi: 21, mid: 18 }, vars: { parts: 2 }, note: "cap 18 → 2 parts → hi=18" },
    { pointers: { lo: 16, hi: 18, mid: 17 }, vars: { parts: 3 }, note: "cap 17 → 3 parts → lo=18" },
    { pointers: { lo: 18, hi: 18 }, vars: { answer: 18 }, note: "converged → 18" }
  ]'
/>

**Complexity** — Time **O(n log sum)**; Space **O(1)**.

## Try it yourself

<JavaRunner problem-slug="split-array-largest-sum" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Interval DP | O(n²·m) | O(n·m) |
| BS on answer | **O(n log sum)** | O(1) |

## When to use which

- **"Min largest chunk after splitting"** → BS on answer.
- **DP alternative** → interval DP; slower but returns actual partition.
- **Related: max smallest chunk** → similar BS with `≥` predicate.

<AiCompanion problem-slug="split-array-largest-sum" pattern-hint="binary search on answer" />

## Related problems

- [Capacity To Ship Packages](/problems/capacity-to-ship-packages-within-d-days) — same skeleton
- [Divide Chocolate](/problems/divide-chocolate) — maximize the minimum
- [Koko Eating Bananas](/problems/bs-on-answer-koko-bananas)

<FeedbackWidget problem-slug="split-array-largest-sum" />

<RelatedProblems problems="binary-search-rotated-sorted::Binary Search Rotated Sorted|find-peak-element::Find Peak Element|koko-bananas::Koko Bananas" />
