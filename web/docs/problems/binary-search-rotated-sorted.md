# Binary Search — Search in Rotated Sorted Array

*[↗ LeetCode: Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/binary-search)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft, Apple, Bloomberg, Adobe" /&gt;

Given a rotated ascending array `nums` and `target`, return its index or `-1`. Time must be **O(log n)**.

**Example 1** — `nums=[4,5,6,7,0,1,2], target=0` → `4`
**Example 2** — `nums=[4,5,6,7,0,1,2], target=3` → `-1`
**Example 3** — `nums=[1], target=0` → `-1`

**Constraints** — `1 ≤ n ≤ 5000`; values distinct.


&lt;Hints
  hint1="The input has a monotonic property somewhere — sorted, or piecewise-sorted."
  hint2="Use half-open `[lo, hi)` template. Invariant: answer lives in `[lo, hi)` throughout. Return `lo`."
  hint3="For rotated arrays: one half is always sorted — compare mid with lo (or hi) to detect which side."
/&gt;
---

&lt;MarkSolved problem-slug="binary-search-rotated-sorted" /&gt;


## Approach 1 — Brute force (linear scan)

**Intuition.** Ignore the rotation; scan.



```java
int searchLinear(int[] a, int target) {
    for (int i = 0; i < a.length; i++)
        if (a[i] == target) return i;
    return -1;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**. Violates the O(log n) requirement.

---

## Approach 2 — Find the pivot, then binary search the correct half

**Insight from brute.** The array is *two* sorted subarrays glued at the pivot. If we find the pivot in O(log n), we can binary-search whichever subarray contains the target.

Step 1: Find pivot (smallest element) with binary search — pivot is where `nums[mid] > nums[hi]`, so move `lo = mid + 1`; otherwise `hi = mid`.
Step 2: Standard binary search on the correct half.



```java
int searchTwoPass(int[] a, int target) {
    int n = a.length;
    int lo = 0, hi = n - 1;
    while (lo < hi) {                       // find pivot
        int mid = lo + (hi - lo) / 2;
        if (a[mid] > a[hi]) lo = mid + 1;
        else                hi = mid;
    }
    int pivot = lo;
    // Standard BS on rotated view
    lo = 0; hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int real = (mid + pivot) % n;
        if (a[real] == target) return real;
        if (a[real] < target) lo = mid + 1;
        else                  hi = mid - 1;
    }
    return -1;
}
```



**Complexity** — Time **O(log n)** (two BS passes); Space **O(1)**. Correct but does two searches.

---

## Approach 3 — One-pass binary search (identify the sorted half)

**Insight from two-pass.** At any `mid`, exactly one of `[lo..mid]` or `[mid..hi]` is a normally-sorted contiguous range. Test which side contains `target` by simple range check, then recurse there.

**Trap.** Use `nums[lo] <= nums[mid]` (**inclusive**). At `[3,1]` with `lo=0, hi=1, mid=0`, strict `<` misroutes.



```java
int search(int[] a, int target) {
    int lo = 0, hi = a.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[lo] <= a[mid]) {              // left half is sorted
            if (a[lo] <= target && target < a[mid]) hi = mid - 1;
            else                                    lo = mid + 1;
        } else {                            // right half is sorted
            if (a[mid] < target && target <= a[hi]) lo = mid + 1;
            else                                    hi = mid - 1;
        }
    }
    return -1;
}
```



<CodeTrace
  title="One-pass BS — nums=[4,5,6,7,0,1,2], target=0"
  :values="[4,5,6,7,0,1,2]"
  :windowKeys="['lo','hi']"
  :cellWidth="38"
  :steps='[
    { pointers: { lo: 0, hi: 6, mid: 3 }, vars: { "a[mid]": 7, "left sorted": true }, note: "left [4..7] sorted, target 0 not in it → lo=mid+1" },
    { pointers: { lo: 4, hi: 6, mid: 5 }, vars: { "a[mid]": 1, "left sorted": true }, note: "left [0..1] sorted, target 0 in it → hi=mid-1" },
    { pointers: { lo: 4, hi: 4, mid: 4 }, vars: { "a[mid]": 0 }, note: "match → return 4", added: [4] }
  ]'
/>

**Complexity** — Time **O(log n)**; Space **O(1)**. Optimal — one pass.

---

## Try it yourself

<JavaRunner problem-slug="binary-search-rotated-sorted" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Linear scan | O(n) | O(1) |
| Pivot then BS | O(log n) | O(1) |
| One-pass BS | **O(log n)** | O(1) |

## When to use which

- **Cold interview** → walk linear → one-pass BS. Two-pass is only worth mentioning if the interviewer wants to see you break the problem into "find rotation, then search."
- **Duplicates allowed?** → Approach 3 doesn't work; you have to shrink `lo`/`hi` by 1 when `nums[lo] == nums[mid] == nums[hi]`, giving worst-case O(n).

&lt;AiCompanion problem-slug="binary-search-rotated-sorted" pattern-hint="binary search" /&gt;

## Related problems (same ladder applies)

- [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) — Approach 2's pivot-finding step alone
- [Search in Rotated Sorted Array II](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/) — same shape, duplicates → worst-case O(n)
- [Find Peak Element](https://leetcode.com/problems/find-peak-element/) — BS on an unsorted array via the peak invariant

&lt;FeedbackWidget problem-slug="binary-search-rotated-sorted" /&gt;
