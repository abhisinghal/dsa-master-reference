# Two Pointers — 3Sum Closest

*[↗ LeetCode: 3Sum Closest](https://leetcode.com/problems/3sum-closest/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft" /&gt;

Given an integer array `nums` of length `n` and integer `target`, return the sum of three integers from `nums` that is closest to `target`.

**Example 1** — `nums = [-1,2,1,-4], target = 1` → `2` (`-1 + 2 + 1 = 2`)
**Example 2** — `nums = [0,0,0], target = 1` → `0`
**Example 3** — `nums = [1,1,1,0], target = -100` → `2`

**Constraints** — `3 ≤ n ≤ 500`; `-10³ ≤ nums[i], target ≤ 10³`.


&lt;Hints
  hint1="Sort first if the input isn’t already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/&gt;
---

&lt;MarkSolved problem-slug="3sum-closest" /&gt;

&lt;InterviewTimer problem-slug="3sum-closest" /&gt;



## Approach 1 — Triple nested loop

**Intuition.** Enumerate every triplet; keep the sum with smallest `|sum - target|`.



```java
int threeSumClosestBrute(int[] nums, int target) {
    int n = nums.length, best = nums[0] + nums[1] + nums[2];
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            for (int k = j + 1; k < n; k++) {
                int s = nums[i] + nums[j] + nums[k];
                if (Math.abs(s - target) < Math.abs(best - target)) best = s;
            }
    return best;
}
```



**Complexity** — Time **O(n³)**; Space **O(1)**.

---

## Approach 2 — Sort + two-pointer

**Insight from brute.** Same shape as [3Sum](/problems/3sum). Sort. Fix `i`; two pointers on `[i+1, n-1]` — move whichever pointer nudges the sum toward `target`.

**Early return.** If sum exactly equals target, we can't beat it.



```java
int threeSumClosest(int[] nums, int target) {
    Arrays.sort(nums);
    int n = nums.length;
    int best = nums[0] + nums[1] + nums[2];
    for (int i = 0; i < n - 2; i++) {
        int l = i + 1, r = n - 1;
        while (l < r) {
            int s = nums[i] + nums[l] + nums[r];
            if (Math.abs(s - target) < Math.abs(best - target)) best = s;
            if (s == target) return s;
            if (s < target) l++;
            else r--;
        }
    }
    return best;
}
```



<CodeTrace
  title="Sort + 2p — nums=[-1,2,1,-4] sorted=[-4,-1,1,2], target=1"
  :values="['-4','-1','1','2']"
  :windowKeys="['i','l','r']"
  :cellWidth="36"
  :steps='[
    { pointers: { i: 0, l: 1, r: 3 }, vars: { sum: -3, dist: 4, best: -3 }, note: "-4+-1+2=-3; distance 4" },
    { pointers: { i: 0, l: 2, r: 3 }, vars: { sum: -1, dist: 2, best: -1 }, note: "advance l; sum=-1 closer" },
    { pointers: { i: 1, l: 2, r: 3 }, vars: { sum: 2, dist: 1, best: 2 }, note: "i=-1: sum=2, dist=1 — new best" },
    { pointers: { i: 1, l: 3, r: 3 }, vars: {}, note: "l==r → break; final best=2" }
  ]'
/>

**Complexity** — Time **O(n²)**; Space **O(1)** extra.

---

## Try it yourself

<JavaRunner problem-slug="3sum-closest" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Triple loop | O(n³) | O(1) | baseline |
| Sort + two-pointer | **O(n²)** | O(1) | expected optimum |

## When to use which

- **First pass** — sort + two-pointer.
- **"Return triplet, not sum"** → track `(a, b, c)` alongside `best`.
- **"kSum closest"** → recurse: fix (k-2) values, close with 2-pointer.
- **Skip duplicates** — not required for closeness (any triplet is fine), but if asked to return the *first* found or all tying triplets, add dedup skips.

&lt;AiCompanion problem-slug="3sum-closest" pattern-hint="two pointers" /&gt;

## Related problems

- [3Sum](/problems/3sum) — exact zero
- [3Sum Smaller](/problems/3sum-smaller) — count strictly less than target
- [4Sum](/problems/4sum) — one more nested loop
- [Two Sum](/problems/hashing-two-sum)

&lt;FeedbackWidget problem-slug="3sum-closest" /&gt;

&lt;RelatedProblems problems="container-with-most-water::Container With Most Water|boats-to-save-people::Boats To Save People|squares-of-a-sorted-array::Squares Of A Sorted Array" /&gt;
