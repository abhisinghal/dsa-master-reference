# K-way Merge — Merge Two Sorted Lists

*[↗ LeetCode: Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/k-way-merge)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Apple, Bloomberg" />

Given the heads of two sorted linked lists, merge them into one sorted list.

**Example 1** — `l1 = 1→2→4, l2 = 1→3→4` → `1→1→2→3→4→4`
**Example 2** — `l1 = [], l2 = []` → `[]`
**Example 3** — `l1 = [], l2 = 0` → `0`

**Constraints** — `0 ≤ len ≤ 50`; values in `[-100, 100]`; both sorted ascending.


<Hints
  hint1="You have k sorted sequences. Which element is globally next?"
  hint2="Min-heap of size k, one head per list. Pop smallest, emit, push its successor from the same list."
  hint3="For ’smallest range covering k lists’, track max-in-heap; window is [minInHeap, maxSeen]."
/>
---

## Approach 1 — Materialize and re-sort

O((m+n) log (m+n)). Baseline; wastes existing sortedness.

## Approach 2 — Iterative two-pointer merge with dummy

**Intuition.** Walk both lists in tandem; append the smaller current node. Use a **dummy head** to avoid special-casing the first append.

**Trap** — always maintain `tail.next = null` semantics; if you re-link into an existing tail, the appended sublist keeps its rest.

```java
ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(0), tail = dummy;
    while (l1 != null && l2 != null) {
        if (l1.val <= l2.val) { tail.next = l1; l1 = l1.next; }
        else { tail.next = l2; l2 = l2.next; }
        tail = tail.next;
    }
    tail.next = (l1 != null) ? l1 : l2;
    return dummy.next;
}
```

<CodeTrace
  title="Merge — l1=1→2→4, l2=1→3→4"
  :values="['1','2','4','|','1','3','4']"
  :windowKeys="['p1','p2']"
  :cellWidth="30"
  :steps='[
    { pointers: { p1: 0, p2: 4 }, vars: { out: "dummy" }, note: "1 == 1 → take l1" },
    { pointers: { p1: 1, p2: 4 }, vars: { out: "→1" }, note: "next tail" },
    { pointers: { p1: 1, p2: 5 }, vars: { out: "→1→1" }, note: "l1=2 > l2=1 → take l2 (1)" },
    { pointers: { p1: 2, p2: 6 }, vars: { out: "→1→1→2→3" }, note: "walk through" },
    { pointers: {}, vars: { out: "1→1→2→3→4→4" }, note: "attach tail; done" }
  ]'
/>

**Complexity** — Time **O(m + n)**; Space **O(1)** (nodes reused).

---

## Approach 3 — Recursive

**Insight from iterative.** The recursive form is cleaner: pick smaller head; recursively merge the rest.

```java
ListNode mergeTwoListsRec(ListNode l1, ListNode l2) {
    if (l1 == null) return l2;
    if (l2 == null) return l1;
    if (l1.val <= l2.val) { l1.next = mergeTwoListsRec(l1.next, l2); return l1; }
    else { l2.next = mergeTwoListsRec(l1, l2.next); return l2; }
}
```

**Complexity** — Time **O(m + n)**; Space **O(m + n)** stack — watch stack overflow on long lists.

---

## Try it yourself

<JavaRunner problem-slug="merge-two-sorted-lists" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Materialize + sort | O((m+n) log(m+n)) | O(m+n) | baseline |
| Iterative + dummy | **O(m + n)** | **O(1)** | canonical |
| Recursive | O(m + n) | O(m + n) stack | elegant but risky |

## When to use which

- **Standard answer** → iterative + dummy head.
- **"No dummy allowed"** → track head via `if (dummy.next == null) dummy.next = ...` — messier.
- **Sorted arrays instead of lists** → same skeleton (see [Merge Sorted Array](/problems/merge-sorted-array)).
- **k lists** → use min-heap (see [Merge k Sorted Lists](/problems/k-way-merge-k-sorted-lists)).

## Related problems

- [Merge k Sorted Lists](/problems/k-way-merge-k-sorted-lists) — k lists, min-heap
- [Merge Sorted Array](/problems/merge-sorted-array) — sorted arrays, fill from back
- [Sort List](/problems/sort-list) — mergesort using merge as primitive