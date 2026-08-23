# Greedy — Video Stitching

*[↗ LeetCode: Video Stitching](https://leetcode.com/problems/video-stitching/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

<CompanyTags companies="Amazon, Google" />

Cover `[0, T]` with fewest clips `[a, b]`. Return `-1` if impossible.

**Example 1** — `clips=[[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]], T=10` → `3`
**Example 2** — `clips=[[0,1],[1,2]], T=5` → `-1`

**Constraints** — `1 ≤ n ≤ 100`; `0 ≤ T ≤ 100`.


<Hints
  hint1="Is there a local rule that provably gives global optimum? (Exchange argument.)"
  hint2="Sort by the greedy criterion (deadline / end / cost). Iterate; make the locally best choice."
  hint3="If greedy fails, DP is likely needed. But prove greedy’s correctness before writing it."
/>
---

<MarkSolved problem-slug="video-stitching" />

<InterviewTimer problem-slug="video-stitching" />



## Approach — Sort by start + farthest reach (canonical)

**Insight.** Same shape as Jump Game II. Sort by start. Maintain `curEnd`; while iterating clips with `start ≤ curEnd`, extend `farReach`. When exhausted, use one clip (advance `curEnd = farReach`).

```java
int videoStitching(int[][] clips, int T) {
    Arrays.sort(clips, (a, b) -> a[0] - b[0]);
    int used = 0, curEnd = 0, farReach = 0, i = 0;
    while (curEnd < T) {
        while (i < clips.length && clips[i][0] <= curEnd)
            farReach = Math.max(farReach, clips[i++][1]);
        if (farReach <= curEnd) return -1;
        used++; curEnd = farReach;
    }
    return used;
}
```

<CodeTrace
  title="Sort by start + farthest reach (canonical)"
  :values="['0', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="video-stitching" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort + reach | **O(n log n)** | O(1) | canonical |

## When to use which

- **Min intervals covering [0,T]** → farthest reach.
- **Same-start bucket by max-end** → O(T) without sort.

<AiCompanion problem-slug="video-stitching" pattern-hint="greedy" />

## Related problems

- [Jump Game II](/problems/greedy-jump-game-ii)
- [Minimum Number of Taps](https://leetcode.com/problems/minimum-number-of-taps-to-open-to-water-a-garden/)

<FeedbackWidget problem-slug="video-stitching" />
