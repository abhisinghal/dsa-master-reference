## The Pattern

Sweep line converts interval overlap into ordered events. Sort starts and ends, scan from left to right, and maintain the state of intervals currently crossing the sweep position: an active count for concurrency, or an active set when you must know which intervals are alive.

!!! pattern "Recognition signals"
    **Signals:** intervals on a timeline, endpoints, calendars, maximum overlap, minimum rooms, skyline-like boundaries, or "how many ranges cover this point?" If the answer changes only at endpoints, process endpoints rather than every coordinate.

```diagram
{"type":"intervals","title":"Events drive the running active count","min":0,"max":7,"intervals":[{"start":1,"end":4,"label":"A [1,4)","role":"green"},{"start":2,"end":5,"label":"B [2,5)","role":"amber"},{"start":4,"end":6,"label":"C [4,6)","role":"primary"},{"start":1,"end":1,"label":"+A active=1","role":"green"},{"start":2,"end":2,"label":"+B active=2","role":"amber"},{"start":4,"end":4,"label":"-A,+C active=2","role":"primary"},{"start":5,"end":5,"label":"-B active=1","role":"muted"}],"caption":"Sort endpoint events; apply tie rules deliberately. The maximum active count is the minimum number of rooms."}
```

## The Invariant

Immediately after processing all events at coordinate `x`, `active` represents exactly the intervals that contain positions just to the right of `x` under the chosen boundary convention. The answer is updated from that state: `maxActive` for rooms/concurrency, active set geometry for skyline, or accumulated length when the next coordinate is known.

## Template

```java
int minMeetingRooms(int[][] intervals) {
    int n = intervals.length;
    int[] starts = new int[n];
    int[] ends = new int[n];
    for (int i = 0; i < n; i++) {
        starts[i] = intervals[i][0];
        ends[i] = intervals[i][1];
    }
    Arrays.sort(starts);
    Arrays.sort(ends);

    int rooms = 0, maxRooms = 0, i = 0, j = 0;
    while (i < n) {
        if (starts[i] < ends[j]) {
            rooms++;
            maxRooms = Math.max(maxRooms, rooms);
            i++;
        } else {
            rooms--;
            j++;
        }
    }
    return maxRooms;
}
```

For custom events, sort with a safe comparator: `Comparator.comparingInt((int[] e) -> e[0]).thenComparingInt(e -> e[1])`, where the second key encodes tie order such as end-before-start for half-open meetings.

## Worked Recognition

- **Meeting Rooms II** (Modules 10/14): every start increases active meetings; every end frees a room. The peak active count is the answer.
- Calendar conflict detection (Module 14): a sweep reveals whether active ever exceeds 1; for repeated bookings, a balanced map of endpoint deltas gives the same invariant online.
- Range coverage summaries: line-sweep deltas accumulate active coverage and can measure covered length between consecutive event coordinates.

## Complexity

!!! complexity "Complexity"
    **T:** O(n log n) for sorting endpoints/events, then O(n) scanning. **S:** O(n) for event arrays, or O(1) beyond sorted endpoint arrays if input can be rearranged.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Mishandling ties: for half-open intervals `[start,end)`, process ends before starts at the same coordinate; for closed intervals, starts may need to count first. Also avoid `a[0] - b[0]` comparators, forgetting to batch same-coordinate events, or using merge-intervals when the question asks for maximum concurrency.

## When NOT to use it

Do not use a full sweep when the domain is tiny enough for direct counting, when online updates require immediate answers without resorting to an ordered delta map, or when interval choices are weighted and require DP rather than local active-state aggregation.
