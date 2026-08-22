# Divide & Conquer — Sort List

*[↗ LeetCode: Sort List](https://leetcode.com/problems/sort-list/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/divide-conquer)

Sort a linked list in O(n log n) time and O(1) *auxiliary* space.

**Example** — `4→2→1→3` → `1→2→3→4`

---

## Approach 1 — Copy to array, sort, rebuild

O(n log n) time; O(n) space. Doesn't meet the O(1) aux bar.

## Approach 2 — Recursive merge sort

**Insight.** Find middle via fast/slow; split; recurse; merge.

```java
ListNode sortList(ListNode h) {
    if (h == null || h.next == null) return h;
    ListNode slow = h, fast = h.next;                        // fast = h.next so slow ends at LEFT middle
    while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
    ListNode right = slow.next; slow.next = null;
    return merge(sortList(h), sortList(right));
}
ListNode merge(ListNode a, ListNode b) {
    ListNode dummy = new ListNode(0), tail = dummy;
    while (a != null && b != null) {
        if (a.val <= b.val) { tail.next = a; a = a.next; }
        else                { tail.next = b; b = b.next; }
        tail = tail.next;
    }
    tail.next = a != null ? a : b;
    return dummy.next;
}
```

<CodeTrace
  title="Merge sort — 4→2→1→3"
  :values="[4,2,1,3]"
  :windowKeys="['step']"
  :cellWidth="42"
  :steps='[
    { pointers: { step: 0 }, vars: { list: "4→2→1→3" }, note: "split at middle → [4,2] and [1,3]" },
    { pointers: { step: 1 }, vars: { left: "[2,4]", right: "[1,3]" }, note: "recurse and merge halves" },
    { pointers: { step: 2 }, vars: { merged: "1→2→3→4" }, note: "merge two sorted halves", added: [2,1,3,0] }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(log n)** recursion stack.

## Approach 3 — Iterative bottom-up merge sort (O(1) aux)

Combine pairs of sublists of size 1, then 2, then 4… until one sublist remains.

**Complexity** — Time **O(n log n)**; Space **O(1)** *aux* (excluding output pointers).

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Array + sort + rebuild | O(n log n) | O(n) |
| Recursive merge sort | O(n log n) | O(log n) stack |
| Iterative bottom-up | **O(n log n)** | **O(1)** aux |

## Related problems

- [Merge Two Sorted Lists](/problems/merge-two-sorted-lists) — merge step used inside
- [Merge k Sorted Lists](/problems/k-way-merge-k-sorted-lists) — generalized
- [Insertion Sort List](https://leetcode.com/problems/insertion-sort-list/) — O(n²) sibling
