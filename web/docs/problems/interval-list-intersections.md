# Merge Intervals — Interval List Intersections

*[↗ LeetCode: Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/merge-intervals)

&lt;CompanyTags companies="Meta, Google, Amazon" /&gt;

Two lists of **sorted, disjoint** intervals. Return their intersection.

**Example 1** — `A=[[0,2],[5,10],[13,23],[24,25]], B=[[1,5],[8,12],[15,24],[25,26]]` → `[[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]`
**Example 2** — `A=[], B=[[1,2]]` → `[]`

**Constraints** — `0 ≤ A.length, B.length ≤ 1000`.


&lt;Hints
  hint1="Sort by start (or end, depending on the question)."
  hint2="Walk once; each interval either extends the current chunk (overlap) or starts a new one."
  hint3="For ’insert’ or ’intersect’, use the same sweep with a merge/intersection rule at overlaps."
/&gt;
---

&lt;MarkSolved problem-slug="interval-list-intersections" /&gt; &lt;Bookmark problem-slug="interval-list-intersections" /&gt;

&lt;InterviewTimer problem-slug="interval-list-intersections" /&gt;



## Approach 1 — All pairs

O(n·m). Baseline.

## Approach 2 — Two-pointer merge (canonical)

**Insight.** Both lists sorted → at each step, compute intersection of `A[i]` and `B[j]`; advance whichever ends first.

Intersection = `[max(starts), min(ends)]` if nonempty.



```java
int[][] intervalIntersection(int[][] A, int[][] B) {
    List<int[]> out = new ArrayList<>();
    int i = 0, j = 0;
    while (i < A.length && j < B.length) {
        int lo = Math.max(A[i][0], B[j][0]);
        int hi = Math.min(A[i][1], B[j][1]);
        if (lo <= hi) out.add(new int[]{lo, hi});
        if (A[i][1] < B[j][1]) i++; else j++;
    }
    return out.toArray(new int[0][]);
}
```



<CodeTrace
  title="Two-pointer — A=[[0,2],[5,10]], B=[[1,5],[8,12]]"
  :values="['[0,2]','[5,10]','|','[1,5]','[8,12]']"
  :windowKeys="['i','j']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0, j: 0 }, vars: { inter: "[1,2]" }, note: "A ends first → i++" },
    { pointers: { i: 1, j: 0 }, vars: { inter: "[5,5]" }, note: "B ends first → j++" },
    { pointers: { i: 1, j: 1 }, vars: { inter: "[8,10]" }, note: "A ends first → i++" }
  ]'
/>

**Complexity** — Time **O(n + m)**; Space **O(1)** extra.

---

## Try it yourself

<JavaRunner problem-slug="interval-list-intersections" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| All pairs | O(n·m) | O(1) | baseline |
| Two-pointer | **O(n+m)** | O(1) | optimum |

## When to use which

- **Two sorted disjoint lists** → two-pointer.
- **k lists intersection** → generalize with k pointers; complexity O(N·k).
- **"Union of intervals"** → merge intervals template instead.

&lt;AiCompanion problem-slug="interval-list-intersections" pattern-hint="merge intervals" /&gt;

## Related problems

- [Merge Intervals](/problems/merge-intervals-classic)
- [Employee Free Time](/problems/employee-free-time) — k-list union
- [Interval Union / Difference] — variants

&lt;FeedbackWidget problem-slug="interval-list-intersections" /&gt;

&lt;RelatedProblems problems="insert-interval::Insert Interval|my-calendar-ii::My Calendar II|merge-intervals-classic::Merge Intervals Classic" /&gt;
