# Sweep Line — The Skyline Problem

*[↗ LeetCode: The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/sweep-line)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg" /&gt;

Given buildings `[left, right, height]`, return the skyline as key points `[x, y]` where the height changes.

**Example 1** — `[[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]` → `[[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]`

**Constraints** — `1 ≤ n ≤ 10⁴`.


&lt;Hints
  hint1="Turn events into `(time, +1/-1)` pairs. What’s the ’active count’ or ’max concurrent’?"
  hint2="Sort events by time; break ties consistently (end before start for ’meetings’, or vice versa)."
  hint3="Sweep; maintain a running count/set. Max active gives room count; drops give free slots."
/&gt;
---

## Approach 1 — Every x

For each x, scan all buildings. O(n·max). TLE.

## Approach 2 — Event sweep + max-heap (canonical)

**Insight.** Create events `(x, height, isStart)`. Sort. Sweep; maintain heap of active heights. When top changes, emit new point.

- Start: push height into heap.
- End: mark for lazy removal.
- Emit `(x, currentMax)` whenever currentMax changed since last emission.



```java
List<List<Integer>> getSkyline(int[][] buildings) {
    List<int[]> events = new ArrayList<>();
    for (int[] b : buildings) {
        events.add(new int[]{b[0], -b[2], b[1]}); // start (neg h)
        events.add(new int[]{b[1], 0, 0});         // end marker
    }
    events.sort((a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]);
    List<List<Integer>> res = new ArrayList<>();
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> b[0] - a[0]);
    pq.offer(new int[]{0, Integer.MAX_VALUE});
    int prev = 0;
    for (int[] e : events) {
        if (e[1] < 0) pq.offer(new int[]{-e[1], e[2]});
        while (pq.peek()[1] <= e[0]) pq.poll();
        int cur = pq.peek()[0];
        if (cur != prev) { res.add(Arrays.asList(e[0], cur)); prev = cur; }
    }
    return res;
}
```



<CodeTrace
  title="Sweep — buildings 3 shown"
  :values="['[2,9,10]','[3,7,15]','[5,12,12]']"
  :windowKeys="['x']"
  :cellWidth="42"
  :steps='[
    { pointers: { x: 2 }, vars: { heap: "[10]", curMax: 10, emit: "[2,10]" }, note: "" },
    { pointers: { x: 3 }, vars: { heap: "[15,10]", curMax: 15, emit: "[3,15]" }, note: "" },
    { pointers: { x: 7 }, vars: { heap: "[12,10]", curMax: 12, emit: "[7,12]" }, note: "15 removed lazily" },
    { pointers: { x: 12 }, vars: { heap: "[]", curMax: 0, emit: "[12,0]" }, note: "" }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="the-skyline-problem" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Every x-scan | O(n·max) | O(1) | baseline |
| Event sweep + heap | **O(n log n)** | O(n) | canonical |

## When to use which

- **"Max active over time"** → event sweep + max-heap.
- **Divide & conquer alternative** → merge two half-skylines in O(n log n).
- **Segment tree with range max** → same complexity, different mental model.

&lt;AiCompanion problem-slug="the-skyline-problem" pattern-hint="sweep line" /&gt;

## Related problems

- [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii)
- [Falling Squares](https://leetcode.com/problems/falling-squares/)
- [Rectangle Area II](https://leetcode.com/problems/rectangle-area-ii/)