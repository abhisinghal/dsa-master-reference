# Merge Intervals

*[↗ LeetCode: Merge Intervals](https://leetcode.com/problems/merge-intervals/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/merge-intervals)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg, Apple, Adobe" /&gt;

Given a list of intervals, merge all overlapping ones and return the result.

**Example 1** — `[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`
**Example 2** — `[[1,4],[4,5]]` → `[[1,5]]` (touching = merging by convention)

**Constraints** — `1 ≤ n ≤ 10⁴`.


&lt;Hints
  hint1="Sort by start (or end, depending on the question)."
  hint2="Walk once; each interval either extends the current chunk (overlap) or starts a new one."
  hint3="For ’insert’ or ’intersect’, use the same sweep with a merge/intersection rule at overlaps."
/&gt;
---

## Approach 1 — Brute force (compare every pair)

**Intuition.** For each pair, if they overlap, merge and restart.



```java
int[][] mergeBrute(int[][] intervals) {
    List<int[]> list = new ArrayList<>();
    for (int[] i : intervals) list.add(i);
    boolean changed = true;
    while (changed) {
        changed = false;
        for (int i = 0; i < list.size(); i++)
            for (int j = i + 1; j < list.size(); j++) {
                int[] a = list.get(i), b = list.get(j);
                if (a[1] >= b[0] && b[1] >= a[0]) {
                    list.set(i, new int[]{Math.min(a[0], b[0]), Math.max(a[1], b[1])});
                    list.remove(j);
                    changed = true;
                    break;
                }
            }
    }
    return list.toArray(new int[0][]);
}
```



**Complexity** — Time **O(n³)**; Space **O(n)**. Ugly.

---

## Approach 2 — Sort + one-pass sweep

**Insight from brute.** Sort by start. Then overlap is a local decision: does the current interval start ≤ last-merged end? If yes, extend the end. If no, start a new bucket.



```java
int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
    List<int[]> out = new ArrayList<>();
    int[] last = intervals[0];
    out.add(last);
    for (int i = 1; i < intervals.length; i++) {
        int[] cur = intervals[i];
        if (cur[0] <= last[1]) last[1] = Math.max(last[1], cur[1]);
        else { last = cur; out.add(last); }
    }
    return out.toArray(new int[0][]);
}
```



<CodeTrace
  title="Sort + sweep — [[1,3],[2,6],[8,10],[15,18]]"
  :values="['[1,3]','[2,6]','[8,10]','[15,18]']"
  :windowKeys="['i']"
  :cellWidth="60"
  :steps='[
    { pointers: { i: 0 }, vars: { last: "[1,3]", out: "[[1,3]]" }, note: "seed with first" },
    { pointers: { i: 1 }, vars: { last: "[1,6]", out: "[[1,6]]" }, note: "2 ≤ 3 → overlap, extend end", added: [0,1] },
    { pointers: { i: 2 }, vars: { last: "[8,10]", out: "[[1,6],[8,10]]" }, note: "8 gt 6 → new bucket" },
    { pointers: { i: 3 }, vars: { last: "[15,18]", out: "[[1,6],[8,10],[15,18]]" }, note: "15 gt 10 → new bucket. done" }
  ]'
/>

**Complexity** — Time **O(n log n)** (sorting dominates); Space **O(n)** for output. Optimal.

---

## Try it yourself

<JavaRunner problem-slug="merge-intervals-classic" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Pairwise merge until stable | O(n³) | O(n) |
| Sort + sweep | **O(n log n)** | O(n) |

## When to use which

- **Cold interview** → jump straight to sort+sweep (brute is only worth stating).
- **Touching vs strict overlap** — clarify with the interviewer. `cur[0] <= last[1]` merges touching; `cur[0] < last[1]` keeps them separate.

## Related problems (same ladder applies)

- [Insert Interval](https://leetcode.com/problems/insert-interval/) — insert one, then merge locally
- [Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) — two-pointer over two sorted interval lists
- [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/) — sorted + adjacent check
- [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) — greedy on end times