# Greedy — Non-overlapping Intervals

*[↗ LeetCode: Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

<CompanyTags companies="Amazon, Google, Meta" />

Min intervals to remove so the rest are non-overlapping.

**Example 1** — `intervals=[[1,2],[2,3],[3,4],[1,3]]` → `1`
**Example 2** — `intervals=[[1,2],[1,2],[1,2]]` → `2`
**Example 3** — `intervals=[[1,2],[2,3]]` → `0`

**Constraints** — `1 ≤ n ≤ 10⁵`. Brute enumerating subsets is `2ⁿ = 10³⁰¹⁰³` — universe-age. Sort + greedy is O(n log n) = 10⁵ · 17 = 1.7·10⁶.


<Hints
  hint1="Is there a local rule that provably gives global optimum? (Exchange argument.)"
  hint2="Sort by the greedy criterion (deadline / end / cost). Iterate; make the locally best choice."
  hint3="If greedy fails, DP is likely needed. But prove greedy's correctness before writing it."
/>
---

<MarkSolved problem-slug="non-overlapping-intervals" /> <Bookmark problem-slug="non-overlapping-intervals" />

<InterviewTimer problem-slug="non-overlapping-intervals" />



## Approach 1 — Brute subset enumeration

**Intuition.** Try every subset. For each, check non-overlapping. Return `n - max_valid_size`.

**Complexity** — Time **O(2ⁿ · n log n)**; Space **O(n)**. TLE past n=20. Just state as the reference: "we're maximising a compatible subset, which is the *activity selection* pattern."

---

## Approach 2 — Sort by end + activity selection (canonical)

**Insight.** Equivalent to maximizing non-overlapping intervals; count to remove = `n - maxKept`. Sort by **end** (not start!); greedily keep every interval whose start ≥ previous end.

**Why end-sort works (exchange argument).** Take any optimal set. The first interval must end at some time `t`. If we swap it for the interval with the *earliest possible end*, the remaining budget is at least as generous. Repeat: optimal converges to greedy.



```java
int eraseOverlapIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[1] - b[1]);
    int kept = 0, end = Integer.MIN_VALUE;
    for (int[] iv : intervals) if (iv[0] >= end) { end = iv[1]; kept++; }
    return intervals.length - kept;
}
```



<CodeTrace
  title="Sort by end + activity selection (canonical)"
  :values="['1', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(1)**. *Say aloud in an interview:* "earliest-deadline-first is the canonical activity-selection template — same trick powers Minimum Arrows to Burst Balloons and Max Length of Pair Chain."

---

## Try it yourself

<JavaRunner problem-slug="non-overlapping-intervals" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute subsets | O(2ⁿ · n log n) | O(n) | Reference; TLE past n=20 |
| **Sort by end + greedy** | **O(n log n)** | O(1) | **Canonical** |

## When to use which

- **"Min remove"** → n − maxKept.
- **"Max keep"** → same skeleton, return count.
- **"Weighted intervals"** → interval scheduling DP.

<AiCompanion problem-slug="non-overlapping-intervals" pattern-hint="greedy" />

## Related problems

- [Maximum Length of Pair Chain](/problems/maximum-length-of-pair-chain)
- [Minimum Arrows](/problems/minimum-number-of-arrows-to-burst-balloons)
- [Meeting Rooms](/problems/meeting-rooms)

<FeedbackWidget problem-slug="non-overlapping-intervals" />

<RelatedProblems problems="best-time-to-buy-and-sell-stock::Best Time To Buy And Sell Stock|course-schedule-iii::Course Schedule III|jump-game::Jump Game" />
