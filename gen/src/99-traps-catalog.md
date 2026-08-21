# Traps Catalog

*Every `[trap]` callout in the book, consolidated here for interview-eve revision. Skim in one sitting; each row is 30 seconds. If a trap surprises you, jump to its source chapter for context.*

## Java Data Structures

- **Array (`int[]`, `T[]`)**: — arrays can't grow: to append repeatedly, use `ArrayList`.
- **`ArrayList<T>` — the growable array** — *ConcurrentModificationException*: — never `l.remove(...)` (the list method) inside a for-each loop; it corrupts the iterator and throws.
- **`ArrayDeque<T>` — stack and queue in one**: — do **not** use `java.util.Stack` (synchronized, exposes indexing, iterates bottom-to-top) or `LinkedList` as a deque (pointer chasing, cache-unfriendly).
- **`HashMap<K,V>` / `HashSet<E>`**: — keys must have consistent `hashCode`/`equals`.
- **`PriorityQueue<T>` — the binary heap**: — iterating a `PriorityQueue` does **not** give sorted order; only the root is guaranteed smallest.
- **`PriorityQueue<T>` — the binary heap**: — a heap gives you *one* extreme cheaply, **not** a sorted view and **not** O(log n) arbitrary removal (`remove(x)` is O(n)).
- **Sorting &amp; Comparators — the part everyone fumbles** — *Common Trap (overflow)*: — never write a comparator as `(a,b) -> a - b`.

## Complexity Model

- **Amortized vs worst-case**: — Claiming an inner `while` loop makes an algorithm O(n²).
- **Common recurrences (Master-theorem shortcuts)**: — Java's `PriorityQueue` has **no O(log n) decrease-key**.

## Sliding Window

- **False friends — problems that *look* like sliding window but aren't** — *The classic silent bug*: — a plain sliding window on any of these problems runs, terminates, and returns *a* number.
- **Maximum Average Subarray I (fixed-size warm-up)**: — Integer overflow on `windowSum`.
- **Smallest Subarray With Sum ≥ Target**: — Forgetting the "no window found" case.
- **Longest Substring Without Repeating Characters**: — Not clamping `left` to its previous position.
- **Minimum Window Substring**: — Decrementing `formed` on every removal.
- **Subarray Product Less Than K (counting + at-most-K trick)**: — Values with `0`s or **negatives** break the shrinkable-product argument (`product = 0` never divides back up; negatives flip the inequality direction).
- **Sliding Window Maximum (Monotonic Deque)**: — Storing values, not indices.

## Two Pointers

- **3Sum**: — Missing any of the three duplicate-skips yields repeated triplets.
- **Container With Most Water**: — Moving the taller wall can never help.
- **Squaring a Sorted Array**: — Squaring in place, then sorting.
- **Sort Colors (Dutch National Flag)**: — Advancing `mid` after swapping with `high` skips an unexamined value.
- **Trapping Rain Water**: — Local vs global boundaries.

## Fast/Slow Pointers

- **Linked List Cycle II (Floyd)**: — Only checking `fast != null`.

## Prefix Sum

- **Subarray Sum Equals K**: — Forgetting the `count.put(0,1)` seed drops subarrays that start at index 0.
- **Difference Array (Range Update)**: — Off-by-one at `r+1`; size the array `n+1` so the closing decrement never overflows the bounds.
- **2D Prefix Sum (Range Sum Query 2D)**: — Sign/index errors in the four-term formula, or omitting the `+1` padding — then corner queries read out of bounds.

## Hashing

- **Two Sum**: — Inserting into the map **before** the check makes an element match itself.
- **Group Anagrams**: — Building the count key without a delimiter collides distinct histograms.
- **Product of Array Except Self**: — Reaching for division.
- **Longest Consecutive Sequence**: — Omitting the `x-1` guard makes it O(n²).

## Monotonic Stack

- **Daily Temperatures (Next Greater Element)**: — Storing values instead of indices.
- **Largest Rectangle in Histogram**: — Forgetting the sentinel `0`.

## Binary Search

- **Canonical templates**: — Mixing conventions.
- **Search in Rotated Sorted Array**: — Wrong inclusivity on the "sorted-half" test.

## Binary Search on Answer

- **Koko Eating Bananas (Search on Answer — rate)**: — Feasibility direction flipped.
- **Split Array Largest Sum / Book Allocation (Search on Answer — partition)**: — Wrong feasibility semantics.
- **Median of Two Sorted Arrays (Partition Binary Search)**: — Off-by-one when the total length is odd.

## Top-K / Heap

- **Kth Largest / Top K Frequent**: — Wrong heap polarity.

## K-way Merge

- **Merge Two / K Sorted Lists**: — Not re-feeding the heap.
- **Merge K Sorted Lists / Smallest Range (K-way merge)**: — Popping without re-feeding the same list.

## Merge Intervals

- **Merge Intervals**: — Touching vs overlapping.

## Sweep Line

- **Meeting Rooms II (Minimum Concurrent Intervals)**: — Tie at `start == end`.

## Topological Sort

- **Course Schedule (Topological Sort)**: — Not detecting cycles.

## Union-Find

- **Union-Find (Disjoint Set Union)**: — Union without rank/size.
- **Minimum Spanning Tree — Kruskal + Union-Find**: — Adding before union-check.

## Greedy

- **Jump Game II (Farthest-Reach Greedy)**: — Counting jumps at every step instead of at the frontier.
- **Gas Station (Prefix-Balance Greedy)**: — Skipping the total check.
- **Non-overlapping Intervals (Interval Scheduling)**: — Sorting by start, not end.

## Backtracking

- **Subsets &amp; Combinations (the start-index template)**: — Forgetting to un-choose.
- **Permutations (the used[] template)**: — Duplicates without sort-and-skip.
- **Combination Sum (reuse &amp; pruning)**: — Passing `i+1` when reuse is allowed.
- **N-Queens (constraint occupancy)**: — Wrong diagonal keys.
- **Word Search (grid backtracking)**: — Not restoring the cell on the way back up.

## Divide & Conquer

- **Merge Sort &amp; Count of Smaller Numbers After Self**: — Adding the inversion count `mid - i + 1` on the wrong branch (it belongs to the *right-element-taken* case, where all remaining left elements exceed it) or using `int` for a count that can reach ~n²/2 — use `long`.

## Dynamic Programming

- **1D DP — Climbing Stairs &amp; House Robber**: — Missing a base case.
- **Maximum Subarray (Kadane) — the running-optimum DP**: — Initializing `best = 0`.
- **0/1 Knapsack &amp; Subset-Sum family**: — Wrong capacity direction.
- **Coin Change (unbounded, min count)**: — Sentinel overflow.
- **Grid DP — Unique Paths &amp; Minimum Path Sum**: — Rolling-row overwritten in wrong order.
- **Subsequence DP — LIS, LCS, Edit Distance**: — Strict vs non-decreasing LIS.
- **Interval DP — Matrix Chain / Burst Balloons**: — Iterating the outer loop over `l` (left endpoint) first.
- **State-Machine DP — Stock trading with cooldown**: — Not enumerating all states.
- **Bitmask DP — Travelling Salesman / assignment**: — `n` too large.

## Trie Pattern

- **Word Search II (Trie + Backtracking)**: — Re-adding a word for every path that reaches it.
- **Maximum XOR of Two Numbers (Binary Trie)**: — Comparing bits in the wrong direction.

## Bit Manipulation

- **Single Number I / II / III (XOR)**: — Whole-XOR as split mask.
- **Counting Bits (DP on bits)**: — Recomputing popcount per number.

## Quickselect

- **Quickselect (Kth Largest Element)**: — Bad pivots.

## Math & Number Theory

- **General**: — Overflow.
- **Fast (Binary) Exponentiation — Pow(x, n)**: — Not widening `n` before negating.
- **Euclid's Algorithm — GCD &amp; LCM**: — `a * b` in LCM overflows even when the LCM fits.
- **Sieve of Eratosthenes — Count Primes**: — Starting the inner loop at `2*i` (redundant) or forgetting to widen.
- **Modular Arithmetic &amp; Combinatorics (toolkit)**: — Forgetting `(a − b + MOD) % MOD` when a subtraction can go negative, or applying the mod only at the very end (the intermediate product already overflowed).

## Design

- **LRU Cache**: — Updating the map but not the list, or the list but not the map.
- **Insert Delete GetRandom O(1)**: — Forgetting to update the moved element's index.
- **Reservoir Sampling — uniform pick from a stream**: — Sampling with the wrong probability.

## Arrays

- **Matrix Mechanics (in-place grid manipulation)**: — Forgetting the two `if` guards before the bottom row and left column.
- **Cyclic Sort (the base template)**: — Advancing `i` after every swap skips values you just placed.
- **Find the Missing Number**: — The range is `0..n`, so a value can equal `n` (out of array bounds); guard `nums[i] < n` before swapping or you'll index out of range.
- **Find All Missing / All Duplicate Numbers**: — Using `if (nums[i] != nums[home])` is what makes duplicates safe: when the home slot already holds the same value, swapping would loop forever, so you skip and advance instead.
- **First Missing Positive (Hard)**: — Trying to place out-of-range values.

## Strings

- **Longest Palindromic Substring (Expand Around Center)**: — Only expanding **odd**-length centers.
- **Encode and Decode Strings (Length Prefixing)**: — Fixed delimiter with unescaped payload.

## Linked Lists

- **Reverse a Linked List**: — Losing `next` before rewiring.
- **Reorder / Palindrome via Split-Reverse-Merge**: — Splitting on the wrong middle.
- **LRU Cache (Design)**: — Not updating recency on `get`.

## Stacks & Queues

- **Valid Parentheses**: — Returning `true` without checking `stack.isEmpty()`.
- **Min Stack (O(1) minimum)**: — A single scalar `min` can't be restored after `pop`.

## Trees

- **Traversals (iterative &amp; the recursion skeleton)**: — Iterative in-order missing the "go-left first" phase.
- **Maximum Depth, Balanced, Diameter (post-order aggregation)**: — Edges vs nodes.
- **Lowest Common Ancestor**: — BST logic on a general tree.
- **Validate BST &amp; BST operations**: — Local-only comparison.
- **Serialize / Deserialize (structure encoding)**: — Ambiguity from missing null markers.
- **Construct Tree from Traversals**: — Repeated linear scans.
- **Tree DP (House Robber III)**: — Returning a scalar instead of a state pair.

## Heaps

- **Heap internals in one page** — *Heap-order misconception*: — Printing or iterating a `PriorityQueue` does not produce sorted order.
- **Find Median from Data Stream (Two Heaps)**: — Skipping the rebalance.
- **Find Median from Data Stream (Two Heaps)** — *Overflow Trap*: — `low.peek() + high.peek()` can overflow `int` before division.

## Trie

- **Implement Trie**: — `isEnd` only on leaves.
- **Implement Trie** — *Alphabet Trap*: — The `c - 'a'` index assumes lowercase English.
- **Implementation upgrades you can mention** — *Deletion Trap*: — Never prune a node just because the deleted word used it.

## Graphs

- **Number of Islands (grid flood fill)**: — Marking after recursing.
- **Rotting Oranges (multi-source BFS)**: — Single-source BFS on a multi-source problem.
- **Dijkstra (weighted shortest path, non-negative)**: — Skipping the stale-pop guard.
- **Bellman–Ford (negative edges &amp; negative-cycle detection)**: — Ignoring `∞ + w` overflow.
- **Clone Graph &amp; Bipartite (traversal bookkeeping)**: — Using a set-based visited map for the clone.
- **Bridges &amp; Articulation Points (Tarjan) — Critical Connections**: — Treating the parent edge as a back-edge.
- **Eulerian Path (Hierholzer) — Reconstruct Itinerary**: — Emitting nodes in visit-order (appending).

## Segment / Fenwick Tree

- **Fenwick Tree (Binary Indexed Tree)**: — 0-index vs 1-index confusion.
- **Segment Tree (range query + range update)**: — Forgetting `push` before recursing into children.

---

*Total: 109 traps catalogued across 34 chapters. If you can read this list without confusion, you're interview-ready.*