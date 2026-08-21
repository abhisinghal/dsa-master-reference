## Algorithm Pattern Decision Tree

This is the most-used page in the book. Given an unfamiliar problem, run its **structural signals** through this triage to generate a ranked list of candidate patterns. You are not committing — you are forming hypotheses to test against the problem's preconditions.

### The triage

```diagram
{"type":"flow","width":520,"box":300,"title":"Triage, part 1 \u2014 structure of the input",
 "steps":[
  {"type":"start","text":"Unknown problem"},
  {"type":"decision","text":"Contiguous subarray / substring?","yes":"no",
    "branch":{"label":"yes","role":"green","text":"Sliding Window\nor Prefix Sum"}},
  {"type":"decision","text":"Sorted, or monotonic answer space?","yes":"no",
    "branch":{"label":"yes","role":"green","text":"Binary Search\n(or on the answer)"}},
  {"type":"decision","text":"Top-K / k-th / streaming extreme?","yes":"no",
    "branch":{"label":"yes","role":"green","text":"Heap / Quickselect"}},
  {"type":"decision","text":"Nearest greater / smaller element?","yes":"no",
    "branch":{"label":"yes","role":"green","text":"Monotonic Stack"}},
  {"type":"end","text":"None fired \u2192 continue to part 2"}
 ]}
```

```diagram
{"type":"flow","width":520,"box":300,"title":"Triage, part 2 \u2014 relationships & structure of the answer",
 "steps":[
  {"type":"start","text":"Still unclassified"},
  {"type":"decision","text":"Ordering with dependencies?","yes":"no",
    "branch":{"label":"yes","role":"green","text":"Topological Sort"}},
  {"type":"decision","text":"Connectivity / grouping?","yes":"no",
    "branch":{"label":"yes","role":"green","text":"Union-Find / DFS / BFS"}},
  {"type":"decision","text":"Overlapping subproblems + optimal substructure?","yes":"no",
    "branch":{"label":"yes","role":"green","text":"Dynamic Programming"}},
  {"type":"decision","text":"Enumerate all valid configurations?","yes":"no",
    "branch":{"label":"yes","role":"green","text":"Backtracking"}},
  {"type":"end","text":"Intervals \u2192 Merge / Sweep Line / Heap"}
 ]}
```

### Signal \u2192 pattern lookup

| Signal in the problem | Primary pattern | Secondary |
|---|---|---|
| "contiguous", "subarray", "substring", window | Sliding Window | Prefix Sum |
| "sum of range", "count subarrays with sum" | Prefix Sum + HashMap | Sliding Window |
| sorted input, or "minimize the maximum / maximize the minimum" | Binary Search (on answer) | Greedy |
| "k largest / smallest / closest / most frequent" | Heap (Top-K) | Quickselect |
| "next greater", "previous smaller", "span", histogram | Monotonic Stack | \u2014 |
| "prerequisites", "build order", "valid ordering" | Topological Sort | DFS cycle check |
| "connected", "provinces", "islands", "accounts merge" | Union-Find / DFS / BFS | \u2014 |
| "number of ways", "min/max cost to reach", "can we partition" | Dynamic Programming | Greedy (verify!) |
| "all permutations / combinations / subsets / partitions" | Backtracking | Bitmask (small n) |
| "intervals", "meetings", "merge", "overlap" | Merge Intervals / Sweep Line | Heap |
| "cycle in list", "find middle", "happy number" | Fast & Slow Pointers | \u2014 |
| "pair summing to target in sorted array", "in-place partition" | Two Pointers | Hashing |
| "shortest path, unweighted" | BFS | \u2014 |
| "shortest path, weighted non-negative" | Dijkstra | \u2014 |
| "minimum spanning tree" | Kruskal / Prim | \u2014 |

### How to use it under pressure

!!! key "Two hypotheses beat one"
    Generate the **top two** candidate patterns, then decide between them by checking preconditions. Example: "count subarrays summing to k" fires both *Sliding Window* and *Prefix Sum + HashMap*. Sliding window requires all-positive numbers (monotone window sum); if negatives are allowed, that precondition fails and you fall back to the prefix-count map. Naming *why* you rejected the first pattern is exactly the senior-level signal interviewers reward.

!!! warning "Greedy is a trap without proof"
    When the tree points to Greedy, you must justify it with an exchange argument or a counterexample search. If you cannot prove the greedy choice is safe, assume the intended solution is Dynamic Programming. See Module 7 and the *Greedy vs DP* comparison in Part III.

### The fallback ladder

If no pattern fires, descend this ladder deliberately: **(1)** brute force to lock in correctness and reveal the bottleneck \u2192 **(2)** sort the input and re-scan for structure \u2192 **(3)** add a hash map to remove a nested scan \u2192 **(4)** ask whether subproblems overlap (DP) \u2192 **(5)** if `n` is tiny, embrace exponential search. Each rung is a concrete, narratable move — never sit in silence.
