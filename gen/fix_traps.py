"""Rewrite canonical-problem traps to include a concrete failing example.
Keyed by exact H2 problem title. Rewrites the first `> [trap] **Common Trap** —` line
in each matching section wholesale.
"""
import re, os

TRAP = {
 "Two Sum": "Inserting into the map **before** the check makes an element match itself. *Example:* `nums=[3,2,4]`, `target=6`. If you `put(3,0)` first, then check for `target-3=3`, you find yourself and emit `(0,0)`. Check first, insert after.",
 "Group Anagrams": "Building the count key without a delimiter collides distinct histograms. *Example:* counts `[1,11]` and `[11,1]` both stringify to `\"111\"` and get grouped together. Separate fields — e.g. `\"1#11\"` vs `\"11#1\"`.",
 "Product of Array Except Self": "Reaching for division. *Example:* `nums=[1,2,0,4]` — dividing the total product by each element blows up at the zero. The prefix/suffix product is division-free and zero-safe.",
 "Longest Consecutive Sequence": "Omitting the `x-1` guard makes it O(n\u00b2). *Example:* `nums=[1,2,3,4]` — without the guard you walk the run from 1, then from 2, then from 3, then from 4 \u2192 4+3+2+1 steps. Only start from values whose predecessor is absent.",
 "3Sum": "Missing any of the three duplicate-skips yields repeated triplets. *Example:* `nums=[-1,-1,-1,2]`. Without skipping duplicate pivots you emit `[-1,-1,2]` twice (once per `-1` as pivot); without skipping `lo`/`hi` after a hit, `[0,0,0,0]` emits `[0,0,0]` multiple times.",
 "Container With Most Water": "Moving the taller wall can never help. *Example:* `heights=[1,8,6,2,5,4,8,3,7]`, `lo=0(h=1), hi=8(h=7)`. Moving `hi` inward shrinks width and can't raise the min (already `1`). Move the shorter wall \u2014 the only move that can improve area.",
 "Squaring a Sorted Array": "Squaring in place, then sorting. *Example:* `nums=[-4,-1,0,3,10]` \u2192 squared `[16,1,0,9,100]` still needs a sort (O(n log n)). Two pointers from the ends fill an output array from the back in O(n).",
 "Sort Colors (Dutch National Flag)": "Advancing `mid` after swapping with `high` skips an unexamined value. *Example:* `[2,0,2]`, `mid=1`. Swap `a[mid]` with `a[high]` \u2192 `[2,0,2]` (a `2` moves in at `mid`). If you `mid++`, you miss re-evaluating that new value. Advance `mid` only when you swapped with `low` or saw a `1`.",
 "Trapping Rain Water": "Local vs global boundaries. *Example:* `heights=[4,2,0,3,2,5]`. Water above index 3 (h=3) is bounded by the global `4` on the left and `5` on the right \u2014 not by 3. Track running max from each side (or the shorter side with two pointers).",
 "Smallest Subarray With Sum \u2265 Target": "Forgetting the \"no window found\" case. *Example:* `nums=[1,1,1]`, `target=100`. No window satisfies the sum; if you return `best` still at `Integer.MAX_VALUE`, the caller thinks a huge window exists. Return `0` when `best` was never updated.",
 "Longest Substring Without Repeating Characters": "Not clamping `left` to its previous position. *Example:* `s=\"abba\"`. At index 3 (`'a'`), the previous `a` was at 0, but `left` has already moved past 2. Without `left = max(left, prev+1)`, `left` retreats and the window contains two `a`s.",
 "Minimum Window Substring": "Decrementing `formed` on every removal. *Example:* `s=\"AAAB\"`, `t=\"AB\"`. When you shrink past an extra `A`, `A`'s count stays \u2265 needed, so `formed` shouldn't drop. Decrement only when the count falls **below** the required threshold.",
 "Longest Repeating Character Replacement": "Assuming `maxCount` must decrease on shrinks. *Example:* `s=\"AABBCC\"`, `k=1`. Even after a shrink discards the majority character, leaving `maxCount` stale doesn't hurt: the window size only grows when the true max grows, so a stale-high value can't inflate the answer. You may skip the O(26) refresh.",
 "Sliding Window Maximum (Monotonic Deque)": "Storing values, not indices. *Example:* `nums=[3,1,3]`, `k=2`. At `i=2`, the front `3` could be the old one that just exited the window \u2014 you can't tell without its index. Store indices; expire the front when `dq.peekFirst() <= i-k`.",
 "Cyclic Sort (the base template)": "Advancing `i` after every swap skips values you just placed. *Example:* `nums=[3,1,2]` at `i=0`. Swap `3` to index 2 \u2192 `[2,1,3]`. If you `i++`, the fresh `2` at index 0 never gets placed at index 1. Use `while` (not `if`) at each `i`.",
 "First Missing Positive (Hard)": "Trying to place out-of-range values. *Example:* `nums=[3,4,-1,1]`. `-1` and `4` can't fit in `[0..n-1]` (n=4). Guard `1 \u2264 v \u2264 n` before every swap or you'll IOOBE.",
 "Valid Parentheses": "Returning `true` without checking `stack.isEmpty()`. *Example:* `s=\"(()\"` \u2014 every closer matched, but one `(` was never closed. Return `stack.isEmpty()`, not just `true`.",
 "Daily Temperatures (Next Greater Element)": "Storing values instead of indices. *Example:* `temps=[73,74,75]`. The answer at index 0 is 1 (`i=1` is warmer), which is `1-0`. If the stack held temperatures, you'd have to search back to recover the gap. Push **indices**, subtract on pop.",
 "Largest Rectangle in Histogram": "Forgetting the sentinel `0`. *Example:* `heights=[2,1,5,6,2,3]` \u2014 the tallest bar (`6`) never sees a shorter one to its right, so it never gets popped. Append a virtual `0` at the end so every remaining bar is resolved uniformly.",
 "Min Stack (O(1) minimum)": "A single scalar `min` can't be restored after `pop`. *Example:* push 5, push 3 (min=3), pop 3 \u2014 should min go back to 5? Without a per-entry or parallel min, you've lost that history. Store the running min with each pushed value.",
 "Search in Rotated Sorted Array": "Wrong inclusivity on the \"sorted-half\" test. *Example:* `nums=[3,1]`, `target=1`, `lo=0, hi=1, mid=0`. With strict `a[lo] < a[mid]`, a single-element left half `[3]` isn't marked sorted and the algorithm misroutes. Use `a[lo] <= a[mid]`.",
 "Koko Eating Bananas (Search on Answer \u2014 rate)": "Feasibility direction flipped. *Example:* `piles=[3,6,7,11]`, `h=8`. If `feasible(speed)` returns `true` when speed is too slow, binary search converges to the fastest failing speed. Sanity-check: `feasible(min)` should be `false` and `feasible(max)` should be `true`.",
 "Split Array Largest Sum / Book Allocation (Search on Answer \u2014 partition)": "Wrong feasibility semantics. *Example:* `nums=[7,2,5,10,8]`, `m=2`. `feasible(cap)` asks *\"can we split into \u2264 m subarrays, each with sum \u2264 cap?\"*. Confusing it with *\"exactly m\"* misclassifies boundaries and the search settles on the wrong split.",
 "Median of Two Sorted Arrays (Partition Binary Search)": "Off-by-one when the total length is odd. *Example:* `A=[1]`, `B=[2,3]`. Left partition should hold `(m+n+1)/2 = 2` elements \u2014 the median is the `max` of that left side. Using `(m+n)/2` puts the median on the wrong side.",
 "Jump Game II (Farthest-Reach Greedy)": "Counting jumps at every step instead of at the frontier. *Example:* `nums=[2,3,1,1,4]`. Incrementing `jumps` at each index gives 5; incrementing only when `i == currentEnd` (frontier boundary) gives 2. Update `currentEnd = farthest` and `jumps++` together.",
 "Gas Station (Prefix-Balance Greedy)": "Skipping the total check. *Example:* `gas=[1,2,3,4]`, `cost=[2,3,4,5]`. Total gas 10 < total cost 14, so **no** station works \u2014 but a local reset can look promising. Verify `sum(gas) >= sum(cost)`; if not, return `-1`.",
 "Merge Intervals": "Touching vs overlapping. *Example:* `[1,2]` and `[2,3]`. If touching counts as overlap \u2192 merge (`cur.start <= last.end`) \u2192 `[1,3]`. If not \u2192 keep separate (`cur.start < last.end`). LeetCode's *Merge Intervals* treats touching as overlap; *Non-overlapping Intervals* does not.",
 "Meeting Rooms II (Minimum Concurrent Intervals)": "Tie at `start == end`. *Example:* meetings `[1,5]` and `[5,10]`. If end-events sort **before** start-events, one room suffices (release, then acquire). If start sorts first, you need 2. LeetCode's *Meeting Rooms II* treats them as one \u2014 sort ends first on ties.",
 "Non-overlapping Intervals (Interval Scheduling)": "Sorting by start, not end. *Example:* `[[1,100],[2,3],[3,4]]`. Sorting by start keeps `[1,100]` first and drops the two short intervals. Sort by **end**: pick `[2,3]`, then `[3,4]` \u2014 remove `[1,100]`.",
 "Subsets & Combinations (the start-index template)": "Forgetting to un-choose. *Example:* generating subsets of `[1,2]`. If you `add(1)` and recurse but don't `remove(1)`, the sibling branch `[2]` starts with path `[1]` and you emit `[1,2]` twice. `remove(path.size()-1)` is the whole discipline.",
 "Permutations (the used[] template)": "Duplicates without sort-and-skip. *Example:* `nums=[1,1,2]` without `if (i>0 && a[i]==a[i-1] && !used[i-1]) continue;` \u2014 you emit `[1,1,2]` twice (once for each `1` picked first). Sort + the `used[i-1]` guard eliminates the twin.",
 "Combination Sum (reuse & pruning)": "Passing `i+1` when reuse is allowed. *Example:* `candidates=[2,3]`, `target=6`. You need `[2,2,2]` and `[3,3]`, which requires re-picking the same index. Recurse with `i` (not `i+1`) \u2014 otherwise you only get `[3,3]`.",
 "N-Queens (constraint occupancy)": "Wrong diagonal keys. *Example:* queens at `(0,0)` and `(1,1)` \u2014 same anti-diagonal (`row-col = 0`). Use **two** bitsets keyed by `row-col` (anti) and `row+col` (main). Swapping them rejects valid boards.",
 "Word Search (grid backtracking)": "Not restoring the cell on the way back up. *Example:* board `[[A,B],[C,D]]` searching `\"AB\"`. If you mark `A` visited via `#` but forget to restore it after the recursive call, a sibling path can't reuse `A`. Overwrite \u2192 recurse \u2192 restore.",
 "Quickselect (Kth Largest Element)": "Bad pivots. *Example:* `nums=[1,2,3,4,5]`, k=1, picking the *last* element as pivot every time \u2192 each partition shrinks by only 1 \u2192 O(n\u00b2). Random pivot (or median-of-three) keeps average O(n).",
 "1D DP \u2014 Climbing Stairs & House Robber": "Missing a base case. *Example:* `nums=[5]` for House Robber. If `dp[i-2]` is unseeded (e.g. `dp[-1]`), the transition breaks. Seed `prev1 = a[0]`, `prev2 = 0` \u2014 the single-house answer is `a[0]`.",
 "0/1 Knapsack & Subset-Sum family": "Wrong capacity direction. *Example:* items=`[1]`, cap=2, 0/1 knapsack. Iterating capacity **ascending** lets `dp[2] = dp[1] + val`, using item 0 twice (illegal). Iterate **descending** for 0/1; ascending only for unbounded.",
 "Coin Change (unbounded, min count)": "Sentinel overflow. *Example:* if `dp[i-c] = Integer.MAX_VALUE` and you compute `dp[i-c]+1`, you wrap to `Integer.MIN_VALUE` \u2014 looks like the smallest answer. Use `amount+1` as the sentinel: bigger than any real answer, safe to add 1.",
 "Grid DP \u2014 Unique Paths & Minimum Path Sum": "Rolling-row overwritten in wrong order. *Example:* grid `[[1,2],[3,4]]`. When collapsing to one row, if you overwrite `dp[j]` before reading it for `dp[j+1]`, you lose the top-neighbour value. For sum-min, update `dp[j] = grid[i][j] + min(dp[j], dp[j-1])` left-to-right; for right-to-left transitions iterate the opposite way.",
 "Subsequence DP \u2014 LIS, LCS, Edit Distance": "Strict vs non-decreasing LIS. *Example:* `[1,3,3,5]`. Strict LIS = 3 (`1,3,5`); non-decreasing = 4. `Collections.binarySearch` returning the insertion point for `3` differs by one between strict (replace at first `\u2265`) and non-strict (replace at first `>`). Confirm the requirement.",
 "Interval DP \u2014 Matrix Chain / Burst Balloons": "Iterating the outer loop over `l` (left endpoint) first. *Example:* Burst Balloons with `nums=[3,1,5,8]`. Outer over left leaves smaller intervals unsolved when you need them. Iterate over **length** first (smallest \u2192 largest), so any subinterval is already computed when you need it.",
 "State-Machine DP \u2014 Stock trading with cooldown": "Not enumerating all states. *Example:* stock with cooldown. Two states (hold, not-hold) miss the cooldown day \u2014 the not-hold state must split into \"just sold\" and \"free.\" Miss the split and cooldown gets ignored.",
 "Bitmask DP \u2014 Travelling Salesman / assignment": "`n` too large. *Example:* `n=25` \u2192 `2\u00b2\u2075 = 33M` masks \u00d7 25 = 800M ops, borderline. Bitmask DP scales as `O(n \u00b7 2\u207f)`, so it caps at n\u224820\u201322. Above that, name the alternative (branch-and-bound, DP with subset-sum precompute).",
 "Single Number I / II / III (XOR)": "Whole-XOR as split mask. *Example:* `nums=[1,2,3,4,1,2]`. `xy = 3^4 = 7 (0b111)`. Splitting by whole `xy` puts `1,2,3` in one group and `4` in the other \u2014 but `1^2^3 = 0`, losing the loner. Isolate a **single** distinguishing bit via `xy & -xy`.",
 "Counting Bits (DP on bits)": "Recomputing popcount per number. *Example:* na\u00efve `Integer.bitCount(i)` for i=0..n is O(n log n). The DP recurrence `bits[i] = bits[i >> 1] + (i & 1)` reuses the answer for `i/2` \u2192 O(n).",
 "Fenwick Tree (Binary Indexed Tree)": "0-index vs 1-index confusion. *Example:* `update(i)` for `i=0` with 0-indexed `i` gives `i & -i == 0`, so the loop never advances. Fenwick trees are naturally 1-indexed; shift external indices by +1 or handle the 0 case explicitly.",
 "Segment Tree (range query + range update)": "Forgetting `push` before recursing into children. *Example:* range-add a `+5` tag on a node, then query one of its children without pushing. The child returns its stale sum (missing the +5) and the aggregate is wrong. Push lazy tags at the top of both `update` and `query` before recursing.",
 "Fast (Binary) Exponentiation \u2014 Pow(x, n)": "Not widening `n` before negating. *Example:* `n = Integer.MIN_VALUE = -2\u00b3\u00b9`. `-n` overflows back to itself, so `n < 0 ? -n : n` yields a negative `n` \u2014 the while-loop never terminates. Widen to `long` first.",
 "Euclid's Algorithm \u2014 GCD & LCM": "`a * b` in LCM overflows even when the LCM fits. *Example:* `a = b = 10\u2079`. `gcd = 10\u2079`, but `a*b = 10\u00b9\u2078` overflows `long`. Always `a / gcd(a,b) * b` \u2014 divide before multiplying.",
 "Sieve of Eratosthenes \u2014 Count Primes": "Starting the inner loop at `2*i` (redundant) or forgetting to widen. *Example:* i \u2248 46341, `i*i` overflows `int` to negative \u2192 index out of range. Use `(long)i*i`; start there because smaller multiples were marked by smaller primes.",
 "Insert Delete GetRandom O(1)": "Forgetting to update the moved element's index. *Example:* `insert 1,2,3` (`vals=[1,2,3]`, `idx={1:0,2:1,3:2}`). `remove(1)`: swap `vals[0]` with last (`3`) \u2192 `vals=[3,2]`. Without `idx.put(3, 0)`, a later `remove(3)` uses stale index `2` \u2192 wrong slot.",
 "Reservoir Sampling \u2014 uniform pick from a stream": "Sampling with the wrong probability. *Example:* if you replace with `rnd.nextInt(count-1) == 0` instead of `nextInt(count) == 0`, the k-th element has probability `1/(k-1)` (or the loop mis-fires at k=1). Off-by-one on the reservoir wrecks uniformity.",
 "Longest Palindromic Substring (Expand Around Center)": "Only expanding **odd**-length centers. *Example:* `\"abba\"` has an even-length palindrome centered between indices 1 and 2. Skip the even-center expansion and you miss `\"abba\"` entirely. Expand twice per index \u2014 `(i,i)` and `(i,i+1)`.",
 "Encode and Decode Strings (Length Prefixing)": "Fixed delimiter with unescaped payload. *Example:* strings `[\"a#b\",\"c\"]` with delimiter `#` \u2192 encode `\"a#b#c\"`, decode as `[\"a\",\"b\",\"c\"]` (wrong). Length-prefixing `\"3#a#b1#c\"` bypasses escaping \u2014 read the count, then exactly that many chars.",
 "Reverse a Linked List": "Losing `next` before rewiring. *Example:* nodes `1\u21922\u21923`. If you do `cur.next = prev;` before saving `cur.next` into a temp, the rest of the list is lost. Always: `next = cur.next; cur.next = prev; prev = cur; cur = next;`.",
 "Linked List Cycle II (Floyd)": "Only checking `fast != null`. *Example:* even-length list `1\u21922`. After one step, `fast` is at `2` (non-null), so `fast.next.next` NPEs on the missing `next`. Check both `fast != null && fast.next != null` before the double hop.",
 "Merge Two / K Sorted Lists": "Not re-feeding the heap. *Example:* three lists `[1,4],[1,3],[2,6]`. After popping `1` from list A, you must `offer(A.next)` (i.e. `4`) \u2014 otherwise list A never appears again and its remaining nodes are silently dropped.",
 "Reorder / Palindrome via Split-Reverse-Merge": "Splitting on the wrong middle. *Example:* even-length list `1\u21922\u21923\u21924`. Fast/slow with `while (fast.next != null && fast.next.next != null)` gives the correct \"first-half\" middle at `2`, so the second half `3\u21924` reverses cleanly. Split at the geometric middle instead and the halves misalign.",
 "LRU Cache (Design)": "Not updating recency on `get`. *Example:* insert 1,2,3 (cap 3); `get(1)`; insert 4. Without moving 1 to the front on the read, 1 is still the LRU and gets evicted \u2014 but `1` was **just** used. `get` must be a mutation.",
 "Traversals (iterative & the recursion skeleton)": "Iterative in-order missing the \"go-left first\" phase. *Example:* tree `1\u21902\u21923`. Popping-and-printing before pushing all lefts prints in preorder, not in-order. Push lefts first, then pop-visit-descend-right.",
 "Maximum Depth, Balanced, Diameter (post-order aggregation)": "Edges vs nodes. *Example:* a 3-node linear tree `A-B-C`. Diameter measured in **edges** is 2 (`A\u2192B\u2192C`); in **nodes** is 3. LeetCode's *Diameter of Binary Tree* counts **edges** \u2014 return `max(leftDepth + rightDepth)`, not `+1`.",
 "Lowest Common Ancestor": "BST logic on a general tree. *Example:* general-tree LCA(5,1) is 3 regardless of value order. Using BST comparisons (`p.val < root.val`) hunts one subtree and misses the split. For general trees, recurse both sides and combine.",
 "Validate BST & BST operations": "Local-only comparison. *Example:* `root=10, left=5, left.right=12`. Locally `5<10` and `12>5` \u2014 both pass \u2014 but `12` violates BST because it's under `10`'s left subtree. Pass an inclusive `(min, max)` bound down.",
 "Serialize / Deserialize (structure encoding)": "Ambiguity from missing null markers. *Example:* trees `[1,2]` (left-child only) and `[1,null,2]` (right-child only) serialize identically if you skip nulls. Emit an explicit sentinel (e.g. `#`) for null children; the pre-order stream then uniquely decodes.",
 "Construct Tree from Traversals": "Repeated linear scans. *Example:* preorder `[3,9,20,15,7]`, inorder `[9,3,15,20,7]`. Locating `3` in inorder each call is O(n) \u2192 total O(n\u00b2). Precompute `Map<Integer,Integer>` from value \u2192 inorder index for O(1) lookup and O(n) total.",
 "Tree DP (House Robber III)": "Returning a scalar instead of a state pair. *Example:* on subtree rooted at `v`, you need both \"best with `v` robbed\" and \"best without\" so the parent can combine \u2014 a single number forces recomputation. Return `int[]{robbed, notRobbed}`.",
 "Kth Largest / Top K Frequent": "Wrong heap polarity. *Example:* the *k-th largest* with a **max**-heap of all n elements costs O(n log n) \u2014 wasteful. A **min**-heap of size k evicts the smallest; the root is your answer in O(n log k).",
 "Merge K Sorted Lists / Smallest Range (K-way merge)": "Popping without re-feeding the same list. *Example:* three lists \u2014 after popping `A.head`, if you push a random next instead of `A.next`, list A gets skipped ahead and its remaining values leak into another list's stream. Push `polled.list.next` from the same list you popped.",
 "Find Median from Data Stream (Two Heaps)": "Skipping the rebalance. *Example:* insert 1,2,3,4. Without rebalancing, all four might land in the low-heap \u2192 median unreadable. After every insert: push to `low`, move `low.top` to `high`; if `high.size() > low.size()` move one back. Two peeks give the median.",
 "Implement Trie": "`isEnd` only on leaves. *Example:* insert `\"car\"` then `\"cars\"`. If you only mark `s` as end, `search(\"car\")` returns false. `isEnd` marks a **word boundary**, independent of children \u2014 set it on `r` too.",
 "Word Search II (Trie + Backtracking)": "Re-adding a word for every path that reaches it. *Example:* board has multiple paths spelling `\"cat\"` from the same trie leaf. Without clearing `node.word` after the first find (or using a `Set<String>` result), you emit `\"cat\"` multiple times.",
 "Maximum XOR of Two Numbers (Binary Trie)": "Comparing bits in the wrong direction. *Example:* numbers `[3,10,5,25]` \u2014 XOR-max hunt greedily wants the **opposite** bit at each level from the query. Insert MSB-first; at each level, walk the child whose bit differs from the current bit (fall back if that branch doesn't exist).",
 "Number of Islands (grid flood fill)": "Marking after recursing. *Example:* grid `[[1,1],[1,1]]`. If you recurse into a neighbour before marking the current cell visited, it recurses back into you \u2192 stack overflow. Mark visited **before** the 4-way recursion.",
 "Rotting Oranges (multi-source BFS)": "Single-source BFS on a multi-source problem. *Example:* two rotten oranges at opposite corners with fresh ones between. From one source, the middle rots at time `d`; from both simultaneously, at `d/2`. Queue **all** rotten cells at t=0.",
 "Course Schedule (Topological Sort)": "Not detecting cycles. *Example:* prerequisites `0\u21921` and `1\u21920`. Kahn's queue starts empty (no in-degree-0 node); if `order.size() < V` at the end, report \"impossible\" rather than a partial order.",
 "Dijkstra (weighted shortest path, non-negative)": "Skipping the stale-pop guard. *Example:* edges push `{v,10}` then `{v,3}` for the same node. When you pop `{v,10}` later, without `if (d > dist[v]) continue;` you re-relax neighbours with the wrong distance. Guard every pop.",
 "Bellman\u2013Ford (negative edges & negative-cycle detection)": "Ignoring `\u221e + w` overflow. *Example:* `dist[u] = Integer.MAX_VALUE`. Then `dist[u] + w` wraps negative and looks like an improvement \u2014 you relax the whole graph incorrectly. Skip any edge whose `dist[u]` is still `\u221e`.",
 "Minimum Spanning Tree \u2014 Kruskal + Union-Find": "Adding before union-check. *Example:* edges `[(A,B,1),(B,C,2),(A,C,3)]`. After adding the first two, A-B-C are connected. If you add `(A,C,3)` without `find(A) != find(C)`, you form a cycle and inflate the total. Trust `union`'s return.",
 "Union-Find (Disjoint Set Union)": "Union without rank/size. *Example:* union(1,2), union(2,3), union(3,4)... chains linearly if you always attach the same way \u2192 `find(1)` walks all n nodes. Union **by rank** (attach shorter to taller) keeps the tree flat.",
 "Clone Graph & Bipartite (traversal bookkeeping)": "Using a set-based visited map for the clone. *Example:* graph `1-2-1`. A plain `Set<Node>` marks `1` visited but can't return its clone when you re-encounter it via `2`. Use `Map<original, clone>` \u2014 it answers both \"seen?\" and \"which copy?\".",
 "Bridges & Articulation Points (Tarjan) \u2014 Critical Connections": "Treating the parent edge as a back-edge. *Example:* tree edge `u\u2192v`. When DFS from `v` looks at neighbours, `u` is in the list \u2014 if you count `u` as a back-edge, `low[v]` drops to `disc[u]` and you miss real bridges. Skip the single parent edge.",
 "Eulerian Path (Hierholzer) \u2014 Reconstruct Itinerary": "Emitting nodes in visit-order (appending). *Example:* tickets `[[JFK,SFO],[JFK,ATL],[ATL,JFK]]`. Appending gives `JFK,SFO,ATL,JFK` \u2014 wrong. Emit only when a node is stuck (no outgoing edges left), and **prepend** \u2014 the reversed exhaustion order is the Eulerian trail.",
}

def apply(root):
    changed = 0; inserted = 0; missed = []
    for f in sorted(os.listdir(root)):
        if not re.match(r'^(3\d|4\d|5\d|6[0-5])-', f): continue
        path = os.path.join(root, f)
        txt = open(path, encoding="utf-8").read()
        orig = txt
        parts = re.split(r'(?m)^(## .+)$', txt)
        rebuilt = [parts[0]]
        for i in range(1, len(parts), 2):
            header = parts[i]
            body = parts[i+1] if i+1 < len(parts) else ''
            title = header[3:].strip().replace('&amp;','&')
            new_trap = TRAP.get(title)
            if new_trap:
                trap_pattern = re.compile(r'^> \[trap\] \*\*Common Trap\*\* [\u2014-] [^\n]+', re.MULTILINE)
                new_body, n = trap_pattern.subn(f"> [trap] **Common Trap** \u2014 {new_trap}", body, count=1)
                if n:
                    body = new_body; changed += 1
                else:
                    # No existing trap: insert one right before "### Same pattern" (or before end)
                    trap_line = f"> [trap] **Common Trap** \u2014 {new_trap}\n\n"
                    m = re.search(r'\n### Same pattern, new tweaks', body)
                    if m:
                        body = body[:m.start()+1] + trap_line + body[m.start()+1:]
                        inserted += 1
                    else:
                        # Insert after Complexity section if present, else missed
                        m2 = re.search(r'\n### Complexity\n[^\n]+\n', body)
                        if m2:
                            body = body[:m2.end()] + "\n" + trap_line + body[m2.end():]
                            inserted += 1
                        else:
                            missed.append(title)
            rebuilt.append(header); rebuilt.append(body)
        new_txt = "".join(rebuilt)
        if new_txt != orig:
            open(path, "w", encoding="utf-8").write(new_txt)
    return changed, inserted, missed

if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "src")
    n, ins, missed = apply(root)
    print(f"traps rewritten: {n} | inserted: {ins}")
    if missed:
        print("titles with no trap-line replacement:")
        for t in missed: print("  -", t)
    # any curated key that never matched?
    all_titles = set()
    for f in os.listdir(root):
        if not re.match(r'^(3\d|4\d|5\d|6[0-5])-', f): continue
        for m in re.finditer(r'(?m)^## (.+)$', open(os.path.join(root,f),encoding="utf-8").read()):
            all_titles.add(m.group(1).strip().replace('&amp;','&'))
    unmatched_keys = [k for k in TRAP if k not in all_titles]
    if unmatched_keys:
        print("\ncurated keys with no matching H2 title:")
        for k in unmatched_keys: print("  ~", k)
