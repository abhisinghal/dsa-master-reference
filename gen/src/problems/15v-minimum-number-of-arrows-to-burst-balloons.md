# Greedy — Minimum Number of Arrows to Burst Balloons

*[↗ LeetCode: Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

<CompanyTags companies="Amazon, Google, Meta" />

Balloons span `[xstart, xend]`. Arrow at x bursts every balloon whose span contains x. Min arrows.

**Example 1** — `points=[[10,16],[2,8],[1,6],[7,12]]` → `2`
**Example 2** — `points=[[1,2],[3,4],[5,6],[7,8]]` → `4` (all disjoint)
**Example 3** — `points=[[1,10],[2,3],[4,5]]` → `1` (all overlap the first)

**Constraints** — `1 ≤ n ≤ 10⁵`; `-2³¹ ≤ x ≤ 2³¹−1`. Brute try-every-arrow-position is O(n · range) = potentially 10⁵ · 2³² = 4·10¹⁴ ops. Sort + greedy is O(n log n) = 1.7·10⁶.


<Hints
  hint1="Is there a local rule that provably gives global optimum? (Exchange argument.)"
  hint2="Sort by the greedy criterion (deadline / end / cost). Iterate; make the locally best choice."
  hint3="If greedy fails, DP is likely needed. But prove greedy's correctness before writing it."
/>
---

<MarkSolved problem-slug="minimum-number-of-arrows-to-burst-balloons" /> <Bookmark problem-slug="minimum-number-of-arrows-to-burst-balloons" />

<InterviewTimer problem-slug="minimum-number-of-arrows-to-burst-balloons" />



## Approach 1 — Brute try every subset of arrows

**Intuition.** For each subset of endpoints, check if the arrows placed there burst every balloon. Return the smallest valid subset size.

**Complexity** — Time **O(2ⁿ · n)** subset check; Space **O(n)**. TLE past n=20. Just state as reference: *"this is set-cover in disguise — greedy earliest-end wins."*

---

## Approach 2 — Sort by end + shoot at end of first alive (canonical)

**Insight.** Sort by `xend`. Shoot the first balloon at its end. That arrow bursts every balloon starting ≤ end. Move to first balloon starting > end.

**Trap** — use `Integer.compare` — subtracting can overflow when spans include `INT_MAX/MIN`.

```java
int findMinArrowShots(int[][] points) {
    Arrays.sort(points, (a, b) -> Integer.compare(a[1], b[1]));
    int arrows = 1, end = points[0][1];
    for (int i = 1; i < points.length; i++)
        if (points[i][0] > end) { arrows++; end = points[i][1]; }
    return arrows;
}
```

<CodeTrace
  title="Sort by end + shoot at end of first alive (canonical)"
  :values="['10', '16']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(1)**. *Say aloud in an interview:* "canonical activity-selection variant — sort by end, greedy pick. Same template as Non-overlapping Intervals and Meeting Rooms II counting."

---

## Try it yourself

<JavaRunner problem-slug="minimum-number-of-arrows-to-burst-balloons" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute subsets | O(2ⁿ · n) | O(n) | TLE past n=20 |
| **Sort + shoot** | **O(n log n)** | O(1) | **Canonical** |

## When to use which

- **"Min points to hit all intervals"** → sort by end + greedy.
- **"Which balloons burst by each arrow"** → track intervals per arrow.

<AiCompanion problem-slug="minimum-number-of-arrows-to-burst-balloons" pattern-hint="greedy" />

## Related problems

- [Non-overlapping Intervals](/problems/non-overlapping-intervals)
- [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii)

<FeedbackWidget problem-slug="minimum-number-of-arrows-to-burst-balloons" />

<RelatedProblems problems="jump-game::Jump Game|course-schedule-iii::Course Schedule III|non-overlapping-intervals::Non Overlapping Intervals" />
