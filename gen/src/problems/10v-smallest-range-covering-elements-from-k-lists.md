# K-way Merge — Smallest Range Covering Elements from K Lists

*[↗ LeetCode: Smallest Range Covering Elements from K Lists](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/k-way-merge)

<CompanyTags companies="Google, Amazon" />

Given `k` sorted lists of integers, find the smallest range `[a, b]` that contains **at least one element from each list**. If multiple, return the one with smaller `a`; if still tied, smaller `b`.

**Example 1** — `lists = [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]` → `[20, 24]` (24-20=4)
**Example 2** — `lists = [[1,2,3],[1,2,3],[1,2,3]]` → `[1, 1]`

**Constraints** — `1 ≤ k ≤ 3500`; total elements ≤ 5·10⁴.


<Hints
  hint1="You have k sorted sequences. Which element is globally next?"
  hint2="Min-heap of size k, one head per list. Pop smallest, emit, push its successor from the same list."
  hint3="For ’smallest range covering k lists’, track max-in-heap; window is [minInHeap, maxSeen]."
/>
---

<MarkSolved problem-slug="smallest-range-covering-elements-from-k-lists" />


## Approach 1 — Merge, sweep with sliding window on tagged list

**Intuition.** Merge all values with `(value, listId)` tags; sort by value; slide a window over the merged sequence containing at least one from every list; track shortest.

**Complexity** — Time **O(N log N)** for sort; Space **O(N)**.

---

## Approach 2 — Min-heap sweep (canonical)

**Insight from merge.** We only need to know the current minimum across all lists (candidate `a`) and track the current max (candidate `b`). A min-heap containing one pointer per list serves this.

- Init: heap of `(lists[i][0], i, 0)`; track `maxSeen` initially = max of all first elements.
- Loop: pop min → it's the current `a`. Range `[a, maxSeen]` is a candidate.
- Advance pointer in that list; push next; update `maxSeen`.
- Stop when a list is exhausted (we can't cover it anymore).

```java
int[] smallestRange(List<List<Integer>> lists) {
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    int maxSeen = Integer.MIN_VALUE;
    for (int i = 0; i < lists.size(); i++) {
        pq.offer(new int[]{lists.get(i).get(0), i, 0});
        maxSeen = Math.max(maxSeen, lists.get(i).get(0));
    }
    int[] best = {-100000, 100000};
    while (true) {
        int[] top = pq.poll();
        int a = top[0];
        if (maxSeen - a < best[1] - best[0]) { best[0] = a; best[1] = maxSeen; }
        if (top[2] + 1 == lists.get(top[1]).size()) break;
        int next = lists.get(top[1]).get(top[2] + 1);
        maxSeen = Math.max(maxSeen, next);
        pq.offer(new int[]{next, top[1], top[2] + 1});
    }
    return best;
}
```

<CodeTrace
  title="Heap sweep — lists as in Example 1"
  :values="['4','0','5','...','20','24']"
  :windowKeys="['min','max']"
  :cellWidth="34"
  :steps='[
    { pointers: { min: 1, max: 2 }, vars: { window: "[0,5]", diff: 5 }, note: "initial: min from list1=0, max=5" },
    { pointers: { min: 0, max: 2 }, vars: { window: "[4,10]", diff: 6 }, note: "pop 0 → advance list1 to 9; max now 10" },
    { pointers: { min: 0, max: 3 }, vars: { window: "[5,18]", diff: 13 }, note: "pop 4 → advance list0 to 10; max 18" },
    { pointers: { min: 1, max: 4 }, vars: { window: "[20,24]", diff: 4 }, note: "after several steps — best window found" }
  ]'
/>

**Complexity** — Time **O(N log k)** where N = total elements; Space **O(k)**.

---

## Try it yourself

<JavaRunner problem-slug="smallest-range-covering-elements-from-k-lists" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Merge + sliding window | O(N log N) | O(N) | acceptable baseline |
| Min-heap sweep | **O(N log k)** | **O(k)** | canonical |

## When to use which

- **Standard k-way merge with "cover all" requirement** → min-heap sweep.
- **Lists arrive as streams (unknown length)** → same min-heap works; break on any list exhausted.
- **"Range covering ≥ m of k lists"** → generalize; needs a multi-set or ordered map.
- **Instead of range: find k-th smallest overall** → still min-heap sweep, just count pops.

<AiCompanion problem-slug="smallest-range-covering-elements-from-k-lists" pattern-hint="k-way merge" />

## Related problems

- [Merge k Sorted Lists](/problems/k-way-merge-k-sorted-lists) — same heap-sweep
- [Ugly Number II](/problems/ugly-number-ii) — heap merges 3 streams
- [Median of Two Sorted Arrays](/problems/median-of-two-sorted-arrays) — 2-list balance BS

<FeedbackWidget problem-slug="smallest-range-covering-elements-from-k-lists" />
