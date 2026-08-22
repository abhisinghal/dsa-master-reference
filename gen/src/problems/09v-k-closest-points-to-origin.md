# Top-K / Heap — K Closest Points to Origin

*[↗ LeetCode: K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/top-k-heap)

Given `points[][2]` and `k`, return the `k` closest to origin (by Euclidean distance).

**Example** — `points=[[1,3],[-2,2]], k=1` → `[[-2,2]]`

---

## Approach 1 — Sort by distance

```java
int[][] kClosestSort(int[][] p, int k) {
    Arrays.sort(p, (a, b) -> (a[0]*a[0]+a[1]*a[1]) - (b[0]*b[0]+b[1]*b[1]));
    return Arrays.copyOfRange(p, 0, k);
}
```

**Complexity** — Time **O(n log n)**; Space **O(1)**.

## Approach 2 — Max-heap of size k

**Insight.** Only the top-k closest matter. Keep a *max*-heap of size k (evict the farthest each insert). Root is the k-th closest at the end; heap contents are the answer.

```java
int[][] kClosestHeap(int[][] p, int k) {
    PriorityQueue<int[]> heap = new PriorityQueue<>(
        (a, b) -> (b[0]*b[0]+b[1]*b[1]) - (a[0]*a[0]+a[1]*a[1])
    );
    for (int[] pt : p) {
        heap.offer(pt);
        if (heap.size() > k) heap.poll();
    }
    return heap.toArray(new int[0][]);
}
```

**Complexity** — Time **O(n log k)**; Space **O(k)**. Good when k << n.

## Approach 3 — Quickselect

**Insight.** Partition around a random pivot's distance; recurse into only the half containing the k-th closest boundary. O(n) expected.

```java
int[][] kClosest(int[][] p, int k) {
    quickSelect(p, 0, p.length - 1, k);
    return Arrays.copyOfRange(p, 0, k);
}
int dist(int[] pt) { return pt[0]*pt[0] + pt[1]*pt[1]; }
void quickSelect(int[][] p, int lo, int hi, int k) {
    while (lo < hi) {
        int pi = partition(p, lo, hi);
        if (pi + 1 == k) return;
        else if (pi + 1 < k) lo = pi + 1;
        else                 hi = pi - 1;
    }
}
int partition(int[][] p, int lo, int hi) {
    int pivot = dist(p[hi]), store = lo;
    for (int i = lo; i < hi; i++) if (dist(p[i]) < pivot) swap(p, store++, i);
    swap(p, store, hi); return store;
}
void swap(int[][] p, int i, int j) { int[] t = p[i]; p[i] = p[j]; p[j] = t; }
```

<CodeTrace
  title="Quickselect by distance — points, k=2"
  :values="['(1,3)','(-2,2)','(2,-2)','(5,8)']"
  :windowKeys="['lo','hi']"
  :cellWidth="52"
  :steps='[
    { pointers: { lo: 0, hi: 3, pivot: 3 }, vars: { distances: "[10,8,8,89]", pivotDist: 89 }, note: "pivot 89 → partition → store=3" },
    { pointers: { lo: 0, hi: 2, pivot: 2 }, vars: { pivotDist: 8 }, note: "search left; pivot 8 → store=2" },
    { pointers: { lo: 0, hi: 1 }, vars: { answer: "(-2,2), (2,-2)" }, note: "converged at k=2", added: [1,2] }
  ]'
/>

**Complexity** — Time **O(n)** expected; Space **O(1)**. Optimal.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Sort | O(n log n) | O(1) |
| Max-heap size k | O(n log k) | O(k) |
| Quickselect | **O(n) avg** | **O(1)** |

## Related problems

- [Kth Largest Element](/problems/quickselect-kth-largest) — quickselect prototype
- [Top K Frequent](/problems/top-k-frequent-elements) — heap or bucket sort
- [Kth Smallest in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) — heap on rows
