## The Pattern

Bitmasking represents a subset of a small universe as an integer: bit `i` is 1 iff item `i` is present. That makes membership, add, remove, toggle, and subset iteration constant-time primitive operations, and it enables DP keyed by visited sets.

!!! pattern "Recognition signals"
    The problem says "subset," "visited set," "choose any combination," "state is a set of indices," or `n <= ~20`. If a `HashSet<Integer>` appears in every recursive state, ask whether an `int` or `long` mask is the real state.

```diagram
{"type":"array","values":[1,0,1,1,0],"index":["4","3","2","1","0"],"highlights":{"0":"green","2":"green","3":"green"},"brackets":[{"from":0,"to":4,"label":"mask 10110 => {1,2,4}","color":"green","row":0}],"caption":"Read bit positions right-to-left: bits 1, 2, and 4 are set."}
```

## The Invariant

For universe `0..n-1`, `mask` is the complete set state: `(mask & (1 << i)) != 0` iff `i` is currently included/visited. Any transition must update only the bit that corresponds to the chosen item, so the integer and conceptual set never diverge.

## Template

```java
List<List<Integer>> subsets(int[] nums) {
    int n = nums.length;
    List<List<Integer>> ans = new ArrayList<>();
    for (int mask = 0; mask < (1 << n); mask++) {
        List<Integer> subset = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) subset.add(nums[i]);
        }
        ans.add(subset);
    }
    return ans;
}

for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
    // sub visits every non-empty submask of mask exactly once
}
```

Bitmask DP uses the same identity with a value table:

```java
int full = 1 << n;
int[][] dp = new int[full][n]; // dp[mask][last]
for (int[] row : dp) Arrays.fill(row, INF);
for (int i = 0; i < n; i++) dp[1 << i][i] = 0;
for (int mask = 0; mask < full; mask++) {
    for (int last = 0; last < n; last++) {
        if (dp[mask][last] == INF) continue;
        for (int next = 0; next < n; next++) {
            if ((mask & (1 << next)) != 0) continue;
            int nextMask = mask | (1 << next);
            dp[nextMask][next] = Math.min(dp[nextMask][next], dp[mask][last] + cost[last][next]);
        }
    }
}
```

## Worked Recognition

- **Power Set (Module 1)**: each integer from `0` to `2^n - 1` is one subset. This is the cleanest way to enumerate all subsets when order of generation is irrelevant.
- **Single Number (Module 1)**: XOR is the one-bit parity version of the same model: each bit position is tracked independently, and duplicate contributions cancel.
- **TSP-style visited-state DP**: when the state is "which nodes have been visited and where am I now?", `dp[mask][last]` replaces expensive set objects with dense arrays.

## Complexity

!!! complexity "Complexity"
    **T:** subset enumeration is O(n · 2^n); iterating all submasks of one mask is O(2^k) for `k` set bits; classic `dp[mask][last]` with transitions to `next` is O(n^2 · 2^n). **S:** O(2^n) or O(n · 2^n) for DP tables.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Writing `1 << n` when `n >= 31` for `int`, forgetting parentheses around bit tests, treating bit order as array order inconsistently, or using bitmask DP when `n` is too large for `2^n` memory.

## When NOT to use it

Do not use bitmasking when the universe is unbounded, sparse, or mostly strings/objects; when `n` exceeds roughly 20–24 for exponential DP; or when a greedy/counting invariant avoids enumerating sets entirely.
