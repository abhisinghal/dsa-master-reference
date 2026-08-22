# Fast/Slow — Linked List Cycle

*[↗ LeetCode: Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/fast-slow)

Return `true` if the linked list has a cycle.

**Example** — `head=[3,2,0,-4]` with `-4.next=2` → `true`.

---

## Approach 1 — Hash-set of visited nodes

```java
boolean hasCycleHash(ListNode h) {
    Set<ListNode> seen = new HashSet<>();
    for (ListNode c = h; c != null; c = c.next)
        if (!seen.add(c)) return true;
    return false;
}
```

**Complexity** — Time **O(n)**; Space **O(n)**.

## Approach 2 — Floyd tortoise & hare (O(1) space)

```java
boolean hasCycle(ListNode h) {
    ListNode slow = h, fast = h;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}
```

<CodeTrace
  title="Floyd — 3→2→0→-4 with -4.next=2"
  :values="[3,2,0,-4]"
  :windowKeys="['slow','fast']"
  :cellWidth="42"
  :steps='[
    { pointers: { slow: 0, fast: 0 }, vars: { }, note: "both at head" },
    { pointers: { slow: 1, fast: 2 }, vars: { }, note: "slow +1, fast +2" },
    { pointers: { slow: 2, fast: 1 }, vars: { }, note: "fast wraps -4→2" },
    { pointers: { slow: 3, fast: 3 }, vars: { }, note: "meeting → cycle proven", added: [3] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. Optimal.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Hash set | O(n) | O(n) |
| Floyd | **O(n)** | **O(1)** |

## Related problems

- [Linked List Cycle II](/problems/fast-slow-linked-list-cycle-ii) — return the cycle *entry* node
- [Happy Number](/problems/happy-number) — Floyd on the digit-square-sum sequence
- [Find the Duplicate Number](/problems/find-the-duplicate-number) — Floyd on `next = nums[i]`
