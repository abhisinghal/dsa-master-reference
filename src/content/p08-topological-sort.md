## The Pattern

Topological Sort orders directed dependencies so every prerequisite appears before the work that depends on it. Use **Kahn's algorithm** when you want an explicit queue of currently-unblocked nodes; use **DFS post-order** when recursive dependency expansion is more natural.

!!! pattern "Recognition signals"
    **Signals:** prerequisites, build order, dependency graph, course schedule, alien alphabet, "must happen before", or cycle detection in directed edges. The graph must be directed; undirected cycle logic is a different pattern.

```diagram
{"type":"graph","title":"DAG with indegree annotations","directed":true,"nodes":[{"id":"A","x":0,"y":1,"role":"green","label":"A\nin=0"},{"id":"B","x":2,"y":0,"role":"primary","label":"B\nin=1"},{"id":"C","x":2,"y":2,"role":"primary","label":"C\nin=1"},{"id":"D","x":4,"y":1,"role":"amber","label":"D\nin=2"}],"edges":[{"from":"A","to":"B","directed":true},{"from":"A","to":"C","directed":true},{"from":"B","to":"D","directed":true},{"from":"C","to":"D","directed":true}],"caption":"Kahn starts with indegree-0 nodes; removing A unlocks B and C, then D."}
```

## The Invariant

In Kahn's algorithm, the queue contains exactly nodes with current indegree 0 among the unprocessed subgraph. Popping a node is safe because no remaining prerequisite points to it. If the algorithm processes fewer than `n` nodes, the unprocessed remainder has no indegree-0 node, which implies a directed cycle.

## Template

```java
List<Integer> topoSort(int n, int[][] edges) {
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    int[] indegree = new int[n];

    for (int[] e : edges) {
        int from = e[0], to = e[1];
        graph.get(from).add(to);
        indegree[to]++;
    }

    ArrayDeque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        if (indegree[i] == 0) q.offer(i);
    }

    List<Integer> order = new ArrayList<>();
    while (!q.isEmpty()) {
        int u = q.poll();
        order.add(u);
        for (int v : graph.get(u)) {
            if (--indegree[v] == 0) q.offer(v);
        }
    }
    return order.size() == n ? order : List.of();
}
```

DFS alternative: mark each node `0=unseen, 1=visiting, 2=done`; a `visiting → visiting` edge is a cycle; append nodes on exit and reverse the result.

## Worked Recognition

- **Course Schedule** (Module 11): courses are nodes and prerequisites are directed edges. Kahn detects whether all courses can be processed.
- **Alien Dictionary** (Module 11): adjacent sorted words imply character precedence edges; topological order reconstructs one valid alphabet, while cycles or invalid prefixes reject the input.
- Build/package planning: libraries with no remaining incoming dependencies are safe to compile/install next.

## Complexity

!!! complexity "Complexity"
    **T:** O(V + E) for Kahn or DFS. **S:** O(V + E) for adjacency plus O(V) indegree/marks/queue. Lexicographically smallest orders add a priority queue and become O((V + E) log V).

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Reversing prerequisite edge direction; failing to include isolated nodes; using `Stack` instead of `ArrayDeque`; not detecting cycles by processed-count or DFS colors; ignoring duplicate edges that inflate indegree; or accepting Alien Dictionary inputs where a longer word precedes its exact prefix.

## When NOT to use it

Do not use topological sort on undirected graphs, graphs where cycles are valid business states, shortest-path problems with weighted dependencies, or scheduling problems where duration/resource constraints dominate ordering.
