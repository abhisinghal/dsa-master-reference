# Greedy


<PatternVideo pattern-name="Greedy" duration="8–12 min" />

<PatternProgress pattern-id="greedy" problems="jump-game-ii, jump-game, gas-station, best-time-to-buy-and-sell-stock, maximum-subarray, non-overlapping-intervals, minimum-number-of-arrows-to-burst-balloons, course-schedule-iii, maximum-length-of-pair-chain, video-stitching, jump-game-iii" />

<script setup>
const theTemplateCode = `// The greedy skeleton: pick a sort key, sweep once, commit each locally-safe choice.
Collections.sort(items, byKey);              // the SORT KEY is the whole thing
Result best = seed();
State state = initialState();
for (Item x : items) {
    if (compatible(x, state)) {              // locally safe?
        state = commit(x, state);            // yes — commit, never look back
        best = update(best, x);
    }
    // otherwise skip (counts as a decision too)
}
return best;

// Correctness: prove the exchange argument.
//   Any optimal OPT differs from greedy at some first choice c.
//   Swap OPT's c for greedy's c without reducing the objective.
//   Repeat; OPT converges to greedy.`

const theTemplateInvariant = {
  statement: `At every step the state represents a "best-feasible prefix of commitments": every element already committed is part of SOME optimal solution, and every element skipped so far cannot be in any solution that includes the committed prefix.`,
  initialization: `Sort by the problem-specific key (earliest finish for activity selection; largest frequency for Huffman; farthest-reach for jump game — the key encodes which local choice is provably safe).`,
  maintenance: `When we commit element x, the exchange argument proves that any optimal solution OPT disagreeing with greedy on x can swap x in without reducing the objective. So "greedy-so-far" extends to "some optimal solution".`,
  termination: `After the sweep, no uncommitted element can improve the objective (would've violated the invariant on an earlier step). The committed set is optimal.`
}

const theTemplateComplexity = {
  time: `O(n log n) when the sort dominates; O(n) when the key is already a prefix-balance or farthest-reach`,
  space: `O(1) besides sorting`
}

const theTemplateSpecializations = [
  { slug: `activity-selection-medium`,     title: `Activity Selection (medium)` },
  { slug: `non-overlapping-intervals-medium`, title: `Non-overlapping Intervals (medium)` },
  { slug: `jump-game-ii-medium`,           title: `Jump Game II (medium)` },
  { slug: `gas-station-medium`,            title: `Gas Station (medium)` },
  { slug: `task-scheduler-medium`,         title: `Task Scheduler (medium)` },
  { slug: `huffman-encoding-medium`,       title: `Huffman Encoding (medium)` },
]

const theTemplateProblemShape = `A locally-safe decision at each step produces a globally optimal result. The sort key (or frequency-max tally) encodes which "best right now" is provably safe via an exchange argument.`

const activitySelectionCode = `// Interval Scheduling Maximization (ISM) — the ur-greedy.
// Given n activities (start, end), pick the max number that don't overlap.
int maxActivities(int[][] activities) {
    Arrays.sort(activities, (a, b) -> Integer.compare(a[1], b[1]));   // SORT BY END
    int count = 0, lastEnd = Integer.MIN_VALUE;
    for (int[] a : activities) {
        if (a[0] >= lastEnd) {           // compatible with the last committed
            count++;
            lastEnd = a[1];
        }
    }
    return count;
}`

const huffmanCode = `// Huffman encoding — the greedy proof archetype.
// Given character frequencies, build a prefix-free binary code minimizing Σ freq[c] * depth[c].
record Node(int freq, Node left, Node right) {}

Node buildHuffman(Map<Character, Integer> freq) {
    PriorityQueue<Node> pq = new PriorityQueue<>(Comparator.comparingInt(n -> n.freq));
    for (var e : freq.entrySet()) {
        pq.offer(new Node(e.getValue(), null, null));
    }
    while (pq.size() > 1) {
        Node a = pq.poll();              // SMALLEST frequency
        Node b = pq.poll();              // SECOND SMALLEST
        pq.offer(new Node(a.freq + b.freq, a, b));   // merge; cost += a.freq + b.freq
    }
    return pq.poll();                     // the root
}

// Correctness proof (sketch): the two LEAST-frequent characters are always leaves at
// MAXIMUM depth in SOME optimal tree. Merging them is a safe commitment —
// Huffman's 1952 exchange argument swaps them in without raising cost.`

const mastery5 = [
  {
    q: `What distinguishes a correct greedy algorithm from a greedy heuristic that happens to work on your test cases?`,
    choices: [
      { text: `A proof — usually an exchange argument — that the local choice can always be swapped into some optimal solution`, correct: true, explanation: `Without a proof, you have "greedy on the test cases I thought of" — not an algorithm.` },
      { text: `Running in O(n log n) time`, correct: false, explanation: `Many greedy heuristics have the right time complexity and the wrong answer.` },
      { text: `Sorting the input first`, correct: false, explanation: `Not all greedy algorithms sort (Gas Station doesn't).` },
      { text: `Being implementable in under 10 lines`, correct: false, explanation: `Code length isn't a correctness criterion.` }
    ]
  },
  {
    q: `Which problem has NO correct greedy solution and must be solved with DP?`,
    choices: [
      { text: `Coin Change with arbitrary denominations (e.g. coins = {1,3,4}, amount = 6)`, correct: true, explanation: `Greedy largest-first takes 4+1+1=3, but optimal is 3+3=2. The greedy-choice property fails.` },
      { text: `Activity Selection`, correct: false, explanation: `Earliest-finish-first is provably optimal.` },
      { text: `Huffman Encoding`, correct: false, explanation: `The merge-two-smallest greedy is provably optimal.` },
      { text: `Kruskal's MST`, correct: false, explanation: `Matroid-greedy, provably optimal.` }
    ]
  },
  {
    q: `For Non-overlapping Intervals (minimum removals), why sort by END time instead of START?`,
    choices: [
      { text: `Finishing earliest leaves the maximum room for future compatible intervals`, correct: true, explanation: `This is the exact exchange argument — swap any kept later-end for an earlier-end and future feasibility can only improve.` },
      { text: `Sorting by start would be O(n²)`, correct: false, explanation: `Both sorts are O(n log n).` },
      { text: `End times are usually smaller numbers`, correct: false, explanation: `Not a correctness consideration.` },
      { text: `It avoids ties`, correct: false, explanation: `Both can tie.` }
    ]
  },
  {
    q: `For Gas Station on a circular route, after you find that start = 3 works locally, what else must you verify?`,
    choices: [
      { text: `Σ gas ≥ Σ cost — total feasibility is a separate global check`, correct: true, explanation: `A local reset can look promising even when the total is infeasible; you'd return a start that fails the loop.` },
      { text: `That gas[3] ≥ cost[3]`, correct: false, explanation: `A single stop's balance isn't enough; depletion can happen mid-route.` },
      { text: `Nothing — if the reset finished, the start is valid`, correct: false, explanation: `False for total-infeasible inputs.` },
      { text: `That the array is sorted`, correct: false }
    ]
  },
  {
    q: `In Jump Game II, when should you increment the jump counter during the sweep?`,
    choices: [
      { text: `Only when i == currentEnd (we exhaust the current BFS layer and must commit a jump)`, correct: true, explanation: `Each "layer" is the set of indices reachable in the same number of jumps.` },
      { text: `At every index`, correct: false, explanation: `Gives n jumps for an input needing 2.` },
      { text: `Only when farthest > currentEnd`, correct: false, explanation: `Doesn't match the layer boundary.` },
      { text: `At the end of the loop (just once)`, correct: false, explanation: `Loses the per-layer accounting.` }
    ]
  }
]
</script>



## Why greedy exists — the story

You're an intern at a scheduling startup. The founder walks up: *"Given a list of meeting requests with start and end times, what's the maximum number of non-overlapping meetings I can pack into one conference room?"*

The obvious approach: try every subset of meetings. Check each for validity (no overlaps). Return the largest valid subset. There are `2ⁿ` subsets — for `n = 30` meetings, that's `10⁹` combinations. Your laptop chokes for a minute, then returns the right answer. It's correct. It's provably optimal. And for `n ≤ 20` it's actually a legit answer that many textbooks use as their reference for scheduling problems.

But at `n = 100` meetings (a large enterprise's daily calendar), brute force is `10³⁰` subsets — **more than the age of the universe** in nanoseconds. And the killer insight is: you don't need to try every subset. You just need to answer *"which meeting should I pick next?"* at each step. If you always pick the meeting that **ends earliest** among all still-available meetings, you provably get the maximum count. **Sort by end time, sweep left to right, greedily pick any meeting that doesn't overlap the last picked.** O(n log n). For 100 meetings, that's ~700 ops — a microsecond. From universe-age to microsecond, by making the *right* local choice.

That's greedy: **grab the best-looking option right now and never look back**. When it works, the code is embarrassingly short (usually just *sort, then sweep once*). The catch is that "best right now" isn't always "best overall," so a greedy algorithm is only correct when two properties hold: the **greedy-choice property** (a locally optimal pick is safe to commit to) and **optimal substructure** (what's left is a smaller version of the same problem). In an interview the code is the easy part; the points come from *proving* it — most often with an **exchange argument**, where you show that any optimal solution can be nudged, one swap at a time, into the greedy one without ever getting worse.

A brute-force solution usually enumerates choices, schedules, subsets, or paths and then picks the best valid one. Can we do better? Only when a local choice can be proved safe. The rest of the chapter is about finding that proof: farthest reach, earliest finish, minimum prefix balance, or a frequency frame.

> [key] **Key Insight** — Before coding greedy, find the sort key that makes the safe choice obvious (earliest finish, largest ratio, nearest deadline). If you can construct a counterexample to "always take the locally best," greedy is wrong → switch to DP.

<GreedyAnim />

## When to use it — local choices with a proof

### Recognize by
- "fewest / smallest / earliest" with a locally safe choice
- sort-then-sweep problems — activity selection, interval scheduling, non-overlapping intervals
- "jump game" family, "gas station" — verify total feasibility, commit to the earliest reset

### When NOT to use it
A locally-best choice can be regretted later — construct a counterexample ("if I take the largest coin first…") and if you find one, switch to [Dynamic Programming](#dynamic-programming). The exchange-argument proof is what separates a safe greedy from a wrong one.

## History — Kruskal 1956, matroid theory 1935

Greedy algorithms as a formal class date to **Joseph Kruskal's 1956 minimum-spanning-tree paper** *"On the shortest spanning subtree of a graph and the traveling salesman problem"* (Proc. AMS 7(1):48-50). Kruskal proved that sorting edges by weight and greedily adding the cheapest cross-component edge produces a globally-optimal MST. The proof used what we now call an **exchange argument** — if the greedy answer differs from any optimal answer, you can swap one edge to reduce the difference without increasing the total weight, contradicting optimality.

The mathematical foundation is even older. **Hassler Whitney's 1935 paper *"On the abstract properties of linear dependence"*** introduced **matroids** — the abstract structure in which greedy always works. A matroid is a set system where "independence" satisfies specific axioms; when your problem is a matroid, the greedy algorithm provably finds the optimal answer. Kruskal's MST and Prim-Jarnik's MST are both matroid-greedy in this sense. Job Sequencing with Deadlines, Activity Selection, and Huffman Coding are also matroid-greedy problems.

**Real-world adoption:**

- **Huffman Coding (1952)** — the greedy compression algorithm inside every ZIP, PNG, JPEG, MP3, and MPEG file. Powered gzip, brotli, and Zstandard.
- **Dijkstra's shortest-path algorithm (1959)** — technically greedy (extract-min from priority queue). Used in every road-routing GPS, every internet routing protocol (OSPF, IS-IS), every network flow analysis.
- **Kruskal's MST** — cell tower placement, Internet backbone design, cluster analysis in bioinformatics, image segmentation.
- **Prim's MST** — the actual algorithm most textbook implementations use.
- **Interval scheduling** (earliest-finish-first) — every meeting-room scheduler, every "book the maximum non-overlapping X" application.
- **Fractional Knapsack** — CPU scheduling in real-time systems, resource allocation in cloud auto-scalers.
- **Set Cover approximation** — every anti-spam filter's rule-selection subsystem.

When you tell an interviewer *"I'll prove correctness with an exchange argument,"* you're citing Kruskal's 1956 proof technique — still the gold standard for greedy-algorithm proofs 70 years later.

## THE template — sort by a safe key, sweep once

<PatternTemplateCard
  slug="greedy"
  title="Greedy"
  language="java"
  :code="theTemplateCode"
  :invariant="theTemplateInvariant"
  :complexity="theTemplateComplexity"
  :specializations="theTemplateSpecializations"
  :problemShape="theTemplateProblemShape"
/>

<InvariantProof
  :statement="theTemplateInvariant.statement"
  :initialization="theTemplateInvariant.initialization"
  :maintenance="theTemplateInvariant.maintenance"
  :termination="theTemplateInvariant.termination"
/>

### The exchange argument — the proof you *must* carry into the interview

For every greedy problem below, the correctness proof is the same shape:
1. Suppose there's an optimal solution OPT that differs from greedy's commitments.
2. Find the earliest step where they differ. OPT has choice `c`, greedy has choice `g`.
3. Show that swapping `c → g` in OPT yields a solution no worse than OPT.
4. Repeat until OPT matches greedy. Contradiction with "OPT is strictly better" means greedy IS optimal.

If you can't construct this swap, **greedy is wrong on this problem — switch to DP**. Classic failure: Coin Change with `{1,3,4}`, amount `6` — largest-coin-first gives `4+1+1=3`, optimal is `3+3=2`.

## When the mechanic breaks — three failure modes

<TrapTrace
  title="Wrong sort key — locally best isn't globally safe"
  bug="Non-overlapping Intervals with input [[1,100],[2,3],[3,4]], sorted by START: first commit is [1,100], which blocks both short intervals → kept = 1, removed = 2. Right answer is kept = 2, removed = 1 (keep [2,3] and [3,4], drop [1,100])."
  fix="For max non-overlapping intervals, sort by END time. The exchange argument: any kept interval with a later end can be swapped for an earlier-end compatible one without reducing count. Start-time sort has no such exchange proof — a locally bad commit forecloses globally better options."
/>

<TrapTrace
  title="Skipping the total-feasibility check in Gas Station"
  bug="For gas=[1,2,3,4], cost=[2,3,4,5], Σ gas = 10 < Σ cost = 14. A local reset finds candidate start = 3 (tank: 4−5 = −1 → bad; shifts to start = 0 → bad), returns 0, which fails the full loop. The local greedy only guarantees 'if any valid start exists, this is it' — not 'a valid start exists'."
  fix="Keep a running total alongside the local tank. After the sweep, return start only if total ≥ 0; otherwise return -1. The two counters cost nothing extra and gate the greedy against infeasible inputs."
/>

<TrapTrace
  title="Counting commitments at every step instead of at the frontier"
  bug="In Jump Game II with nums=[2,3,1,1,4], if you increment jumps at every index you get 5. The intended BFS-layer semantics: jumps is 'minimum hops to reach i', and all indices in one layer share a jump count — you commit a new jump only when i exhausts the current layer's rightmost reach."
  fix="Maintain two frontiers: currentEnd (right edge of the current BFS layer) and farthest (right edge of the layer below). Increment jumps and set currentEnd = farthest ONLY when i == currentEnd. The code is three lines; the mental model is one layer at a time."
/>

## Sub-variations of the template

<PatternSubVariationNav pattern="greedy" />

### Activity Selection <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Non-overlapping Intervals (companion)](https://leetcode.com/problems/non-overlapping-intervals/)*

The bare mechanic. Given `n` activities with start/end times, pick the maximum number of non-overlapping activities. Sort by end time, sweep, keep every compatible one.

#### Why this is the ur-greedy

Activity Selection (also called **Interval Scheduling Maximization**) was the first problem shown to be solvable by a provably-correct greedy — the classical 1972 paper by Horn, and the standard proof in Kleinberg & Tardos. Its exchange argument is template for the entire chapter.

**Exchange proof sketch:** Suppose OPT picks activity `a` at step k. Greedy picks `g` (the earliest-ending compatible). If `a ≠ g`, then `g.end ≤ a.end` (greedy picked the earliest-finishing). Any activity OPT can pick after `a` can also be picked after `g` (its start time ≥ a.end ≥ g.end). So swapping `a → g` keeps OPT optimal. Repeat.

> [key] Pick the maximum number of pairwise non-overlapping activities.

<TemplateReveal
  slug="activity-selection"
  language="java"
  :canonical="activitySelectionCode"
/>

> [inv] **Invariant** — After the sweep, every committed activity is in SOME optimal solution. The sort-by-end order makes each commit locally-safe (earliest finish dominates all later-finish compatibles).

**Trace** — activities `[(1,3), (2,4), (3,5), (0,6), (5,7), (8,9), (5,9)]`. Sorted by end: `(1,3),(2,4),(3,5),(0,6),(5,7),(8,9),(5,9)`. Sweep: keep `(1,3)` → `lastEnd = 3`. Skip `(2,4)` (`2 < 3`). Keep `(3,5)` → `lastEnd = 5`. Skip `(0,6)` and `(5,7)` is compatible (`5 >= 5`) → keep → `lastEnd = 7`. Skip `(5,9)` → `lastEnd = 7`. Keep `(8,9)` → `lastEnd = 9`. Count = **4**.

**Complexity:** O(n log n) sort + O(n) sweep.

**Classic companion problem:** [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) — same mechanic, different objective (`removals = n − maxKept`).

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Sort by END time, not start.** Earliest-finishing-first is the greedy pick that admits an exchange proof; sort-by-start fails on `[(0,10),(1,2),(3,4)]`.
- **The exchange argument is the ur-template for this chapter.** Any later greedy you meet (Jump Game II, Task Scheduler, Huffman) borrows the shape: assume OPT differs at step k, swap greedy's pick in, show it stays ≥ OPT.
- **`lastEnd` is the single state variable** — the sweep is O(n) after the sort. Keep an activity iff `start ≥ lastEnd`.
- **Boundary convention matters**: `start ≥ lastEnd` treats `[1,3]` and `[3,5]` as non-overlapping (common in CS). `start > lastEnd` would reject them. Pick based on the problem statement.
- **"Removals" variant** (LC-435 Non-overlapping Intervals) is the same algorithm with `answer = n − maxKept`. Same code; different return.
- **Siblings: Minimum Number of Arrows to Burst Balloons (same sort-by-end, keep count), Maximum Length of Pair Chain.**

</details>

### Jump Game II <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Jump Game II](https://leetcode.com/problems/jump-game-ii/)*

<ProgressCheck id="jump-game-ii-farthest-reach-greedy" />

```svg
<svg role="img" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Diagram illustrating: Jump Game II (Farthest-Reach Greedy) Medium">
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

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- Why loop only to `a.length - 1`? — you do not need to jump after reaching the last index.
- Why update `farthest` every index? — it records the best next frontier from the current BFS layer.
- Why increment only at `i == curEnd`? — that is where the current jump range is exhausted.
- Why set `curEnd = farthest`? — the next jump can cover exactly the farthest range discovered so far.
- Why not choose a concrete next index? — only the frontier matters for the minimum jump count.
- Why greedy works? — farther reach dominates shorter choices within the same layer.

</details>

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

### Gas Station <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Gas Station](https://leetcode.com/problems/gas-station/)*

<ProgressCheck id="gas-station-prefix-balance-greedy" />

```svg
<svg role="img" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Diagram illustrating: Gas Station (Prefix-Balance Greedy) Medium">
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

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- Why keep `total`? — it proves whether any solution exists globally.
- Why keep `tank` separately? — it measures surplus from the current candidate start only.
- Why reset when `tank < 0`? — every station in that failed segment is impossible.
- Why set `start = i + 1`? — the next station is the first candidate not disproved by the deficit.
- Why reset `tank = 0`? — the new candidate starts with an empty local balance.
- Why return `start` only if `total >= 0`? — local recovery cannot fix global shortage.

</details>

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

### Task Scheduler <span class="diff diff-m">Medium</span>

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

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- Why count frequencies? — only the most frequent labels determine unavoidable idle frames.
- Why use `maxFreq - 1` blocks? — the last copy of the most frequent task does not need a following cooldown frame.
- Why multiply by `n + 1`? — each internal block holds one anchor task plus n cooldown positions.
- Why add `maxCount`? — all labels tied for maximum frequency occupy the final block.
- Why `Math.max(tasks.length, frame)`? — other tasks can fill idles, but the answer can never be shorter than the task count.
- Why earliest-finish for activity selection? — finishing sooner leaves the most room for future compatible intervals.

</details>

### When greedy fails → DP
<p class="secgoal"><b>What & why:</b> the tell-tale signs that a locally optimal choice is <i>not</i> globally safe. Goal — decide fast between a greedy one-pass and a DP, and back the call with a counterexample or an exchange argument.</p>

*Coin Change* with arbitrary denominations breaks greedy (largest-coin-first fails for coins `{1,3,4}`, amount 6: greedy 4+1+1=3 coins vs optimal 3+3=2). *0/1 Knapsack* breaks greedy (value/weight ratio is optimal only for the fractional version). The tell: a locally best choice can foreclose a better global combination.

> [inv] **Invariant test** — Greedy is safe iff you can prove the exchange argument. No proof, construct a small counterexample; if one exists, the problem is DP.


### Non-overlapping Intervals <span class="diff diff-m">Medium</span>

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

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- Why sort by end? — earliest finish leaves maximum room for later intervals.
- Why initialize `end` very small? — the first interval should always be eligible to keep.
- Why `iv[0] >= end`? — touching endpoints are non-overlapping for this problem.
- Why update `end = iv[1]` only when kept? — removed intervals should not constrain future choices.
- Why count `removed++` on overlap? — sorting by end means the current interval is no better than the one already kept.
- Why this greedy is safe? — an exchange argument swaps any later-ending kept interval for the earlier-ending one.

</details>

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

### Huffman Encoding <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Minimum Cost to Connect Sticks (closest LeetCode variant)](https://leetcode.com/problems/minimum-cost-to-connect-sticks/)*

#### Problem
Given character frequencies, build a **prefix-free binary code** minimizing the weighted total bit-length Σ `freq[c] · depth[c]`. This is the compression algorithm powering ZIP, PNG, JPEG, MP3, and brotli.

#### The move — repeatedly merge the two LEAST frequent

The counterintuitive insight: at any point, the two characters currently of least frequency are **always** at maximum depth in some optimal tree. So merging them (making them siblings under a new internal node) is a safe commitment. Repeat until one tree remains.

> [key] Build a prefix-code minimizing Σ freq × depth; always merge the two smallest-frequency subtrees.

<TemplateReveal
  slug="huffman"
  language="java"
  :canonical="huffmanCode"
/>

> [inv] **Invariant** — The priority queue always holds optimal subtrees for the characters/subtrees it contains. Merging the two smallest adds `a.freq + b.freq` to the total cost — which equals the sum of all merge costs = Σ freq × depth over the final tree.

**Why this is the proof archetype.** Huffman (1952) is the first greedy algorithm whose correctness was proved before the algorithm existed. The proof:

1. **Lowest-frequency leaves have maximum depth.** In any optimal tree, if a lowest-freq leaf `a` were at depth `d` and some other leaf `b` with `freq(b) ≥ freq(a)` were at depth `d' > d`, swapping them changes the cost by `(freq(a) - freq(b))(d' - d) ≤ 0` — never worsens.
2. **The two lowest-freq leaves can be siblings.** Both at max depth means they're on the same bottom level; adjacent siblings are a valid rearrangement.
3. **Merging them is safe.** Replace `{a, b}` with a merged node of frequency `freq(a) + freq(b)` — the problem shrinks to one fewer leaf, and the merge cost added equals exactly the extra depth savings from treating them as siblings.
4. **Induct.** The subproblem (one fewer character) has the same shape; greedy continues.

**Complexity:** O(n log n) — each merge is one heap push and two pops.

**In the wild — DEFLATE's canonical Huffman.** gzip, PNG, and ZIP use a *canonical* Huffman code (same code lengths as the greedy tree, but code bits are assigned in a deterministic order) so the decoder only needs the code lengths — not the tree. The algorithmic core is still greedy; the serialization is the extra engineering.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **The greedy move: repeatedly merge the two SMALLEST-frequency subtrees.** Pop twice, push a new internal node with their combined frequency. The total compression cost is the sum of these combined frequencies.
- **Why min-heap is the natural data structure**: you need "give me the two smallest" repeatedly. Each merge is 2 pops + 1 push → O(log n). Total O(n log n).
- **The proof archetype**: (1) lowest-freq leaves are at max depth in some optimal tree, (2) they can be siblings, (3) merging them is safe, (4) induct on the (n−1)-leaf subproblem. This is the Huffman exchange argument.
- **Prefix-free property is automatic** — no character's code is a prefix of another because leaves don't lie on paths to other leaves in a binary tree.
- **Tie-breaking is implementation-defined** but doesn't affect optimality: different tie-break rules produce different trees with the same minimum weighted path length Σ freq × depth.
- **Canonical Huffman** (used by DEFLATE/gzip/PNG) stores only the code LENGTHS, not the tree — the decoder reconstructs codes deterministically from lengths. Same algorithm, better serialization.
- **Siblings: Minimum Cost to Connect Sticks (LC-1167, identical pattern), Merge Stones (DP variant when merges must respect order).**

</details>

## In the wild — Linux CFS task scheduler

The Linux kernel's **Completely Fair Scheduler** (`kernel/sched/fair.c`, since 2.6.23 in 2007) uses a partly-greedy approach to pick the next task to run. Every runnable task has a **virtual runtime** (`vruntime`) — the time it has consumed, weighted by priority. CFS picks the task with the lowest vruntime next:

```c
/* kernel/sched/fair.c (paraphrased, slightly simplified) */
static struct sched_entity *pick_next_entity(struct cfs_rq *cfs_rq) {
    /* The red-black tree holds all runnable tasks, keyed by vruntime.
       The leftmost node is the task with the LEAST vruntime so far.
       Greedy choice: pick the task with the smallest vruntime next. */
    struct sched_entity *left = __pick_first_entity(cfs_rq);

    /* Exception: respect a currently-running task if its vruntime
       is close enough to left's — avoids thrashing on context switches. */
    if (cfs_rq->curr && entity_before(cfs_rq->curr, left))
        return cfs_rq->curr;

    return left;
}
```

**Why this is "partly greedy":** the vruntime-smallest pick is the greedy commitment. The red-black tree gives O(log n) insert/delete, so maintaining the sorted order has amortized cost comparable to a heap. But CFS has edge cases (sleep bonus, group scheduling, nice-value weighting) where strict greedy would thrash — those are the "partly" caveats.

**Correctness intuition:** if every task is picked exactly when its vruntime is smallest, no task runs more than ε ahead of any other, i.e. no task is systematically starved. That's the *fairness* in CFS — a property that falls out of the greedy choice when weighted by nice value.

**Other production greedy algorithms:**
1. **gzip / brotli / Zstandard compression** — Huffman coding (greedy merge of smallest-frequency subtrees).
2. **TCP congestion control (New Reno, Cubic)** — AIMD slow-start is greedy on the window-size parameter; packet-loss triggers exponential backoff.
3. **GPU shader compiler register allocation** — graph-coloring heuristic is a greedy pick-the-highest-saturation-degree algorithm (Chaitin-Briggs).
4. **Google's Chubby / etcd leader election** — once a quorum forms, the greedy node with highest known term wins; ties broken by node ID.

## Recognition drill

<RecognitionDrill pattern="greedy" :count="10" />

## Advanced — follow-ups and failure modes

<details>
<summary><strong>What if the exchange argument fails for some problem?</strong></summary>

Three paths:
- **Switch to DP** — the sub-problem optimality + overlapping sub-problems structure gives correctness where greedy fails.
- **Greedy + proof of approximation ratio** — for NP-hard problems like Set Cover, the natural greedy (pick the set covering the most uncovered elements) gives an `O(log n)` approximation, provably within log n of optimal.
- **Randomized greedy** — e.g. randomized rounding of LP relaxations gives expected approximation guarantees for problems like Max-SAT.

Example: Coin Change with `{1, 3, 4}` and amount 6 — greedy gives 3 coins (4+1+1); DP gives 2 (3+3). No exchange argument exists.
</details>

<details>
<summary><strong>What if the "cost" is multi-dimensional (Pareto frontier)?</strong></summary>

Greedy on one dimension can be arbitrarily bad on another. Options:
- **Lagrangian dualization** — combine dimensions into one weighted sum, binary-search the weight (as in [BS-on-answer](/patterns/bs-on-answer)).
- **Pareto-front sweep** — maintain the set of non-dominated commitments; the Pareto front has size ≤ `product(dim_sizes)` in the worst case.
- **ILP / branch-and-bound** — exact solution, exponential worst case but often fast in practice.
</details>

<details>
<summary><strong>What if the input arrives online (one element at a time) and you can't sort?</strong></summary>

**Online algorithms** replace "sort first" with "maintain the sorted structure incrementally":
- **Online Interval Scheduling** — maintain the committed intervals in a sorted set; on each new interval, binary-search for compatibility and update. Competitive ratio depends on adversary model.
- **Online Huffman (adaptive Huffman)** — rebalance the tree after each character; worst case `O(n log n)` per character, O(n) total extra space. Used in Vitter's algorithm.

The greedy choice is the same; the data structure cost absorbs the lack of sort.
</details>

<details>
<summary><strong>What if the exchange argument requires a non-obvious swap?</strong></summary>

Some greedy algorithms need a **regret** or **lookahead** swap:
- **Course Schedule III** — sort by deadline, greedily take each course; if the schedule overruns, drop the LONGEST course taken so far (regret the greediest earlier commit).
- **Job Sequencing with Deadlines** — sort by profit; greedily place each job at the latest free slot before its deadline.
- **Interval Covering with Minimum Points** — sort by end; place a point at every uncovered end.

The regret swap preserves feasibility while strictly improving the objective — it's an exchange argument with a different swap target.
</details>

<details>
<summary><strong>What if greedy gives the right answer but you can't prove it?</strong></summary>

The honest answer in an interview is to **say so**: *"I believe this greedy works because [intuition], but I haven't fully proved the exchange argument. If the interviewer wants the proof I can walk through it; if they're OK with the intuition I'll proceed."* The failure mode is a wrong-but-plausible greedy that passes test cases and fails on the interviewer's edge case.

**Rules of thumb:** if the "safe choice" involves a priority queue + a frequency table (Task Scheduler, Huffman), the exchange argument is usually clean. If it involves hand-picked ordering heuristics ("sort by this weird key"), suspect DP.
</details>

### Breaking point

Greedy **stops being correct** when:
- The greedy-choice property fails — a locally optimal commit forecloses a globally better combination.
- The problem has overlapping sub-problems with sub-structure that greedy can't commit to irrevocably — hallmark of DP.
- The objective is multi-dimensional and the dimensions trade off.
- The input is adversarial online — competitive ratio drops below the offline optimum.

### Three cross-pattern problems

- [Coin Change (322)](https://leetcode.com/problems/coin-change/) — the canonical "looks greedy, actually DP" trap problem.
- [Minimum Cost to Hire K Workers (857)](https://leetcode.com/problems/minimum-cost-to-hire-k-workers/) — sorts + priority queue, but the sorting key is the *quality ratio* — bridges greedy with ratio-based proofs.
- [Patching Array (330)](https://leetcode.com/problems/patching-array/) — a non-obvious greedy where you double the reach each time; the exchange argument is subtle.

---

## Check your understanding

<Quiz pattern-id="greedy" :questions="mastery5" />

<PrintButton />

<RelatedPatterns pattern-id="greedy" />
