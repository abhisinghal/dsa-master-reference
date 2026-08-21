<div class="part-divider">
<div class="pnum">Part IV</div>
<div class="ptitle">Cheat Sheets &amp; Self-Check</div>
<div class="rule"></div>
<div class="pdesc">Last-mile revision. Dense tables and templates to scan in the hour before an interview — complexities, algorithm picks, copy-ready code skeletons, self-check drills, and a checkable index of every problem in the book.</div>
</div>

# Master Cheat Sheets &amp; Templates

## Big-O of common operations

| Algorithm / structure | Time | Space | Note |
|---|---|---|---|
| Binary search | O(log n) | O(1) | sorted / monotone predicate |
| Two pointers / sliding window | O(n) | O(1) | monotone validity |
| Sort (Timsort / merge / heap) | O(n log n) | O(n)/O(1) | Java `Arrays.sort` objects = Timsort |
| Quickselect | O(n) avg / O(n²) | O(1) | randomize pivot |
| Heap push/pop | O(log n) | — | peek O(1), build O(n) |
| HashMap get/put | O(1) avg | O(n) | O(n) adversarial |
| TreeMap ops | O(log n) | O(n) | ordered, floor/ceiling |
| BFS / DFS | O(V+E) | O(V) | traversal |
| Topological sort | O(V+E) | O(V) | Kahn / DFS |
| Dijkstra (heap) | O(E log V) | O(V+E) | weights ≥ 0 |
| Bellman–Ford | O(V·E) | O(V) | negative edges |
| Floyd–Warshall | O(V³) | O(V²) | all-pairs, small V |
| MST (Kruskal/Prim) | O(E log E) | O(V) | DSU / heap |
| Union-Find op | O(α(n)) ≈ O(1) | O(n) | compression + rank |
| Trie op | O(L) | O(Σ·nodes) | L = key length |
| Fenwick / Segment tree | O(log n) | O(n) | range query/update |
| DP (typical) | O(states × transition) | O(states) | collapse dims |

## Sorting algorithms

| Sort | Best | Avg | Worst | Space | Stable | When |
|---|---|---|---|---|---|---|
| Merge | n log n | n log n | n log n | O(n) | yes | stable, linked lists, external |
| Quick | n log n | n log n | n² | O(log n) | no | in-place, cache-friendly (avg) |
| Heap | n log n | n log n | n log n | O(1) | no | guaranteed n log n, in-place |
| Timsort (Java objects) | n | n log n | n log n | O(n) | yes | real-world, partially sorted |
| Counting / radix | n+k | n+k | n+k | O(n+k) | yes | bounded integer keys |
| Insertion | n | n² | n² | O(1) | yes | tiny / nearly sorted |

> [key] **Key Insight** — Java: `Arrays.sort(primitive[])` is dual-pivot quicksort (not stable); `Arrays.sort(Object[])` / `Collections.sort` is Timsort (stable). Need stability on primitives? Box them or sort indices.

## Graph algorithm selector

| Need | Use |
|---|---|
| Reachability / components | DFS, BFS, or Union-Find |
| Shortest path, unweighted | BFS |
| Shortest path, weights ∈ {0,1} | 0-1 BFS (deque) |
| Shortest path, weights ≥ 0 | Dijkstra |
| Shortest path, negative edges | Bellman–Ford (detect neg cycle) |
| All-pairs shortest, small V | Floyd–Warshall |
| Order under prerequisites | Topological sort |
| Cycle in directed graph | DFS 3-color / topo incompleteness |
| Cycle in undirected graph | Union-Find / DFS parent check |
| Min cost to connect all | MST (Kruskal + DSU / Prim) |
| Dynamic connectivity | Union-Find |
| Bipartite check | 2-coloring BFS/DFS |

## Binary search templates

```java
// (A) Find target index, or -1 — classic closed interval.
int lo = 0, hi = n - 1;
while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;
    if (a[mid] == target) return mid;
    else if (a[mid] < target) lo = mid + 1;
    else hi = mid - 1;
}
return -1;

// (B) First index where predicate P is true — half-open [lo, hi).
int lo = 0, hi = n;              // hi returned if none
while (lo < hi) {
    int mid = lo + (hi - lo) / 2;
    if (P(mid)) hi = mid;        // keep mid as candidate
    else        lo = mid + 1;
}
return lo;                       // = lower_bound

// (C) Binary search on the answer.
long lo = minAns, hi = maxAns;
while (lo < hi) {
    long mid = lo + (hi - lo) / 2;
    if (feasible(mid)) hi = mid; // minimize feasible x
    else               lo = mid + 1;
}
return lo;
```

> [inv] **Invariant** — Template (B): `P(lo-1)` false, `P(hi)` true. Pick one template style and reuse it everywhere to avoid boundary bugs.

## Traversal templates

```java
// BFS (shortest path in unweighted graph / level order)
Queue<Integer> q = new ArrayDeque<>();
boolean[] seen = new boolean[n];
q.offer(src); seen[src] = true;
int dist = 0;
while (!q.isEmpty()) {
    for (int i = q.size(); i > 0; i--) {     // one layer
        int u = q.poll();
        for (int v : adj[u]) if (!seen[v]) { seen[v] = true; q.offer(v); }
    }
    dist++;
}

// DFS (recursive)
void dfs(int u, boolean[] seen, List<Integer>[] adj) {
    seen[u] = true;
    for (int v : adj[u]) if (!seen[v]) dfs(v, seen, adj);
}

// Grid directions
int[][] DIR = {{1,0},{-1,0},{0,1},{0,-1}};   // add diagonals for 8-dir
```

## Backtracking template

```java
void backtrack(State s) {
    if (isComplete(s)) { record(s); return; }
    for (Choice c : choices(s)) {
        if (!valid(c, s)) continue;   // prune
        apply(c, s);                  // choose
        backtrack(s);                 // explore
        undo(c, s);                   // un-choose
    }
}
```

## DP design checklist

```text
[ ] STATE captures ALL future-relevant info (add a dimension if two same-state
    situations can diverge).
[ ] TRANSITION enumerates every last decision correctly.
[ ] BASE CASES seeded (empty prefix row/col, dp[0]).
[ ] ORDER computes dependencies first (knapsack loop direction!).
[ ] SPACE collapse if dp[i] uses only dp[i-1] (rolling array).
[ ] ANSWER read from the right cell (not always dp[n]).
```

## Pattern → complexity quick recall

| Pattern | Typical time |
|---|---|
| Sliding window / two pointers | O(n) |
| Prefix sum + hashmap | O(n) |
| Monotonic stack/deque | O(n) |
| Binary search (+ on answer) | O(log n) / O(n log range) |
| Heap top-k / k-way merge | O(n log k) / O(N log k) |
| Backtracking | O(branch^depth) |
| Graph BFS/DFS/topo | O(V+E) |
| Dijkstra | O(E log V) |
| Union-Find batch | O(E α(n)) |
| DP | O(states × transition) |
| Bitmask DP | O(2ⁿ × poly) |

## Edge-case &amp; dry-run checklist

Run this list in **phase 6 (Verify)** of every problem — the interviewer is watching for exactly these.

```text
INPUT SHAPE
[ ] empty          — [], "", null, empty grid/list
[ ] single element — n == 1 (windows/pointers degenerate)
[ ] two elements   — smallest case that exercises "both ends"
[ ] all identical  — [5,5,5] (duplicates, dedup logic)
[ ] already sorted / reverse sorted (best & worst for many algos)

VALUES
[ ] negatives and zero (Kadane seed, prefix sums, division)
[ ] overflow — sum/product > 2³¹−1 → use long; mid = lo + (hi-lo)/2
[ ] max constraints — does n = 10⁵ blow O(n²)? does a value hit Integer.MAX?

STRUCTURE-SPECIFIC
[ ] array   — off-by-one at both ends; is the range [lo,hi) or [lo,hi]?
[ ] string  — case, spaces, unicode, empty vs " "
[ ] linked list — head == null, single node, cycle, even/odd length for "middle"
[ ] tree    — null root, single node, skewed (linked-list shaped), unbalanced
[ ] graph   — disconnected components, self-loops, isolated node, cycle

CORRECTNESS MOVES
[ ] trace the given example line by line — does your code reproduce it?
[ ] state final TIME and SPACE out loud
[ ] does the answer come from the right variable / cell?
```

> [trap] **The bug you'll actually ship** — integer overflow in `(lo + hi) / 2`, a sum that should be `long`, or a `best = 0` seed on an all-negative array. Say "let me check overflow" *before* the interviewer does.

## Java interview-hygiene checklist

- Use `ArrayDeque` for stacks/queues; never `Stack` or `LinkedList` for these.
- `map.getOrDefault(k, 0)`, `map.merge(k, 1, Integer::sum)`, `computeIfAbsent`.
- `long` for sums/products that can exceed `2³¹−1`; `1L << k` for high bits; `>>>` for logical shift.
- Comparators: `Integer.compare(a, b)` / `Long.compare` — never `a - b` on large ints (overflow).
- `int[26]` frequency vector over `HashMap<Character,Integer>` for fixed alphabets.
- Grid cells as `int[]{r, c}`; predefine a `DIR` array.
- Copy collections before storing (`new ArrayList<>(path)`) in backtracking/BFS results.
- Guard linked-list fast pointers: `fast != null && fast.next != null`.

> [key] **Final Recognition Mantra** — *Contiguous* → window/prefix. *Sorted / monotone* → binary search. *Nearest greater/smaller* → monotonic stack. *Top-k / kth* → heap / quickselect. *Dependencies* → topo sort. *Connectivity* → DFS/BFS/DSU. *All combinations* → backtracking. *Overlapping subproblems* → DP. *Intervals* → sort + sweep/merge. *n ≤ 20* → bitmask. Name the family first; the algorithm follows.
