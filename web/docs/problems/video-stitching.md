# Greedy — Video Stitching

*[↗ LeetCode: Video Stitching](https://leetcode.com/problems/video-stitching/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

Cover `[0, T]` with fewest clips `[a, b]`. Return -1 if impossible.

---

## Approach 1 — Sort by start + greedy farthest reach
**Insight.** Sort by start. Track `[curEnd, farReach]`: while iterating clips with `start ≤ curEnd`, extend `farReach`. When we exhaust that batch, use one more clip (advance `curEnd = farReach`).



```java
int videoStitching(int[][] clips, int T) {
    Arrays.sort(clips, (a, b) -> a[0] - b[0]);
    int used = 0, curEnd = 0, farReach = 0, i = 0;
    while (curEnd < T) {
        while (i < clips.length && clips[i][0] <= curEnd)
            farReach = Math.max(farReach, clips[i++][1]);
        if (farReach <= curEnd) return -1;
        used++;
        curEnd = farReach;
    }
    return used;
}
```



**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Approach 2 — Bucket by start; single pass without sort
For each starting time `s`, store the largest end. Sweep — same jump-game logic in O(T).

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort by start + greedy farthest reach | O(n log n) | O(1) | baseline |
| Bucket by start; single pass without sort | O(T) | — | optimum |

## When to use which

- **State it for signal** → Sort by start + greedy farthest reach (O(n log n)). Correct baseline; call it out then move on.
- **Ship this** → Bucket by start; single pass without sort (O(T), —). Expected optimum in interview.

## Related problems

- [Jump Game II](/problems/greedy-jump-game-ii) — same "farthest reach in current layer" idea
- [Minimum Number of Taps to Open to Water a Garden](https://leetcode.com/problems/minimum-number-of-taps-to-open-to-water-a-garden/) — sibling
