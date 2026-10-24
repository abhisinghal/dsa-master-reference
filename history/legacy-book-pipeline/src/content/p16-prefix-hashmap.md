## The Pattern

Prefix Sum + HashMap converts a subarray-sum question into a difference of two prefixes. At index `i`, if `prefix[i] - prefix[j] == k`, then the subarray `(j + 1)..i` sums to `k`. The map stores previously seen prefixes as counts for counting problems or first indices for longest/shortest range problems.

!!! pattern "Recognition signals"
    You need contiguous subarrays with a target sum/count, values may be negative, and sliding-window monotonicity is not guaranteed. Look for equations of the form `currentPrefix - priorPrefix = target`.

```diagram
{"type":"array","values":[0,2,3,2,5,7],"index":["p0","p1","p2","p3","p4","p5"],"highlights":{"1":"amber","4":"green"},"brackets":[{"from":1,"to":4,"label":"prefix 5 - prefix 2 = 3 => nums[1..3]","color":"green","row":0}],"caption":"A target subarray is the difference between two prefix sums, not necessarily a monotone window."}
```

## The Invariant

Before processing `nums[i]`, the map summarizes all prefix sums ending before `i`. After adding `nums[i]`, every prior prefix equal to `prefix - k` defines one subarray ending at `i` with sum `k`. Then insert the current prefix so future positions can use it.

## Template

```java
int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> countByPrefix = new HashMap<>();
    countByPrefix.put(0, 1);

    int prefix = 0;
    int ans = 0;
    for (int x : nums) {
        prefix += x;
        ans += countByPrefix.getOrDefault(prefix - k, 0);
        countByPrefix.merge(prefix, 1, Integer::sum);
    }
    return ans;
}
```

For longest length, store `firstIndexByPrefix.putIfAbsent(prefix, i)` and test `prefix - k`; for exact counts, store frequencies because multiple equal prefixes create multiple valid starts.

## Worked Recognition

- **Subarray Sum Equals K (Modules 2/14)**: the canonical count problem. Initialize prefix `0` with count 1 so subarrays starting at index 0 are counted naturally.
- **Sliding Window (Pattern 1)** contrast: a two-pointer window works for non-negative arrays because expanding increases sum and shrinking decreases it. Negative values break that monotonicity; prefix differences still work.
- **Zero-sum and equal-count variants**: set `k = 0`, or transform categories to `+1/-1` and reuse the same prefix-index invariant.

## Complexity

!!! complexity "Complexity"
    **T:** O(n) expected with a hash map. **S:** O(n) distinct prefix sums in the worst case. Use `long` for `prefix` when values or length can overflow `int`.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Updating the map before counting, which accidentally allows empty subarrays; forgetting the initial `{0:1}`; using sliding window with negative numbers; or storing only one index when the question asks for the number of subarrays.

## When NOT to use it

Do not use this pattern when the array is all non-negative and the task asks for minimal/longest window under inequalities, where sliding window is simpler and O(1) space. For many offline range-sum queries on immutable data, a plain prefix array may be enough.
