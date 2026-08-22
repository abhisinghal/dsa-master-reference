# Merge Intervals — Interval List Intersections

*[↗ LeetCode: Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/merge-intervals)

Given two lists of pairwise-disjoint intervals sorted by start, return their intersections.

**Example** — `A=[[0,2],[5,10]], B=[[1,5],[8,12]]` → `[[1,2],[5,5],[8,10]]`

---

## Approach 1 — Brute nested pair

O(n·m). Wasteful.

## Approach 2 — Two pointers on both sorted lists

**Insight.** Intersection of `A[i]` and `B[j]` is `[max(starts), min(ends)]`, valid iff `max ≤ min`. Advance whichever interval ends first.



```java
int[][] intervalIntersection(int[][] A, int[][] B) {
    List<int[]> out = new ArrayList<>();
    int i = 0, j = 0;
    while (i < A.length && j < B.length) {
        int lo = Math.max(A[i][0], B[j][0]);
        int hi = Math.min(A[i][1], B[j][1]);
        if (lo <= hi) out.add(new int[]{lo, hi});
        if (A[i][1] < B[j][1]) i++;
        else                   j++;
    }
    return out.toArray(new int[0][]);
}
```



<CodeTrace
  title="Two-pointer — A=[[0,2],[5,10]], B=[[1,5],[8,12]]"
  :values="['[0,2]','[5,10]']"
  :windowKeys="['i']"
  :cellWidth="60"
  :steps='[
    { pointers: { i: 0, j: 0 }, vars: { lo: 1, hi: 2 }, note: "intersect [1,2]. A[0] ends first → i++", added: [0] },
    { pointers: { i: 1, j: 0 }, vars: { lo: 5, hi: 5 }, note: "intersect [5,5]. B[0] ends first → j++", added: [1] },
    { pointers: { i: 1, j: 1 }, vars: { lo: 8, hi: 10 }, note: "intersect [8,10]. A[1] ends first → i++. done", added: [1] }
  ]'
/>

**Complexity** — Time **O(n + m)**; Space **O(n + m)** output.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute nested | O(n·m) | O(output) |
| Two pointers | **O(n + m)** | O(output) |

## Related problems

- [Merge Intervals](/problems/merge-intervals-classic) — one list
- [Employee Free Time](/problems/employee-free-time) — flatten multiple sorted lists
- [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii)
