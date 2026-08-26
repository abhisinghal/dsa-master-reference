# Topological Sort


<PatternVideo pattern-name="Topological Sort" duration="8–12 min" />

<PatternProgress pattern-id="topological-sort" problems="course-schedule, alien-dictionary, minimum-height-trees, parallel-courses, sequence-reconstruction" />



## Why topological sort exists — the story

You're a build engineer at Google, maintaining Bazel. Every codebase has thousands of source files, each declaring its dependencies. A user runs `bazel build //frontend/app`. The build system must compile files **in an order** that respects: *nothing gets compiled before its dependencies*.

The naive approach: for every file, check if all its dependencies are ready; if yes, compile it; repeat until done. With 100,000 source files in the average monorepo, that's a **quadratic scan** — `10¹⁰` checks per full build. At 10ns per check, that's **100 seconds** of pure scheduling overhead, before a single compile actually runs. On Google's monorepo (2 billion lines of code), naive scheduling would cost hours.

Worse, the naive approach silently loops forever if there's a **cycle** — file A depends on B which depends on A. Not paranoia: every experienced C++ engineer has hit a circular include exactly once, and remembers where they were.

The pattern is **topological sort**: use graph structure to schedule the traversal in **O(V + E)** — linear in the size of the dependency graph, regardless of quadratic worst-case. Kahn's algorithm (1962) does it with a queue: start with all files that have zero unresolved dependencies, emit them, decrement each dependent's remaining count, and enqueue any that just hit zero. **Detects cycles as a side effect** — if the queue empties before every file is emitted, the remaining files form a cycle. That's how Bazel, Make, npm, Cargo, and every other build system on Earth schedules parallel work.

Some tasks are not about shortest paths or reachability. They are about **order**. You cannot take Algorithms before Data Structures, cannot deploy before tests pass, and cannot compile a file before its dependencies compile. When the rules are directed prerequisites — "B must happen before A" — you are looking for a topological ordering.

Take four courses: `0` has no prerequisites, `1` needs `0`, `2` needs `0`, and `3` needs both `1` and `2`. One valid order is `0,1,2,3`; another is `0,2,1,3`. The exact order is not unique, but every valid answer respects the arrows. If you add one more rule, `0` needs `3`, the graph becomes a cycle: `0 → 1 → 3 → 0` or `0 → 2 → 3 → 0`. Now no course can be first, because each course in the loop waits for another.

> [key] **Key Insight** — Topological sort exists iff the graph is a DAG. If Kahn's queue empties before you've emitted all V nodes, the remaining nodes form a cycle.

There are two standard algorithms, and they feel mechanically different. **Kahn's BFS** repeatedly removes nodes with zero remaining prerequisites; it is like saying, "what can I do right now?" **DFS post-order** dives down prerequisites and appends a node after all of its descendants are done; reversing that finish order gives a valid topo order. Both are O(V+E), both detect cycles as a side-effect, and interviewers often accept either if you explain the invariant clearly.

<TopoSortAnim />

> [key] **Key Insight — Kahn's algorithm is BFS on the *indegree=0 frontier*.** The queue holds nodes ready-to-emit; each pop removes one from the graph and decrements neighbours' indegrees. It's a BFS in structure, but on the *dependency* graph rather than a raw graph.

> [key] **Key Insight — DFS-based topo emits in *post-order*.** After visiting all descendants of `u`, push `u` onto a stack. Reverse the stack at the end. The invariant: `u` is pushed only after everything reachable from `u` is pushed, so `u` appears later in the reversed stack. Equally valid, equally O(V+E), preferred when you want to reuse the DFS bookkeeping for cycle detection.

> [inv] **Invariant — Kahn's queue is exactly the set of nodes with indegree 0 given the current graph.** Every pop reduces the graph by one node; every enqueue reflects a neighbour whose last dependency just left. If the queue empties while unemitted nodes remain, those nodes form a **cycle** — every node in the cycle depends on another node in the cycle, so no one hits indegree 0.

> [inv] **Invariant — emitted order respects every edge.** For every edge `u → v` in the original graph, `u` appears before `v` in the output. Verify by walking the output and checking each edge; this is the constant-factor way to sanity-check your implementation without believing your correctness proof.

## When to use it — and when not to

### Recognize by
- *directed graph with prerequisites* — "course schedule", "build order", "task dependencies".
- "return any valid ordering" subject to constraints.
- "detect whether all tasks can be completed" where impossibility means a dependency cycle.
- "alien dictionary" — infer letter order from sorted words, then topologically sort.
- "some items have zero prerequisites first, then unlock others" — Kahn's algorithm language.
- "DAG dynamic programming" — process nodes only after their predecessors are ready.

### When NOT to use it
The graph is *undirected* — topological sort is undefined. For "reach everything from x" use BFS/DFS. For "is this graph a DAG?" use DFS with a 3-colour visitor. If dependencies come with weights (build times, delays), reach for critical-path DP instead.

> [trap] **Trap — using DFS three-coloring wrong.** Cycle detection with DFS needs *three* states: white (unvisited), gray (in current DFS stack), black (finished). Encountering a gray node is a back-edge = cycle. Using just visited/unvisited (two states) fails on graphs like `A → B, A → C, B → D, C → D` — you'd flag the second visit to `D` as a cycle, but it isn't.

> [trap] **Trap — building the reverse graph when you meant the forward graph.** Kahn's needs `outEdges[u]` for "when I emit u, decrement all its dependents' indegrees." Some candidates build `inEdges[u]` (the wrong direction) and get infinite loops. **Rule: `outEdges[u] = list of v such that u → v`.**

> [trap] **Trap — assuming unique output.** Topo order is generally *not* unique — for parallel-independent tasks, any ordering that respects edges is valid. If the problem says "return *the* topological order" it's usually a tell that only one valid order exists (given tie-breaks like lexicographic). If your submission fails a "wrong answer" test but your order respects edges, check whether the grader wants a specific tie-break.

Also avoid it when:
- edges do not represent precedence; shortest path, connected components, and MSTs are different problems.
- the graph can contain cycles but you still need a best effort ordering; use SCC condensation first.
- you need a unique order; topo sort may return many valid orders unless extra rules are added.
- prerequisites change online after every query; maintaining a topo order dynamically is a separate problem.
- the input is really a tree parent relationship; a simple traversal may be enough.

## How to use it — templates

**Kahn's BFS template:**

```java
List<List<Integer>> adj = new ArrayList<>();
int[] indeg = new int[n];
for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
for (int[] e : edges) { adj.get(e[0]).add(e[1]); indeg[e[1]]++; }
Queue<Integer> q = new ArrayDeque<>();
for (int i = 0; i < n; i++) if (indeg[i] == 0) q.offer(i);
List<Integer> order = new ArrayList<>();
while (!q.isEmpty()) {
    int u = q.poll(); order.add(u);
    for (int v : adj.get(u)) if (--indeg[v] == 0) q.offer(v);
}
boolean acyclic = order.size() == n;
```

**DFS post-order template:**

```java
boolean dfs(int u, List<List<Integer>> adj, int[] state, List<Integer> order) {
    if (state[u] == 1) return false;        // back-edge: cycle
    if (state[u] == 2) return true;         // already finished
    state[u] = 1;
    for (int v : adj.get(u)) if (!dfs(v, adj, state, order)) return false;
    state[u] = 2;
    order.add(u);                           // post-order
    return true;
}
```

Prefer Kahn when the problem naturally talks about prerequisites, semesters, waves, or "available now" nodes. Prefer DFS when you are already doing graph recursion, need a compact cycle detector, or want post-order for DAG DP. In Java interviews, Kahn is often easier to debug because the in-degree array makes the invariant visible.


## Kahn vs DFS — same answer, different proof

Kahn's algorithm proves validity from the front of the order. When a node leaves the queue, every prerequisite has already been emitted, because its in-degree has dropped to zero. DFS proves validity from the back of the order. A DFS call appends `u` only after every node reachable from `u` has already been appended, so reversing the post-order places `u` before its dependents.

Cycle detection also appears differently. In Kahn, a cycle shows up as "no node has zero remaining prerequisites," so the emitted count is too small. In DFS, a cycle shows up as a back-edge to a node currently in the recursion stack, which is why the three states are `0 = unvisited`, `1 = visiting`, and `2 = done`. If you only use a boolean visited set in DFS, you can miss the difference between "already safely processed" and "currently on my path," and cycle detection becomes wrong.

A tiny cycle trace makes this concrete: prerequisites `[0,1]` and `[1,0]` create edges `1→0` and `0→1`. Kahn starts with no zero-in-degree node, so it emits nothing. DFS starts at `0`, marks it visiting, goes to `1`, marks it visiting, and then sees edge `1→0` into a visiting node. Both algorithms report impossible, but they discover the problem through different mechanical signals.


## Building the graph is often the real problem

In Course Schedule, the graph is handed to you as pairs. In Alien Dictionary, you must infer it. Compare adjacent words in the sorted dictionary and find the first differing character; if word `w1` has `x` and word `w2` has `y` at that position, add edge `x → y`. Then stop comparing that pair, because later characters tell you nothing once the first difference explains the order. If no differing character exists and the first word is longer, like `"abc"` before `"ab"`, the dictionary is invalid immediately; topo sort cannot fix a bad prefix rule.

This is a common interview twist: topological sort is only half the solution. The other half is translating the domain into nodes and directed edges without inventing edges that the input does not prove. When in doubt, say what a node represents, what an edge means, and why each edge is justified by the problem statement.

## History — Kahn 1962 and every build system on Earth

Topological sort was formalized by **Arthur B. Kahn in 1962** in his paper *"Topological sorting of large networks"* (Communications of the ACM 5(11):558-562). Kahn's algorithm — repeatedly remove nodes with zero indegree — is the same one you'd write today. His motivation was **program dependency analysis**: given a set of tasks with precedence constraints, find a valid execution order. His paper is unusually readable for 1962 and is worth reading if you want to see the pattern in its original form.

The DFS-based topological sort was popularized by **Robert Tarjan** in the 1970s as a byproduct of his strongly-connected-components work. Cormen-Leiserson-Rivest-Stein's *Introduction to Algorithms* (CLRS, 1990) presents both flavors side by side.

**Real-world adoption is universal.** Every build system on Earth is a topological sort:

- **`make`** (1976) topologically sorts source files by `#include` dependencies.
- **`npm install`** topologically sorts npm packages by `dependencies`.
- **`pip install -r requirements.txt`** does the same for Python.
- **Cargo** (Rust), **Bazel** (Google's monorepo build), **Buck** (Meta), **Gradle** (Android) — all topological sort under the hood.
- **Excel's formula recalculation**: cells depend on other cells; topo sort determines evaluation order.
- **Terraform's plan** topologically sorts resource-creation order (VPCs before subnets, subnets before EC2 instances).
- **Airflow / Dagster / Prefect** DAG-based workflow schedulers are literally named after topological sort's precondition (Directed Acyclic Graph).
- **CI/CD pipelines** (GitHub Actions, CircleCI, Jenkins) topologically sort job dependencies.

When you tell an interviewer *"Kahn's algorithm, O(V+E), cycle detection as a side effect,"* you're citing the algorithm that powers essentially every build tool your company uses.

---

## Course Schedule (Topological Sort) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)*

<ProgressCheck id="course-schedule-topological-sort" />

```svg
<svg role="img" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Diagram illustrating: Course Schedule (Topological Sort) Medium">
  <defs>
    <marker id="ar-topo-primary" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="27" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">Kahn's algorithm emits zero-in-degree courses</text>

  <g stroke="var(--dsa-primary)" stroke-width="2" fill="none" marker-end="url(#ar-topo-primary)">
    <line x1="116" y1="80" x2="178" y2="80"/>
    <line x1="116" y1="96" x2="178" y2="150"/>
    <line x1="222" y1="80" x2="284" y2="96"/>
    <line x1="222" y1="150" x2="284" y2="112"/>
  </g>
  <g text-anchor="middle">
    <circle cx="90" cy="88" r="22" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
    <circle cx="200" cy="80" r="22" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
    <circle cx="200" cy="158" r="22" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
    <circle cx="310" cy="104" r="22" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <g font-size="17" font-weight="700" fill="var(--dsa-ink)">
      <text x="90" y="94">A</text><text x="200" y="86">B</text><text x="200" y="164">C</text><text x="310" y="110">D</text>
    </g>
    <g font-size="11" fill="var(--dsa-neutral)">
      <text x="90" y="122">in=0</text><text x="200" y="114">in=1</text><text x="200" y="192">in=1</text><text x="310" y="138">in=2</text>
    </g>
  </g>

  <text x="67" y="211" font-size="12" font-weight="700" fill="var(--dsa-success)">queue</text>
  <rect x="116" y="193" width="44" height="44" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <text x="138" y="221" text-anchor="middle" font-size="17" font-weight="700" fill="var(--dsa-ink)">A</text>
  <text x="246" y="212" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">DAG ⇔ can emit all n</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> Start with the zero-in-degree queue, emit those courses, remove their outgoing edges, and repeat; if every course is emitted, there is no cycle.</div>

### Problem
Given `numCourses` and prerequisite pairs `[a,b]` (finish `b` before `a`), return a **valid order** to take all courses, or an empty array if impossible (a cycle exists).

**Constraints:** `1 ≤ numCourses ≤ 2000`; up to `5000` prerequisite pairs.

**Example 1:** 4 courses, prereqs `1→0, 2→0, 3→1, 3→2` → `[0,1,2,3]`.

**Example 2:** `numCourses = 2`, prerequisites `[[1,0],[0,1]]` → `[]` because the cycle makes an order impossible.

### Solution — brute force
A simple but slow approach repeatedly scans all courses looking for one whose prerequisites are already completed.

```java
// Pseudocode baseline:
// while order has fewer than numCourses:
//     find an uncompleted course whose every prerequisite is completed
//     if none exists, return [] because a cycle blocks progress
//     mark it completed and append it to order
```

This is conceptually Kahn's algorithm without the in-degree bookkeeping. Each round may scan every course and every prerequisite again, so it can degrade toward O(VE). Kahn optimizes the same idea by storing "remaining prerequisite count" and updating only neighbours of the course you just completed.

### Solution — optimized
Kahn's algorithm: repeatedly remove in-degree-0 nodes. If you can't emit all nodes, a cycle exists.

> [inv] **Invariant** — A node enters the queue only when every prerequisite is already emitted; the emission order is a valid topological order.

```mermaid
flowchart TD
  A([Compute in-degree of every node]) --> B[Enqueue all nodes with in-degree 0]
  B --> C{Queue empty?}
  C -- no --> D[Pop u · append u to order]
  D --> E["For each edge u→v:<br/>in-degree[v]-- ; if 0 → enqueue v"]
  E --> C
  C -- yes --> F{Emitted all V nodes?}
  F -- yes --> G([Valid topological order])
  F -- no --> H([Cycle exists — no ordering])
```
<div class="figcap">Kahn's algorithm — repeatedly remove in-degree-0 nodes; incompleteness proves a cycle.</div>
<div class="readfig"><b>How to read it:</b> "In-degree" is how many prerequisites a task still has. Start by queueing every task with zero prerequisites — those are safe to do now. Each time you finish one (pop it), you remove it as a prerequisite from its dependents, and any dependent that drops to zero becomes free, so it joins the queue. Follow the loop and you emit a valid order. If you get stuck before finishing everything, the leftover tasks depend on each other in a circle — a cycle — so no order exists.</div>

#### Steps
1. Build the adjacency list `graph[prereq] → [course]` and an `inDegree[]` counter.
2. Enqueue every node with `inDegree == 0` — they can start immediately.
3. Repeatedly pop, add to the order, and decrement each neighbour's in-degree. Enqueue neighbours whose in-degree hits 0.
4. After the loop, if `order.size() < V` — there was a cycle → return `[]` (or `false` for the boolean variant).
5. Otherwise return the order. O(V + E) time.

#### Java
```java
int[] findOrder(int numCourses, int[][] prereqs) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
    int[] indeg = new int[numCourses];
    for (int[] p : prereqs) { adj.get(p[1]).add(p[0]); indeg[p[0]]++; }
    Queue<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < numCourses; i++) if (indeg[i] == 0) q.offer(i);
    int[] order = new int[numCourses]; int k = 0;
    while (!q.isEmpty()) {
        int u = q.poll(); order[k++] = u;
        for (int v : adj.get(u)) if (--indeg[v] == 0) q.offer(v);
    }
    return k == numCourses ? order : new int[0];    // incomplete => cycle
}
```

> [note] **Trace it** — `numCourses=4`, prerequisites `[1,0], [2,0], [3,1], [3,2]`.

<CodeTrace
  title="Course Schedule II — 4 courses, edges 0→1, 0→2, 1→3, 2→3"
  :values="[0,1,2,3]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { indeg: "[0,1,1,2]", queue: "[0]" }, note: "seed queue with indegree-0 nodes" },
    { pointers: { i: 0 }, vars: { indeg: "[_,0,0,2]", queue: "[1,2]", out: "[0]" }, note: "pop 0, drop edges → 1 and 2 free", added: [0] },
    { pointers: { i: 1 }, vars: { indeg: "[_,_,0,1]", queue: "[2]", out: "[0,1]" }, note: "pop 1, drop 1→3", added: [1] },
    { pointers: { i: 2 }, vars: { indeg: "[_,_,_,0]", queue: "[3]", out: "[0,1,2]" }, note: "pop 2, drop 2→3 → 3 free", added: [2] },
    { pointers: { i: 3 }, vars: { indeg: "[_,_,_,_]", queue: "[]", out: "[0,1,2,3]" }, note: "pop 3. all courses ordered", added: [3] }
  ]'
/>

#### Edge-building intuition
The most common Course Schedule bug is direction. Pair `[a,b]` means "to take `a`, first take `b`." So the unlock direction is `b → a`: completing `b` reduces the remaining prerequisite count of `a`. If you reverse it, your graph still has the same nodes and the code still runs, which makes the bug feel sneaky, but the queue now represents courses unlocked by their dependents instead of by their prerequisites.

Isolated courses matter too. If `numCourses = 4` and only course `3` appears in prerequisites, courses `0`, `1`, and `2` are still valid zero-in-degree courses. Initialize adjacency for every course from `0` to `numCourses-1`, not just for keys seen in the edge list. A topo order must include all vertices, including the boring ones.

#### What if multiple nodes are available?
When the queue contains `[1,2]`, either order is valid unless the problem asks for lexicographically smallest order. For standard Course Schedule II, returning `[0,1,2,3]` or `[0,2,1,3]` is fine. If a problem wants the smallest valid order, replace the FIFO queue with a min-heap. The pattern is unchanged: remove a zero-in-degree node, emit it, and unlock neighbours. Only the policy for choosing among currently-free nodes changes.

### Time Complexity
Time O(V + E). Building adjacency touches each prerequisite once, and Kahn processes every node and edge once.

### Space Complexity
Space O(V + E) for the adjacency list, in-degree array, queue, and output order.

### Learning notes
- Why add edge `p[1] → p[0]`? — finishing the prerequisite unlocks the dependent course.
- Why maintain `indeg[]`? — it is the remaining prerequisite count for each node.
- Why enqueue only `indeg == 0`? — those courses are safe to take immediately.
- Why `--indeg[v] == 0`? — a neighbour becomes available exactly when its last prerequisite is removed.
- Why compare `k == numCourses`? — emitting fewer nodes means a cycle blocked the queue.
- Why Kahn over DFS here? — the BFS queue makes cycle detection and “available now” reasoning visible.

Additional notes:

Time O(V+E) · Space O(V+E). Building the graph touches each edge once, and the queue loop removes each node and edge once.

> [trap] **Common Trap** — Not detecting cycles. *Example:* prerequisites `0→1` and `1→0`. Kahn's queue starts empty (no in-degree-0 node); if `order.size() < V` at the end, report "impossible" rather than a partial order.

<TrapTrace title="Not detecting cycles" input="0→1" bug="prerequisites '0→1' and '1→0'. Kahn's queue starts empty (no in-degree-0 node); if 'order.size() lt V' at the end, report 'impossible' rather than a partial order." fix="See the guidance in the trap description and the code snippet." />

> [note] **Interview script** — First, I'd restate the edge direction: pair `[a,b]` means `b` must come before `a`, so I add edge `b → a`. The brute force is to repeatedly scan for a course whose prerequisites are all done, but that repeats work. I optimize with Kahn's algorithm: maintain in-degrees, queue all zero-in-degree courses, and decrement neighbours as I emit courses. If I emit fewer than `numCourses`, I know a cycle prevented completion; otherwise the order is valid in O(V+E).

#### Common Mistakes
- **Edge direction reversed**: `prereq → course`, not `course → prereq`. Reverse it and cycle detection breaks.
- **Not detecting the cycle**: if `order.size() < V` at the end, report impossible — don't return a partial order.
- **Building the graph off `numCourses` instead of the max node index**: initialize adjacency for all `numCourses` even if some are isolated.
- **DFS variant needs 3-state marking**: unvisited / in-progress / done — a back-edge into an in-progress node is the cycle.

> [pat] **Pattern Connection** — DFS post-order (reversed) is the alternative; three-color DFS detects the cycle. *Alien Dictionary* builds the graph from adjacent-word char differences, then topo-sorts.



#### Layered Kahn for semesters
Sometimes the question is not "what is one order?" but "how many rounds are needed if all currently-free tasks can run together?" Use the same queue, but process it level by level. At the start of a semester, the queue contains every course whose prerequisites were finished in earlier semesters. Pop exactly that many nodes, unlock neighbours, then increment the semester count. This is still Kahn's algorithm; the answer you record changes from a flat list to a number of waves.

#### Uniqueness check
If a problem asks whether a proposed sequence is the only possible reconstruction, watch the queue size. In Kahn's algorithm, a queue with two or more nodes means you have a choice, so multiple valid orders exist. A unique topo order requires exactly one available node at every step, and that node must match the proposed sequence. This is a small tweak, but it shows how much information the "available now" frontier gives you.

#### DFS variant in interview words
If I choose DFS instead, I would say: "I mark a node as visiting when it enters the recursion stack. If I ever reach a visiting node again, that is a directed cycle. After all neighbours are safely processed, I mark the node done and append it to post-order. At the end I reverse post-order to get prerequisites before dependents." This version uses the call stack instead of an explicit queue, but the output contract and O(V+E) complexity are the same.

#### Same pattern, new tweaks

"Repeatedly remove what has no remaining prerequisites" (Kahn) adapts by changing what the nodes/edges mean:

| Variation | The one thing that changes |
|---|---|
| [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | Emit the actual order, not just "is it possible?" |
| [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) | Build edges by comparing adjacent words' first differing character, then topo-sort the alphabet. |
| [Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/) | Peel leaves layer by layer on an undirected tree; this is Kahn-shaped but not true directed topo sort. |
| [Parallel Courses](https://leetcode.com/problems/parallel-courses/) | Count Kahn "waves"; each wave is one semester of courses that can run together. |
| [Sequence Reconstruction](https://leetcode.com/problems/sequence-reconstruction/) | Require the queue to have exactly one choice at every step to prove the order is unique. |

---

## Check your understanding

<Quiz
  pattern-id="topological-sort"
  :questions='[{"q": "Kahn’s BFS toposort starts with nodes of what indeg?", "choices": [{"text": "0", "correct": true, "explanation": "No incoming edges → no prerequisites."}, {"text": "1", "correct": false}, {"text": "n-1", "correct": false}, {"text": "Max indeg", "correct": false}]}, {"q": "How does Kahn’s detect a cycle?", "choices": [{"text": "If the emitted count < n, some nodes were never freed → cycle", "correct": true, "explanation": "Cycle nodes always have indeg > 0."}, {"text": "Timeout", "correct": false}, {"text": "DFS gives back-edges", "correct": false, "explanation": "That is DFS-based; Kahn is BFS."}, {"text": "Impossible in linear time", "correct": false}]}, {"q": "For \"unique topological order\" check, what do you assert at every BFS step?", "choices": [{"text": "Queue size ≤ 1", "correct": true, "explanation": "Multiple nodes with indeg 0 simultaneously = ambiguous order."}, {"text": "Queue size ≥ 1", "correct": false}, {"text": "Queue size == n", "correct": false}, {"text": "Nothing", "correct": false}]}, {"q": "For Minimum Height Trees, why does leaf-peeling find the center(s)?", "choices": [{"text": "Tree centers are the innermost nodes after successively removing leaves", "correct": true, "explanation": "At most 2 remain (they are the median(s) of the longest path)."}, {"text": "Random", "correct": false}, {"text": "By eccentricity computation", "correct": false, "explanation": "Works but O(n²)."}, {"text": "By BFS from root", "correct": false}]}, {"q": "Alien Dictionary: what edges are added to the precedence graph?", "choices": [{"text": "First differing character between two adjacent words: a[i] → b[i]", "correct": true, "explanation": "That is the sole ordering signal."}, {"text": "Every char pair", "correct": false, "explanation": "Would over-constrain."}, {"text": "Random pairs", "correct": false}, {"text": "Alphabet order edges", "correct": false, "explanation": "Alphabet is unknown."}]}]'
/>

<PrintButton />

<RelatedPatterns pattern-id="topo-sort" />
