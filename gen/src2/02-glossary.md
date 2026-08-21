# Glossary — Words We Use Everywhere

This book is dense, so a handful of terms recur on almost every page. Read these once and the rest of the book stops feeling like jargon.

> [key] **Canonical problem** — the *standard, representative* problem that teaches a pattern in its purest form. When we say "the canonical two-pointer problem is 3Sum," we mean: if you understand this one, you understand the technique, and most variations are small tweaks on it. We deliberately pick **one strong canonical problem per idea** instead of ten near-duplicates.

> [key] **Monotone / monotonic** — a quantity that moves in **one direction only**: it never decreases (non-decreasing) *or* never increases (non-increasing) as you scan. Monotonicity is the secret ingredient behind three whole patterns:
> - **Binary search** needs the *answer* to be monotone: if `x` works then everything larger works too, so a single true/false boundary exists.
> - **Sliding window** needs *validity* to be monotone: once a window is valid, shrinking keeps it comparable, so you never backtrack.
> - **Monotonic stack/deque** literally *maintains* a monotone sequence so the next-greater/smaller element pops out in O(1).
>
> Example: in `[1,2,4,7,11]` the prefix sums `1,3,7,14,25` only increase — monotone — so you can binary-search for "first prefix ≥ 10." In `[1,-2,3]` prefix sums `1,-1,2` go down then up — **not** monotone — which is exactly why "subarray sum = k with negatives" cannot use a window and needs a hash map instead.

> [inv] **Invariant** — a statement that is **true at every step** of a loop or recursion — before it starts, after every iteration, and when it ends. It is the backbone of a correctness argument: if the invariant holds at the end and the loop has terminated, the answer must be right. Example (binary search): "the target, if present, is always inside `[lo, hi]`." Each step preserves this while shrinking the range, so when the range is empty you can conclude the target is absent.

> [note] **Amortized cost** — the *average* cost per operation across a worst-case **sequence** of operations, not a probabilistic average. A single operation may be expensive, but if expensive ones are rare enough that a long run averages out cheap, the amortized cost is low. Example: appending to an `ArrayList` is usually O(1), but occasionally the array is full and a resize copies all `n` elements (O(n)). Because resizes double the capacity, `n` appends cost ≤ `2n` total — **O(1) amortized**.

> [note] **Prefix (of an array/string)** — the first `k` elements, `a[0..k-1]`. A **prefix sum** is the running total of a prefix; a **prefix** in a trie is the leading characters of a word. "Suffix" is the mirror image — the last elements.

> [note] **Feasibility / feasible** — a yes/no test asking "is answer `x` achievable?" Used in *binary search on the answer*: e.g. "can Koko eat all bananas in `h` hours at speed `x`?" If feasibility is monotone in `x`, we binary-search the smallest feasible `x`.

> [note] **In place** — modifying the input using O(1) extra memory (beyond the input itself), rather than allocating a new structure. Example: reversing an array by swapping ends inward.

> [note] **Stable (sort)** — equal elements keep their original relative order after sorting. Matters when you sort by one key but want ties broken by prior order. Java's `Arrays.sort` on **objects** is stable (Timsort); on **primitives** it is not (dual-pivot quicksort).

> [note] **Two's-complement / overflow** — Java's `int` is 32-bit signed, so values above `2³¹−1 ≈ 2.1×10⁹` **wrap around** to negative. Any sum, product, or `a - b` that can exceed this must use `long`, and comparators should use `Integer.compare(a,b)` rather than `a - b`.

> [note] **DAG** — Directed Acyclic Graph: a directed graph with no cycles. Prerequisite/ordering problems live here; topological sort only exists for a DAG.

> [note] **Subarray / substring / subsequence** — three things people mix up. A **subarray** is a *contiguous* slice of an array — e.g. `[2,3,4]` taken from `[1,2,3,4,5]`. A **substring** is the same idea for text: contiguous characters — `"ell"` from `"hello"`. A **subsequence** keeps the original order but is allowed to *skip* elements, so it need **not** be contiguous — `[1,3,5]` is a subsequence of `[1,2,3,4,5]`, and `"hlo"` is a subsequence of `"hello"`. Rule of thumb: *sub-array / sub-string* ⇒ contiguous (think sliding window); *subsequence* ⇒ pick-and-skip (think DP).

> [note] **DFS & BFS** — the two ways to explore a tree or graph. **DFS (Depth-First Search)** dives as deep as it can down one path, then backtracks — written with recursion or an explicit stack. **BFS (Breadth-First Search)** explores in rings: everything one step away, then two steps, and so on — written with a queue. On an *unweighted* graph BFS finds shortest paths (fewest edges); DFS is the natural fit for "visit everything," cycle detection, and topological order.

> [note] **Memoization vs tabulation** — the two ways to write a DP. **Memoization** is *top-down*: keep your natural recursion but cache each subproblem's answer the first time you compute it, so it's never recomputed. **Tabulation** is *bottom-up*: fill a table from the base cases upward, no recursion. Same answers and same Big-O — memoization is easier to write; tabulation avoids deep recursion and is often a bit faster.

> [note] **Optimal substructure & overlapping subproblems** — the two properties that signal DP. **Optimal substructure:** an optimal answer is assembled from optimal answers to smaller pieces (the cheapest way to make 11¢ builds on the cheapest way to make a smaller amount). **Overlapping subproblems:** the same smaller question keeps recurring, so naive recursion redoes work and caching pays off. Both true ⇒ DP. If only optimal substructure holds *and* a locally best choice is provably safe, greedy may work instead.

> [note] **Recurrence (relation)** — an equation that defines a quantity in terms of smaller instances of itself, e.g. `T(n) = 2T(n/2) + O(n)` reads "the work on `n` items = two half-size subproblems + O(n) to combine." Matching a recurrence to a known form (see the Master-theorem shortcuts) gives the Big-O without tracing every call.

> [note] **Exchange argument** — the standard proof that a greedy choice is safe. Take any optimal solution, swap one of its decisions for the greedy one, and show the result is no worse; repeat until it *is* the greedy solution. If every swap is harmless, greedy must be optimal.

> [note] **Pivot & partition** — the engine of Quicksort/Quickselect. A **pivot** is a chosen reference element. To **partition** is to rearrange the array so everything smaller than the pivot ends up on its left and everything larger on its right — after which the pivot sits at its final sorted position. Quicksort then recurses into *both* sides; Quickselect recurses into *only* the side that contains the rank it's hunting for.

> [note] **Relaxation (shortest paths)** — attempting to shorten a node's best-known distance using one edge: if `dist[u] + weight(u,v) < dist[v]`, lower `dist[v]`. Dijkstra and Bellman–Ford are just different disciplined orders of relaxing edges until nothing improves.

> [note] **Spanning tree & MST** — a **spanning tree** of a connected graph keeps every vertex connected using exactly `V−1` edges and no cycle. A **Minimum Spanning Tree (MST)** is the spanning tree of least total edge weight — "connect everything as cheaply as possible" (built by Kruskal or Prim).
