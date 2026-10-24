## Concepts & Mental Models

Graphs model **relationships**: roads between cities, prerequisites between courses, transformations between words, dependencies between services, and adjacency between grid cells. The interview challenge is rarely "what is a graph?" It is choosing the right *state representation* and the right *frontier policy* so that correctness falls out of a clean invariant.

### Representations: adjacency list vs matrix vs implicit graph

| Representation | Space | Edge lookup | Iterating neighbors | Best when |
|---|---:|---:|---:|---|
| Adjacency list `List<int[]>[]` | O(V + E) | O(outdegree) unless augmented | O(outdegree) | Sparse graphs, almost all interviews |
| Adjacency matrix `boolean[][]` / `int[][]` | O(V²) | O(1) | O(V) | Dense graphs, tiny `V`, constant-time edge queries |
| `Map<Integer,List<int[]>>` | O(V + E) | O(outdegree) | O(outdegree) | Node ids are sparse or not `0..n-1` |
| Implicit graph | Generated on demand | Depends on generator | Depends on branching factor | Word Ladder, grids, puzzles |

For weighted graphs, store each edge as `int[]{to, weight}`. For unweighted graphs, `List<Integer>[]` is fine, but using `int[]{to, w}` consistently reduces mental branching. For grids, the graph is implicit: each cell is a vertex, and the four direction vectors are the edges.

!!! key "Graph thinking starts with the vertex state"
    Decide what a vertex *means*. In a grid it may be `(r,c)`. In Word Ladder it is a whole string. In Cheapest Flights it is not just `city`; it is `(city, edgesUsed)` because the stop budget is part of the state. Most wrong graph solutions collapse distinct states into one visited bit too early.

### BFS vs DFS

**DFS** follows one path deeply before backtracking. It is natural for connected components, cycle detection, flood fill, clone-by-recursion, and topological ordering via postorder. Its invariant is usually about a recursion stack: "grey nodes are ancestors in the current path."

**BFS** expands a frontier in layers. It is natural for shortest path in an **unweighted** graph, multi-source spread processes, and minimum number of transformations. Its invariant is layer-based: when a node is first dequeued (or first discovered, depending on implementation), the recorded distance is the minimum number of edges from the source.

### Visited-state management

The visited structure is not just an optimization; it defines the correctness boundary.

- **Boolean visited**: enough for ordinary traversal and unweighted shortest path when the first arrival is optimal.
- **Three colors (`0/1/2`)**: essential for DFS cycle detection in directed graphs. `1` means currently on recursion stack; seeing it again proves a back edge.
- **Distance array**: replaces visited for weighted shortest paths. A node may be discovered many times before the best distance is finalized.
- **Layered visited/dist**: needed when extra constraints are part of the state, e.g. `dist[steps][city]` or repeated Bellman-Ford arrays for stops.

### When BFS gives shortest path

BFS gives shortest path only when each edge has identical cost. The queue processes all vertices at distance `d` before any at distance `d + 1`, so the first time you reach a vertex is optimal. The moment edges have different weights, "fewest edges" and "lowest cost" diverge; use Dijkstra for non-negative weights or Bellman-Ford-style relaxation when edge counts are bounded or negative edges are possible.

### Relaxation: the core idea behind shortest paths

Relaxation is a local improvement rule:

```text
if dist[u] + w(u,v) < dist[v]:
    dist[v] = dist[u] + w(u,v)
```

Dijkstra chooses the currently smallest tentative distance and then **settles** that node; with non-negative weights, no future path can improve it. Bellman-Ford does not settle greedily. It repeatedly relaxes all edges, so after `k` rounds, distances are optimal among paths using at most `k` edges. Cheapest Flights uses exactly that layered interpretation.

!!! key "Dijkstra's invariant"
    Once a vertex is removed from the priority queue with the smallest tentative distance and accepted as unsettled → settled, its distance is final. This is true only because all edge weights are non-negative.

### MST intuition

A Minimum Spanning Tree connects all vertices with minimum total edge weight and no cycles. It is not a shortest-path tree: MST optimizes total infrastructure cost, while shortest paths optimize source-to-each-destination distances.

Two greedy views dominate:

- **Kruskal** sorts edges by weight and adds the next cheapest edge that connects two different components. Union-Find answers "would this create a cycle?"
- **Prim** grows one connected tree from an arbitrary start, repeatedly adding the cheapest edge crossing from the tree to an outside vertex.

Both rely on the **cut property**: for any cut of the vertices, the lightest edge crossing that cut is safe to include in some MST.

---

## Number of Islands (grid DFS/BFS)

!!! pattern "Pattern: Grid connected components · T: O(mn) · S: O(mn)"
    **Signals:** 2D grid, four-direction adjacency, count regions/components, mutate-or-visited choice.

### 1. Problem

Given an `m x n` grid of `'1'` land and `'0'` water, count the number of islands. An island is a maximal set of horizontally or vertically adjacent land cells. Diagonal contact does not connect islands.

### 2. Intuition

Treat each land cell as a vertex in an implicit graph. Edges connect four-neighbor land cells. Counting islands is counting connected components among land vertices. When we find an unvisited land cell, we have discovered a new component; flood-fill it so no cell in that island starts another count.

### 3. Naive

For every land cell, run a search to see whether it connects to previous cells. Without a visited set or mutation, the same island is explored repeatedly, degenerating toward O((mn)²) on a large all-land grid.

### 4. Key Observation

!!! key "Key observation"
    The first unvisited land cell encountered in row-major scan is a representative of a new island. A DFS/BFS from it marks exactly that island, so each land cell participates in one component traversal.

### 5. Pattern Recognition

**Signals.** "Number of regions," "connected 1s," "flood fill," "capture surrounded areas."  
**Shortcut.** If adjacency is local and uniform, avoid building an explicit graph; generate neighbors with direction arrays.  
**Related.** Max Area of Island, Surrounded Regions, Pacific Atlantic Water Flow.

### 6. Invariant

After scanning cells before `(r,c)`, every land cell in that prefix has either been converted to water/visited as part of a previously counted island, or it is water. Therefore, encountering `'1'` at `(r,c)` means no earlier traversal reached it, so it begins a new island.

### 7. Visual Explanation

```diagram
{"type":"dptable","corner":"","col_head":["0","1","2","3","4"],"row_head":["0","1","2","3"],"grid":[["1","1","0","0","0"],["1","1","0","1","0"],["0","0","1","0","0"],["0","0","0","1","1"]],"highlights":[[0,0,"green"],[0,1,"green"],[1,0,"green"],[1,1,"green"],[1,3,"amber"],[2,2,"purple"],[3,3,"primary"],[3,4,"primary"]],"arrows":[{"from":[0,0],"to":[0,1],"color":"green"},{"from":[0,0],"to":[1,0],"color":"green"},{"from":[3,3],"to":[3,4],"color":"primary"}]}
```

```diagram
{"type":"dptable","corner":"","col_head":["0","1","2","3","4"],"row_head":["0","1","2","3"],"grid":[["0","0","0","0","0"],["0","0","0","1","0"],["0","0","1","0","0"],["0","0","0","1","1"]],"highlights":[[1,3,"amber"],[2,2,"purple"],[3,3,"primary"],[3,4,"primary"]],"arrows":[]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":520,"box":270,"title":"Count islands by flood fill","steps":[{"type":"start","text":"count = 0"},{"type":"decision","text":"scan has next cell?","yes":"yes","branch":{"label":"no","text":"return count","role":"green"}},{"type":"decision","text":"grid[r][c] == '1'?","yes":"yes","branch":{"label":"no","text":"continue scan","role":"primary"}},{"type":"process","text":"count++"},{"type":"process","text":"DFS/BFS mark entire island as visited/water"},{"type":"process","text":"continue scan"}]}
```

### 9. Walkthrough

| Scan event | Action | Count |
|---|---|---:|
| `(0,0)` is land | Flood-fill top-left component | 1 |
| `(1,3)` is land | Single-cell island | 2 |
| `(2,2)` is land | Single-cell island | 3 |
| `(3,3)` is land | Flood-fill `(3,3)-(3,4)` | 4 |

### 10. Why It Works

Every island has a first cell in row-major order. When the scan reaches that cell, no earlier flood-fill could have reached it unless it belonged to a previous island, which contradicts being the first unvisited cell of its island. We increment once for that island, then mark all and only cells connected to it by four-direction land paths. Thus each island contributes exactly one count.

### 11. Java

```java
int numIslands(char[][] grid) {
    if (grid == null || grid.length == 0 || grid[0].length == 0) return 0;
    int m = grid.length, n = grid[0].length;
    int count = 0;
    int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

    for (int r = 0; r < m; r++) {
        for (int c = 0; c < n; c++) {
            if (grid[r][c] != '1') continue;
            count++;
            ArrayDeque<int[]> q = new ArrayDeque<>();
            q.offer(new int[]{r, c});
            grid[r][c] = '0';

            while (!q.isEmpty()) {
                int[] cur = q.poll();
                for (int[] d : dirs) {
                    int nr = cur[0] + d[0], nc = cur[1] + d[1];
                    if (nr < 0 || nr >= m || nc < 0 || nc >= n || grid[nr][nc] != '1') {
                        continue;
                    }
                    grid[nr][nc] = '0';
                    q.offer(new int[]{nr, nc});
                }
            }
        }
    }
    return count;
}
```

### 12. Code Walkthrough

The outer loops choose component representatives. The queue performs BFS over the implicit grid graph. Marking a cell as water at enqueue time prevents duplicate enqueues from two neighboring cells. Mutating the grid avoids a separate `boolean[][] visited`; if mutation is disallowed, replace writes with `visited[nr][nc] = true`.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(mn), because every cell is scanned once and each land cell is enqueued at most once. **S:** O(mn) worst-case queue size for a large island; O(1) extra if mutation is not counted and recursion is avoided, but the BFS frontier can still hold many cells.

### 14. Edge Cases

- Empty grid or empty row → `0`.
- All water → `0`.
- All land → `1`, but queue/recursion depth can be O(mn).
- Diagonal-only contact still forms separate islands.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Marking visited only when dequeuing allows the same cell to be enqueued multiple times. Also be explicit about four-direction adjacency; adding diagonals silently changes the problem.

### 16. Optimization

Use in-place mutation for memory if allowed. For very large grids in Java, prefer iterative BFS/DFS over recursive DFS to avoid stack overflow.

### 17. Alternatives

DFS recursion is shorter but stack-risky. Union-Find is useful for dynamic island additions or when edges are streamed, but it is heavier for a static grid.

### 18. Interview Follow-Ups

- Return the maximum island area.
- Count islands after each land addition.
- Treat diagonals as connected.
- Do not modify the input grid.

### 19. Variations

Number of Enclaves, Closed Islands, Walls and Gates, Rotting Oranges, Pacific Atlantic Water Flow.

### 20. Pattern Connection

This is the canonical **connected components on an implicit graph** problem. The same scan-and-flood-fill shape appears whenever local adjacency defines regions.

---

## Clone Graph

!!! pattern "Pattern: Graph traversal with memoization · T: O(V + E) · S: O(V)"
    **Signals:** deep copy of connected graph, cycles possible, preserve topology not object identity.

### Problem

Given a reference to a node in an undirected connected graph, return a deep copy of the graph. Each node has a value and a list of neighbors.

### Key Observation

!!! key "Key observation"
    A clone must be created exactly once per original node, then reused whenever that original is encountered again. The map `original -> clone` is both the visited set and the identity-preservation table.

### Invariant

When a node is in the map, its clone object exists. After processing that node, every neighbor reference in the clone points to the mapped clone of the corresponding original neighbor.

### Visual

```diagram
{"type":"graph","directed":false,"nodes":[{"id":"1","x":1,"y":1,"label":"1","role":"green"},{"id":"2","x":5,"y":1,"label":"2","role":"amber"},{"id":"3","x":5,"y":5,"label":"3","role":"primary"},{"id":"4","x":1,"y":5,"label":"4","role":"purple"}],"edges":[{"from":"1","to":"2"},{"from":"2","to":"3"},{"from":"3","to":"4"},{"from":"4","to":"1"}]}
```

### Java

```java
class Node {
    public int val;
    public List<Node> neighbors;
    public Node() { val = 0; neighbors = new ArrayList<>(); }
    public Node(int val) { this.val = val; neighbors = new ArrayList<>(); }
    public Node(int val, List<Node> neighbors) { this.val = val; this.neighbors = neighbors; }
}

Node cloneGraph(Node node) {
    if (node == null) return null;
    Map<Node, Node> seen = new HashMap<>();
    ArrayDeque<Node> q = new ArrayDeque<>();
    seen.put(node, new Node(node.val));
    q.offer(node);

    while (!q.isEmpty()) {
        Node cur = q.poll();
        for (Node nei : cur.neighbors) {
            if (!seen.containsKey(nei)) {
                seen.put(nei, new Node(nei.val));
                q.offer(nei);
            }
            seen.get(cur).neighbors.add(seen.get(nei));
        }
    }
    return seen.get(node);
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(V + E), visiting every node and neighbor entry. **S:** O(V), for the clone map and traversal queue.

### Pattern Connection

Clone Graph is traversal plus memoization. The same "create before recursing, then wire edges" pattern appears in copying linked structures with cycles and in object graph serialization.

---

## Rotting Oranges (multi-source BFS)

!!! pattern "Pattern: Multi-source BFS · T: O(mn) · S: O(mn)"
    **Signals:** simultaneous spread, minimum minutes/waves, multiple starting sources.

### Problem

In a grid, `0` is empty, `1` is fresh orange, and `2` is rotten orange. Every minute, fresh oranges adjacent to rotten ones become rotten. Return the minimum minutes until no fresh orange remains, or `-1` if impossible.

### Key Observation

!!! key "Key observation"
    All initially rotten oranges are distance-0 sources. A single BFS seeded with all of them models simultaneous spread; each BFS layer is one minute.

### Invariant

At the start of minute `t`, the queue contains exactly the oranges that became rotten at minute `t - 1` and can infect fresh neighbors for minute `t`.

### Visual

```diagram
{"type":"dptable","corner":"","col_head":["0","1","2"],"row_head":["0","1","2"],"grid":[["2","1","1"],["1","1","0"],["0","1","1"]],"highlights":[[0,0,"red"],[0,1,"amber"],[1,0,"amber"],[2,2,"primary"]],"arrows":[{"from":[0,0],"to":[0,1],"color":"red"},{"from":[0,0],"to":[1,0],"color":"red"}]}
```

### Java

```java
int orangesRotting(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    ArrayDeque<int[]> q = new ArrayDeque<>();
    int fresh = 0;
    for (int r = 0; r < m; r++) {
        for (int c = 0; c < n; c++) {
            if (grid[r][c] == 2) q.offer(new int[]{r, c});
            else if (grid[r][c] == 1) fresh++;
        }
    }
    if (fresh == 0) return 0;

    int minutes = 0;
    int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    while (!q.isEmpty()) {
        int size = q.size();
        boolean rottedThisMinute = false;
        for (int i = 0; i < size; i++) {
            int[] cur = q.poll();
            for (int[] d : dirs) {
                int nr = cur[0] + d[0], nc = cur[1] + d[1];
                if (nr < 0 || nr >= m || nc < 0 || nc >= n || grid[nr][nc] != 1) continue;
                grid[nr][nc] = 2;
                fresh--;
                rottedThisMinute = true;
                q.offer(new int[]{nr, nc});
            }
        }
        if (rottedThisMinute) minutes++;
    }
    return fresh == 0 ? minutes : -1;
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(mn), each cell is inspected a constant number of times. **S:** O(mn), for the queue in the worst case.

### Pattern Connection

This is the same shortest-distance BFS invariant as ordinary BFS, but with a **set of sources**. Initialize the queue with every distance-0 node rather than running BFS from each source separately.

---

## Course Schedule / Topological Sort (Kahn + DFS cycle)

!!! pattern "Pattern: Directed acyclic graph · T: O(V + E) · S: O(V + E)"
    **Signals:** prerequisites/dependencies, need valid order, detect cycle in directed graph.

### 1. Problem

Given `numCourses` labeled `0..numCourses-1` and prerequisite pairs `[course, prereq]`, determine whether all courses can be finished. A course can be taken only after its prerequisites. The ordering question is topological sort; the feasibility question is whether the directed dependency graph is acyclic.

### 2. Intuition

Represent each prerequisite as edge `prereq -> course`. Courses with indegree 0 have no unmet prerequisites and are immediately available. Kahn's algorithm repeatedly takes such courses and "removes" their outgoing edges. If every course is removed, the graph is a DAG. If some remain, they are trapped in a directed cycle.

### 3. Naive

Repeatedly scan all prerequisites looking for a course whose prerequisites are satisfied. This can cost O(VE) because the same edges are rescanned after every course.

### 4. Key Observation

!!! key "Key observation"
    Topological order is exactly an ordering in which every directed edge `u -> v` places `u` before `v`. Maintaining indegrees lets us identify all currently legal next vertices in O(1) amortized per edge.

### 5. Pattern Recognition

**Signals.** Prerequisites, build order, dependency resolution, "can finish all?"  
**Shortcut.** Edge direction should point from prerequisite to dependent if you want Kahn's algorithm to emit executable order.  
**Related.** Alien Dictionary, Task Scheduler with dependencies, build systems.

### 6. Invariant

In Kahn's algorithm, the queue contains exactly vertices whose incoming edges from the remaining graph are zero. The emitted list is always a valid topological prefix: every emitted vertex has all prerequisites already emitted.

### 7. Visual Explanation

```diagram
{"type":"graph","directed":true,"nodes":[{"id":"0","x":1,"y":1,"label":"0","role":"green"},{"id":"1","x":3,"y":1,"label":"1","role":"green"},{"id":"2","x":2,"y":3,"label":"2","role":"amber"},{"id":"3","x":4,"y":3,"label":"3","role":"primary"}],"edges":[{"from":"0","to":"2","directed":true},{"from":"1","to":"2","directed":true},{"from":"2","to":"3","directed":true}]}
```

```diagram
{"type":"dptable","corner":"step","col_head":["queue","take","indeg[0]","indeg[1]","indeg[2]","indeg[3]"],"row_head":["0","1","2","3"],"grid":[["0,1","","0","0","2","1"],["1","0","0","0","1","1"],["2","1","0","0","0","1"],["3","2","0","0","0","0"]],"highlights":[[0,0,"green"],[2,0,"amber"],[3,5,"green"]],"arrows":[]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":540,"box":290,"title":"Kahn topological feasibility","steps":[{"type":"start","text":"Build graph and indegree[]"},{"type":"process","text":"Enqueue all indegree-0 courses"},{"type":"decision","text":"queue non-empty?","yes":"yes","branch":{"label":"no","text":"processed == numCourses?","role":"primary"}},{"type":"process","text":"pop u; processed++"},{"type":"process","text":"for each u -> v: indegree[v]--"},{"type":"decision","text":"indegree[v] == 0?","yes":"yes","branch":{"label":"no","text":"skip","role":"red"}},{"type":"process","text":"enqueue v"},{"type":"end","text":"cycle iff processed < numCourses"}]}
```

### 9. Walkthrough

For prerequisites `[[2,0],[2,1],[3,2]]`, indegrees are `[0,0,2,1]`. Queue starts with `0,1`. Taking `0` reduces `2` to 1; taking `1` reduces `2` to 0 and unlocks it; taking `2` unlocks `3`. Four courses processed → feasible.

### 10. Why It Works

If Kahn emits a vertex, all remaining incoming edges to it are gone, so all prerequisites are in the prefix. Thus the prefix is always valid. Every finite DAG has at least one indegree-0 vertex; otherwise following incoming edges forever would repeat a vertex and form a cycle. Therefore, if the graph is acyclic, Kahn can keep removing vertices until none remain. If it stops early, the remaining subgraph has no indegree-0 vertex, so it contains a directed cycle.

### 11. Java

```java
boolean canFinish(int numCourses, int[][] prerequisites) {
    List<Integer>[] graph = new ArrayList[numCourses];
    for (int i = 0; i < numCourses; i++) graph[i] = new ArrayList<>();
    int[] indegree = new int[numCourses];

    for (int[] p : prerequisites) {
        int course = p[0], prereq = p[1];
        graph[prereq].add(course);
        indegree[course]++;
    }

    ArrayDeque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < numCourses; i++) {
        if (indegree[i] == 0) q.offer(i);
    }

    int processed = 0;
    while (!q.isEmpty()) {
        int u = q.poll();
        processed++;
        for (int v : graph[u]) {
            indegree[v]--;
            if (indegree[v] == 0) q.offer(v);
        }
    }
    return processed == numCourses;
}

boolean canFinishDfs(int numCourses, int[][] prerequisites) {
    List<Integer>[] graph = new ArrayList[numCourses];
    for (int i = 0; i < numCourses; i++) graph[i] = new ArrayList<>();
    for (int[] p : prerequisites) graph[p[1]].add(p[0]);

    int[] color = new int[numCourses]; // 0 unvisited, 1 visiting, 2 done
    for (int i = 0; i < numCourses; i++) {
        if (color[i] == 0 && hasCycle(i, graph, color)) return false;
    }
    return true;
}

boolean hasCycle(int u, List<Integer>[] graph, int[] color) {
    color[u] = 1;
    for (int v : graph[u]) {
        if (color[v] == 1) return true;
        if (color[v] == 0 && hasCycle(v, graph, color)) return true;
    }
    color[u] = 2;
    return false;
}
```

### 12. Code Walkthrough

Kahn's version stores outgoing dependents and counts unmet prerequisites in `indegree`. `processed` counts emitted vertices; it is more robust than checking queue emptiness because an empty queue is normal at the end. The DFS version uses the precise directed-cycle invariant: an edge to a `visiting` node is a back edge to an ancestor.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(V + E), building the graph and processing each edge once. **S:** O(V + E), for adjacency plus indegree/queue or recursion/color state.

### 14. Edge Cases

- No prerequisites → all courses available.
- Self dependency `[0,0]` → cycle.
- Duplicate edges may over-increment indegree; either accept if input permits duplicates as separate constraints or deduplicate with sets.
- Disconnected DAG components are handled by multiple initial indegree-0 nodes.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Reversing edge direction and then interpreting the emitted order as executable. For feasibility either direction can detect cycles if used consistently, but topological order semantics require `prereq -> course`.

### 16. Optimization

Use primitive arrays and `ArrayDeque`. If only cycle existence is needed, DFS may avoid storing indegrees, but it still needs adjacency.

### 17. Alternatives

DFS postorder can produce a topological order by adding nodes after exploring descendants and reversing the result. Kahn is usually better when you need lexicographically smallest order or streaming "currently available" tasks.

### 18. Interview Follow-Ups

- Return one valid course order.
- Return the lexicographically smallest order with a `PriorityQueue`.
- Find all courses involved in cycles.
- Support incremental prerequisite additions.

### 19. Variations

Course Schedule II, Alien Dictionary, Sequence Reconstruction, Minimum Height Trees (different graph direction but similar queue trimming).

### 20. Pattern Connection

Topological sort is the dependency counterpart of BFS: the frontier is not "distance layer" but "all prerequisites satisfied." The same indegree frontier powers build systems and task schedulers.

---

## Alien Dictionary

!!! pattern "Pattern: Topological sort from ordering constraints · T: O(C) · S: O(1) bounded alphabet"
    **Signals:** sorted dictionary in unknown alphabet, derive character precedence, invalid prefix case.

### Problem

Given words sorted according to an unknown alien alphabet, return a valid ordering of the distinct characters, or `""` if no valid order exists.

### Key Observation

!!! key "Key observation"
    The first differing character between two adjacent words is the only ordering constraint that pair can prove. If `w1 = "abc"` appears before `w2 = "abx"`, then `c -> x`; later characters are irrelevant.

### Invariant

The graph contains exactly the precedence constraints implied by adjacent word pairs processed so far. Kahn's emitted prefix contains only characters whose known prerequisites have already appeared.

### Visual

```diagram
{"type":"graph","directed":true,"nodes":[{"id":"w","x":1,"y":1,"label":"w","role":"green"},{"id":"e","x":3,"y":1,"label":"e","role":"amber"},{"id":"r","x":5,"y":1,"label":"r","role":"primary"},{"id":"t","x":2,"y":4,"label":"t","role":"purple"},{"id":"f","x":4,"y":4,"label":"f","role":"muted"}],"edges":[{"from":"w","to":"e","directed":true},{"from":"e","to":"r","directed":true},{"from":"r","to":"t","directed":true},{"from":"t","to":"f","directed":true}]}
```

### Java

```java
String alienOrder(String[] words) {
    Map<Character, Set<Character>> graph = new HashMap<>();
    Map<Character, Integer> indegree = new HashMap<>();
    for (String word : words) {
        for (char ch : word.toCharArray()) {
            graph.putIfAbsent(ch, new HashSet<>());
            indegree.putIfAbsent(ch, 0);
        }
    }

    for (int i = 0; i + 1 < words.length; i++) {
        String a = words[i], b = words[i + 1];
        if (a.length() > b.length() && a.startsWith(b)) return "";
        int len = Math.min(a.length(), b.length());
        for (int j = 0; j < len; j++) {
            char u = a.charAt(j), v = b.charAt(j);
            if (u == v) continue;
            if (graph.get(u).add(v)) indegree.put(v, indegree.get(v) + 1);
            break;
        }
    }

    ArrayDeque<Character> q = new ArrayDeque<>();
    for (char ch : indegree.keySet()) {
        if (indegree.get(ch) == 0) q.offer(ch);
    }

    StringBuilder order = new StringBuilder();
    while (!q.isEmpty()) {
        char u = q.poll();
        order.append(u);
        for (char v : graph.get(u)) {
            indegree.put(v, indegree.get(v) - 1);
            if (indegree.get(v) == 0) q.offer(v);
        }
    }
    return order.length() == indegree.size() ? order.toString() : "";
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(C), where `C` is the total number of characters scanned. **S:** O(U + E), with `U` distinct characters; for lowercase English-like alphabets this is bounded.

### Pattern Connection

Alien Dictionary is Course Schedule with edges extracted from sorted strings. The unique trap is the invalid prefix case: `"abc"` before `"ab"` cannot be explained by any alphabet.

---

## Dijkstra's Algorithm / Network Delay Time

!!! pattern "Pattern: Non-negative weighted shortest path · T: O((V + E) log V) · S: O(V + E)"
    **Signals:** positive travel times, minimum delay/cost from one source, graph may be sparse.

### 1. Problem

Given directed weighted edges `times[i] = [u, v, w]`, `n` nodes labeled `1..n`, and a start node `k`, compute how long it takes for a signal to reach every node. Return the maximum shortest-path distance from `k`, or `-1` if some node is unreachable.

### 2. Intuition

Maintain the best known distance to every node. Always expand the unsettled node with the smallest tentative distance. Because edge weights are non-negative, any alternate route to that node through not-yet-settled nodes would be at least as large, so the node's distance becomes final.

### 3. Naive

Relax all edges repeatedly `V - 1` times as in Bellman-Ford: O(VE). Correct for non-negative weights, but unnecessarily slow when a priority queue can focus exploration around the smallest distances.

### 4. Key Observation

!!! key "Key observation"
    With non-negative weights, the smallest tentative distance in the priority queue cannot be improved later. This is the settled-node invariant that makes Dijkstra greedy rather than exhaustive.

### 5. Pattern Recognition

**Signals.** Weighted graph, no negative weights, one source, shortest delay/cost.  
**Shortcut.** If all weights are `1`, use BFS. If weights are `0/1`, use 0-1 BFS. If negative weights or stop layers matter, Dijkstra's plain settled invariant may not apply.  
**Related.** Path With Minimum Effort, Cheapest Flights (but stop constraint changes state), shortest path in road networks.

### 6. Invariant

At any point, settled nodes have final shortest distances. The priority queue may contain stale entries, but the first non-stale extraction for a node is its final distance. For every unsettled node, `dist[v]` is the best path found so far whose internal vertices are settled.

### 7. Visual Explanation

```diagram
{"type":"graph","directed":true,"nodes":[{"id":"1","x":1,"y":3,"label":"1","role":"green"},{"id":"2","x":3,"y":1,"label":"2","role":"amber"},{"id":"3","x":3,"y":5,"label":"3","role":"primary"},{"id":"4","x":5,"y":3,"label":"4","role":"purple"}],"edges":[{"from":"1","to":"2","w":1,"directed":true},{"from":"1","to":"3","w":4,"directed":true},{"from":"2","to":"3","w":2,"directed":true},{"from":"2","to":"4","w":6,"directed":true},{"from":"3","to":"4","w":3,"directed":true}]}
```

```diagram
{"type":"dptable","corner":"settled","col_head":["d(1)","d(2)","d(3)","d(4)","pq"],"row_head":["start","1","2","3","4"],"grid":[["0","∞","∞","∞","(1,0)"],["0","1","4","∞","(2,1),(3,4)"],["0","1","3","7","(3,3),(3,4),(4,7)"],["0","1","3","6","(4,6),(4,7)"],["0","1","3","6",""]],"highlights":[[1,0,"green"],[2,1,"green"],[3,2,"green"],[4,3,"green"]],"arrows":[]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":560,"box":300,"title":"Dijkstra with stale-entry skip","steps":[{"type":"start","text":"dist[source] = 0; push (0, source)"},{"type":"decision","text":"priority queue non-empty?","yes":"yes","branch":{"label":"no","text":"distances finalized for reachable nodes","role":"green"}},{"type":"process","text":"pop smallest (d, u)"},{"type":"decision","text":"d != dist[u]?","yes":"yes","branch":{"label":"no","text":"settle u","role":"green"}},{"type":"process","text":"skip stale entry"},{"type":"process","text":"relax each edge u -> v with weight w"},{"type":"decision","text":"d + w < dist[v]?","yes":"yes","branch":{"label":"no","text":"keep old distance","role":"primary"}},{"type":"process","text":"update dist[v]; push new pair"}]}
```

### 9. Walkthrough

Starting at `1`, settle `1` with distance 0 and discover `2=1`, `3=4`. Settle `2` next; relaxing `2 -> 3` improves `3` from 4 to 3 and `2 -> 4` sets `4=7`. Settle `3` at 3; `3 -> 4` improves `4` to 6. The stale `(3,4)` queue entry is ignored. Settle `4`; max distance is 6.

### 10. Why It Works

Assume the smallest unsettled node `u` is popped with distance `d`, but some shorter path to `u` exists. Let `x -> y` be the first edge on that path crossing from settled to unsettled. The prefix to `x` is final, and relaxing `x -> y` would have made `dist[y]` no more than the length of that prefix plus a non-negative edge. Therefore `dist[y]` would be ≤ the alleged shorter path to `u`, which is < `d`, contradicting that `u` had the smallest tentative distance.

### 11. Java

```java
int networkDelayTime(int[][] times, int n, int k) {
    List<int[]>[] graph = new ArrayList[n + 1];
    for (int i = 1; i <= n; i++) graph[i] = new ArrayList<>();
    for (int[] e : times) graph[e[0]].add(new int[]{e[1], e[2]});

    int[] dist = new int[n + 1];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[k] = 0;

    PriorityQueue<int[]> pq = new PriorityQueue<>(
        (a, b) -> Integer.compare(a[0], b[0])
    );
    pq.offer(new int[]{0, k});

    while (!pq.isEmpty()) {
        int[] cur = pq.poll();
        int d = cur[0], u = cur[1];
        if (d != dist[u]) continue;

        for (int[] edge : graph[u]) {
            int v = edge[0], w = edge[1];
            if (d <= Integer.MAX_VALUE - w && d + w < dist[v]) {
                dist[v] = d + w;
                pq.offer(new int[]{dist[v], v});
            }
        }
    }

    int ans = 0;
    for (int i = 1; i <= n; i++) {
        if (dist[i] == Integer.MAX_VALUE) return -1;
        ans = Math.max(ans, dist[i]);
    }
    return ans;
}
```

### 12. Code Walkthrough

The adjacency list stores `(to, weight)`. The priority queue is ordered with `Integer.compare`, avoiding overflow-prone subtraction. We do not need a separate `visited` array; `if (d != dist[u]) continue` discards older queue entries after a better path has been found. The final answer is the maximum finite distance because all nodes receive the signal in parallel along shortest paths.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O((V + E) log V) with a binary heap and adjacency lists; duplicate heap entries make it O(E log E) in the loosest Java implementation, equivalent for sparse interview bounds. **S:** O(V + E), for graph, distances, and heap.

### 14. Edge Cases

- Disconnected nodes → `-1`.
- Source has no outgoing edges and `n > 1` → `-1`.
- Multiple edges between same nodes are fine; relaxation keeps the best.
- Weight 0 is allowed; negative weights are not.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Marking a node visited when it is first inserted into the priority queue is wrong. A later relaxation may find a cheaper path before the node is settled. Settle on pop, not on push.

### 16. Optimization

For dense graphs, an O(V²) matrix-based Dijkstra can be competitive and simpler. For very large weights, use `long[] dist` to avoid overflow.

### 17. Alternatives

Bellman-Ford handles negative edges at O(VE). Floyd-Warshall gives all-pairs shortest paths at O(V³). BFS is correct only when every edge has equal weight.

### 18. Interview Follow-Ups

- Recover the actual shortest path tree with a `parent[]`.
- Count number of shortest paths.
- Support `0/1` weights with deque-based 0-1 BFS.
- Detect negative cycles with Bellman-Ford.

### 19. Variations

Minimum Cost to Connect Points is MST, not shortest path. Path With Minimum Effort uses Dijkstra where path cost is max edge effort rather than sum. Swim in Rising Water uses the same min-frontier idea.

### 20. Pattern Connection

Dijkstra is BFS with a priority queue and relaxation. Replace "next layer" with "next smallest tentative cost"; keep the settled-distance invariant front and center.

---

## Cheapest Flights Within K Stops (Bellman-Ford / layered BFS)

!!! pattern "Pattern: Bounded-edge shortest path · T: O((K + 1)E) · S: O(V)"
    **Signals:** cheapest path with at most K stops, non-negative prices, edge-count constraint changes state.

### 1. Problem

Given `n` cities, directed flights `[from, to, price]`, source `src`, destination `dst`, and at most `K` stops, return the cheapest price from `src` to `dst`, or `-1` if no such route exists. `K` stops means at most `K + 1` flight edges.

### 2. Intuition

The stop limit makes "best price to city" insufficient. A more expensive route to an intermediate city using fewer edges may be the only one that can still reach the destination. Bellman-Ford's layered relaxation fits perfectly: after `i` rounds, distances represent cheapest prices using at most `i` flights.

### 3. Naive

Run ordinary Dijkstra over cities and keep one `dist[city]`. This can prune a higher-cost-but-fewer-stops state that is necessary under the constraint. Alternatively enumerating all routes explodes exponentially in branching factor.

### 4. Key Observation

!!! key "Key observation"
    Copy the previous distance array before each relaxation round. Round `i` may only build from paths using at most `i - 1` flights, so one round cannot accidentally chain multiple flights.

### 5. Pattern Recognition

**Signals.** "At most K stops/edges," bounded path length, price minimization.  
**Shortcut.** If a constraint limits number of edges, think layers: `dp[edges][city]`.  
**Related.** Bellman-Ford, shortest path with coupons, resource-constrained routing.

### 6. Invariant

After round `i`, `dist[v]` equals the cheapest cost from `src` to `v` using at most `i` flights. The previous snapshot `prev` contains exactly the values for at most `i - 1` flights.

### 7. Visual Explanation

```diagram
{"type":"graph","directed":true,"nodes":[{"id":"0","x":1,"y":3,"label":"0","role":"green"},{"id":"1","x":3,"y":1,"label":"1","role":"amber"},{"id":"2","x":5,"y":3,"label":"2","role":"primary"},{"id":"3","x":3,"y":5,"label":"3","role":"purple"}],"edges":[{"from":"0","to":"1","w":100,"directed":true},{"from":"1","to":"2","w":100,"directed":true},{"from":"0","to":"2","w":500,"directed":true},{"from":"0","to":"3","w":50,"directed":true},{"from":"3","to":"2","w":500,"directed":true}]}
```

```diagram
{"type":"dptable","corner":"flights","col_head":["city 0","city 1","city 2","city 3"],"row_head":["0","1","2"],"grid":[["0","∞","∞","∞"],["0","100","500","50"],["0","100","200","50"]],"highlights":[[1,2,"amber"],[2,2,"green"],[1,3,"purple"]],"arrows":[]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":560,"box":310,"title":"Layered Bellman-Ford for K stops","steps":[{"type":"start","text":"dist[src] = 0; all others = INF"},{"type":"process","text":"Repeat for flights = 1..K+1"},{"type":"process","text":"prev = copy(dist)"},{"type":"process","text":"for each edge u -> v with price w"},{"type":"decision","text":"prev[u] finite and prev[u] + w < dist[v]?","yes":"yes","branch":{"label":"no","text":"no update","role":"primary"}},{"type":"process","text":"dist[v] = prev[u] + w"},{"type":"end","text":"answer dist[dst] or -1"}]}
```

### 9. Walkthrough

For `src=0`, `dst=2`, `K=1`, at most 2 flights. Round 0 has only `0=0`. Round 1 finds direct prices: `1=100`, `2=500`, `3=50`. Round 2 can extend one more flight from the snapshot: `1 -> 2` improves destination to `200`; `3 -> 2` gives `550`, not better.

### 10. Why It Works

The invariant is Bellman-Ford restricted to `K + 1` rounds. Any valid route with at most `i` flights ends with some edge `u -> v`; its prefix to `u` uses at most `i - 1` flights, whose optimal cost is in `prev[u]`. Relaxing all edges considers every possible last edge. Conversely, using `prev` prevents a path with more than `i` flights from being formed inside one round.

### 11. Java

```java
int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
    final int INF = 1_000_000_000;
    int[] dist = new int[n];
    Arrays.fill(dist, INF);
    dist[src] = 0;

    for (int flightsUsed = 1; flightsUsed <= k + 1; flightsUsed++) {
        int[] prev = dist.clone();
        for (int[] e : flights) {
            int u = e[0], v = e[1], price = e[2];
            if (prev[u] == INF) continue;
            if (prev[u] + price < dist[v]) {
                dist[v] = prev[u] + price;
            }
        }
    }
    return dist[dst] == INF ? -1 : dist[dst];
}
```

### 12. Code Walkthrough

`dist` is the best cost using up to the current number of flights. `prev` freezes the previous layer. Updating `dist[v]` rather than `next[v]` is acceptable because `dist` already contains cheaper paths using fewer flights; the key is that the source side of every relaxation is read from `prev`.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O((K + 1)E), one full edge scan per allowed flight count. **S:** O(V), for the current and previous distance arrays.

### 14. Edge Cases

- `src == dst` → `0`.
- `K = 0` allows only direct flights.
- A cheaper route with too many stops must be rejected.
- Use a large finite `INF` to avoid overflow from adding to `Integer.MAX_VALUE`.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Updating from `dist[u]` in the same round chains multiple edges and violates the stop limit. Always relax from the previous layer snapshot.

### 16. Optimization

Early-stop if a round makes no updates. For sparse graphs and small reachable frontiers, a layered BFS over `(city,cost,edges)` states with pruning may do less work, but it is easier to get wrong.

### 17. Alternatives

Use a priority queue over `(cost, city, flightsUsed)` and keep best costs per `(city, flightsUsed)`. This can be faster in practice but requires not collapsing all visits to one `visited[city]`.

### 18. Interview Follow-Ups

- Return the actual itinerary.
- Require exactly `K` stops rather than at most.
- Add a second resource constraint, such as total time.
- Explain why plain Dijkstra is insufficient.

### 19. Variations

Minimum Cost to Reach Destination in Time, Shortest Path with Alternating Colors, constrained coupon/discount shortest paths.

### 20. Pattern Connection

This problem is the bridge between shortest paths and dynamic programming: `dp[edges][city]` is Bellman-Ford's heart. The state includes the resource consumed, not just the vertex.

---

## Word Ladder (BFS on implicit graph)

!!! pattern "Pattern: BFS on implicit unweighted graph · T: O(NL²) · S: O(NL)"
    **Signals:** minimum transformations, one-character changes, dictionary membership.

### Problem

Given `beginWord`, `endWord`, and a dictionary, return the length of the shortest transformation sequence where each step changes exactly one character and every intermediate word is in the dictionary.

### Key Observation

!!! key "Key observation"
    Words are graph nodes; edges connect words that differ by one character. Since every transformation has equal cost, BFS from `beginWord` finds the minimum number of words in the sequence.

### Invariant

When a word is dequeued at level `d`, `d` is the shortest transformation length from `beginWord` to that word.

### Visual

```diagram
{"type":"graph","directed":false,"nodes":[{"id":"hit","x":1,"y":3,"label":"hit","role":"green"},{"id":"hot","x":2.5,"y":3,"label":"hot","role":"amber"},{"id":"dot","x":4,"y":1.5,"label":"dot","role":"primary"},{"id":"dog","x":5.5,"y":1.5,"label":"dog","role":"purple"},{"id":"lot","x":4,"y":4.5,"label":"lot","role":"primary"},{"id":"log","x":5.5,"y":4.5,"label":"log","role":"purple"},{"id":"cog","x":6,"y":3,"label":"cog","role":"green"}],"edges":[{"from":"hit","to":"hot"},{"from":"hot","to":"dot"},{"from":"dot","to":"dog"},{"from":"hot","to":"lot"},{"from":"lot","to":"log"},{"from":"dog","to":"cog"},{"from":"log","to":"cog"}]}
```

### Java

```java
int ladderLength(String beginWord, String endWord, List<String> wordList) {
    Set<String> dict = new HashSet<>(wordList);
    if (!dict.contains(endWord)) return 0;

    ArrayDeque<String> q = new ArrayDeque<>();
    q.offer(beginWord);
    Set<String> visited = new HashSet<>();
    visited.add(beginWord);
    int level = 1;

    while (!q.isEmpty()) {
        int size = q.size();
        for (int i = 0; i < size; i++) {
            String word = q.poll();
            if (word.equals(endWord)) return level;
            char[] chars = word.toCharArray();
            for (int pos = 0; pos < chars.length; pos++) {
                char old = chars[pos];
                for (char ch = 'a'; ch <= 'z'; ch++) {
                    if (ch == old) continue;
                    chars[pos] = ch;
                    String next = new String(chars);
                    if (dict.contains(next) && visited.add(next)) q.offer(next);
                }
                chars[pos] = old;
            }
        }
        level++;
    }
    return 0;
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(N · L · 26 · L) = O(NL²), because each generated candidate string costs O(L). **S:** O(NL), for dictionary, visited, and queue strings.

### Pattern Connection

Word Ladder is graph traversal without materializing all edges. Generate neighbors on demand; BFS remains standard because the implicit edges are unweighted.

---

## Kruskal's MST (with union-find) and Prim's MST

!!! pattern "Pattern: Minimum spanning tree by cut property · T: O(E log E) · S: O(V)"
    **Signals:** connect all nodes with minimum total edge cost, undirected weighted graph, cycle avoidance.

### 1. Problem

Given an undirected connected weighted graph, find a set of `V - 1` edges that connects all vertices with minimum total weight. For Kruskal, edges are considered globally from lightest to heaviest; an edge is accepted only if it joins two different connected components.

### 2. Intuition

Imagine every vertex starts as its own island. The cheapest bridge between two different islands is safe because it cannot be worse than another way to connect those two sides across the same cut. Kruskal repeatedly adds the cheapest safe bridge until one component remains.

### 3. Naive

Try all subsets of `V - 1` edges, filter those that form a spanning tree, and take the minimum. This is combinatorial and unusable beyond tiny graphs.

### 4. Key Observation

!!! key "Key observation"
    By the cut property, the lightest edge crossing any cut is safe for some MST. Sorting edges lets Kruskal encounter safe cheap edges early; Union-Find rejects exactly those edges whose endpoints are already connected and would form a cycle.

### 5. Pattern Recognition

**Signals.** "Minimum cost to connect all," undirected weighted edges, total network cost.  
**Shortcut.** If the problem asks for paths from one source, it is shortest path, not MST. If it asks for total cost to connect all nodes, think MST.  
**Related.** Min Cost to Connect Points, Connecting Cities With Minimum Cost.

### 6. Invariant

After processing some prefix of sorted edges, the accepted edges form a forest that is extendable to an MST. Each Union-Find component corresponds to one tree in that forest.

### 7. Visual Explanation

```diagram
{"type":"graph","directed":false,"nodes":[{"id":"A","x":1,"y":1,"label":"A","role":"green"},{"id":"B","x":3,"y":1,"label":"B","role":"green"},{"id":"C","x":5,"y":1,"label":"C","role":"amber"},{"id":"D","x":2,"y":4,"label":"D","role":"primary"},{"id":"E","x":4,"y":4,"label":"E","role":"purple"}],"edges":[{"from":"A","to":"B","w":1,"color":"green"},{"from":"B","to":"C","w":2,"color":"green"},{"from":"D","to":"E","w":2,"color":"green"},{"from":"B","to":"D","w":3,"color":"green"},{"from":"C","to":"E","w":4},{"from":"A","to":"D","w":5},{"from":"C","to":"D","w":6}]}
```

```diagram
{"type":"dptable","corner":"after edge","col_head":["A","B","C","D","E"],"row_head":["start","AB(1)","BC(2)","DE(2)","BD(3)"],"grid":[["A","B","C","D","E"],["A","A","C","D","E"],["A","A","A","D","E"],["A","A","A","D","D"],["A","A","A","A","A"]],"highlights":[[1,0,"green"],[1,1,"green"],[2,2,"green"],[3,3,"purple"],[3,4,"purple"],[4,0,"green"],[4,4,"green"]],"arrows":[]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":560,"box":300,"title":"Kruskal with DSU","steps":[{"type":"start","text":"Make each vertex its own DSU set"},{"type":"process","text":"Sort all edges by weight"},{"type":"decision","text":"need more edges and edges remain?","yes":"yes","branch":{"label":"no","text":"done or disconnected","role":"primary"}},{"type":"process","text":"take next lightest edge (u,v,w)"},{"type":"decision","text":"find(u) != find(v)?","yes":"yes","branch":{"label":"no","text":"reject cycle","role":"red"}},{"type":"process","text":"add edge to MST; union(u,v)"},{"type":"end","text":"MST has V-1 edges"}]}
```

### 9. Walkthrough

Sorted edges: `AB(1), BC(2), DE(2), BD(3), CE(4), AD(5), CD(6)`. Accept `AB`, merging `{A,B}`. Accept `BC`, merging `{A,B,C}`. Accept `DE`, merging `{D,E}`. Accept `BD`, merging the two components into `{A,B,C,D,E}`. Now `V - 1 = 4` edges are chosen; total weight is `1 + 2 + 2 + 3 = 8`.

### 10. Why It Works

Kruskal's accepted edges never contain a cycle because Union-Find accepts only cross-component edges. For optimality, consider the first edge `e` Kruskal accepts that is absent from some MST `T`. Adding `e` to `T` creates a cycle. That cycle must contain another edge `f` crossing the same component cut at that moment. Since Kruskal processed edges by weight and `e` was the lightest safe crossing edge, `w(e) <= w(f)`. Replacing `f` with `e` yields another MST containing Kruskal's choice. Repeating this exchange proves all choices can be part of an MST.

### 11. Java

```java
int kruskalMst(int n, int[][] edges) {
    Arrays.sort(edges, (a, b) -> Integer.compare(a[2], b[2]));
    UnionFind uf = new UnionFind(n);
    int total = 0;
    int used = 0;

    for (int[] e : edges) {
        int u = e[0], v = e[1], w = e[2];
        if (!uf.union(u, v)) continue;
        total += w;
        used++;
        if (used == n - 1) return total;
    }
    return -1;
}

class UnionFind {
    private final int[] parent;
    private final int[] rank;

    UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }

    boolean union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;
        if (rank[ra] < rank[rb]) {
            parent[ra] = rb;
        } else if (rank[ra] > rank[rb]) {
            parent[rb] = ra;
        } else {
            parent[rb] = ra;
            rank[ra]++;
        }
        return true;
    }
}
```

### 12. Code Walkthrough

Sorting enforces the global greedy order. `union` returns false exactly when `u` and `v` are already in the same tree, so the edge would create a cycle. Path compression flattens DSU trees during `find`; union by rank keeps them shallow.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(E log E), dominated by sorting; DSU operations are effectively O(α(V)) each. **S:** O(V), for parent/rank arrays, excluding the input edge list.

### 14. Edge Cases

- Disconnected graph → no spanning tree; return `-1` or throw depending on API.
- Negative edge weights are fine for MST.
- Parallel edges are fine; cheaper safe one wins.
- Self-loops are always rejected by DSU.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Confusing MST with shortest paths. An MST can give a very poor route between two specific vertices; it minimizes total selected edge weight, not pairwise travel cost.

### 16. Optimization

Stop once `V - 1` edges are accepted. If edges are already sorted or bounded small integer weights, sorting can be optimized with counting/bucket techniques.

### 17. Alternatives

Prim's algorithm grows one tree using a priority queue of crossing edges. It is often better when the graph is naturally represented as adjacency lists and you do not already have an edge list.

### 18. Interview Follow-Ups

- Return the actual edges, not just cost.
- Prove the cut property.
- Find the second-best MST.
- Handle points in the plane where all pairwise Manhattan edges exist.

### 19. Variations

Min Cost to Connect All Points, Optimize Water Distribution in a Village, Accounts Merge (Union-Find without weights), Redundant Connection.

### 20. Pattern Connection

Kruskal is the cleanest example of **greedy + DSU**: sort candidates, accept if they merge components, reject if they preserve connectivity and create a cycle.

### Prim's MST — condensed

!!! pattern "Pattern: Grow cheapest crossing edge · T: O(E log E) · S: O(V + E)"
    **Signals:** undirected weighted graph, adjacency list already available, need minimum total connection cost.

#### Problem

Find an MST by starting from any vertex and repeatedly adding the cheapest edge from the current tree to a vertex outside the tree.

#### Key Observation

!!! key "Key observation"
    At every step, the priority queue contains candidate edges crossing the cut between vertices already in the tree and vertices outside it. The cheapest crossing edge is safe by the cut property.

#### Invariant

The `inMst` vertices are connected by chosen edges, and the heap contains all discovered edges from that set to outside vertices. When a vertex is first accepted from the heap, its connecting edge is the cheapest safe way to grow the tree among known crossing edges.

#### Visual

```diagram
{"type":"graph","directed":false,"nodes":[{"id":"A","x":1,"y":2,"label":"A","role":"green"},{"id":"B","x":3,"y":1,"label":"B","role":"green"},{"id":"C","x":5,"y":2,"label":"C","role":"amber"},{"id":"D","x":2,"y":5,"label":"D","role":"primary"},{"id":"E","x":4,"y":5,"label":"E","role":"purple"}],"edges":[{"from":"A","to":"B","w":1,"color":"green"},{"from":"B","to":"C","w":2,"color":"green"},{"from":"B","to":"D","w":3,"color":"green"},{"from":"D","to":"E","w":2,"color":"green"},{"from":"C","to":"E","w":4},{"from":"A","to":"D","w":5}]}
```

#### Java

```java
int primMst(int n, List<int[]>[] graph) {
    boolean[] inMst = new boolean[n];
    PriorityQueue<int[]> pq = new PriorityQueue<>(
        (a, b) -> Integer.compare(a[1], b[1])
    );
    pq.offer(new int[]{0, 0});
    int total = 0, used = 0;

    while (!pq.isEmpty() && used < n) {
        int[] cur = pq.poll();
        int u = cur[0], cost = cur[1];
        if (inMst[u]) continue;
        inMst[u] = true;
        total += cost;
        used++;

        for (int[] edge : graph[u]) {
            int v = edge[0], w = edge[1];
            if (!inMst[v]) pq.offer(new int[]{v, w});
        }
    }
    return used == n ? total : -1;
}
```

#### Complexity

!!! complexity "Complexity"
    **T:** O(E log E) with duplicate heap entries. **S:** O(V + E), including the adjacency list and heap.

#### Pattern Connection

Prim is Dijkstra-shaped but optimizes the cheapest edge entering the tree, not distance from a source. The heap key is edge weight, not accumulated path length.
