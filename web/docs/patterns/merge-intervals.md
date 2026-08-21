# Merge Intervals

## Why merge intervals exists — the story

An interval is a promise about a stretch of time or space: a meeting from 9 to 10, a reservation from 4 to 7, a closed range `[1, 3]` on a number line. The hard part is not understanding one interval. The hard part is what happens when you receive a messy pile of them: `[8,10]`, `[1,3]`, `[2,6]`, `[15,18]`. At first glance, any interval could overlap any other interval, so the brute-force instinct is to compare every pair. The merge-intervals pattern exists because sorting turns the pile into a line.

Sort by start time: `[1,3]`, `[2,6]`, `[8,10]`, `[15,18]`. Now you only need a "current merged block." Start with `[1,3]`. The next interval starts at `2`, which is before the current block ends at `3`, so merge them into `[1,6]`. The next starts at `8`, after `6`, so the old block is finished and you start a new one. The final answer is `[[1,6],[8,10],[15,18]]`. Sorting made the question local: once starts are ordered, a future interval cannot reach backward past the current block without first touching it.

That is the intuition to carry into interviews. You are not sorting because the output must be sorted; you are sorting because it creates an invariant. Every interval you have already emitted is final. The only interval that can still grow is the current one. That reduces "compare everything against everything" to one left-to-right sweep.

<Callout kind="key" title="Key Insight">

Two intervals `[a,b]` and `[c,d]` overlap iff `a ≤ d && c ≤ b`. After sorting by start, overlap with the running interval is simply `next.start ≤ cur.end`.

</Callout>

## When to use it — ordered ranges that may touch

### Recognize by
- *intervals* on a number line — meetings, flights, ranges, bookings, CPU jobs
- "merge overlapping intervals", "combine ranges", "return disjoint intervals"
- "insert a new interval" into an already sorted list
- "remove covered intervals" or "erase overlaps" after sorting by one endpoint
- "find free time" as the gaps between merged busy blocks
- values are pairs like `[start, end]`, and the answer needs the intervals themselves

### When NOT to use it
You need *how many are active at time t?* rather than *which merged into which?* — that's the [Sweep Line](/patterns/sweep-line) variant. Also skip this pattern when intervals live on multiple axes (2-D) — reach for coordinate compression + segment tree.

Do not use plain merge-intervals if order is already fixed by original sequence and you are forbidden to reorder; then you may need a stack or greedy pass over the given order. Do not use it when intervals are open/closed in a nonstandard way until you clarify whether touching endpoints count as overlap. Finally, if you only need the maximum number of simultaneous meetings, sorting starts and ends separately is often cleaner than building merged ranges.

## How to use it — template



```java
Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
List<int[]> out = new ArrayList<>();
int[] cur = intervals[0];
for (int i = 1; i < intervals.length; i++) {
    int[] next = intervals[i];
    if (next[0] <= cur[1]) {
        cur[1] = Math.max(cur[1], next[1]);
    } else {
        out.add(cur);
        cur = next;
    }
}
out.add(cur);
return out.toArray(new int[0][]);
```



The sort is the setup. `cur` is the union of the current overlapping cluster. If the next interval starts before or exactly at `cur`'s end, it belongs to the same cluster, so only the end might extend. If the next interval starts after `cur` ends, there is a gap; `cur` can never be touched again, so emit it and begin a new cluster. That "emit only after a gap" rule is the main invariant.

---

## Merge Intervals <span class="diff diff-m">Medium</span>
*[↗ LeetCode: Merge Intervals](https://leetcode.com/problems/merge-intervals/)*

### Problem
Given a list of intervals, **merge all overlapping** ones and return the disjoint result.

**Constraints:** `1 ≤ n ≤ 10⁴`; `start ≤ end`; values up to 10⁴.

**Example 1:** `[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`.

**Example 2:** `[[1,4],[4,5]]` → `[[1,5]]` because touching closed intervals merge.

### Solution — brute force
A brute-force way is to repeatedly search for any two intervals that overlap, merge that pair, and restart. It feels natural because the problem says "merge all overlaps," but it does too much repeated scanning.



```text
list = all intervals
changed = true
while changed:
    changed = false
    for every pair i, j:
        if list[i] overlaps list[j]:
            replace them with their union
            changed = true
            restart scanning
return list
```



In the worst case, finding overlaps costs O(n²) per round, and you may merge many times. Even with careful implementation, pairwise comparison is at least O(n²). Sorting by start gives the same result with O(n log n) sorting plus O(n) scanning.



```text
for each interval i:
    for each interval j after i:
        if i overlaps j:
            replace i and j with their union
            restart scanning until no pair overlaps
return the remaining intervals
```



Brute force complexity: at least O(n²) comparisons, and repeated merge rounds can make it worse.

### Solution — optimized
Sort by start; extend the current interval while the next overlaps.

<Callout kind="inv" title="Invariant">

All emitted intervals are disjoint and sorted; `cur` is the running union of the overlapping cluster.

</Callout>

#### Steps
1. Sort the intervals by `start` — O(n log n) prerequisite for the linear sweep.
2. Initialize `out` with the first interval.
3. For each subsequent interval `cur`: if `cur.start <= last.end` — they overlap or touch; update `last.end = max(last.end, cur.end)`.
4. Otherwise — push `cur` as a new interval.
5. Return `out`. O(n log n) total.

#### Java


```java
int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (x, y) -> Integer.compare(x[0], y[0]));
    List<int[]> out = new ArrayList<>();
    int[] cur = intervals[0];
    for (int i = 1; i < intervals.length; i++) {
        if (intervals[i][0] <= cur[1]) cur[1] = Math.max(cur[1], intervals[i][1]);  // overlap
        else { out.add(cur); cur = intervals[i]; }                                   // gap
    }
    out.add(cur);
    return out.toArray(new int[0][]);
}
```



<Callout kind="note" title="Trace it">

`[[1,3],[2,6],[8,10],[15,18]]` sorted by start.

| Step | Current interval | Next interval | Decision | Output so far |
|---|---|---|---|---|
| start | `[1,3]` | — | seed current block | `[]` |
| 1 | `[1,3]` | `[2,6]` | `2 <= 3`, merge to `[1,6]` | `[]` |
| 2 | `[1,6]` | `[8,10]` | `8 > 6`, emit `[1,6]` | `[[1,6]]` |
| 3 | `[8,10]` | `[15,18]` | `15 > 10`, emit `[8,10]` | `[[1,6],[8,10]]` |
| finish | `[15,18]` | — | emit last current block | `[[1,6],[8,10],[15,18]]` |

The last `out.add(cur)` is not optional. The loop only emits when it sees a gap; the final cluster has no future gap to trigger emission.

</Callout>

### Time Complexity
Time O(n log n). Sorting dominates; the left-to-right merge pass is O(n).

### Space Complexity
Space O(n) for the output list in the worst case; the in-place interval mutation avoids extra interval copies.

### Learning notes
- Why sort by start? — it makes every emitted interval final once a gap appears.
- Why keep `cur`? — it is the running union of the current overlapping cluster.
- Why test `intervals[i][0] <= cur[1]`? — after start-sorting, only the next start can decide overlap.
- Why `Math.max(cur[1], intervals[i][1])`? — contained intervals must not shrink the merged end.
- Why `out.add(cur)` in the `else`? — a gap proves the current block can never grow again.
- Why the final `out.add(cur)`? — the last cluster has no later gap to trigger emission.

Additional notes:

Time O(n log n) · Space O(n).

Sorting dominates the runtime. The sweep itself is O(n) because each interval is considered once. The output list can hold O(n) intervals in the case where nothing overlaps. Depending on the sort implementation and whether you mutate intervals in place, there may also be sorting stack or temporary-array overhead.

<Callout kind="note" title="The sort line, explained">

`Arrays.sort(intervals, (x, y) -> Integer.compare(x[0], y[0]))` sorts the rows by their start value. The `(x, y) -> ...` part is a **lambda** — a throwaway function that takes two intervals and returns negative / zero / positive to mean "x comes before / same / after y." We compare `x[0]` with `y[0]` (the starts) using `Integer.compare`, which is the safe way to compare ints — writing `x[0] - y[0]` can overflow and flip the sign. To sort by end instead, compare `x[1]` with `y[1]`; to add a tie-breaker, chain `Comparator.comparingInt(a -> a[0]).thenComparingInt(a -> a[1])`. (Full comparator tour in the *Java Data Structures* chapter.)

</Callout>

<Callout kind="trap" title="Common Trap">

Touching vs overlapping. *Example:* `[1,2]` and `[2,3]`. If touching counts as overlap → merge (`cur.start <= last.end`) → `[1,3]`. If not → keep separate (`cur.start < last.end`). LeetCode's *Merge Intervals* treats touching as overlap; *Non-overlapping Intervals* does not.

</Callout>

<Callout kind="note" title="Interview script">

First, I'd clarify whether intervals are closed and whether touching endpoints should merge. The brute force is to compare every pair and repeatedly merge overlaps, but that is at least O(n²). I can do better by sorting by start, keeping one running interval, and only comparing each next interval to that running interval. Sorting costs O(n log n), the sweep is O(n), and the output space is O(n).

</Callout>

#### Common Mistakes
- **Touching vs overlapping**: `[1,2]` and `[2,3]` are treated as overlapping on LC Merge Intervals; `<=` is correct here.
- **Sorting by end** would break the merging invariant — sort by start.
- **Mutating input intervals** may cause bugs when the interviewer's harness reuses them — push copies.
- **Comparator overflow**: use `Integer.compare(a[0], b[0])`, not `a[0] - b[0]`, for large starts.
- **Forgetting the final interval**: the last cluster must be added after the loop.

<Callout kind="pat" title="Pattern Connection">

*Insert Interval* is merge with a single new interval (three phases: before, overlapping-merge, after). *Interval List Intersections* uses two-pointer overlap testing.

</Callout>

#### Why sorting by start is the invariant-maker
After sorting by start, suppose `cur = [1,6]` and the next interval is `[8,10]`. Every later interval starts at least `8`, so no later interval can overlap `[1,6]`. That means `[1,6]` is safe to emit permanently. Without sorting, seeing `[8,10]` tells you nothing; a later `[4,5]` could still overlap the old block. This is why sorting by end is not a harmless style change for merging. End-sorted order can place `[2,3]` before `[1,10]`, and your running-current reasoning becomes awkward because a later interval can swallow an earlier one from the left.

The overlap check also becomes one-sided after sorting. General interval overlap is `a.start <= b.end && b.start <= a.end`. But when `cur.start <= next.start` is guaranteed by sorting, the first half is automatically true. You only test `next.start <= cur.end`.

#### Closed, open, and half-open intervals

Before coding, clarify endpoint semantics. LeetCode's Merge Intervals uses closed intervals, so `[1,2]` and `[2,3]` overlap at point `2` and merge into `[1,3]`. Many scheduling systems use half-open intervals, where `[1,2)` ends exactly when `[2,3)` begins; those do not overlap and should remain separate. The only code change is the comparison: closed intervals use `next.start <= cur.end`, half-open intervals use `next.start < cur.end`.

This is not a tiny wording detail. For meeting rooms, a meeting ending at 10 and another starting at 10 usually do not conflict. For integer range coverage, `[1,2]` and `[2,3]` usually share the integer or point `2`. State your assumption before choosing `<` or `<=`.

#### Mutating versus copying intervals

The compact solution stores `cur = intervals[0]` and mutates `cur[1]` as it merges. That is common in LeetCode solutions and efficient. In production, mutating input can surprise callers if they reuse the original array later. A copy-safe version would create a new `int[]` whenever it starts a current block and whenever it emits output.

For interviews, it is usually fine to mutate unless the prompt says otherwise. You can add one sentence: "This mutates the interval objects; if the caller needs the input preserved, I would copy each interval before storing it in `out`." That shows engineering judgment without bloating the core algorithm.

#### How interval problems split into families

Merge Intervals is one member of a larger interval toolkit. If you need the **union of ranges**, sort by start and merge. If you need the **number of simultaneous active ranges**, split each interval into start/end events and sweep counts. If you need **intersections between two already-sorted lists**, use two pointers and advance whichever interval ends first. If you need to **minimize removals**, sort by end time and greedily keep intervals that finish earliest. The input shape may look identical, but the output question chooses the pattern.

Use this quick decision guide:

| Question asks for | Pattern to reach for | Why |
|---|---|---|
| merged disjoint ranges | sort by start + running union | output is the union itself |
| can attend all meetings? | sort by start and check neighbour overlap | any conflict is local after sorting |
| minimum rooms / max overlap | sweep line or min-heap of end times | you need active count, not union |
| intersections of two lists | two pointers | both lists are already sorted and disjoint |
| remove minimum overlaps | greedy by earliest end | keeping short-ending intervals leaves room |

#### Testing checklist

Small tests catch almost every merge bug:

| Input | Expected | Lesson |
|---|---|---|
| `[[1,3]]` | `[[1,3]]` | single interval still gets emitted |
| `[[1,4],[2,3]]` | `[[1,4]]` | contained interval should not shrink the end |
| `[[1,2],[2,3]]` | `[[1,3]]` for closed intervals | choose `<=` deliberately |
| `[[5,6],[1,2]]` | `[[1,2],[5,6]]` | sort before sweeping |
| `[[1,4],[0,0]]` | `[[0,0],[1,4]]` | gaps create separate output blocks |

#### From this problem to Insert Interval

Once Merge Intervals feels natural, *Insert Interval* should feel like the same sweep with one new range carried in your hand. The input list is already sorted and non-overlapping, so you do not need to sort. First copy every interval that ends before the new interval starts. Then merge every interval that overlaps the new interval, expanding the new interval's start and end as needed. Finally copy the remaining intervals after the merged block.

For example, intervals `[[1,2],[3,5],[6,7],[8,10],[12,16]]` and new interval `[4,8]` become `[[1,2],[3,10],[12,16]]`. `[1,2]` is before the new interval, so it is copied. `[3,5]`, `[6,7]`, and `[8,10]` all touch or overlap `[4,8]`, so the carried interval grows to `[3,10]`. `[12,16]` is after it, so the merge is done. That is the same \"current block grows until a gap appears\" idea, just without the initial sort.

#### From this problem to Meeting Rooms II

Meeting Rooms II looks like interval merging, but the answer is a count of simultaneous meetings, not the merged ranges. If you merge `[1,10]`, `[2,3]`, and `[4,5]`, you get `[1,10]`, but that does not tell you whether you needed two rooms or three. For active counts, use a min-heap of end times or a sweep line of start/end events. This distinction is a good interview signal: you are choosing the pattern based on the output, not just the input shape.

#### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Insert Interval](https://leetcode.com/problems/insert-interval/) | three phases — copy intervals before, merge those overlapping the new one, copy the rest | O(n) if already sorted |
| [Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) | two sorted lists; each overlap is `[max(starts), min(ends)]`, then advance the earlier end | O(m+n) |
| [Employee Free Time](https://leetcode.com/problems/employee-free-time/) | merge everyone's busy intervals; gaps between merged blocks are the free time | O(n log n) |
| [Remove Covered Intervals](https://leetcode.com/problems/remove-covered-intervals/) | sort by start then end descending; count intervals not swallowed by the widest previous end | O(n log n) |
| [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/) | after sorting by start, any overlap between neighbours means one person cannot attend all meetings | O(n log n) |
