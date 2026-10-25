# Sweep Line


<PatternVideo pattern-name="Sweep Line" duration="8–12 min" />

<PatternProgress pattern-id="sweep-line" problems="meeting-rooms-ii, my-calendar-ii, the-skyline-problem, car-pooling, employee-free-time" />

<script setup>
const bareTemplateCode = `# python — count sweep
events = []
for s, e in intervals:
    events.append((s, +1))     # opening
    events.append((e, -1))     # closing
# tie-break: closings before openings at the same t (half-open semantics)
events.sort(key=lambda ev: (ev[0], ev[1]))
active, best = 0, 0
for t, delta in events:
    active += delta
    best = max(best, active)
return best`

const bareInvariant = {
  statement: `After processing all events with timestamp \`<= t\`, \`active\` equals the number of intervals that cover point \`t\` under half-open \`[s, e)\` semantics; \`best\` is the maximum \`active\` seen so far.`,
  initialization: `Before entering the loop, \`active = 0\` and \`best = 0\`. No events processed, no intervals active — correct.`,
  maintenance: `Each event is either \`+1\` (an interval starts) or \`-1\` (an interval ends). Adding the delta is the atomic change in membership at that timestamp. The sort order and tie-break (-1 before +1 at the same time) ensure that an interval ending at \`t\` releases its slot before another interval starting at \`t\` claims it, which encodes half-open semantics. After the update, \`best = max(best, active)\` keeps the running maximum current.`,
  termination: `Once all events are consumed, \`active = 0\` (every \`+1\` has a matching \`-1\`) and \`best\` records the peak concurrency across the entire sweep.`
}

const bareComplexity = {
  time: `O(n log n) — sorting dominates; the scan is O(n).`,
  space: `O(n) for the event array.`
}

const templateSpecializations = [
  { slug: `max-simultaneous-overlap-medium`, title: `Max simultaneous overlap` },
  { slug: `meeting-rooms-ii-medium`, title: `Meeting Rooms II` },
  { slug: `car-pooling-medium`, title: `Car Pooling` },
  { slug: `the-skyline-problem-hard`, title: `Skyline` },
  { slug: `employee-free-time-hard`, title: `Employee Free Time` }
]

const maxSimulInvariant = {
  statement: `After processing all events with timestamp \`<= t\`, \`active\` equals the number of intervals covering \`t\`.`,
  initialization: `Before the loop, \`active = 0\`. No intervals have started, so zero cover any point.`,
  maintenance: `Each event is \`+1\` on an open or \`-1\` on a close. The sort places events in timestamp order; the tie-break puts closes before opens, encoding half-open semantics (end-touching-start is not an overlap). After adding the delta, \`active\` reflects the exact set covering \`t\`.`,
  termination: `All events consumed. \`best\` is the max covering count ever seen; by the invariant, that's the max simultaneous overlap.`
}

const carPoolingCode = `# python — diff-array sweep over fixed 1001-stop route
def car_pooling(trips, capacity):
    diff = [0] * 1001
    for passengers, start, end in trips:
        diff[start] += passengers    # pick up
        diff[end]   -= passengers    # drop off (half-open: no one is on at 'end')
    load = 0
    for d in diff:
        load += d
        if load > capacity:
            return False
    return True`

const carPoolingInvariant = {
  statement: `After the prefix sum reaches stop \`k\`, \`load\` equals the number of passengers currently in the car at the half-open interval \`[k, k+1)\`.`,
  initialization: `At \`k = 0\` before the loop, \`load = 0\` — the car is empty.`,
  maintenance: `\`diff[k]\` is the net passenger change at stop \`k\`: pickups add, drop-offs subtract. The prefix-sum step \`load += diff[k]\` applies that change. Because drop-offs are recorded at the drop-off stop (not drop-off+1), a trip \`[p, s, e]\` contributes \`+p\` to the running load only while \`s <= k < e\` — exactly the half-open semantics the problem specifies.`,
  termination: `At the final stop, \`load = 0\` (every pickup has a matching drop-off). If \`load > capacity\` ever fired, we already returned \`False\`.`
}

const skylineCode = `# python — sweep + max-heap with lazy deletion
import heapq
def getSkyline(buildings):
    events = []
    for L, R, H in buildings:
        events.append((L, -H, R))    # start: negative H for max-heap
        events.append((R, 0, 0))     # end sentinel to force a check
    events.sort()
    out, heap = [], [(0, float('inf'))]   # (neg-height, right-edge)
    for x, negH, R in events:
        if negH != 0:
            heapq.heappush(heap, (negH, R))
        while heap[0][1] <= x:            # lazy pop expired buildings
            heapq.heappop(heap)
        cur_h = -heap[0][0]
        if not out or out[-1][1] != cur_h:
            out.append([x, cur_h])
    return out`

const skylineInvariant = {
  statement: `At every sweep point \`x\`, the heap top (after lazy popping) is the tallest building whose x-span still covers \`x\`.`,
  initialization: `Before the sweep, the heap contains only the sentinel \`(0, inf)\` representing "ground, extending forever."`,
  maintenance: `When x passes an \`(L, -H, R)\` start event, that building \`(negH, R)\` is pushed; the heap top may change if \`-H\` beats the previous top. The while-loop lazily pops any \`(negH', R')\` with \`R' <= x\` — these buildings no longer cover \`x\`. After pushes and pops, the top is the max active height. If it differs from \`out[-1][1]\`, a skyline key point exists.`,
  termination: `All events processed. The heap drains back to the ground sentinel; the final emitted point at the last right edge is at height 0.`
}

const freeTimeCode = `# python — merge all busy intervals via sweep, emit zero-active gaps
def employeeFreeTime(schedule):
    events = []
    for employee in schedule:
        for iv in employee:
            events.append((iv.start, +1))
            events.append((iv.end,   -1))
    events.sort(key=lambda ev: (ev[0], ev[1]))
    out, active, prev_end = [], 0, None
    for t, delta in events:
        if active == 0 and prev_end is not None and prev_end < t:
            out.append(Interval(prev_end, t))     # a gap!
        active += delta
        if active == 0:
            prev_end = t
    return out`

const freeTimeInvariant = {
  statement: `At every moment during the sweep, \`active = 0\` iff NO employee is busy at that instant; \`prev_end\` is the last time \`active\` fell to 0.`,
  initialization: `Before the sweep, \`active = 0\` and \`prev_end = None\` — no events seen, no "last fall to zero" yet.`,
  maintenance: `At each event the delta is \`+1\` (an employee's interval opens) or \`-1\` (one closes). The running sum therefore equals the count of employees busy at that instant. Just before applying a \`+1\` event, if \`active = 0\` and \`prev_end\` is set, the open interval \`(prev_end, t)\` was free time for everyone — emit it. After applying, update \`prev_end\` on the way back down to 0.`,
  termination: `All events consumed. All busy windows have been swept; every maximal interval during which \`active = 0\` has been emitted.`
}

const trapAcode = {
  statement: `Tie-break at \`start == end\`: closings before openings for half-open \`[s,e)\`.`,
  bug: `Meetings \`[1,5]\` and \`[5,10]\` — if the \`+1\` at 5 fires before the \`-1\` at 5, \`active\` momentarily becomes 2 and you report "need 2 rooms" when 1 would suffice.`,
  fix: `In the sort key, make \`-1\` events sort first on equal timestamps. Python: \`events.sort(key=lambda ev: (ev[0], ev[1]))\` works because \`-1 < +1\`. Java: \`(a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]\`. Decide if the problem is half-open before coding.`
}

const trapBcode = {
  statement: `Reporting the aggregate before applying the event instead of after.`,
  bug: `For max-concurrency, swapping \`active += delta\` and \`best = max(best, active)\` has you record the OLD state when the event causes a spike — you miss the peak by one.`,
  fix: `For peak-max: update \`active\` first, then record \`best\`. For coverage-length (where you measure the segment BEFORE the event): record using OLD \`active\`, then update. Different problems need different orders — write out which "between-event state" you're measuring before coding.`
}

const trapCcode = {
  statement: `Allocating an event-length array over coordinate space on huge or sparse coordinates.`,
  bug: `Car Pooling restricts stops to 0..1000, so a 1001-cell diff-array works. But for timestamps in Unix seconds or geographic longitudes (\`10^9\` scale), the same approach OOMs or TLEs. You can't allocate a billion-cell array.`,
  fix: `For dense small-domain coordinates (0..N): diff array is optimal. For sparse large-domain coordinates: event list sorted by timestamp (as in the canonical template), or a \`TreeMap<coord, delta>\` for online. Decide from the constraint, not habit.`
}

const quizQuestions = [
  {q: "What events do you emit for the classic Meeting Rooms II problem?", choices: [{text: "(start, +1) and (end, -1)", correct: true, explanation: "Sweep time; maintain running count; max is the answer."}, {text: "(start, meeting)", correct: false}, {text: "(start, +1) only", correct: false}, {text: "Interval midpoints", correct: false}]},
  {q: "For The Skyline Problem, what data structure processes active heights?", choices: [{text: "Max-heap (with lazy removal) or a TreeMap", correct: true, explanation: "You need max-active at each event."}, {text: "Min-heap", correct: false, explanation: "You want max, not min."}, {text: "Simple stack", correct: false}, {text: "Queue", correct: false}]},
  {q: "In sweep events, why does the tie-break 'end before start at same time' matter for Meeting Rooms II?", choices: [{text: "A meeting ending exactly when another starts doesn't need a new room", correct: true, explanation: "End-first tie-break correctly reuses rooms."}, {text: "It doesn't matter", correct: false}, {text: "For alphabetical ordering", correct: false}, {text: "To avoid duplicates", correct: false}]},
  {q: "For Car Pooling on constrained coordinates (0..1000), what structure is optimal?", choices: [{text: "Difference array indexed by stop", correct: true, explanation: "O(n + K) where K=1001; no sort needed."}, {text: "Sorted event list", correct: false, explanation: "Works but O((n+K) log n) is unnecessary."}, {text: "Segment tree", correct: false, explanation: "Overkill for a bounded 1D domain."}, {text: "Min-heap", correct: false}]},
  {q: "Sweep Line vs Difference Array: when is Sweep Line preferred?", choices: [{text: "When coordinates are unbounded / very sparse", correct: true, explanation: "Diff arrays need contiguous integer coords; sweep works on any comparable timestamps."}, {text: "When coordinates are 1..n dense", correct: false, explanation: "Diff arrays are perfect there."}, {text: "Always", correct: false}, {text: "Never", correct: false}]}
]

const mrIIsolvePrompt = `Given meeting intervals, return the minimum number of rooms. Example: \`[[0,30],[5,10],[15,20]]\` → 2.`

const carPoolingSolvePrompt = `Given trips \`[[passengers, start, end], ...]\` and a car \`capacity\`, decide whether the car can serve all trips. Stops are integers 0..1000.`

const skylineSolvePrompt = `Given buildings \`[[L, R, H], ...]\`, return the skyline silhouette as key points \`[[x, height], ...]\` where the height changes.`

const freeTimeSolvePrompt = `Given each employee's busy intervals, return the common free time (intervals where everyone is simultaneously free).`
</script>

## Why sweep line exists — the story

You're an SRE at Uber. Every ride creates a `driver_online` event at time `t_start` and a `driver_offline` event at time `t_end`. Your dashboard shows: **"How many drivers are on the road at any moment during the peak-hour surge?"**

The obvious approach: for every timestamp in the surge window, count how many `[t_start, t_end]` ranges contain it. With 100,000 drivers and one query per second, that's `10⁵` interval-containment checks per query × 3600 queries per hour = **3.6·10⁸ ops per hour**. Doable for one dashboard. But now imagine a company like Uber with 200 cities, each running this analytic, and you're at `7·10¹⁰` ops per hour. Fleet dies.

And the naive approach re-does work. When time advances from `12:00:00` to `12:00:01`, the driver count changes by *at most a handful* — someone came online, someone finished a ride. Yet the naive scan asks the question from scratch on every second. **Every one of those 100,000 checks is unchanged from the previous second.**

The pattern is **sweep line**: turn intervals into a stream of events. A `driver_online` event is `+1`. A `driver_offline` is `−1`. Sort all events by time. Scan left to right, maintaining a running `active` counter. Now the "how many drivers online at time t" query is just: **read the counter after processing events up to time t**. **O(n log n)** sort + **O(n)** scan, answers *every* time-point query in the surge window in a single pass. 3.6·10⁸ ops per hour → about 2·10⁵. **Four orders of magnitude faster.**

The pattern gets its name from geometry: imagine a vertical line sweeping across a drawing from left to right. Whenever the line hits the start or end of an interval, your state changes. For meeting rooms the state is a count. For car pooling it is passengers in the car. For skyline it is a max-heap of active building heights. The reusable idea is always the same: sort the moments where state can change, then process them in order.

> [key] **Key Insight** — Same input, different lens. Merge Intervals asks "which intervals overlap into which?"; sweep line asks "how many are active at time t?". The +1/−1 event stream answers the second in one linear pass.

## The bare mechanic — simplest working example

Three meetings: `[0,30]`, `[5,10]`, `[15,20]`. Turn each into two events, sort, scan:

| event | time | delta | active after | best |
|---|---|---|---|---|
| start [0,30] | 0 | +1 | 1 | 1 |
| start [5,10] | 5 | +1 | 2 | 2 |
| end [5,10] | 10 | −1 | 1 | 2 |
| start [15,20] | 15 | +1 | 2 | 2 |
| end [15,20] | 20 | −1 | 1 | 2 |
| end [0,30] | 30 | −1 | 0 | 2 |

```svg
<svg role="img" viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Bare mechanic sweep">
  <rect x="0" y="0" width="400" height="180" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">+1 on start, -1 on end, scan sorted events</text>
  <line x1="30" y1="60" x2="370" y2="60" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <g text-anchor="middle" font-size="10" fill="var(--dsa-neutral)">
    <text x="40" y="78">0</text><text x="100" y="78">5</text><text x="160" y="78">10</text><text x="220" y="78">15</text><text x="280" y="78">20</text><text x="360" y="78">30</text>
  </g>
  <g font-size="11" font-weight="700" text-anchor="middle">
    <circle cx="40" cy="60" r="5" fill="var(--dsa-success)"/><text x="40" y="98" fill="var(--dsa-success)">+1</text>
    <circle cx="100" cy="60" r="5" fill="var(--dsa-success)"/><text x="100" y="98" fill="var(--dsa-success)">+1</text>
    <circle cx="160" cy="60" r="5" fill="var(--dsa-danger)"/><text x="160" y="98" fill="var(--dsa-danger)">-1</text>
    <circle cx="220" cy="60" r="5" fill="var(--dsa-success)"/><text x="220" y="98" fill="var(--dsa-success)">+1</text>
    <circle cx="280" cy="60" r="5" fill="var(--dsa-danger)"/><text x="280" y="98" fill="var(--dsa-danger)">-1</text>
    <circle cx="360" cy="60" r="5" fill="var(--dsa-danger)"/><text x="360" y="98" fill="var(--dsa-danger)">-1</text>
  </g>
  <text x="30" y="130" font-size="10" font-weight="700" fill="var(--dsa-neutral)">active:</text>
  <g font-size="12" font-weight="700" text-anchor="middle" fill="var(--dsa-ink)">
    <text x="40" y="132">1</text><text x="100" y="132">2</text><text x="160" y="132">1</text><text x="220" y="132">2</text><text x="280" y="132">1</text><text x="360" y="132">0</text>
  </g>
  <text x="200" y="160" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-primary)">peak = 2 — two rooms needed</text>
</svg>
```

<PatternTemplateCard
  slug="sweep-line-bare"
  language="python"
  :code="bareTemplateCode"
  :invariant="bareInvariant"
  :complexity="bareComplexity"
  problemShape="list of intervals; return peak overlap (count sweep)"
  defaultRevealed />

## When to use it — and when not to

### Recognize by
- *peak concurrency* — "minimum meeting rooms", "maximum number of active sessions", "busiest moment".
- total coverage / uncovered gap on a number line.
- "can capacity ever be exceeded?" — passenger count, CPU load, bandwidth, reservations.
- "timeline of changes" — starts add something, ends remove something.
- "skyline" — max height at every x-coordinate (event = building start/end).
- many intervals where only endpoints matter; nothing changes inside an interval.

### When NOT to use it
You need to *reconstruct which intervals were merged* rather than count activity. Use Merge Intervals instead. Also, if events arrive *online* (no chance to sort up front), reach for a TreeMap or segment tree instead of an event-array sweep.

Also avoid the plain event sweep when:
- intervals are not known in advance and you need instant answers after each insertion.
- the query asks for membership of specific original intervals, not aggregate state.
- coordinates are huge but sparse and you accidentally allocate an array over the coordinate range.
- endpoints have ambiguous inclusivity; decide whether `[1,5]` and `[5,10]` overlap before coding.
- state cannot be updated by a simple add/remove; you may need a heap, multiset, or segment tree as the swept state.

## History — Bentley-Ottmann sweep, 1979

The sweep-line technique was formalized by **Jon Bentley and Thomas Ottmann in 1979** for the classical problem of finding *all* intersection points among `n` line segments in a 2D plane. Their algorithm sweeps a vertical line from left to right, maintaining a **binary search tree of active segments** ordered by their y-coordinate at the sweep line. When a segment starts, it's inserted; when it ends, it's removed; segment intersections happen precisely when adjacent segments in the BST swap order. Total complexity: **O((n + k) log n)** where `k` is the number of intersections — a huge win over the naive O(n²) brute force.

The idea generalized beyond geometry. **Franco Preparata and Michael Shamos**'s foundational textbook *Computational Geometry* (1985) devoted an entire chapter to the pattern. Today, the "sweep as event-processing" metaphor is the mental model behind every event-driven state machine.

## THE template

Four flavors share one shape. The state you carry while sweeping decides which flavor you're in:

| Flavor | State carried | Example question |
|---|---|---|
| Count sweep | `active += delta` | How many rooms are needed? |
| Weighted sweep | `load += passengers` | Does car pooling exceed capacity? |
| Extremum sweep | heap or multiset of active values | What is the skyline height at each x? |
| Coverage sweep | previous coordinate + active flag | What length of the number line is covered? |

<PatternTemplateCard
  slug="sweep-line-canonical"
  title="Sweep-line canonical event sweep"
  language="python"
  :code="bareTemplateCode"
  :invariant="bareInvariant"
  :complexity="bareComplexity"
  :specializations="templateSpecializations"
  problemShape="intervals → (start,+1)/(end,-1) events → sort → scan with running state" />

## Interactive diagram

<SweepLineAnim />

## Sub-variations of the template

<PatternSubVariationNav pattern="sweep-line" />

### Max simultaneous overlap <span class="diff diff-m">Medium</span>

The **bare mechanic** written as its own problem: "At what moment are the most intervals simultaneously active, and what is that count?"

<InvariantProof
  :statement="maxSimulInvariant.statement"
  :initialization="maxSimulInvariant.initialization"
  :maintenance="maxSimulInvariant.maintenance"
  :termination="maxSimulInvariant.termination" />

**Trace** on `[[1,5], [2,6], [8,10]]`:
- Events sorted: `(1,+1), (2,+1), (5,-1), (6,-1), (8,+1), (10,-1)`.
- active goes `0 → 1 → 2 → 1 → 0 → 1 → 0`. Peak = 2.

This bare version is useful as a warm-up and shows up directly in: *"what's the most concurrent users on the platform during the hour?"*, *"what is the maximum vehicle count ever on this bridge?"*, *"when did my log file see the most open file handles?"*

**Related sibling: total covered length.** Replace `best = max(best, active)` with a running `covered += (t - prev_t) if active > 0`. Measures the length of the number line that at least one interval covers.

---

### Meeting Rooms II <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/)*

<ProgressCheck id="meeting-rooms-ii-medium" />

> [key] **The twist:** half-open interval semantics. A meeting ending at `t` frees a room *before* another starting at `t` needs one. Two equivalent solutions: event sweep with end-before-start tie-break, OR a min-heap of end times.

```svg
<svg role="img" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Diagram illustrating: Meeting Rooms II (Minimum Concurrent Intervals) Medium">
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

> [key] **Blind-solve first:** {{ mrIIsolvePrompt }}

<TemplateReveal
  slug="meeting-rooms-ii"
  language="java"
  :canonical="`int minMeetingRooms(int[][] meetings) {
    Arrays.sort(meetings, (a, b) -> a[0] - b[0]);          // by start
    PriorityQueue<Integer> ends = new PriorityQueue<>();   // min-heap of end times
    for (int[] m : meetings) {
        if (!ends.isEmpty() && ends.peek() <= m[0]) ends.poll();  // room freed
        ends.offer(m[1]);
    }
    return ends.size();
}`"
  problemShape="meetings → sort by start → min-heap of end times" />

**Trace** on `[[0,30],[5,10],[15,20]]` (heap version):

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

**Why either solution works:** the heap keeps only *active* meetings. When the next starts, if the earliest end has already passed, that room is free — pop it and reuse. The heap size at the end equals the peak concurrency. The event sweep achieves the same by sorting and scanning; both are O(n log n). The heap version is more memory-efficient when most intervals don't overlap (heap stays small).

---

### Car Pooling <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Car Pooling](https://leetcode.com/problems/car-pooling/)*

> [key] **The twist:** coordinates are bounded integers (stops 0..1000) and the sweep carries *weights*, not just a count. A fixed-size diff-array gives `O(n + K)` with no sort step at all — a specialization of event sweep that beats the sort when `K ≤ n log n`.

<InvariantProof
  :statement="carPoolingInvariant.statement"
  :initialization="carPoolingInvariant.initialization"
  :maintenance="carPoolingInvariant.maintenance"
  :termination="carPoolingInvariant.termination" />

```svg
<svg role="img" viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Car Pooling diff-array sweep">
  <rect x="0" y="0" width="400" height="180" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">trips = [[2,1,5], [3,3,7]], capacity = 4</text>
  <line x1="30" y1="60" x2="370" y2="60" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <g text-anchor="middle" font-size="10" fill="var(--dsa-neutral)">
    <text x="60" y="78">1</text><text x="100" y="78">3</text><text x="190" y="78">5</text><text x="280" y="78">7</text>
  </g>
  <g font-size="10" fill="var(--dsa-ink)" text-anchor="middle">
    <text x="60" y="100">+2</text><text x="100" y="100">+3</text><text x="190" y="100">-2</text><text x="280" y="100">-3</text>
  </g>
  <g text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-ink)">
    <text x="80" y="130">load=2</text><text x="145" y="130">load=5 ✗</text><text x="235" y="130">load=3</text><text x="320" y="130">load=0</text>
  </g>
  <text x="200" y="160" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-danger)">load exceeds capacity between stops 3 and 5 → return False</text>
</svg>
```

> [key] **Blind-solve first:** {{ carPoolingSolvePrompt }}

<TemplateReveal
  slug="car-pooling"
  language="python"
  :canonical="carPoolingCode"
  problemShape="trips [[p,s,e]...] on bounded stops → diff-array → prefix-sum sweep" />

**Trace** on `trips = [[2,1,5],[3,3,7]]`, `capacity = 4`:
- diff after pickups/drop-offs: `diff[1]=+2, diff[3]=+3, diff[5]=-2, diff[7]=-3`.
- Prefix sum: at stop 1 load=2 ✓, stop 3 load=5 ✗ > capacity → return `False`.

**When to prefer this over the generic event sweep:** when the problem gives you a bounded integer coordinate domain. Train scheduling where stops are 0..100, hour-of-day analytics on a 24-cell array, grid cells 0..1000 — all benefit from the diff-array specialization. For unbounded or sparse coordinates (Unix timestamps, geographic longitude), fall back to the sorted event list.

---

### The Skyline Problem <span class="diff diff-h">Hard</span>

*[↗ LeetCode: The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/)*

> [key] **The twist:** the state carried isn't a count — it's a max-heap of active heights. At each event you need the tallest building still "alive" at this x. Lazy deletion (don't remove on the end event; discard when it bubbles to the top past its right edge) keeps each operation `O(log n)` amortized.

<InvariantProof
  :statement="skylineInvariant.statement"
  :initialization="skylineInvariant.initialization"
  :maintenance="skylineInvariant.maintenance"
  :termination="skylineInvariant.termination" />

```svg
<svg role="img" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Skyline sweep">
  <rect x="0" y="0" width="400" height="200" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">buildings = [[2,9,10], [3,7,15], [5,12,12]]</text>
  <line x1="30" y1="170" x2="370" y2="170" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <rect x="50" y="110" width="140" height="60" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" opacity="0.5"/>
  <rect x="75" y="65" width="100" height="105" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)" opacity="0.6"/>
  <rect x="125" y="88" width="175" height="82" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" opacity="0.5"/>
  <polyline points="50,110 50,65 175,65 175,88 300,88 300,170" fill="none" stroke="var(--dsa-danger)" stroke-width="2.5"/>
  <text x="200" y="192" text-anchor="middle" font-size="10" font-style="italic" fill="var(--dsa-neutral)">red = silhouette key points at height changes</text>
</svg>
```

> [key] **Blind-solve first:** {{ skylineSolvePrompt }}

<TemplateReveal
  slug="the-skyline-problem"
  language="python"
  :canonical="skylineCode"
  problemShape="buildings → events → sweep + max-heap with lazy popping" />

**Why the heap, not a count:** two buildings `[1,10,20]` and `[5,8,30]` overlap in `[5,8]`. At `x=5`, the count would just be 2, but the silhouette height is `max(20, 30) = 30`. You need the maximum height, not the number of overlapping buildings. The heap gives you that `O(log n)`.

**Why lazy deletion:** removing an arbitrary heap element is `O(n)`. Instead, on the end event, do nothing; on each iteration pop entries from the top whose right-edge has passed. Each building is pushed once and popped once — amortized `O(log n)` per event.

---

### Employee Free Time <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Employee Free Time](https://leetcode.com/problems/employee-free-time/)*

> [key] **The twist:** sweep over the union of all employees' intervals, then emit the gaps where `active = 0`. One sweep over `n = Σ|schedule[i]|` events; no k-way merge needed.

<InvariantProof
  :statement="freeTimeInvariant.statement"
  :initialization="freeTimeInvariant.initialization"
  :maintenance="freeTimeInvariant.maintenance"
  :termination="freeTimeInvariant.termination" />

> [key] **Blind-solve first:** {{ freeTimeSolvePrompt }}

<TemplateReveal
  slug="employee-free-time"
  language="python"
  :canonical="freeTimeCode"
  problemShape="k sorted interval lists → merged events → emit zero-active gaps" />

**Trace** on `schedule = [[[1,2],[5,6]], [[1,3]], [[4,10]]]`:
- Events sorted: `(1,+1), (1,+1), (2,-1), (3,-1), (4,+1), (5,+1), (6,-1), (10,-1)`.
- active trace: `1 → 2 → 1 → 0 (prev_end=3) → 1 → 2 → 1 → 0`. Gap emitted when active rises from 0 at `t=4`: free time = `[3, 4]`.
- **Result:** `[[3,4]]`.

**Alternative: k-way merge with a heap of pointers.** `O(n log k)` instead of `O(n log n)`; faster when `k` (number of employees) is much smaller than total intervals. The sweep is simpler to write; the k-way merge is strictly better when `k ≪ n`.

---

## Traps & gotchas

<TrapTrace
  :title="trapAcode.statement"
  :bug="trapAcode.bug"
  :fix="trapAcode.fix" />

<TrapTrace
  :title="trapBcode.statement"
  :bug="trapBcode.bug"
  :fix="trapBcode.fix" />

<TrapTrace
  :title="trapCcode.statement"
  :bug="trapCcode.bug"
  :fix="trapCcode.fix" />

## In the wild — Mapbox label-collision avoidance

Mapbox renders a vector map with city, street, POI, and road labels, all pushed from server-side tiles. On a zoomed-out view, 10,000+ candidate labels might fit in a 1024×1024 tile. Showing them all would be unreadable. **Label collision avoidance uses a 2D sweep line** to decide which labels get placed:

1. Each label is represented by its bounding rectangle plus a priority score.
2. Sort rectangles by priority (highest first).
3. Sweep from top (lowest y) to bottom: maintain a **"skyline" of placed labels** per x-column.
4. For each candidate, check if its rectangle intersects any already-placed label's rectangle via sweep line's active-set BST ordered by y-interval overlap.
5. Place the label if no collision; otherwise discard.

This runs on every pan/zoom gesture in real time at 60fps.

Other named production uses:
- **AutoCAD / Fusion 360** sweep lines to find overlapping boundaries while drawing — pure Bentley-Ottmann 2D sweep.
- **Verilog chip-layout DRC** (design-rule check) uses sweep to find metal traces violating minimum-spacing constraints on billion-transistor circuits.
- **Google Maps / Apple Maps** compute "where is traffic currently congested?" via a sweep over road-segment speed events.
- **PostgreSQL's range-join operator** (`&&`) uses sweep plus a GiST index for `WHERE t1.period && t2.period`.

## Recognition drill

<RecognitionDrill pattern="sweep-line" :count="10" />

## Advanced — follow-ups and failure modes

<details>
<summary><b>What if events arrive online (one booking at a time)?</b></summary>

Use a **`TreeMap<coord, delta>`** (Java) or **`std::map<int, int>`** (C++). Each booking does `map[start] += 1; map[end] -= 1;`. To query current peak-overlap, iterate keys in order with a running sum.

For queries after every booking, that's `O(n)` per query; **My Calendar II/III** use this when `n` is small (≤ 1000). For large `n` with many queries, upgrade to a **segment tree with lazy propagation** indexed on compressed coordinates — `O(log n)` per update and per max query.
</details>

<details>
<summary><b>What if coordinates are 10⁹ apart but you have only n = 10⁵ events?</b></summary>

**Coordinate compression.** Collect all unique endpoints, sort them, map each to a dense index 0..2n. Then use a difference array or segment tree over the compressed space. `O(n log n)` time, `O(n)` space, no 10⁹-element allocation.

Comes up in: GPS trajectory analytics (longitude 10⁹ precision but only `n` driver positions), financial tick-data (nanosecond timestamps), telemetry pipelines.
</details>

<details>
<summary><b>What if intervals are weighted and you need total weighted coverage, not peak?</b></summary>

The sweep carries a weighted sum. For intervals `[s, e, w]`, emit `(s, +w)` and `(e, -w)` events. Scan sorted events; between two adjacent event times `t1 < t2`, the segment `[t1, t2)` has whatever weighted sum you carried from the last event — add `(t2 - t1) * current_sum` to total weighted coverage.

Used in: ad-impression billing (weighted by impressions per second), network bandwidth billing (weighted by bytes/sec served on each stream).
</details>

<details>
<summary><b>What if intervals are 2D rectangles and you need total covered area?</b></summary>

**Klee's problem.** The 1D sweep generalizes: sweep a vertical line across the plane. The *active set* is a set of y-intervals (one per rectangle whose x-range covers the sweep line). The 1D-covered-length of this active set, multiplied by the horizontal distance to the next event, is the area contributed. Maintain the active set with a **segment tree over compressed y-coordinates** supporting "add interval / remove interval / query total covered length." Overall `O(n log n)`.

Used in: VLSI layout area counting, GIS urban-footprint analytics, graphics software for "selected area" measurement.
</details>

<details>
<summary><b>Breaking point — when a plain sweep stops being enough.</b></summary>

- **Dynamic intervals with mid-sweep insertions**: You can't un-sort. Use a `TreeMap` of deltas instead.
- **Nested queries** (how many intervals contain point *p* AND satisfy some predicate on them): need a segment tree or interval tree with per-node metadata.
- **Range updates with point queries** (e.g. "add 5 to all intervals covering [a,b]"): switch to segment tree with lazy propagation.
- **Billions of intervals that don't fit in RAM**: external-memory sort of events, stream through with the sweep logic. Google uses this for ad-impression billing at scale.
</details>

### Cross-pattern problems

| Problem | Primary pattern | What sweep contributes |
|---|---|---|
| [My Calendar III](https://leetcode.com/problems/my-calendar-iii/) | TreeMap sweep | each booking is a delta; max prefix sum is the answer |
| [Rectangle Area II](https://leetcode.com/problems/rectangle-area-ii/) | 2D sweep + segment tree | Klee's problem; 2D area of union of rectangles |
| [Falling Squares](https://leetcode.com/problems/falling-squares/) | sweep + segment tree | each new square's landing height is the max in its x-range |

## Related patterns + Check your understanding

<RelatedPatterns pattern-id="sweep-line" />

<Quiz
  pattern-id="sweep-line"
  :questions="quizQuestions" />

<PrintButton />
