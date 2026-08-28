# Prefix Sum — Car Pooling

*[↗ LeetCode: Car Pooling](https://leetcode.com/problems/car-pooling/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

<CompanyTags companies="Meta, Amazon, Uber, Lyft" />

Given trips `[numPassengers, from, to]` and car `capacity`, return `true` iff you can carry all passengers without exceeding capacity.

**Example 1** — `trips=[[2,1,5],[3,3,7]], capacity=4` → `false`
**Example 2** — `trips=[[2,1,5],[3,3,7]], capacity=5` → `true`
**Example 3** — `trips=[[2,1,5],[3,5,7]], capacity=3` → `true` (drop-off at 5 before pickup at 5)

**Constraints** — `1 ≤ trips.length ≤ 1000`; `0 ≤ from < to ≤ 1000`. Brute simulates every km — O(sum of trip lengths) = 10⁹ at max (TLE). Diff-array / bucket approach with 10³ stops uses O(trips + stops) = 2·10³ ops.
<Hints
  hint1="Ask: can I answer `sum(i, j)` in O(1) given a preprocessed structure?"
  hint2="Prefix sums let you compute range sums as `pref[j+1] - pref[i]`. For ’count subarrays with property X on sum’, use a hash-map of prefix sums."
  hint3="For ’≥ 2 length’ or ’divisible by k’ variants, store first occurrence and check remainders."
/>
---

<MarkSolved problem-slug="car-pooling" /> <Bookmark problem-slug="car-pooling" />

<InterviewTimer problem-slug="car-pooling" />



## Approach 1 — Sort by time + sweep

Split each trip into (from, +p) and (to, -p) events. Sort. Sweep tracking load.

## Approach 2 — Difference array (canonical)

**Insight.** Same shape as Corporate Flight Bookings. `+p` at `from`, `-p` at `to` — note `to` is **exclusive** for pickup, passenger drops off exactly at that stop.



```java
boolean carPooling(int[][] trips, int capacity) {
    int[] diff = new int[1001];
    for (int[] t : trips) {
        diff[t[1]] += t[0];
        diff[t[2]] -= t[0];
    }
    int load = 0;
    for (int c : diff) {
        load += c;
        if (load > capacity) return false;
    }
    return true;
}
```



<CodeTrace
  title="Diff — trips=[[2,1,5],[3,3,7]], cap=4"
  :values="['0','2','2','5','5','3','3','0']"
  :windowKeys="['t']"
  :cellWidth="30"
  :steps='[
    { pointers: { t: 1 }, vars: { load: 2 }, note: "+2 at stop 1" },
    { pointers: { t: 3 }, vars: { load: 5 }, note: "+3 at stop 3 → 5 > 4 → false" }
  ]'
/>

**Complexity** — Time **O(n + max)**; Space **O(max)**.

---

## Try it yourself

<JavaRunner problem-slug="car-pooling" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Event sort + sweep | O(n log n) | O(n) | acceptable |
| Difference array | **O(n + max)** | O(max) | optimum when max small |

## When to use which

- **Bounded coord range** → difference array.
- **Unbounded / very large coords** → coordinate compress + diff array, or event sweep.
- **Multi-resource capacity** → per-resource diff arrays.

<AiCompanion problem-slug="car-pooling" pattern-hint="prefix sum" />

## Related problems

- [Corporate Flight Bookings](/problems/corporate-flight-bookings)
- [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii)
- [Range Addition](/problems/range-addition)

<FeedbackWidget problem-slug="car-pooling" />

<RelatedProblems problems="prefix-sum-subarray-sum-equals-k::Prefix Sum Subarray Sum Equals K|contiguous-array::Contiguous Array|continuous-subarray-sum::Continuous Subarray Sum" />
