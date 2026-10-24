## Concepts & Mental Models

Prefix sums convert repeated range aggregation into arithmetic. For an array `a[0..n-1]`, build `prefix` of size `n + 1` with `prefix[0] = 0` and `prefix[i + 1] = prefix[i] + a[i]`. The exact identity is:

`prefix[r + 1] - prefix[l] = sum(a[l..r])`

The extra leading zero is not cosmetic; it makes empty-left-boundary ranges and zero-based indexing uniform.

Difference arrays are the inverse mental model. Instead of storing values directly, store boundary deltas: `diff[i]` says how much the running value changes when you enter index `i`. A range update `[l, r] += v` becomes two O(1) edits: `diff[l] += v` and, if `r + 1 < n`, `diff[r + 1] -= v`. The final values are reconstructed by one prefix pass. The reconstruction invariant is: after processing index `i`, `running = diff[0] + ... + diff[i]`, and `running` equals the net value applied to position `i`.

Sweep line generalizes the same idea from array indices to ordered coordinates or times. Convert intervals into events, sort events, and scan left to right while maintaining running state: active intervals, current load, open segments, or max concurrency. Prefix sum, difference array, and sweep line are the same family: **put changes at boundaries, then integrate in order**.

---

## Prefix Sum

!!! pattern "Pattern: Prefix Sum · T: O(n) build / O(1) query · S: O(n)"
    **Signals:** many immutable range-sum queries, repeated subarray aggregation, need `sum(l..r)` without rescanning.

### 1. Problem

Given an immutable integer array, preprocess it so each range sum query `sumRange(l, r)` returns the sum of elements from index `l` through `r` inclusive in O(1). Extend the idea to a 2D matrix where `sumRegion(r1, c1, r2, c2)` returns an axis-aligned rectangle sum.

### 2. Intuition

If you know the sum before the range and the sum through the range, subtracting them isolates the middle. The prefix array is a ledger of cumulative totals at boundaries, not at elements. `prefix[i]` means "sum of elements strictly before index `i`." That definition makes the range `[l, r]` become boundary interval `[l, r + 1)`.

### 3. Naive

For every query, loop from `l` to `r` and add elements. This is O(r - l + 1) per query and becomes O(nq) over many queries. For 2D, scanning every cell in the rectangle is O(area) per query.

### 4. Key Observation

!!! key "Key observation"
    Store cumulative sums at boundaries: `prefix[0] = 0`, `prefix[i + 1] = prefix[i] + nums[i]`. Then the range sum is precisely `prefix[r + 1] - prefix[l] = sum(l..r)`. The left term removes everything before `l`; the right boundary includes `r` because of the `+1`.

### 5. Pattern Recognition

**Signals.** Immutable input, many sum queries, static preprocessing allowed, query endpoints vary.

**Shortcut.** If the operation is associative and has an inverse under subtraction-like cancellation, ask whether two cumulative states can isolate a range.

**Related.** Prefix counts for characters, prefix XOR, 2D prefix sums, subarray sum via prefix differences, Fenwick trees for mutable variants.

### 6. Invariant

After building through element `i - 1`, `prefix[i] = nums[0] + ... + nums[i - 1]`. Therefore `prefix[r + 1]` contains everything up to `r`, while `prefix[l]` contains exactly the part before `l`; their difference contains only `l..r`.

For 2D, `ps[r + 1][c + 1]` equals the sum of all cells in rows `< r + 1` and columns `< c + 1`. A rectangle is obtained by inclusion-exclusion:

`ps[r2 + 1][c2 + 1] - ps[r1][c2 + 1] - ps[r2 + 1][c1] + ps[r1][c1]`.

### 7. Visual Explanation

```diagram
{"type":"array","values":[2,-1,3,5,-2],"index":[0,1,2,3,4],"highlights":{"1":"amber","2":"amber","3":"amber"},"pointers":[{"name":"l","index":1,"color":"primary","side":"bottom"},{"name":"r","index":3,"color":"primary","side":"bottom"}],"brackets":[{"from":1,"to":3,"label":"query [1,3]","color":"primary","row":0}],"caption":"The raw range is nums[1..3] = -1 + 3 + 5."}
```

```diagram
{"type":"array","values":[0,2,1,4,9,7],"index":[0,1,2,3,4,5],"highlights":{"1":"red","4":"green"},"pointers":[{"name":"prefix[l]","index":1,"color":"red","side":"bottom"},{"name":"prefix[r+1]","index":4,"color":"green","side":"bottom"}],"brackets":[{"from":1,"to":4,"label":"boundary interval [l,r+1)","color":"primary","row":0}],"caption":"prefix[4] - prefix[1] = 9 - 2 = 7, which equals nums[1] + nums[2] + nums[3]."}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":460,"box":270,"title":"Immutable range sum","steps":[{"type":"start","text":"Build prefix[0] = 0"},{"type":"process","text":"For each i:\nprefix[i+1] = prefix[i] + nums[i]"},{"type":"io","text":"Query (l, r)"},{"type":"process","text":"answer = prefix[r+1] - prefix[l]"},{"type":"end","text":"Return answer"}]}
```

### 9. Walkthrough

For `nums = [2, -1, 3, 5, -2]`:

| i | nums[i] | prefix[i + 1] |
|---|---:|---:|
| - | - | `prefix[0] = 0` |
| 0 | 2 | 2 |
| 1 | -1 | 1 |
| 2 | 3 | 4 |
| 3 | 5 | 9 |
| 4 | -2 | 7 |

`sumRange(1, 3) = prefix[4] - prefix[1] = 9 - 2 = 7`.

### 10. Why It Works

The build invariant follows by induction: `prefix[0]` is the empty sum; adding `nums[i]` extends the sum from elements `< i` to elements `< i + 1`. At query time, `prefix[r + 1]` contains the desired range plus all earlier elements, and `prefix[l]` contains exactly those earlier elements. Subtraction cancels the shared prefix and leaves the requested range.

### 11. Java

```java
class NumArray {
    private final long[] prefix;

    NumArray(int[] nums) {
        prefix = new long[nums.length + 1];
        for (int i = 0; i < nums.length; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
    }

    long sumRange(int left, int right) {
        return prefix[right + 1] - prefix[left];
    }
}

class NumMatrix {
    private final long[][] ps;

    NumMatrix(int[][] matrix) {
        int m = matrix.length;
        int n = m == 0 ? 0 : matrix[0].length;
        ps = new long[m + 1][n + 1];

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                ps[r + 1][c + 1] = matrix[r][c]
                    + ps[r][c + 1]
                    + ps[r + 1][c]
                    - ps[r][c];
            }
        }
    }

    long sumRegion(int r1, int c1, int r2, int c2) {
        return ps[r2 + 1][c2 + 1]
            - ps[r1][c2 + 1]
            - ps[r2 + 1][c1]
            + ps[r1][c1];
    }
}
```

### 12. Code Walkthrough

`prefix` has length `n + 1` so `prefix[0]` represents "before the first element." Query endpoint `right` maps to boundary `right + 1`. The 2D version uses the same boundary convention in both dimensions. The `- ps[r][c]` term removes the overlap counted twice when adding top and left accumulated regions.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n) preprocessing and O(1) per 1D query; O(mn) preprocessing and O(1) per 2D query. **S:** O(n) for 1D; O(mn) for 2D. Use `long` when cumulative sums may exceed `int`.

### 14. Edge Cases

- `l = 0` works because `prefix[0] = 0`.
- Single-element query `l == r` returns `prefix[l + 1] - prefix[l]`.
- Negative values are fine; prefix sums do not require monotonicity.
- Empty matrix should allocate a valid `(m + 1) x (n + 1)` prefix shape.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    The most common bug is using `prefix[r] - prefix[l]` for an inclusive query. With a size-`n+1` prefix array, inclusive `r` always maps to `r + 1`. In 2D, forgetting to add back the overlapped top-left rectangle double-subtracts it.

### 16. Optimization

For immutable arrays, this is already optimal for arbitrary range-sum queries: O(1) query time requires storing enough cumulative state. If memory is tight and queries are offline, batching or block decomposition can trade O(1) queries for lower space.

### 17. Alternatives

Segment trees and Fenwick trees support updates but have O(log n) query/update costs. Sparse tables work for idempotent operations such as min/max, not sums with updates. Direct scanning is viable only for very few or tiny queries.

### 18. Interview Follow-Ups

- Make the array mutable: use a Fenwick tree or segment tree.
- Count subarrays with a given sum: store counts of prior prefix values.
- Support rectangle updates: use 2D difference arrays or Fenwick trees.

### 19. Variations

- Prefix XOR: `xor(l..r) = px[r + 1] ^ px[l]`.
- Prefix counts: store cumulative frequency per character or value bucket.
- Prefix minima/maxima: useful for one-sided queries, but not arbitrary range isolation because min/max lack inverses.

### 20. Pattern Connection

Prefix sums are the read-query side of the boundary-delta family. Difference arrays reverse the direction: make range updates cheap, then do one prefix pass to materialize values. Sweep line applies the same boundary accounting after sorting arbitrary coordinates.

---

## Subarray Sum Equals K

### Problem

Given an integer array and an integer `k`, count the number of contiguous subarrays whose sum equals `k`.

### Key Observation

!!! key "Key observation"
    Let `prefix[j]` be the sum before index `j`. A subarray ending at current boundary has sum `k` when `currentPrefix - previousPrefix = k`, so `previousPrefix = currentPrefix - k`. Count how many previous prefix sums have that value. Unlike sliding window from Module 2, this works with negatives because it never relies on monotonic expansion or shrinking.

### Invariant

Before processing `nums[i]`, the map stores frequencies of all prefix sums ending before `i`. After adding `nums[i]` to `sum`, every prior prefix `sum - k` identifies one subarray ending at `i` with total `k`; then the current prefix is inserted for future endpoints.

### Diagram

```diagram
{"type":"array","values":[0,1,3,2,5],"index":[0,1,2,3,4],"highlights":{"1":"red","4":"green"},"pointers":[{"name":"prev = current-k","index":1,"color":"red","side":"bottom"},{"name":"current","index":4,"color":"green","side":"bottom"}],"brackets":[{"from":1,"to":4,"label":"prefix difference = k","color":"primary","row":0}],"caption":"If current prefix is 5 and k = 4, every previous prefix 1 forms a valid subarray between the two boundaries."}
```

### Java

```java
int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> count = new HashMap<>();
    count.put(0, 1);

    int sum = 0;
    int ans = 0;
    for (int x : nums) {
        sum += x;
        ans += count.getOrDefault(sum - k, 0);
        count.put(sum, count.getOrDefault(sum, 0) + 1);
    }
    return ans;
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n) expected with hashing. **S:** O(n) for distinct prefix sums. Use `long` keys when input bounds can overflow `int`.

### Pattern Connection

This is prefix sum plus frequency counting, not two pointers. Cross-reference Module 2 for hash-map counting mechanics; the key distinction here is that negative numbers break sliding-window monotonicity, while prefix-difference identities remain exact.

---

## Range Addition / Difference Array

!!! pattern "Pattern: Difference Array · T: O(q + n) · S: O(n)"
    **Signals:** many range increment updates, final array requested after all updates, no need to query between updates.

### 1. Problem

You are given an initially zero array of length `n` and a list of updates `[l, r, val]`, each meaning add `val` to every index from `l` through `r` inclusive. Return the final array after all updates.

### 2. Intuition

Do not write `val` into every cell of `[l, r]`. Instead, mark where the value starts affecting the running total and where it stops. A range increment is a step function: it jumps up at `l` and jumps down just after `r`.

### 3. Naive

Apply each update by looping from `l` to `r`. With `q` updates over length `n`, worst-case time is O(qn). This is the exact shape difference arrays eliminate.

### 4. Key Observation

!!! key "Key observation"
    Store boundary changes, not final values. For `[l, r] += v`, do `diff[l] += v` and, if `r + 1 < n`, `diff[r + 1] -= v`. One final prefix pass reconstructs the array. The reconstruction invariant is: after index `i`, `running = diff[0] + ... + diff[i]`, which equals the total update value active at `i`.

### 5. Pattern Recognition

**Signals.** Range updates are offline, the operation is additive, and only the final state is needed.

**Shortcut.** If every update paints a contiguous interval with the same delta, convert interval interiors into two boundary events.

**Related.** Corporate Flight Bookings, car pooling capacity checks, imos method, sweep line over compressed coordinates.

### 6. Invariant

During reconstruction, `running` equals the sum of all `v` for updates whose `l <= i <= r`. Each such update has contributed `+v` at or before `i` and has not yet contributed its `-v` cancellation. Updates ending before `i` have already canceled at `r + 1`.

### 7. Visual Explanation

```diagram
{"type":"array","values":[0,0,0,0,0],"index":[0,1,2,3,4],"highlights":{"1":"green","4":"red"},"pointers":[{"name":"+3 at l","index":1,"color":"green","side":"bottom"},{"name":"-3 at r+1","index":4,"color":"red","side":"bottom"}],"brackets":[{"from":1,"to":3,"label":"update [1,3] += 3","color":"primary","row":0}],"caption":"The update affects indices 1..3. The negative boundary at 4 turns the effect off."}
```

```diagram
{"type":"array","values":[0,3,0,0,-3],"index":[0,1,2,3,4],"highlights":{"1":"green","4":"red"},"pointers":[{"name":"enter","index":1,"color":"green","side":"bottom"},{"name":"exit","index":4,"color":"red","side":"bottom"}],"brackets":[{"from":1,"to":4,"label":"diff encodes boundaries, not filled values","color":"primary","row":0}],"caption":"Prefixing diff gives [0,3,3,3,0]."}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":470,"box":285,"title":"Range addition with difference array","steps":[{"type":"start","text":"diff = new long[n]"},{"type":"process","text":"For each update [l,r,v]:\ndiff[l] += v"},{"type":"decision","text":"r + 1 < n?","yes":"yes","branch":{"label":"no","text":"skip closing boundary","role":"primary"}},{"type":"process","text":"diff[r+1] -= v"},{"type":"process","text":"Prefix-scan diff into answer"},{"type":"end","text":"Return answer"}]}
```

### 9. Walkthrough

For `n = 5`, updates `[1,3,3]`, `[2,4,2]`, `[0,2,-1]`:

| update | diff after boundary edits |
|---|---|
| start | `[0, 0, 0, 0, 0]` |
| `[1,3]+=3` | `[0, 3, 0, 0, -3]` |
| `[2,4]+=2` | `[0, 3, 2, 0, -3]` |
| `[0,2]+=-1` | `[-1, 3, 2, 1, -3]` |

Prefix reconstruction: `[-1, 2, 4, 5, 2]`.

### 10. Why It Works

Each update contributes `v` to `running` starting at `l`. It contributes `-v` at `r + 1`, so for positions after `r`, the update's net contribution is zero. Thus exactly the indices inside `[l, r]` see that update in the running sum. Since addition is associative and commutative, overlapping updates simply accumulate.

### 11. Java

```java
long[] getModifiedArray(int n, int[][] updates) {
    long[] diff = new long[n + 1];

    for (int[] update : updates) {
        int l = update[0];
        int r = update[1];
        int v = update[2];
        diff[l] += v;
        diff[r + 1] -= v;
    }

    long[] ans = new long[n];
    long running = 0;
    for (int i = 0; i < n; i++) {
        running += diff[i];
        ans[i] = running;
    }
    return ans;
}
```

### 12. Code Walkthrough

The implementation allocates `n + 1` so `diff[r + 1] -= v` is always legal, even when `r == n - 1`; the sentinel slot is never copied to the answer. The final loop is the integration step: every boundary delta becomes an active value until canceled.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(q + n), where `q` is the number of updates. Each update is O(1), then one prefix pass reconstructs the array. **S:** O(n) for `diff` and the returned result.

### 14. Edge Cases

- Update starts at `0`: `diff[0] += v` immediately affects the running sum.
- Update ends at `n - 1`: the `n + 1` sentinel absorbs the closing delta.
- Negative updates work naturally as additive deltas.
- Multiple updates with the same boundary should be added, not overwritten.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Forgetting the closing boundary `diff[r + 1] -= v` turns a finite range into a suffix update. Allocating only `n` cells and conditionally skipping the final close is valid, but using `n + 1` is safer and keeps the formula uniform.

### 16. Optimization

If the input bounds guarantee `int` safety, `int[]` is acceptable. In production and senior interviews, prefer `long[]` unless constraints explicitly cap the total accumulated value.

### 17. Alternatives

Segment trees or Fenwick trees are appropriate when updates and queries are interleaved. Lazy propagation handles online range updates and range queries. For one final materialization, those structures are unnecessary overhead.

### 18. Interview Follow-Ups

- Support range update and point query online: Fenwick tree over the difference array.
- Support range update and range sum query online: two Fenwick trees or lazy segment tree.
- Extend to 2D rectangle additions: update four corners, then prefix in two dimensions.

### 19. Variations

- Difference over event times for car pooling.
- Character shift ranges in strings.
- Coverage count over compressed coordinates.
- Offline capacity validation by checking maximum reconstructed load.

### 20. Pattern Connection

Difference arrays are prefix sums turned inside out. Prefix sums answer many range reads on immutable data; difference arrays absorb many range writes and pay one final integration cost.

---

## Corporate Flight Bookings

### Problem

There are `n` flights labeled `1..n`. Each booking `[first, last, seats]` adds `seats` passengers to every flight from `first` through `last`. Return the total seats booked for each flight.

### Key Observation

!!! key "Key observation"
    Convert the 1-based inclusive booking interval to zero-based boundaries: `l = first - 1`, `r = last - 1`. Then apply the standard difference update `diff[l] += seats`, `diff[r + 1] -= seats`, followed by one prefix pass.

### Invariant

At flight index `i`, the reconstruction running sum equals the total seats from all bookings whose converted interval contains `i`. A booking contributes at `first - 1` and is canceled immediately after `last - 1`.

### Index Conversion

The input uses 1-based flight labels, but Java arrays are zero-based. Convert the inclusive booking `[first, last]` to `l = first - 1` and close at `last`, which is exactly `r + 1` after conversion.

### Diagram

```diagram
{"type":"array","values":[0,10,0,-10,0,0],"index":[0,1,2,3,4,5],"highlights":{"1":"green","3":"red"},"pointers":[{"name":"first-1","index":1,"color":"green","side":"bottom"},{"name":"last","index":3,"color":"red","side":"bottom"}],"brackets":[{"from":1,"to":2,"label":"booking flights 2..3 += 10","color":"primary","row":0}],"caption":"For 1-based [2,3], add at zero-based 1 and close at index 3."}
```

### Java

```java
int[] corpFlightBookings(int[][] bookings, int n) {
    int[] diff = new int[n + 1];

    for (int[] booking : bookings) {
        int l = booking[0] - 1;
        int r = booking[1] - 1;
        int seats = booking[2];
        diff[l] += seats;
        diff[r + 1] -= seats;
    }

    int[] ans = new int[n];
    int running = 0;
    for (int i = 0; i < n; i++) {
        running += diff[i];
        ans[i] = running;
    }
    return ans;
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(b + n), where `b` is the number of bookings. **S:** O(n) for the difference array and answer.

### Pattern Connection

This is not a flight-specific problem; it is pure range addition with 1-based input labels. The only interview trap is index conversion. Once converted, it is the same boundary-delta invariant as the flagship difference-array template.

---

## Meeting Rooms II via Sweep Line

!!! pattern "Pattern: Sweep Line · T: O(n log n) · S: O(n)"
    **Signals:** intervals overlap, need maximum simultaneous activity, endpoints define all possible state changes.

### 1. Problem

Given meeting intervals `[start, end)`, return the minimum number of rooms required so all meetings can be scheduled. The answer is the maximum number of meetings active at any time.

### 2. Intuition

A room is needed only while a meeting is active. Starts increase active meetings; ends decrease active meetings. If we process all time events in sorted order, the maximum running active count is exactly the number of rooms needed.

### 3. Naive

For each meeting, compare it with every other meeting or try to assign rooms greedily by scanning existing room end times. A simple room-list scan can degrade to O(n²). Sorting endpoints gives the same information in O(n log n).

### 4. Key Observation

!!! key "Key observation"
    Minimum rooms equals maximum concurrency. Treat each start as `+1` and each end as `-1`, sort by time, and scan. For half-open intervals `[start, end)`, process an end at time `t` before a start at time `t` so a meeting ending at 10 frees a room for one starting at 10.

### 5. Pattern Recognition

**Signals.** Intervals, "minimum resources," "maximum overlap," "active at the same time."

**Shortcut.** Convert intervals to start/end events; the answer is often an extremum of a running count.

**Related.** Car pooling, employee free time, skyline, number of airplanes in the sky, maximum population year.

### 6. Invariant

After processing all events up to time `t` in tie-safe order, `active` equals the number of meetings with `start <= t < end` that have started but not ended. `maxActive` is the maximum such value seen so far, so it is the minimum number of rooms required.

### 7. Visual Explanation

```diagram
{"type":"intervals","min":0,"max":40,"intervals":[{"start":0,"end":30,"label":"A","role":"amber"},{"start":5,"end":10,"label":"B","role":"primary"},{"start":10,"end":20,"label":"C","role":"green"},{"start":15,"end":25,"label":"D","role":"purple"},{"start":15,"end":15,"label":"max = 3","role":"red"}]}
```

```diagram
{"type":"array","values":["0:+1","5:+1","10:-1","10:+1","15:+1","20:-1","25:-1","30:-1"],"index":[0,1,2,3,4,5,6,7],"highlights":{"4":"red"},"pointers":[{"name":"active becomes 3","index":4,"color":"red","side":"bottom"}],"brackets":[{"from":0,"to":7,"label":"sorted events; ends before starts on ties","color":"primary","row":0}],"caption":"The peak active count is 3, so three rooms are required."}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":470,"box":285,"title":"Sweep line for minimum rooms","steps":[{"type":"start","text":"Create start[] and end[]"},{"type":"process","text":"Sort both arrays"},{"type":"decision","text":"next start < next end?","yes":"yes","branch":{"label":"no","text":"end meeting: active--","role":"primary"}},{"type":"process","text":"start meeting: active++\nmax = max(max, active)"},{"type":"process","text":"advance selected pointer"},{"type":"end","text":"Return max"}]}
```

### 9. Walkthrough

Intervals: `[0,30)`, `[5,10)`, `[10,20)`, `[15,25)`.

| event | active | max |
|---|---:|---:|
| start 0 | 1 | 1 |
| start 5 | 2 | 2 |
| end 10 | 1 | 2 |
| start 10 | 2 | 2 |
| start 15 | 3 | 3 |
| end 20 | 2 | 3 |
| end 25 | 1 | 3 |
| end 30 | 0 | 3 |

### 10. Why It Works

A room is occupied exactly on the half-open interval from its meeting's start to its end. The sweep count is therefore the exact occupancy after every boundary event. Between two adjacent event times, occupancy cannot change, so the maximum must occur immediately after processing some event. The peak occupancy is both necessary and sufficient: necessary because that many simultaneous meetings need distinct rooms; sufficient because reusing rooms at end events never violates overlap constraints.

### 11. Java

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

    int s = 0;
    int e = 0;
    int active = 0;
    int maxRooms = 0;

    while (s < n) {
        if (starts[s] < ends[e]) {
            active++;
            maxRooms = Math.max(maxRooms, active);
            s++;
        } else {
            active--;
            e++;
        }
    }
    return maxRooms;
}
```

### 12. Code Walkthrough

Two sorted arrays avoid allocating event objects. When the next start is strictly before the next end, a new meeting overlaps existing active meetings, so it consumes a room. Otherwise, an earlier meeting has ended and its room is released first. The strict `<` encodes half-open intervals and handles back-to-back meetings correctly.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n log n) for sorting starts and ends; the scan is O(n). **S:** O(n) for endpoint arrays. If intervals may be modified and object sorting is acceptable, event sorting has the same asymptotic cost.

### 14. Edge Cases

- Empty interval list returns 0.
- Back-to-back meetings `[1,5)` and `[5,8)` require one room, not two.
- Identical start times accumulate multiple rooms.
- Zero-length intervals should be clarified; under `[start,end)` semantics, they consume no time.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Processing starts before ends at the same timestamp overcounts rooms for back-to-back meetings. In the two-array version, use `starts[s] < ends[e]`, not `<=`, when intervals are `[start, end)`.

### 16. Optimization

If times are small bounded integers, a difference array over time can reduce sorting to O(U + n), where `U` is the coordinate range. For large timestamps, coordinate compression or ordinary sorting is preferable.

### 17. Alternatives

A min-heap of room end times also works: sort intervals by start, pop rooms whose end is `<= start`, push current end, track heap size. It is often easier to adapt when you must output room assignments, not just the count.

### 18. Interview Follow-Ups

- Return actual room assignments: use a min-heap of `(end, roomId)`.
- Find free time across calendars: sweep active count and emit gaps where active is zero.
- Add capacity per room or weighted meetings: maintain weighted active load instead of count.

### 19. Variations

- Car Pooling: passenger count is active load; capacity bounds the maximum.
- Number of Airplanes in the Sky: same max-concurrency sweep.
- Maximum population year: births are starts, deaths are ends with problem-specific tie rules.

### 20. Pattern Connection

Sweep line is a difference array without dense indices. Instead of writing `diff[t]`, you create sparse boundary events, sort them, and prefix-scan the deltas. The core invariant—running state equals the sum of all boundary changes seen so far—is identical.
