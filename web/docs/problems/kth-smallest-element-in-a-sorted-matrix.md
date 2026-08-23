# BS on Answer — Kth Smallest Element in a Sorted Matrix

*[↗ LeetCode: Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/bs-on-answer)

<CompanyTags companies="Meta, Amazon, Google, Uber, Bloomberg" />

Given `n×n` matrix sorted row and column, return the k-th smallest element.

**Example** — `matrix=[[1,5,9],[10,11,13],[12,13,15]], k=8` → `13`

**Constraints** — `1 ≤ n ≤ 300`; `1 ≤ k ≤ n²`.


<Hints
  hint1="Can I write a `feasible(x)` check that returns true iff answer ≤ x (or ≥ x)?"
  hint2="If `feasible` is monotonic in x, binary search over the answer space `[lo, hi]`. Range: min possible value to max possible value."
  hint3="The feasibility check is O(n); total complexity is O(n log range)."
/>
---

<MarkSolved problem-slug="kth-smallest-element-in-a-sorted-matrix" /> <Bookmark problem-slug="kth-smallest-element-in-a-sorted-matrix" />

<InterviewTimer problem-slug="kth-smallest-element-in-a-sorted-matrix" />



## Approach 1 — Flatten + sort

O(n² log n²).

## Approach 2 — Min-heap of rows

Heap starts with each row's head. Pop-then-push-next `k-1` times. O((n+k) log n).

## Approach 3 — Binary search on value

**Insight.** `countLE(v)` = elements ≤ v. Monotonic in v. Binary search for the smallest v with `countLE(v) ≥ k`. `countLE` uses staircase walk from bottom-left: O(n).



```java
int kthSmallest(int[][] m, int k) {
    int n = m.length;
    int lo = m[0][0], hi = m[n - 1][n - 1];
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        int count = 0, r = n - 1, c = 0;
        while (r >= 0 && c < n) {
            if (m[r][c] <= mid) { count += r + 1; c++; }
            else                r--;
        }
        if (count < k) lo = mid + 1;
        else           hi = mid;
    }
    return lo;
}
```



<CodeTrace
  title="BS on value — matrix=[[1,5,9],[10,11,13],[12,13,15]], k=8"
  :values="[1,5,9,10,11,13,12,13,15]"
  :windowKeys="['lo','hi']"
  :cellWidth="34"
  :steps='[
    { pointers: { lo: 1, hi: 15, mid: 8 }, vars: { countLE: 2 }, note: "2 lt 8 → lo=9" },
    { pointers: { lo: 9, hi: 15, mid: 12 }, vars: { countLE: 6 }, note: "6 lt 8 → lo=13" },
    { pointers: { lo: 13, hi: 15, mid: 14 }, vars: { countLE: 8 }, note: "8 ≥ 8 → hi=14" },
    { pointers: { lo: 13, hi: 14, mid: 13 }, vars: { countLE: 8 }, note: "8 ≥ 8 → hi=13" },
    { pointers: { lo: 13, hi: 13 }, vars: { answer: 13 }, note: "converged → 13" }
  ]'
/>

**Complexity** — Time **O(n log(max-min))**; Space **O(1)**.

## Try it yourself

<JavaRunner problem-slug="kth-smallest-element-in-a-sorted-matrix" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Flatten + sort | O(n² log n) | O(n²) |
| Heap of rows | O((n+k) log n) | O(n) |
| BS on value | **O(n log(max-min))** | O(1) |

## When to use which

- **Sorted matrix kth** → BS on value or min-heap merge.
- **BS on value** is cleaner for max n; heap wins for small n.
- **Kth in unsorted** → Quickselect or heap.

<AiCompanion problem-slug="kth-smallest-element-in-a-sorted-matrix" pattern-hint="binary search on answer" />

## Related problems

- [Find K-th Smallest Pair Distance](/problems/find-k-th-smallest-pair-distance)
- [Median of Two Sorted Arrays](/problems/median-of-two-sorted-arrays)
- [Search a 2D Matrix II](https://leetcode.com/problems/search-a-2d-matrix-ii/) — same staircase walk

<FeedbackWidget problem-slug="kth-smallest-element-in-a-sorted-matrix" />
