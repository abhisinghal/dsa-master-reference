# Segment Tree &amp; Fenwick Tree

When you need **both** range queries and point/range updates in O(log n), a flat prefix-sum array (O(n) update) no longer suffices. Two structures solve this: the **Fenwick tree** (BIT) — tiny, fast, ideal for prefix sums with point updates — and the **segment tree** — more general, supporting any associative range aggregate and (with lazy propagation) range updates.

```text
Fenwick idea: index i is responsible for a range of length (i & -i).
update/query walk O(log n) indices by adding/removing the lowest set bit.
```

## Fenwick Tree (Binary Indexed Tree) <span class="diff diff-m">Medium</span>


*[↗ LeetCode: Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/)*

<ProgressCheck id="fenwick-tree-binary-indexed-tree" />

### Problem

Support **point updates** and **prefix-sum (or range-sum) queries** on a mutable array, each in O(log n).

**Constraints:** up to `3·10⁴` mixed update/query operations.

**Example:** after `update(i, +v)`, `prefixSum(k)` returns the running total including the update.

**Example 1:** After add(3,5), prefix sums at indices >= 3 include +5.

**Example 2:** rangeSum(l,r) = sum(r) - sum(l-1).

### Solution — brute force

Ignore the structural shortcut and scan/recompute from scratch for each decision.

```text
for each query or candidate:
  scan the relevant array/list/tree/graph state
  recompute the answer directly
```

Brute-force complexity: usually O(n) per operation or O(n^2)+ overall, with extra space when a copied structure is used.

### Solution — optimized

**Pattern:**
Point update + prefix-sum query in O(log n) using the `i & -i` lowest-set-bit stride.

> [key] **Key Insight** — Each Fenwick index `i` stores the sum of `a[i - (i&-i) + 1 .. i]`. To update, walk *up* adding `i += i & -i`; to query a prefix, walk *down* subtracting `i -= i & -i`. Range sum `[l,r] = query(r) − query(l-1)`.

**Java (1-indexed):**
```java
class Fenwick {
    private final long[] tree;
    Fenwick(int n) { tree = new long[n + 1]; }
    void update(int i, long delta) {                 // add delta at index i (1-based)
        for (; i < tree.length; i += i & -i) tree[i] += delta;
    }
    long query(int i) {                              // prefix sum [1..i]
        long s = 0;
        for (; i > 0; i -= i & -i) s += tree[i];
        return s;
    }
    long range(int l, int r) { return query(r) - query(l - 1); }
}
```

> [note] **Trace it** — `prefixSum(6)` visits indices `6 → 4 → 0` (each step strips the lowest set bit via `i -= i & -i`), summing three stored partials instead of six elements.

### Time Complexity

O(log n) per point update and prefix/range query.

Original summary: Update/query O(log n) · Build O(n log n) (or O(n) with a linear build) · Space O(n).

### Space Complexity

O(n) for the 1-indexed tree array.

> [trap] **Common Trap** — 0-index vs 1-index confusion. *Example:* `update(i)` for `i=0` with 0-indexed `i` gives `i & -i == 0`, so the loop never advances. Fenwick trees are naturally 1-indexed; shift external indices by +1 or handle the 0 case explicitly.

> [pat] **Pattern Connection** — BIT answers *Count of Smaller Numbers After Self* (compress values, sweep right-to-left, query prefix counts), *Range Sum Query — Mutable*, and inversion counting.

### Learning notes

- Why 1-indexing? lowbit loops need 0 as the stop state.
- Why i & -i? It isolates the covered range size.
- Why sum(r)-sum(l-1)? Ranges are prefix differences.
- Why Fenwick over segment tree? Shorter/faster for point updates plus prefix sums.

#### Same pattern, new tweaks

Point-update + prefix-query in O(log n):

| Variation | The one thing that changes | Time |
|---|---|---|
| [Range Sum Query — Mutable](https://leetcode.com/problems/range-sum-query-mutable/) | the canonical use — update one index, query any prefix/range | — |
| [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | compress values, sweep right→left, and query "how many smaller seen so far." | — |
| [Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) | a BIT over compressed values counting `a[i] > 2·a[j]` | — |
| [Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/) | a BIT over prefix sums | — |

## Segment Tree (range query + range update) <span class="diff diff-m">Medium</span>


*[↗ LeetCode: Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/)*

<ProgressCheck id="segment-tree-range-query-range-update" />

### Problem

Support **range queries** (sum/min/max) and **updates** on a mutable array, each in O(log n); with lazy propagation, whole-range updates too.

**Constraints:** up to ~`10⁵` elements and operations.

**Example:** over `[1,3,5,7,9,11]`, `sum(1..3) = 15`; after `update(1, +2)`, `sum(1..3) = 17`.

**Example 1:** Query [l,r] combines O(log n) canonical segments.

**Example 2:** After updating index 2, every segment covering index 2 recomputes its sum.

### Solution — brute force

Ignore the structural shortcut and scan/recompute from scratch for each decision.

```text
for each query or candidate:
  scan the relevant array/list/tree/graph state
  recompute the answer directly
```

Brute-force complexity: usually O(n) per operation or O(n^2)+ overall, with extra space when a copied structure is used.

### Solution — optimized

**Pattern:**
A binary tree over array segments; each node stores an aggregate of its range. Queries and updates split into O(log n) canonical nodes. **Lazy propagation** defers range updates until a child is actually needed.

> [inv] **Invariant** — Each internal node's value is the aggregate (sum/min/max) of its two children; a pending lazy tag means "this node's value is current, but children haven't been informed yet."

**Java (sum segment tree, point update):**
```java
class SegTree {
    private final int n;
    private final long[] t;
    SegTree(int[] a) {
        n = a.length; t = new long[2 * n];
        for (int i = 0; i < n; i++) t[n + i] = a[i];       // leaves
        for (int i = n - 1; i > 0; i--) t[i] = t[2*i] + t[2*i+1];
    }
    void update(int i, long val) {                          // point assign
        for (t[i += n] = val; i > 1; i >>= 1)
            t[i >> 1] = t[i] + t[i ^ 1];                    // recompute parents
    }
    long query(int l, int r) {                              // sum [l, r)
        long res = 0;
        for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
            if ((l & 1) == 1) res += t[l++];
            if ((r & 1) == 1) res += t[--r];
        }
        return res;
    }
}
```

> [note] **Trace it** — over `[1,3,5,7,9,11]`, a query for `sum(1..3)` combines two canonical nodes (covering `[1,1]` and `[2,3]`) → `3 + (5+7) = 15`, touching O(log n) nodes instead of scanning the range.

**Java (lazy propagation — range add + range sum):**
```java
class LazySeg {
    private final int n;
    private final long[] sum, lazy;                        // lazy[node] = pending "+x" for the subtree
    LazySeg(int n) { this.n = n; sum = new long[4*n]; lazy = new long[4*n]; }

    private void push(int node, int l, int r) {            // apply this node's tag, hand it to children
        if (lazy[node] == 0) return;
        int mid = (l + r) >>> 1, lc = 2*node, rc = 2*node+1;
        sum[lc] += lazy[node] * (mid - l + 1); lazy[lc] += lazy[node];
        sum[rc] += lazy[node] * (r - mid);     lazy[rc] += lazy[node];
        lazy[node] = 0;
    }
    void update(int node, int l, int r, int ql, int qr, long v) {   // add v to [ql,qr]
        if (qr < l || r < ql) return;                      // disjoint
        if (ql <= l && r <= qr) {                          // fully covered → tag, don't recurse
            sum[node] += v * (r - l + 1); lazy[node] += v; return;
        }
        push(node, l, r);
        int mid = (l + r) >>> 1;
        update(2*node, l, mid, ql, qr, v);
        update(2*node+1, mid+1, r, ql, qr, v);
        sum[node] = sum[2*node] + sum[2*node+1];
    }
    long query(int node, int l, int r, int ql, int qr) {   // sum of [ql,qr]
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return sum[node];
        push(node, l, r);
        int mid = (l + r) >>> 1;
        return query(2*node, l, mid, ql, qr) + query(2*node+1, mid+1, r, ql, qr);
    }
}
```

> [note] **Trace it** — `update(1,0,n-1, 1,3, +2)` on `[1,3,5,7,9,11]` never touches leaves `1..3` individually: nodes fully inside `[1,3]` get a `+2` tag and their `sum` bumped by `2 × (width)`. A later `query` that dives past a tagged node calls `push` first, so children see the pending add exactly when — and only when — they're needed.

> [trap] **Common Trap** — Forgetting `push` before recursing into children. *Example:* range-add a `+5` tag on a node, then query one of its children without pushing. The child returns its stale sum (missing the +5) and the aggregate is wrong. Push lazy tags at the top of both `update` and `query` before recursing.

> [pat] **Pattern Connection** — Segment trees back *Range Sum/Min/Max Query — Mutable*, *Range Add + Range Sum* (lazy), *The Skyline Problem* (segment tree on heights), and *Count of Range Sum*. When only prefix sums with point updates are needed, prefer the simpler, faster Fenwick tree.

### Time Complexity

O(log n) per point update/range query; lazy range operations are also O(log n).

Original summary: Query/update O(log n) · Build O(n) · Space O(n).

### Space Complexity

O(n) logically, commonly allocated as O(4n).

> [key] **Key Insight** — The iterative bottom-up segment tree above is compact and cache-friendly for point updates. For **range updates** (add v to `[l,r]`), add lazy tags and a recursive `push-down`: apply the tag to a node, mark its children pending, and only propagate when recursing into them.

### Learning notes

- Why 4*n size? Safe upper bound for recursive layout.
- Why split at mid? Nodes summarize contiguous halves.
- Why no-overlap returns 0? Sum identity contributes nothing.
- Why lazy propagation? Range updates defer child work.
- Why segment tree over Fenwick? It handles richer range operations.

#### Same pattern, new tweaks

Any associative range aggregate, in O(log n):

| Variation | The one thing that changes | Time |
|---|---|---|
| [Range Sum/Min/Max Query — Mutable](https://leetcode.com/problems/range-sum-query-mutable/) | swap the combine function (`+`, `min`, `max`) and the identity element | — |
| [Range Add + Range Sum](https://leetcode.com/problems/range-sum-query-mutable/) | add **lazy propagation** so a whole range updates in | O(log n) |
| [The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/) | a segment tree over x-coordinates tracking the max active height | — |
| [Count of Range Sum / Range Module](https://leetcode.com/problems/count-of-range-sum/) | a dynamic/segment tree over value or coordinate space | — |
