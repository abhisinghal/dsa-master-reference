## The Recognition Framework

Unknown problems are solved by converting ambiguity into testable hypotheses. Do not jump from prompt → code; move through a repeatable pipeline that exposes constraints, rejects invalid patterns, and produces an invariant you can defend.

```diagram
{"type":"flow","width":560,"box":320,"title":"Unknown problem recognition framework","steps":[{"type":"start","text":"Clarify inputs, outputs, constraints"},{"type":"process","text":"Classify structural signals\ncontiguous? sorted? graph? choices?"},{"type":"process","text":"Hypothesize top two patterns\nprimary + fallback"},{"type":"decision","text":"Do preconditions hold?\nmonotonicity, weights, signs, acyclicity","yes":"yes","branch":{"label":"no","role":"red","text":"Reject pattern\nand test fallback"}},{"type":"process","text":"Pick data structures\nmap, set, heap, deque, DSU, DP table"},{"type":"process","text":"State invariant\nwhat is always true after each step?"},{"type":"process","text":"Code from invariant\nnot from examples"},{"type":"end","text":"Test edge cases + complexity claim"}]}
```

| Step | What to say | What you are proving |
|---|---|---|
| Clarify | "Can values be negative? Are duplicates allowed? Need one answer or all?" | Preconditions, not preferences. |
| Classify signals | "This asks about a contiguous substring and a maximum length." | The problem has a recognizable structure. |
| Hypothesize two patterns | "Sliding window is first; prefix counts is the fallback if negatives break monotonicity." | You are not overfitting to a memorized solution. |
| Check preconditions | "Window sum only moves monotonically if all numbers are non-negative." | The selected pattern is legal. |
| Pick data structures | "I need a `HashMap<Integer, Integer>` of prefix frequencies, not just a set, because counts matter." | Operations meet the target complexity. |
| State invariant | "Before processing `i`, the map contains prefixes ending before `i`." | Correctness can be reasoned locally. |
| Code | "I'll update the answer before inserting the current prefix to avoid counting an empty future interval." | Ordering bugs are controlled. |
| Test | "Empty input, single element, duplicates, overflow, and the example." | The implementation matches the invariant. |

!!! key "Senior-level recognition"
    The strongest signal is not naming the pattern quickly; it is naming the **precondition** that makes the pattern valid and the fallback when that precondition fails.

## From Brute Force to Optimal

Start with the brute force only long enough to identify the repeated work. Then remove exactly one bottleneck at a time. This keeps the interview grounded: every optimization has a reason, and every data structure earns its place.

| Repeated work / bottleneck | Remedy | Usually becomes |
|---|---|---|
| Re-scanning a range for sum/count/min/max | Maintain running state while expanding/shrinking | Sliding Window |
| Recomputing range sums | Precompute cumulative state | Prefix Sum |
| Nested lookup for "have we seen complement/state?" | Store previous states in `HashMap` / `HashSet` | Hashing, Prefix Count |
| Trying every split/index in a sorted or monotone domain | Eliminate half by predicate | Binary Search / Search on Answer |
| Sorting just to keep top `k` | Keep bounded extreme set | Heap of size `k` |
| Repeatedly finding next greater/smaller | Maintain candidates in monotone order | Monotonic Stack / Deque |
| Re-solving same suffix/subtree/state | Memoize state or tabulate | Dynamic Programming |
| Re-checking connectivity after each union | Maintain components incrementally | Union-Find |
| Re-exploring graph nodes through many paths | Mark discovered/settled states | BFS / DFS / Dijkstra |
| Enumerating invalid branches | Prune using feasibility constraints | Backtracking |
| Comparing all interval pairs | Sort endpoints and sweep once | Merge Intervals / Sweep Line |

A useful ladder:

1. **Lock correctness:** write the brute-force recurrence or loops in words.
2. **Name the bottleneck:** "For each right endpoint I rescan all left endpoints."
3. **Ask what would make it O(1):** cached sum, last index, frequency, min/max candidate, best subproblem.
4. **Choose the structure:** map for arbitrary keys, array for dense keys, heap for partial order, deque/stack for monotonic candidates.
5. **Prove no information was lost:** the optimized state must answer exactly the query the brute force asked.

!!! tip "Optimization narration"
    Say: "The brute force is useful because it reveals the query I need to answer repeatedly. I will maintain exactly that query incrementally." That sounds deliberate, not lucky.

## Estimating the Target Complexity from Constraints

Constraint reading is a design input. Estimate the upper bound before choosing a pattern; it prevents both over-engineering and under-solving.

| `n` or state size | Likely acceptable | Typical patterns | Red flags |
|---:|---|---|---|
| `n ≤ 20` | `O(2^n)`, `O(n · 2^n)`, sometimes `O(n!)` | Backtracking, bitmask DP, subsets | Missing pruning may still TLE for permutations. |
| `n ≤ 30–40` | Meet-in-the-middle, `O(2^(n/2))` | Subset split + sort/hash | Plain `2^n` too large. |
| `n ≤ 100` | `O(n^3)` maybe, `O(n^2)` safe | Interval DP, Floyd-Warshall | Hidden dimension can make `n^4`. |
| `n ≤ 1,000` | `O(n^2)` | Classic DP, pair enumeration | `O(n^3)` likely risky in Java. |
| `n ≤ 10^5` | `O(n log n)` or `O(n)` | Sorting, heap, maps, BFS/DFS, binary search | Nested loops are almost always wrong. |
| `n ≤ 10^6` | `O(n)` or tight `O(n log n)` | Linear scan, counting, prefix, union-find | High constants and object churn matter. |
| `n ≤ 10^9` | `O(log n)`, `O(√n)`, math | Binary search, number theory | Cannot allocate arrays of size `n`. |
| Graph: `V,E ≤ 10^5` | `O(V+E)` or `O(E log V)` | BFS/DFS, topological sort, Dijkstra | Matrix graph is too large. |
| Grid: `R·C ≤ 10^6` | `O(R·C)` | Multi-source BFS, DFS iterative | Recursive DFS may overflow. |

Also inspect value bounds: if sums/products can exceed `int`, use `long`; if keys are small and dense, an array beats `HashMap`; if strings are long, account for substring copying and hashing.

## Narrating in the Interview

Think aloud as a sequence of commitments and checks. Interviewers are not scoring a monologue; they are scoring whether your decisions are justified, reversible, and implemented safely.

| Moment | Strong narration | What senior interviewers score |
|---|---|---|
| Prompt intake | "I want to clarify signs, duplicates, and whether any valid answer is enough." | Requirements discipline. |
| Brute force | "The obvious `O(n^2)` tries every interval; correctness is clear but repeated sums are the bottleneck." | Baseline correctness before optimization. |
| Pattern choice | "Sliding window works only if the condition is monotone as I move `right`; otherwise I need prefix counts." | Preconditions and tradeoff awareness. |
| Invariant | "At loop start, all candidates in the deque are inside the window and decreasing by value." | Ability to reason beyond examples. |
| Edge cases | "I'll test empty, one element, all equal, duplicates, overflow, and no-solution." | Production-quality caution. |
| Complexity | "Each index enters and leaves the deque once, so total time is linear." | Amortized reasoning. |

Avoid narrating every keystroke. Narrate **why** you branch, **what invariant** your code maintains, and **how** each test targets a known failure mode.
