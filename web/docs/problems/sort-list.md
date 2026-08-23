# Divide & Conquer — Sort List

*[↗ LeetCode: Sort List](https://leetcode.com/problems/sort-list/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/divide-conquer)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg" /&gt;

Sort a linked list in **O(n log n)** time, O(1) extra space (constant beyond recursion stack).

**Example 1** — `4→2→1→3` → `1→2→3→4`
**Example 2** — `-1→5→3→4→0` → `-1→0→3→4→5`

**Constraints** — `0 ≤ n ≤ 5·10⁴`.


&lt;Hints
  hint1="Can I split the input in half, solve each half, then combine? Combine step is the trick."
  hint2="Merge sort framework: recurse left, recurse right, then merge with the counting/comparison logic on the boundary."
  hint3="For count-of-X-across-boundary, two-pointer walk during the merge step."
/&gt;
---

## Approach 1 — Copy to array, sort, rebuild

O(n log n) time, O(n) space. Rejected by spec.

## Approach 2 — Merge sort with fast/slow split (canonical)

**Insight.** Divide: find middle with fast/slow. Recurse left and right. Merge two sorted lists.



```java
ListNode sortList(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode slow = head, fast = head, prev = null;
    while (fast != null && fast.next != null) {
        prev = slow;
        slow = slow.next;
        fast = fast.next.next;
    }
    prev.next = null;
    return merge(sortList(head), sortList(slow));
}
ListNode merge(ListNode a, ListNode b) {
    ListNode dummy = new ListNode(0), tail = dummy;
    while (a != null && b != null) {
        if (a.val <= b.val) { tail.next = a; a = a.next; }
        else { tail.next = b; b = b.next; }
        tail = tail.next;
    }
    tail.next = a != null ? a : b;
    return dummy.next;
}
```



<CodeTrace
  title="Merge sort — 4→2→1→3"
  :values="['4','2','1','3']"
  :windowKeys="['step']"
  :cellWidth="34"
  :steps='[
    { pointers: { step: 1 }, vars: { split: "[4,2] | [1,3]" }, note: "" },
    { pointers: { step: 2 }, vars: { sorted: "[2,4] and [1,3]" }, note: "" },
    { pointers: { step: 3 }, vars: { merged: "[1,2,3,4]" }, note: "" }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(log n)** recursion stack.

---

## Approach 3 — Iterative bottom-up merge sort (true O(1) space)

**Insight from top-down.** Iterate over merge widths 1, 2, 4, … splitting the list at fixed offsets. No recursion; O(1) extra beyond output.

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="sort-list" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Materialize + sort | O(n log n) | O(n) | rejected |
| Recursive merge sort | O(n log n) | O(log n) | canonical |
| Bottom-up merge sort | **O(n log n)** | **O(1)** | polish |

## When to use which

- **Standard interview** → recursive top-down.
- **True O(1) space required** → iterative bottom-up.
- **Doubly linked list** → merge sort still wins over quicksort due to O(1) split.

&lt;AiCompanion problem-slug="sort-list" pattern-hint="divide & conquer" /&gt;

## Related problems

- [Merge Two Sorted Lists](/problems/merge-two-sorted-lists) — the merge primitive
- [Merge k Sorted Lists](/problems/k-way-merge-k-sorted-lists) — extension
- [Middle of the Linked List](/problems/middle-of-the-linked-list) — split primitive