# Binary Search — Find Peak Element

*[↗ LeetCode: Find Peak Element](https://leetcode.com/problems/find-peak-element/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/binary-search)

<CompanyTags companies="Meta, Google, Amazon, Bloomberg" />

A peak is an element strictly greater than its neighbors. Given `nums` (with `nums[-1] = nums[n] = -∞`), return the index of any peak. Must run in **O(log n)**.

**Example 1** — `nums = [1,2,3,1]` → `2` (value 3 is a peak)
**Example 2** — `nums = [1,2,1,3,5,6,4]` → `1` or `5` (both are peaks)
**Example 3** — `nums = [1]` → `0`

**Constraints** — `1 ≤ n ≤ 1000`; `-2³¹ ≤ nums[i] ≤ 2³¹ − 1`; adjacent values differ (no plateau).


<Hints
  hint1="The input has a monotonic property somewhere — sorted, or piecewise-sorted."
  hint2="Use half-open `[lo, hi)` template. Invariant: answer lives in `[lo, hi)` throughout. Return `lo`."
  hint3="For rotated arrays: one half is always sorted — compare mid with lo (or hi) to detect which side."
/>
---

## Approach 1 — Linear scan

O(n). Rejected.

## Approach 2 — Binary search on slope

**Intuition.** Compare `nums[mid]` with `nums[mid+1]`:
- If `nums[mid] < nums[mid+1]`, the slope is climbing → a peak must be at `mid+1` or to its right (since `nums[n] = -∞`, some right neighbor must eventually drop).
- Else, the slope is falling → peak at `mid` or to its left.

**Why it works.** The invariant is: at least one peak exists in `[lo, hi]`. Each step preserves that invariant by choosing the half that includes a rising boundary going down.

```java
int findPeakElement(int[] nums) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < nums[mid + 1]) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

<CodeTrace
  title="BS on slope — nums=[1,2,1,3,5,6,4]"
  :values="['1','2','1','3','5','6','4']"
  :windowKeys="['lo','hi','mid']"
  :cellWidth="34"
  :steps='[
    { pointers: { lo: 0, hi: 6, mid: 3 }, vars: { midVal: 3, next: 5 }, note: "3 < 5 → climbing → lo=4" },
    { pointers: { lo: 4, hi: 6, mid: 5 }, vars: { midVal: 6, next: 4 }, note: "6 > 4 → falling → hi=5" },
    { pointers: { lo: 4, hi: 5, mid: 4 }, vars: { midVal: 5, next: 6 }, note: "5 < 6 → lo=5" },
    { pointers: { lo: 5, hi: 5 }, vars: { peak: 6 }, note: "lo==hi → index 5 is a peak" }
  ]'
/>

**Complexity** — Time **O(log n)**; Space **O(1)**.

---

## Approach 3 — Find *global* max (for the "any peak" spec, wasteful)

O(n) linear pass; rejected.

---

## Try it yourself

<JavaRunner problem-slug="find-peak-element" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Linear scan | O(n) | O(1) | rejected |
| BS on slope | **O(log n)** | O(1) | expected |

## When to use which

- **Any peak** → BS on slope.
- **All peaks** → linear pass.
- **"Peak in 2D matrix"** → recurse on rows/cols, similar BS idea (LC 1901).
- **"Peak with plateau"** → strict inequality assumption fails; problem becomes harder.

<AiCompanion problem-slug="find-peak-element" pattern-hint="binary search" />

## Related problems

- [Find Minimum in Rotated Sorted Array](/problems/find-minimum-in-rotated-sorted-array) — similar BS on non-monotone
- [Peak Index in a Mountain Array](https://leetcode.com/problems/peak-index-in-a-mountain-array/) — guaranteed single peak
- [Find a Peak Element II](https://leetcode.com/problems/find-a-peak-element-ii/) — 2D