## Concepts & Mental Models

Arrays give constant-time positional access; hashing gives **O(1) expected associative memory** over arbitrary keys. Most senior-level array/hashmap interview problems are not about the container itself — they are about choosing the smallest state that makes a future decision local.

!!! key "Core models"
    **Hashing as memory:** replace "scan everything before me" with `seen.get(state)`. **Prefix/running state:** a subarray becomes a difference between two prefix states. **Seen-before map:** store counts, earliest indices, or membership for prior states. **In-place partitioning:** split the array into regions with meanings, then move the unknown frontier.

### Transfer checklist

| Situation | State to keep | Typical pattern |
|---|---|---|
| "Have I seen the complement?" | set/map of values | Two Sum, duplicates |
| "How many subarrays end here?" | frequency of prefix states | Subarray Sum Equals K |
| "Best interval ending here?" | running DP state | Kadane, max product |
| "Sort a few categories in-place?" | region boundaries | Dutch National Flag |
| "All except this index?" | prefix + suffix contribution | Product Except Self |

---

## Dutch National Flag (Three-Way Partition)

!!! pattern "Pattern: In-place partitioning · T: O(n) · S: O(1)"
    **Signals:** three categories, in-place reorder, constant space, values like `0/1/2` or `< pivot`/`=`/`> pivot`.

### 1. Problem

Given an array containing only `0`, `1`, and `2`, reorder it in-place so all `0`s come first, then all `1`s, then all `2`s. The point is not comparison sorting; it is maintaining partition regions while the array mutates.

### 2. Intuition

Think of the array as four regions: known `0`s, known `1`s, unknown values, known `2`s. Inspect the first unknown value and swap it into its region. The unknown region shrinks every iteration.

### 3. Naive

Count the three values, then overwrite the array. This is O(n), but it is two-pass and works only when overwriting values is legal.

```java
void sortColorsCounting(int[] nums) {
    int[] count = new int[3];
    for (int x : nums) count[x]++;
    int write = 0;
    for (int value = 0; value < 3; value++) {
        for (int c = 0; c < count[value]; c++) nums[write++] = value;
    }
}
```

### 4. Key Observation

!!! key "Key observation"
    Maintain `[0, low)` as `0`, `[low, mid)` as `1`, `[mid, high]` as unknown, and `(high, n)` as `2`. Each branch preserves these meanings and removes one element from the unknown region.

### 5. Pattern Recognition

**Signals.** In-place, small finite categories, partition by key, unstable order acceptable.

**Shortcut.** `0` goes left and advances `low, mid`; `1` is already in the middle and advances `mid`; `2` goes right and only decreases `high`.

**Related.** Quicksort three-way partition, quickselect, segregate negatives/positives, remove element.

### 6. Invariant

Before every loop iteration:

- `nums[0..low-1]` are all `0`.
- `nums[low..mid-1]` are all `1`.
- `nums[mid..high]` are unclassified.
- `nums[high+1..n-1]` are all `2`.

When `mid > high`, no unknown cells remain.

### 7. Visual Explanation

```diagram
{"type":"array","title":"Classify the first unknown cell","values":[2,0,2,1,1,0],"highlights":{"0":"amber","5":"purple"},"pointers":[{"name":"low","index":0,"color":"green","side":"bottom"},{"name":"mid","index":0,"color":"primary","side":"top"},{"name":"high","index":5,"color":"red","side":"bottom"}],"brackets":[{"from":0,"to":5,"label":"unknown","color":"amber","row":0}],"caption":"nums[mid] is 2, so swap it with nums[high]. The incoming value at mid is still unknown."}
```

```diagram
{"type":"array","title":"After moving a 2 into the right region","values":[0,0,2,1,1,2],"highlights":{"0":"green","5":"red"},"pointers":[{"name":"low","index":0,"color":"green","side":"bottom"},{"name":"mid","index":0,"color":"primary","side":"top"},{"name":"high","index":4,"color":"red","side":"bottom"}],"brackets":[{"from":0,"to":4,"label":"unknown","color":"amber","row":0},{"from":5,"to":5,"label":"2s","color":"red","row":1}],"caption":"The right region is fixed. The next classification sees nums[mid] = 0."}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":460,"box":270,"title":"Dutch National Flag flow","steps":[{"type":"start","text":"low = 0\nmid = 0\nhigh = n - 1"},{"type":"decision","text":"mid <= high?","yes":"yes","branch":{"label":"no","text":"done","role":"green"}},{"type":"decision","text":"nums[mid] == 0?","yes":"yes","branch":{"label":"no","text":"check 2","role":"primary"}},{"type":"process","text":"swap(low, mid)\nlow++\nmid++"},{"type":"decision","text":"nums[mid] == 2?","yes":"yes","branch":{"label":"no","text":"mid++","role":"green"}},{"type":"process","text":"swap(mid, high)\nhigh--"},{"type":"end","text":"partitioned"}]}
```

### 9. Walkthrough

| step | low | mid | high | action | array |
|---|---:|---:|---:|---|---|
| 0 | 0 | 0 | 5 | start | `[2,0,2,1,1,0]` |
| 1 | 0 | 0 | 4 | swap `2` with high | `[0,0,2,1,1,2]` |
| 2 | 1 | 1 | 4 | move `0` left | `[0,0,2,1,1,2]` |
| 3 | 2 | 2 | 4 | move `0` left | `[0,0,2,1,1,2]` |
| 4 | 2 | 2 | 3 | swap `2` with high | `[0,0,1,1,2,2]` |
| 5 | 2 | 4 | 3 | scan two `1`s | `[0,0,1,1,2,2]` |

### 10. Why It Works

The invariant is preserved by cases. A `0` swapped with `low` extends the left region; the value moved from `low` is from the `1` region or the same cell, so advancing both pointers is safe. A `1` extends the middle region. A `2` swapped with `high` extends the right region, but the incoming value at `mid` must still be classified. The unknown region strictly shrinks, so termination yields a sorted partition.

### 11. Java

```java
void sortColors(int[] nums) {
    int low = 0, mid = 0, high = nums.length - 1;
    while (mid <= high) {
        if (nums[mid] == 0) {
            swap(nums, low++, mid++);
        } else if (nums[mid] == 2) {
            swap(nums, mid, high--);
        } else {
            mid++;
        }
    }
}

private void swap(int[] a, int i, int j) {
    if (i == j) return;
    int t = a[i];
    a[i] = a[j];
    a[j] = t;
}
```

### 12. Code Walkthrough

`low` is the next slot for `0`; `high` is the next slot for `2`; `mid` is the classifier. The `2` branch intentionally does not increment `mid`.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n) — every iteration shrinks the unknown interval. **S:** O(1) — three pointers.

### 14. Edge Cases

Empty arrays, single elements, all same value, already sorted, and reverse sorted inputs all satisfy the same invariant.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Incrementing `mid` after swapping with `high` skips an unclassified value. Using `mid < high` can leave the final unknown cell unprocessed.

### 16. Optimization

Already optimal for unstable in-place partitioning. Counting can reduce swaps but does not preserve records and is less general.

### 17. Alternatives

Counting overwrite, comparison sort, or stable partition. Only DNF gives one-pass, in-place, key-preserving partitioning.

### 18. Interview Follow-Ups

Generalize to `< pivot`, `= pivot`, `> pivot`; discuss stability; use the same invariant in three-way quicksort.

### 19. Variations

Sort k colors, segregate parity, partition linked lists, quickselect partition with duplicates.

### 20. Pattern Connection

DNF is the template for region invariants: name the regions first, then write pointer updates that preserve their meanings.

---

## Kadane's Algorithm (Maximum Subarray)

!!! pattern "Pattern: Running optimum · T: O(n) · S: O(1)"
    **Signals:** maximum contiguous subarray sum, negatives allowed, choose extend-or-restart at every endpoint.

### 1. Problem

Given a non-empty integer array, return the maximum sum of any non-empty contiguous subarray.

### 2. Intuition

For a subarray ending at index `i`, only two choices exist: extend the best subarray ending at `i - 1`, or restart at `i`. A negative prefix is dead weight for every future extension.

### 3. Naive

Enumerate every start and end while maintaining a running sum.

```java
long maxSubArrayQuadratic(int[] nums) {
    long best = Long.MIN_VALUE;
    for (int left = 0; left < nums.length; left++) {
        long sum = 0;
        for (int right = left; right < nums.length; right++) {
            sum += nums[right];
            best = Math.max(best, sum);
        }
    }
    return best;
}
```

### 4. Key Observation

!!! key "Key observation"
    Let `endingHere` be the best non-empty subarray sum that must end at the current index. Then `endingHere = max(x, endingHere + x)`, and the global answer is the best `endingHere` ever seen.

### 5. Pattern Recognition

**Signals.** Contiguous, maximum/minimum, one-dimensional interval, local state tied to the current endpoint.

**Shortcut.** If the running suffix hurts, restart.

**Related.** Maximum product subarray, stock profit, circular maximum subarray, 2D max submatrix.

### 6. Invariant

After index `i`, `endingHere` is the maximum sum of a non-empty subarray ending exactly at `i`, and `best` is the maximum sum in the processed prefix.

### 7. Visual Explanation

```diagram
{"type":"bars","title":"Best subarray emerges after abandoning negative baggage","values":[-2,1,-3,4,-1,2,1,-5],"highlights":{"3":"green","4":"green","5":"green","6":"green"},"caption":"The optimal interval [4,-1,2,1] has sum 6."}
```

```diagram
{"type":"dptable","title":"Kadane running state","corner":"i","col_head":["0","1","2","3","4","5","6","7"],"row_head":["x","ending","best"],"grid":[["-2","1","-3","4","-1","2","1","-5"],["-2","1","-2","4","3","5","6","1"],["-2","1","1","4","4","5","6","6"]],"highlights":[[1,3,"green"],[1,4,"green"],[1,5,"green"],[1,6,"green"],[2,6,"purple"]],"arrows":[{"from":[1,3],"to":[1,4],"color":"green"},{"from":[1,4],"to":[1,5],"color":"green"},{"from":[1,5],"to":[1,6],"color":"green"}]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":450,"box":270,"title":"Kadane flow","steps":[{"type":"start","text":"endingHere = nums[0]\nbest = nums[0]"},{"type":"decision","text":"more elements?","yes":"yes","branch":{"label":"no","text":"return best","role":"green"}},{"type":"process","text":"endingHere = max(x, endingHere + x)"},{"type":"process","text":"best = max(best, endingHere)"},{"type":"end","text":"maximum sum"}]}
```

### 9. Walkthrough

| i | x | extend | restart | endingHere | best |
|---:|---:|---:|---:|---:|---:|
| 0 | -2 | — | -2 | -2 | -2 |
| 1 | 1 | -1 | 1 | 1 | 1 |
| 2 | -3 | -2 | -3 | -2 | 1 |
| 3 | 4 | 2 | 4 | 4 | 4 |
| 4 | -1 | 3 | -1 | 3 | 4 |
| 5 | 2 | 5 | 2 | 5 | 5 |
| 6 | 1 | 6 | 1 | 6 | 6 |
| 7 | -5 | 1 | -5 | 1 | 6 |

### 10. Why It Works

Every subarray ending at `i` is either `[i]` or a subarray ending at `i - 1` extended by `nums[i]`. The recurrence chooses the better of exactly those possibilities. Taking the maximum over all endpoints gives the answer.

### 11. Java

```java
long maxSubArray(int[] nums) {
    if (nums.length == 0) throw new IllegalArgumentException("nums must be non-empty");
    long endingHere = nums[0];
    long best = nums[0];
    for (int i = 1; i < nums.length; i++) {
        long x = nums[i];
        endingHere = Math.max(x, endingHere + x);
        best = Math.max(best, endingHere);
    }
    return best;
}
```

### 12. Code Walkthrough

Initialization from `nums[0]` enforces non-empty semantics and handles all-negative arrays. `long` prevents ordinary `int` accumulation overflow.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n) — one pass. **S:** O(1) — two accumulators.

### 14. Edge Cases

All negative, single element, large magnitude sums, and empty input policy.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Resetting to zero returns `0` for `[-5]`, which is wrong unless empty subarrays are allowed.

### 16. Optimization

Optimal. To return indices, track a candidate start when `x > endingHere + x` and commit it when `best` improves.

### 17. Alternatives

Prefix minimum (`prefix - minPrefix`), divide and conquer, or DP array. Kadane is the space-compressed endpoint DP.

### 18. Interview Follow-Ups

Return boundaries; circular maximum subarray; maximum submatrix by row compression.

### 19. Variations

Minimum subarray, maximum product subarray, maximum average with constraints.

### 20. Pattern Connection

Kadane is the running-state version of prefix thinking: keep the only endpoint state that can influence future intervals.

---

## Subarray Sum Equals K (Prefix Sum + HashMap)

!!! pattern "Pattern: Prefix sum + seen-before map · T: O(n) · S: O(n)"
    **Signals:** count contiguous subarrays with target sum, negatives allowed, all starts ending at current index matter.

### 1. Problem

Given `nums` and integer `k`, return the number of contiguous subarrays whose sum equals `k`.

### 2. Intuition

If the current prefix is `sum`, then any earlier prefix equal to `sum - k` starts a subarray ending here with sum `k`. Store prefix frequencies.

### 3. Naive

Check all subarrays with a nested loop. Negative values prevent a monotonic sliding-window shortcut.

```java
long subarraySumQuadratic(int[] nums, long k) {
    long count = 0;
    for (int left = 0; left < nums.length; left++) {
        long sum = 0;
        for (int right = left; right < nums.length; right++) {
            sum += nums[right];
            if (sum == k) count++;
        }
    }
    return count;
}
```

### 4. Key Observation

!!! key "Key observation"
    `sum(left..right) = prefix[right] - prefix[left-1]`. At each `right`, the number of valid `left` values is exactly the frequency of prior prefix `prefix[right] - k`.

### 5. Pattern Recognition

**Signals.** Contiguous target sum, count all, negative numbers or zeros, no fixed window size.

**Shortcut.** Turn the subarray equation into a complement lookup over previous prefix sums.

**Related.** Two Sum, subarrays divisible by K, longest subarray sum K, Path Sum III.

### 6. Invariant

Before processing `nums[i]`, `freq` contains counts of all prefix sums before `i`, including empty prefix `0`. After adding `nums[i]`, `freq[prefix-k]` is the number of valid subarrays ending at `i`.

### 7. Visual Explanation

```diagram
{"type":"array","title":"Current prefix looks for prefix - k","values":[1,2,3,-2,2],"highlights":{"0":"green","1":"green","2":"primary"},"pointers":[{"name":"i","index":2,"color":"primary","side":"top"}],"brackets":[{"from":0,"to":2,"label":"prefix = 6","color":"primary","row":0},{"from":0,"to":1,"label":"prior prefix = 3","color":"green","row":1},{"from":2,"to":2,"label":"sum k = 3","color":"purple","row":2}],"caption":"For k=3, current prefix 6 needs a prior prefix 3."}
```

```diagram
{"type":"dptable","title":"Prefix frequencies, k = 3","corner":"step","col_head":["init","1","2","3","-2","2"],"row_head":["prefix","need","matches","count"],"grid":[["0","1","3","6","4","6"],["—","-2","0","3","1","3"],["—","0","1","1","1","1"],["0","0","1","2","3","4"]],"highlights":[[1,2,"green"],[2,2,"green"],[3,5,"purple"]],"arrows":[{"from":[0,2],"to":[1,3],"color":"primary"},{"from":[1,3],"to":[2,3],"color":"green"}]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":470,"box":290,"title":"Prefix hashmap flow","steps":[{"type":"start","text":"freq[0] = 1\nprefix = 0\ncount = 0"},{"type":"decision","text":"more elements?","yes":"yes","branch":{"label":"no","text":"return count","role":"green"}},{"type":"process","text":"prefix += x"},{"type":"process","text":"count += freq[prefix - k]"},{"type":"process","text":"freq[prefix]++"},{"type":"end","text":"all endings counted"}]}
```

### 9. Walkthrough

| i | x | prefix | need | matches | count |
|---:|---:|---:|---:|---:|---:|
| — | — | 0 | — | — | 0 |
| 0 | 1 | 1 | -2 | 0 | 0 |
| 1 | 2 | 3 | 0 | 1 | 1 |
| 2 | 3 | 6 | 3 | 1 | 2 |
| 3 | -2 | 4 | 1 | 1 | 3 |
| 4 | 2 | 6 | 3 | 1 | 4 |

### 10. Why It Works

For every endpoint, the prefix equation is necessary and sufficient. The map contains exactly prior prefixes, and each occurrence corresponds to a distinct start. Updating after the query prevents the current prefix from serving as its own prior state.

### 11. Java

```java
long subarraySum(int[] nums, long k) {
    Map<Long, Integer> freq = new HashMap<>();
    freq.put(0L, 1);
    long prefix = 0;
    long count = 0;
    for (int x : nums) {
        prefix += x;
        count += freq.getOrDefault(prefix - k, 0);
        freq.put(prefix, freq.getOrDefault(prefix, 0) + 1);
    }
    return count;
}
```

### 12. Code Walkthrough

The empty prefix allows subarrays beginning at index 0. Frequencies, not mere existence, are required because equal prefix sums at different indices create distinct starts.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n) expected. **S:** O(n) for distinct prefix sums. `long` protects sums and answer count.

### 14. Edge Cases

`k = 0`, many zeros, negative values, empty array, and count larger than `Integer.MAX_VALUE`.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Using a `Set` undercounts. Updating `freq[prefix]` before querying can count a zero-length subarray when `k = 0`.

### 16. Optimization

Optimal for arbitrary integers. For non-negative arrays only, a sliding window may use less space.

### 17. Alternatives

Prefix array plus map, balanced tree for range inequalities, or sliding window for positive-only inputs.

### 18. Interview Follow-Ups

Longest subarray with sum `k`; subarrays divisible by `k`; 2D submatrix sum equals `k`; tree path-sum variant.

### 19. Variations

Binary subarrays with sum, continuous subarray sum modulo K, count subarrays with equal 0s and 1s via normalized prefix.

### 20. Pattern Connection

This is the canonical seen-before map: current state plus complementary prior state yields an answer ending now.

---

## Product of Array Except Self

!!! pattern "Pattern: Prefix/suffix products · T: O(n) · S: O(1) extra"
    **Signals:** answer for each index using all other elements, no division, associative operation with left/right contributions.

### 1. Problem

Given an integer array, return `ans[i] = product(nums[j])` for all `j != i`, without division. A production-safe Java version returns `long[]`.

### 2. Intuition

The product except `i` is `(product left of i) * (product right of i)`. Store left products in the output, then multiply by a right-running suffix.

### 3. Naive

For every index, multiply all other indices: O(n²).

```java
long[] productExceptSelfQuadratic(int[] nums) {
    long[] ans = new long[nums.length];
    for (int i = 0; i < nums.length; i++) {
        long product = 1;
        for (int j = 0; j < nums.length; j++) {
            if (i != j) product *= nums[j];
        }
        ans[i] = product;
    }
    return ans;
}
```

### 4. Key Observation

!!! key "Key observation"
    The current element is excluded by operation order: write the running prefix before multiplying by `nums[i]`, and multiply by the running suffix before updating it with `nums[i]`.

### 5. Pattern Recognition

**Signals.** "Except self," "all other positions," "no division," one answer per index.

**Shortcut.** Split the array around the index and combine left/right aggregate states.

**Related.** Prefix sums, prefix XOR, range queries, trapping rain water.

### 6. Invariant

After the left pass, `ans[i]` is product of elements left of `i`. During the right pass, `suffix` is product of elements right of `i` before `ans[i]` is multiplied.

### 7. Visual Explanation

```diagram
{"type":"array","title":"Split around the excluded index","values":[2,3,4,5],"highlights":{"0":"green","1":"green","2":"amber","3":"purple"},"pointers":[{"name":"i","index":2,"color":"amber","side":"top"}],"brackets":[{"from":0,"to":1,"label":"left = 6","color":"green","row":0},{"from":3,"to":3,"label":"right = 5","color":"purple","row":0}],"caption":"ans[2] = 6 · 5 = 30."}
```

```diagram
{"type":"dptable","title":"Two passes for [2,3,4,5]","corner":"state","col_head":["0","1","2","3"],"row_head":["nums","left pass","final"],"grid":[["2","3","4","5"],["1","2","6","24"],["60","40","30","24"]],"highlights":[[1,2,"green"],[2,2,"purple"]],"arrows":[{"from":[1,0],"to":[1,1],"color":"green"},{"from":[1,1],"to":[1,2],"color":"green"},{"from":[2,3],"to":[2,2],"color":"purple"},{"from":[2,2],"to":[2,1],"color":"purple"}]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":460,"box":280,"title":"Prefix/suffix product flow","steps":[{"type":"start","text":"ans = new long[n]\nprefix = 1"},{"type":"process","text":"for i left→right:\nans[i] = prefix\nprefix *= nums[i]"},{"type":"process","text":"suffix = 1"},{"type":"process","text":"for i right→left:\nans[i] *= suffix\nsuffix *= nums[i]"},{"type":"end","text":"return ans"}]}
```

### 9. Walkthrough

| pass | i | running before | write | running after |
|---|---:|---:|---:|---:|
| left | 0 | 1 | 1 | 2 |
| left | 1 | 2 | 2 | 6 |
| left | 2 | 6 | 6 | 24 |
| left | 3 | 24 | 24 | 120 |
| right | 3 | 1 | 24 | 5 |
| right | 2 | 5 | 30 | 20 |
| right | 1 | 20 | 40 | 60 |
| right | 0 | 60 | 60 | 120 |

### 10. Why It Works

For each index, all excluded-self factors lie strictly left or strictly right. The two passes compute exactly those factors without including `nums[i]`. Zeros need no branches because multiplication naturally propagates them.

### 11. Java

```java
long[] productExceptSelf(int[] nums) {
    long[] ans = new long[nums.length];
    long prefix = 1;
    for (int i = 0; i < nums.length; i++) {
        ans[i] = prefix;
        prefix *= nums[i];
    }
    long suffix = 1;
    for (int i = nums.length - 1; i >= 0; i--) {
        ans[i] *= suffix;
        suffix *= nums[i];
    }
    return ans;
}
```

### 12. Code Walkthrough

The output array is also prefix storage, so extra space is constant. Both running products are applied before incorporating the current element.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n) — two passes. **S:** O(1) extra, excluding output. Use `BigInteger` if products can exceed `long`.

### 14. Edge Cases

One zero, multiple zeros, negative values, empty array, and single element (`[1]` by empty product convention).

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Updating `prefix` or `suffix` before writing includes `nums[i]` in its own answer. Division fails with zeros and violates the constraint.

### 16. Optimization

Optimal without division. Division plus zero counting is a valid follow-up but less general.

### 17. Alternatives

Separate left/right arrays, division with zero cases, or parallel prefix scan.

### 18. Interview Follow-Ups

Return `int[]` under fit guarantees; generalize to other associative operations; support mutable updates.

### 19. Variations

Sum except self, XOR except self, left/right max precomputation for trapping rain water.

### 20. Pattern Connection

This is prefix/suffix decomposition: when the current index is excluded, compute the world on both sides.

---

## Longest Consecutive Sequence

### 1. Problem

Given an unsorted integer array, return the length of the longest run of consecutive values. Duplicates do not extend a run.

### 2. Key Observation

!!! key "Key observation"
    Store values in a set, but expand only from numbers with no predecessor. Each maximal run is traversed exactly once from its smallest value.

### 3. Invariant

When expanding from start `x`, every checked value belongs to the same maximal run. No interior value can start a second expansion because its predecessor exists.

### 4. Visual Explanation

```diagram
{"type":"array","title":"Only canonical starts expand","values":[100,4,200,1,3,2],"highlights":{"3":"green","5":"green","4":"green","1":"green"},"pointers":[{"name":"start: 1","index":3,"color":"green","side":"top"},{"name":"skip: 3 has 2","index":4,"color":"red","side":"bottom"}],"caption":"Hash membership discovers the logical run 1→2→3→4 even though positions are unsorted."}
```

### 5. Java

```java
int longestConsecutive(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int x : nums) set.add(x);
    int best = 0;
    for (int x : set) {
        if (x != Integer.MIN_VALUE && set.contains(x - 1)) continue;
        int len = 1;
        int cur = x;
        while (cur != Integer.MAX_VALUE && set.contains(cur + 1)) {
            cur++;
            len++;
        }
        best = Math.max(best, len);
    }
    return best;
}
```

### 6. Complexity

!!! complexity "Complexity"
    **T:** O(n) expected — every set value is expanded at most once as part of a run. **S:** O(n) for the set.

### 7. Edge Cases

Empty input returns 0. Duplicates collapse in the set. The implementation guards integer overflow around `x - 1` and `cur + 1`.

### 8. Pattern Connection

This is hash-set membership plus **canonical start detection**. The transfer: avoid duplicate work by launching traversal only from component roots.

---

## Maximum Product Subarray

### 1. Problem

Given an integer array, return the maximum product of a non-empty contiguous subarray. Values can be positive, negative, or zero.

### 2. Key Observation

!!! key "Key observation"
    A negative value can turn the smallest product into the largest. Track both `maxEndingHere` and `minEndingHere`; the next extrema come from `x`, `x * previousMax`, and `x * previousMin`.

### 3. Invariant

After index `i`, `maxEnding` is the largest product of a subarray ending at `i`, `minEnding` is the smallest, and `best` is the largest product over all processed endpoints.

### 4. Visual Explanation

```diagram
{"type":"dptable","title":"Carry both extremes because signs flip","corner":"i","col_head":["0","1","2","3"],"row_head":["x","maxEnd","minEnd","best"],"grid":[["2","3","-2","4"],["2","6","-2","4"],["2","3","-12","-48"],["2","6","6","6"]],"highlights":[[1,1,"green"],[2,2,"red"],[3,2,"purple"]],"arrows":[{"from":[1,1],"to":[2,2],"color":"red"},{"from":[2,2],"to":[1,3],"color":"green"}]}
```

### 5. Java

```java
long maxProduct(int[] nums) {
    if (nums.length == 0) throw new IllegalArgumentException("nums must be non-empty");
    long maxEnding = nums[0];
    long minEnding = nums[0];
    long best = nums[0];
    for (int i = 1; i < nums.length; i++) {
        long x = nums[i];
        long a = maxEnding * x;
        long b = minEnding * x;
        maxEnding = Math.max(x, Math.max(a, b));
        minEnding = Math.min(x, Math.min(a, b));
        best = Math.max(best, maxEnding);
    }
    return best;
}
```

### 6. Complexity

!!! complexity "Complexity"
    **T:** O(n) — one pass. **S:** O(1) — two endpoint states plus answer. `long` reduces overflow risk; use `BigInteger` for unbounded products.

### 7. Edge Cases

Zeros reset both extrema naturally because `x` itself is always a candidate. All-negative arrays work because the minimum may become maximum after another negative. Initialize from the first element to preserve non-empty semantics.

### 8. Pattern Connection

This is Kadane with richer state. When the transition can reverse ordering, carry the companion worst state because it may become the next best.
