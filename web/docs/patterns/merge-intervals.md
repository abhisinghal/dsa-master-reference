# Merge Intervals


<PatternVideo pattern-name="Merge Intervals" duration="8–12 min" />

<PatternProgress pattern-id="merge-intervals" problems="merge-intervals-classic, insert-interval, non-overlapping-intervals, meeting-rooms-i, interval-list-intersections, employee-free-time, remove-covered-intervals" />

<script setup>
const bareTemplateCode = `# python
intervals.sort(key=lambda iv: iv[0])      # sort by start
out = [intervals[0]]
for s, e in intervals[1:]:
    if s &lt;= out[-1][1]:                   # overlap → extend
        out[-1][1] = max(out[-1][1], e)
    else:
        out.append([s, e])                # gap → emit, start new
return out`

const bareInvariant = {
  statement: `All intervals in \`out\` are disjoint and finalized; \`out[-1]\` is the only interval that can still grow.`,
  initialization: `Before entry \`out = [intervals[0]]\`. One interval, so it's trivially disjoint; being the last entry, it's the only one that can grow.`,
  maintenance: `For each next \`[s,e]\` in start-sorted order: if \`s &lt;= out[-1][1]\` the two overlap, so updating \`out[-1][1] = max(out[-1][1], e)\` keeps \`out[-1]\` the only mutable interval and preserves disjointness with everything to its left (whose end is strictly less than any new start by construction). Else a gap exists, so \`out[-1]\` is forever disjoint from anything to come (future starts ≥ \`s &gt; out[-1][1]\`); appending \`[s,e]\` makes it the new mutable tail.`,
  termination: `When the loop exits, every interval has been placed. All of \`out[:-1]\` are already finalized disjoint intervals and \`out[-1]\` is finalized too (no more inputs can touch it). So \`out\` is the merged union of all inputs.`
}

const bareComplexity = {
  time: `O(n log n) — sort dominates; the sweep is O(n).`,
  space: `O(n) output in the worst case (no overlaps).`
}

const templateSpecializations = [
  { slug: `classic-merge-intervals-medium`, title: `Classic Merge Intervals` },
  { slug: `insert-interval-medium`, title: `Insert Interval` },
  { slug: `non-overlapping-intervals-medium`, title: `Non-overlapping Intervals` },
  { slug: `meeting-rooms-i-easy`, title: `Meeting Rooms I` }
]

const insertIntervalCode = `# python — three phases, no sort needed
def insert(intervals, new):
    out, i, n = [], 0, len(intervals)
    # phase 1: copy intervals strictly before new
    while i &lt; n and intervals[i][1] &lt; new[0]:
        out.append(intervals[i]); i += 1
    # phase 2: merge every interval that touches new
    while i &lt; n and intervals[i][0] &lt;= new[1]:
        new = [min(new[0], intervals[i][0]), max(new[1], intervals[i][1])]
        i += 1
    out.append(new)
    # phase 3: copy intervals strictly after new
    while i &lt; n:
        out.append(intervals[i]); i += 1
    return out`

const insertInvariant = {
  statement: `At every pointer position, \`out\` holds exactly the final answer for all intervals \`intervals[:i]\` with respect to the carried \`new\`.`,
  initialization: `Before the loop, \`out = []\` and \`i = 0\`. Vacuously true — nothing has been placed yet.`,
  maintenance: `Phase 1 copies strictly-before intervals; they can never meet \`new\` or anything to the right of it, so they stay final. Phase 2 is the merging sweep: every interval whose start is ≤ \`new[1]\` extends \`new\`'s bounds, so after phase 2 the carried \`new\` is the union of itself and all overlapping existing intervals. Phase 3 copies strictly-after intervals; they begin past the extended \`new\`'s end so cannot touch it.`,
  termination: `All intervals have been processed. \`out\` holds pre-insert intervals, then the fully-merged \`new\`, then post-insert intervals, in sorted order.`
}

const nonOverlappingCode = `# python — greedy by end
intervals.sort(key=lambda iv: iv[1])      # sort by END
removed, cur_end = 0, float('-inf')
for s, e in intervals:
    if s &gt;= cur_end:                      # keep this interval
        cur_end = e
    else:                                 # overlap → remove this one
        removed += 1
return removed`

const nonOverlappingInvariant = {
  statement: `After processing the first k intervals, \`cur_end\` equals the minimum possible end-value among any valid non-overlapping subset of the first k; \`removed\` is the correct count of removals.`,
  initialization: `Before the loop, \`cur_end = -∞\` (no interval kept) and \`removed = 0\`. Minimum possible end for empty subset is \`-∞\`, by convention.`,
  maintenance: `Consider interval \`[s, e]\` in end-sorted order. Case A — \`s &gt;= cur_end\`: it fits after the last kept interval; keeping it gives us an interval whose end \`e\` is the smallest end achievable among any valid subset ending at or after position k (because the array is end-sorted, no earlier choice could produce a smaller end). Case B — \`s &lt; cur_end\`: this interval overlaps the one anchoring \`cur_end\`. We can keep at most one of them, and \`cur_end\` already has the smaller end (it came earlier in the end-sorted order), so dropping \`[s,e]\` is at least as good as any swap. Increment \`removed\`.`,
  termination: `All intervals are processed. The greedy exchange argument shows the kept set is a maximum non-overlapping subset, so \`removed = n - (max non-overlapping count)\`.`
}

const meetingRoomsCode = `# python — adjacent-check after start-sort
def can_attend_all(meetings):
    meetings.sort(key=lambda iv: iv[0])
    for i in range(1, len(meetings)):
        if meetings[i][0] &lt; meetings[i-1][1]:
            return False
    return True`

const meetingRoomsInvariant = {
  statement: `If any pair of meetings overlap, there exist two adjacent (in start-sorted order) ones that overlap.`,
  initialization: `Trivial: a single meeting has no conflicts.`,
  maintenance: `Suppose meetings \`a, b, c\` in start-sorted order with \`a\` and \`c\` overlapping (so \`c.start &lt; a.end\`). Then \`b.start &lt;= c.start &lt; a.end\`, so \`a\` and \`b\` overlap too — and they're adjacent. By induction, any pair-overlap manifests as an adjacent-pair overlap in sorted order.`,
  termination: `After sorting, scanning adjacent pairs catches every conflict. If none fire, no pair overlaps and one person can attend them all.`
}

const trapAcode = {
  statement: `Touching endpoints: \`[1,5]\` and \`[5,10]\` — half-open \`[s,e)\` (meetings) are not overlapping; closed \`[s,e]\` (number-line) are.`,
  bug: `Using \`next.start &lt;= cur.end\` on half-open interval problems (Meeting Rooms, Google Calendar busy blocks) merges meetings that end exactly when the next starts — wrong.`,
  fix: `Clarify endpoint semantics BEFORE coding. Half-open → \`next.start &lt; cur.end\`. Closed → \`next.start &lt;= cur.end\`. Problem statements rarely spell it out; ask explicitly.`
}

const trapBcode = {
  statement: `Sort key by output type: start for merge/attend-all, end for max-non-overlapping / min-arrows.`,
  bug: `Sorting by start when the question is "minimum removals to make non-overlapping" produces a sub-optimal greedy (keeps earliest-starting instead of earliest-ending), silently wrong on \`[[1,100],[2,3],[3,4]]\` (right answer 1, start-sort gives 2).`,
  fix: `Decide sort key from the output: start-sort when you emit the union; end-sort when you count-keep or count-remove. If you're not sure, write the exchange argument on scratch paper before coding.`
}

const trapCcode = {
  statement: `Insert-interval boundary off-by-one: strict \`&lt;\` vs non-strict \`&lt;=\` on phase edges.`,
  bug: `Writing \`while i &lt; n and intervals[i][1] &lt;= new[0]:\` in phase 1 (should be \`&lt;\`) copies an interval that actually touches \`new\` on closed intervals — \`new\` never grows left; you emit \`[1,2], [2,8]\` instead of merged \`[1,8]\`.`,
  fix: `Phase 1 skips intervals whose end is strictly less than \`new.start\`. Phase 2 merges intervals whose start is \`&lt;= new.end\`. If the interval's end touches \`new.start\` on closed intervals, it belongs to phase 2 (it merges), not phase 1.`
}

const quizQuestions = [
  {q: "Standard Merge Intervals: sort by what?", choices: [{text: "Start ascending", correct: true, explanation: "Then walk once and merge on overlap."}, {text: "End ascending", correct: false, explanation: "Better for activity selection / non-overlap counting."}, {text: "Length descending", correct: false}, {text: "Random", correct: false}]},
  {q: "For Insert Interval into a pre-sorted list, what is the canonical algorithm?", choices: [{text: "Three-phase single pass: copy-before, merge-overlapping, copy-after", correct: true, explanation: "O(n) time; no re-sort needed since input is sorted."}, {text: "Insert then run full Merge Intervals", correct: false, explanation: "Works but O(n log n)."}, {text: "Sort by end and use greedy", correct: false, explanation: "That is Non-overlap Intervals."}, {text: "Binary search only", correct: false}]},
  {q: "Non-overlapping Intervals: greedy correctness requires sorting by…?", choices: [{text: "End ascending — keep the interval that frees the timeline earliest", correct: true, explanation: "Exchange argument: swapping any kept interval for one with an earlier end can only help future choices."}, {text: "Start ascending", correct: false, explanation: "Silently wrong on cases like [[1,100],[2,3],[3,4]]."}, {text: "Length ascending", correct: false, explanation: "Length ignores where intervals sit on the line."}, {text: "Doesn't matter — all orderings give the same answer", correct: false}]},
  {q: "For Meeting Rooms I (bool \"can attend all\"), what is the O(n log n) check?", choices: [{text: "Sort by start; verify each start ≥ previous end", correct: true, explanation: "By the adjacency lemma, any pair-overlap shows up adjacent in start-sorted order."}, {text: "Full n² pair check", correct: false, explanation: "Wasteful."}, {text: "Union-Find", correct: false}, {text: "DP", correct: false}]},
  {q: "Interval List Intersections (two sorted disjoint lists) is best solved by:", choices: [{text: "Two-pointer merge with `[max(starts), min(ends)]` intersection formula", correct: true, explanation: "O(n+m) linear pass."}, {text: "Sort both then binary search", correct: false, explanation: "Already sorted; unnecessary sort."}, {text: "Union all then re-detect overlaps", correct: false, explanation: "Overkill."}, {text: "Recursion", correct: false}]}
]

const insertSolvePrompt = `Given a sorted, non-overlapping list of intervals and a new interval \`[s,e]\`, insert it and return the merged list — in one pass, no re-sort.`

const nonOverlappingSolvePrompt = `Return the minimum number of intervals to remove so the remaining ones are non-overlapping. Example: \`[[1,2],[2,3],[3,4],[1,3]]\` → 1 (remove \`[1,3]\`).`

const meetingRoomsSolvePrompt = `Given meeting intervals \`[[s,e], ...]\`, decide whether one person can attend all of them. Return a boolean.`
</script>

## Why merge intervals exists — the story

You're building the calendar backend for Google Meet. Users grant you a list of "busy" blocks from their Outlook, Zoom, and Slack calendars. Before showing free/busy to a meeting scheduler, you must **merge** overlapping busy blocks into one clean list.

The honest first attempt: for each pair of intervals, check if they overlap and merge. Nested loop. For 50 busy blocks per user (typical exec calendar), it's `~1,250` comparisons — instant. And it's a legit first answer: interviewers accept it as the baseline.

But at scale it dies. Meet processes calendar-merge requests for **1 billion users** to power its "find a time" feature. If each user has 200 busy blocks (5-day rolling window), naive is `200² = 40,000` ops per user × `10⁹` users = `4·10¹³` ops. At 100M ops/sec per core, that's **12 million CPU-hours** — daily. Google's infra team would notice.

The pattern is: sort once, then sweep left to right. After sort, if the next interval's start is `≤` the current merged block's end, extend the block; otherwise, close the block and open a new one. **O(n log n)** sort + **O(n)** sweep. For 200 blocks per user, that's ~1,500 ops — 25× faster and, more importantly, asymptotically better. What makes this work is an **invariant**: after sorting by start time, every interval you've already emitted is final; only the current one can still grow. Sorting turned a global relation ("does this overlap with any of the 199 others?") into a local check ("does this touch the previous?").

<Callout kind="key" title="Key Insight">

Two intervals `[a,b]` and `[c,d]` overlap iff `a ≤ d && c ≤ b`. After sorting by start, overlap with the running interval is simply `next.start ≤ cur.end`.

</Callout>

<Callout kind="key" title="Key Insight — sort direction depends on the question.">

For "merge all overlaps," sort by **start**. For "minimum arrows to burst balloons" or "max non-overlapping," sort by **end**. For "erase overlaps," end-sort simplifies the greedy proof. **Wrong sort key = wrong invariant = silently wrong answer.**

</Callout>

## The bare mechanic — simplest working example

Input: `[[1,3],[2,6],[8,10],[15,18]]` (already start-sorted). Walk left to right, carrying one "current" interval. Each next interval either overlaps (extend end) or doesn't (emit current, start fresh).

| Step | next | cur before | overlap? | cur after | out |
|---|---|---|---|---|---|
| 0 | — | — | — | `[1,3]` | `[]` |
| 1 | `[2,6]` | `[1,3]` | `2 ≤ 3` yes | `[1,6]` | `[]` |
| 2 | `[8,10]` | `[1,6]` | `8 > 6` no | `[8,10]` | `[[1,6]]` |
| 3 | `[15,18]` | `[8,10]` | `15 > 10` no | `[15,18]` | `[[1,6],[8,10]]` |
| end | — | — | — | — | `[[1,6],[8,10],[15,18]]` |





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" role="img" viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Bare mechanic — four intervals becoming three merged ranges">
  <rect x="0" y="0" width="400" height="180" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">sort by start, then one-pass merge</text>
  <line x1="30" y1="56" x2="370" y2="56" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <g text-anchor="middle" font-size="10" fill="var(--dsa-neutral)">
    <text x="40" y="74">1</text><text x="80" y="74">3</text><text x="70" y="74">2</text><text x="140" y="74">6</text>
    <text x="190" y="74">8</text><text x="230" y="74">10</text><text x="310" y="74">15</text><text x="360" y="74">18</text>
  </g>
  <rect x="40" y="88" width="40" height="12" rx="5" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.4"/>
  <rect x="70" y="102" width="70" height="12" rx="5" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.4"/>
  <rect x="190" y="88" width="40" height="12" rx="5" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.4"/>
  <rect x="310" y="88" width="50" height="12" rx="5" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.4"/>
  <rect x="40" y="130" width="100" height="14" rx="5" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)" stroke-width="1.6"/>
  <rect x="190" y="130" width="40" height="14" rx="5" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)" stroke-width="1.6"/>
  <rect x="310" y="130" width="50" height="14" rx="5" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)" stroke-width="1.6"/>
  <g font-size="10" font-weight="700" text-anchor="middle" fill="var(--dsa-warning)">
    <text x="90" y="141">[1,6]</text><text x="210" y="141">[8,10]</text><text x="335" y="141">[15,18]</text>
  </g>
  <text x="200" y="168" text-anchor="middle" font-size="11" font-style="italic" fill="var(--dsa-neutral)">overlapping cluster collapses; gaps mark new intervals</text>
</svg>
</div>




<PatternTemplateCard
  slug="merge-intervals-template"
  language="python"
  :code="bareTemplateCode"
  :invariant="bareInvariant"
  :complexity="bareComplexity"
  problemShape="start-sorted interval list; return disjoint union"
  defaultRevealed />

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

## History — Bentley's *Programming Pearls*, 1986

The interval-merging pattern was formalized by **Jon Bentley** in his classic 1986 book **Programming Pearls**, specifically in the essay *"Column 8: Algorithm Design Techniques."* Bentley used the interval-cover problem as a running example to teach the general principle: **when brute force is quadratic pairwise comparison, sort first and reduce it to a linear sweep.** His larger contribution was the "sort-then-sweep" idiom, which underlies not just Merge Intervals but the entire interval-scheduling family (Meeting Rooms, Non-overlapping Intervals, Insert Interval).

Bentley was also a co-inventor of **kd-trees** and *Bentley-Ottmann sweep* (see the Sweep Line chapter). His *Programming Pearls* essays first appeared as columns in *Communications of the ACM*; every essay taught one specific transformation from naive to elegant algorithm. When you tell an interviewer "I'll sort by start time and sweep in O(n log n)," you're citing exactly the pattern Bentley wrote about in 1986.

## THE template

The pattern has one canonical shape and four sub-variations. The template is the shape; the sub-variations differ in *sort key*, *what you carry*, and *what you emit*. The chip row below jumps to each sub-variation.

<PatternTemplateCard
  slug="merge-intervals-canonical"
  title="Merge-Intervals canonical sweep"
  language="python"
  :code="bareTemplateCode"
  :invariant="bareInvariant"
  :complexity="bareComplexity"
  :specializations="templateSpecializations"
  problemShape="interval list → sort → single left-to-right pass with one carried state" />

## Interactive diagram

<MergeIntervalsAnim />

## Sub-variations of the template

<PatternSubVariationNav pattern="merge-intervals" />

### Classic Merge Intervals <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Merge Intervals](https://leetcode.com/problems/merge-intervals/)*

<ProgressCheck id="merge-intervals" />

<InvariantProof
  :statement="bareInvariant.statement"
  :initialization="bareInvariant.initialization"
  :maintenance="bareInvariant.maintenance"
  :termination="bareInvariant.termination" />





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" role="img" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Diagram illustrating: Merge Intervals Medium">
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

#### Problem
Given a list of intervals, **merge all overlapping** ones and return the disjoint result.

**Constraints:** `1 ≤ n ≤ 10⁴`; `start ≤ end`; values up to 10⁴.

**Example 1:** `[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`.

**Example 2:** `[[1,4],[4,5]]` → `[[1,5]]` because touching closed intervals merge.

#### Solution — brute force
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

#### Solution — optimized
Sort by start; extend the current interval while the next overlaps.

**Steps:**
1. Sort the intervals by `start` — O(n log n) prerequisite for the linear sweep.
2. Initialize `out` with the first interval.
3. For each subsequent interval `cur`: if `cur.start <= last.end` — they overlap or touch; update `last.end = max(last.end, cur.end)`.
4. Otherwise — push `cur` as a new interval.
5. Return `out`. O(n log n) total.



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

**Time:** O(n log n). Sorting dominates; the sweep is O(n).
**Space:** O(n) for the output list in the worst case.

#### Why sorting by start is the invariant-maker
After sorting by start, suppose `cur = [1,6]` and the next interval is `[8,10]`. Every later interval starts at least `8`, so no later interval can overlap `[1,6]`. That means `[1,6]` is safe to emit permanently. Without sorting, seeing `[8,10]` tells you nothing; a later `[4,5]` could still overlap the old block. The overlap check also becomes one-sided: general overlap is `a.start <= b.end && b.start <= a.end`, but when `cur.start <= next.start` is guaranteed by sorting, the first half is automatic.

#### Closed, open, and half-open intervals

LeetCode's Merge Intervals uses closed intervals, so `[1,2]` and `[2,3]` overlap at point `2` and merge into `[1,3]`. Many scheduling systems use half-open intervals, where `[1,2)` ends exactly when `[2,3)` begins; those do not overlap. The only code change is the comparison: closed → `next.start <= cur.end`; half-open → `next.start < cur.end`. State your assumption before choosing `<` or `<=`.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Sort by START is the only correct pre-step.** Once sorted, every overlap is LOCAL (adjacent in sorted order) and a one-pass fold suffices. Sorting by end gives wrong answers on inputs like `[1,10],[2,3],[4,5]`.
- **Overlap test depends on interval convention.** Closed intervals (LeetCode default) → `next.start <= cur.end` ("touching" counts). Half-open intervals → `next.start < cur.end`. Decide BEFORE writing the comparison.
- **Extend the end to `max(cur.end, next.end)`, not `next.end`.** The second interval might be fully contained inside the first (e.g. `[1,10]` + `[2,3]`), in which case the end does not change — a plain assignment would shrink it incorrectly.
- **O(n log n) time dominated by the sort; the fold itself is O(n).** Space is O(1) extra if you can modify the input, else O(n) for the output list.
- **This fold is the ENGINE for the whole chapter** — insert, non-overlap, meeting rooms, employee-free-time all compose with or reduce to this same one-pass merge after sort-by-start.

</details>

---

### Insert Interval <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Insert Interval](https://leetcode.com/problems/insert-interval/)*

<Callout kind="key" title="The twist:">

input is already sorted and disjoint, so you don't need to sort. Walk through once, carrying `new` in your hand, and emit three phases: strictly-before, overlap-merge-into-new, strictly-after.

</Callout>

<InvariantProof
  :statement="insertInvariant.statement"
  :initialization="insertInvariant.initialization"
  :maintenance="insertInvariant.maintenance"
  :termination="insertInvariant.termination" />





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" role="img" viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Insert Interval three-phase trace">
  <rect x="0" y="0" width="400" height="180" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">insert [4,8] into sorted list</text>
  <line x1="20" y1="56" x2="380" y2="56" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <rect x="30" y="68" width="22" height="12" rx="4" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/>
  <text x="41" y="78" text-anchor="middle" font-size="9" fill="var(--dsa-neutral)">[1,2]</text>
  <rect x="65" y="68" width="48" height="12" rx="4" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)"/>
  <text x="89" y="78" text-anchor="middle" font-size="9" fill="var(--dsa-warning)">[3,5]</text>
  <rect x="130" y="68" width="22" height="12" rx="4" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)"/>
  <text x="141" y="78" text-anchor="middle" font-size="9" fill="var(--dsa-warning)">[6,7]</text>
  <rect x="170" y="68" width="42" height="12" rx="4" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)"/>
  <text x="191" y="78" text-anchor="middle" font-size="9" fill="var(--dsa-warning)">[8,10]</text>
  <rect x="245" y="68" width="55" height="12" rx="4" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/>
  <text x="272" y="78" text-anchor="middle" font-size="9" fill="var(--dsa-neutral)">[12,16]</text>
  <rect x="95" y="96" width="90" height="12" rx="4" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
  <text x="140" y="106" text-anchor="middle" font-size="10" fill="var(--dsa-primary)">new = [4,8]</text>
  <rect x="30" y="130" width="22" height="14" rx="5" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/>
  <rect x="65" y="130" width="147" height="14" rx="5" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/>
  <rect x="245" y="130" width="55" height="14" rx="5" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/>
  <g font-size="10" font-weight="700" text-anchor="middle" fill="var(--dsa-success)">
    <text x="41" y="140">[1,2]</text><text x="138" y="140">[3,10]</text><text x="272" y="140">[12,16]</text>
  </g>
  <text x="200" y="166" text-anchor="middle" font-size="10" font-style="italic" fill="var(--dsa-neutral)">three phases: before-copy, merge-with-new, after-copy</text>
</svg>
</div>




<Callout kind="key" title="Blind-solve first:">

{{ insertSolvePrompt }}

</Callout>

<TemplateReveal
  slug="insert-interval"
  language="python"
  :canonical="insertIntervalCode"
  problemShape="sorted non-overlapping list + new interval → 3-phase sweep" />

**Trace** on `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]`, `new = [4,8]`:
- `[1,2]`: end `2 < 4` → phase 1, copy → `out = [[1,2]]`.
- `[3,5]`: start `3 <= 8` → phase 2, `new` grows to `[3,8]`.
- `[6,7]`: start `6 <= 8` → phase 2, `new` grows to `[3,8]` (unchanged — already covers it).
- `[8,10]`: start `8 <= 8` → phase 2 (touching counts), `new` grows to `[3,10]`.
- `[12,16]`: start `12 > 10` → phase 3; emit `new = [3,10]`, then copy `[12,16]`.
- **Result:** `[[1,2],[3,10],[12,16]]`.

**Why this beats "insert then run full merge":** no sort pass. `O(n)` instead of `O(n log n)` — exploits the pre-sorted invariant the caller already paid for.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Three-phase scan maps to loop structure.** (1) copy intervals strictly BEFORE the new one, (2) merge all intervals that overlap the new one into ONE, (3) copy intervals strictly AFTER. Clean phase boundaries beat a tangled conditional.
- **Overlap tests are STRICT inequalities.** `intervals[i].start > newInterval.end` means "we are past overlap"; `intervals[i].end < newInterval.start` means "not yet overlapping". The complement — neither condition true — is overlap.
- **Shrink the newInterval in place during phase 2** — on each overlap, update `newInterval = [min(start, i.start), max(end, i.end)]`; append it once at the phase-2 → phase-3 boundary.
- **O(n) time — DO NOT re-sort.** The input is pre-sorted; a sort-then-merge solution is `O(n log n)` and signals you missed the gift the problem gave you. This is the ONLY problem in the chapter where the input is pre-sorted.
- **Space is O(n) for the output list.** The algorithm itself keeps only `i` and the growing `newInterval` — the extra space is unavoidable since you must emit a new list to be safe for the caller.

</details>

---

### Non-overlapping Intervals <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)*

<Callout kind="key" title="The twist:">

sort by **end**, not start. The greedy "keep the earliest-ending interval first" works because an earlier end leaves more room for future choices — classic exchange argument.

</Callout>

<InvariantProof
  :statement="nonOverlappingInvariant.statement"
  :initialization="nonOverlappingInvariant.initialization"
  :maintenance="nonOverlappingInvariant.maintenance"
  :termination="nonOverlappingInvariant.termination" />





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" role="img" viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Non-overlapping end-sort greedy">
  <rect x="0" y="0" width="400" height="180" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">sort by END; keep earliest finishers</text>
  <line x1="20" y1="60" x2="380" y2="60" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <rect x="30" y="72" width="30" height="12" rx="4" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <text x="45" y="82" text-anchor="middle" font-size="9" fill="var(--dsa-success)">[1,2] ✓</text>
  <rect x="60" y="90" width="30" height="12" rx="4" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <text x="75" y="100" text-anchor="middle" font-size="9" fill="var(--dsa-success)">[2,3] ✓</text>
  <rect x="90" y="72" width="30" height="12" rx="4" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <text x="105" y="82" text-anchor="middle" font-size="9" fill="var(--dsa-success)">[3,4] ✓</text>
  <rect x="30" y="110" width="90" height="12" rx="4" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="1.6"/>
  <text x="75" y="120" text-anchor="middle" font-size="9" fill="var(--dsa-danger)">[1,3] ✗ removed</text>
  <text x="200" y="150" text-anchor="middle" font-size="11" font-style="italic" fill="var(--dsa-neutral)">removed = 1 (minimum to make the rest non-overlapping)</text>
</svg>
</div>




<Callout kind="key" title="Blind-solve first:">

{{ nonOverlappingSolvePrompt }}

</Callout>

<TemplateReveal
  slug="non-overlapping-intervals"
  language="python"
  :canonical="nonOverlappingCode"
  problemShape="interval list → end-sort → one-pass greedy keep/drop" />

**Trace** on `intervals = [[1,2],[2,3],[3,4],[1,3]]`:
- End-sort: `[[1,2],[2,3],[1,3],[3,4]]`. (Ties between `[2,3]` and `[1,3]` broken by second key, but either order works for the count — think about why.)
- `[1,2]`: `1 >= -∞` → keep; `cur_end = 2`.
- `[2,3]`: `2 >= 2` → keep (touching ok under problem's convention); `cur_end = 3`.
- `[1,3]`: `1 < 3` → remove; `removed = 1`.
- `[3,4]`: `3 >= 3` → keep; `cur_end = 4`.
- **Result:** `removed = 1`.

<Callout kind="key" title="Why start-sort fails here:">

on `[[1,100],[2,3],[3,4]]`, start-sort would greedy-keep `[1,100]` first (it starts first), then be forced to remove both `[2,3]` and `[3,4]` — `removed = 2`. But the right answer is `1` (remove `[1,100]`, keep the other two). End-sort picks `[2,3]` first (end `3` &lt; end `100`), leaves room for `[3,4]`, and drops `[1,100]`.

</Callout>

**Related sibling: Minimum Arrows to Burst Balloons** uses the same end-sort greedy — count the kept intervals instead of the removed ones. Also related: **Weighted Interval Scheduling** needs DP (not greedy) because weights break the exchange argument.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Greedy by END, not by START.** The exchange argument: whichever interval finishes first leaves the most room for the rest, so it is always safe to keep. Sort-by-start would greedy-pick a long-reaching interval and FORCE removals that end-sort avoids.
- **The invariant: `prevEnd` is the end of the LAST KEPT interval.** Next interval is kept iff `interval.start >= prevEnd`; otherwise it is counted as a removal and `prevEnd` stays put.
- **Removals = total − kept.** Different variants ask for the removal count, the kept set, or the kept count; convert between them with this one line.
- **Concrete counter-example for sort-by-start:** on `[1,100],[2,3],[3,4]`, start-sort keeps `[1,100]` and removes both others (2 removals); end-sort keeps `[2,3]` and `[3,4]`, dropping `[1,100]` (1 removal — the correct answer).
- **This IS Activity Selection, the classic greedy exchange-argument problem.** When the "sort by end" instinct kicks in, recognize the family.
- **Minimum Arrows to Burst Balloons** is literally the same code — the count of KEPT intervals instead of removed ones.

</details>

---

### Meeting Rooms I <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Meeting Rooms](https://leetcode.com/problems/meeting-rooms/)*

<Callout kind="key" title="The twist:">

boolean answer, not merged intervals. Any pair-conflict in the input shows up as an *adjacent-pair* conflict after start-sort, so a single O(n) adjacent scan after sort gives the answer.

</Callout>

<InvariantProof
  :statement="meetingRoomsInvariant.statement"
  :initialization="meetingRoomsInvariant.initialization"
  :maintenance="meetingRoomsInvariant.maintenance"
  :termination="meetingRoomsInvariant.termination" />





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" role="img" viewBox="0 0 400 160" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Meeting Rooms I adjacency check">
  <rect x="0" y="0" width="400" height="160" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">adjacent overlap after start-sort → conflict</text>
  <line x1="30" y1="56" x2="370" y2="56" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <rect x="40" y="68" width="80" height="14" rx="5" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
  <text x="80" y="78" text-anchor="middle" font-size="10" fill="var(--dsa-primary)">[0,30]</text>
  <rect x="55" y="88" width="25" height="14" rx="5" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="1.6"/>
  <text x="68" y="98" text-anchor="middle" font-size="9" fill="var(--dsa-danger)">[5,10]</text>
  <rect x="140" y="88" width="50" height="14" rx="5" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/>
  <text x="165" y="98" text-anchor="middle" font-size="9" fill="var(--dsa-neutral)">[15,20]</text>
  <text x="200" y="130" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-danger)">meetings[1].start = 5 lt meetings[0].end = 30 → cannot attend all</text>
</svg>
</div>




<Callout kind="key" title="Blind-solve first:">

{{ meetingRoomsSolvePrompt }}

</Callout>

<TemplateReveal
  slug="meeting-rooms-i"
  language="python"
  :canonical="meetingRoomsCode"
  problemShape="interval list → start-sort → check all adjacent pairs" />

**Trace** on `[[0,30],[5,10],[15,20]]`:
- Start-sort: already sorted.
- Pair `(1): meetings[1][0] = 5, meetings[0][1] = 30`. `5 < 30` → return `False`.

**Why this is strictly weaker than Meeting Rooms II:** Rooms I returns a boolean; Rooms II returns the minimum room count. For the count, start+end-sort separately and sweep (chapter 32 Sweep Line) — merged ranges tell you *which blocks are busy*, but not *how many simultaneous meetings*. If you merge `[1,10]`, `[2,3]`, `[4,5]`, you get one block `[1,10]`, which doesn't reveal whether you needed two rooms or three.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **The simplest interval problem.** Sort by start, check `intervals[i].start < intervals[i-1].end` for any adjacent overlap; return false on the first hit.
- **Any pair-overlap shows up as an ADJACENT-pair overlap after start-sort.** This is why one O(n) adjacent scan is sufficient after the O(n log n) sort — you don't need an all-pairs check.
- **Short-circuit on first conflict.** As soon as one overlap is found, the answer is false; no point in continuing to scan.
- **Edge-touch (`[1,2]` and `[2,3]`) is NOT overlap for scheduling** — a meeting ending at 2:00 doesn't block one starting at 2:00. Use strict `<`, not `<=`. Different problems (interval-merge, calendar-overlap) have different conventions; always re-read the statement.
- **O(n log n) time (sort), O(1) scan.** Space is O(1) if you can mutate input, O(n) for a sorted copy otherwise.
- **Meeting Rooms II is a DIFFERENT problem** — needs a min-heap of end times OR Sweep Line. The boolean form (Rooms I) and the count form (Rooms II) look similar but solve differently; don't blur them in interviews.

</details>

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

## In the wild — Google Calendar conflict detection

Google Calendar's "Find a time" feature in Meet reads busy intervals from every attendee's connected calendars (Google, Outlook, Zoom, Slack-blocked time), merges them per attendee, then intersects the free-time blocks across all attendees. The merge step is the kernel of this chapter — same `sort-by-start + sweep` sweep, same `max(cur.end, next.end)` extension — scaled to:

- **~1 billion active users** (as of 2024), each with up to a few hundred busy intervals in the 7-day lookahead window.
- **Hundreds of millions of "find a time" requests per day.** Each pulls busy data for N attendees in parallel, merges each independently, then intersects.
- **Hard sub-second latency budget** — the suggest-time dropdown has to appear instantly after you add attendees to a meeting.

Related production uses:
- **Kubernetes `PodDisruptionBudget`** merges maintenance windows across node pools to check whether a drain is safe.
- **AWS Reserved Instance billing** merges overlapping usage records across EC2/RDS/EKS by the hour to apply RI discounts correctly.
- **Video-editing timelines** (DaVinci Resolve, Premiere) merge overlapping clip ranges on a track when the user drags one into another.
- **grep's `-f FILE`** uses an interval-merge pass to collapse adjacent/overlapping file-offset ranges when printing matches with `-A/-B/-C` context flags.

## Recognition drill

<RecognitionDrill pattern="merge-intervals" :count="10" />

## Advanced — follow-ups and failure modes

<details>
<summary><b>What if intervals stream in and the list can't fit in RAM?</b></summary>

Use a **TreeMap keyed by start** (Java `TreeMap<Integer, Integer>` or C++ `std::map<int,int>`). On each new `[s, e]`:
1. Find the predecessor and successor by start; merge with the predecessor if `pred.end >= s`.
2. Advance forward absorbing every successor whose start ≤ current end.
3. Insert the merged entry.

Each operation is `O(log n)` amortized; total `O(n log n)` across n intervals streamed. This also handles **"query active intervals at time t"** in `O(log n)` via `floorEntry(t)`.

**Where it's used:** financial order books (merging limit orders at the same price level), network flow sampling (merging overlapping sampling windows).
</details>

<details>
<summary><b>What if each interval has a weight and you want max-weight non-overlapping subset?</b></summary>

Greedy fails. Example: weights `[10, 1, 1]` on intervals `[[1,10], [2,3], [4,5]]`. End-sort greedy picks the two short intervals (total weight 2); correct answer picks `[1,10]` alone (weight 10).

Use **DP**: sort by end; let `dp[i] = max(dp[i-1], w[i] + dp[p(i)])` where `p(i)` is the latest interval ending before `i`'s start (found via binary search). `O(n log n)` total. This is the **Weighted Interval Scheduling** problem — Kleinberg & Tardos cover it at length. Comes up in: ad slot auctions (each ad has a bid × duration), CPU batch job scheduling, DNA sequence alignment.
</details>

<details>
<summary><b>What if intervals are on a circle (24h schedule, wrapping)?</b></summary>

A "circular interval" `[22, 2]` wraps around midnight. Standard trick: **split** each wrapping interval into `[22, 24]` and `[0, 2]`, then run the standard sweep. Beware the final merge pass must check if the first and last merged intervals wrap around (first starts at 0, last ends at 24 — merge them into one wrapping interval if needed).

**Where it's used:** radio frequency allocation, 24h on-call rotations, satellite coverage windows.
</details>

<details>
<summary><b>What if the output needs to be max-coverage with ≤ k intervals (budget constraint)?</b></summary>

**NP-hard in general** (maximum coverage problem). Use the **greedy** approximation: repeatedly pick the interval that covers the most uncovered points. Guaranteed to achieve `1 - 1/e ≈ 63%` of optimal (Nemhauser et al., 1978). Comes up in sensor placement, ad-impression maximization under budget.
</details>

<details>
<summary><b>Breaking point — when does sort-sweep stop being enough?</b></summary>

- **2-D intervals** (axis-aligned rectangles): sort-sweep becomes `O(n²)` because a single x-axis sort doesn't localize y-overlap. Use **sweep line + segment tree on y** (chapter 32).
- **n &gt; 10⁸ with values in {0, 1, …, 10⁴}**: sort itself is `O(n log n)`; using a **bucket of flags** indexed by value gives O(n + V) and beats sort when V is small.
- **Mutable intervals under concurrent writes**: a plain `TreeMap` serializes. Use **interval tree with per-node locks** or **optimistic concurrency with retry**.
</details>

### Cross-pattern problems

| Problem | Primary pattern | What the merge pattern contributes |
|---|---|---|
| [Employee Free Time](https://leetcode.com/problems/employee-free-time/) | k-way merge + interval merge | merge all employees' busy blocks across their schedules, then emit gaps |
| [Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) | two-pointers | each intersection is `[max(starts), min(ends)]`; advance the earlier-ending list |
| [My Calendar II / III](https://leetcode.com/problems/my-calendar-ii/) | sweep line + overlap-tracker | merge intervals is the base case (My Calendar I); II/III track overlap counts |

## Related patterns + Check your understanding

<RelatedPatterns pattern-id="intervals" />

<Quiz
  pattern-id="merge-intervals"
  :questions="quizQuestions" />

<PrintButton />
