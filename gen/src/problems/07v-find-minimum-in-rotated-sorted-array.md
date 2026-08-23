# Binary Search — Find Minimum in Rotated Sorted Array

*[↗ LeetCode: Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/binary-search)

<CompanyTags companies="Meta, Amazon, Google, Microsoft" />

Given a sorted array rotated at some unknown pivot, return the minimum. All values are **unique**.

**Example 1** — `nums = [3,4,5,1,2]` → `1`
**Example 2** — `nums = [4,5,6,7,0,1,2]` → `0`
**Example 3** — `nums = [11,13,15,17]` → `11` (no rotation)

**Constraints** — `1 ≤ n ≤ 5000`. Distinct values. Must run in **O(log n)**.


<Hints
  hint1="The input has a monotonic property somewhere — sorted, or piecewise-sorted."
  hint2="Use half-open `[lo, hi)` template. Invariant: answer lives in `[lo, hi)` throughout. Return `lo`."
  hint3="For rotated arrays: one half is always sorted — compare mid with lo (or hi) to detect which side."
/>
---

## Approach 1 — Linear scan

O(n). Rejected.

## Approach 2 — Binary search on the sorted-half invariant

**Intuition.** For any `mid`, compare `nums[mid]` with `nums[hi]`:
- If `nums[mid] > nums[hi]`, the min is in `(mid, hi]` — pivot to right.
- Else, min is in `[lo, mid]`.

**Why compare with `hi`, not `lo`.** With `lo` you can't distinguish "no rotation" from "in rotated region." `hi` is always in the smaller/rotated half if a rotation exists.

**Trap** — use half-open convention or handle equality carefully.

```java
int findMin(int[] nums) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > nums[hi]) lo = mid + 1;
        else hi = mid;
    }
    return nums[lo];
}
```

<CodeTrace
  title="BS — nums=[4,5,6,7,0,1,2]"
  :values="['4','5','6','7','0','1','2']"
  :windowKeys="['lo','hi','mid']"
  :cellWidth="34"
  :steps='[
    { pointers: { lo: 0, hi: 6, mid: 3 }, vars: { midVal: 7, hiVal: 2 }, note: "7 > 2 → min is right of mid → lo=4" },
    { pointers: { lo: 4, hi: 6, mid: 5 }, vars: { midVal: 1, hiVal: 2 }, note: "1 < 2 → min is left/at mid → hi=5" },
    { pointers: { lo: 4, hi: 5, mid: 4 }, vars: { midVal: 0, hiVal: 1 }, note: "0 < 1 → hi=4" },
    { pointers: { lo: 4, hi: 4 }, vars: { min: 0 }, note: "lo == hi → return nums[4]=0" }
  ]'
/>

**Complexity** — Time **O(log n)**; Space **O(1)**.

---

## Approach 3 — With duplicates (LC 154)

**Insight.** If `nums[mid] == nums[hi]`, we can't decide which side has the min. Shrink `hi--` and retry.

**Complexity** — Time **O(log n)** average, **O(n)** worst (all duplicates); Space **O(1)**.

```java
int findMinDup(int[] nums) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > nums[hi]) lo = mid + 1;
        else if (nums[mid] < nums[hi]) hi = mid;
        else hi--;
    }
    return nums[lo];
}
```

---

## Try it yourself

<JavaRunner problem-slug="find-minimum-in-rotated-sorted-array" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Linear scan | O(n) | O(1) | rejected |
| BS with sorted-half invariant | **O(log n)** | **O(1)** | expected |
| BS with duplicates handling | O(log n) avg, O(n) worst | O(1) | for LC 154 |

## When to use which

- **Distinct values** → the simpler BS with `nums[mid] > nums[hi]`.
- **With duplicates** → include the `hi--` fallback.
- **"Find max instead of min"** → symmetric — compare with `lo`.
- **"Return the pivot index"** → same algorithm; return `lo`.

## Related problems

- [Find Minimum in Rotated Sorted Array II](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/) — duplicates
- [Search in Rotated Sorted Array](/problems/binary-search-rotated-sorted) — search for target
- [Search in Rotated Sorted Array II](/problems/search-in-rotated-sorted-array-ii)
- [Find Peak Element](/problems/find-peak-element) — related BS on non-monotone