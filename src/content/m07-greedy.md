## Concepts & Mental Models

Greedy algorithms make an irrevocable local choice, then rely on structure to prove that this choice can live inside some global optimum. Two properties matter:

!!! key "Greedy correctness checklist"
    **Greedy-choice property:** there exists an optimal solution whose first decision is the locally best decision. **Optimal substructure:** after fixing that decision, the remaining suffix/subproblem is the same kind of problem. Without both, the algorithm is usually just a heuristic.

The standard proof tool is the **exchange argument**: take an arbitrary optimal solution, show that if it does not use the greedy choice, you can swap in the greedy choice without making the solution worse, and preserve feasibility. Repeating the exchange transforms some optimum into the greedy solution.

Greedy fails when a choice has hidden downstream coupling that cannot be summarized by a small invariant. If the best local decision may need to be sacrificed for future compatibility, reach, capacity, or value, the problem usually needs DP: keep multiple states instead of committing to one path. A senior-level interview signal is not merely knowing greedy recipes, but being able to say what state you are proving unnecessary.

---

## Activity Selection / Non-overlapping Intervals (Earliest Finish Time)

!!! pattern "Pattern: Interval Greedy · T: O(n log n) · S: O(1) excluding sort"
    **Signals:** choose maximum number of mutually compatible intervals; interval endpoints matter more than weights; all accepted intervals have equal value.

### 1. Problem

Given intervals `[start, end)`, select the maximum number of non-overlapping intervals. Equivalently, remove the fewest intervals so the rest do not overlap. The canonical greedy rule is: **sort by earliest finish time, then take every interval whose start is at least the finish time of the last selected interval**.

For closed intervals, replace `start >= lastEnd` with the convention required by the problem. Most interview variants use half-open scheduling semantics, while LeetCode's non-overlapping intervals treats `end <= nextStart` as compatible.

### 2. Intuition

The interval that ends first leaves the largest remaining timeline for every future choice. Choosing a later-ending interval cannot create new opportunities before its end; it can only block candidates. This is not because the earliest-ending interval is always in every optimum, but because some optimum can be exchanged to include it.

### 3. Naive

Try all subsets, reject overlapping subsets, and keep the largest. That is O(2^n · n log n) if each subset is checked by sorting or scanning. A DP over sorted intervals also works, but for the unweighted version it carries unnecessary state: every selected interval contributes exactly 1, so finish time dominates all other details.

### 4. Key Observation

!!! key "Key observation"
    Among all intervals available at a decision point, choosing the one with the smallest end time is safe: any optimal solution that starts with a different compatible interval can exchange its first interval for the earlier-finishing one without reducing the number of intervals.

### 5. Pattern Recognition

**Signals.** Max count of non-overlapping intervals, every interval has equal profit, or minimum removals where `answer = n - maxSelected`.

**Shortcut.** If the objective is count and compatibility depends only on the previous end, sort by `end`. If the objective is weighted profit, this greedy rule fails and the problem becomes weighted interval scheduling DP.

**Related.** Meeting scheduling, erase overlap intervals, interval packing on one resource, activity selection in CLRS.

### 6. Invariant

After scanning intervals sorted by end time, `lastEnd` is the minimum possible finish time among all feasible schedules of size `selected` using intervals seen so far. Therefore the greedy prefix is at least as extendable as any other prefix of the same size.

### 7. Visual Explanation

```diagram
{"type":"intervals","min":0,"max":11,"intervals":[{"start":1,"end":4,"label":"A reject","role":"red"},{"start":2,"end":3,"label":"B take","role":"green"},{"start":3,"end":5,"label":"C take","role":"green"},{"start":0,"end":6,"label":"D reject","role":"red"},{"start":5,"end":7,"label":"E take","role":"green"},{"start":6,"end":9,"label":"F reject","role":"red"},{"start":8,"end":10,"label":"G take","role":"green"}]}
```

```diagram
{"type":"intervals","min":0,"max":11,"intervals":[{"start":1,"end":4,"label":"opt first X","role":"amber"},{"start":2,"end":3,"label":"greedy G","role":"green"},{"start":4,"end":7,"label":"future","role":"primary"},{"start":7,"end":10,"label":"future","role":"primary"}]}
```

The second picture is the exchange: replacing `X` by `G` cannot hurt because `G.end <= X.end`, so every interval that started after `X.end` still starts after `G.end`.

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":460,"box":270,"title":"Earliest-finish interval selection","steps":[{"type":"start","text":"sort intervals by end ascending"},{"type":"process","text":"lastEnd = -∞\nselected = 0"},{"type":"decision","text":"next interval exists?","yes":"yes","branch":{"label":"no","text":"return selected","role":"green"}},{"type":"decision","text":"interval.start >= lastEnd?","yes":"take","branch":{"label":"overlap","text":"reject interval","role":"red"}},{"type":"process","text":"selected++\nlastEnd = interval.end"},{"type":"process","text":"advance scan"}]}
```

### 9. Walkthrough

For intervals `[1,4], [2,3], [3,5], [0,6], [5,7], [6,9], [8,10]`, sort by end:

| sorted interval | compatible with `lastEnd`? | action | `lastEnd` | selected |
|---|---:|---|---:|---:|
| `[2,3]` | yes | take | 3 | 1 |
| `[1,4]` | no | reject | 3 | 1 |
| `[3,5]` | yes | take | 5 | 2 |
| `[0,6]` | no | reject | 5 | 2 |
| `[5,7]` | yes | take | 7 | 3 |
| `[6,9]` | no | reject | 7 | 3 |
| `[8,10]` | yes | take | 10 | 4 |

### 10. Why It Works

Let `g` be the interval with earliest finish time among all intervals currently compatible with the already chosen prefix. Consider any optimal completion `O` for this subproblem. If `O` already starts with `g`, we are done. Otherwise, let its first interval be `o`. Since `g.end <= o.end`, replacing `o` with `g` keeps feasibility: every later interval in `O` starts at or after `o.end`, hence also at or after `g.end`. The number of intervals is unchanged, so the exchanged solution is still optimal and now begins with the greedy choice.

Apply this exchange after every selected interval. The chosen prefix can always be extended to an optimum for the remaining suffix, and the suffix is the same interval-selection problem restricted to intervals starting after `lastEnd`. By induction, the greedy algorithm returns an optimal maximum-cardinality schedule.

### 11. Java

```java
import java.util.Arrays;
import java.util.Comparator;

class Solution {
    int maxNonOverlapping(int[][] intervals) {
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[1]));
        int selected = 0;
        int lastEnd = Integer.MIN_VALUE;

        for (int[] interval : intervals) {
            if (interval[0] >= lastEnd) {
                selected++;
                lastEnd = interval[1];
            }
        }
        return selected;
    }

    int eraseOverlapIntervals(int[][] intervals) {
        return intervals.length - maxNonOverlapping(intervals);
    }
}
```

### 12. Code Walkthrough

`Comparator.comparingInt(a -> a[1])` avoids subtraction overflow. Once sorted by finish time, the loop maintains the invariant directly: reject overlaps, and when an interval is compatible, accepting it gives the smallest possible new `lastEnd` for schedules of that size.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n log n) for sorting plus O(n) scan. **S:** O(1) auxiliary if the sort is in-place by the runtime contract; otherwise O(log n) stack/implementation overhead. The comparison count dominates.

### 14. Edge Cases

- Empty input returns 0.
- Touching intervals such as `[1,3]` and `[3,5]` are compatible under half-open semantics.
- Negative times work because only ordering matters.
- Duplicate end times can be in any order; choosing either gives the same finish boundary.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Sorting by start time picks long early intervals that block many short intervals. Sorting by duration is also wrong: a short interval in the middle can block two compatible intervals around it. The proof depends specifically on earliest finish time.

### 16. Optimization

If intervals are already sorted by end time, the algorithm is O(n). For immutable APIs, copy only if callers require input order preservation; otherwise sorting in place is the cleanest interview implementation.

### 17. Alternatives

- DP over previous compatible interval is correct but unnecessary for unweighted counts.
- Weighted interval scheduling requires DP + binary search because exchanging by earliest finish can lose high value.
- Sweep-line counts overlaps but does not directly construct the maximum compatible subset.

### 18. Interview Follow-Ups

- Return the selected intervals, not just the count.
- Min removals: return `n - selected`.
- Closed intervals: clarify whether equal endpoints overlap.
- Weighted intervals: explain why greedy fails and present DP recurrence.

### 19. Variations

Minimum meeting rooms asks for maximum simultaneous overlap, not maximum compatible subset. Minimum arrows for balloons uses a closely related end-point greedy: sort by end and shoot at the current end, covering every interval whose start is before that point.

### 20. Pattern Connection

This is the cleanest exchange-argument greedy. It teaches the difference between **choosing the earliest start** (a tempting but wrong chronological scan) and **choosing the earliest finish** (the state-minimizing action). The same exchange shape appears in arrows, some deadline scheduling problems, and canonical matroid-like greedy proofs.

---

## Jump Game II (Fewest Jumps, BFS-Layers Greedy)

!!! pattern "Pattern: Greedy frontier / implicit BFS · T: O(n) · S: O(1)"
    **Signals:** array value gives maximum forward reach; need minimum number of jumps; all jumps have unit cost; explicit BFS would visit ranges of indices.

### 1. Problem

Given `nums`, where `nums[i]` is the maximum jump length from index `i`, return the minimum number of jumps needed to reach the last index. Assume the last index is reachable unless the variant says otherwise.

### 2. Intuition

Think of indices as nodes in an unweighted directed graph: from `i`, edges go to `i+1 ... i+nums[i]`. Minimum jumps is shortest path length, so BFS is natural. But BFS layers are contiguous ranges in this graph. Instead of enqueueing every edge, maintain the current layer boundary `currentEnd` and the farthest index reachable by one more jump from any index in the layer.

### 3. Naive

Build BFS explicitly. From each index, push every reachable next index not yet seen. In the worst case this scans O(n^2) edges because `nums[i]` can be O(n) for many `i`. DP with `dp[i] = min jumps to i` is also O(n^2) unless optimized back into the same frontier idea.

### 4. Key Observation

!!! key "Key observation"
    All indices reachable with the same number of jumps form a contiguous layer. While scanning that layer, the only information needed for the next layer is the maximum `i + nums[i]` seen so far.

### 5. Pattern Recognition

**Signals.** Minimum number of moves, every move has equal cost, and each position reaches an interval of future positions.

**Shortcut.** If the graph's BFS frontier is a contiguous interval, replace the queue with `[layerStart, currentEnd]` and accumulate the next layer's right boundary.

**Related.** Jump Game I reachability, minimum taps to water a garden, video stitching, interval cover.

### 6. Invariant

At the start of processing an index `i`, `jumps` is the number of jumps needed to reach every index up to `currentEnd`, and `farthest` is the maximum index reachable using `jumps + 1` jumps from any processed index in the current layer.

### 7. Visual Explanation

```diagram
{"type":"array","values":[2,3,1,1,4],"index":1,"highlights":{"0":"green","1":"amber","2":"amber","4":"muted"},"pointers":[{"name":"currentEnd","index":2,"color":"primary","side":"bottom"},{"name":"farthest","index":4,"color":"green","side":"top"}],"brackets":[{"from":0,"to":0,"label":"0 jumps","color":"green","row":0},{"from":1,"to":2,"label":"1 jump layer","color":"amber","row":1},{"from":3,"to":4,"label":"next layer","color":"primary","row":2}],"caption":"Scanning indices 1..2 computes the boundary reachable with 2 jumps."}
```

```diagram
{"type":"bars","values":[2,4,4],"highlights":{"0":"green","1":"amber","2":"primary"}}
```

The bars show `farthest` after scanning indices `0, 1, 2`: it only moves right, and a jump is counted exactly when the scan crosses the current layer boundary.

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":470,"box":285,"title":"Compress BFS layers into two boundaries","steps":[{"type":"start","text":"jumps = 0\ncurrentEnd = 0\nfarthest = 0"},{"type":"decision","text":"i < n - 1?","yes":"scan","branch":{"label":"no","text":"return jumps","role":"green"}},{"type":"process","text":"farthest = max(farthest, i + nums[i])"},{"type":"decision","text":"i == currentEnd?","yes":"finish layer","branch":{"label":"no","text":"continue scanning layer","role":"primary"}},{"type":"process","text":"jumps++\ncurrentEnd = farthest"},{"type":"decision","text":"currentEnd >= n - 1?","yes":"return jumps","branch":{"label":"no","text":"advance i","role":"primary"}}]}
```

### 9. Walkthrough

For `nums = [2,3,1,1,4]`:

| i | nums[i] | farthest after update | boundary event | jumps | currentEnd |
|---:|---:|---:|---|---:|---:|
| 0 | 2 | 2 | end of layer 0 | 1 | 2 |
| 1 | 3 | 4 | inside layer | 1 | 2 |
| 2 | 1 | 4 | end of layer 1 | 2 | 4 |

The scan stops before the last index; once `currentEnd` reaches `n - 1`, two jumps are sufficient.

### 10. Why It Works

The implicit graph is unweighted, so BFS gives shortest paths. From any contiguous layer `[L, R]`, the union of outgoing edges is another contiguous prefix ending at `max(i + nums[i])` for `i in [L, R]`. Therefore the entire BFS queue for the next depth can be summarized by one integer, `farthest`.

When `i == currentEnd`, every node reachable in `jumps` moves has been processed. No algorithm can reach beyond `farthest` in `jumps + 1` moves, because `farthest` is the maximum outgoing reach over the whole layer. Conversely, every index up to `farthest` is reachable in `jumps + 1` moves by taking the jump from the layer index that provides enough reach. Thus incrementing `jumps` at the boundary exactly advances one BFS level, preserving shortest-path optimality.

### 11. Java

```java
class Solution {
    int jump(int[] nums) {
        if (nums.length <= 1) return 0;

        int jumps = 0;
        int currentEnd = 0;
        int farthest = 0;

        for (int i = 0; i < nums.length - 1; i++) {
            farthest = Math.max(farthest, i + nums[i]);
            if (i == currentEnd) {
                jumps++;
                currentEnd = farthest;
                if (currentEnd >= nums.length - 1) break;
            }
        }
        return jumps;
    }
}
```

### 12. Code Walkthrough

The loop excludes the last index because you never need to jump from the destination. `farthest` gathers the next BFS layer while scanning the current one. Hitting `currentEnd` means the current layer is exhausted, so one more jump is mandatory and sufficient.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n) — each index before the destination is scanned once. **S:** O(1) — the BFS queue is compressed into two boundaries.

### 14. Edge Cases

- Length 0 or 1: zero jumps under normal method contracts; most platforms give length at least 1.
- A zero inside the current layer is harmless if another index extends `farthest`.
- If reachability is not guaranteed, detect `i == currentEnd && farthest == currentEnd` as stuck.
- Large `nums[i]` is safe for typical constraints; use `long` if `i + nums[i]` can exceed `Integer.MAX_VALUE`.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Incrementing `jumps` whenever `farthest` improves counts candidates, not BFS layers. Updating `currentEnd` before finishing the layer can also overcount or undercount because it mixes depths.

### 16. Optimization

The O(n) scan is optimal. The only practical optimization is early exit once `currentEnd >= n - 1` after a layer transition.

### 17. Alternatives

- Explicit BFS is conceptually simple but can be O(n^2).
- DP is useful when jump costs vary; with unit costs and interval reach, it collapses to greedy frontier scanning.
- Jump Game I only asks reachability; it needs `maxReach`, not layer counting.

### 18. Interview Follow-Ups

- Return `-1` if unreachable.
- Recover one minimum-jump path by remembering which index produced each next boundary.
- Support weighted jumps: then shortest path may need Dijkstra or DP.
- Minimize something other than jump count: greedy frontier may no longer be valid.

### 19. Variations

Minimum taps to water a garden and video stitching convert intervals into the same greedy cover: while the current coverage is not enough, pick among all intervals starting before coverage the one extending farthest.

### 20. Pattern Connection

Jump Game II is greedy because BFS state has a one-dimensional monotone frontier. The moment choices have different costs, penalties, or non-contiguous reach, the frontier summary breaks and DP/shortest-path state becomes necessary.

---

## Gas Station

!!! pattern "Pattern: Running sum reset / circular greedy · T: O(n) · S: O(1)"
    **Signals:** circular route; each station contributes `gas[i] - cost[i]`; need a feasible start; total feasibility plus local deficit reset.

### 1. Problem

Given arrays `gas` and `cost`, station `i` gives `gas[i]` fuel and traveling from `i` to `(i + 1) mod n` costs `cost[i]`. Return an index from which a full circuit is possible, or `-1` if no such index exists.

### 2. Intuition

Convert each station to a net gain `diff[i] = gas[i] - cost[i]`. If the total sum is negative, no start can create fuel. If the total is nonnegative, the only question is where to start so the running tank never dips below zero. Whenever a candidate start fails at index `i`, every station between that start and `i` also fails as a start, so skip them all.

### 3. Naive

Try every start and simulate the circle: O(n^2) in the worst case. Prefix sums can reduce some repeated arithmetic, but the key is stronger: a failed segment eliminates all starts inside it.

### 4. Key Observation

!!! key "Key observation"
    If starting at `s` first makes the tank negative at `i`, then no station `k` in `[s, i]` can be a valid start. The partial sum from `k` to `i` is no larger than the failed suffix after discarding a nonnegative prefix, so it also goes negative.

### 5. Pattern Recognition

**Signals.** Circular feasibility with additive gains/losses, one pass, and a guarantee/ask about total sum.

**Shortcut.** Track total sum for existence and a local tank for the current candidate. Reset the candidate after any negative tank.

**Related.** Minimum prefix-sum rotation, circular array balancing, Kadane-style resets.

### 6. Invariant

Before processing station `i`, `start` is the first station after the last eliminated failed block. `tank` is the sum of `diff[start..i-1]` and is nonnegative. All indices before `start` have been proven invalid as starts.

### 7. Visual Explanation

```diagram
{"type":"array","values":[-2,-2,-2,3,3],"index":3,"highlights":{"0":"red","1":"red","2":"red","3":"green","4":"green"},"pointers":[{"name":"start","index":3,"color":"green","side":"bottom"}],"caption":"Negative blocks eliminate their stations; after station 2 the candidate resets to 3."}
```

```diagram
{"type":"bars","values":[-2,-4,-6,-3,0],"highlights":{"2":"red","4":"green"}}
```

The bars show prefix sums of `diff`. A valid start can be placed after a minimum prefix sum, because every subsequent circular prefix is lifted above that minimum.

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":470,"box":285,"title":"Gas station one-pass reset","steps":[{"type":"start","text":"start = 0\ntank = 0\ntotal = 0"},{"type":"decision","text":"next station exists?","yes":"yes","branch":{"label":"no","text":"check total","role":"primary"}},{"type":"process","text":"diff = gas[i] - cost[i]\ntank += diff\ntotal += diff"},{"type":"decision","text":"tank < 0?","yes":"reset","branch":{"label":"no","text":"advance i","role":"green"}},{"type":"process","text":"start = i + 1\ntank = 0"},{"type":"decision","text":"total >= 0?","yes":"return start","branch":{"label":"no","text":"return -1","role":"red"}}]}
```

### 9. Walkthrough

`gas = [1,2,3,4,5]`, `cost = [3,4,5,1,2]`, so `diff = [-2,-2,-2,3,3]`.

| i | diff | tank | total | action | start |
|---:|---:|---:|---:|---|---:|
| 0 | -2 | -2 | -2 | reset | 1 |
| 1 | -2 | -2 | -4 | reset | 2 |
| 2 | -2 | -2 | -6 | reset | 3 |
| 3 | 3 | 3 | -3 | keep | 3 |
| 4 | 3 | 6 | 0 | keep | 3 |

Total is zero, so a solution exists; the candidate `3` completes the circle.

### 10. Why It Works

First, if `sum(diff) < 0`, every full circuit loses fuel overall, so no start can succeed.

Now assume `sum(diff) >= 0`. During the scan, suppose candidate `s` first fails at station `i`, meaning `sum(diff[s..i]) < 0`, while every prefix before `i` from `s` was nonnegative. For any `k` with `s <= k <= i`, the sum `diff[k..i]` equals `diff[s..i] - diff[s..k-1]`. The removed prefix `diff[s..k-1]` is nonnegative by first-failure minimality, so `diff[k..i] <= diff[s..i] < 0`. Thus `k` also cannot reach past `i`; all starts in the failed block are invalid and resetting to `i + 1` loses no solution.

Equivalently, with prefix sums `P[0]=0`, `P[t+1]=P[t]+diff[t]`, a valid circular start is any index immediately after a minimum prefix sum. If total is nonnegative, every suffix from that minimum is nonnegative relative to it, and after wrapping, adding the nonnegative total keeps the wrapped prefixes nonnegative. The reset algorithm returns exactly the index after the last running minimum encountered in a left-to-right scan.

### 11. Java

```java
class Solution {
    int canCompleteCircuit(int[] gas, int[] cost) {
        int start = 0;
        int tank = 0;
        int total = 0;

        for (int i = 0; i < gas.length; i++) {
            int diff = gas[i] - cost[i];
            tank += diff;
            total += diff;

            if (tank < 0) {
                start = i + 1;
                tank = 0;
            }
        }
        return total >= 0 ? start : -1;
    }
}
```

### 12. Code Walkthrough

`total` decides existence. `tank` tests the current candidate only. When `tank` becomes negative, the proof eliminates the entire candidate block, so the next possible start is `i + 1` and the local tank resets to zero.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n) — one pass. **S:** O(1) — three scalar variables. If `gas[i]` and `cost[i]` can be very large, use `long` for `tank` and `total`.

### 14. Edge Cases

- Single station: valid iff `gas[0] >= cost[0]`.
- Multiple valid starts: this algorithm returns one determined by reset positions.
- Total exactly zero can still be feasible; do not require positive total.
- Consecutive deficits are skipped as a block.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Returning `start` without checking `total >= 0` accepts impossible cycles. Another common error is resetting on `tank <= 0`; zero tank is still feasible and should not eliminate the current start.

### 16. Optimization

The algorithm is already optimal. A two-pass prefix-min method is equally O(n), but the reset version combines finding the minimum-prefix successor and checking total in one scan.

### 17. Alternatives

- Brute force simulation: O(n^2).
- Prefix-min rotation: compute all prefix sums, pick index after the minimum prefix, then check total.
- Deque/sliding approaches are unnecessary for the single full-cycle feasibility question.

### 18. Interview Follow-Ups

- Prove uniqueness under the platform's constraints, or explain why uniqueness is not generally guaranteed.
- Return all valid starts: requires more prefix-sum analysis, not this single reset.
- Allow finite tank capacity: greedy changes; surplus may be wasted, so extra state is needed.

### 19. Variations

The same reset logic appears in maximum subarray: a negative running sum cannot help any future subarray. Here the circle and total-sum condition add the existence proof.

### 20. Pattern Connection

Gas Station is the canonical **running-sum greedy**. Unlike interval scheduling, the proof is not an exchange of objects but an elimination lemma over failed prefixes plus a prefix-min characterization. It is greedy because the scan proves entire ranges of starts irrelevant.

---

## Fractional Knapsack (Value/Weight Ratio)

!!! pattern "Pattern: Density greedy · T: O(n log n) · S: O(1) excluding sort"
    **Signals:** items are divisible; maximize value under capacity; each infinitesimal unit of weight from an item has constant value density.

### 1. Problem

Given items with `value` and `weight`, and a knapsack capacity, maximize total value when you may take any fraction of an item.

### 2. Greedy Rule

Sort items by decreasing `value / weight`, then take as much as possible from each item in that order. The rule is about **density**, not absolute value.

### 3. Key Observation

!!! key "Key observation"
    If a solution takes weight from a lower-density item while leaving available weight from a higher-density item, swapping an equal amount of weight increases or preserves value. Therefore an optimum is sorted by nonincreasing density.

### 4. Invariant

After processing the first `i` density-sorted items, the algorithm has the maximum possible value among all solutions using the same consumed capacity from the processed density prefix.

### 5. Visual Explanation

```diagram
{"type":"bars","values":[60,100,120],"highlights":{"0":"green","1":"green","2":"amber"}}
```

For weights `[10,20,30]` and values `[60,100,120]`, densities are `6,5,4`. Capacity `50` takes all of the first two items and `20/30` of the third.

### 6. Java

```java
import java.util.Arrays;

class FractionalKnapsack {
    static final class Item {
        final int value;
        final int weight;

        Item(int value, int weight) {
            this.value = value;
            this.weight = weight;
        }
    }

    double maxValue(Item[] items, int capacity) {
        Arrays.sort(items, (a, b) ->
            Long.compare((long) b.value * a.weight, (long) a.value * b.weight));

        double total = 0.0;
        int remaining = capacity;
        for (Item item : items) {
            if (remaining == 0) break;
            int take = Math.min(remaining, item.weight);
            total += (double) item.value * take / item.weight;
            remaining -= take;
        }
        return total;
    }
}
```

### 7. Complexity

!!! complexity "Complexity"
    **T:** O(n log n) for sorting. **S:** O(1) auxiliary excluding sort implementation. Cross-multiplication uses `long` to avoid comparator overflow and precision bugs.

### 8. Pattern Connection

Fractional knapsack is greedy; 0/1 knapsack is DP. Divisibility is the structural difference: exchange can move an arbitrary small amount of weight between items. Once items are indivisible, local density can be wrong because capacity remainders become combinatorial state.

---

## Interval Scheduling / Minimum Number of Arrows / Meeting-room Style Greedy

!!! pattern "Pattern: Interval endpoint greedy · T: O(n log n) · S: O(1) to O(n)"
    **Signals:** intervals, endpoints, compatibility/coverage/overlap count; sort transforms geometry into a one-pass invariant.

### 1. Problem

Several interview problems share interval mechanics but ask different objectives:

- **Minimum arrows to burst balloons:** each arrow shot at coordinate `x` bursts every interval containing `x`; minimize arrows.
- **Meeting rooms required:** given meeting intervals, return the maximum number of simultaneous meetings.
- **Interval scheduling:** choose or remove intervals using endpoint compatibility.

### 2. Greedy Rule

For arrows, sort by end coordinate and shoot at the earliest current end; it covers the maximum possible set without reducing future options. For meeting rooms, sort start/end events and greedily reuse a room when the earliest ending meeting has finished.

### 3. Key Observation

!!! key "Key observation"
    Intervals become easy when the maintained state is an endpoint: a chosen arrow position, the last selected finish time, or the earliest room-release time. If the objective is unweighted and the state is monotone, sorting by the right endpoint or sweeping events is usually enough.

### 4. Invariant

For arrows, after shooting at `arrowX`, all processed intervals are burst, and `arrowX` is the smallest possible endpoint for the current overlapping group. For meeting rooms, the min-heap contains exactly the end times of active meetings.

### 5. Visual Explanation

```diagram
{"type":"intervals","min":0,"max":12,"intervals":[{"start":1,"end":6,"label":"burst @6","role":"green"},{"start":2,"end":8,"label":"burst @6","role":"green"},{"start":7,"end":12,"label":"burst @12","role":"primary"},{"start":10,"end":11,"label":"burst @11","role":"amber"}]}
```

The first overlapping group can be stabbed at the earliest end `6`. Intervals starting after `6` need a new arrow. Meeting rooms uses the dual view: instead of stabbing groups, count how many are simultaneously active.

### 6. Java

```java
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;

class IntervalGreedy {
    int findMinArrowShots(int[][] points) {
        if (points.length == 0) return 0;
        Arrays.sort(points, Comparator.comparingInt(a -> a[1]));

        int arrows = 1;
        int arrowX = points[0][1];
        for (int i = 1; i < points.length; i++) {
            if (points[i][0] > arrowX) {
                arrows++;
                arrowX = points[i][1];
            }
        }
        return arrows;
    }

    int minMeetingRooms(int[][] intervals) {
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));
        PriorityQueue<Integer> ends = new PriorityQueue<>();

        for (int[] meeting : intervals) {
            if (!ends.isEmpty() && ends.peek() <= meeting[0]) {
                ends.poll();
            }
            ends.offer(meeting[1]);
        }
        return ends.size();
    }
}
```

### 7. Complexity

!!! complexity "Complexity"
    **T:** O(n log n) for sorting; meeting rooms also performs O(log n) heap operations per interval. **S:** O(1) for arrows excluding sort, O(n) for the meeting-room heap.

### 8. Pattern Connection

These variants differ by objective: **select compatible intervals** sorts by end and accepts gaps; **stab intervals** sorts by end and groups overlaps; **count resources** sweeps active intervals. If intervals have weights or require choosing among incompatible future values, move to DP.
