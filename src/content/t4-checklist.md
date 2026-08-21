## The Night-Before Pass

Use this as a final invariant audit. You should be able to state each invariant before writing code and test one edge case that would break it.

| Module / template | Checklist |
|---|---|
| Binary search boundaries | - [ ] I can implement closed `[lo, hi]` and half-open `[lo, hi)` without mixing them.<br>- [ ] I can write first-true / last-true search-on-answer.<br>- [ ] I compute `mid = lo + (hi - lo) / 2` and guarantee progress. |
| Sliding window | - [ ] I know the validity condition.<br>- [ ] I know when to shrink: while invalid, or while still valid for minimum length.<br>- [ ] I update the answer at the correct moment for max vs min windows. |
| Prefix sum / prefix count | - [ ] I insert the neutral prefix `0` before scanning when counting from index `0` matters.<br>- [ ] I update answer before inserting current prefix when looking backward.<br>- [ ] I use `long` for large sums. |
| Two pointers | - [ ] I know whether pointers converge, move in parallel, or partition.<br>- [ ] Sortedness or partition invariant is explicit.<br>- [ ] Duplicate skipping happens after recording a valid answer. |
| Dijkstra | - [ ] Distances initialize to infinity except source `0`.<br>- [ ] Relaxation is `if (dist[u] + w < dist[v])` with `long` if needed.<br>- [ ] Stale heap entries are skipped on poll. |
| BFS / DFS | - [ ] BFS marks discovered on enqueue.<br>- [ ] Directed cycle detection uses `visiting` and `visited` states.<br>- [ ] Large Java traversals avoid recursive stack overflow. |
| Dynamic programming | - [ ] State captures all future-relevant information.<br>- [ ] Transition considers every legal previous choice exactly once.<br>- [ ] Base cases cover empty prefix, zero capacity, and impossible states. |
| Union-Find | - [ ] `find` uses path compression.<br>- [ ] `union` uses rank/size and decrements component count only on successful merge.<br>- [ ] Mapping from objects to ids is stable. |
| Monotonic stack / deque | - [ ] The structure is monotone by value and valid by index.<br>- [ ] I know whether to pop `<`, `<=`, `>`, or `>=` for duplicates.<br>- [ ] Each index is pushed and popped at most once. |
| Backtracking | - [ ] Choose → recurse → undo is symmetric.<br>- [ ] Pruning cannot remove a valid solution.<br>- [ ] Duplicates are skipped at the same recursion depth after sorting. |
| Floyd cycle / fast-slow | - [ ] Fast moves two, slow moves one, and null checks are safe.<br>- [ ] For cycle entry, reset one pointer to head and move both one step.<br>- [ ] I can explain the distance equation, not just memorize it. |
| Heap size-`k` idiom | - [ ] For k largest, keep a min-heap and eject when size exceeds `k`.<br>- [ ] For k smallest, keep a max-heap or invert comparator safely.<br>- [ ] Comparator never subtracts. |

!!! key "Last pass priority"
    Do not reread every problem. Rehearse the invariants that prevent bugs: boundary contracts, update ordering, duplicate handling, overflow, and when an item becomes final.

## 60-Second Pattern Recall

| Signal | Pattern to try first | Disqualifier / fallback |
|---|---|---|
| Contiguous subarray/substring with max/min length | Sliding Window | Negative numbers or non-monotone validity → Prefix Sum / DP |
| Exact subarray sum/count | Prefix Sum + HashMap | All positive and length optimization → Sliding Window |
| Sorted array pair/triple | Two Pointers | Need arbitrary lookup → HashSet / HashMap |
| Minimize maximum / maximize minimum | Binary Search on Answer | Predicate not monotone → DP / greedy proof needed |
| k-th / top-k / streaming extreme | Heap | Need full ordered result once → Sorting |
| Nearest greater/smaller, span, histogram | Monotonic Stack | Need global extreme independent of adjacency → Heap |
| Shortest path, unweighted | BFS | Weighted edges → Dijkstra / Bellman-Ford |
| Shortest path, non-negative weights | Dijkstra | Negative edge → Bellman-Ford |
| Connectivity under merges | Union-Find | Need actual path traversal/order → DFS/BFS |
| Prerequisites / build order | Topological Sort | Undirected connectivity only → DFS/DSU |
| Min/max/count ways over choices | DP | No overlapping states and output all choices → Backtracking |
| Enumerate subsets/permutations/partitions | Backtracking | Count only with repeated states → DP |
| Intervals overlap / rooms / calendar | Sort + Sweep / Heap | Static merge only → sort by start and merge |
| Linked list cycle / middle | Fast & Slow Pointers | Need random access → array/list conversion only if allowed |
| Range queries with static array | Prefix / Sparse / Segment Tree | Updates present → Fenwick / Segment Tree |
| Tree path aggregate | DFS with return state | Many arbitrary path queries → LCA / preprocessing |

## Templates You Should Be Able to Write Blind

- [ ] **Binary search first true:** monotone predicate over `[lo, hi]`, shrink toward the first feasible answer.
- [ ] **Binary search last true:** bias `mid` upward or use first false minus one.
- [ ] **Sliding window max length:** expand right, shrink while invalid, record valid window length.
- [ ] **Sliding window min length:** expand right, shrink while valid, record before breaking validity.
- [ ] **Prefix sum count:** `count += freq.getOrDefault(prefix - target, 0)` then increment current prefix frequency.
- [ ] **Two-sum sorted:** move the smaller side up or larger side down based on comparison to target.
- [ ] **BFS levels:** queue size loop for distance/layers; mark on enqueue.
- [ ] **Iterative DFS:** stack plus visited set/state to avoid Java recursion depth failures.
- [ ] **Dijkstra:** priority queue of `(distance, node)`, stale-entry skip, relax outgoing edges.
- [ ] **Topological sort (Kahn):** indegree array, queue zero-indegree nodes, count processed nodes.
- [ ] **Union-Find:** `find`, `union`, component count, path compression, union by size/rank.
- [ ] **0-1 BFS:** deque; weight `0` pushes front, weight `1` pushes back.
- [ ] **Monotonic stack:** pop dominated indices before using/pushing current index.
- [ ] **Monotonic deque window max:** remove expired front, pop smaller back, front is max.
- [ ] **Backtracking:** choose, recurse, undo; skip duplicates at same depth after sorting.
- [ ] **Memoized DP:** key all future-relevant state; cache before returning.
- [ ] **Bottom-up DP:** define table meaning first, then fill in dependency order.
- [ ] **Heap top-k:** bounded heap of size `k`; comparator safe with `Integer.compare`.
- [ ] **Merge intervals:** sort by start, extend current end or emit and start new interval.
- [ ] **Floyd cycle entry:** detect meeting, reset one pointer to head, move both one step.
