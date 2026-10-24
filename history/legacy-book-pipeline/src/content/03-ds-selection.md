## Data Structure Selection Guide

Choosing the right container is half the algorithm. This guide maps *what you need to do* to *what you should reach for*, then to the Java type.

### Selection matrix

| You need to\u2026 | Reach for | Java type | Cost |
|---|---|---|---|
| Test membership / dedup | hash set | `HashSet` | O(1)* |
| Map keys \u2192 values, count | hash map | `HashMap` | O(1)* |
| Keep keys sorted; floor/ceiling/range | balanced BST | `TreeMap` / `TreeSet` | O(log n) |
| Repeatedly get the min or max | heap | `PriorityQueue` | O(log n) push/pop |
| LIFO (undo, DFS, matching) | stack | `ArrayDeque` | O(1) |
| FIFO (BFS, streaming) | queue | `ArrayDeque` | O(1) |
| Both ends (sliding-window max) | deque | `ArrayDeque` | O(1) |
| Index-based random access | dynamic array | `ArrayList` / `int[]` | O(1) access |
| Prefix-based string keys / autocomplete | trie | custom nodes | O(L) |
| Merge disjoint groups / connectivity | union-find | `int[] parent` | O(\u03b1(n)) |
| Range sum/min with point updates | Fenwick / segment tree | custom | O(log n) |

!!! tip "Interview defaults"
    Reach for `HashMap`/`HashSet` first — most "make it faster" moves are just *precompute a lookup*. Use `ArrayDeque` for **both** stack and queue (never `java.util.Stack`, which is a synchronized legacy `Vector`). Use `PriorityQueue` the moment the words "k largest / smallest / closest / most frequent" appear.

### Decision flow

```diagram
{"type":"flow","width":500,"box":300,"title":"Which container?",
 "steps":[
  {"type":"start","text":"What is the dominant operation?"},
  {"type":"decision","text":"Need order / sorted keys?","yes":"no",
    "branch":{"label":"yes","role":"primary","text":"TreeMap / TreeSet\n(log n, floor/ceiling)"}},
  {"type":"decision","text":"Only ever need the extreme?","yes":"no",
    "branch":{"label":"yes","role":"primary","text":"PriorityQueue (heap)"}},
  {"type":"decision","text":"Membership / counting?","yes":"no",
    "branch":{"label":"yes","role":"green","text":"HashSet / HashMap"}},
  {"type":"decision","text":"LIFO / FIFO / both ends?","yes":"no",
    "branch":{"label":"yes","role":"green","text":"ArrayDeque"}},
  {"type":"end","text":"Indexable \u2192 ArrayList / array"}
 ]}
```

### The hash-map super-pattern

More interview optimizations reduce to *"store what you have seen so you never recompute it"* than any other idea. The complement-lookup in Two Sum, the prefix-count map in Subarray Sum Equals K, the last-seen index in Longest Substring Without Repeating Characters, and memoization in DP are all the **same move**: trade O(n) space for the removal of a nested O(n) scan.

!!! key "The trade you are always making"
    Almost every speedup in this book is *space for time*: a hash map, a prefix array, a memo table, or a heap that caches a partial order. When stuck, ask "what expensive thing am I recomputing, and could I store it once?"

### Choosing between the close calls

| If deciding between\u2026 | Prefer\u2026 when\u2026 |
|---|---|
| `HashMap` vs `TreeMap` | `TreeMap` only if you need ordering, range, or floor/ceiling |
| heap vs full sort | heap when you need the top-k or a streaming extreme, not the whole order |
| array vs linked list | array almost always (cache locality); list only for O(1) splice given the node |
| BFS vs DFS | BFS for shortest path / level structure; DFS for existence, paths, and recursion-natural problems |
| union-find vs DFS for connectivity | union-find for incremental/streaming unions; DFS for a one-shot static graph |
