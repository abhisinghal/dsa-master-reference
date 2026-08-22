# K-way Merge — Merge Two Sorted Lists

*[↗ LeetCode: Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/k-way-merge)

Merge two sorted lists into one sorted list.

**Example** — `l1=[1,2,4], l2=[1,3,4]` → `[1,1,2,3,4,4]`

---

## Approach 1 — Dummy-head splice (iterative)

```java
ListNode mergeTwoLists(ListNode a, ListNode b) {
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
  title="Two-pointer splice — [1,2,4] + [1,3,4]"
  :values="[1,2,4]"
  :windowKeys="['step']"
  :cellWidth="42"
  :steps='[
    { pointers: { step: 0 }, vars: { a: 1, b: 1, out: "" }, note: "tie → take a" },
    { pointers: { step: 1 }, vars: { a: 2, b: 1, out: "1" }, note: "1 lt 2 → take b" },
    { pointers: { step: 2 }, vars: { a: 2, b: 3, out: "1,1" }, note: "take a" },
    { pointers: { step: 3 }, vars: { a: 4, b: 3, out: "1,1,2" }, note: "take b" },
    { pointers: { step: 4 }, vars: { a: 4, b: 4, out: "1,1,2,3,4,4" }, note: "drain → final" }
  ]'
/>

**Complexity** — Time **O(n + m)**; Space **O(1)** (in-place link splice).

## Approach 2 — Recursive

```java
ListNode mergeRec(ListNode a, ListNode b) {
    if (a == null) return b;
    if (b == null) return a;
    if (a.val <= b.val) { a.next = mergeRec(a.next, b); return a; }
    else                { b.next = mergeRec(a, b.next); return b; }
}
```

**Complexity** — Time **O(n + m)**; Space **O(n + m)** stack.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Iterative splice | O(n + m) | O(1) |
| Recursive | O(n + m) | O(n + m) stack |

## Related problems

- [Merge k Sorted Lists](/problems/k-way-merge-k-sorted-lists) — same, generalized to k
- [Sort List](https://leetcode.com/problems/sort-list/) — merge sort on linked list uses this as merge step
- [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) — array version, merge from the back
