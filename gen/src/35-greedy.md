# Greedy

Greedy is the "grab the best-looking option right now and never look back" strategy. When it works it's beautiful — usually just *sort, then sweep once*. The catch is that "best right now" isn't always "best overall," so a greedy algorithm is only correct when two properties hold: the **greedy-choice property** (a locally optimal pick is safe to commit to) and **optimal substructure** (what's left is a smaller version of the same problem). In an interview the code is the easy part; the points come from *proving* it — most often with an **exchange argument**, where you show that any optimal solution can be nudged, one swap at a time, into the greedy one without ever getting worse.

> [key] **Key Insight** — Before coding greedy, find the sort key that makes the safe choice obvious (earliest finish, largest ratio, nearest deadline). If you can construct a counterexample to "always take the locally best," greedy is wrong → switch to DP.

### Recognize by
- "fewest / smallest / earliest" with a locally safe choice
- sort-then-sweep problems — activity selection, interval scheduling, non-overlapping intervals
- "jump game" family, "gas station" — verify total feasibility, commit to the earliest reset

### When NOT to use it
A locally-best choice can be regretted later — construct a counterexample ("if I take the largest coin first…") and if you find one, switch to [Dynamic Programming](#dynamic-programming). The exchange-argument proof is what separates a safe greedy from a wrong one.

---

## Jump Game II (Farthest-Reach Greedy)
*[↗ LeetCode: Jump Game II](https://leetcode.com/problems/jump-game-ii/)*

### Problem
Each `nums[i]` is the **max jump length** from index `i`. Find the **fewest jumps** to reach the last index (reaching the end is always possible).

**Constraints:** `1 ≤ n ≤ 10⁴`; `0 ≤ nums[i] ≤ 1000`.

**Example:** `[2,3,1,1,4]` → `2` (jump `0→1→4`).

### Brute force
Brute force models each index as a node and explores every reachable next index to find the shortest path to the end. A plain recursive search can be exponential because it branches over all jump lengths; BFS is O(n²) in the worst case if every index reaches many later indices. The optimized greedy scan compresses BFS levels into two integers: the current frontier and the farthest next frontier.

### Pattern
BFS-like level expansion: from the current reachable range, jump to the farthest reachable next.

> [inv] **Invariant** — `curEnd` is the boundary of positions reachable in `jumps` steps; `farthest` is the boundary reachable in `jumps+1`. When `i` hits `curEnd`, one more jump is forced.

### Java
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

Time O(n) · Space O(1).

> [note] **Interview script** — "I first confirm the end is reachable and I need the minimum number of jumps. I start with brute force DFS or BFS over all jumps, which can be exponential for DFS or O(n²) for naive BFS. I optimize by tracking the current level boundary and farthest next reach in one pass, giving O(n) time and O(1) space."


> [key] **Key Insight** — Each "level" is the set of indices reachable with the same number of jumps; taking the farthest reach is provably optimal because it dominates every other choice's future reach.

> [trap] **Common Trap** — Counting jumps at every step instead of at the frontier. *Example:* `nums=[2,3,1,1,4]`. Incrementing `jumps` at each index gives 5; incrementing only when `i == currentEnd` (frontier boundary) gives 2. Update `currentEnd = farthest` and `jumps++` together.

> [pat] **Pattern Connection** — This is BFS on an implicit graph collapsed to O(n). *Jump Game I* (reachability) is an even simpler farthest-reach scan.

### Same pattern, new tweaks

"Track the farthest you can reach from the current level" is a greedy BFS in disguise:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Jump Game I](https://leetcode.com/problems/jump-game/) | just track the farthest reachable index; return whether it reaches the end | — |
| [Jump Game III](https://leetcode.com/problems/jump-game-iii/) | actual BFS/DFS since you can jump both directions by `arr[i]` | — |
| [Video Stitching / Minimum Number of Taps](https://leetcode.com/problems/video-stitching/) | the same "cover the line in fewest intervals" farthest-reach greedy | — |
| [Minimum Number of Arrows](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) | the interval-cover cousin (sort by end) | — |

## Gas Station (Prefix-Balance Greedy)
*[↗ LeetCode: Gas Station](https://leetcode.com/problems/gas-station/)*

### Problem
Around a circular route, station `i` provides `gas[i]` and it costs `cost[i]` to drive to the next station. Return the **starting index** from which you can complete the whole loop (or -1). A unique answer exists whenever total gas ≥ total cost.

**Constraints:** `1 ≤ n ≤ 10⁵`; values `≥ 0`.

**Example:** `gas = [1,2,3,4,5], cost = [3,4,5,1,2]` → `3`.

### Brute force
Brute force tries every station as a start and simulates a full circuit while tracking tank balance. That is O(n²) time and O(1) space, and it repeats the same failing prefixes over and over. The optimized greedy scan uses the fact that if a candidate start fails at station `i`, every start inside that failed segment also fails, so the next candidate is `i + 1` after a global total check.

### Pattern
If total gas ≥ total cost, a unique start exists; it's just after the point of minimum running balance.

> [key] **Key Insight** — If you run out of gas going from `start` to `i`, no station in `[start, i]` can be the answer (each had ≤ 0 surplus to offer) → restart at `i+1`. Total feasibility is a separate global check.

> [inv] **Invariant** — `tank` is the surplus since the current candidate start; the moment it goes negative, every earlier candidate is eliminated.

### Java
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

Time O(n) · Space O(1).

> [note] **Interview script** — "I first confirm the route is circular and returning any valid start is enough when total gas can cover total cost. I start with brute force by simulating the full loop from every station, which is O(n²) time and O(1) space. I optimize by resetting the candidate after any negative tank and checking total surplus, giving O(n) time and O(1) space."


> [trap] **Common Trap** — Skipping the total check. *Example:* `gas=[1,2,3,4]`, `cost=[2,3,4,5]`. Total gas 10 < total cost 14, so **no** station works — but a local reset can look promising. Verify `sum(gas) >= sum(cost)`; if not, return `-1`.

> [pat] **Pattern Connection** — "Reset the start when the running sum dips" mirrors Kadane's max-subarray reset — both discard a prefix that can only hurt.

### Same pattern, new tweaks

"A running tally you reset the moment a prefix can only hurt" recurs across greedy scans:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Maximum Subarray (Kadane)](https://leetcode.com/problems/maximum-subarray/) | reset the running sum to 0 whenever it goes negative | — |
| [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | track the min price so far and the best profit against it | — |
| [Gas Station](https://leetcode.com/problems/gas-station/) | reset the start to `i+1` when the tank dips below 0, with a global feasibility gate | — |

## Task Scheduler / Activity Selection (Sort-Driven Greedy)
*[↗ LeetCode: Task Scheduler](https://leetcode.com/problems/task-scheduler/)*

### Problem
Given task labels and a cooldown `n` (identical tasks must be at least `n` apart), find the **minimum number of intervals** (including idle slots) to run every task.

**Constraints:** `1 ≤ tasks ≤ 10⁴`; labels `A–Z`; `0 ≤ n ≤ 100`.

**Example:** `["A","A","A","B","B","B"], n = 2` → `8` (`AB_AB_AB`).

### Brute force
For task scheduling, brute force can simulate each time slot by repeatedly choosing an available task and trying schedules with idle slots when blocked. That search branches heavily and is effectively exponential if you enumerate orders; even a priority-queue simulation is more machinery than needed. The optimized formula observes that the most frequent task creates the idle-frame skeleton, then fills gaps with all other tasks in linear time over the task counts.

**Activity selection** — to fit the most non-overlapping intervals, sort by **earliest finish time** and greedily take any activity starting after the last taken finish. Exchange argument: swapping in the earliest-finishing compatible activity never reduces the count.

**Task Scheduler** (cooldown n between equal tasks) — the most frequent task dictates the skeleton: `(maxFreq−1)·(n+1) + (#tasks with maxFreq)`, floored by total tasks.

> [key] **Key Insight** — Greedy interval problems almost always sort by *finish* time (maximize count) or *start* time (merge/coverage). Choosing the wrong key is the classic greedy failure.

> [pat] **Pattern Connection** — Earliest-finish selection underlies *Non-overlapping Intervals* (min removals) and *Minimum Arrows to Burst Balloons* (max non-overlap = min points).

> [note] **Trace it** — tasks `AAABBB, n=2`. The three `A`s frame the timeline `A??A??A`; `B`s and idles fill the gaps → `AB_AB_AB` = **8** intervals.

> [note] **Interview script** — "I first confirm identical tasks need at least `n` intervals between runs and idle slots are allowed. I start with brute force by enumerating or simulating possible schedules, which is exponential if I search all valid orders. I optimize by counting frequencies and using the max-frequency frame formula, giving O(tasks + A) time and O(A) space for alphabet size `A`."


## When greedy fails → DP
<p class="secgoal"><b>What & why:</b> the tell-tale signs that a locally optimal choice is <i>not</i> globally safe. Goal — decide fast between a greedy one-pass and a DP, and back the call with a counterexample or an exchange argument.</p>

*Coin Change* with arbitrary denominations breaks greedy (largest-coin-first fails for coins `{1,3,4}`, amount 6: greedy 4+1+1=3 coins vs optimal 3+3=2). *0/1 Knapsack* breaks greedy (value/weight ratio is optimal only for the fractional version). The tell: a locally best choice can foreclose a better global combination.

> [inv] **Invariant test** — Greedy is safe iff you can prove the exchange argument. No proof, construct a small counterexample; if one exists, the problem is DP.


## Non-overlapping Intervals (Interval Scheduling)
*[↗ LeetCode: Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)*

### Problem
Find the **minimum number of intervals to remove** so the remaining ones don't overlap.

**Constraints:** `1 ≤ n ≤ 10⁵`; `start < end`.

**Example:** `[[1,2],[2,3],[3,4],[1,3]]` → `1` (remove `[1,3]`).

### Brute force
Brute force tries subsets of intervals, checks which subsets are pairwise non-overlapping, and keeps the largest valid subset; removals are `n - kept`. That is exponential time and O(n) recursion space, so it is a correctness baseline only. The greedy optimization sorts by end time and always keeps the compatible interval that finishes earliest, because that leaves maximum room for all future intervals.

### Pattern
Sort by **end**; greedily keep the earliest-finishing interval; count removals of those that overlap the last kept.

> [inv] **Invariant** — Keeping the earliest-ending compatible interval leaves the most room for the rest (exchange argument).

### Java
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

Time O(n log n) · Space O(1).

> [note] **Interview script** — "I first confirm touching endpoints like `[1,2]` and `[2,3]` are non-overlapping under the problem definition. I start with brute force by testing subsets of intervals, which is exponential time and O(n) space. I optimize by sorting by end time and greedily keeping compatible intervals, giving O(n log n) time and O(1) extra space."


> [trap] **Common Trap** — Sorting by start, not end. *Example:* `[[1,100],[2,3],[3,4]]`. Sorting by start keeps `[1,100]` first and drops the two short intervals. Sort by **end**: pick `[2,3]`, then `[3,4]` — remove `[1,100]`.

> [pat] **Pattern Connection** — Max non-overlapping set = *Minimum Arrows to Burst Balloons* (min points to stab all). Sort-by-end greedy is the shared core.

### Same pattern, new tweaks

Sort by **end time** and greedily keep the earliest-finishing compatible interval:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Minimum Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) | max non-overlapping set = minimum stabbing points | — |
| [Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/) | the same earliest-finish chain, counting length | — |
| [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | removals = total − (max non-overlapping kept) | — |
| [Course Schedule III](https://leetcode.com/problems/course-schedule-iii/) | sort by deadline; greedily take courses, dropping the longest with a max-heap when you overrun | — |
