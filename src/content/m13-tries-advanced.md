## Concepts & Mental Models

Tries, union-find, and segment trees solve three different forms of structural reuse. A **trie** is a prefix-sharing automaton: every root-to-node path is a prefix, every edge consumes one character, and all words sharing a prefix share the same state sequence. A search is not "scan all words"; it is "follow the automaton until the next transition is missing."

A **segment tree** is a balanced recursive decomposition of an array. Each node owns an interval `[l, r]` and stores an aggregate for exactly that interval. Range queries split only where necessary, and point updates repair the O(log n) ancestors whose contracts changed.

A **union-find / disjoint set union (DSU)** stores a partition of elements into components. The invariant is precise: **each set has exactly one representative root `r` with `parent[r] == r`; every member reaches that root by repeatedly following `parent`.** Path compression rewires visited nodes directly to the root; union by rank attaches the shallower root under the deeper root. Together they make each operation amortized O(alpha(n)), where `alpha` is the inverse Ackermann function — effectively constant for interview-scale and real systems alike.

!!! key "When to reach for each structure"
    Use a trie when many strings share prefixes or you need prefix pruning. Use DSU when relationships are monotonic merges and you only need component identity. Use a segment tree when an array changes over time and you need repeated associative range aggregates.

---

## Implement Trie (Prefix Tree)

!!! pattern "Pattern: Prefix automaton · T: O(L) per operation · S: O(total characters)"
    **Signals:** dictionary of strings, prefix queries, autocomplete, word existence, shared leading substrings.

### 1. Problem

Design a trie with three operations: `insert(word)`, `search(word)`, and `startsWith(prefix)`. Words are lowercase English letters. `search` must return true only for a complete inserted word; `startsWith` returns true for any prefix path that exists.

### 2. Intuition

A hash set can answer full-word membership, but it cannot expose prefix structure without checking many words. A trie materializes prefixes as states. Inserting `car` and `cat` stores `c -> a` once, then branches at the third character.

### 3. Naive

Store every word in a `HashSet<String>`. `search` is O(L), but `startsWith(prefix)` requires scanning all words or maintaining a second index of every prefix. That is O(number of words * prefix length) per prefix query or inflated preprocessing.

### 4. Key Observation

!!! key "Key observation"
    Prefix queries become O(P) when the dictionary is represented as a graph of prefixes. If you can follow all characters of `prefix` from the root, at least one inserted word has that prefix; the terminal marker is needed only to distinguish `app` from prefix-only `ap`.

### 5. Pattern Recognition

**Signals.** Repeated string prefixes, word dictionary, autocomplete, lexicographic traversal, pruning invalid search branches.

**Shortcut.** If the operation asks "do any stored words begin with this?", build shared-prefix state rather than comparing strings.

**Related.** Word Search II, Replace Words, Design Add and Search Words Data Structure, maximum XOR trie.

### 6. Invariant

For every inserted word `w`, after processing character `w[i]`, there exists a node whose root path spells `w[0..i]`. A node's `end` flag is true iff the exact path from root to that node was inserted as a complete word.

### 7. Visual Explanation

```diagram
{"type":"tree","values":["root","c","a","a","r","t",null],"labels":{"0":"root","1":"c","2":"a","3":"a","4":"r*","5":"t*"},"highlights":{"4":"green","5":"green"},"edge_highlights":[[0,1],[1,3],[3,4],[3,5]]}
```

```diagram
{"type":"tree","values":["root","a",null,"p",null,null,null,"p",null,null,null,null,null,null,null,"*"],"labels":{"0":"root","1":"a","3":"p","7":"p","15":"app*"},"highlights":{"15":"green"},"edge_highlights":[[0,1],[1,3],[3,7],[7,15]]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":460,"box":270,"steps":[{"type":"start","text":"node = root"},{"type":"decision","text":"next char exists?","yes":"yes","branch":{"label":"no","text":"create child for insert\nor return false for query","role":"red"}},{"type":"process","text":"node = child[c]"},{"type":"decision","text":"more chars?","yes":"yes","branch":{"label":"no","text":"insert: mark end\nsearch: return end\nprefix: return true","role":"green"}}]}
```

### 9. Walkthrough

| operation | path followed/created | final answer |
|---|---|---|
| `insert("app")` | root -> a -> p -> p, mark end | — |
| `search("ap")` | root -> a -> p | false; node exists but `end=false` |
| `startsWith("ap")` | root -> a -> p | true |
| `search("app")` | root -> a -> p -> p | true |

### 10. Why It Works

Insertion establishes the invariant by creating exactly the missing transition for each character and marking only the final node. `search` follows the same deterministic transitions; if any transition is missing, no inserted word has that spelling. If all transitions exist, `end` distinguishes a complete word from a strict prefix.

### 11. Java

```java
class Trie {
    private static class Node {
        Node[] child = new Node[26];
        boolean end;
    }

    private final Node root = new Node();

    public void insert(String word) {
        Node cur = root;
        for (char ch : word.toCharArray()) {
            int i = ch - 'a';
            if (cur.child[i] == null) cur.child[i] = new Node();
            cur = cur.child[i];
        }
        cur.end = true;
    }

    public boolean search(String word) {
        Node node = walk(word);
        return node != null && node.end;
    }

    public boolean startsWith(String prefix) {
        return walk(prefix) != null;
    }

    private Node walk(String s) {
        Node cur = root;
        for (char ch : s.toCharArray()) {
            int i = ch - 'a';
            if (cur.child[i] == null) return null;
            cur = cur.child[i];
        }
        return cur;
    }
}
```

### 12. Code Walkthrough

`Node[] child = new Node[26]` gives O(1) transitions for lowercase letters. `walk` centralizes traversal for both exact and prefix queries. `search` adds the terminal check; `startsWith` intentionally does not.

### 13. Complexity

!!! complexity "Complexity"
    **T:** `insert`, `search`, and `startsWith` are O(L), where L is the input string length. **S:** O(total inserted characters) nodes in the worst case; less when prefixes are shared.

### 14. Edge Cases

- Searching a prefix that was never inserted as a word.
- Inserting the same word multiple times — `end` remains true.
- Empty string if allowed: root itself would be marked `end=true`.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Returning true from `search` just because the path exists; that implements prefix search, not word search. Also avoid `containsKey` plus `get` double lookups if using a `Map` node.

### 16. Optimization

Use `Node[26]` for fixed lowercase alphabets; use `Map<Character, Node>` for Unicode, sparse alphabets, or case-sensitive dictionaries. For memory-heavy production tries, compress chains into radix-tree edges.

### 17. Alternatives

A `HashSet` plus prefix set works when only insert/query are needed, but it stores every prefix separately. Sorting supports prefix range queries but complicates dynamic insertion.

### 18. Interview Follow-Ups

- Support delete: unmark `end`, then prune nodes no longer used.
- Support wildcard `.`: DFS over all children at wildcard positions.
- Return all words for a prefix: walk to prefix node, then DFS descendants.

### 19. Variations

- Bitwise trie for maximum XOR.
- Suffix trie/automaton for substring questions.
- Ternary search tree when memory is constrained.

### 20. Pattern Connection

A trie is the string analogue of a decision tree: every consumed character narrows the search state. In Word Search II, the trie becomes a pruning oracle that prevents exploring grid paths that cannot lead to any word.

---

## Word Search II (trie + grid backtracking)

!!! pattern "Pattern: Trie-guided backtracking · T: O(cells * branching) pruned · S: O(total word chars)"
    **Signals:** find many dictionary words in a grid, adjacent-cell paths, avoid running DFS once per word.

### 1. Problem

Given an `m x n` board of lowercase letters and a list of words, return all words that can be formed by sequentially adjacent horizontal/vertical cells. A cell may not be reused in the same word path.

### 2. Intuition

Running a separate DFS for every word repeats the same prefix work. Instead, build one trie for all words and run DFS from each cell. Each partial grid path is checked against the trie; if no dictionary word has that prefix, stop immediately.

### 3. Naive

For each word, start DFS from every board cell and try to match its characters. With W words of length L, the upper bound is O(W * m * n * 4^L), and shared prefixes like `app`, `apple`, `apply` are recomputed.

### 4. Key Observation

!!! key "Key observation"
    The trie converts "is this partial path useful for any word?" into one pointer transition. Backtracking explores only grid paths that are prefixes of at least one remaining dictionary word.

### 5. Pattern Recognition

**Signals.** Multiple target strings, same search space, prefix pruning, paths with visited constraints.

**Shortcut.** If you are about to DFS the board once per word, invert the loop: build a trie once, DFS the board once.

**Related.** Boggle solver, word squares, wildcard trie search with DFS.

### 6. Invariant

At DFS state `(r, c, node)`, `node` represents exactly the trie prefix spelled by the current path before consuming `board[r][c]`. After moving to `next = node.child[ch]`, the path's letters equal the root-to-`next` string, and the visited marks are exactly the cells in that path.

### 7. Visual Explanation

```diagram
{"type":"grid","col_head":["0","1","2"],"row_head":["0","1","2"],"corner":"","grid":[["o","a","t"],["e","t","a"],["i","h","k"]],"highlights":[[0,0,"green"],[0,1,"green"],[0,2,"green"]],"arrows":[{"from":[0,0],"to":[0,1],"color":"green"},{"from":[0,1],"to":[0,2],"color":"green"}]}
```

```diagram
{"type":"tree","values":["root","o","e","a",null,"a",null,"t",null,null,null,"t",null,null,null],"labels":{"0":"root","1":"o","2":"e","3":"a","5":"a","7":"t*","11":"t*"},"highlights":{"7":"green","11":"green"},"edge_highlights":[[0,1],[1,3],[3,7],[0,2],[2,5],[5,11]]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":500,"box":300,"steps":[{"type":"start","text":"Build trie with word stored at terminal nodes"},{"type":"process","text":"Start DFS from every board cell"},{"type":"decision","text":"child for board[r][c]?","yes":"yes","branch":{"label":"no","text":"return; prefix impossible","role":"red"}},{"type":"decision","text":"terminal word found?","yes":"yes","branch":{"label":"yes","text":"add word and null it to dedupe","role":"green"}},{"type":"process","text":"mark cell, explore 4 neighbors, unmark"},{"type":"end","text":"return collected words"}]}
```

### 9. Walkthrough

| step | action | reason |
|---|---|---|
| 1 | Insert `oat`, `eat`, `hat` | one trie represents all targets |
| 2 | DFS at `o` | `root.child['o']` exists |
| 3 | Move to `a`, then `t` | each prefix transition exists |
| 4 | Terminal node contains `oat` | emit and clear terminal word |
| 5 | Neighbor prefix missing | prune without deeper DFS |

### 10. Why It Works

Every valid word path is considered because DFS starts at every cell and explores all non-repeating adjacent paths unless the trie proves no target has that prefix. Pruning cannot remove a solution: if `node.child[ch]` is null, no dictionary word starts with the current path plus `ch`. Terminal nodes report exactly inserted words.

### 11. Java

```java
class Solution {
    private static class Node {
        Node[] child = new Node[26];
        String word;
    }

    private final int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

    public List<String> findWords(char[][] board, String[] words) {
        Node root = build(words);
        List<String> ans = new ArrayList<>();
        int rows = board.length, cols = board[0].length;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                dfs(board, r, c, root, ans);
            }
        }
        return ans;
    }

    private Node build(String[] words) {
        Node root = new Node();
        for (String word : words) {
            Node cur = root;
            for (char ch : word.toCharArray()) {
                int i = ch - 'a';
                if (cur.child[i] == null) cur.child[i] = new Node();
                cur = cur.child[i];
            }
            cur.word = word;
        }
        return root;
    }

    private void dfs(char[][] board, int r, int c, Node node, List<String> ans) {
        if (r < 0 || c < 0 || r == board.length || c == board[0].length) return;
        char ch = board[r][c];
        if (ch == '#') return;
        Node next = node.child[ch - 'a'];
        if (next == null) return;

        if (next.word != null) {
            ans.add(next.word);
            next.word = null;
        }

        board[r][c] = '#';
        for (int[] d : dirs) dfs(board, r + d[0], c + d[1], next, ans);
        board[r][c] = ch;
    }
}
```

### 12. Code Walkthrough

The terminal node stores the full word, avoiding repeated `StringBuilder` reconstruction. `'#'` is an in-place visited marker. Clearing `next.word` deduplicates words found through multiple paths without needing a `Set`.

### 13. Complexity

!!! complexity "Complexity"
    **T:** Building the trie is O(total word characters). DFS is bounded by O(mn * 3^L) after the first step because a path cannot immediately return to the previous cell, and trie pruning usually makes it much smaller. **S:** O(total word characters + L recursion depth).

### 14. Edge Cases

- Duplicate words: terminal clearing returns each word once.
- One-cell board: works for one-letter words.
- Words longer than `m*n`: they will never be emitted.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Forgetting to restore the board cell after DFS corrupts later starts. Another common bug is marking visited before verifying the trie child, then returning early without unmarking.

### 16. Optimization

After exploring a child, you can prune dead trie leaves to reduce later work. Also prefilter words by board letter frequencies when the dictionary is huge.

### 17. Alternatives

DFS once per word is simpler but slower. A DAWG can compress a very large dictionary, but it is overkill for most interviews.

### 18. Interview Follow-Ups

- Allow diagonal moves by expanding `dirs`.
- Return coordinates for each word by carrying the current path.
- Support dynamic dictionary updates by exposing trie insert/delete.

### 19. Variations

- Word Search I is the single-word version without a trie.
- Boggle scoring adds terminal metadata.
- Prefix-constrained board generation reverses the search objective.

### 20. Pattern Connection

This problem composes two patterns: trie prefix pruning and grid backtracking. The senior-level move is recognizing that the trie is not just storage; it is the admissibility test for the recursion tree.

---

## Union-Find / Disjoint Set Union (the data structure + Number of Connected Components)

!!! pattern "Pattern: Monotonic connectivity · T: O((n + e) alpha(n)) · S: O(n)"
    **Signals:** undirected connectivity, components merge over time, equivalence classes, no edge deletions.

### 1. Problem

Implement DSU and use it to count connected components in an undirected graph with `n` nodes labeled `0..n-1` and an edge list. Return the number of components after all edges are processed.

### 2. Intuition

Connectivity is an equivalence relation: reflexive, symmetric, transitive. DSU stores each equivalence class as a rooted tree. Adding an edge between two nodes merges their two classes if they were previously different.

### 3. Naive

Build adjacency lists and run DFS/BFS from every unvisited node. That is O(n + e) and excellent for static graphs, but if edges arrive online and you need connectivity after each addition, repeated traversal is expensive.

### 4. Key Observation

!!! key "Key observation"
    For monotonic connectivity, you never need the full path between nodes — only whether their component representatives match. `union(a, b)` changes the partition only when `find(a) != find(b)`.

### 5. Pattern Recognition

**Signals.** "Connect", "merge accounts", "same group", "number of islands as land is added", Kruskal MST, redundant connection.

**Shortcut.** If relationships only add equivalences and never delete them, DSU is a candidate.

**Related.** Accounts Merge, Friend Circles, Graph Valid Tree, Kruskal's algorithm.

### 6. Invariant

The DSU represents a partition of elements. Each set has exactly one root `r` satisfying `parent[r] == r`; for any element `x`, repeated parent links terminate at that root. Two elements are in the same set iff `find(x) == find(y)`. `rank[root]` upper-bounds tree height and is meaningful only for roots.

### 7. Visual Explanation

```diagram
{"type":"graph","directed":false,"nodes":[{"id":"0","x":0,"y":0,"label":"0","role":"green"},{"id":"1","x":1.4,"y":0,"label":"1","role":"green"},{"id":"2","x":3.2,"y":0,"label":"2","role":"primary"},{"id":"3","x":4.6,"y":0,"label":"3","role":"primary"},{"id":"4","x":6,"y":0,"label":"4","role":"amber"}],"edges":[{"from":"0","to":"1","color":"green"},{"from":"2","to":"3","color":"primary"}]}
```

```diagram
{"type":"recursion","nodes":[{"id":"0","label":"0","x":0,"y":1,"role":"green"},{"id":"1","label":"1 root","x":1,"y":0,"role":"green"},{"id":"2","label":"2","x":3,"y":1,"role":"primary"},{"id":"3","label":"3 root","x":4,"y":0,"role":"primary"},{"id":"merged","label":"root 1 absorbs root 3","x":2,"y":2,"role":"amber"}],"edges":[{"from":"0","to":"1","label":"parent","color":"green"},{"from":"2","to":"3","label":"parent","color":"primary"},{"from":"3","to":"1","label":"union","color":"amber"}]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":470,"box":290,"steps":[{"type":"start","text":"components = n"},{"type":"io","text":"for each edge (u, v)"},{"type":"decision","text":"find(u) == find(v)?","yes":"yes","branch":{"label":"yes","text":"already connected; skip","role":"primary"}},{"type":"process","text":"union roots by rank"},{"type":"process","text":"components--"},{"type":"end","text":"return components"}]}
```

### 9. Walkthrough

| edge | roots before | action | components |
|---|---|---|---|
| init | — | five singleton sets | 5 |
| (0,1) | 0, 1 | merge | 4 |
| (2,3) | 2, 3 | merge | 3 |
| (1,2) | 0/1 root, 2/3 root | merge | 2 |
| (3,0) | same root | skip | 2 |

### 10. Why It Works

An undirected edge asserts that its endpoints belong to the same connected component. If they are already in the same DSU set, transitivity already accounts for that edge. If not, union merges exactly two components into one. By induction over edges, DSU components match graph connected components after each processed prefix.

### 11. Java

```java
class Solution {
    public int countComponents(int n, int[][] edges) {
        DSU dsu = new DSU(n);
        int components = n;
        for (int[] edge : edges) {
            if (dsu.union(edge[0], edge[1])) components--;
        }
        return components;
    }

    static class DSU {
        private final int[] parent;
        private final int[] rank;

        DSU(int n) {
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
}
```

### 12. Code Walkthrough

`find` both discovers and compresses the path to the root. `union` compares roots, not raw nodes. The boolean return tells the caller whether the component count changed.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O((n + e) alpha(n)) for initialization plus all edge operations. `alpha(n)` is effectively constant. **S:** O(n) for `parent` and `rank`.

### 14. Edge Cases

- `n = 0` if allowed: return 0.
- Duplicate edges do not change the component count.
- Self-loops have equal roots and are skipped.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Updating `parent[a]` instead of `parent[rootA]` can corrupt the forest. Another bug is decrementing component count for every edge, including edges within an existing component.

### 16. Optimization

Iterative `find` avoids recursion depth concerns in languages with small stacks. Size-based union is equivalent to rank-based union for interviews and often easier to reason about.

### 17. Alternatives

DFS/BFS is simpler for one static connected-components query. DSU wins when connectivity is incremental, when edges are naturally processed as pairs, or when the graph itself is too expensive to store.

### 18. Interview Follow-Ups

- Detect cycle in an undirected graph.
- Count islands as land is added online.
- Use DSU in Kruskal's MST.
- Explain why DSU does not support arbitrary edge deletion efficiently.

### 19. Variations

- Weighted DSU for equations/ratios.
- DSU with parity for bipartiteness constraints.
- Rollback DSU for offline dynamic connectivity.

### 20. Pattern Connection

DSU is the canonical structure for maintaining equivalence classes. Accounts Merge is the same idea with emails as elements and account rows as merge constraints.

---

## Accounts Merge (union-find application)

### Problem

Given accounts where each row is `[name, email1, email2, ...]`, merge rows that share at least one email. Return each merged account as `[name, sorted emails...]`.

### Key Observation

!!! key "Key observation"
    Emails are the true identities; names are labels. Every account row asserts that all its emails belong to the same connected component.

### Invariant

Each email maps to exactly one DSU id. After processing a row, all emails in that row have the same root as the row's first email. After all rows, emails with equal roots are precisely emails connected by one or more shared-account chains.

### Diagram

```diagram
{"type":"graph","directed":false,"nodes":[{"id":"a","x":0,"y":0,"label":"john@mail","role":"green"},{"id":"b","x":2,"y":0,"label":"john2@mail","role":"green"},{"id":"c","x":4,"y":0,"label":"john3@mail","role":"primary"},{"id":"d","x":2,"y":1.5,"label":"mary@mail","role":"amber"}],"edges":[{"from":"a","to":"b","color":"green"},{"from":"b","to":"c","color":"green"}]}
```

### Algorithm

Assign each unique email a DSU id. For every account, union all emails with the first email in that row. Then group emails by compressed root and output each group with the associated name plus lexicographically sorted emails.

### Java

```java
class Solution {
    public List<List<String>> accountsMerge(List<List<String>> accounts) {
        Map<String, Integer> id = new HashMap<>();
        Map<String, String> emailToName = new HashMap<>();
        int emailCount = 0;
        for (List<String> account : accounts) {
            String name = account.get(0);
            for (int i = 1; i < account.size(); i++) {
                String email = account.get(i);
                if (!id.containsKey(email)) id.put(email, emailCount++);
                emailToName.put(email, name);
            }
        }

        DSU dsu = new DSU(emailCount);
        for (List<String> account : accounts) {
            int first = id.get(account.get(1));
            for (int i = 2; i < account.size(); i++) {
                dsu.union(first, id.get(account.get(i)));
            }
        }

        Map<Integer, TreeSet<String>> groups = new HashMap<>();
        for (String email : id.keySet()) {
            int root = dsu.find(id.get(email));
            groups.computeIfAbsent(root, k -> new TreeSet<>()).add(email);
        }

        List<List<String>> ans = new ArrayList<>();
        for (TreeSet<String> emails : groups.values()) {
            List<String> merged = new ArrayList<>();
            merged.add(emailToName.get(emails.first()));
            merged.addAll(emails);
            ans.add(merged);
        }
        return ans;
    }

    static class DSU {
        int[] parent, rank;
        DSU(int n) {
            parent = new int[n];
            rank = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }
        int find(int x) {
            if (parent[x] != x) parent[x] = find(parent[x]);
            return parent[x];
        }
        void union(int a, int b) {
            int ra = find(a), rb = find(b);
            if (ra == rb) return;
            if (rank[ra] < rank[rb]) parent[ra] = rb;
            else if (rank[ra] > rank[rb]) parent[rb] = ra;
            else { parent[rb] = ra; rank[ra]++; }
        }
    }
}
```

### Complexity

!!! complexity "Complexity"
    Let E be the total number of email occurrences and U the number of unique emails. **T:** O(E alpha(U) + U log U) including sorted output. **S:** O(U) for maps, DSU arrays, and groups.

### Pattern Connection

Accounts Merge is connected components over implicit edges: each row forms a clique, but DSU avoids materializing all pairwise email edges by unioning every email with the row's first email.

---

## Segment Tree for Range Sum Query (build/query/update)

!!! pattern "Pattern: Recursive range decomposition · T: O(log n) query/update · S: O(n)"
    **Signals:** mutable array, repeated range sums/min/max/gcd, point updates, associative aggregate.

### 1. Problem

Design a data structure over an integer array that supports `sumRange(left, right)` and `update(index, value)`. Build once, then answer many range-sum queries while point updates change the array.

### 2. Intuition

Prefix sums answer range sums in O(1), but a point update invalidates every later prefix. A segment tree keeps sums for hierarchical intervals. Updating one element changes only one root-to-leaf path; querying a range touches only intervals that exactly cover disjoint pieces of the query.

### 3. Naive

- Recompute sum by scanning `[left, right]`: O(n) query, O(1) update.
- Prefix sums: O(1) query, O(n) update.

Neither supports both frequent queries and updates efficiently.

### 4. Key Observation

!!! key "Key observation"
    Sum is associative, so a range can be split into disjoint subranges and recombined. Store the sum for every canonical interval in a balanced binary decomposition; both query and update visit O(log n) levels.

### 5. Pattern Recognition

**Signals.** "Range query with updates," "mutable array," "sum/min/max over interval," "many operations."

**Shortcut.** Static range sums: prefix sums. Mutable point updates plus range aggregates: segment tree or Fenwick tree.

**Related.** Fenwick Tree, Range Minimum Query, Lazy Propagation for range updates.

### 6. Invariant

For tree index `node` covering interval `[l, r]`, `tree[node]` equals the sum of `nums[l..r]`. If `l < r`, with `mid = l + (r-l)/2`, the left child covers `[l, mid]`, the right child covers `[mid+1, r]`, and `tree[node] = tree[2*node] + tree[2*node+1]`.

The recursion contract is exact: `query(node, l, r, ql, qr)` returns the sum of `nums[max(l,ql)..min(r,qr)]` contributed by this node's interval, returning 0 for no overlap, `tree[node]` for total cover, and otherwise combining child contributions.

### 7. Visual Explanation

```diagram
{"type":"tree","values":["[0,3]=16","[0,1]=9","[2,3]=7","[0,0]=2","[1,1]=7","[2,2]=3","[3,3]=4"],"labels":{"0":"[0,3] 16","1":"[0,1] 9","2":"[2,3] 7","3":"[0] 2","4":"[1] 7","5":"[2] 3","6":"[3] 4"},"highlights":{"1":"green","5":"green"}}
```

```diagram
{"type":"tree","values":["[0,3]=18","[0,1]=11","[2,3]=7","[0,0]=2","[1,1]=9","[2,2]=3","[3,3]=4"],"labels":{"0":"[0,3] 18","1":"[0,1] 11","2":"[2,3] 7","3":"[0] 2","4":"[1] 9","5":"[2] 3","6":"[3] 4"},"highlights":{"0":"amber","1":"amber","4":"amber"},"edge_highlights":[[0,1],[1,4]]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":500,"box":300,"steps":[{"type":"start","text":"Build(node,l,r)"},{"type":"decision","text":"l == r?","yes":"yes","branch":{"label":"yes","text":"tree[node] = nums[l]","role":"green"}},{"type":"process","text":"build left and right children"},{"type":"process","text":"tree[node] = leftSum + rightSum"},{"type":"io","text":"query/update descends by interval overlap"},{"type":"end","text":"combine affected child results"}]}
```

### 9. Walkthrough

For `nums = [2,7,3,4]`, build stores root sum 16. Query `[1,3]` skips `[0,0]`, takes `[1,1]`, and takes `[2,3]` entirely, returning `7 + 7 = 14`. Updating index 1 to 9 changes `[1,1]` to 9, `[0,1]` to 11, and root to 18.

### 10. Why It Works

The invariant is established bottom-up during build. A point update changes one leaf; recomputing ancestors restores the invariant everywhere else unchanged. A query partitions the requested interval into O(log n) canonical tree intervals. Because sum is associative and those intervals are disjoint, adding their stored sums returns exactly the requested range sum.

### 11. Java

```java
class NumArray {
    private final int n;
    private final int[] nums;
    private final int[] tree;

    public NumArray(int[] nums) {
        this.n = nums.length;
        this.nums = nums.clone();
        this.tree = new int[Math.max(1, 4 * n)];
        if (n > 0) build(1, 0, n - 1);
    }

    public void update(int index, int val) {
        if (n == 0) return;
        update(1, 0, n - 1, index, val);
    }

    public int sumRange(int left, int right) {
        if (n == 0) return 0;
        return query(1, 0, n - 1, left, right);
    }

    private void build(int node, int l, int r) {
        if (l == r) {
            tree[node] = nums[l];
            return;
        }
        int mid = l + (r - l) / 2;
        build(node * 2, l, mid);
        build(node * 2 + 1, mid + 1, r);
        tree[node] = tree[node * 2] + tree[node * 2 + 1];
    }

    private void update(int node, int l, int r, int index, int val) {
        if (l == r) {
            nums[index] = val;
            tree[node] = val;
            return;
        }
        int mid = l + (r - l) / 2;
        if (index <= mid) update(node * 2, l, mid, index, val);
        else update(node * 2 + 1, mid + 1, r, index, val);
        tree[node] = tree[node * 2] + tree[node * 2 + 1];
    }

    private int query(int node, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return tree[node];
        int mid = l + (r - l) / 2;
        return query(node * 2, l, mid, ql, qr)
             + query(node * 2 + 1, mid + 1, r, ql, qr);
    }
}
```

### 12. Code Walkthrough

The array-backed tree uses 1-based indexing so children are `2*node` and `2*node+1`. `4*n` capacity is a standard safe bound for arbitrary `n`. Query's three cases — no overlap, total cover, partial overlap — are the core recursion contract.

### 13. Complexity

!!! complexity "Complexity"
    **T:** Build O(n); point update O(log n); range query O(log n) for canonical segment decomposition. **S:** O(n) for the backing tree and copied values.

### 14. Edge Cases

- Empty input if the API permits it.
- Query of a single index hits one leaf path.
- Negative values work because sums remain associative and identity is 0.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Mixing inclusive and exclusive interval endpoints causes off-by-one errors. Define every node as inclusive `[l, r]` and keep that contract consistent in build, update, and query.

### 16. Optimization

For sum only, a Fenwick tree is shorter and uses O(n) with smaller constants. Segment trees generalize more naturally to min/max, custom aggregates, and lazy propagation.

### 17. Alternatives

- Prefix sum: static arrays only.
- Fenwick tree: point update plus prefix/range sums.
- Sqrt decomposition: simpler, O(sqrt n) operations.

### 18. Interview Follow-Ups

- Add range updates with lazy propagation.
- Change sum to min/max/gcd by changing the aggregate and identity.
- Build an iterative segment tree with leaves at offset `n`.

### 19. Variations

- 2D segment tree for mutable matrix range sums.
- Persistent segment tree for versioned queries.
- Merge-sort tree for order statistics over ranges.

### 20. Pattern Connection

Segment trees are divide-and-conquer made persistent as a data structure. They occupy the same design space as prefix sums, but trade more memory and implementation complexity for efficient mutation.
