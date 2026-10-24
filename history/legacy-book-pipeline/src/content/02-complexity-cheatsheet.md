## Complexity Cheat Sheet

A consolidated, print-friendly reference for the time and space costs you will quote in interviews. Keep this page bookmarked for revision.

### Big-O growth, ranked

```diagram
{"type":"bars","title":"Relative cost as n grows (lower is better)",
 "values":[1,2,4,6,10,16],
 "highlights":{"0":"green","1":"green","2":"accent","3":"amber","4":"amber","5":"red"},
 "caption":"O(1) \u00b7 O(log n) \u00b7 O(n) \u00b7 O(n log n) \u00b7 O(n\u00b2) \u00b7 O(2\u207f) \u2014 left to right"}
```

| Class | Name | Typical source |
|---|---|---|
| O(1) | constant | hash lookup, array index, math formula |
| O(log n) | logarithmic | binary search, balanced BST, heap push/pop |
| O(n) | linear | single scan, two pointers, sliding window, BFS/DFS |
| O(n log n) | linearithmic | comparison sort, heap of n items, divide & conquer |
| O(n\u00b2) | quadratic | nested loops, pairwise DP, naive substring |
| O(n\u00b7k) | pseudo-poly | knapsack (n items, capacity k), coin change |
| O(2\u207f) / O(n!) | exponential / factorial | subsets, permutations, brute-force backtracking |

### Data-structure operation costs

| Structure | Access | Search | Insert | Delete | Notes |
|---|---|---|---|---|---|
| Array | O(1) | O(n) | O(n) | O(n) | contiguous, cache-friendly |
| Dynamic array (`ArrayList`) | O(1) | O(n) | O(1)* | O(n) | *amortized append |
| Hash map/set (`HashMap`) | \u2014 | O(1)* | O(1)* | O(1)* | *expected; O(n) worst |
| Balanced BST (`TreeMap`) | \u2014 | O(log n) | O(log n) | O(log n) | ordered keys, floor/ceiling |
| Binary heap (`PriorityQueue`) | O(1) peek | O(n) | O(log n) | O(log n) | extremum only |
| Stack / Queue (`ArrayDeque`) | \u2014 | O(n) | O(1) | O(1) | LIFO / FIFO |
| Linked list | O(n) | O(n) | O(1)** | O(1)** | **given the node |
| Trie | \u2014 | O(L) | O(L) | O(L) | L = key length |
| Union-Find | \u2014 | O(\u03b1(n)) | O(\u03b1(n)) | \u2014 | near-constant amortized |

### Sorting algorithms

| Algorithm | Best | Average | Worst | Space | Stable | When |
|---|---|---|---|---|---|---|
| Quicksort | O(n log n) | O(n log n) | O(n\u00b2) | O(log n) | no | general in-memory |
| Mergesort | O(n log n) | O(n log n) | O(n log n) | O(n) | yes | stable / linked lists / external |
| Heapsort | O(n log n) | O(n log n) | O(n log n) | O(1) | no | guaranteed, in-place |
| Counting/Radix | O(n+k) | O(n+k) | O(n+k) | O(n+k) | yes | small integer keys |
| Insertion | O(n) | O(n\u00b2) | O(n\u00b2) | O(1) | yes | nearly sorted / tiny n |

!!! note "Java's sorts"
    `Arrays.sort(int[])` is a dual-pivot quicksort (O(n\u00b2) worst case, no stability guarantee). `Arrays.sort(Object[])` and `Collections.sort` use TimSort — stable, O(n log n) worst case. Choose boxed arrays when you need stability.

### Graph algorithms

| Algorithm | Complexity | Use |
|---|---|---|
| BFS / DFS | O(V + E) | traversal, connectivity, unweighted shortest path |
| Topological sort (Kahn/DFS) | O(V + E) | dependency ordering, DAG |
| Dijkstra (binary heap) | O(E log V) | non-negative weighted shortest path |
| Bellman\u2013Ford | O(V\u00b7E) | negative edges, negative-cycle detection |
| Floyd\u2013Warshall | O(V\u00b3) | all-pairs shortest path |
| Kruskal (with DSU) | O(E log E) | MST, edge-sorted |
| Prim (heap) | O(E log V) | MST, dense-friendly |

### Tree & heap operations

| Operation | BST (balanced) | Heap |
|---|---|---|
| find min/max | O(log n) / O(log n) | O(1) min-heap peek |
| insert | O(log n) | O(log n) |
| delete | O(log n) | O(log n) extract |
| build from n items | O(n log n) | **O(n)** heapify |
| ordered traversal | O(n) in-order | not supported |

!!! complexity "The amortized subtlety"
    "Amortized O(1)" (dynamic-array append, hash insert) means the *average over a sequence* is constant, even though a single operation may cost O(n) during a resize/rehash. In interviews, state both the amortized and worst-case bounds — senior interviewers probe the difference.

### Recursion & space

Recursive algorithms consume **O(depth)** stack space even when they allocate nothing on the heap. A DFS on a skewed tree or a linear-recursion (e.g. naive linked-list reversal) is O(n) space; converting to iteration with an explicit `ArrayDeque` makes the space cost visible and controllable.
