## The Pattern

Union-Find, or Disjoint Set Union (DSU), maintains a partition of `n` elements under two operations: `find(x)` returns the representative of x's component, and `union(a, b)` merges two components. It is the right pattern when connectivity is built by a stream of equivalence facts: every edge says "these two endpoints now belong to the same set."

!!! pattern "Recognition signals"
    **Signals:** dynamic connectivity, "are these in the same group?", merge accounts/emails, count components as edges arrive, or choose safe edges by component membership. Prefer it over DFS/BFS when unions are incremental or repeated connectivity queries would otherwise rescan the graph.

```diagram
{"type":"graph","directed":false,"nodes":[{"id":"0","x":0,"y":0,"role":"primary","label":"0"},{"id":"1","x":1.4,"y":0,"role":"primary","label":"1"},{"id":"2","x":3.2,"y":0,"role":"amber","label":"2"},{"id":"3","x":4.6,"y":0,"role":"amber","label":"3"},{"id":"4","x":2.3,"y":1.4,"role":"green","label":"4"}],"edges":[{"from":"0","to":"1","color":"primary"},{"from":"2","to":"3","color":"amber"},{"from":"1","to":"4","color":"green"},{"from":"3","to":"4","color":"green","dash":true}]}
```

## The Invariant

`parent[root] == root` exactly for component representatives. For every node x, repeatedly following `parent` pointers reaches the representative of x's current component. `rank` (or size) is a balancing hint: attach the shallower tree under the deeper tree; if ranks tie, choose one root and increment its rank.

Path compression strengthens the invariant operationally: after `find(x)`, every node on x's search path points directly to the representative. Union by rank prevents tall trees from forming; path compression flattens whatever remains. Together they give amortized **α(n)** time, effectively constant for interview-scale inputs.

## Template

```java
final class DSU {
    private final int[] parent;
    private final int[] rank;
    private int components;

    DSU(int n) {
        parent = new int[n];
        rank = new int[n];
        components = n;
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
        components--;
        return true;
    }

    boolean connected(int a, int b) {
        return find(a) == find(b);
    }

    int components() {
        return components;
    }
}
```

## Worked Recognition

- **Number of Connected Components** (Module 11): each undirected edge is a `union(u, v)`; the answer is the DSU component count after all successful merges. DFS is equally valid for one static pass, but DSU wins when edges are streamed or queries interleave with updates.
- **Accounts Merge** (Module 11): each email is an identity node; emails appearing in the same account are unioned. The representative becomes the grouping key, while sorting emails is a separate output-formatting concern.
- **Kruskal** (Module 13): process edges by increasing weight; accept an edge only when `union(u, v)` succeeds. DSU encodes "does this edge create a cycle?" in α(n) time.

## Complexity

!!! complexity "Complexity"
    **T:** O((n + m) α(n)) for initialization plus m operations with path compression and union by rank. **S:** O(n) for `parent` and `rank`. Without both optimizations, adversarial unions can degrade to linear-height trees.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Forgetting to call `find` before comparing parents, decrementing component count on a no-op union, using rank as exact height after path compression, or solving dynamic connectivity with repeated DFS. Also normalize external keys first: emails, strings, and sparse IDs need a map to dense integer IDs.

## When NOT to use it

Do not use DSU when you need the actual traversal order, shortest paths, directed reachability, deletions, or per-component structure that changes after arbitrary splits. For one-off static connected components, DFS/BFS may be simpler and just as fast asymptotically.
