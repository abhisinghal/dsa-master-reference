# Sweep Line — Meeting Rooms II

*[↗ LeetCode: Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sweep-line)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg" />

Given meeting intervals `[[start, end)]`, return the minimum number of rooms required.

**Example 1** — `[[0,30],[5,10],[15,20]]` → `2`
**Example 2** — `[[7,10],[2,4]]` → `1`

**Constraints** — `1 ≤ n ≤ 10⁴`; `0 ≤ start < end ≤ 10⁶`.


<Hints
  hint1="Turn events into `(time, +1/-1)` pairs. What’s the ’active count’ or ’max concurrent’?"
  hint2="Sort events by time; break ties consistently (end before start for ’meetings’, or vice versa)."
  hint3="Sweep; maintain a running count/set. Max active gives room count; drops give free slots."
/>
---

## Approach 1 — Brute force (per-minute counter)

**Intuition.** For each minute in `[0..max_end)`, count active meetings; take the max.

```java
int minMeetingRoomsBrute(int[][] meetings) {
    int mx = 0;
    for (int[] m : meetings) mx = Math.max(mx, m[1]);
    int rooms = 0;
    for (int t = 0; t < mx; t++) {
        int active = 0;
        for (int[] m : meetings) if (m[0] <= t && t < m[1]) active++;
        rooms = Math.max(rooms, active);
    }
    return rooms;
}
```

**Complexity** — Time **O(n · max_end)**; Space **O(1)**. Fails when times are large.

---

## Approach 2 — Sort ends + heap of end times

**Insight from brute.** We only care about times where the count *changes*. Sort by start. A min-heap of end times of running meetings: when starting a new one, if the earliest end ≤ new start, reuse that room (replace); otherwise add a new room.

```java
int minMeetingRoomsHeap(int[][] meetings) {
    Arrays.sort(meetings, (a, b) -> a[0] - b[0]);
    PriorityQueue<Integer> ends = new PriorityQueue<>();
    for (int[] m : meetings) {
        if (!ends.isEmpty() && ends.peek() <= m[0]) ends.poll();
        ends.offer(m[1]);
    }
    return ends.size();
}
```

<CodeTrace
  title="Heap approach — meetings=[[0,30],[5,10],[15,20]]"
  :values="['[0,30]','[5,10]','[15,20]']"
  :windowKeys="['i']"
  :cellWidth="52"
  :steps='[
    { pointers: { i: 0 }, vars: { heap: "[30]", rooms: 1 }, note: "first meeting → room 1 ends at 30" },
    { pointers: { i: 1 }, vars: { heap: "[10,30]", rooms: 2 }, note: "5 lt 30 → need new room" },
    { pointers: { i: 2 }, vars: { heap: "[20,30]", rooms: 2 }, note: "15 ≥ 10 → reuse; replace 10 with 20", added: [2] },
    { pointers: { i: 3 }, vars: { heap: "[20,30]", rooms: 2 }, note: "done → 2 rooms" }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(n)**.

---

## Approach 3 — Two-array sweep (chronological events)

**Insight from heap.** Sort **starts** and **ends** separately. Walk both with two pointers. A `start` bumps the counter; a start-time ≥ the smallest end means that end has already fired first — a room freed. Track running max.

```java
int minMeetingRooms(int[][] meetings) {
    int n = meetings.length;
    int[] starts = new int[n], ends = new int[n];
    for (int i = 0; i < n; i++) { starts[i] = meetings[i][0]; ends[i] = meetings[i][1]; }
    Arrays.sort(starts); Arrays.sort(ends);
    int rooms = 0, peak = 0, e = 0;
    for (int s = 0; s < n; s++) {
        if (starts[s] < ends[e]) { rooms++; peak = Math.max(peak, rooms); }
        else                     { e++; }
    }
    return peak;
}
```

**Complexity** — Time **O(n log n)**; Space **O(n)**. No heap, tight and easy to verify.

---

## Try it yourself

<JavaRunner problem-slug="sweep-line-meeting-rooms-ii" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Per-minute counter | O(n · max_end) | O(1) |
| Heap of end times | O(n log n) | O(n) |
| Two-array sweep | **O(n log n)** | O(n) |

## When to use which

- **Cold interview** → walk brute → heap → two-array. Show the "we only care about events" reframing.
- **Tie at `start == end`** → decide with the interviewer: touching = one room or two?

<AiCompanion problem-slug="sweep-line-meeting-rooms-ii" pattern-hint="sweep line" />

## Related problems (same ladder applies)

- [Car Pooling](https://leetcode.com/problems/car-pooling/) — same shape with capacity checks
- [The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/) — sweep + heap for max heights over intervals
- [My Calendar II](https://leetcode.com/problems/my-calendar-ii/) — sweep with 2-limit constraint
- [Employee Free Time](https://leetcode.com/problems/employee-free-time/) — flatten schedules, then find gaps