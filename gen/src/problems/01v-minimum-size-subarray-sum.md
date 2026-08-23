# Sliding Window — Minimum Size Subarray Sum

*[↗ LeetCode: Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

<CompanyTags companies="Amazon, Google, Microsoft, Meta" />

Given a positive-int array `nums` and target `target`, return the minimal length of a contiguous subarray whose sum is at least `target`. Return `0` if none.

**Example 1** — `target = 7, nums = [2,3,1,2,4,3]` → `2` (the subarray `[4,3]` sums to 7)
**Example 2** — `target = 4, nums = [1,4,4]` → `1` (single 4)
**Example 3** — `target = 11, nums = [1,1,1,1,1,1,1,1]` → `0` (impossible)

**Constraints** — `1 ≤ n ≤ 10⁵`; `1 ≤ nums[i], target ≤ 10⁴`. **All values positive.**


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

<MarkSolved problem-slug="minimum-size-subarray-sum" /> <Bookmark problem-slug="minimum-size-subarray-sum" />

<InterviewTimer problem-slug="minimum-size-subarray-sum" />



## Approach 1 — All subarrays

**Intuition.** For each `i`, expand `j` and accumulate the sum. On first `sum ≥ target`, record length and break the inner loop (extending further only lengthens).

```java
int minSubArrayLenBrute(int target, int[] nums) {
    int best = Integer.MAX_VALUE;
    for (int i = 0; i < nums.length; i++) {
        int sum = 0;
        for (int j = i; j < nums.length; j++) {
            sum += nums[j];
            if (sum >= target) { best = Math.min(best, j - i + 1); break; }
        }
    }
    return best == Integer.MAX_VALUE ? 0 : best;
}
```

<CodeTrace
  title="Brute — target=7, nums=[2,3,1,2,4,3]"
  :values="['2','3','1','2','4','3']"
  :windowKeys="['i','j']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0, j: 3 }, vars: { sum: 8, len: 4, best: 4 }, note: "2+3+1+2 ≥ 7 → best=4" },
    { pointers: { i: 1, j: 4 }, vars: { sum: 10, len: 4, best: 4 }, note: "3+1+2+4 ≥ 7 → same length" },
    { pointers: { i: 3, j: 4 }, vars: { sum: 6 }, note: "not enough; continue" },
    { pointers: { i: 4, j: 5 }, vars: { sum: 7, len: 2, best: 2 }, note: "4+3 = 7 — best 2" }
  ]'
/>

**Complexity** — Time **O(n²)** worst; Space **O(1)**.

---

## Approach 2 — Sliding window (positives only)

**Insight from brute.** With positive values, growing `right` monotonically increases `sum`, and shrinking `left` monotonically decreases it. So we can extend `right` until `sum ≥ target`, then shrink `left` while the window is still valid — tracking the min length.

```java
int minSubArrayLen(int target, int[] nums) {
    int left = 0, sum = 0, best = Integer.MAX_VALUE;
    for (int right = 0; right < nums.length; right++) {
        sum += nums[right];
        while (sum >= target) {
            best = Math.min(best, right - left + 1);
            sum -= nums[left++];
        }
    }
    return best == Integer.MAX_VALUE ? 0 : best;
}
```

<CodeTrace
  title="Sliding — target=7, nums=[2,3,1,2,4,3]"
  :values="['2','3','1','2','4','3']"
  :windowKeys="['left','right']"
  :cellWidth="34"
  :steps='[
    { pointers: { left: 0, right: 3 }, vars: { sum: 8, best: 4 }, note: "sum ≥ 7 — record len 4; shrink" },
    { pointers: { left: 2, right: 4 }, vars: { sum: 7, best: 3 }, note: "shrunk to [1,2,4]; sum=7 — best 3" },
    { pointers: { left: 4, right: 4 }, vars: { sum: 4 }, note: "invalid; extend right" },
    { pointers: { left: 4, right: 5 }, vars: { sum: 7, best: 2 }, note: "[4,3] sum=7 — best 2" }
  ]'
/>

**Complexity** — Time **O(n)** — each index enters and leaves the window at most once; Space **O(1)**.

---

## Approach 3 — Prefix sum + binary search (extends to negatives? No)

**Insight from sliding.** Sliding window fails once values can be negative — shrinking doesn't monotonically decrease sum. A prefix-sum + binary-search approach handles positives at **O(n log n)** and generalizes to a **monotonic deque** approach for negatives (see [Shortest Subarray with Sum at Least K](/problems/shortest-subarray-with-sum-at-least-k)).

```java
int minSubArrayLenBS(int target, int[] nums) {
    int n = nums.length;
    int[] pref = new int[n + 1];
    for (int i = 0; i < n; i++) pref[i + 1] = pref[i] + nums[i];
    int best = Integer.MAX_VALUE;
    for (int i = 0; i < n; i++) {
        int need = pref[i] + target;
        int j = Arrays.binarySearch(pref, i + 1, n + 1, need);
        if (j < 0) j = -j - 1;
        if (j <= n) best = Math.min(best, j - i);
    }
    return best == Integer.MAX_VALUE ? 0 : best;
}
```

**Complexity** — Time **O(n log n)**; Space **O(n)**. Loses to sliding for positives-only but sets up the generalization.

---

## Try it yourself

<JavaRunner problem-slug="minimum-size-subarray-sum" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| All subarrays | O(n²) | O(1) | baseline |
| Sliding window | **O(n)** | O(1) | expected optimum for positives |
| Prefix + binary search | O(n log n) | O(n) | polish — generalizes to negatives via deque |

## When to use which

- **First pass** — sliding window is the right answer for positives.
- **"What if values can be negative?"** → mention the generalization: **monotonic deque on prefix sums**.
- **"Return the subarray itself"** → track `(bestL, bestLen)` and slice.
- **"Sum exactly equal to target"** → different problem — needs prefix-sum + hash-map (see [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k)).

<AiCompanion problem-slug="minimum-size-subarray-sum" pattern-hint="sliding window" />

## Related problems

- [Shortest Subarray with Sum at Least K](/problems/shortest-subarray-with-sum-at-least-k) — with negatives, monotonic deque
- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k) — count of subarrays, not length
- [Maximum Subarray](/problems/maximum-subarray) — Kadane
- [Minimum Window Substring](/problems/minimum-window-substring) — same shrinking template

<FeedbackWidget problem-slug="minimum-size-subarray-sum" />

<RelatedProblems problems="count-number-of-nice-subarrays::Count Number Of Nice Subarrays|max-consecutive-ones-iii::Max Consecutive Ones III|subarray-product-less-than-k::Subarray Product Less Than K" />
