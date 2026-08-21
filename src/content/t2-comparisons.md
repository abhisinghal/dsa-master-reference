## Common Interview Traps

!!! pitfall "Integer overflow"
    `int` overflows silently in Java. Use `long` for sums, products, distances, midpoint-like arithmetic over large bounds, and multiplication in feasibility checks. Prefer `lo + (hi - lo) / 2` and compare with `Long.compare` / `Integer.compare`, not subtraction.

!!! pitfall "Off-by-one binary search"
    Decide the contract before coding: closed interval `[lo, hi]` or half-open `[lo, hi)`. For search-on-answer, keep a monotone predicate and return the first/last feasible value deliberately. If the loop is `while (lo < hi)`, every branch must strictly shrink the interval.

!!! pitfall "Unstable or overflowing comparators"
    Never write `(a, b) -> a - b` for arbitrary integers. It can overflow and violate comparator transitivity. Use `Integer.compare(a, b)`, `Long.compare(a[0], b[0])`, or `Comparator.comparingInt(x -> x.field)`.

!!! pitfall "Mutating during iteration"
    Do not structurally modify a `List`, `Map`, or `Set` inside an enhanced `for` loop over the same collection. Use an `Iterator` with `remove`, collect changes separately, or iterate by index when safe.

!!! pitfall "Forgetting visited/discovered state in graphs"
    Mark nodes when enqueuing for BFS, not when dequeuing, unless duplicates are intentional. In DFS, distinguish `visiting` from `visited` for cycle detection in directed graphs.

!!! pitfall "Recursion depth in Java"
    Recursive DFS over `10^5` nodes can throw `StackOverflowError`. Prefer iterative `ArrayDeque` traversal for large graphs/grids, or explicitly state the recursion-depth risk.

!!! pitfall "Heap entries becoming stale"
    Dijkstra and streaming top-k often leave old entries in the `PriorityQueue`. On poll, discard entries whose distance/count/version no longer matches the authoritative array/map.

!!! pitfall "Inclusive/exclusive interval confusion"
    Normalize intervals early. For sweep-line counts, decide whether an ending at `t` conflicts with a starting at `t`; that determines endpoint ordering.

!!! pitfall "DP state missing information"
    If two histories with the same state can lead to different futures, the state is incomplete. Add the missing dimension or reformulate the recurrence.

!!! pitfall "Backtracking without undo"
    Every mutation before recursion must be undone on return: path append/remove, used mark/unmark, count decrement/increment. Prefer local immutable values when the state is small.

## Confusable Techniques, Disambiguated

### BFS vs DFS

| Dimension | BFS | DFS |
|---|---|---|
| Data structure | `ArrayDeque` as queue | recursion or `ArrayDeque` as stack |
| Best for | shortest path in unweighted graph, levels | reachability, components, cycle/ordering structure |
| First time seen means | minimum edge count | merely reachable |
| Space | frontier width | depth / stack |

Choose BFS when distance in number of edges or level order matters. Choose DFS when you need exhaustive traversal, connected components, topological cycle detection, or backtracking-style exploration. If the graph is huge and deep in Java, iterative DFS avoids stack overflow.

### BFS vs Dijkstra

| Dimension | BFS | Dijkstra |
|---|---|---|
| Edge weights | all equal / unweighted | non-negative, variable weights |
| Frontier | FIFO queue | min-priority queue |
| Relaxation | first visit is optimal | better distance may be found before settling |
| Complexity | `O(V + E)` | `O((V + E) log V)` |

Use BFS only when every edge has identical cost. The moment costs differ, FIFO order no longer guarantees optimality; use Dijkstra if weights are non-negative. For weights `0` and `1`, use 0-1 BFS with a deque.

### Dijkstra vs Bellman-Ford

| Dimension | Dijkstra | Bellman-Ford |
|---|---|---|
| Weights | non-negative only | negative allowed |
| Negative cycles | not detected | detectable |
| Complexity | `O(E log V)` with heap | `O(VE)` |
| Mechanism | settle nearest unsettled node | relax all edges repeatedly |

Use Dijkstra for normal shortest-path interviews with non-negative weights. Use Bellman-Ford when negative edges exist or the question asks whether a negative cycle is reachable. If all-pairs shortest paths are needed and `V` is small, consider Floyd-Warshall.

### Prim vs Kruskal

| Dimension | Prim | Kruskal |
|---|---|---|
| Grows | one connected tree | forest merged by edges |
| Core structure | heap of crossing edges | sort edges + DSU |
| Good for | dense-ish graph from a start node | edge list, sparse graph |
| Connectivity | naturally visits reachable component | DSU reveals components |

Use Kruskal when edges are already available as a list and sorting is natural. Use Prim when the graph is adjacency-list based and you want to expand from any node using cheapest frontier edges. Both require undirected weighted graphs and produce an MST only if the graph is connected.

### Greedy vs DP

| Dimension | Greedy | Dynamic Programming |
|---|---|---|
| Choice | commit once | compare alternatives over states |
| Proof | exchange argument / stays-ahead | recurrence + induction |
| State | usually small | explicit dimensions |
| Failure sign | local best can block global best | overlapping subproblems present |

Try greedy only when you can prove the local choice is safe. If a counterexample is easy to construct or the prompt asks min/max over many interacting choices, formulate DP. Senior answer: "I would prefer greedy if this exchange holds; otherwise the DP state is..."

### Sliding Window vs Prefix Sum

| Dimension | Sliding Window | Prefix Sum |
|---|---|---|
| Requires | monotone expand/shrink condition | associative cumulative quantity |
| Handles negatives | often no for sum constraints | yes, with hashmap counts |
| Best for | longest/shortest contiguous window | range sum/count queries |
| State | current window | historical prefixes |

Use sliding window when moving one boundary monotonically lets you restore validity. Use prefix sums when you need arbitrary previous boundaries, especially with negative numbers or exact-sum counts. Many problems present both signals; signs and monotonicity decide.

### Two Pointers vs Sliding Window

| Dimension | Two Pointers | Sliding Window |
|---|---|---|
| Shape | two indices moving toward/through data | contiguous interval maintained |
| Typical input | sorted array, partitioning | subarray/substring |
| Invariant | relation between left/right candidates | window validity and aggregate state |
| Output | pair/count/partition | best length/count/value over windows |

Use two pointers for sorted-pair logic, in-place partitioning, or convergence from both ends. Use sliding window when the active segment between pointers is itself the object being optimized and must maintain validity.

### Heap vs Sorting

| Dimension | Heap | Sorting |
|---|---|---|
| Need | incremental extremes | total order once |
| Complexity | `O(n log k)` for top-k | `O(n log n)` |
| Streaming | yes | no, unless buffered |
| Simplicity | more moving parts | often simpler |

Use sorting when all data is known and a complete order or deterministic traversal is useful. Use a heap when only the best `k`, next event, or dynamic extreme is needed. If `k` is close to `n`, sorting may be simpler and competitive.

### Backtracking vs DP

| Dimension | Backtracking | Dynamic Programming |
|---|---|---|
| Goal | enumerate valid objects | count/optimize/decide over repeated states |
| Tree | explores choices explicitly | collapses equivalent subtrees |
| Memoization | optional when states repeat | central |
| Output size | may be exponential | usually polynomial answer |

Use backtracking when the output itself is all combinations, permutations, paths, or partitions. Use DP when many branches converge to the same `(index, remaining, mask, ...)` state and the question asks for count, existence, min, or max rather than listing every object.

### Binary Search vs Binary Search on Answer

| Dimension | Binary Search | Search on Answer |
|---|---|---|
| Search space | array indices | numeric answer domain |
| Predicate | compare `nums[mid]` to target | feasibility of candidate answer |
| Needs sorted array | yes | no, needs monotone feasibility |
| Return | found index / insertion point | minimum feasible or maximum feasible value |

Use ordinary binary search when the data is sorted. Use search-on-answer when the phrase is "minimize the maximum", "maximize the minimum", capacity, speed, days, distance, or threshold, and you can write a monotone `can(x)` check.

### Monotonic Stack vs Heap

| Dimension | Monotonic Stack | Heap |
|---|---|---|
| Order exploited | original index order | priority order independent of index |
| Answers | nearest greater/smaller, spans | global/dynamic min/max |
| Removal | dominated by current element | explicit poll by priority |
| Complexity | `O(n)` amortized | `O(n log n)` or `O(n log k)` |

Use a monotonic stack when the nearest previous/next element in the original sequence matters and each element can eliminate worse candidates. Use a heap when candidates are not ordered by adjacency and you repeatedly need the globally smallest/largest remaining item.
