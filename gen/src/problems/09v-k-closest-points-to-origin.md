# Top-K / Heap — K Closest Points to Origin

*[↗ LeetCode: K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/top-k-heap)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Uber, Bloomberg, LinkedIn" />

Given `points[][2]` and integer `k`, return the `k` points closest to origin `(0, 0)` (Euclidean).

**Example 1** — `points = [[1,3],[-2,2]], k = 1` → `[[-2,2]]`
**Example 2** — `points = [[3,3],[5,-1],[-2,4]], k = 2` → `[[3,3],[-2,4]]`
**Example 3** — `points = [[0,0],[1,1]], k = 1` → `[[0,0]]`

**Constraints** — `1 ≤ k ≤ n ≤ 10⁴`; `-10⁴ ≤ x, y ≤ 10⁴`. Any order accepted.


<Hints
  hint1="You need the k largest/smallest. Sort is O(n log n). Can you do O(n log k)?"
  hint2="Maintain a heap of size k. Min-heap → k largest at root candidates; max-heap → k smallest."
  hint3="For ’k closest’ or ’k most frequent’, the heap’s comparator holds the distance/frequency metric."
/>
---

## Approach 1 — Sort by distance

**Intuition.** Sort all points by squared distance; take first k.

**Trap** — use squared distance `x² + y²`, not `sqrt` (avoid FP and unnecessary cost).

```java
int[][] kClosestSort(int[][] points, int k) {
    Arrays.sort(points, (a, b) -> (a[0]*a[0] + a[1]*a[1]) - (b[0]*b[0] + b[1]*b[1]));
    return Arrays.copyOfRange(points, 0, k);
}
```

**Complexity** — Time **O(n log n)**; Space **O(1)** in-place sort.

---

## Approach 2 — Max-heap of size k

**Insight from sort.** We don't need to sort everything — maintain a **max-heap** of size `k` on distance. Push each point; if size exceeds k, pop the farthest. The heap always holds the k closest seen so far.

```java
int[][] kClosest(int[][] points, int k) {
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) ->
        (b[0]*b[0] + b[1]*b[1]) - (a[0]*a[0] + a[1]*a[1]));
    for (int[] p : points) {
        pq.offer(p);
        if (pq.size() > k) pq.poll();
    }
    return pq.toArray(new int[0][]);
}
```

<CodeTrace
  title="Max-heap k=2 — points=[[3,3],[5,-1],[-2,4]]"
  :values="['[3,3]','[5,-1]','[-2,4]']"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { heap: "[(3,3):d=18]" }, note: "insert (3,3)" },
    { pointers: { i: 1 }, vars: { heap: "[(5,-1):d=26,(3,3):d=18]" }, note: "insert (5,-1); size=2 ≤ k" },
    { pointers: { i: 2 }, vars: { heap: "[(5,-1):26,(3,3):18,(-2,4):20]" }, note: "size 3 > k → pop max=(5,-1)" },
    { pointers: { i: 3 }, vars: { heap: "[(-2,4):20,(3,3):18]" }, note: "final k closest" }
  ]'
/>

**Complexity** — Time **O(n log k)**; Space **O(k)**.

---

## Approach 3 — Quickselect (avg O(n))

**Insight from heap.** Since we don't need the k closest *in order*, we can partition around the k-th smallest — like Quickselect. Pick pivot; partition; recurse on the side containing the boundary.

```java
int[][] kClosestQS(int[][] points, int k) {
    quickselect(points, 0, points.length - 1, k);
    return Arrays.copyOfRange(points, 0, k);
}
void quickselect(int[][] a, int lo, int hi, int k) {
    if (lo >= hi) return;
    int p = partition(a, lo, hi);
    if (p == k) return;
    if (p < k) quickselect(a, p + 1, hi, k);
    else quickselect(a, lo, p - 1, k);
}
int partition(int[][] a, int lo, int hi) {
    int pivotDist = dist(a[hi]);
    int i = lo;
    for (int j = lo; j < hi; j++)
        if (dist(a[j]) < pivotDist) swap(a, i++, j);
    swap(a, i, hi);
    return i;
}
int dist(int[] p) { return p[0]*p[0] + p[1]*p[1]; }
void swap(int[][] a, int i, int j) { int[] t = a[i]; a[i] = a[j]; a[j] = t; }
```

**Complexity** — Time **O(n)** average; **O(n²)** worst; Space **O(1)** in place (recursion O(log n) avg).

---

## Try it yourself

<JavaRunner problem-slug="k-closest-points-to-origin" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort by distance | O(n log n) | O(1) | baseline; simplest |
| Max-heap of size k | **O(n log k)** | O(k) | canonical Top-K answer |
| Quickselect | O(n) avg | O(1) | best asymptotic when order doesn't matter |

## When to use which

- **Order matters within top-k** → max-heap or sort.
- **Order doesn't matter, best avg time** → Quickselect.
- **Streaming (points arrive one by one)** → max-heap.
- **k close to n** → sort or min-heap of size (n-k).

<AiCompanion problem-slug="k-closest-points-to-origin" pattern-hint="top-K / heap" />

## Related problems

- [Top K Frequent Elements](/problems/top-k-frequent-elements) — canonical Top-K
- [Kth Largest Element in an Array](/problems/quickselect-kth-largest) — Quickselect archetype
- [Kth Largest Element in a Stream](/problems/kth-largest-element-in-a-stream) — streaming
- [Kth Smallest Element in a Sorted Matrix](/problems/kth-smallest-element-in-a-sorted-matrix) — BS-on-answer alternative