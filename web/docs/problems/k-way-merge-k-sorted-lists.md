# K-way Merge — Merge k Sorted Lists

*[↗ LeetCode: Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/k-way-merge)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Adobe, Uber" />

Merge `k` sorted linked lists into one sorted list.

**Example 1** — `[[1,4,5],[1,3,4],[2,6]]` → `[1,1,2,3,4,4,5,6]`
**Example 2** — `[[]]` → `[]`
**Example 3** — `[[1],[2],[3],[4],[5]]` → `[1,2,3,4,5]`

**Constraints** — `k ≤ 10⁴`; total nodes `N ≤ 10⁴`; values `-10⁴..10⁴`. Naive collect-then-sort is O(N log N) — throws away that inputs are pre-sorted. Sequential merging is O(kN) — at k=N=10⁴ that's 10⁸ ops. Heap merge is O(N log k) ≈ 1.3·10⁵ — 750× faster.


<Hints
  hint1="You have k sorted sequences. Which element is globally next?"
  hint2="Min-heap of size k, one head per list. Pop smallest, emit, push its successor from the same list."
  hint3="For 'smallest range covering k lists', track max-in-heap; window is [minInHeap, maxSeen]."
/>
---

<MarkSolved problem-slug="k-way-merge-k-sorted-lists" /> <Bookmark problem-slug="k-way-merge-k-sorted-lists" />

<InterviewTimer problem-slug="k-way-merge-k-sorted-lists" />



## Approach 1 — Collect + sort

**Intuition.** Walk every list; collect values; sort; rebuild.



```java
ListNode mergeKListsSort(ListNode[] lists) {
    List<Integer> all = new ArrayList<>();
    for (ListNode l : lists) for (ListNode c = l; c != null; c = c.next) all.add(c.val);
    Collections.sort(all);
    ListNode dummy = new ListNode(0), tail = dummy;
    for (int v : all) { tail.next = new ListNode(v); tail = tail.next; }
    return dummy.next;
}
```



**Complexity** — Time **O(N log N)**; Space **O(N)**. Ignores that inputs are already sorted.

---

## Approach 2 — Merge pairs sequentially

**Intuition.** Repeatedly merge `answer` with next list (two-list merge).



```java
ListNode mergeKListsSeq(ListNode[] lists) {
    ListNode answer = null;
    for (ListNode l : lists) answer = mergeTwo(answer, l);
    return answer;
}
```



**Complexity** — Time **O(k · N)** (each merge sees up to N nodes); Space **O(1)**. Bad when k is large.

---

## Approach 3 — Divide and conquer (pair-wise merges)

**Insight from sequential.** Merging pairs symmetrically halves the work per round. `log k` rounds, each round processes all N nodes → `O(N log k)`.



```java
ListNode mergeKLists(ListNode[] lists) {
    if (lists.length == 0) return null;
    while (lists.length > 1) {
        List<ListNode> merged = new ArrayList<>();
        for (int i = 0; i < lists.length; i += 2) {
            ListNode a = lists[i];
            ListNode b = i + 1 < lists.length ? lists[i + 1] : null;
            merged.add(mergeTwo(a, b));
        }
        lists = merged.toArray(new ListNode[0]);
    }
    return lists[0];
}
```



**Complexity** — Time **O(N log k)**; Space **O(log k)** recursion.

---

## Approach 4 — Min-heap of live heads

**Insight from D&C.** Instead of merging offline, keep a min-heap of `k` live heads. Pop the smallest, splice onto the answer, push its `.next`. Each of the `N` nodes is popped once → `O(N log k)`.

**Trap.** Re-feed the heap — after popping a node from list A, immediately offer `A.next` (or the list is orphaned).



```java
ListNode mergeKListsHeap(ListNode[] lists) {
    PriorityQueue<ListNode> heap = new PriorityQueue<>((a, b) -> a.val - b.val);
    for (ListNode l : lists) if (l != null) heap.offer(l);
    ListNode dummy = new ListNode(0), tail = dummy;
    while (!heap.isEmpty()) {
        ListNode n = heap.poll();
        tail.next = n; tail = n;
        if (n.next != null) heap.offer(n.next);
    }
    return dummy.next;
}
```



<CodeTrace
  title="Min-heap merge — [[1,4,5],[1,3,4],[2,6]]"
  :values="[1,4,5]"
  :windowKeys="['step']"
  :cellWidth="42"
  :steps='[
    { pointers: { step: 0 }, vars: { heap: "[1A, 1B, 2C]", output: "" }, note: "seed with heads" },
    { pointers: { step: 1 }, vars: { heap: "[1B, 2C, 4A]", output: "1" }, note: "pop 1A, push 4A" },
    { pointers: { step: 2 }, vars: { heap: "[2C, 3B, 4A]", output: "1,1" }, note: "pop 1B, push 3B" },
    { pointers: { step: 3 }, vars: { heap: "[3B, 4A, 6C]", output: "1,1,2" }, note: "pop 2C, push 6C" },
    { pointers: { step: 4 }, vars: { heap: "[]", output: "1,1,2,3,4,4,5,6" }, note: "drain → final" }
  ]'
/>

**Complexity** — Time **O(N log k)**; Space **O(k)**. Same time as D&C, but streaming-friendly and easier to reason about.

---

## Try it yourself

<JavaRunner problem-slug="k-way-merge-k-sorted-lists" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Collect + sort | O(N log N) | O(N) |
| Sequential pairs | O(k · N) | O(1) |
| D&C pairs | **O(N log k)** | O(log k) |
| Min-heap | **O(N log k)** | O(k) |

## When to use which

- **Small k or lists in memory** → D&C.
- **Streaming or k unknown at start** → min-heap.
- **k = 2 special case** → dummy-head splice (see Merge Two Sorted Lists).

<AiCompanion problem-slug="k-way-merge-k-sorted-lists" pattern-hint="k-way merge" />

## Related problems (same ladder applies)

- [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) — k=2 special case
- [Smallest Range Covering Elements from K Lists](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/) — heap of one from each list
- [Ugly Number II](https://leetcode.com/problems/ugly-number-ii/) — 3-way merge with dedup
- [Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) — heap of row heads

<FeedbackWidget problem-slug="k-way-merge-k-sorted-lists" />

<RelatedProblems problems="top-k-frequent-elements::Top K Frequent Elements|ugly-number-ii::Ugly Number II|smallest-range-covering-elements-from-k-lists::Smallest Range Covering Elements From K Lists" />
