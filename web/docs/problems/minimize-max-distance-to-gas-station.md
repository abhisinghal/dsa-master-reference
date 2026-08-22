# BS on Answer — Minimize Max Distance to Gas Station

*[↗ LeetCode: Minimize Max Distance to Gas Station](https://leetcode.com/problems/minimize-max-distance-to-gas-station/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/bs-on-answer)

Given sorted station positions and integer `k`, add `k` new stations to minimize the max distance between adjacent stations. Return that distance (real number).

**Example** — `stations=[1,2,3,4,5,6,7,8,9,10], k=9` → `0.5`

---

## Approach 1 — Priority queue (greedy)

Track each gap's current "sub-gap size after splits"; repeatedly split the largest. O(k log n).

## Approach 2 — Binary search on real-number answer

**Insight.** `feasible(D)` = "can we place ≤ k stations so every gap ≤ D?" — for each existing gap `g`, we need `⌈g/D⌉ - 1` splits (i.e. `floor(g/D)` new stations). Total ≤ k.

**Trap.** Real BS: use a small epsilon or a fixed number of iterations to converge.



```java
double minmaxGasDist(int[] s, int k) {
    double lo = 0, hi = s[s.length - 1] - s[0];
    while (hi - lo > 1e-6) {
        double mid = (lo + hi) / 2;
        int count = 0;
        for (int i = 1; i < s.length; i++) count += (int) ((s[i] - s[i - 1]) / mid);
        if (count > k) lo = mid;                                // need more allowed → increase D
        else            hi = mid;
    }
    return lo;
}
```



**Complexity** — Time **O(n log(hi/eps))** ≈ O(n · 30); Space **O(1)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Max-heap greedy | O(k log n) | O(n) |
| Real-number BS | **O(n · log(hi/eps))** | O(1) |

## Related problems

- [Koko Eating Bananas](/problems/bs-on-answer-koko-bananas) — integer BS
- [Divide Chocolate](/problems/divide-chocolate) — maximize-min
- [Path With Minimum Effort](/problems/path-with-minimum-effort)
