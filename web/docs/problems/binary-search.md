# Binary Search — Binary Search

*[↗ LeetCode: Binary Search](https://leetcode.com/problems/binary-search/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/binary-search)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft" /&gt;

Given a sorted array `nums` and an integer `target`, return the index of `target`, or `-1` if not present. Must run in **O(log n)** time.

**Example 1** — `nums = [-1,0,3,5,9,12], target = 9` → `4`
**Example 2** — `nums = [-1,0,3,5,9,12], target = 2` → `-1`
**Example 3** — `nums = [5], target = 5` → `0`

**Constraints** — `1 ≤ n ≤ 10⁴`; all distinct; sorted ascending.


&lt;Hints
  hint1="The input has a monotonic property somewhere — sorted, or piecewise-sorted."
  hint2="Use half-open `[lo, hi)` template. Invariant: answer lives in `[lo, hi)` throughout. Return `lo`."
  hint3="For rotated arrays: one half is always sorted — compare mid with lo (or hi) to detect which side."
/&gt;
---

## Approach 1 — Linear scan

O(n) time. Rejected by spec.

## Approach 2 — Standard binary search (closed interval)

**Intuition.** Maintain `[lo, hi]` as the still-possible range. Look at `mid`; discard one half.

**Trap** — use `lo + (hi - lo) / 2` to avoid integer overflow when `lo + hi` overflows.



```java
int search(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```



<CodeTrace
  title="Standard — nums=[-1,0,3,5,9,12], target=9"
  :values="['-1','0','3','5','9','12']"
  :windowKeys="['lo','hi','mid']"
  :cellWidth="34"
  :steps='[
    { pointers: { lo: 0, hi: 5, mid: 2 }, vars: { midVal: 3 }, note: "3 < 9 → lo=3" },
    { pointers: { lo: 3, hi: 5, mid: 4 }, vars: { midVal: 9 }, note: "found — return 4" }
  ]'
/>

**Complexity** — Time **O(log n)**; Space **O(1)**.

---

## Approach 3 — Half-open convention (`[lo, hi)`) — safer for boundary problems

**Insight.** Using `hi = nums.length` (one past the end) and `lo < hi` avoids off-by-one errors when generalizing to "first true" / "last false" problems.



```java
int searchHO(int[] nums, int target) {
    int lo = 0, hi = nums.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return (lo < nums.length && nums[lo] == target) ? lo : -1;
}
```



**Why this template.** After the loop, `lo` is the smallest index with `nums[lo] ≥ target` (lower_bound). Widely reusable for [Search Insert Position](https://leetcode.com/problems/search-insert-position/), first-occurrence, etc.

**Complexity** — Time **O(log n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="binary-search" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Linear scan | O(n) | O(1) | rejected |
| Closed-interval BS | **O(log n)** | O(1) | expected |
| Half-open BS | O(log n) | O(1) | polish — extensible template |

## When to use which

- **Presence check on sorted array** → either template works.
- **Search-insert / lower_bound / upper_bound** → half-open template is cleaner.
- **Rotated sorted array** → see [Search in Rotated Sorted Array](/problems/binary-search-rotated-sorted).
- **Binary search on the answer** → apply the same template with a feasibility predicate; see [Koko Eating Bananas](/problems/bs-on-answer-koko-bananas).

## Related problems

- [Search Insert Position](https://leetcode.com/problems/search-insert-position/) — lower_bound
- [First Bad Version](https://leetcode.com/problems/first-bad-version/) — "first true"
- [Search in Rotated Sorted Array](/problems/binary-search-rotated-sorted) — piecewise-sorted
- [Find Peak Element](/problems/find-peak-element) — BS on non-monotone