# Sweep Line — My Calendar II

*[↗ LeetCode: My Calendar II](https://leetcode.com/problems/my-calendar-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sweep-line)

Implement `book(start, end)` that returns `true` if adding the event `[start, end)` never causes **triple** booking (i.e. no point in time is covered by 3+ events).

**Example** — Series: `book(10,20)=true`, `book(50,60)=true`, `book(10,40)=true`, `book(5,15)=false`, `book(5,10)=true`.

---

## Approach 1 — Track singles + doubles explicitly

**Intuition.** Maintain two lists: intervals covered once, intervals covered twice (double-booked). A new interval fails only if it overlaps any double-booked one. Otherwise, add its intersection with singles → doubles; then add the whole thing to singles.

```java
class MyCalendarTwo {
    List<int[]> singles = new ArrayList<>();
    List<int[]> doubles = new ArrayList<>();
    public boolean book(int s, int e) {
        for (int[] d : doubles) if (s < d[1] && d[0] < e) return false;
        for (int[] one : singles)
            if (s < one[1] && one[0] < e)
                doubles.add(new int[]{Math.max(s, one[0]), Math.min(e, one[1])});
        singles.add(new int[]{s, e});
        return true;
    }
}
```

**Complexity** — Time **O(n)** per booking; Space **O(n)** for both lists.

## Approach 2 — Sweep line via TreeMap of delta counts

**Insight.** Represent every booking as `+1` at start, `-1` at end. Any prefix sum > 2 means a triple booking exists. Try adding the event; if the prefix count breaches 3, roll back.

```java
class MyCalendarTwoSweep {
    TreeMap<Integer, Integer> delta = new TreeMap<>();
    public boolean book(int s, int e) {
        delta.merge(s, 1, Integer::sum);
        delta.merge(e, -1, Integer::sum);
        int active = 0;
        for (int c : delta.values()) {
            active += c;
            if (active >= 3) {
                delta.merge(s, -1, Integer::sum);
                delta.merge(e, 1, Integer::sum);
                return false;
            }
        }
        return true;
    }
}
```

<CodeTrace
  title="Sweep — book series"
  :values="['book(10,20)','book(50,60)','book(10,40)','book(5,15)','book(5,10)']"
  :windowKeys="['op']"
  :cellWidth="72"
  :steps='[
    { pointers: { op: 0 }, vars: { delta: "{10:+1,20:-1}", max: 1 }, note: "book 10-20 → OK", added: [0] },
    { pointers: { op: 1 }, vars: { delta: "+50:+1, 60:-1", max: 1 }, note: "book 50-60 → OK", added: [1] },
    { pointers: { op: 2 }, vars: { delta: "+10:+1, 40:-1", max: 2 }, note: "book 10-40 → double at [10,20), OK", added: [2] },
    { pointers: { op: 3 }, vars: { max: 3, rollback: true }, note: "book 5-15 → triple at [10,15) → REJECT", removed: [3] },
    { pointers: { op: 4 }, vars: { max: 2 }, note: "book 5-10 → OK (touches, doesn`t triple)", added: [4] }
  ]'
/>

**Complexity** — Time **O(n)** per booking (sweep the map); Space **O(n)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Singles + doubles lists | O(n) per op | O(n) |
| TreeMap sweep of deltas | **O(n)** per op | **O(n)** |

## Related problems

- [My Calendar I](https://leetcode.com/problems/my-calendar-i/) — reject even *double* booking
- [My Calendar III](https://leetcode.com/problems/my-calendar-iii/) — return max concurrent bookings so far
- [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii) — offline max concurrency
