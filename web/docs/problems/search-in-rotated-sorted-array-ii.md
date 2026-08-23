# Binary Search — Search in Rotated Sorted Array II

*[↗ LeetCode: Search in Rotated Sorted Array II](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/binary-search)

Sorted array rotated at unknown pivot, **may contain duplicates**. Return true iff `target` exists.

**Example 1** — `nums = [2,5,6,0,0,1,2], target = 0` → `true`
**Example 2** — `nums = [2,5,6,0,0,1,2], target = 3` → `false`
**Example 3** — `nums = [1,0,1,1,1], target = 0` → `true`

**Constraints** — `1 ≤ n ≤ 5000`; duplicates allowed.

---

## Approach 1 — Linear scan

O(n). Correct baseline; interviewer may accept if worst-case duplicates force it anyway.

## Approach 2 — Modified BS with sorted-half detection + duplicate shrink

**Insight from LC 33 (no duplicates).** At each step, one half `[lo, mid]` or `[mid, hi]` is guaranteed sorted. Compare `nums[mid]` with `nums[lo]`:
- `nums[mid] > nums[lo]` → left half `[lo, mid]` is sorted.
- `nums[mid] < nums[lo]` → right half `[mid, hi]` is sorted.
- `nums[mid] == nums[lo]` → **can't decide** (duplicate). Shrink `lo++` and retry.

Once we know a sorted half, check whether `target` lies within its range; recurse.



```java
boolean search(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return true;
        if (nums[mid] == nums[lo]) { lo++; continue; }
        if (nums[mid] > nums[lo]) {
            // left half sorted
            if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            // right half sorted
            if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return false;
}
```



<CodeTrace
  title="BS with dups — nums=[2,5,6,0,0,1,2], target=0"
  :values="['2','5','6','0','0','1','2']"
  :windowKeys="['lo','hi','mid']"
  :cellWidth="34"
  :steps='[
    { pointers: { lo: 0, hi: 6, mid: 3 }, vars: { midVal: 0 }, note: "found! return true" }
  ]'
/>

For `target = 3`:
- mid=3, val=0 ≠ 3.
- nums[mid]=0 &lt; nums[lo]=2 → right half [3..6]=[0,0,1,2] sorted.
- 0 &lt; 3 ≤ 2? No — go left, hi = 2.
- mid=1, val=5 ≠ 3; nums[mid]=5 &gt; nums[lo]=2 → left half [0..1] sorted; 2 ≤ 3 &lt; 5 → hi=0.
- mid=0, val=2 ≠ 3 → lo=1.
- lo &gt; hi → return false.

**Complexity** — Time **O(log n)** average; **O(n)** worst-case when many duplicates force `lo++`.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Linear scan | O(n) | O(1) | acceptable given worst case |
| Modified BS | **O(log n) avg**, O(n) worst | O(1) | expected optimum |

## When to use which

- **Distinct values guaranteed** → use [Search in Rotated Sorted Array](/problems/binary-search-rotated-sorted) (LC 33) — always O(log n).
- **Duplicates possible** → this problem — accept O(n) worst case.
- **"Return the index, not boolean"** → same skeleton; `return mid` on match, `return -1` at end.

## Related problems

- [Search in Rotated Sorted Array](/problems/binary-search-rotated-sorted) — no duplicates
- [Find Minimum in Rotated Sorted Array](/problems/find-minimum-in-rotated-sorted-array) — same pivot logic
- [Find Minimum in Rotated Sorted Array II](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/) — duplicates variant of that
