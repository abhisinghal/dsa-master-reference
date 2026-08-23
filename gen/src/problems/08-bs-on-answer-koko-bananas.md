# Binary Search on Answer — Koko Eating Bananas

*[↗ LeetCode: Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/bs-on-answer)

<CompanyTags companies="Google, Amazon, Meta" />

Koko has `n` piles of bananas, `piles[i]` in each. She can eat at speed `k` bananas/hour. Each hour she picks one pile; if it has ≥ `k` bananas she eats `k`, otherwise she eats the whole pile (and rests the remainder of that hour). She must finish all piles in `h` hours. Return the minimum `k`.

**Example 1** — `piles=[3,6,7,11], h=8` → `4`
**Example 2** — `piles=[30,11,23,4,20], h=5` → `30`
**Example 3** — `piles=[30,11,23,4,20], h=6` → `23`

**Constraints** — `1 ≤ n ≤ 10⁴`; `1 ≤ piles[i] ≤ 10⁹`; `n ≤ h ≤ 10⁹`.


<Hints
  hint1="Can I write a `feasible(x)` check that returns true iff answer ≤ x (or ≥ x)?"
  hint2="If `feasible` is monotonic in x, binary search over the answer space `[lo, hi]`. Range: min possible value to max possible value."
  hint3="The feasibility check is O(n); total complexity is O(n log range)."
/>
---

<MarkSolved problem-slug="bs-on-answer-koko-bananas" />

<InterviewTimer problem-slug="bs-on-answer-koko-bananas" />



## Approach 1 — Brute force (try every speed)

**Intuition.** Try `k = 1, 2, 3, …` in order; return the first `k` that finishes on time.

```java
int minEatingSpeedBrute(int[] piles, int h) {
    for (int k = 1; ; k++) {
        long hours = 0;
        for (int p : piles) hours += (p + k - 1) / k;
        if (hours <= h) return k;
    }
}
```

**Complexity** — Time **O(max(piles) · n)** worst-case; Space **O(1)**. At `piles[i] = 10⁹` this is a trillion operations. TLE.

---

## Approach 2 — Binary search on the answer

**Insight from brute.** The `feasible(k)` predicate is **monotonic**: if speed `k` finishes on time, then every `k' > k` also does. That's a sorted boolean array of `[false, false, …, true, true, …]`. Binary search for the first `true`.

**Range.** `lo = 1`, `hi = max(piles)`. Any speed above `max(piles)` finishes in exactly `n` hours (one pile per hour), which fits since `n ≤ h`.

**Trap.** Get the feasibility direction right: `feasible(k) = totalHours(k) ≤ h`. Flipping this returns the *fastest failing* speed instead of the slowest passing one.

```java
int minEatingSpeed(int[] piles, int h) {
    int lo = 1, hi = 0;
    for (int p : piles) hi = Math.max(hi, p);
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (feasible(piles, mid, h)) hi = mid;   // keep candidate
        else                          lo = mid + 1;
    }
    return lo;
}
private boolean feasible(int[] piles, int k, int h) {
    long hours = 0;
    for (int p : piles) hours += (p + k - 1) / k;
    return hours <= h;
}
```

<CodeTrace
  title="BS on answer — piles=[3,6,7,11], h=8"
  :values="[3,6,7,11]"
  :windowKeys="['lo','hi']"
  :cellWidth="46"
  :steps='[
    { pointers: { lo: 1, hi: 11, mid: 6 }, vars: { hours: 6, ok: true }, note: "speed 6 → 6 hrs ≤ 8 → hi=mid=6" },
    { pointers: { lo: 1, hi: 6, mid: 3 }, vars: { hours: 10, ok: false }, note: "speed 3 → 10 hrs → lo=mid+1=4" },
    { pointers: { lo: 4, hi: 6, mid: 5 }, vars: { hours: 8, ok: true }, note: "speed 5 → 8 hrs → hi=5" },
    { pointers: { lo: 4, hi: 5, mid: 4 }, vars: { hours: 8, ok: true }, note: "speed 4 → 8 hrs → hi=4" },
    { pointers: { lo: 4, hi: 4 }, vars: { answer: 4 }, note: "converged → return 4" }
  ]'
/>

**Complexity** — Time **O(n log max)**; Space **O(1)**. Optimal.

---

## Try it yourself

<JavaRunner problem-slug="bs-on-answer-koko-bananas" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Linear scan on k | O(n · max) | O(1) |
| Binary search on answer | **O(n log max)** | O(1) |

## When to use which

- **"Minimum X such that … works"** or **"maximum X such that … works"** → BS on answer.
- **Sanity-check the feasibility direction**: `feasible(minSpeed)` should be `false`, `feasible(maxSpeed)` should be `true`. If not, you have the polarity wrong.

<AiCompanion problem-slug="bs-on-answer-koko-bananas" pattern-hint="binary search on answer" />

## Related problems (same ladder applies)

- [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) — same skeleton with capacity as the answer
- [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) — feasibility: can we split into ≤ m parts each with sum ≤ cap
- [Minimize Max Distance to Gas Station](https://leetcode.com/problems/minimize-max-distance-to-gas-station/) — real-number BS on max gap
- [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) — BS on the partition point

<FeedbackWidget problem-slug="bs-on-answer-koko-bananas" />
