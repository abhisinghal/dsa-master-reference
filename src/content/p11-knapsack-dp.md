## The Pattern

Knapsack DP solves "choose items under a capacity-like constraint" by making the capacity part of the state. The core move is binary: skip the item or pick it if it fits. The decisive distinction is whether picking consumes the item forever (**0/1 knapsack**) or leaves it available again (**unbounded knapsack**).

!!! pattern "Recognition signals"
    **Signals:** target sum, capacity, budget, "use each at most once", "use unlimited coins", maximize value under weight, count ways to reach an amount, or decide whether a subset reaches half the total.

```diagram
{"type":"dptable","corner":"item\\cap","col_head":["0","1","2","3","4","5","6"],"row_head":["∅","w2/v4","w3/v5","w4/v6"],"grid":[["0","0","0","0","0","0","0"],["0","0","4","4","4","4","4"],["0","0","4","5","5","9","9"],["0","0","4","5","6","9","10"]],"highlights":[[3,6,"green"],[2,6,"primary"],[2,2,"amber"]],"arrows":[{"from":[2,6],"to":[3,6],"color":"primary"},{"from":[2,2],"to":[3,6],"color":"amber"}]}
```

## The Invariant

**STATE:** for 0/1 max-value knapsack, `dp[i][c]` is the best value using only the first `i` items with capacity `c`. For decision/counting variants, replace "best value" with "reachable?" or "number of ways."

**TRANSITION:** skip or pick: `dp[i][c] = dp[i - 1][c]`; if `w <= c`, also consider `value + dp[i - 1][c - w]`. For unbounded knapsack, picking stays on the same item layer conceptually: `value + dp[i][c - w]`.

**BASE CASE:** `dp[0][c] = 0` for max value, `reachable[0] = true` for subset sum, and `ways[0] = 1` for counting. Impossible states should remain false, 0 ways, or -∞ depending on the objective.

## Template

```java
int zeroOneKnapsack(int[] weight, int[] value, int capacity) {
    int[] dp = new int[capacity + 1];
    for (int i = 0; i < weight.length; i++) {
        int w = weight[i], v = value[i];
        for (int c = capacity; c >= w; c--) {
            dp[c] = Math.max(dp[c], v + dp[c - w]);
        }
    }
    return dp[capacity];
}

int unboundedKnapsack(int[] weight, int[] value, int capacity) {
    int[] dp = new int[capacity + 1];
    for (int i = 0; i < weight.length; i++) {
        int w = weight[i], v = value[i];
        for (int c = w; c <= capacity; c++) {
            dp[c] = Math.max(dp[c], v + dp[c - w]);
        }
    }
    return dp[capacity];
}
```

## Worked Recognition

- **Coin Change** (Module 12): amount is capacity; coins are items. Minimum coins uses `min`, impossible states as large sentinels, and unbounded forward iteration because a coin may be reused.
- **Partition Equal Subset Sum** (Module 12): target is `sum / 2`; each number is usable once. The 1D boolean DP must iterate capacity backward or the same number can be used multiple times.
- **0/1 value maximization** (Module 12 family): the pick/skip recurrence is literal. If the interviewer asks for chosen items, keep parent decisions or reconstruct from a 2D table.

## Complexity

!!! complexity "Complexity"
    **T:** O(nC), where C is the numeric capacity/target, not the input length. **S:** O(nC) for a full table or O(C) with rolling 1D DP. This is pseudo-polynomial: excellent for bounded targets, unsuitable when C is huge.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Iterating 0/1 capacity forward, which silently turns the solution unbounded; initializing all counting states to 1; confusing combinations with permutations in coin-change loops; and using `int` for counts when the number of ways can overflow.

## When NOT to use it

Avoid knapsack DP when capacity is enormous, weights are real-valued, constraints require ordering/adjacency rather than set choice, or a greedy proof exists. Meet-in-the-middle can beat O(nC) when n is small and C is too large.
