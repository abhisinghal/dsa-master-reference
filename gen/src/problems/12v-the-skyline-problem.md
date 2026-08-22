# Sweep Line — The Skyline Problem

*[↗ LeetCode: The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/sweep-line)

Given buildings `[left, right, height]`, return the skyline as `[x, y]` critical points where the height changes.

**Example** — `[[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]` → `[[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]`

---

## Approach 1 — Brute per-x scan

For each integer x in range, scan every building; take the max height covering it. O(x_max · n).

**Complexity** — TLE at `x_max = 10⁹`.

## Approach 2 — Sweep events sorted + max-heap

**Insight.** Only key x-values matter — the left and right edges of buildings. Sort events; process left-to-right. At a **left edge**, add the building's height to a running structure; at a **right edge**, remove it. Emit the current max height whenever it changes.

**Trap.** A plain max-heap can't remove non-top elements in O(log n) — use *lazy deletion*: keep a queue of pending-remove heights, and skip the heap top until it's not pending.

```java
List<List<Integer>> getSkyline(int[][] buildings) {
    List<int[]> events = new ArrayList<>();
    for (int[] b : buildings) {
        events.add(new int[]{b[0], -b[2]});                  // start: negative height
        events.add(new int[]{b[1], b[2]});                   // end: positive
    }
    events.sort((a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]);
    PriorityQueue<Integer> heap = new PriorityQueue<>(Comparator.reverseOrder());
    heap.offer(0);                                             // ground
    List<List<Integer>> out = new ArrayList<>();
    int prev = 0;
    for (int[] e : events) {
        if (e[1] < 0) heap.offer(-e[1]);                       // start → add
        else          heap.remove(e[1]);                       // end → remove (O(n) but acceptable)
        int cur = heap.peek();
        if (cur != prev) { out.add(Arrays.asList(e[0], cur)); prev = cur; }
    }
    return out;
}
```

<CodeTrace
  title="Sweep skyline — buildings=[[2,9,10],[3,7,15],[5,12,12]]"
  :values="[2,3,5,7,9,12]"
  :windowKeys="['x']"
  :cellWidth="42"
  :steps='[
    { pointers: { x: 0 }, vars: { heap: "[10]", height: 10 }, note: "start at 2, +10 → skyline (2,10)", added: [0] },
    { pointers: { x: 1 }, vars: { heap: "[15,10]", height: 15 }, note: "start at 3, +15 → skyline (3,15)", added: [1] },
    { pointers: { x: 2 }, vars: { heap: "[15,12,10]", height: 15 }, note: "start at 5, +12 (no change)" },
    { pointers: { x: 3 }, vars: { heap: "[12,10]", height: 12 }, note: "end at 7, -15 → skyline (7,12)", added: [3] },
    { pointers: { x: 4 }, vars: { heap: "[12]", height: 12 }, note: "end at 9, -10 (no change)" },
    { pointers: { x: 5 }, vars: { heap: "[]", height: 0 }, note: "end at 12, -12 → skyline (12,0)", added: [5] }
  ]'
/>

**Complexity** — Time **O(n² log n)** with `remove`; **O(n log n)** with lazy delete; Space **O(n)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute per-x scan | O(x_max · n) | O(1) |
| Sweep + max-heap | O(n² log n) or O(n log n) lazy | O(n) |

## Related problems

- [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii) — max concurrency, simpler
- [Falling Squares](https://leetcode.com/problems/falling-squares/) — sweep + segment tree
- [My Calendar II](/problems/my-calendar-ii) — sweep with deltas
