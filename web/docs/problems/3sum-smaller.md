# Two Pointers — 3Sum Smaller

*[↗ LeetCode: 3Sum Smaller](https://leetcode.com/problems/3sum-smaller/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Google, Amazon" />

Count triplets `(i, j, k)` with `i < j < k` and `nums[i] + nums[j] + nums[k] < target`.

**Example 1** — `nums=[-2,0,1,3], target=2` → `2`
**Example 2** — `nums=[], target=0` → `0`

**Constraints** — `0 ≤ n ≤ 3500`. Brute is O(n³) ≈ 4·10¹⁰ ops at n=3500 (TLE). Sort + two-pointer with count is O(n²) ≈ 1.2·10⁷ ops.
<Hints
  hint1="Sort first if the input isn’t already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/>
---

<MarkSolved problem-slug="3sum-smaller" /> <Bookmark problem-slug="3sum-smaller" />

<InterviewTimer problem-slug="3sum-smaller" />



## Approach 1 — Triple loop

O(n³).

## Approach 2 — Sort + counting two-pointer (canonical)

**Insight.** After sorting, for each `i` and left pointer `l`, if `nums[i]+nums[l]+nums[r] < target`, then **every** `k` in `(l, r]` also satisfies it — add `r - l`.



```java
int threeSumSmaller(int[] nums, int target) {
    Arrays.sort(nums);
    int count = 0;
    for (int i = 0; i < nums.length - 2; i++) {
        int l = i + 1, r = nums.length - 1;
        while (l < r) {
            if (nums[i] + nums[l] + nums[r] < target) { count += r - l; l++; }
            else r--;
        }
    }
    return count;
}
```



<CodeTrace
  title="Triple loop"
  :values="['-2', '0', '1', '3']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n²)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="3sum-smaller" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Triple loop | O(n³) | O(1) | baseline |
| Sort + counting | **O(n²)** | O(1) | canonical |

## When to use which

- **"Count triplets &lt; target"** → sort + counting shortcut.
- **"Return the triplets"** → enumerate; loses O(1).

<AiCompanion problem-slug="3sum-smaller" pattern-hint="two pointers" />

## Related problems

- [3Sum](/problems/3sum)
- [3Sum Closest](/problems/3sum-closest)

<FeedbackWidget problem-slug="3sum-smaller" />

<RelatedProblems problems="container-with-most-water::Container With Most Water|3sum-closest::3sum Closest|move-zeroes::Move Zeroes" />
