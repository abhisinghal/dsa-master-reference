# Complexity, Amortization &amp; the Cost Model

Interview optimization is a conversation about **which term dominates** and **what you are trading**. You rarely need formal proofs; you need to name the dominant cost and justify a tradeoff.

## Growth hierarchy
<p class="secgoal"><b>What & why:</b> the ordered ladder of complexity classes from fastest to slowest. Goal — be able to rank any two complexities on sight and name which term dominates, so you can judge whether a solution is fast enough for the given input.</p>

From fastest to slowest, the orders you will actually cite:

`O(1) < O(α(n)) < O(log n) < O(√n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)`

`α(n)` is the inverse-Ackermann function (Union-Find) — ≤ 4 for any realistic `n`, effectively constant.

> [key] **Key Insight** — Drop constants and lower-order terms, but *never* drop them silently in an interview when they change the feasible input size. `O(n log n)` at n=10⁶ is fine; `O(n²)` is not.

## Input-size → target-complexity heuristic
<p class="secgoal"><b>What & why:</b> a table that turns the problem's input limit into the complexity — and therefore the technique — the interviewer expects. Goal — learn to read `n` as a hint so you pick the right approach before writing code.</p>

Use the constraint to reverse-engineer the intended complexity (assume ~10⁸ simple ops/sec):

| n (max) | Feasible complexity | Typical technique |
|---|---|---|
| ≤ 10–12 | O(n!), O(2ⁿ·n) | Permutation backtracking, bitmask DP |
| ≤ 20–24 | O(2ⁿ), O(2ⁿ·n) | Subset enumeration, meet-in-the-middle |
| ≤ 100–500 | O(n³) | Interval DP, Floyd–Warshall |
| ≤ 5·10³ | O(n²) | Pairwise DP, LCS, edit distance |
| ≤ 10⁵–10⁶ | O(n log n) | Sort, heap, binary search, balanced BST |
| ≤ 10⁷–10⁸ | O(n), O(n log log n) | Two pointers, sieve, counting |
| ≥ 10⁹ | O(log n), O(1) | Binary search on answer, math |

> [pat] **Pattern Connection** — Reading `n ≤ 20` almost always means *bitmask/subset*; `n ≤ 500` with pairs/intervals means *O(n³) DP*; huge `n` with a "minimum feasible value" phrasing means *binary search on the answer*.

### Worked example — why `n ≤ 10–12` screams "brute force is fine"
<p class="secgoal"><b>What & why:</b> a plug-in-the-numbers walkthrough of one row of the table above. Goal — see concretely why a tiny bound is a green light for exponential/factorial solutions, and which technique each small bound points to.</p>

A CPU does roughly **10⁸ simple operations per second**, so anything finishing within a few ×10⁸ operations passes in about a second. Now plug in that tiny bound:

- `12! ≈ 4.8 × 10⁸` — right at the edge, but acceptable. This is the cost of trying **every ordering** of 12 items.
- `2¹² × 12 ≈ 49,000` — utterly trivial. This is the cost of trying **every subset** of 12 items and doing O(n) work per subset.

So a constraint that small is not a limitation — it is a **loud hint**. The interviewer is telling you: *an exponential or factorial solution is the intended answer.* Concretely, `n ≤ 10–12` points to:

- **Permutation backtracking — O(n!)** — when the answer depends on *ordering* (arrange all items / visit all cities / assign in sequence). Example: "find the shortest route visiting all 10 cities" — try permutations, or upgrade to bitmask DP.
- **Bitmask DP — O(2ⁿ · n)** — when the answer depends on *which subset* is chosen/used (assignment, "visit all nodes," partition). The set of used elements fits in the bits of one integer.

Contrast: if you *ever* see `n = 10⁵`, an O(n!) or O(2ⁿ) idea is off the table by a factor of astronomically many — that constraint is instead whispering "O(n log n)." **Always read the constraint first, then pick the technique.**

## Amortized vs worst-case
<p class="secgoal"><b>What & why:</b> what "amortized" actually means (average over a worst-case sequence, not probability) and the three arguments that justify it. Goal — confidently defend an O(n) claim when a loop looks quadratic.</p>

**Amortized** = average cost per operation over a worst-case *sequence*, not probabilistic average. Three standard arguments:

- **Aggregate** — dynamic array `push`: n pushes cost ≤ 2n total (geometric resizing) → O(1) amortized. Any single push may be O(n).
- **Banker's / potential** — each cheap op "prepays" credit spent by rare expensive ops. Monotonic stack: each element is pushed and popped at most once → O(n) for n operations even with an inner while-loop.
- **HashMap** — O(1) average `get/put`; O(n) worst case under adversarial collisions (mitigated by treeification to O(log n) in Java 8+).

> [trap] **Common Trap** — Claiming an inner `while` loop makes an algorithm O(n²). If each element enters/leaves the structure once (monotonic stack, sliding window), the total work is O(n) — the amortized argument, not the nested-loop shape, determines the bound.

## Space: count what persists
<p class="secgoal"><b>What & why:</b> how to count memory honestly — recursion stack plus tables — and when a DP can be squeezed to O(1) extra space. Goal — give the correct space bound, not just the time bound.</p>

Recursion stack counts as space. Recursive DFS on a skewed tree/graph is O(h) stack, worst O(n). A DP table is O(states); most 2D DPs collapse to O(min dimension) by keeping only the previous row.

> [inv] **Invariant (rolling DP)** — If `dp[i]` depends only on `dp[i-1]` (and a constant window), you may overwrite in place or keep two rows; the recurrence's *dependency cone* dictates how much you must retain.

## Common recurrences (Master-theorem shortcuts)
<p class="secgoal"><b>What & why:</b> a lookup table of the divide-and-conquer recurrences you actually meet, each with its closed-form Big-O. Goal — read a recursive solution's cost straight off the shape of its recursion (how many subproblems, how big, how much work to combine) instead of re-deriving it every time.</p>

| Recurrence | Result | Example |
|---|---|---|
| T(n)=2T(n/2)+O(n) | O(n log n) | Merge sort, most D&C |
| T(n)=2T(n/2)+O(1) | O(n) | Tree traversal, size counts |
| T(n)=T(n/2)+O(1) | O(log n) | Binary search |
| T(n)=T(n/2)+O(n) | O(n) | Quickselect (avg) |
| T(n)=2T(n-1)+O(1) | O(2ⁿ) | Naïve subsets/Fibonacci |
| T(n)=n·T(n-1) | O(n!) | Permutations |

Each recurrence encodes a *scenario*: `a·T(n/b)` means "make `a` recursive calls on inputs of size `n/b`," and the trailing `O(…)` is the **combine** (or per-call) work. Here is where each comes from and how the result drops out — read the general shape as a **recursion tree**: how much work sits at each level, times how many levels.

**`T(n) = 2T(n/2) + O(n) → O(n log n)`  — merge sort, worked out fully**

*The scenario.* You split the array in half, sort each half **recursively**, then **merge** the two sorted halves back together in a single O(n) pass. The two recursive calls are the `2T(n/2)`; the merge is the `+ O(n)`.

The cleanest way to see the total cost is to draw the **recursion tree** — one node per subproblem, labelled with the *size* it works on — and add up the work level by level.

```svg
<svg width="720" height="360" viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <defs>
    <marker id="rt-a" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8"/></marker>
  </defs>
  <rect x="0" y="0" width="720" height="360" fill="#fbfcfe"/>

  <!-- edges -->
  <g stroke="#94a3b8" stroke-width="1.4" fill="none" marker-end="url(#rt-a)">
    <path d="M250,58 L166,96"/><path d="M250,58 L334,96"/>
    <path d="M160,122 L104,160"/><path d="M160,122 L212,160"/>
    <path d="M340,122 L288,160"/><path d="M340,122 L396,160"/>
  </g>
  <g stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4 3">
    <path d="M100,186 L92,236"/><path d="M120,186 L150,236"/>
    <path d="M300,186 L300,236"/><path d="M400,186 L420,236"/>
  </g>

  <!-- level 0 -->
  <rect x="220" y="32" width="60" height="26" rx="7" fill="#eff6ff" stroke="#2563eb" stroke-width="1.6"/>
  <text x="250" y="49" text-anchor="middle" font-size="13" font-weight="700" fill="#0b1220">n</text>
  <!-- level 1 -->
  <rect x="130" y="96" width="60" height="26" rx="7" fill="#eff6ff" stroke="#2563eb" stroke-width="1.4"/>
  <text x="160" y="113" text-anchor="middle" font-size="12" font-weight="700" fill="#0b1220">n/2</text>
  <rect x="310" y="96" width="60" height="26" rx="7" fill="#eff6ff" stroke="#2563eb" stroke-width="1.4"/>
  <text x="340" y="113" text-anchor="middle" font-size="12" font-weight="700" fill="#0b1220">n/2</text>
  <!-- level 2 -->
  <g font-size="11" font-weight="700" fill="#0b1220" text-anchor="middle">
    <rect x="78" y="160" width="46" height="24" rx="6" fill="#eff6ff" stroke="#93c5fd"/><text x="101" y="176">n/4</text>
    <rect x="190" y="160" width="46" height="24" rx="6" fill="#eff6ff" stroke="#93c5fd"/><text x="213" y="176">n/4</text>
    <rect x="278" y="160" width="46" height="24" rx="6" fill="#eff6ff" stroke="#93c5fd"/><text x="301" y="176">n/4</text>
    <rect x="378" y="160" width="46" height="24" rx="6" fill="#eff6ff" stroke="#93c5fd"/><text x="401" y="176">n/4</text>
  </g>
  <text x="250" y="222" text-anchor="middle" font-size="16" fill="#94a3b8">⋮</text>
  <!-- leaves -->
  <g font-size="10" font-weight="700" fill="#0b1220" text-anchor="middle">
    <rect x="72"  y="236" width="20" height="20" rx="5" fill="#f0fdf4" stroke="#16a34a"/><text x="82"  y="250">1</text>
    <rect x="120" y="236" width="20" height="20" rx="5" fill="#f0fdf4" stroke="#16a34a"/><text x="130" y="250">1</text>
    <rect x="168" y="236" width="20" height="20" rx="5" fill="#f0fdf4" stroke="#16a34a"/><text x="178" y="250">1</text>
    <text x="222" y="250" font-size="12" fill="#94a3b8">· · ·</text>
    <rect x="288" y="236" width="20" height="20" rx="5" fill="#f0fdf4" stroke="#16a34a"/><text x="298" y="250">1</text>
    <rect x="360" y="236" width="20" height="20" rx="5" fill="#f0fdf4" stroke="#16a34a"/><text x="370" y="250">1</text>
    <rect x="412" y="236" width="20" height="20" rx="5" fill="#f0fdf4" stroke="#16a34a"/><text x="422" y="250">1</text>
  </g>

  <!-- level brace (left) -->
  <path d="M22,32 q-8,0 -8,10 L14,238 q0,10 8,10" stroke="#a78bfa" stroke-width="1.4" fill="none"/>
  <text x="8" y="150" transform="rotate(-90 8,150)" text-anchor="middle" font-size="11" fill="#7c3aed">log₂ n + 1 levels</text>

  <!-- work-per-level annotations (right) -->
  <g font-size="12" fill="#334155">
    <text x="470" y="49">1 piece × n</text>       <text x="592" y="49" font-weight="700" fill="#2563eb">= n</text>
    <text x="470" y="113">2 pieces × n/2</text>    <text x="592" y="113" font-weight="700" fill="#2563eb">= n</text>
    <text x="470" y="176">4 pieces × n/4</text>    <text x="592" y="176" font-weight="700" fill="#2563eb">= n</text>
    <text x="470" y="250">n pieces × 1</text>       <text x="592" y="250" font-weight="700" fill="#2563eb">= n</text>
  </g>

  <!-- summary bar -->
  <rect x="40" y="300" width="640" height="42" rx="9" fill="#eef5ff" stroke="#2563eb"/>
  <text x="360" y="326" text-anchor="middle" font-size="13" fill="#0b1220">
    <tspan font-weight="700">(log₂ n + 1)</tspan> levels  ×  <tspan font-weight="700">n</tspan> per level
    =  n·log₂ n + n  =  <tspan font-weight="700" fill="#2563eb">O(n log n)</tspan>
  </text>
</svg>
```
<div class="readfig"><b>How to read it:</b> Each box is one subproblem, labelled with the input size it handles. Going down, the size halves; the number of boxes doubles. The magic is in the right column: at every level the <i>pieces × size-per-piece</i> multiply out to exactly <b>n</b> — the doubling count and the halving size cancel. So the total is just "how much per level" × "how many levels".</div>

*Step by step:*

1. **Each level halves the size.** The root works on `n`, its two children on `n/2` each, their four children on `n/4`, and so on.
2. **Count the levels.** Repeatedly halving `n` until you reach size 1 takes `log₂ n` halvings — so there are `log₂ n + 1` levels (top row through the leaves).
3. **Find the work on one level.** Level `k` has `2ᵏ` pieces, each of size `n/2ᵏ`, and each piece does work proportional to its size. Multiply: `2ᵏ × (n / 2ᵏ) = n`. The `2ᵏ` (how many) and the `1/2ᵏ` (how big) **cancel** — every level costs the same `n`.
4. **Multiply levels × per-level work.** `(log₂ n + 1) × n = n·log₂ n + n`. Drop the lower-order `n` → **O(n log n)**.
5. **Cross-check with the Master Theorem.** With `a = 2, b = 2`, compare `n^(log_b a) = n¹ = n` against the combine cost `O(n)`. They're the same size, which is **case 2**, and the rule for case 2 tacks on a `log n` → `O(n log n)`. ✓

> [key] **Take-away** — this "work-per-level × number-of-levels" method beats memorizing the Master Theorem. The *shape* of the recursion (how fast pieces multiply vs. how fast sizes shrink) tells you whether the top level, the leaves, or every level equally dominates the cost.

**`T(n)=2T(n/2)+O(1) → O(n)`**
&nbsp;&nbsp;• *Scenario:* recurse on both halves but combine in O(1) — e.g. **counting nodes in a tree** or summing a subtree (`size = 1 + size(L) + size(R)`).
&nbsp;&nbsp;• *Derivation:* the cost is dominated by the *leaves*. A binary tree of recursion over halves has ~`n` leaves, each O(1), and the internal levels form a geometric series that sums to O(n). **O(n).** (Master case 1 — leaf-heavy.)

**`T(n)=T(n/2)+O(1) → O(log n)`**
&nbsp;&nbsp;• *Scenario:* discard half the input and recurse on **one** side with O(1) work — **binary search**.
&nbsp;&nbsp;• *Derivation:* a single chain of calls, each halving `n`, so the depth is `log₂ n`; O(1) per level → **O(log n).**

**`T(n)=T(n/2)+O(n) → O(n)`**
&nbsp;&nbsp;• *Scenario:* do O(n) work up front (e.g. a partition), then recurse into **only one** half — **quickselect** (average case).
&nbsp;&nbsp;• *Derivation:* the work per level *shrinks geometrically*: `n + n/2 + n/4 + … = 2n`. The first level dominates, so the sum is **O(n).** (Master case 3 — root-heavy; contrast with the O(n log n) case where *both* halves recurse.)

**`T(n)=2T(n-1)+O(1) → O(2ⁿ)`**
&nbsp;&nbsp;• *Scenario:* each call spawns **two** calls on an input smaller by just **one** — naïve recursive **Fibonacci** or "include/exclude" subset enumeration.
&nbsp;&nbsp;• *Derivation:* the recursion tree has branching factor 2 and depth `n`, so it holds ~`2ⁿ` nodes. **O(2ⁿ).** (This is why such recursions *must* be memoized into DP.)

**`T(n)=n·T(n-1) → O(n!)`**
&nbsp;&nbsp;• *Scenario:* at the top there are `n` choices, then `n−1` for the next position, then `n−2` … — generating **all permutations** / arranging all items.
&nbsp;&nbsp;• *Derivation:* multiply the choices per level: `n × (n−1) × … × 1 = n!`. **O(n!).**

> [key] **Key Insight** — Two knobs decide everything: *how many recursive calls* (branching) and *how fast the input shrinks*. Halving + one call → logarithmic. Halving + both calls → linear or n·log n depending on combine cost. Shrinking by one + branching → exponential/factorial. Sketch the recursion tree and sum the levels; the answer is almost always "levels × work-per-level."

# Data-Structure Operation Costs
<p class="secgoal"><b>What & why:</b> a one-glance cost table for every core structure's operations. Goal — pick the container whose cheap operations match the ones your problem hammers, and justify the choice on the spot.</p>

Selection is 80% of the battle: the right structure makes the algorithm obvious. Memorize the table; the **revision cards** below it explain *why* each cost is what it is (full behaviour and code live in the *Java Data Structures* chapter).

| Structure | Access | Search | Insert | Delete | Notes |
|---|---|---|---|---|---|
| Array / `int[]` | O(1) | O(n) | O(n) | O(n) | Contiguous; cache-friendly |
| Dynamic array `ArrayList` | O(1) | O(n) | O(1)* end | O(n) | *amortized push |
| `ArrayDeque` (stack/queue) | — | O(n) | O(1) both ends | O(1) both ends | Use instead of `Stack`/`LinkedList` |
| Singly linked list | O(n) | O(n) | O(1)† | O(1)† | †given node ref |
| `HashMap`/`HashSet` | — | O(1) avg | O(1) avg | O(1) avg | O(n) adversarial; no order |
| `LinkedHashMap` | — | O(1) avg | O(1) | O(1) | Insertion/access order → LRU |
| `TreeMap`/`TreeSet` (RB-tree) | — | O(log n) | O(log n) | O(log n) | Ordered; `floor/ceiling/first/last` |
| Binary heap `PriorityQueue` | peek O(1) | O(n) | O(log n) | O(log n) pop | No efficient arbitrary delete |
| Trie | — | O(L) | O(L) | O(L) | L = key length; prefix queries |
| Union-Find | — | α(n) | — | — | Near-constant find/union |
| Fenwick (BIT) | — | O(log n) | O(log n) | — | Prefix sums, point update |
| Segment tree | — | O(log n) | O(log n) | — | Range query + range update (lazy) |

### Why these costs — quick revision cards
<p class="secgoal"><b>What & why:</b> short "because…" cards explaining where each cost in the table comes from. Goal — hold the numbers as understanding you can reconstruct, not trivia you have to memorise.</p>

Each card: *what it is → the operation costs and the one-line reason.* Use it to re-derive the table instead of memorizing it.

- **Array / `int[]`** — contiguous memory. *Access O(1)* (address = `base + i×size`); *search O(n)* (scan); *insert/delete O(n)* (shift the tail to open/close a gap). Fixed size.
- **`ArrayList`** — array that **doubles** when full. Same O(1) access; *append O(1) amortized* (n appends copy ≤ 2n elements total); *middle insert/delete O(n)* (shift).
- **`ArrayDeque`** — **ring buffer** with head/tail indices. *Both ends O(1)* (move a wrapped pointer); *middle O(n)*. The right stack **and** queue.
- **Singly linked list** — nodes chained by `next`. *Access/search O(n)* (pointer chase — no indexing); *insert/delete O(1)* **only if you already hold the node** (just relink).
- **`HashMap` / `HashSet`** — key hashed to a bucket. *get/put/remove O(1) average*; degrades to *O(n)* under adversarial collisions, capped at *O(log n)* by treeified buckets (Java 8+). No ordering.
- **`LinkedHashMap`** — hash map + a doubly-linked **order chain**. Same O(1) ops, but iteration is ordered and access-order mode yields an LRU cache.
- **`TreeMap` / `TreeSet`** — balanced BST of height ≈ `log n`. *get/put/remove O(log n)* (one root-to-leaf path); uniquely supports ordered `floor/ceiling/first/last/subMap`.
- **`PriorityQueue`** (binary heap) — complete tree in an array. *peek O(1)* (root is the extreme); *insert/extract O(log n)* (sift up/down one path); *arbitrary remove O(n)*; no decrease-key.
- **Trie** — one node per character. *insert/search/prefix O(L)* in key length `L`, independent of dictionary size; shared prefixes save memory.
- **Union-Find** — parent-pointer forest with path compression + union by rank. *find/union ≈ O(α(n)) ≈ O(1)* — compression flattens trees so future finds are near-instant.
- **Fenwick (BIT)** — implicit tree indexed by the low bit. *update/query O(log n)* — each jumps `i ± (i & −i)`, at most `log n` hops.
- **Segment tree** — tree over array ranges. *query/update O(log n)* — any range decomposes into ≤ `2·log n` canonical nodes; lazy tags add range updates.

> [key] **Key Insight** — Three recurring "upgrade" moves: replace an *O(n) search* with a **HashMap** (unordered) or **TreeMap** (need order/floor/ceiling/range); replace *repeated max/min scanning* with a **heap** or **monotonic structure**; answer *kth / order-statistic* queries with a **heap** or **Quickselect**.

> [trap] **Common Trap** — Java's `PriorityQueue` has **no O(log n) decrease-key**. For Dijkstra, insert duplicate `(node, dist)` entries and skip stale pops (lazy deletion) rather than trying to update in place.
