# K-way Merge — Smallest Range Covering K Lists

*[↗ LeetCode: Smallest Range Covering Elements from K Lists](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/k-way-merge)

Given `k` sorted lists, find the smallest range `[a, b]` that contains at least one element from each list.

**Example** — `[[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]` → `[20,24]` (contains 24, 20, 22)

---

## Approach 1 — Cartesian product (brute force)

Enumerate every combination of "one element from each list"; track min range width. **O(n^k)** — TLE fast.

## Approach 2 — Sliding window over merged elements

**Insight.** Merge all elements into one sorted array tagged by list-of-origin. Sliding window with a `have`/`need` map ensures all k lists represented; track min window width.

**Complexity** — Time **O(N log N)** for merge sort; Space **O(N)**.

## Approach 3 — Min-heap of "one from each list"

**Insight from window.** Maintain a min-heap of exactly one element from each list. The range = `[min(heap), max_seen]`. Pop the min → advance that list; if that list's next value exceeds `max_seen`, update `max_seen`. Repeat.



```java
int[] smallestRange(List<List<Integer>> lists) {
    PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    int max = Integer.MIN_VALUE;
    for (int i = 0; i < lists.size(); i++) {
        int v = lists.get(i).get(0);
        heap.offer(new int[]{v, i, 0});
        max = Math.max(max, v);
    }
    int[] best = {heap.peek()[0], max};
    while (heap.size() == lists.size()) {
        int[] top = heap.poll();
        if (max - top[0] < best[1] - best[0]) { best[0] = top[0]; best[1] = max; }
        int nextIdx = top[2] + 1;
        if (nextIdx < lists.get(top[1]).size()) {
            int v = lists.get(top[1]).get(nextIdx);
            heap.offer(new int[]{v, top[1], nextIdx});
            max = Math.max(max, v);
        }
    }
    return best;
}
```



<CodeTrace
  title="Min-heap merge — [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]"
  :values="[4,10,15,24,26]"
  :windowKeys="['step']"
  :cellWidth="42"
  :steps='[
    { pointers: { step: 0 }, vars: { heap: "[0,4,5]", max: 5, range: "[0,5]" }, note: "seed with head of each list. width 5" },
    { pointers: { step: 1 }, vars: { heap: "[4,5,9]", max: 9, range: "[4,9]" }, note: "advance list1 (0→9). width 5" },
    { pointers: { step: 2 }, vars: { heap: "[5,9,10]", max: 10 }, note: "advance list0 (4→10)" },
    { pointers: { step: 3 }, vars: { heap: "[9,10,18]", max: 18 }, note: "advance list2 (5→18)" },
    { pointers: { step: 6 }, vars: { heap: "[20,24,22]", max: 24, best: "[20,24]" }, note: "final smallest range = [20,24]", added: [3] }
  ]'
/>

**Complexity** — Time **O(N log k)** where N = total elements; Space **O(k)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Cartesian product | O(n^k) | O(1) |
| Merge + sliding window | O(N log N) | O(N) |
| Min-heap "one from each" | **O(N log k)** | **O(k)** |

## Related problems

- [Merge k Sorted Lists](/problems/k-way-merge-k-sorted-lists) — heap of live heads
- [Ugly Number II](/problems/ugly-number-ii) — 3-way merge
- [Find K Pairs with Smallest Sums](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/)
