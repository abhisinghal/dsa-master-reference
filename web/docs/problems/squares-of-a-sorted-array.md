# Two Pointers — Squares of a Sorted Array

*[↗ LeetCode: Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

&lt;CompanyTags companies="Amazon, Google, Meta" /&gt;

Return squares of a sorted (possibly-negative) array, sorted.

**Example 1** — `nums=[-4,-1,0,3,10]` → `[0,1,9,16,100]`
**Example 2** — `nums=[-7,-3,2,3,11]` → `[4,9,9,49,121]`

**Constraints** — `1 ≤ n ≤ 10⁴`; sorted ascending.


&lt;Hints
  hint1="Sort first if the input isn’t already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/&gt;
---

&lt;MarkSolved problem-slug="squares-of-a-sorted-array" /&gt;

&lt;InterviewTimer problem-slug="squares-of-a-sorted-array" /&gt;



## Approach 1 — Square then sort

O(n log n).

## Approach 2 — Two pointers filling from back (canonical)

**Insight.** Largest square is at one of the two ends. Compare, place at `k = n-1`, decrement, repeat.



```java
int[] sortedSquares(int[] nums) {
    int n = nums.length, l = 0, r = n - 1, k = n - 1;
    int[] out = new int[n];
    while (l <= r) {
        int a = nums[l] * nums[l], b = nums[r] * nums[r];
        if (a > b) { out[k--] = a; l++; }
        else { out[k--] = b; r--; }
    }
    return out;
}
```



<CodeTrace
  title="Square then sort"
  :values="['-4', '-1', '0', '3', '10']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 4 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)** for output.

---

## Try it yourself

<JavaRunner problem-slug="squares-of-a-sorted-array" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort | O(n log n) | O(n) | baseline |
| Fill from back | **O(n)** | O(n) | canonical |

## When to use which

- **"Sorted array with monotone-transform"** → fill-from-ends technique.
- **In-place mutation** → different — see [Merge Sorted Array](/problems/merge-sorted-array).

&lt;AiCompanion problem-slug="squares-of-a-sorted-array" pattern-hint="two pointers" /&gt;

## Related problems

- [Merge Sorted Array](/problems/merge-sorted-array)
- [Sort Colors](https://leetcode.com/problems/sort-colors/)

&lt;FeedbackWidget problem-slug="squares-of-a-sorted-array" /&gt;

&lt;RelatedProblems problems="3sum-closest::3sum Closest|move-zeroes::Move Zeroes|container-with-most-water::Container With Most Water" /&gt;
