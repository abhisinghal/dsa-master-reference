# K-way Merge — Ugly Number II

*[↗ LeetCode: Ugly Number II](https://leetcode.com/problems/ugly-number-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/k-way-merge)

An "ugly number" has only 2, 3, or 5 as prime factors. Return the `n`-th ugly number (1-indexed; 1 counts as ugly).

**Example** — `n=10` → `12` (sequence `1,2,3,4,5,6,8,9,10,12`)

**Constraints** — `1 ≤ n ≤ 1690`.

---

## Approach 1 — Brute force check every integer

For each candidate `k = 1, 2, 3…`, factor out all 2/3/5; if result is 1, it's ugly. Count until `n`. O(n·log candidate).

**Complexity** — Slow at n=1690.

## Approach 2 — Min-heap of frontier candidates

**Insight.** If `u` is ugly, so are `2u, 3u, 5u`. Start with `{1}` in a min-heap + a seen-set. Pop smallest → push `2x, 3x, 5x` for that x. The n-th pop is the answer.



```java
int nthUglyNumberHeap(int n) {
    PriorityQueue<Long> heap = new PriorityQueue<>();
    Set<Long> seen = new HashSet<>();
    heap.offer(1L); seen.add(1L);
    long u = 1;
    for (int i = 0; i < n; i++) {
        u = heap.poll();
        for (int p : new int[]{2, 3, 5}) {
            long next = u * p;
            if (seen.add(next)) heap.offer(next);
        }
    }
    return (int) u;
}
```



**Complexity** — Time **O(n log n)**; Space **O(n)**.

## Approach 3 — Three-way merge (DP with 3 pointers)

**Insight.** Every ugly number is one of prev-uglies × 2, × 3, or × 5. Maintain three pointers `i2, i3, i5` into the sequence-so-far, each pointing at the smallest prev-ugly whose ×p hasn't been emitted yet. Next ugly = `min(u[i2]*2, u[i3]*3, u[i5]*5)`.



```java
int nthUglyNumber(int n) {
    int[] u = new int[n];
    u[0] = 1;
    int i2 = 0, i3 = 0, i5 = 0;
    for (int i = 1; i < n; i++) {
        int n2 = u[i2] * 2, n3 = u[i3] * 3, n5 = u[i5] * 5;
        int next = Math.min(n2, Math.min(n3, n5));
        u[i] = next;
        if (next == n2) i2++;
        if (next == n3) i3++;
        if (next == n5) i5++;
    }
    return u[n - 1];
}
```



<CodeTrace
  title="3-way merge — first 10 ugly numbers"
  :values="[1,2,3,4,5,6,8,9,10,12]"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0, i2: 0, i3: 0, i5: 0 }, vars: { emit: 1 }, note: "seed", added: [0] },
    { pointers: { i: 1, i2: 1, i3: 0, i5: 0 }, vars: { emit: 2 }, note: "min(2,3,5)=2 → advance i2", added: [1] },
    { pointers: { i: 2, i2: 1, i3: 1, i5: 0 }, vars: { emit: 3 }, note: "min(4,3,5)=3 → advance i3", added: [2] },
    { pointers: { i: 3, i2: 2, i3: 1, i5: 0 }, vars: { emit: 4 }, note: "min(4,6,5)=4 → advance i2", added: [3] },
    { pointers: { i: 9, i2: 5, i3: 3, i5: 1 }, vars: { emit: 12 }, note: "…10th ugly = 12", added: [9] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)**. Optimal.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute check each integer | ~O(n · log) | O(1) |
| Min-heap of frontier | O(n log n) | O(n) |
| 3-way merge pointers | **O(n)** | O(n) |

## Related problems

- [Super Ugly Number](https://leetcode.com/problems/super-ugly-number/) — k primes; generalized k-way merge
- [Merge k Sorted Lists](/problems/k-way-merge-k-sorted-lists) — same k-way merge shape
- [Nth Digit](https://leetcode.com/problems/nth-digit/) — different counting problem
