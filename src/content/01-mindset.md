## The DSA Interview Mindset

At the senior and staff level, interviewers are not checking whether you *know* an algorithm. They assume you do. They are watching **how you navigate from a problem you have never seen to a correct, efficient solution** — and whether you can justify every decision. This chapter installs the mental operating system the rest of the book runs on.

### Recognition beats recall

The single highest-leverage skill is **pattern recognition**: mapping a novel problem onto a small set of reusable techniques. There are only about twenty patterns in this book, and the overwhelming majority of interview questions are thin disguises over one or two of them.

!!! key "The recognition loop"
    Read the problem \u2192 extract its *structural signals* (sorted? contiguous? top-k? dependencies? overlapping subproblems?) \u2192 hypothesize a pattern \u2192 check whether the pattern's precondition holds \u2192 derive the algorithm from the pattern's invariant. If the precondition fails, discard and try the next hypothesis. This loop, run out loud, is exactly what interviewers score.

### From brute force to optimal — always

Never freeze trying to produce the optimal solution first. The professional move is to **state the brute force immediately**, analyze its complexity, and then attack its bottleneck.

```diagram
{"type":"flow","width":470,"box":300,"title":"The universal solving pipeline",
 "steps":[
  {"type":"start","text":"Restate problem + clarify constraints"},
  {"type":"process","text":"Brute force + its complexity"},
  {"type":"decision","text":"Where is the waste?","yes":"identify bottleneck",
    "branch":{"label":"none","text":"brute force IS optimal\n\u2014 code it"}},
  {"type":"process","text":"Match bottleneck to a pattern\n(precompute? order? prune?)"},
  {"type":"process","text":"Derive algorithm from invariant"},
  {"type":"process","text":"Verify on example + edge cases"},
  {"type":"end","text":"Code, then test"}
 ]}
```

The bottleneck almost always has a canonical remedy:

| Brute-force waste | Remedy | Pattern |
|---|---|---|
| Re-scanning for membership | hash set / map | Arrays & Hashing |
| Re-summing a range | prefix sum / difference array | Prefix Sum |
| Re-searching a sorted space | binary search | Binary Search |
| Re-computing overlapping subproblems | memo / table | Dynamic Programming |
| Re-finding next greater/smaller | monotonic stack | Monotonic Stack |
| Re-sorting to get extremes | heap | Top-K / Heap |
| Re-exploring the same window | sliding window | Sliding Window |

### Extract the invariant

An **invariant** is a property that is true before and after every step of your algorithm. Correctness proofs, off-by-one bugs, and loop termination all flow from a clearly stated invariant. Throughout this book, every canonical solution names its invariant explicitly — because *if you can state the invariant, you can reconstruct the code from memory under pressure.*

!!! tip "Say the invariant out loud"
    "At the top of each loop, `left` is the smallest index for which the window `[left,right]` is still valid." That one sentence encodes the entire sliding-window solution. Interviewers relax visibly when they hear it, because it signals you understand *why*, not just *what*.

### Complexity is a design tool, not an afterthought

The target complexity is usually inferable from the constraints **before you write any code**:

| Input size `n` | Plausible target | Signals |
|---|---|---|
| `n \u2264 20` | O(2\u207f) / O(n!) | subsets, permutations, bitmask DP |
| `n \u2264 500` | O(n\u00b3) | interval DP, Floyd\u2013Warshall |
| `n \u2264 5000` | O(n\u00b2) | pairwise DP, LIS (n\u00b2) |
| `n \u2264 10\u2075\u201310\u2076` | O(n log n) / O(n) | sort, heap, sliding window, binary search |
| `n \u2265 10\u2077` | O(n) / O(log n) | streaming, math, two pointers |

!!! warning "Read the constraints first"
    If `n \u2264 20`, the interviewer is *inviting* exponential search — stop hunting for a clever polynomial trick. If `n = 10\u2076`, an O(n\u00b2) idea is dead on arrival; jump straight to sorting, hashing, or a linear scan.

### Communication is part of correctness

State your assumptions, think aloud, and drive the whiteboard. A correct solution delivered in silence scores worse than a near-correct solution narrated with clear pattern reasoning. The chapters that follow give you the vocabulary — patterns, invariants, and complexity — to narrate fluently.
