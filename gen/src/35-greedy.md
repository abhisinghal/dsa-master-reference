# Greedy


<PatternVideo pattern-name="Greedy" duration="8–12 min" />

<PatternProgress pattern-id="greedy" problems="jump-game-ii, jump-game, gas-station, best-time-to-buy-and-sell-stock, maximum-subarray, non-overlapping-intervals, minimum-number-of-arrows-to-burst-balloons, course-schedule-iii, maximum-length-of-pair-chain, video-stitching, jump-game-iii" />



## Why greedy exists — the story

Greedy is the "grab the best-looking option right now and never look back" strategy. When it works it's beautiful — usually just *sort, then sweep once*. The catch is that "best right now" isn't always "best overall," so a greedy algorithm is only correct when two properties hold: the **greedy-choice property** (a locally optimal pick is safe to commit to) and **optimal substructure** (what's left is a smaller version of the same problem). In an interview the code is the easy part; the points come from *proving* it — most often with an **exchange argument**, where you show that any optimal solution can be nudged, one swap at a time, into the greedy one without ever getting worse.

A brute-force solution usually enumerates choices, schedules, subsets, or paths and then picks the best valid one. Can we do better? Only when a local choice can be proved safe. The rest of the chapter is about finding that proof: farthest reach, earliest finish, minimum prefix balance, or a frequency frame.

> [key] **Key Insight** — Before coding greedy, find the sort key that makes the safe choice obvious (earliest finish, largest ratio, nearest deadline). If you can construct a counterexample to "always take the locally best," greedy is wrong → switch to DP.

## When to use it — local choices with a proof

### Recognize by
- "fewest / smallest / earliest" with a locally safe choice
- sort-then-sweep problems — activity selection, interval scheduling, non-overlapping intervals
- "jump game" family, "gas station" — verify total feasibility, commit to the earliest reset

### When NOT to use it
A locally-best choice can be regretted later — construct a counterexample ("if I take the largest coin first…") and if you find one, switch to [Dynamic Programming](#dynamic-programming). The exchange-argument proof is what separates a safe greedy from a wrong one.

---

## Jump Game II (Farthest-Reach Greedy) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Jump Game II](https://leetcode.com/problems/jump-game-ii/)*

<ProgressCheck id="jump-game-ii-farthest-reach-greedy" />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <defs>
    <marker id="ar-jump-success" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-success)"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="27" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">greedy BFS frontier: current range → farthest next</text>

  <rect x="124" y="67" width="100" height="62" rx="10" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="2.4"/>
  <text x="174" y="59" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">current range</text>
  <g text-anchor="middle">
    <rect x="76" y="76" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <rect x="124" y="76" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
    <rect x="172" y="76" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary-line)" stroke-width="1.6"/>
    <rect x="220" y="76" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <rect x="268" y="76" width="44" height="44" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
    <g font-size="17" font-weight="700" fill="var(--dsa-ink)">
      <text x="98" y="104">2</text><text x="146" y="104">3</text><text x="194" y="104">1</text><text x="242" y="104">1</text><text x="290" y="104">4</text>
    </g>
    <g font-size="11" fill="var(--dsa-neutral)">
      <text x="98" y="140">0</text><text x="146" y="140">1</text><text x="194" y="140">2</text><text x="242" y="140">3</text><text x="290" y="140">4</text>
    </g>
  </g>
  <path d="M146 151 C171 182, 244 182, 290 124" fill="none" stroke="var(--dsa-success)" stroke-width="2" marker-end="url(#ar-jump-success)"/>
  <text x="223" y="174" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-success)">farthest = max(i + nums[i]) = 4</text>
  <rect x="40" y="196" width="320" height="31" rx="10" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
  <text x="200" y="216" text-anchor="middle" font-size="11.5" fill="var(--dsa-neutral)">when index passes end, jump++ and current-range = farthest so far</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> Treat each jump count as a BFS layer; scan all indices in the current range, remember the farthest next range, and take one jump only when the current range is exhausted.</div>

### Problem
Each `nums[i]` is the **max jump length** from index `i`. Find the **fewest jumps** to reach the last index (reaching the end is always possible).

**Constraints:** `1 ≤ n ≤ 10⁴`; `0 ≤ nums[i] ≤ 1000`.

**Example 1:** `[2,3,1,1,4]` → `2` (jump `0→1→4`).

<ExamplePreview compact :input="['2', '3', '1', '1', '4']" :output="['2']" />

**Example 2:** `[2,3,0,1,4]` → `2` (jump `0→1→4`).

<ExamplePreview compact :input="['2', '3', '0', '1', '4']" :output="['2']" />

### Solution — brute force
Brute force models each index as a node and explores every reachable next index to find the shortest path to the end. A plain recursive search can be exponential because it branches over all jump lengths; BFS is O(n²) in the worst case if every index reaches many later indices. The optimized greedy scan compresses BFS levels into two integers: the current frontier and the farthest next frontier.

```text
queue = [0]
steps = 0
while queue is not empty:
    pop every index in the current BFS layer
    push every reachable next index not seen before
    if the last index is reached, return steps + 1
```

Brute force complexity: naive BFS can examine O(n²) edges; recursive enumeration can be exponential.

### Solution — optimized
BFS-like level expansion: from the current reachable range, jump to the farthest reachable next.

> [inv] **Invariant** — `curEnd` is the boundary of positions reachable in `jumps` steps; `farthest` is the boundary reachable in `jumps+1`. When `i` hits `curEnd`, one more jump is forced.

#### Java
```java
int jump(int[] a) {
    int jumps = 0, curEnd = 0, farthest = 0;
    for (int i = 0; i < a.length - 1; i++) {
        farthest = Math.max(farthest, i + a[i]);
        if (i == curEnd) { jumps++; curEnd = farthest; }
    }
    return jumps;
}
```

> [note] **Trace it** — `[2,3,1,1,4]`. From index 0 (reach 2) the best next hop is index 1 (which reaches index 4). Two jumps `0→1→4` → answer **2**.

> [note] **Interview script** — "I first confirm identical tasks need at least `n` intervals between runs and idle slots are allowed. I start with brute force by enumerating or simulating possible schedules, which is exponential if I search all valid orders. I optimize by counting frequencies and using the max-frequency frame formula, giving O(tasks + A) time and O(A) space for alphabet size `A`."


<CodeTrace
  title="Jump Game II — nums=[2,3,1,1,4]"
  :values="[2,3,1,1,4]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { end: 0, farthest: 2, jumps: 0 }, note: "from 0 can reach up to 2" },
    { pointers: { i: 1 }, vars: { end: 2, farthest: 4, jumps: 1 }, note: "i==end → commit jump. best from window=[1,2] reaches 4", added: [1] },
    { pointers: { i: 2 }, vars: { end: 2, farthest: 4, jumps: 1 }, note: "no better than 4" },
    { pointers: { i: 3 }, vars: { end: 4, farthest: 4, jumps: 2 }, note: "i==end → jump. reaches idx 4 — done. answer 2", added: [4] }
  ]'
/>

### Time Complexity
Time O(n). Each index before the last is scanned once while updating the farthest reachable boundary.

### Space Complexity
Space O(1). The greedy scan keeps only `jumps`, `curEnd`, and `farthest`.

### Learning notes
- Why loop only to `a.length - 1`? — you do not need to jump after reaching the last index.
- Why update `farthest` every index? — it records the best next frontier from the current BFS layer.
- Why increment only at `i == curEnd`? — that is where the current jump range is exhausted.
- Why set `curEnd = farthest`? — the next jump can cover exactly the farthest range discovered so far.
- Why not choose a concrete next index? — only the frontier matters for the minimum jump count.
- Why greedy works? — farther reach dominates shorter choices within the same layer.

> [note] **Interview script** — "I first confirm the end is reachable and I need the minimum number of jumps. I start with brute force DFS or BFS over all jumps, which can be exponential for DFS or O(n²) for naive BFS. I optimize by tracking the current level boundary and farthest next reach in one pass, giving O(n) time and O(1) space."


> [key] **Key Insight** — Each "level" is the set of indices reachable with the same number of jumps; taking the farthest reach is provably optimal because it dominates every other choice's future reach.

> [trap] **Common Trap** — Counting jumps at every step instead of at the frontier. *Example:* `nums=[2,3,1,1,4]`. Incrementing `jumps` at each index gives 5; incrementing only when `i == currentEnd` (frontier boundary) gives 2. Update `currentEnd = farthest` and `jumps++` together.

<TrapTrace title="Counting jumps at every step instead of at the frontier" input="nums=[2,3,1,1,4]" bug="'nums=[2,3,1,1,4]'. Incrementing 'jumps' at each index gives 5; incrementing only when 'i == currentEnd' (frontier boundary) gives 2" fix="Update 'currentEnd = farthest' and 'jumps++' together." />

> [pat] **Pattern Connection** — This is BFS on an implicit graph collapsed to O(n). *Jump Game I* (reachability) is an even simpler farthest-reach scan.

#### Same pattern, new tweaks

"Track the farthest you can reach from the current level" is a greedy BFS in disguise:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Jump Game I](https://leetcode.com/problems/jump-game/) | just track the farthest reachable index; return whether it reaches the end | — |
| [Jump Game III](https://leetcode.com/problems/jump-game-iii/) | actual BFS/DFS since you can jump both directions by `arr[i]` | — |
| [Video Stitching / Minimum Number of Taps](https://leetcode.com/problems/video-stitching/) | the same "cover the line in fewest intervals" farthest-reach greedy | — |
| [Minimum Number of Arrows](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) | the interval-cover cousin (sort by end) | — |

## Gas Station (Prefix-Balance Greedy) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Gas Station](https://leetcode.com/problems/gas-station/)*

<ProgressCheck id="gas-station-prefix-balance-greedy" />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <defs>
    <marker id="ar-gas-primary" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="27" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">prefix-balance greedy on a circular route</text>

  <circle cx="200" cy="118" r="72" fill="none" stroke="var(--dsa-neutral-line)" stroke-width="2.4"/>
  <path d="M254 72 C282 100, 283 136, 260 165" fill="none" stroke="var(--dsa-primary)" stroke-width="2" marker-end="url(#ar-gas-primary)"/>
  <g text-anchor="middle">
    <circle cx="200" cy="46" r="15" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="1.6"/>
    <circle cx="268" cy="96" r="15" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="1.6"/>
    <circle cx="242" cy="178" r="15" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="1.6"/>
    <circle cx="158" cy="178" r="17" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
    <circle cx="132" cy="96" r="15" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
    <g font-size="12" font-weight="700" fill="var(--dsa-ink)">
      <text x="200" y="50">0</text><text x="268" y="100">1</text><text x="242" y="182">2</text><text x="158" y="182">3</text><text x="132" y="100">4</text>
    </g>
  </g>
  <g font-size="11" fill="var(--dsa-neutral)" text-anchor="middle">
    <text x="200" y="31">1/3</text><text x="304" y="98">2/4</text><text x="274" y="203">3/5</text><text x="126" y="203">4/1</text><text x="96" y="98">5/2</text>
  </g>
  <g font-size="12" font-weight="700" text-anchor="middle">
    <text x="217" y="67" fill="var(--dsa-danger)">tank -2 ✕</text>
    <text x="302" y="125" fill="var(--dsa-danger)">tank -2 ✕</text>
    <text x="244" y="223" fill="var(--dsa-danger)">tank -2 ✕</text>
    <text x="128" y="156" fill="var(--dsa-success)">candidate start</text>
    <text x="154" y="223" fill="var(--dsa-success)">tank +3</text>
    <text x="87" y="125" fill="var(--dsa-primary)">tank +6</text>
  </g>
  <text x="200" y="235" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">if tank goes negative, restart from next; single pass</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> A negative tank proves every start inside that failed segment is impossible, so the next station becomes the only candidate worth trying.</div>

### Problem
Around a circular route, station `i` provides `gas[i]` and it costs `cost[i]` to drive to the next station. Return the **starting index** from which you can complete the whole loop (or -1). A unique answer exists whenever total gas ≥ total cost.

**Constraints:** `1 ≤ n ≤ 10⁵`; values `≥ 0`.

**Example 1:** `gas = [1,2,3,4,5], cost = [3,4,5,1,2]` → `3`.

<ExamplePreview compact :input="['1', '2', '3', '4', '5', '|', '3', '4', '5', '1', '2']" :output="['3']" />

**Example 2:** `gas = [2,3,4], cost = [3,4,3]` → `-1` because total gas is insufficient.

<ExamplePreview compact :input="['2', '3', '4', '|', '3', '4', '3']" :output="['-1']" />

### Solution — brute force
Brute force tries every station as a start and simulates a full circuit while tracking tank balance. That is O(n²) time and O(1) space, and it repeats the same failing prefixes over and over. The optimized greedy scan uses the fact that if a candidate start fails at station `i`, every start inside that failed segment also fails, so the next candidate is `i + 1` after a global total check.

```text
for each station start:
    tank = 0
    for n legs around the circle:
        tank += gas[i] - cost[i]
        if tank < 0: fail this start
    if all legs succeed: return start
return -1
```

Brute force complexity: O(n²) time and O(1) extra space.

### Solution — optimized
If total gas ≥ total cost, a unique start exists; it's just after the point of minimum running balance.

> [key] **Key Insight** — If you run out of gas going from `start` to `i`, no station in `[start, i]` can be the answer (each had ≤ 0 surplus to offer) → restart at `i+1`. Total feasibility is a separate global check.

> [inv] **Invariant** — `tank` is the surplus since the current candidate start; the moment it goes negative, every earlier candidate is eliminated.

#### Java
```java
int canCompleteCircuit(int[] gas, int[] cost) {
    int total = 0, tank = 0, start = 0;
    for (int i = 0; i < gas.length; i++) {
        int diff = gas[i] - cost[i];
        total += diff;
        tank  += diff;
        if (tank < 0) { start = i + 1; tank = 0; }   // reset candidate
    }
    return total >= 0 ? start : -1;
}
```

> [note] **Trace it** — `gas=[1,2,3,4,5], cost=[3,4,5,1,2]`. Running balance bottoms out entering index 3, so start at **3**: `4→5→1→2→3` never dips below zero.

<CodeTrace
  title="Gas Station — gas=[1,2,3,4,5], cost=[3,4,5,1,2]"
  :values="[1,2,3,4,5]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { tank: -2, total: -2, start: 1 }, note: "1-3=-2 → tanklt0 → try start=1" },
    { pointers: { i: 1 }, vars: { tank: -2, total: -4, start: 2 }, note: "2-4=-2 → try start=2" },
    { pointers: { i: 2 }, vars: { tank: -2, total: -6, start: 3 }, note: "3-5=-2 → try start=3" },
    { pointers: { i: 3 }, vars: { tank: 3, total: -3, start: 3 }, note: "4-1=+3 → keep", added: [3] },
    { pointers: { i: 4 }, vars: { tank: 6, total: 0, start: 3 }, note: "5-2=+3 → sum ≥ 0. answer 3", added: [4] }
  ]'
/>

### Time Complexity
Time O(n). One pass computes total surplus and eliminates invalid start ranges.

### Space Complexity
Space O(1). Only `total`, `tank`, and `start` are stored.

### Learning notes
- Why keep `total`? — it proves whether any solution exists globally.
- Why keep `tank` separately? — it measures surplus from the current candidate start only.
- Why reset when `tank < 0`? — every station in that failed segment is impossible.
- Why set `start = i + 1`? — the next station is the first candidate not disproved by the deficit.
- Why reset `tank = 0`? — the new candidate starts with an empty local balance.
- Why return `start` only if `total >= 0`? — local recovery cannot fix global shortage.

> [note] **Interview script** — "I first confirm the route is circular and returning any valid start is enough when total gas can cover total cost. I start with brute force by simulating the full loop from every station, which is O(n²) time and O(1) space. I optimize by resetting the candidate after any negative tank and checking total surplus, giving O(n) time and O(1) space."


> [trap] **Common Trap** — Skipping the total check. *Example:* `gas=[1,2,3,4]`, `cost=[2,3,4,5]`. Total gas 10 < total cost 14, so **no** station works — but a local reset can look promising. Verify `sum(gas) >= sum(cost)`; if not, return `-1`.

<TrapTrace title="Skipping the total check" input="gas=[1,2,3,4]" bug="'gas=[1,2,3,4]', 'cost=[2,3,4,5]'. Total gas 10 lt total cost 14, so **no** station works — but a local reset can look promising. Verify 'sum(gas) gt= sum(cost)'; if not, return '-1'." fix="See the guidance in the trap description and the code snippet." />

> [pat] **Pattern Connection** — "Reset the start when the running sum dips" mirrors Kadane's max-subarray reset — both discard a prefix that can only hurt.

#### Same pattern, new tweaks

"A running tally you reset the moment a prefix can only hurt" recurs across greedy scans:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Maximum Subarray (Kadane)](https://leetcode.com/problems/maximum-subarray/) | reset the running sum to 0 whenever it goes negative | — |
| [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | track the min price so far and the best profit against it | — |
| [Gas Station](https://leetcode.com/problems/gas-station/) | reset the start to `i+1` when the tank dips below 0, with a global feasibility gate | — |

## Task Scheduler / Activity Selection (Sort-Driven Greedy) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Task Scheduler](https://leetcode.com/problems/task-scheduler/)*

<ProgressCheck id="task-scheduler-activity-selection-sort-driven-greedy" />

### Problem
Given task labels and a cooldown `n` (identical tasks must be at least `n` apart), find the **minimum number of intervals** (including idle slots) to run every task.

**Constraints:** `1 ≤ tasks ≤ 10⁴`; labels `A–Z`; `0 ≤ n ≤ 100`.

**Example 1:** `["A","A","A","B","B","B"], n = 2` → `8` (`AB_AB_AB`).

**Example 2:** `tasks = ["A","A","A","B","B","B"], n = 0` → `6` because no cooldown gaps are needed.

### Solution — brute force
For task scheduling, brute force can simulate each time slot by repeatedly choosing an available task and trying schedules with idle slots when blocked. That search branches heavily and is effectively exponential if you enumerate orders; even a priority-queue simulation is more machinery than needed. The optimized formula observes that the most frequent task creates the idle-frame skeleton, then fills gaps with all other tasks in linear time over the task counts.

```text
try every ordering of the tasks:
    insert idle slots whenever a repeated label is too close
    keep the shortest valid timeline
return the best length
```

Brute force complexity: exponential if schedules are enumerated; simulation alternatives are usually O(T log A).

### Solution — optimized
**Activity selection** — to fit the most non-overlapping intervals, sort by **earliest finish time** and greedily take any activity starting after the last taken finish. Exchange argument: swapping in the earliest-finishing compatible activity never reduces the count.

**Task Scheduler** (cooldown n between equal tasks) — the most frequent task dictates the skeleton: `(maxFreq−1)·(n+1) + (#tasks with maxFreq)`, floored by total tasks.

#### Java
```java
int leastInterval(char[] tasks, int n) {
    int[] freq = new int[26];
    for (char task : tasks) freq[task - 'A']++;
    int maxFreq = 0, maxCount = 0;
    for (int f : freq) {
        if (f > maxFreq) { maxFreq = f; maxCount = 1; }
        else if (f == maxFreq) maxCount++;
    }
    int frame = (maxFreq - 1) * (n + 1) + maxCount;
    return Math.max(tasks.length, frame);
}
```

> [key] **Key Insight** — Greedy interval problems almost always sort by *finish* time (maximize count) or *start* time (merge/coverage). Choosing the wrong key is the classic greedy failure.

> [pat] **Pattern Connection** — Earliest-finish selection underlies *Non-overlapping Intervals* (min removals) and *Minimum Arrows to Burst Balloons* (max non-overlap = min points).

> [note] **Trace it** — tasks `AAABBB, n=2`. The three `A`s frame the timeline `A??A??A`; `B`s and idles fill the gaps → `AB_AB_AB` = **8** intervals.

<CodeTrace
  title="Task Scheduler — tasks=[A,A,A,B,B,B], n=2 cooldown"
  :values="['A','B','_','A','B','_','A','B']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { max_freq: 3, gap: "n+1=3", slots: "3 chunks" }, note: "3 A blocks → framework A??A??A", added: [0,3,6] },
    { pointers: { i: 1 }, vars: { filled: "B in slot 1", idle: 0 }, note: "put B in gap after 1st A", added: [1] },
    { pointers: { i: 2 }, vars: { filled: "B in slot 2", idle: 1 }, note: "B goes after 2nd A, need one idle slot", added: [2,4] },
    { pointers: { i: 3 }, vars: { filled: "B in slot 3", idle: 2 }, note: "B after 3rd A. final length = 8", added: [7] }
  ]'
/>

### Time Complexity
Time O(T + A), where T is the task count and A is the alphabet size. Counting dominates for fixed uppercase labels.

### Space Complexity
Space O(A) for the frequency table.

### Learning notes
- Why count frequencies? — only the most frequent labels determine unavoidable idle frames.
- Why use `maxFreq - 1` blocks? — the last copy of the most frequent task does not need a following cooldown frame.
- Why multiply by `n + 1`? — each internal block holds one anchor task plus n cooldown positions.
- Why add `maxCount`? — all labels tied for maximum frequency occupy the final block.
- Why `Math.max(tasks.length, frame)`? — other tasks can fill idles, but the answer can never be shorter than the task count.
- Why earliest-finish for activity selection? — finishing sooner leaves the most room for future compatible intervals.

## When greedy fails → DP
<p class="secgoal"><b>What & why:</b> the tell-tale signs that a locally optimal choice is <i>not</i> globally safe. Goal — decide fast between a greedy one-pass and a DP, and back the call with a counterexample or an exchange argument.</p>

*Coin Change* with arbitrary denominations breaks greedy (largest-coin-first fails for coins `{1,3,4}`, amount 6: greedy 4+1+1=3 coins vs optimal 3+3=2). *0/1 Knapsack* breaks greedy (value/weight ratio is optimal only for the fractional version). The tell: a locally best choice can foreclose a better global combination.

> [inv] **Invariant test** — Greedy is safe iff you can prove the exchange argument. No proof, construct a small counterexample; if one exists, the problem is DP.


## Non-overlapping Intervals (Interval Scheduling) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)*

<ProgressCheck id="non-overlapping-intervals-interval-scheduling" />

### Problem
Find the **minimum number of intervals to remove** so the remaining ones don't overlap.

**Constraints:** `1 ≤ n ≤ 10⁵`; `start < end`.

**Example 1:** `[[1,2],[2,3],[3,4],[1,3]]` → `1` (remove `[1,3]`).

**Example 2:** `[[1,2],[1,2],[1,2]]` → `2` (keep one interval, remove two).

### Solution — brute force
Brute force tries subsets of intervals, checks which subsets are pairwise non-overlapping, and keeps the largest valid subset; removals are `n - kept`. That is exponential time and O(n) recursion space, so it is a correctness baseline only. The greedy optimization sorts by end time and always keeps the compatible interval that finishes earliest, because that leaves maximum room for all future intervals.

```text
bestKept = 0
for each subset of intervals:
    if every pair in the subset is non-overlapping:
        bestKept = max(bestKept, subset size)
return n - bestKept
```

Brute force complexity: O(2^n · n²) time to enumerate and validate subsets.

### Solution — optimized
Sort by **end**; greedily keep the earliest-finishing interval; count removals of those that overlap the last kept.

> [inv] **Invariant** — Keeping the earliest-ending compatible interval leaves the most room for the rest (exchange argument).

#### Java
```java
int eraseOverlapIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[1], b[1]));   // by end
    int end = Integer.MIN_VALUE, removed = 0;
    for (int[] iv : intervals) {
        if (iv[0] >= end) end = iv[1];   // keep (compatible)
        else removed++;                   // overlaps -> remove this one
    }
    return removed;
}
```

> [note] **Trace it** — `[[1,2],[2,3],[3,4],[1,3]]`. Keeping earliest-finishers `[1,2],[2,3],[3,4]` forces dropping `[1,3]` → **1** removal.

<CodeTrace
  title="Non-overlapping Intervals — sorted by end"
  :values="['[1,2]','[2,3]','[1,3]','[3,4]']"
  :windowKeys="['i']"
  :cellWidth="60"
  :steps='[
    { pointers: { i: 0 }, vars: { end: 2, keep: "yes", removed: 0 }, note: "keep [1,2]" },
    { pointers: { i: 1 }, vars: { end: 3, keep: "yes", removed: 0 }, note: "[2,3] start=2 ≥ end=2 → keep", added: [0,1] },
    { pointers: { i: 2 }, vars: { end: 3, keep: "no", removed: 1 }, note: "[1,3] start=1 lt 3 → drop", removed: [2] },
    { pointers: { i: 3 }, vars: { end: 4, keep: "yes", removed: 1 }, note: "[3,4] start=3 ≥ 3 → keep. total=1", added: [3] }
  ]'
/>

### Time Complexity
Time O(n log n). Sorting by end dominates; the greedy keep/remove pass is O(n).

### Space Complexity
Space O(1) extra besides the input array, ignoring sorting implementation overhead.

### Learning notes
- Why sort by end? — earliest finish leaves maximum room for later intervals.
- Why initialize `end` very small? — the first interval should always be eligible to keep.
- Why `iv[0] >= end`? — touching endpoints are non-overlapping for this problem.
- Why update `end = iv[1]` only when kept? — removed intervals should not constrain future choices.
- Why count `removed++` on overlap? — sorting by end means the current interval is no better than the one already kept.
- Why this greedy is safe? — an exchange argument swaps any later-ending kept interval for the earlier-ending one.

> [note] **Interview script** — "I first confirm touching endpoints like `[1,2]` and `[2,3]` are non-overlapping under the problem definition. I start with brute force by testing subsets of intervals, which is exponential time and O(n) space. I optimize by sorting by end time and greedily keeping compatible intervals, giving O(n log n) time and O(1) extra space."


> [trap] **Common Trap** — Sorting by start, not end. *Example:* `[[1,100],[2,3],[3,4]]`. Sorting by start keeps `[1,100]` first and drops the two short intervals. Sort by **end**: pick `[2,3]`, then `[3,4]` — remove `[1,100]`.

<TrapTrace title="Sorting by start, not end" input="[[1,100],[2,3],[3,4]]" bug="'[[1,100],[2,3],[3,4]]'. Sorting by start keeps '[1,100]' first and drops the two short intervals" fix="Sort by **end**: pick '[2,3]', then '[3,4]' — remove '[1,100]'." />

> [pat] **Pattern Connection** — Max non-overlapping set = *Minimum Arrows to Burst Balloons* (min points to stab all). Sort-by-end greedy is the shared core.

#### Same pattern, new tweaks

Sort by **end time** and greedily keep the earliest-finishing compatible interval:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Minimum Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) | max non-overlapping set = minimum stabbing points | — |
| [Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/) | the same earliest-finish chain, counting length | — |
| [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | removals = total − (max non-overlapping kept) | — |
| [Course Schedule III](https://leetcode.com/problems/course-schedule-iii/) | sort by deadline; greedily take courses, dropping the longest with a max-heap when you overrun | — |

---

## Check your understanding

<Quiz
  pattern-id="greedy"
  :questions='[{"q": "What is the risk of a greedy algorithm?", "choices": [{"text": "Local optimum may not equal global optimum", "correct": true, "explanation": "Must prove correctness — usually via exchange argument."}, {"text": "It is always slow", "correct": false, "explanation": "Greedy is usually fastest."}, {"text": "Uses too much memory", "correct": false}, {"text": "Doesn’t terminate", "correct": false}]}, {"q": "For Jump Game (reachability), what does the greedy track?", "choices": [{"text": "Farthest index reachable so far", "correct": true, "explanation": "If i > farthest, we’re stuck."}, {"text": "Number of jumps used", "correct": false, "explanation": "That is Jump Game II."}, {"text": "Sum of nums", "correct": false}, {"text": "Min-heap of jumps", "correct": false}]}, {"q": "For Course Schedule III, what makes the \"regret\" greedy correct?", "choices": [{"text": "Sort by deadline; swap out longest past-taken course when infeasible", "correct": true, "explanation": "Preserves feasibility while maximizing count."}, {"text": "Sort by duration", "correct": false, "explanation": "Doesn’t enforce deadlines."}, {"text": "Random", "correct": false}, {"text": "DP", "correct": false, "explanation": "Works but slower."}]}, {"q": "For Non-overlapping Intervals (minimum removes), sort by:", "choices": [{"text": "End ascending", "correct": true, "explanation": "Choosing earliest end leaves maximal room — classic activity selection."}, {"text": "Start ascending", "correct": false, "explanation": "That is Merge Intervals."}, {"text": "Length descending", "correct": false}, {"text": "Random", "correct": false}]}, {"q": "For Gas Station (circular route), what allows the O(n) reset trick?", "choices": [{"text": "If tank < 0 at index i, no start in [candidateStart..i] works — reset to i+1", "correct": true, "explanation": "Any start ≤ i would have failed by i too."}, {"text": "Sort by cost", "correct": false}, {"text": "Total sum trick only", "correct": false, "explanation": "Also needed but not the reset itself."}, {"text": "DP", "correct": false}]}]'
/>

<PrintButton />

<RelatedPatterns pattern-id="greedy" />
