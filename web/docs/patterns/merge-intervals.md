# Merge Intervals


<PatternVideo pattern-name="Merge Intervals" duration="8–12 min" />

<PatternProgress pattern-id="merge-intervals" problems="merge-intervals-classic, insert-interval, meeting-rooms, interval-list-intersections, employee-free-time, remove-covered-intervals" />



## Why merge intervals exists — the story

You're building the calendar backend for Google Meet. Users grant you a list of "busy" blocks from their Outlook, Zoom, and Slack calendars. Before showing free/busy to a meeting scheduler, you must **merge** overlapping busy blocks into one clean list.

The honest first attempt: for each pair of intervals, check if they overlap and merge. Nested loop. For 50 busy blocks per user (typical exec calendar), it's `~1,250` comparisons — instant. And it's a legit first answer: interviewers accept it as the baseline.

But at scale it dies. Meet processes calendar-merge requests for **1 billion users** to power its "find a time" feature. If each user has 200 busy blocks (5-day rolling window), naive is `200² = 40,000` ops per user × `10⁹` users = `4·10¹³` ops. At 100M ops/sec per core, that's **12 million CPU-hours** — daily. Google's infra team would notice.

The pattern is: sort once, then sweep left to right. After sort, if the next interval's start is `≤` the current merged block's end, extend the block; otherwise, close the block and open a new one. **O(n log n)** sort + **O(n)** sweep. For 200 blocks per user, that's ~1,500 ops — 25× faster and, more importantly, asymptotically better. What makes this work is an **invariant**: after sorting by start time, every interval you've already emitted is final; only the current one can still grow. Sorting turned a global relation ("does this overlap with any of the 199 others?") into a local check ("does this touch the previous?").

Sort by start time: `[1,3]`, `[2,6]`, `[8,10]`, `[15,18]`. Now you only need a "current merged block." Start with `[1,3]`. The next interval starts at `2`, which is before the current block ends at `3`, so merge them into `[1,6]`. The next starts at `8`, after `6`, so the old block is finished and you start a new one. The final answer is `[[1,6],[8,10],[15,18]]`. Sorting made the question local: once starts are ordered, a future interval cannot reach backward past the current block without first touching it.

That is the intuition to carry into interviews. You are not sorting because the output must be sorted; you are sorting because it creates an invariant. Every interval you have already emitted is final. The only interval that can still grow is the current one. That reduces "compare everything against everything" to one left-to-right sweep.

<Callout kind="key" title="Key Insight">

Two intervals `[a,b]` and `[c,d]` overlap iff `a ≤ d && c ≤ b`. After sorting by start, overlap with the running interval is simply `next.start ≤ cur.end`.

</Callout>

<MergeIntervalsAnim />

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

<ProgressCheck id="merge-intervals" />





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="27" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">merge intervals after sorting by start</text>
  <line x1="48" y1="64" x2="352" y2="64" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <g text-anchor="middle" font-size="11" fill="var(--dsa-neutral)">
    <text x="50" y="82">1</text><text x="83" y="82">2</text><text x="149" y="82">4</text><text x="182" y="82">5</text>
    <text x="248" y="82">7</text><text x="281" y="82">8</text><text x="314" y="82">9</text><text x="347" y="82">10</text>
  </g>
  <rect x="50" y="102" width="99" height="16" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
  <rect x="83" y="124" width="99" height="16" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <rect x="248" y="102" width="66" height="16" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
  <rect x="281" y="124" width="66" height="16" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <g font-size="11" font-weight="700" fill="var(--dsa-ink)">
    <text x="84" y="114">[1,4]</text><text x="117" y="136">[2,5]</text><text x="266" y="114">[7,9]</text><text x="300" y="136">[8,10]</text>
  </g>
  <text x="200" y="166" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--dsa-warning)">sort by start, then extend or emit</text>
  <rect x="50" y="184" width="132" height="18" rx="7" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)" stroke-width="1.6"/>
  <rect x="248" y="184" width="99" height="18" rx="7" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)" stroke-width="1.6"/>
  <g text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-warning)">
    <text x="116" y="198">[1,5]</text><text x="298" y="198">[7,10]</text>
  </g>
  <text x="200" y="230" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">sort by start; extend while overlapping</text>
</svg>
</div>




<div class="readfig"><b>How to read it:</b> Once intervals are sorted, each new bar either overlaps the current merged bar and extends its end, or starts a fresh merged interval.</div>

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

</Callout>

<CodeTrace
  title="Merge Intervals — sorted by start"
  :values="['[1,3]','[2,6]','[8,10]','[15,18]']"
  :windowKeys="['i']"
  :cellWidth="60"
  :steps='[
    { pointers: { i: 0 }, vars: { last: "[1,3]", out: "[[1,3]]" }, note: "start with first interval" },
    { pointers: { i: 1 }, vars: { last: "[1,6]", out: "[[1,6]]" }, note: "2 ≤ 3 → overlap, extend end to max(3,6)=6", added: [0,1] },
    { pointers: { i: 2 }, vars: { last: "[8,10]", out: "[[1,6],[8,10]]" }, note: "8 gt 6 → new interval" },
    { pointers: { i: 3 }, vars: { last: "[15,18]", out: "[[1,6],[8,10],[15,18]]" }, note: "15 gt 10 → new interval. done" }
  ]'
/>
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

<TrapTrace title="Touching vs overlapping" input="[1,2]" bug="'[1,2]' and '[2,3]'. If touching counts as overlap → merge ('cur.start lt= last.end') → '[1,3]'. If not → keep separate ('cur.start lt last.end'). LeetCode's *Merge Intervals* treats touching as overlap; *Non-overlapping Intervals* does not." fix="See the guidance in the trap description and the code snippet." />

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

---

## Check your understanding

<Quiz
  pattern-id="merge-intervals"
  :questions='[{"q": "Standard Merge Intervals: sort by what?", "choices": [{"text": "Start ascending", "correct": true, "explanation": "Then walk once and merge on overlap."}, {"text": "End ascending", "correct": false, "explanation": "Better for activity selection / non-overlap counting."}, {"text": "Length descending", "correct": false}, {"text": "Random", "correct": false}]}, {"q": "For Insert Interval into a pre-sorted list, what is the canonical algorithm?", "choices": [{"text": "Three-phase single pass: copy-before, merge-overlapping, copy-after", "correct": true, "explanation": "O(n) time; no re-sort needed since input is sorted."}, {"text": "Insert then run full Merge Intervals", "correct": false, "explanation": "Works but O(n log n)."}, {"text": "Sort by end and use greedy", "correct": false, "explanation": "That is Non-overlap Intervals."}, {"text": "Binary search only", "correct": false}]}, {"q": "For Remove Covered Intervals, what tie-break at same-start intervals?", "choices": [{"text": "Sort by start asc, end DESC", "correct": true, "explanation": "Ensures the covering interval comes first when starts tie."}, {"text": "Sort by start asc, end asc", "correct": false, "explanation": "Would mislabel the shorter one as covering."}, {"text": "No tie-break needed", "correct": false}, {"text": "Random tie-break", "correct": false}]}, {"q": "For Meeting Rooms (bool \"can attend all\"), what is the O(n log n) check?", "choices": [{"text": "Sort by start; verify each start ≥ previous end", "correct": true, "explanation": "Adjacent-check suffices after sorting."}, {"text": "Full n² pair check", "correct": false, "explanation": "Wasteful."}, {"text": "Union-Find", "correct": false}, {"text": "DP", "correct": false}]}, {"q": "Interval List Intersections (two sorted disjoint lists) is best solved by:", "choices": [{"text": "Two-pointer merge with `[max(starts), min(ends)]` intersection formula", "correct": true, "explanation": "O(n+m) linear pass."}, {"text": "Sort both then binary search", "correct": false, "explanation": "Already sorted; unnecessary sort."}, {"text": "Union all then re-detect overlaps", "correct": false, "explanation": "Overkill."}, {"text": "Recursion", "correct": false}]}]'
/>

<PrintButton />

<RelatedPatterns pattern-id="intervals" />
