## Concepts & Mental Models

Dynamic programming is disciplined reuse: name a repeated subproblem, solve it once, and make every larger answer depend only on already-solved smaller answers. The point is not memorizing famous arrays; it is learning to derive a recurrence from the shape of the choices.

!!! key "The DP recipe"
    Before code, write **STATE** (what a cell means), **TRANSITION** (the equation), **BASE CASE** (known smallest states), and **ORDER** (the fill order that satisfies dependencies). If one of these is fuzzy, the implementation will be fragile.

DP is justified by two properties. **Overlapping subproblems** means brute force asks the same question many times: `rob(i)`, `coins(a)`, `lcs(i,j)`, `solve(l,r)`. **Optimal substructure** means an optimal large answer can be composed from optimal smaller answers without remembering the whole history.

**Memoization** is top-down: write the recursion first and cache states on demand. It is natural for trees, intervals, and sparse state spaces. **Tabulation** is bottom-up: fill states in dependency order. It is usually easier to space-optimize and easier to audit in interviews. **State compression** is legal only when the recurrence reads a bounded frontier; compress after the full table is correct.

!!! pattern "Pattern: DP state design"
    **Signals:** choose/skip decisions, prefixes of strings, target amounts, capacities, grid cells, tree subproblems, intervals, or state machines; words like "minimum", "maximum", "count ways", "can form", or "best profit" under constraints.

### The DP thought process

1. Start with a recursive question: `f(state) = answer for this smaller problem`.
2. Choose parameters that make the future independent of the past.
3. Classify the last choice, first choice, or current status; write the equation.
4. Pin down empty prefixes, zero amount, borders, null nodes, or length-0 intervals.
5. Draw dependency arrows; the arrows determine loop order.
6. Only then compress memory, preserving the same dependency graph.

```diagram
{"type":"flow","title":"DP derivation loop","width":520,"box":260,"steps":[{"type":"start","text":"Define f(state)"},{"type":"process","text":"Classify the decision"},{"type":"process","text":"Write transition equation"},{"type":"process","text":"Set base cases"},{"type":"decision","text":"Dependencies already solved?","yes":"tabulate / memoize","branch":{"label":"no","text":"change order or state","role":"red"}},{"type":"end","text":"compress if safe"}]}
```

```diagram
{"type":"dptable","corner":"state","col_head":["base","...","answer"],"row_head":["subproblem"],"grid":[["known","→","derive"]],"highlights":[[0,0,"green"],[0,2,"primary"]],"arrows":[{"from":[0,0],"to":[0,1],"color":"green"},{"from":[0,1],"to":[0,2],"color":"green"}]}
```

---

## Climbing Stairs & House Robber (1D DP)

### Climbing Stairs — condensed

!!! pattern "Pattern: Fibonacci 1D DP · T: O(n) · S: O(1)"
    **Signals:** reach position `i` from a fixed set of previous positions; count ways.

#### Problem

Climb `n` steps, taking 1 or 2 steps at a time. Count distinct ways.

#### State/Transition

**STATE:** `dp[i]` = ways to stand on step `i`. **TRANSITION:** `dp[i] = dp[i-1] + dp[i-2]`. **BASE:** `dp[0]=1`, `dp[1]=1`. **ORDER:** increasing `i`.

#### Key Observation

!!! key "Key observation"
    Partition paths by the final move. A path to `i` ends with either a 1-step move from `i-1` or a 2-step move from `i-2`; these sets are disjoint, so counts add.

```diagram
{"type":"dptable","corner":"i","col_head":["0","1","2","3","4","5"],"row_head":["ways"],"grid":[[1,1,2,3,5,8]],"highlights":[[0,4,"primary"],[0,3,"green"],[0,2,"amber"]],"arrows":[{"from":[0,3],"to":[0,4],"color":"green"},{"from":[0,2],"to":[0,4],"color":"amber"}]}
```

#### Java

```java
int climbStairs(int n) {
    int prev2 = 1, prev1 = 1;
    for (int i = 2; i <= n; i++) {
        int cur = prev1 + prev2;
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
```

#### Complexity

!!! complexity "Complexity"
    **T:** O(n). **S:** O(1).

#### Pattern Connection

This is the seed of 1D DP: the index is the state, the last move gives the recurrence, and a fixed-width dependency window enables rolling variables.

### House Robber

!!! pattern "Pattern: 1D choose/skip DP · T: O(n) · S: O(1)"
    **Signals:** choose numbers from a line; adjacent choices are incompatible; maximize total.

#### 1. The Problem

Given non-negative `nums[i]` representing money in house `i`, return the maximum money you can rob without robbing adjacent houses.

#### 2. The Intuition

At house `i`, either skip it and keep the best prefix through `i-1`, or rob it and combine its value with the best prefix through `i-2`. The adjacency constraint is local, so two previous prefix optima summarize all relevant history.

#### 3. The Naive Approach

Backtracking branches into rob/skip at each house: `best(i)=max(best(i+1), nums[i]+best(i+2))`. Without caching, the recursion tree is exponential because the same suffix index is reached through many paths.

#### 4. The Key Observation 🔑

!!! key "Key observation"
    The final decision for prefix `0..i` is exhaustive: either house `i` is excluded (`dp[i-1]`) or included (`dp[i-2] + nums[i]`). Thus `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`.

#### 5. Pattern Recognition

**Signals.** "No adjacent", "choose subset from a line", "maximize sum". **Shortcut.** If taking `i` only forbids `i-1`, keep the best results ending one and two positions back. **Related.** Delete and Earn, weighted independent set on a path, House Robber II/III.

#### 6. The Invariant

After processing house `i`, `prev1` is the optimal value for houses `0..i`, and `prev2` is the optimal value for `0..i-1` before the update. The transition evaluates the only two legal statuses of the current house.

**STATE:** `dp[i]` = max money from houses `0..i`. **TRANSITION:** `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`. **BASE CASE:** `dp[-1]=0`, `dp[0]=nums[0]`. **ORDER:** left to right.

#### 7. Visual Explanation

```diagram
{"type":"dptable","corner":"i","col_head":["0","1","2","3","4"],"row_head":["nums","dp"],"grid":[[2,7,9,3,1],[2,7,11,11,12]],"highlights":[[1,4,"primary"],[1,3,"amber"],[1,2,"green"],[0,4,"green"]],"arrows":[{"from":[1,3],"to":[1,4],"color":"amber"},{"from":[1,2],"to":[1,4],"color":"green"},{"from":[0,4],"to":[1,4],"color":"green"}]}
```

```diagram
{"type":"flow","title":"House Robber rolling DP","width":460,"box":250,"steps":[{"type":"start","text":"prev2 = 0, prev1 = 0"},{"type":"decision","text":"more houses?","yes":"yes","branch":{"label":"no","text":"return prev1","role":"green"}},{"type":"process","text":"cur = max(prev1, prev2 + nums[i])"},{"type":"process","text":"prev2 = prev1\nprev1 = cur"}]}
```

#### 8. Algorithm Flow Diagram

The flow is the compressed version of the table: compute the current prefix optimum from the two previous prefix optima, then slide the window.

#### 9. Step-by-Step Walkthrough

For `[2,7,9,3,1]`:

| i | value | take | skip | best |
|---|---:|---:|---:|---:|
| 0 | 2 | 2 | 0 | 2 |
| 1 | 7 | 7 | 2 | 7 |
| 2 | 9 | 11 | 7 | 11 |
| 3 | 3 | 10 | 11 | 11 |
| 4 | 1 | 12 | 11 | 12 |

#### 10. Why It Works

By induction on the prefix. Any optimal solution for `0..i` either excludes `i`, reducing to the optimal solution for `0..i-1`, or includes `i`, forcing exclusion of `i-1` and reducing to `0..i-2`. The recurrence chooses the better exhaustive case.

#### 11. Java Implementation

```java
int rob(int[] nums) {
    int prev2 = 0, prev1 = 0;
    for (int money : nums) {
        int cur = Math.max(prev1, prev2 + money);
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
```

#### 12. Code Walkthrough

`prev1` is `dp[i-1]`; `prev2` is `dp[i-2]`. Initial zeros implement virtual empty prefixes and handle an empty array.

#### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n). **S:** O(1).

#### 14. Edge Cases

Empty input returns 0 if allowed; one house returns its value; two houses return their max; all zeros return 0.

#### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Greedy local choice fails on `[2,1,1,2]`. Also update the rolling variables in the right order: the old `prev1` becomes the new `prev2`.

#### 16. Optimization

The rolling version is the optimized tabulation. Keep a full table only if reconstructing selected house indices.

#### 17. Alternatives

Top-down memoization mirrors the decision tree:

```java
int robMemo(int[] nums) {
    Integer[] memo = new Integer[nums.length];
    return best(nums, 0, memo);
}

int best(int[] nums, int i, Integer[] memo) {
    if (i >= nums.length) return 0;
    if (memo[i] != null) return memo[i];
    memo[i] = Math.max(best(nums, i + 1, memo), nums[i] + best(nums, i + 2, memo));
    return memo[i];
}
```

#### 18. Interview Follow-Ups

Circular houses: solve two paths excluding first or last. Tree houses: return rob/skip states per node. Chosen houses: store parent decisions.

#### 19. Variations

Delete and Earn, maximum non-adjacent subsequence sum, weighted independent set on a path, and cooldown-like scheduling.

#### 20. Pattern Connection

House Robber is canonical choose/skip DP: local incompatibility means a small frontier summarizes the entire prefix.

---

## Decode Ways (1D with constraints)

!!! pattern "Pattern: constrained 1D counting DP · T: O(n) · S: O(1)"
    **Signals:** parse a string as one- or two-character tokens; invalid zeros; count interpretations.

### Problem

Given digits where `1 -> A` through `26 -> Z`, return the number of decodings. `0` cannot stand alone.

### State/Transition

**STATE:** `dp[i]` = decodings of prefix length `i`. **TRANSITION:** add `dp[i-1]` if `s[i-1]` is `1..9`; add `dp[i-2]` if `s[i-2..i-1]` is `10..26`. **BASE:** `dp[0]=1`, and `dp[1]=1` only when first char is not `0`. **ORDER:** increasing `i`.

### Key Observation

!!! key "Key observation"
    Count by the final token. The token has length one or two, but contributes only if valid. Zeros are not special states; they simply invalidate the one-character edge unless paired as `10` or `20`.

```diagram
{"type":"dptable","corner":"i","col_head":["0","1","2","3","4"],"row_head":["prefix","dp"],"grid":[["","2","22","226","2260"],[1,1,2,3,0]],"highlights":[[1,3,"primary"],[1,2,"green"],[1,1,"amber"],[1,4,"red"]],"arrows":[{"from":[1,2],"to":[1,3],"color":"green"},{"from":[1,1],"to":[1,3],"color":"amber"}]}
```

### Java

```java
int numDecodings(String s) {
    if (s == null || s.isEmpty() || s.charAt(0) == '0') return 0;
    int prev2 = 1, prev1 = 1;
    for (int i = 2; i <= s.length(); i++) {
        int cur = 0;
        if (s.charAt(i - 1) != '0') cur += prev1;
        int two = (s.charAt(i - 2) - '0') * 10 + (s.charAt(i - 1) - '0');
        if (two >= 10 && two <= 26) cur += prev2;
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n). **S:** O(1).

### Pattern Connection

Decode Ways is Climbing Stairs with guarded edges: the recurrence shape is identical, but validity constraints remove illegal transitions.

---

## Coin Change (unbounded, min coins)

!!! pattern "Pattern: unbounded min-count DP · T: O(amount × coins) · S: O(amount)"
    **Signals:** unlimited reuse of denominations; exact target; minimize item count.

### 1. The Problem

Given coin denominations and a target `amount`, return the fewest coins needed to make exactly that amount, or `-1` if impossible. Each coin may be used unlimited times.

### 2. The Intuition

Ask what the last coin was. If the final coin has value `c`, the previous amount was `a-c`; therefore the best way to make `a` is one more than the best reachable previous amount.

### 3. The Naive Approach

Recursive search tries every coin at every remaining amount: `f(a)=1+min(f(a-c))`. Without memoization, the same remaining amount is recomputed through many coin orders.

### 4. The Key Observation 🔑

!!! key "Key observation"
    The state is the amount, not the sequence of coins. Different orders that leave the same remaining amount have identical futures, so one `dp[a]` is sufficient.

### 5. Pattern Recognition

**Signals.** "Minimum coins", "unlimited", "exact sum". **Shortcut.** If the last reusable item can be any denomination, use a 1D amount DP. **Related.** Perfect Squares, minimum tickets, shortest path on implicit amount graph.

### 6. The Invariant

After filling amount `a`, every `dp[x]` for `x <= a` is the minimum number of coins for `x`. Every transition to `a` reads `a-c`, a smaller amount that is already final.

**STATE:** `dp[a]` = min coins for amount `a`. **TRANSITION:** `dp[a] = min(dp[a], dp[a-c] + 1)` for each coin `c <= a` where `dp[a-c]` is reachable. **BASE CASE:** `dp[0]=0`, positive amounts start at infinity. **ORDER:** increasing amount.

### 7. Visual Explanation

```diagram
{"type":"dptable","corner":"amount","col_head":["0","1","2","3","4","5","6"],"row_head":["dp"],"grid":[[0,1,2,1,1,2,2]],"highlights":[[0,6,"primary"],[0,5,"green"],[0,3,"amber"],[0,2,"purple"]],"arrows":[{"from":[0,5],"to":[0,6],"color":"green"},{"from":[0,3],"to":[0,6],"color":"amber"},{"from":[0,2],"to":[0,6],"color":"purple"}]}
```

```diagram
{"type":"flow","title":"Coin Change tabulation","width":470,"box":250,"steps":[{"type":"start","text":"dp[0]=0; others=∞"},{"type":"process","text":"for amount a = 1..target"},{"type":"process","text":"try every coin c <= a"},{"type":"decision","text":"dp[a-c] reachable?","yes":"relax dp[a]","branch":{"label":"no","text":"next coin","role":"red"}},{"type":"end","text":"return dp[target] or -1"}]}
```

### 8. Algorithm Flow Diagram

This is shortest-path relaxation over amounts: an edge of cost 1 goes from `a-c` to `a`. Increasing amount order works because all edges point from smaller to larger amounts.

### 9. Step-by-Step Walkthrough

For `coins=[1,3,4]`, `amount=6`: `dp[0]=0`, `dp[1]=1`, `dp[2]=2`, `dp[3]=1`, `dp[4]=1`, `dp[5]=2`, `dp[6]=2` via `3+3`.

### 10. Why It Works

Every valid solution for `a` has a final coin `c`; removing it leaves a valid solution for `a-c`, so the optimum is at least one of the candidate transitions. Conversely, any reachable `dp[a-c]` plus coin `c` forms amount `a`. Minimizing over all coins is exact.

### 11. Java Implementation

```java
int coinChange(int[] coins, int amount) {
    int inf = amount + 1;
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, inf);
    dp[0] = 0;
    for (int a = 1; a <= amount; a++) {
        for (int c : coins) {
            if (c <= a && dp[a - c] != inf) {
                dp[a] = Math.min(dp[a], dp[a - c] + 1);
            }
        }
    }
    return dp[amount] == inf ? -1 : dp[amount];
}
```

### 12. Code Walkthrough

`amount + 1` is a safe sentinel larger than any possible valid coin count. The amount loop guarantees the source state `a-c` has already been computed.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(amount × coins). **S:** O(amount). This is pseudo-polynomial in the numeric amount.

### 14. Edge Cases

`amount=0` returns 0; unreachable targets return `-1`; duplicate denominations waste work but do not affect correctness.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Initializing unreachable states to 0 makes impossible amounts look free. Also remember to convert the sentinel to `-1` at the end.

### 16. Optimization

Sort coins and break when `c > a` to reduce constants. BFS over amounts can stop early, but tabulation is simpler and deterministic.

### 17. Alternatives

Memoization is useful when many amounts are unreachable:

```java
int coinChangeMemo(int[] coins, int amount) {
    int[] memo = new int[amount + 1];
    Arrays.fill(memo, Integer.MIN_VALUE);
    return minCoins(coins, amount, memo);
}

int minCoins(int[] coins, int rem, int[] memo) {
    if (rem == 0) return 0;
    if (rem < 0) return -1;
    if (memo[rem] != Integer.MIN_VALUE) return memo[rem];
    int best = Integer.MAX_VALUE;
    for (int c : coins) {
        int sub = minCoins(coins, rem - c, memo);
        if (sub >= 0) best = Math.min(best, sub + 1);
    }
    memo[rem] = best == Integer.MAX_VALUE ? -1 : best;
    return memo[rem];
}
```

### 18. Interview Follow-Ups

Return one optimal combination by storing predecessor coins; count combinations instead of minimizing; add limited coin counts to get bounded knapsack.

### 19. Variations

Perfect Squares, minimum travel tickets, least dictionary words to form a prefix, and shortest cost over integer states.

### 20. Pattern Connection

Coin Change is unbounded knapsack with a min objective. Reuse is encoded by reading the same 1D table at smaller amounts.

---

## Coin Change II (count ways) & Partition Equal Subset Sum & 0/1 Knapsack

### Coin Change II — condensed

!!! pattern "Pattern: unbounded combination counting · T: O(amount × coins) · S: O(amount)"
    **Signals:** count combinations, unlimited coins, order of coins should not create new answers.

#### Problem

Return how many combinations form `amount` using unlimited coins.

#### State/Transition

**STATE:** `dp[a]` = combinations for amount `a` using coin types processed so far. **TRANSITION:** for each coin `c`, for `a=c..amount`, `dp[a] += dp[a-c]`. **BASE:** `dp[0]=1`. **ORDER:** coins outer, amounts increasing.

#### Key Observation

!!! key "Key observation"
    Loop order prevents permutation counting. Coins outer builds combinations in coin-type order; amount outer would count `[1,2]` and `[2,1]` separately.

```diagram
{"type":"dptable","corner":"amount","col_head":["0","1","2","3","4","5"],"row_head":["after 1","after 2","after 5"],"grid":[[1,1,1,1,1,1],[1,1,2,2,3,3],[1,1,2,2,3,4]],"highlights":[[2,5,"primary"],[1,5,"amber"],[2,0,"green"]],"arrows":[{"from":[1,5],"to":[2,5],"color":"amber"},{"from":[2,0],"to":[2,5],"color":"green"}]}
```

#### Java

```java
int change(int amount, int[] coins) {
    int[] dp = new int[amount + 1];
    dp[0] = 1;
    for (int c : coins) {
        for (int a = c; a <= amount; a++) {
            dp[a] += dp[a - c];
        }
    }
    return dp[amount];
}
```

#### Complexity

!!! complexity "Complexity"
    **T:** O(amount × coins). **S:** O(amount).

#### Pattern Connection

Same unbounded amount state as Coin Change, but the objective changes from minimum to counting and the loop order encodes combination semantics.

### Partition Equal Subset Sum — condensed

!!! pattern "Pattern: 0/1 subset-sum feasibility · T: O(n × sum) · S: O(sum)"
    **Signals:** split into equal sums; each number used once; boolean feasibility.

#### Problem

Return whether `nums` can be partitioned into two subsets with equal sum.

#### State/Transition

If total is odd, return false. Let `target=total/2`. **STATE:** `dp[s]` = whether some processed subset sums to `s`. **TRANSITION:** `dp[s] = dp[s] || dp[s-x]`. **BASE:** `dp[0]=true`. **ORDER:** for each number, scan `s` downward to avoid reuse.

#### Key Observation

!!! key "Key observation"
    It is enough to find one subset with half the total; the complement automatically has the other half.

```diagram
{"type":"dptable","corner":"sum","col_head":["0","1","2","3","4","5","6"],"row_head":["start","use 1","use 5"],"grid":[[true,false,false,false,false,false,false],[true,true,false,false,false,false,false],[true,true,false,false,false,true,true]],"highlights":[[2,6,"primary"],[1,1,"green"],[1,6,"amber"]],"arrows":[{"from":[1,1],"to":[2,6],"color":"green"},{"from":[1,6],"to":[2,6],"color":"amber"}]}
```

#### Java

```java
boolean canPartition(int[] nums) {
    int total = 0;
    for (int x : nums) total += x;
    if ((total & 1) == 1) return false;
    int target = total / 2;
    boolean[] dp = new boolean[target + 1];
    dp[0] = true;
    for (int x : nums) {
        for (int s = target; s >= x; s--) {
            dp[s] = dp[s] || dp[s - x];
        }
    }
    return dp[target];
}
```

#### Complexity

!!! complexity "Complexity"
    **T:** O(n × target). **S:** O(target).

#### Pattern Connection

This is boolean 0/1 knapsack. Descending capacity is the proof that each number is used at most once.

### 0/1 Knapsack

!!! pattern "Pattern: 0/1 capacity DP · T: O(n × W) · S: O(W)"
    **Signals:** each item chosen at most once; capacity constraint; maximize value.

#### 1. The Problem

Given weights `wt`, values `val`, and capacity `W`, choose a subset of items with total weight at most `W` and maximum value. Each item may be selected once.

#### 2. The Intuition

For each item, choose or skip. If chosen, capacity decreases and value increases, but the remaining value must come only from earlier items.

#### 3. The Naive Approach

Enumerating subsets costs O(2^n). Pruning cannot remove the worst case because close weights and values can make many subsets plausible.

#### 4. The Key Observation 🔑

!!! key "Key observation"
    The future is determined by `(items considered, remaining capacity)`, not by the exact subset history. That yields a rectangular DP table.

#### 5. Pattern Recognition

**Signals.** "At most once", "capacity", "maximize". **Shortcut.** If item reuse is forbidden, transitions for item `i` must read previous-row states. **Related.** Partition Equal Subset Sum, Target Sum, Ones and Zeroes.

#### 6. The Invariant

After processing the first `i` items, `dp[w]` in the compressed version is the best value with capacity `w` using only those items. Descending `w` keeps `dp[w-wt[i]]` from the previous item frontier.

**STATE:** `dp[i][w]` = max value using first `i` items with capacity `w`. **TRANSITION:** `dp[i][w]=max(dp[i-1][w], dp[i-1][w-wt[i-1]]+val[i-1])` when the item fits. **BASE CASE:** row 0 and capacity 0 are 0. **ORDER:** increasing item; descending capacity for 1D.

#### 7. Visual Explanation

```diagram
{"type":"dptable","corner":"i\\w","col_head":["0","1","2","3","4","5"],"row_head":["0 items","w2 v3","w3 v4","w4 v5"],"grid":[[0,0,0,0,0,0],[0,0,3,3,3,3],[0,0,3,4,4,7],[0,0,3,4,5,7]],"highlights":[[2,5,"primary"],[1,5,"amber"],[1,2,"green"]],"arrows":[{"from":[1,5],"to":[2,5],"color":"amber"},{"from":[1,2],"to":[2,5],"color":"green"}]}
```

```diagram
{"type":"flow","title":"0/1 Knapsack compressed loop","width":470,"box":250,"steps":[{"type":"start","text":"dp[w] = 0"},{"type":"process","text":"for each item"},{"type":"process","text":"for w = W down to weight"},{"type":"process","text":"dp[w] = max(dp[w], dp[w-weight] + value)"},{"type":"end","text":"return dp[W]"}]}
```

#### 8. Algorithm Flow Diagram

Descending capacity is the compressed equivalent of reading from row `i-1`; upward capacity would allow the current item to feed itself.

#### 9. Step-by-Step Walkthrough

For weights `[2,3,4]`, values `[3,4,5]`, `W=5`: item 1 gives value 3 for capacities 2..5; item 2 combines with capacity 2 to give 7 at capacity 5; item 3 improves capacity 4 to 5 but leaves capacity 5 at 7.

#### 10. Why It Works

Any optimal subset among first `i` items either excludes item `i-1` or includes it. Exclusion gives `dp[i-1][w]`; inclusion gives the best previous subset fitting `w-wt` plus the item's value. These cases are exhaustive.

#### 11. Java Implementation

```java
int knapsack01(int[] wt, int[] val, int W) {
    int[] dp = new int[W + 1];
    for (int i = 0; i < wt.length; i++) {
        for (int w = W; w >= wt[i]; w--) {
            dp[w] = Math.max(dp[w], dp[w - wt[i]] + val[i]);
        }
    }
    return dp[W];
}
```

#### 12. Code Walkthrough

`dp[w]` is the skip case before assignment. Since `w` descends, `dp[w-wt[i]]` still excludes the current item, so adding `val[i]` uses it exactly once.

#### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n × W). **S:** O(W), compressed from O(n × W).

#### 14. Edge Cases

`W=0` returns 0; too-heavy items are naturally skipped; zero-weight positive-value items need explicit variant rules.

#### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Iterating capacity upward changes the problem into unbounded knapsack by reusing the same item multiple times.

#### 16. Optimization

Use 1D for value only. To reconstruct selected items, keep a parent table or full 2D table.

#### 17. Alternatives

When capacity is huge but total value is small, invert the DP: store the minimum weight needed to achieve each value.

#### 18. Interview Follow-Ups

Unbounded items use upward capacity; exact-fill variants initialize impossible states to negative infinity; counting variants replace max with addition.

#### 19. Variations

Target Sum, Last Stone Weight II, Ones and Zeroes, subset sum, and budgeted selection.

#### 20. Pattern Connection

0/1 Knapsack is the parent resource-allocation DP. Loop direction is not an implementation detail; it encodes item multiplicity.

---

## Unique Paths & Minimum Path Sum (grid DP)

### Unique Paths — condensed

!!! pattern "Pattern: grid counting DP · T: O(mn) · S: O(n)"
    **Signals:** move right/down; count paths to cells.

#### Problem

Count paths from top-left to bottom-right in an `m × n` grid moving only right or down.

#### State/Transition

**STATE:** `dp[r][c]` = paths to `(r,c)`. **TRANSITION:** `dp[r][c]=dp[r-1][c]+dp[r][c-1]`. **BASE:** first row and first column are 1. **ORDER:** row-major.

#### Key Observation

!!! key "Key observation"
    A path enters a cell from exactly above or left. Those predecessor sets are disjoint, so counts add.

```diagram
{"type":"dptable","corner":"r\\c","col_head":["0","1","2","3"],"row_head":["0","1","2"],"grid":[[1,1,1,1],[1,2,3,4],[1,3,6,10]],"highlights":[[2,2,"primary"],[1,2,"green"],[2,1,"amber"]],"arrows":[{"from":[1,2],"to":[2,2],"color":"green"},{"from":[2,1],"to":[2,2],"color":"amber"}]}
```

#### Java

```java
int uniquePaths(int m, int n) {
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    for (int r = 1; r < m; r++) {
        for (int c = 1; c < n; c++) dp[c] += dp[c - 1];
    }
    return dp[n - 1];
}
```

#### Complexity

!!! complexity "Complexity"
    **T:** O(mn). **S:** O(n).

#### Pattern Connection

Grid DP is prefix DP in two dimensions: a cell is derived from already-filled neighboring cells.

### Minimum Path Sum — condensed

!!! pattern "Pattern: grid min-cost DP · T: O(mn) · S: O(n)"
    **Signals:** right/down movement; minimize accumulated cell cost.

#### Problem

Find the minimum cost path from top-left to bottom-right, moving only right or down.

#### State/Transition

**STATE:** `dp[r][c]` = minimum cost to reach `(r,c)`. **TRANSITION:** `grid[r][c] + min(dp[r-1][c], dp[r][c-1])`. **BASE:** top-left is `grid[0][0]`; borders accumulate. **ORDER:** row-major.

#### Key Observation

!!! key "Key observation"
    Same dependency geometry as Unique Paths; replace counting addition with a minimum over predecessor costs.

```diagram
{"type":"dptable","corner":"r\\c","col_head":["0","1","2"],"row_head":["0","1","2"],"grid":[[1,4,5],[2,7,6],[6,8,7]],"highlights":[[2,2,"primary"],[1,2,"green"],[2,1,"amber"]],"arrows":[{"from":[1,2],"to":[2,2],"color":"green"},{"from":[2,1],"to":[2,2],"color":"amber"}]}
```

#### Java

```java
int minPathSum(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    int[] dp = new int[n];
    dp[0] = grid[0][0];
    for (int c = 1; c < n; c++) dp[c] = dp[c - 1] + grid[0][c];
    for (int r = 1; r < m; r++) {
        dp[0] += grid[r][0];
        for (int c = 1; c < n; c++) {
            dp[c] = grid[r][c] + Math.min(dp[c], dp[c - 1]);
        }
    }
    return dp[n - 1];
}
```

#### Complexity

!!! complexity "Complexity"
    **T:** O(mn). **S:** O(n).

#### Pattern Connection

In a rolling row, `dp[c]` before update is "from above" and `dp[c-1]` after update is "from left".

---

## Longest Increasing Subsequence

!!! pattern "Pattern: subsequence DP + greedy tails · T: O(n²) or O(n log n) · S: O(n)"
    **Signals:** longest ordered subsequence; compare current element to previous chosen element.

### 1. The Problem

Return the length of the longest strictly increasing subsequence. A subsequence preserves order but may skip elements.

### 2. The Intuition

The DP view asks for the best increasing subsequence ending at each index. The optimized view stores the smallest possible tail for every subsequence length; smaller tails leave more room for future values.

### 3. The Naive Approach

Enumerate all subsequences in O(2^n). Memoizing `(index, previousIndex)` gives O(n²), but the ending-at-index table is cleaner.

### 4. The Key Observation 🔑

!!! key "Key observation"
    To extend with `nums[i]`, only the last chosen value matters. Every `j<i` with `nums[j] < nums[i]` can contribute `dp[j]+1`; choose the best.

### 5. Pattern Recognition

**Signals.** "Subsequence", "increasing", "longest". **Shortcut.** Start with O(n²) ending-at-index DP; if only length is needed, look for a monotonic tails frontier. **Related.** Russian Doll Envelopes, Maximum Sum Increasing Subsequence.

### 6. The Invariant

For O(n²), `dp[i]` is LIS length ending exactly at `i`. For patience sorting, `tails[len-1]` is the minimum tail value among increasing subsequences of length `len` seen so far.

**STATE:** `dp[i]` = LIS ending at `i`. **TRANSITION:** `dp[i] = 1 + max(dp[j])` for `j<i` and `nums[j]<nums[i]`, else 1. **BASE CASE:** each element alone has length 1. **ORDER:** increasing `i`.

### 7. Visual Explanation

```diagram
{"type":"dptable","corner":"i","col_head":["0","1","2","3","4","5"],"row_head":["nums","dp"],"grid":[[10,9,2,5,3,7],[1,1,1,2,2,3]],"highlights":[[1,5,"primary"],[1,3,"green"],[1,4,"green"],[0,5,"primary"]],"arrows":[{"from":[1,3],"to":[1,5],"color":"green"},{"from":[1,4],"to":[1,5],"color":"green"}]}
```

```diagram
{"type":"flow","title":"Patience tails update","width":470,"box":250,"steps":[{"type":"start","text":"tails empty"},{"type":"process","text":"for x in nums"},{"type":"process","text":"lower_bound first tail >= x"},{"type":"decision","text":"pos == size?","yes":"append x","branch":{"label":"no","text":"replace tails[pos]","role":"primary"}},{"type":"end","text":"size is LIS length"}]}
```

### 8. Algorithm Flow Diagram

The O(n log n) flow stores a frontier, not necessarily an actual subsequence. Replacing a tail preserves length while improving future extensibility.

### 9. Step-by-Step Walkthrough

For `[10,9,2,5,3,7,101,18]`, tails evolve as `[10]`, `[9]`, `[2]`, `[2,5]`, `[2,3]`, `[2,3,7]`, `[2,3,7,101]`, `[2,3,7,18]`; answer 4.

### 10. Why It Works

The O(n²) recurrence is exhaustive over the predecessor of `i`. For tails, maintaining the minimum possible tail for each length is safe because a smaller tail dominates a larger one for all future extensions. Lower bound ensures equal values replace rather than extend in strict LIS.

### 11. Java Implementation

```java
int lengthOfLIS(int[] nums) {
    int[] tails = new int[nums.length];
    int size = 0;
    for (int x : nums) {
        int lo = 0, hi = size;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (tails[mid] < x) lo = mid + 1;
            else hi = mid;
        }
        tails[lo] = x;
        if (lo == size) size++;
    }
    return size;
}

int lengthOfLISQuadratic(int[] nums) {
    int[] dp = new int[nums.length];
    Arrays.fill(dp, 1);
    int best = 0;
    for (int i = 0; i < nums.length; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) dp[i] = Math.max(dp[i], dp[j] + 1);
        }
        best = Math.max(best, dp[i]);
    }
    return best;
}
```

### 12. Code Walkthrough

Binary search finds the first tail `>= x`. If `x` is greater than all tails it extends the frontier; otherwise it improves an existing length's tail.

### 13. Complexity

!!! complexity "Complexity"
    **Quadratic DP:** **T:** O(n²), **S:** O(n). **Tails:** **T:** O(n log n), **S:** O(n).

### 14. Edge Cases

Empty array returns 0; all decreasing returns 1; duplicates do not extend strict LIS; non-decreasing LIS changes the binary search to first `> x`.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    `tails` is not necessarily a valid subsequence from the input. It is a dominance frontier. Store predecessors if you need the actual LIS.

### 16. Optimization

Use O(n log n) for length. Use index arrays and predecessor links for reconstruction.

### 17. Alternatives

Fenwick or segment trees over compressed values solve weighted or counted LIS variants.

### 18. Interview Follow-Ups

Return one LIS; count all LIS; solve Russian Doll Envelopes by sorting width ascending and height descending, then LIS on heights.

### 19. Variations

Maximum Sum Increasing Subsequence, Longest Divisible Subset, Longest Bitonic Subsequence.

### 20. Pattern Connection

LIS shows how a many-predecessor DP can sometimes be optimized by keeping a monotonic frontier of nondominated states.

---

## Longest Common Subsequence

!!! pattern "Pattern: two-sequence prefix DP · T: O(mn) · S: O(min(m,n))"
    **Signals:** two strings; preserve order; may skip characters.

### 1. The Problem

Given `text1` and `text2`, return the length of their longest common subsequence.

### 2. The Intuition

Compare the final characters of two prefixes. If they match, pair them and extend the smaller prefixes. If not, skip one final character.

### 3. The Naive Approach

Recursive mismatches branch into `lcs(i-1,j)` and `lcs(i,j-1)`, repeatedly recomputing the same prefix pairs.

### 4. The Key Observation 🔑

!!! key "Key observation"
    A subproblem is fully described by two prefix lengths. Match means diagonal plus one; mismatch means max of top and left.

### 5. Pattern Recognition

**Signals.** Two sequences, subsequence not substring, ordered alignment. **Shortcut.** Prefix lengths `(i,j)` usually handle operations that consume ends of two strings. **Related.** Edit Distance, Shortest Common Supersequence, Uncrossed Lines.

### 6. The Invariant

`dp[i][j]` is LCS length for `text1[0..i-1]` and `text2[0..j-1]`.

**STATE:** `dp[i][j]` = LCS of first `i` and first `j` chars. **TRANSITION:** if equal, `dp[i][j]=dp[i-1][j-1]+1`; else `max(dp[i-1][j], dp[i][j-1])`. **BASE CASE:** empty row/column are 0. **ORDER:** increasing `i`, increasing `j`.

### 7. Visual Explanation

```diagram
{"type":"dptable","corner":"a\\b","col_head":["","a","c","e"],"row_head":["","a","b","c"],"grid":[[0,0,0,0],[0,1,1,1],[0,1,1,1],[0,1,2,2]],"highlights":[[3,2,"primary"],[2,1,"green"],[2,2,"amber"],[3,1,"purple"]],"arrows":[{"from":[2,1],"to":[3,2],"color":"green"},{"from":[2,2],"to":[3,2],"color":"amber"},{"from":[3,1],"to":[3,2],"color":"purple"}]}
```

```diagram
{"type":"flow","title":"LCS cell recurrence","width":460,"box":250,"steps":[{"type":"start","text":"empty prefixes = 0"},{"type":"process","text":"for i=1..m, j=1..n"},{"type":"decision","text":"chars equal?","yes":"diagonal + 1","branch":{"label":"no","text":"max(top, left)","role":"primary"}},{"type":"end","text":"answer dp[m][n]"}]}
```

### 8. Algorithm Flow Diagram

Match consumes both strings; mismatch consumes one side in the optimal skip direction.

### 9. Step-by-Step Walkthrough

For `"abc"` and `"ace"`, `a/a` gives 1, `b/c` keeps 1, `c/c` extends the diagonal to 2, and the final mismatch with `e` keeps 2.

### 10. Why It Works

If final characters match, an optimal subsequence can pair them and reduce to smaller prefixes. If they differ, an optimal subsequence cannot use both as a matched pair, so it excludes one of them; top and left cover both exclusions.

### 11. Java Implementation

```java
int longestCommonSubsequence(String text1, String text2) {
    int m = text1.length(), n = text2.length();
    int[] prev = new int[n + 1];
    int[] cur = new int[n + 1];
    for (int i = 1; i <= m; i++) {
        Arrays.fill(cur, 0);
        for (int j = 1; j <= n; j++) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) cur[j] = prev[j - 1] + 1;
            else cur[j] = Math.max(prev[j], cur[j - 1]);
        }
        int[] tmp = prev;
        prev = cur;
        cur = tmp;
    }
    return prev[n];
}
```

### 12. Code Walkthrough

`prev[j]` is top, `cur[j-1]` is left, and `prev[j-1]` is diagonal. Two rows preserve all dependencies.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(mn). **S:** O(n), or O(mn) when reconstructing a subsequence with parent pointers.

### 14. Edge Cases

Either string empty returns 0; identical strings return their length; repeated characters require DP rather than greedy first matching.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Do not confuse subsequence with substring. Longest common substring resets to 0 on mismatch; LCS takes max(top,left).

### 16. Optimization

Use the shorter string as columns. Hirschberg reconstructs an LCS in linear space but is overkill for most interviews.

### 17. Alternatives

Top-down memoization over `(i,j)` is equivalent and often easier to derive aloud.

### 18. Interview Follow-Ups

Print one LCS; shortest common supersequence length is `m+n-LCS`; minimum deletions to equalize strings is `m+n-2*LCS`.

### 19. Variations

Uncrossed Lines, diff algorithms, sequence alignment, and delete-only string distance.

### 20. Pattern Connection

LCS is the reference two-sequence prefix DP; Edit Distance reuses the same grid with operation costs.

---

## Edit Distance

!!! pattern "Pattern: two-sequence transformation DP · T: O(mn) · S: O(min(m,n))"
    **Signals:** transform one string into another; insert/delete/replace; minimize operations.

### 1. The Problem

Given `word1` and `word2`, compute the minimum number of insertions, deletions, and replacements needed to transform `word1` into `word2`.

### 2. The Intuition

Classify the final operation on two prefixes. If final characters match, no operation is needed for them. Otherwise, the last operation is insert, delete, or replace.

### 3. The Naive Approach

A recursive mismatch branches three ways, producing exponential work because many operation orders lead to the same prefix pair.

### 4. The Key Observation 🔑

!!! key "Key observation"
    Removing the final edit operation from an optimal script leaves an optimal script for a smaller prefix pair. That makes prefix lengths the right state.

### 5. Pattern Recognition

**Signals.** Two strings, minimum edits, operations consume source and/or target characters. **Shortcut.** Define `dp[i][j]` and ask what the last operation did. **Related.** LCS, one edit distance, weighted alignment.

### 6. The Invariant

`dp[i][j]` is the minimum edits to convert `word1[0..i-1]` into `word2[0..j-1]`.

**STATE:** `dp[i][j]` = min edits for first `i` and first `j` chars. **TRANSITION:** if equal, `dp[i][j]=dp[i-1][j-1]`; else `1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])`. **BASE CASE:** `dp[i][0]=i`, `dp[0][j]=j`. **ORDER:** increasing `i`, increasing `j`.

### 7. Visual Explanation

```diagram
{"type":"dptable","corner":"a\\b","col_head":["","r","o","s"],"row_head":["","h","o","r","s"],"grid":[[0,1,2,3],[1,1,2,3],[2,2,1,2],[3,2,2,2],[4,3,3,2]],"highlights":[[3,3,"primary"],[3,2,"amber"],[2,3,"green"],[2,2,"purple"]],"arrows":[{"from":[3,2],"to":[3,3],"color":"amber"},{"from":[2,3],"to":[3,3],"color":"green"},{"from":[2,2],"to":[3,3],"color":"purple"}]}
```

```diagram
{"type":"flow","title":"Edit Distance final operation","width":480,"box":260,"steps":[{"type":"start","text":"fill empty prefix costs"},{"type":"process","text":"for each prefix pair"},{"type":"decision","text":"chars equal?","yes":"copy diagonal","branch":{"label":"no","text":"1 + min(insert, delete, replace)","role":"primary"}},{"type":"end","text":"return dp[m][n]"}]}
```

### 8. Algorithm Flow Diagram

Left means insert target char, top means delete source char, diagonal means replace source char. Equal characters use diagonal without cost.

### 9. Step-by-Step Walkthrough

For `horse -> ros`, one optimal sequence is replace `h` with `r`, delete an extra middle character, delete `e`, for cost 3. The table derives that cost by solving all smaller prefix conversions first.

### 10. Why It Works

An optimal edit script either leaves equal final characters matched or ends with exactly one of insert/delete/replace. Removing that final action yields a smaller subproblem; trying all final actions and taking the minimum is exhaustive and optimal.

### 11. Java Implementation

```java
int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[] prev = new int[n + 1];
    int[] cur = new int[n + 1];
    for (int j = 0; j <= n; j++) prev[j] = j;
    for (int i = 1; i <= m; i++) {
        cur[0] = i;
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) cur[j] = prev[j - 1];
            else cur[j] = 1 + Math.min(cur[j - 1], Math.min(prev[j], prev[j - 1]));
        }
        int[] tmp = prev;
        prev = cur;
        cur = tmp;
    }
    return prev[n];
}
```

### 12. Code Walkthrough

The first row is insertions into empty `word1`; `cur[0]` is deletions to empty `word2`. Rolling rows preserve left, top, and diagonal dependencies.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(mn). **S:** O(n), or O(mn) for edit-script reconstruction.

### 14. Edge Cases

Empty string costs the other length; identical strings cost 0; repeated letters still require DP because local matches can block better global alignment.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Keep prefix lengths separate from character indices: cell `(i,j)` reads characters `i-1` and `j-1` only inside loops starting at 1.

### 16. Optimization

Use the shorter word as columns. If an edit threshold is small, banded DP can restrict computation near the diagonal.

### 17. Alternatives

With only insertions and deletions, use LCS: `m+n-2*lcs`. Different operation costs only change the mismatch formula.

### 18. Interview Follow-Ups

Return the edit script; check one-edit distance; support weighted operations or substitutions.

### 19. Variations

Minimum ASCII Delete Sum, wildcard matching, regex matching, and bioinformatics sequence alignment.

### 20. Pattern Connection

Edit Distance teaches final-operation DP. It shares LCS's prefix grid but changes the aggregation from length maximization to cost minimization.

---

## Best Time to Buy/Sell Stock with Cooldown (state-machine DP)

!!! pattern "Pattern: finite-state DP · T: O(n) · S: O(1)"
    **Signals:** daily actions, inventory status, cooldown or transaction constraints.

### Problem

Maximize stock profit with unlimited transactions, but after selling you must wait one day before buying again.

### State/Transition

Use three states after each day: `hold` = holding stock; `sold` = sold today; `rest` = not holding and did not sell today. **TRANSITION:** `newHold=max(hold, rest-price)`, `newSold=hold+price`, `newRest=max(rest, sold)`. **BASE:** `hold=-∞`, `sold=-∞`, `rest=0`. **ORDER:** days left to right.

### Key Observation

!!! key "Key observation"
    Cooldown is awkward as a day-index condition but simple as a legal-state transition. Track the status that determines tomorrow's allowed actions.

```diagram
{"type":"dptable","corner":"day","col_head":["0 p1","1 p2","2 p3","3 p0","4 p2"],"row_head":["hold","sold","rest"],"grid":[[-1,-1,-1,1,1],[-999,1,2,-1,3],[0,0,1,2,2]],"highlights":[[1,4,"primary"],[0,3,"green"],[2,3,"amber"]],"arrows":[{"from":[0,3],"to":[1,4],"color":"green"},{"from":[2,3],"to":[0,4],"color":"amber"}]}
```

### Java

```java
int maxProfitCooldown(int[] prices) {
    int hold = Integer.MIN_VALUE / 4;
    int sold = Integer.MIN_VALUE / 4;
    int rest = 0;
    for (int price : prices) {
        int prevHold = hold, prevSold = sold, prevRest = rest;
        hold = Math.max(prevHold, prevRest - price);
        sold = prevHold + price;
        rest = Math.max(prevRest, prevSold);
    }
    return Math.max(sold, rest);
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n). **S:** O(1).

### Pattern Connection

State-machine DP applies when constraints depend on the last action. Name statuses first; the recurrence becomes a transition graph.

---

## House Robber III (tree DP)

!!! pattern "Pattern: tree choose/skip DP · T: O(n) · S: O(h)"
    **Signals:** parent-child conflict; choose nodes in a tree; postorder aggregation.

### Problem

Rob nodes in a binary tree without robbing directly-linked parent and child nodes. Return max money.

### State/Transition

For each node return `{take, skip}`. **TRANSITION:** `take = node.val + left.skip + right.skip`; `skip = max(left.take,left.skip) + max(right.take,right.skip)`. **BASE:** null returns `{0,0}`. **ORDER:** postorder.

### Key Observation

!!! key "Key observation"
    A scalar best subtree value loses whether the subtree root was robbed. The parent needs that status, so each node exposes both outcomes.

```diagram
{"type":"dptable","corner":"node","col_head":["leaf 3","leaf 1","node 2","root 3"],"row_head":["take","skip"],"grid":[[3,1,2,7],[0,0,3,6]],"highlights":[[0,3,"primary"],[1,2,"green"],[0,0,"amber"]],"arrows":[{"from":[1,2],"to":[0,3],"color":"green"},{"from":[0,0],"to":[1,2],"color":"amber"}]}
```

```diagram
{"type":"recursion","nodes":[{"id":"root","label":"3\n(7,6)","x":3,"y":0,"role":"primary"},{"id":"l","label":"2\n(2,3)","x":1,"y":1,"role":"green"},{"id":"r","label":"3\n(3,1)","x":5,"y":1,"role":"green"},{"id":"lr","label":"3\n(3,0)","x":2,"y":2,"role":"amber"},{"id":"rr","label":"1\n(1,0)","x":6,"y":2,"role":"amber"}],"edges":[{"from":"root","to":"l","label":"child","color":"green"},{"from":"root","to":"r","label":"child","color":"green"},{"from":"l","to":"lr","label":"","color":"amber"},{"from":"r","to":"rr","label":"","color":"amber"}]}
```

### Java

```java
int rob(TreeNode root) {
    int[] ans = dfs(root);
    return Math.max(ans[0], ans[1]);
}

int[] dfs(TreeNode node) {
    if (node == null) return new int[]{0, 0};
    int[] left = dfs(node.left);
    int[] right = dfs(node.right);
    int take = node.val + left[1] + right[1];
    int skip = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);
    return new int[]{take, skip};
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n). **S:** O(h) recursion stack.

### Pattern Connection

Tree DP returns enough information from each child to make the parent's decision independent of the child's internal structure.

---

## Burst Balloons

!!! pattern "Pattern: interval DP with last action · T: O(n³) · S: O(n²)"
    **Signals:** deleting items changes neighbors; operation order over intervals; stable sentinel boundaries.

### 1. The Problem

Bursting balloon `k` earns `left * nums[k] * right`, where `left` and `right` are its current unburst neighbors. Return the maximum coins after all balloons are burst.

### 2. The Intuition

The first burst is hard because it changes future neighbors. Choose the last balloon burst inside an interval instead. At that moment, its neighbors are the fixed interval boundaries.

### 3. The Naive Approach

Trying all burst orders is O(n!). Memoizing arbitrary remaining sets is still exponential. The interval-last view collapses the state to contiguous ranges.

### 4. The Key Observation 🔑

!!! key "Key observation"
    In open interval `(l,r)`, if `k` is burst last, its final gain is `val[l] * val[k] * val[r]`, independent of how the left and right subintervals were solved.

### 5. Pattern Recognition

**Signals.** Current neighbors matter, deletions/merges change context, all operation orders considered. **Shortcut.** If first action destabilizes state, ask whether the last action has stable boundaries. **Related.** Matrix Chain Multiplication, stick cutting, polygon triangulation.

### 6. The Invariant

`dp[l][r]` is the max coins from bursting all balloons strictly between padded indices `l` and `r`, while boundaries `l` and `r` remain unburst.

**STATE:** `dp[l][r]` = max coins for open interval `(l,r)`. **TRANSITION:** `dp[l][r] = max_k(dp[l][k] + val[l]*val[k]*val[r] + dp[k][r])` for `l<k<r`. **BASE CASE:** `r=l+1` gives 0. **ORDER:** increasing interval length.

### 7. Visual Explanation

```diagram
{"type":"dptable","corner":"l\\r","col_head":["0","1","2","3","4"],"row_head":["0","1","2","3","4"],"grid":[[0,0,3,30,35],["",0,0,15,30],["","",0,0,5],["","","",0,0],["","","","",0]],"highlights":[[0,4,"primary"],[0,1,"green"],[1,4,"amber"],[0,3,"purple"],[3,4,"green"]],"arrows":[{"from":[0,1],"to":[0,4],"color":"green"},{"from":[1,4],"to":[0,4],"color":"amber"},{"from":[0,3],"to":[0,4],"color":"purple"},{"from":[3,4],"to":[0,4],"color":"green"}]}
```

```diagram
{"type":"recursion","nodes":[{"id":"a","label":"(l,r) choose last k","x":3,"y":0,"role":"primary"},{"id":"b","label":"(l,k)","x":1,"y":1,"role":"green"},{"id":"c","label":"(k,r)","x":5,"y":1,"role":"amber"},{"id":"d","label":"val[l]*val[k]*val[r]","x":3,"y":2,"role":"purple"}],"edges":[{"from":"a","to":"b","label":"left","color":"green"},{"from":"a","to":"c","label":"right","color":"amber"},{"from":"a","to":"d","label":"last burst","color":"purple"}]}
```

### 8. Algorithm Flow Diagram

The recursion diagram explains the recurrence; the implementation fills the same states bottom-up by interval length so both child intervals are ready.

### 9. Step-by-Step Walkthrough

For `[3,1,5]`, pad to `[1,3,1,5,1]`. Length-2 intervals give `(0,2)=3`, `(1,3)=15`, `(2,4)=5`; length-3 intervals give `(0,3)=30`, `(1,4)=30`; final `(0,4)=35`.

### 10. Why It Works

Fix an optimal order for `(l,r)` and let `k` be the last internal balloon. Before bursting `k`, all balloons in `(l,k)` and `(k,r)` have been removed independently, and the only remaining neighbors of `k` are `l` and `r`. Maximizing over all choices of `k` covers every valid order by its final internal balloon.

### 11. Java Implementation

```java
int maxCoins(int[] nums) {
    int n = nums.length;
    int[] val = new int[n + 2];
    val[0] = 1;
    val[n + 1] = 1;
    for (int i = 0; i < n; i++) val[i + 1] = nums[i];
    int[][] dp = new int[n + 2][n + 2];
    for (int len = 2; len <= n + 1; len++) {
        for (int left = 0; left + len <= n + 1; left++) {
            int right = left + len;
            for (int k = left + 1; k < right; k++) {
                int coins = dp[left][k] + val[left] * val[k] * val[right] + dp[k][right];
                dp[left][right] = Math.max(dp[left][right], coins);
            }
        }
    }
    return dp[0][n + 1];
}
```

### 12. Code Walkthrough

Padding with 1 removes boundary cases. Intervals of length 1 have no internal balloon and remain 0; every candidate `k` splits the interval into two smaller already-computed intervals.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n³) for O(n²) intervals and O(n) last-balloon choices. **S:** O(n²).

### 14. Edge Cases

Empty input returns 0; one balloon `x` returns `x`; zeros are handled by the recurrence but may produce many zero-gain choices.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    A closed-interval definition often multiplies by neighbors that have already changed. Use open intervals with fixed external boundaries.

### 16. Optimization

O(n³) is expected for the canonical problem. Store the maximizing `k` if reconstructing an optimal order.

### 17. Alternatives

Top-down memoization uses the same recurrence:

```java
int maxCoinsMemo(int[] nums) {
    int n = nums.length;
    int[] val = new int[n + 2];
    val[0] = val[n + 1] = 1;
    for (int i = 0; i < n; i++) val[i + 1] = nums[i];
    Integer[][] memo = new Integer[n + 2][n + 2];
    return solve(val, 0, n + 1, memo);
}

int solve(int[] val, int left, int right, Integer[][] memo) {
    if (right == left + 1) return 0;
    if (memo[left][right] != null) return memo[left][right];
    int best = 0;
    for (int k = left + 1; k < right; k++) {
        int coins = solve(val, left, k, memo) + val[left] * val[k] * val[right]
                + solve(val, k, right, memo);
        best = Math.max(best, coins);
    }
    memo[left][right] = best;
    return best;
}
```

### 18. Interview Follow-Ups

Compare with Matrix Chain Multiplication; return burst order by storing splits; minimize cost variants by replacing max with min.

### 19. Variations

Minimum Cost to Cut a Stick, Matrix Chain Multiplication, Strange Printer, palindrome removal, and polygon triangulation.

### 20. Pattern Connection

Burst Balloons is the flagship interval DP: reversing time turns unstable neighbors into fixed boundaries and exposes independent subintervals.
