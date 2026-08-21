# Appendix: Self-Check &amp; Mastery Drills

You don't *know* a pattern until you can recognize it cold, in a problem you've never seen, phrased in words designed to hide it. This appendix is how you find out. Work each drill **before** peeking at the answer key — cover the answers, commit to a choice out loud, then check. The gap between "I recognized it instantly" and "I had to think" is exactly the list of things left to drill.

There's a companion **interactive** version too — `DSA_MASTER_REFERENCE_Quiz.html` (open it in any browser; it's fully offline) — with a timed Pattern Drill and spaced-repetition flashcards. Use this printed appendix for a cold read; use the HTML for repeated reps.

<Callout kind="note" title="How to score yourself.">

Instant + correct = mastered. Correct but slow (&gt;10 s) = fragile, re-drill weekly. Wrong = go back to that chapter's intro and the "Recognition signals" line. Aim for **instant** on the whole Decision Tree before your interview.

</Callout>

---

## Drill 1 — The Decision Tree, cold

For each cue, name the **pattern** (and the data structure, if one is implied) in one breath. These are worded the way an interviewer would — the pattern name never appears.

| # | Problem cue (as you'd hear it) | Your call |
| --- | --- | --- |
| 1 | "Longest stretch of the array with at most K distinct values." | |
| 2 | "The array is sorted; find two entries that add to a target." | |
| 3 | "For each element, the next element to its right that's bigger." | |
| 4 | "Return the 5th largest number in this unsorted list." | |
| 5 | "Some courses can't start until others are done — can you finish them all?" | |
| 6 | "How many separate islands of land are in this grid?" | |
| 7 | "List every way to make change for N using these coins (each once)." | |
| 8 | "Fewest coins to make amount N; coins reusable." | |
| 9 | "Merge these meeting time ranges that overlap." | |
| 10 | "n ≤ 18 cities; shortest tour visiting all of them." | |
| 11 | "Smallest window in S that contains every character of T." | |
| 12 | "First index where `isBad(version)` flips from false to true." | |
| 13 | "Kth smallest element in a row/column-sorted matrix." | |
| 14 | "Detect whether this linked list has a cycle, O(1) space." | |
| 15 | "Max profit from one buy and one later sell." | |
| 16 | "Are these two account groups the same connected user set?" | |
| 17 | "Return all subsets whose sum equals the target." | |
| 18 | "Cheapest path from A to B, non-negative edge weights." | |
| 19 | "Longest run of consecutive integers in an unsorted array." | |
| 20 | "Reverse the linked list in groups of k." | |

<div class="pagebreak"></div>

### Answer key — Drill 1

1. **Sliding Window** (variable, shrink on &gt;K distinct; `HashMap` count). 2. **Two Pointers** (converging, sorted). 3. **Monotonic Stack** (decreasing, next-greater). 4. **Heap or Quickselect** (kth largest). 5. **Topological Sort** (cycle detection on a DAG). 6. **DFS/BFS flood fill** (or **Union-Find**). 7. **Backtracking** (each coin once → subset enumeration). 8. **DP** (unbounded knapsack / coin-change min). 9. **Intervals** — sort by start, **sweep/merge**. 10. **Bitmask DP** (n ≤ 20, visited-set state). 11. **Sliding Window** (variable, "contains all of T" → need-map). 12. **Binary Search on answer** (monotonic predicate). 13. **Heap** or **Binary Search on value**. 14. **Fast/Slow pointers** (Floyd). 15. **DP / single-pass** (track min-so-far). 16. **Union-Find** (connectivity). 17. **Backtracking** (subset-sum). 18. **Dijkstra** (non-negative → shortest path). 19. **Hashing** (put all in a set, expand from run-starts). 20. **Linked-list reversal** (pointer surgery in k-blocks).

<Callout kind="trap">

If you answered "sort it" for #19, notice the O(n) hash approach beats O(n log n) — the word *consecutive* plus *unsorted* is the tell for a **set**, not a sort.

</Callout>

---

## Drill 2 — Name the invariant

The invariant is the sentence that stays true on every iteration — lose it and your loop is guesswork. Fill in the blank, then check.

| # | Pattern | The invariant is… |
| --- | --- | --- |
| 1 | Sliding Window (variable) | |
| 2 | Binary Search `[lo, hi)` | |
| 3 | Monotonic Stack (next-greater) | |
| 4 | Two Pointers (sorted pair-sum) | |
| 5 | Dijkstra | |
| 6 | Backtracking | |
| 7 | Fast/Slow pointers | |
| 8 | Cyclic Sort | |

### Answer key — Drill 2

1. *The window `[left, right]` always satisfies the constraint after each shrink* — so every recorded answer is valid. 2. *The answer, if it exists, is always inside `[lo, hi)`*; the range only ever shrinks. 3. *The stack holds indices whose "next greater" is still unknown, kept in monotonic order.* 4. *Everything outside `[left, right]` is already proven impossible* — moving the pointer that's too small/large never skips a solution. 5. *Once a node is popped from the min-heap, its shortest distance is final.* 6. *The `path` variable always reflects the choices made so far; every `undo` restores state exactly.* 7. *If a cycle exists, fast gains one step on slow each move, so they must meet inside it.* 8. *After processing index `i`, the value `i+1` sits at index `i`* (numbers 1..n land in their home slots).

---

## Drill 3 — Recurrence → Big-O (say it in one line)

| # | Recurrence / loop shape | Big-O | Why |
| --- | --- | --- | --- |
| 1 | `T(n) = 2T(n/2) + O(n)` | | |
| 2 | `T(n) = 2T(n/2) + O(1)` | | |
| 3 | `T(n) = T(n/2) + O(1)` | | |
| 4 | `T(n) = T(n−1) + O(n)` | | |
| 5 | `T(n) = 2T(n−1) + O(1)` | | |
| 6 | nested loop, inner runs `n, n/2, n/4…` | | |

### Answer key — Drill 3

1. **O(n log n)** — log n levels × O(n) work each (merge sort). 2. **O(n)** — leaf-dominated; work halves per level but doubles in count, geometric sum → O(n) (heapify). 3. **O(log n)** — one branch, halving (binary search). 4. **O(n²)** — n + (n−1) + … = arithmetic series. 5. **O(2ⁿ)** — branching factor 2, depth n (naïve subsets/Fibonacci). 6. **O(n)** — the *sum* `n + n/2 + n/4 + … = 2n` is geometric, not O(n log n); the log-many *terms* fool people.

<Callout kind="key">

The two classic traps: a **geometric** sum (#2, #6) collapses to O(largest term), while a **log-many-equal-terms** sum (#1) gives the extra log factor. Ask "do the terms *shrink* or *stay equal*?" — that one question separates O(n) from O(n log n).

</Callout>

---

## Drill 4 — Spot the trap

Each line has a subtle bug or a wrong instinct. Say what breaks.

1. `mid = (lo + hi) / 2` on a large sorted `int[]`.
2. Comparator `(a, b) -> a - b` to sort `Integer` keys that can be near `Integer.MAX_VALUE`.
3. Using `Stack<Integer>` for a DFS on a hot path.
4. BFS on a weighted graph to get the shortest *cost* path.
5. Backtracking that stores `path` (the live list) directly into the results list.
6. Fast-pointer loop `while (fast.next != null)` for cycle detection.
7. `visited` marked when a node is *dequeued* in BFS instead of when enqueued.

### Answer key — Drill 4

1. **Overflow**: `lo + hi` can exceed `int`. Use `lo + (hi - lo) / 2`. 2. **Overflow** in subtraction → wrong order/negative wraparound. Use `Integer.compare(a, b)`. 3. `Stack` is a synchronized legacy `Vector`; use **`ArrayDeque`**. 4. BFS only finds fewest *edges*, not least *cost* — use **Dijkstra**. 5. You store a reference that later mutates to empty; **copy** it: `new ArrayList<>(path)`. 6. NPE when `fast` itself is null; guard `fast != null && fast.next != null`. 7. Same node gets enqueued many times → blowup; mark visited **on enqueue**.

---

## Drill 5 — Teach it back (rubric)

For each topic, without notes, speak these four sentences aloud. If any sentence stalls, that topic isn't interview-ready.

<div markdown="1" class="teachback">

1. **Recognition** — "I reach for this when the problem says ______."
2. **Core idea** — "The mechanism is ______."
3. **Invariant** — "The thing that stays true every step is ______."
4. **Cost** — "It runs in ______ time and ______ space because ______."

</div>

Run the rubric across: Sliding Window · Two Pointers · Binary Search · Monotonic Stack · Heap/Quickselect · Backtracking · BFS/DFS · Topological Sort · Dijkstra · Union-Find · Trie · DP (1-D, grid, subsequence, interval, bitmask) · Intervals/Sweep · Bit tricks. Fifteen topics × four sentences = your final pre-interview checklist. Green across the board means you're ready.

<Callout kind="key" title="The only mantra that matters:">

name the *family* first (contiguous? sorted? dependencies? overlapping subproblems?), and the specific algorithm falls out of it. Interviewers reward the engineer who says "this is a shortest-path problem" before writing a line — because that sentence is the actual skill.

</Callout>
