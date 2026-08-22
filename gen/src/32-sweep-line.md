# Sweep Line

## Why sweep line exists — the story

Suppose you are watching a hallway with meetings scheduled as intervals: `[0,30]`, `[5,10]`, and `[15,20]`. A direct question like "how many rooms do I need?" sounds like it asks about pairs of meetings: compare every meeting to every other meeting and see what overlaps. That works, but it is the wrong lens. You do not really care which pair overlaps; you care how many meetings are active as time moves forward.

Sweep line changes the input into events. A meeting start is `+1` active meeting, and a meeting end is `-1` active meeting. For the tiny schedule, the events are `(0,+1)`, `(30,-1)`, `(5,+1)`, `(10,-1)`, `(15,+1)`, `(20,-1)`. Sort them by time and scan left to right: active becomes `1` at time 0, `2` at time 5, back to `1` at time 10, up to `2` at time 15, down to `1` at time 20, and finally `0` at time 30. The peak active count is `2`, so two rooms are enough.

> [key] **Key Insight** — Same input, different lens. Merge Intervals asks "which intervals overlap into which?"; sweep line asks "how many are active at time t?". The +1/−1 event stream answers the second in one linear pass.

The pattern gets its name from geometry: imagine a vertical line sweeping across a drawing from left to right. Whenever the line hits the start or end of an interval, your state changes. For meeting rooms the state is a count. For car pooling it is passengers in the car. For skyline it is a max-heap of active building heights. The reusable idea is always the same: sort the moments where state can change, then process them in order.

```svg
<svg width="720" height="240" viewBox="0 0 720 240" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <defs>
    <marker id="swp-ar-blue" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/></marker>
    <filter id="swp-s1" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="var(--dsa-neutral)" flood-opacity="0.5"/></filter>
  </defs>
  <rect x="0" y="0" width="720" height="240" fill="var(--dsa-bg)"/>
  <text x="360" y="24" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-ink)">turn intervals into sorted start/end events, then sweep left → right</text>
  <g font-size="11" fill="var(--dsa-neutral)" text-anchor="end">
    <text x="62" y="58">[0,30]</text><text x="62" y="85">[5,10]</text><text x="62" y="112">[15,20]</text>
  </g>
  <g filter="url(#swp-s1)">
    <rect x="78" y="43" width="572" height="16" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary-line)"/>
    <rect x="180" y="70" width="110" height="16" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/>
    <rect x="400" y="97" width="110" height="16" rx="7" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)"/>
  </g>
  <line x1="70" y1="130" x2="662" y2="130" stroke="var(--dsa-primary)" stroke-width="2" marker-end="url(#swp-ar-blue)"/>
  <g font-size="11" text-anchor="middle" font-weight="700">
    <circle cx="78" cy="130" r="5" fill="var(--dsa-success)"/><text x="78" y="151" fill="var(--dsa-success)">0 +1</text>
    <circle cx="180" cy="130" r="5" fill="var(--dsa-success)"/><text x="180" y="151" fill="var(--dsa-success)">5 +1</text>
    <circle cx="290" cy="130" r="5" fill="var(--dsa-danger)"/><text x="290" y="151" fill="var(--dsa-danger)">10 −1</text>
    <circle cx="400" cy="130" r="5" fill="var(--dsa-success)"/><text x="400" y="151" fill="var(--dsa-success)">15 +1</text>
    <circle cx="510" cy="130" r="5" fill="var(--dsa-danger)"/><text x="510" y="151" fill="var(--dsa-danger)">20 −1</text>
    <circle cx="650" cy="130" r="5" fill="var(--dsa-danger)"/><text x="650" y="151" fill="var(--dsa-danger)">30 −1</text>
  </g>
  <line x1="180" y1="34" x2="180" y2="205" stroke="var(--dsa-primary)" stroke-width="2.5" stroke-dasharray="6 4"/>
  <text x="194" y="42" font-size="11" font-weight="700" fill="var(--dsa-primary)">sweep line at t=5</text>
  <text x="60" y="190" text-anchor="end" font-size="11" font-weight="700" fill="var(--dsa-neutral)">active</text>
  <g filter="url(#swp-s1)" font-size="14" font-weight="700" text-anchor="middle">
    <rect x="61" y="172" width="34" height="28" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><text x="78" y="191" fill="var(--dsa-ink)">1</text>
    <rect x="163" y="172" width="34" height="28" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="180" y="191" fill="var(--dsa-ink)">2</text>
    <rect x="273" y="172" width="34" height="28" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><text x="290" y="191" fill="var(--dsa-ink)">1</text>
    <rect x="383" y="172" width="34" height="28" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="400" y="191" fill="var(--dsa-ink)">2</text>
    <rect x="493" y="172" width="34" height="28" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><text x="510" y="191" fill="var(--dsa-ink)">1</text>
    <rect x="633" y="172" width="34" height="28" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)"/><text x="650" y="191" fill="var(--dsa-ink)">0</text>
  </g>
  <text x="360" y="222" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-neutral)">peak active count = 2 rooms</text>
</svg>
```
<div class="readfig"><b>How to read it:</b> Each interval becomes two events: green starts add <b>+1</b>, red ends add <b>−1</b>. The blue sweep line processes events in sorted order and maintains the running <code>active</code> count. The maximum value in that row is <b>2</b>, so two meetings overlap at peak and two rooms are required.</div>

## When to use it — and when not to

### Recognize by
- *peak concurrency* — "minimum meeting rooms", "maximum number of active sessions", "busiest moment".
- total coverage / uncovered gap on a number line.
- "can capacity ever be exceeded?" — passenger count, CPU load, bandwidth, reservations.
- "timeline of changes" — starts add something, ends remove something.
- "skyline" — max height at every x-coordinate (event = building start/end).
- many intervals where only endpoints matter; nothing changes inside an interval.


<SweepLineAnim />


### When NOT to use it
You need to *reconstruct which intervals were merged* rather than count activity. Use [Merge Intervals](#merge-intervals) instead. Also, if events arrive *online* (no chance to sort up front), reach for a TreeMap or segment tree instead of an event-array sweep.

Also avoid the plain event sweep when:
- intervals are not known in advance and you need instant answers after each insertion.
- the query asks for membership of specific original intervals, not aggregate state.
- coordinates are huge but sparse and you accidentally allocate an array over the coordinate range.
- endpoints have ambiguous inclusivity; decide whether `[1,5]` and `[5,10]` overlap before coding.
- state cannot be updated by a simple add/remove; you may need a heap, multiset, or segment tree as the swept state.

## How to use it — template

```java
List<int[]> events = new ArrayList<>();
for (int[] in : intervals) {
    events.add(new int[]{in[0], +1});        // opening event
    events.add(new int[]{in[1], -1});        // closing event
}
events.sort((a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]);
int active = 0, best = 0;
for (int[] e : events) {
    active += e[1];
    best = Math.max(best, active);
}
return best;
```

The first loop turns intervals into the only moments that matter: starts and ends. The sort creates the left-to-right sweep order. The tie-break is part of the problem definition: with `-1` before `+1`, a meeting ending at `5` frees the room before another meeting starting at `5` asks for one. The scan keeps the current aggregate in `active` and records whatever the problem asks for — maximum, total covered length, first overload, or a list of output segments.


## Sweep-line flavors you should name out loud

Not every sweep line uses the same state. Before coding, decide which flavor you are in:

| Flavor | State carried while sweeping | Example question |
|---|---|---|
| Count sweep | `active += delta` | How many rooms/platforms are needed? |
| Weighted sweep | `load += passengers` | Does car pooling exceed capacity? |
| Coverage sweep | previous coordinate + active count | How many total units are covered by at least one interval? |
| Extremum sweep | heap or multiset of active values | What is the skyline height at each x? |

For coverage length, the scan records distance, not just state. If the previous coordinate was `prev` and current coordinate is `x`, then the segment `[prev, x)` had whatever active count you carried from the last event. If `active > 0`, add `x - prev` to covered length. Then apply all events at `x`. This tiny ordering detail is why sweep line feels subtle at first: the state between events describes the open segment after the previous coordinate, not the point itself.

### Tie-breaks are part of the problem
At equal coordinates, you must know whether an end and a start overlap. For meetings, `[1,5]` followed by `[5,10]` usually uses one room, so process the end before the start. For closed intervals where both endpoints count, touching intervals do overlap, so you may process starts before ends or shift end events by one in integer-coordinate problems. For skyline, starts and ends at the same x need special ordering by height so the silhouette does not briefly dip or spike. Do not treat the comparator as boilerplate; it encodes the interval semantics.

---

## Meeting Rooms II (Minimum Concurrent Intervals) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/)*

<ProgressCheck id="meeting-rooms-ii-minimum-concurrent-intervals" />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <defs>
    <marker id="ar-sweep-primary" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="27" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">sweep events and track active meetings</text>

  <line x1="50" y1="57" x2="350" y2="57" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <g font-size="11" fill="var(--dsa-neutral)" text-anchor="middle">
    <text x="70" y="75">0</text><text x="120" y="75">5</text><text x="170" y="75">10</text><text x="230" y="75">15</text><text x="280" y="75">20</text><text x="330" y="75">30</text>
  </g>
  <rect x="70" y="91" width="260" height="16" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
  <rect x="120" y="119" width="50" height="16" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <rect x="230" y="147" width="50" height="16" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <g font-size="11" font-weight="700" fill="var(--dsa-ink)">
    <text x="74" y="103">[0,30]</text><text x="123" y="131">[5,10]</text><text x="233" y="159">[15,20]</text>
  </g>
  <line x1="145" y1="43" x2="145" y2="176" stroke="var(--dsa-primary)" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#ar-sweep-primary)"/>
  <text x="151" y="42" font-size="11.5" font-weight="700" fill="var(--dsa-primary)">sweep</text>

  <rect x="70" y="185" width="260" height="30" rx="10" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
  <text x="200" y="204" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">count: 0→1→2→1→0, peak = 2</text>
  <text x="200" y="233" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">max concurrency = peak count on sweep</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> Convert every start to +1 and every end to -1, sweep from left to right, and the largest active count is the number of rooms needed.</div>

### Problem
Given meeting time intervals, find the **minimum number of rooms** so that no two overlapping meetings share a room.

**Constraints:** `1 ≤ n ≤ 10⁴`; `start < end`.

**Example 1:** `[[0,30],[5,10],[15,20]]` → `2`.

**Example 2:** `[[7,10],[2,4]]` → `1` because the meetings do not overlap.

### Solution — brute force
A direct baseline checks every interesting time and counts how many intervals cover it.

```java
// Pseudocode baseline:
// best = 0
// for each meeting m as a candidate time:
//     active = number of intervals with interval.start <= m.start < interval.end
//     best = max(best, active)
```

You only need to test meeting start times because the active count can increase only when a meeting starts. This still takes O(n²): for each of `n` starts, scan all `n` intervals. Sweep line compresses those repeated counts into one sorted event stream.

```text
best = 0
for each meeting start t:
    active = 0
    for each interval [s, e):
        if s <= t < e:
            active++
    best = max(best, active)
return best
```

Brute force complexity: O(n²) time and O(1) extra space.

### Solution — optimized
Either a **min-heap of end times** or a **sweep of +1/−1 events**. Both compute the peak number of simultaneously active intervals.

> [key] **Key Insight** — You need a new room only when the earliest-ending active meeting hasn't finished before the next starts. The heap top is that earliest end; reuse the room if it's free.

> [inv] **Invariant (sweep)** — After sorting all start(+1)/end(−1) events by time, the running sum equals the number of active meetings at that instant; the maximum is the room count.

#### Java (heap)
```java
int minMeetingRooms(int[][] meetings) {
    Arrays.sort(meetings, (a, b) -> a[0] - b[0]);          // by start
    PriorityQueue<Integer> ends = new PriorityQueue<>();   // min-heap of end times
    for (int[] m : meetings) {
        if (!ends.isEmpty() && ends.peek() <= m[0]) ends.poll();  // room freed
        ends.offer(m[1]);
    }
    return ends.size();
}
```

> [note] **Trace it** — heap version on `[[0,30],[5,10],[15,20]]`.

<CodeTrace
  title="Meeting Rooms II (heap) — meetings=[[0,30],[5,10],[15,20]]"
  :values="['[0,30]','[5,10]','[15,20]']"
  :windowKeys="['i']"
  :cellWidth="52"
  :steps='[
    { pointers: { i: 0 }, vars: { heap: "[30]", rooms: 1 }, note: "first meeting → room 1 ends at 30" },
    { pointers: { i: 1 }, vars: { heap: "[10,30]", rooms: 2 }, note: "5 lt 30 → need new room. peek=10" },
    { pointers: { i: 2 }, vars: { heap: "[20,30]", rooms: 2 }, note: "15 ≥ 10 → reuse room, replace 10 with 20", added: [2] },
    { pointers: { i: 3 }, vars: { heap: "[20,30]", rooms: 2 }, note: "done. answer = 2 rooms" }
  ]'
/>
#### Java (sweep, tie-break end before start)
```java
int minMeetingRoomsSweep(int[][] meetings) {
    int n = meetings.length;
    int[] starts = new int[n], ends = new int[n];
    for (int i = 0; i < n; i++) { starts[i] = meetings[i][0]; ends[i] = meetings[i][1]; }
    Arrays.sort(starts); Arrays.sort(ends);
    int rooms = 0, best = 0, i = 0, j = 0;
    while (i < n) {
        if (starts[i] < ends[j]) { rooms++; i++; best = Math.max(best, rooms); }
        else { rooms--; j++; }        // a meeting ended: free a room
    }
    return best;
}
```

> [note] **Trace it** — two-array sweep on starts `[0,5,15]` and ends `[10,20,30]`.

<CodeTrace
  title="Meeting Rooms II (two-array sweep) — starts / ends sorted"
  :values="[0,5,10,15,20,30]"
  :windowKeys="['si','ei']"
  :cellWidth="42"
  :steps='[
    { pointers: { si: 0, ei: 0 }, vars: { rooms: 1, peak: 1 }, note: "0 lt 10 → room+" },
    { pointers: { si: 1, ei: 0 }, vars: { rooms: 2, peak: 2 }, note: "5 lt 10 → room+ (2 concurrent)" },
    { pointers: { si: 2, ei: 0 }, vars: { rooms: 1, peak: 2 }, note: "15 ≥ 10 → advance end (5-10 done)" },
    { pointers: { si: 2, ei: 1 }, vars: { rooms: 2, peak: 2 }, note: "15 lt 20 → room+" },
    { pointers: { si: 3, ei: 2 }, vars: { rooms: 2, peak: 2 }, note: "starts exhausted. answer = 2 rooms" }
  ]'
/>
### Time Complexity
Time O(n log n). Sorting starts/ends or meetings dominates; each event or heap operation is processed once.

### Space Complexity
Space O(n). The heap can hold active meeting ends, and the two-array sweep stores all starts and ends.

### Learning notes
- Why store starts and ends separately? — it turns overlap counting into two sorted event streams.
- Why `starts[i] < ends[j]`? — equal time means a room frees before the next meeting starts.
- Why increment `rooms` on a start? — a new active meeting needs capacity right now.
- Why decrement on an end? — that meeting no longer occupies a room.
- Why track `best` instead of returning current rooms? — the answer is the peak concurrency over the whole sweep.
- Why a min-heap alternative? — the smallest end time tells whether the earliest room is reusable.

Additional notes:

Time O(n log n) · Space O(n). The sort dominates. The heap version stores active room end times; the sweep version stores starts and ends.

> [trap] **Common Trap** — Tie at `start == end`. *Example:* meetings `[1,5]` and `[5,10]`. If end-events sort **before** start-events, one room suffices (release, then acquire). If start sorts first, you need 2. LeetCode's *Meeting Rooms II* treats them as one — sort ends first on ties.

<TrapTrace title="Tie at 'start == end'" input="[1,5]" bug="meetings '[1,5]' and '[5,10]'. If end-events sort **before** start-events, one room suffices (release, then acquire). If start sorts first, you need 2. LeetCode's *Meeting Rooms II* treats them as one — sort ends first on ties." fix="See the guidance in the trap description and the code snippet." />

> [note] **Interview script** — First, I'd clarify whether a meeting ending at time `t` frees a room for another starting at `t`; here it does. The brute force is to count active intervals at every start time, which is O(n²). To optimize, I can either sort starts and ends as events or keep a min-heap of active end times. Both are O(n log n); the sweep makes the peak-concurrency idea especially explicit.

> [pat] **Pattern Connection** — Peak-concurrency sweep also solves *Car Pooling*, *Minimum Number of Platforms*, and (with a heap keyed on height) *The Skyline Problem*.

---

## Sweep Line — the general recipe
<p class="secgoal"><b>What & why:</b> the event-sorting template behind interval and scheduling problems. Goal — turn any "how many overlap / when is it busiest" question into a sorted stream of +1/−1 events you scan once.</p>

For any "at each coordinate, what is the aggregate of intervals covering it?" problem:

```text
1. Emit events: (start, +delta) and (end, -delta).
2. Sort events by coordinate; break ties so closings that free capacity
   are processed before openings when intervals touching should not overlap.
3. Sweep left to right, maintaining a running aggregate (count / sum / heap).
4. Record the aggregate (max, or per-segment) as you pass each coordinate.
```

> [key] **Key Insight** — Sweep line converts a 2D "which intervals overlap here" question into a 1D ordered event stream. The state you carry (counter, sum, or a heap of active heights) defines the problem.

### Choosing the swept state
A counter is enough when every interval contributes the same `+1` while active. A running sum handles weighted intervals, like passengers in a car or CPU load from jobs. A heap or multiset is needed when you need the maximum active value, such as skyline height. A `TreeMap` of deltas is the online-friendly version: insert `+delta` and `-delta` as bookings arrive, then scan the ordered map to answer overlap.

### Endpoint policy
Most sweep bugs are endpoint bugs. Decide if intervals are half-open `[start,end)` or closed `[start,end]`. Meeting rooms usually behave like half-open intervals: a meeting ending at 10 does not overlap one starting at 10. Calendar booking problems may define overlap differently. Once you decide, encode it in the tie-break. For half-open counting, process end before start at the same coordinate.


### Online sweep with `TreeMap`
If the intervals arrive one booking at a time, you cannot sort a fresh event array after every call unless the constraints are tiny. The same idea becomes a difference map: add `+1` at `start`, add `-1` at `end`, then scan keys in order to compute the max prefix sum. This is how the My Calendar family is usually introduced. The map stores only coordinates where something changes, so it avoids allocating a giant timeline.

The trade-off is that each query may still scan many keys unless you maintain extra segment-tree information. That distinction is useful in interviews: an event array is best for batch input; a `TreeMap` delta structure is best for moderate online input; a segment tree is for large online input with many queries.

### Coverage example by hand
For intervals `[1,4]` and `[2,6]` as half-open ranges, events are `(1,+1)`, `(4,-1)`, `(2,+1)`, `(6,-1)`. Sweep sorted coordinates `1,2,4,6`. From `1` to `2`, active is 1, so length 1 is covered. From `2` to `4`, active is 2, so length 2 is covered. From `4` to `6`, active is 1, so length 2 is covered. Total covered length is 5, representing `[1,6)`. Notice we never asked which interval owns each point; the active count was enough.

> [note] **Interview script** — First, I'd convert the intervals into events because the active count changes only at endpoints. Then I'd sort the events, explicitly defining the tie-break for equal times. As I sweep left to right, the running count is the number of active intervals, and the maximum is the rooms needed. The brute force is O(n²); sorting events gives O(n log n) time and O(n) space.


### Brute force to optimized, in one mental move
The brute force asks, "for this time, how many intervals contain it?" Sweep line asks the same question for every time in sorted order, while carrying the answer forward. Between two adjacent event times, the active set cannot change, so there is no reason to rescan all intervals. This is the core optimization: replace repeated membership checks with incremental state updates.

### Debugging checklist
When a sweep solution is off by one room or one unit of coverage, check these in order: Are end events ordered before start events for half-open intervals? Are multiple events at the same coordinate grouped or at least processed with the correct tie-break? Are you recording the answer before or after applying the event? Are you using coordinate compression or a map instead of allocating an array from `0` to `10^9`? Most sweep bugs live in those four questions, not in the loop itself.

> [pat] **Pattern Connection** — With a `TreeMap` as the event/difference structure, sweep handles *My Calendar I/II/III* (max booking overlap) online. With a max-heap of active building heights, it yields the skyline silhouette.

### Same pattern, new tweaks

"Turn intervals into +1/−1 events and track the running count" measures peak overlap everywhere:

| Variation | The one thing that changes |
|---|---|
| [Car Pooling](https://leetcode.com/problems/car-pooling/) | +passengers at pickup, −passengers at drop-off; fail as soon as the running load exceeds capacity. |
| [Minimum Number of Platforms](https://leetcode.com/problems/meeting-rooms-ii/) | Train arrival/departure times are just meeting starts/ends with railway names. |
| [My Calendar II / III](https://leetcode.com/problems/my-calendar-ii/) | Use a `TreeMap` of deltas because bookings arrive one at a time. |
| [The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/) | Events add/remove building heights; the swept state is a max-heap or multiset, not a count. |
| [Employee Free Time](https://leetcode.com/problems/employee-free-time/) | Sweep all busy intervals and record gaps where the active count is zero. |

---

## Check your understanding

<Quiz patternId="sweep-line" :questions='[
  {
    "q": "A meeting problem asks for the maximum number active at once. Which lens fits best?",
    "choices": [
      {
        "text": "Sweep line events",
        "correct": true,
        "explanation": "Yes. Starts add active meetings, ends remove them, and the maximum counter is the answer."
      },
      {
        "text": "Quickselect rank"
      },
      {
        "text": "Subsets backtracking"
      },
      {
        "text": "Fast-slow cycle"
      }
    ]
  },
  {
    "q": "For meetings [1,5] and [5,10], how should tied events be ordered when one room can be reused?",
    "choices": [
      {
        "text": "Start before end"
      },
      {
        "text": "End before start",
        "correct": true,
        "explanation": "Correct. Release the room at time 5 before taking the next meeting at time 5."
      },
      {
        "text": "Ignore both events"
      },
      {
        "text": "Sort ties randomly"
      }
    ]
  },
  {
    "q": "Bookings arrive online and you need running overlap counts. Which structure matches the chapter?",
    "choices": [
      {
        "text": "TreeMap of deltas",
        "correct": true,
        "explanation": "Right. Ordered deltas let each booking update the sweep state incrementally."
      },
      {
        "text": "One offline sorted array only"
      },
      {
        "text": "Fixed-size sliding window"
      },
      {
        "text": "Plain recursion tree"
      }
    ]
  }
]' />
