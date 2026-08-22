# Fast/Slow — Middle of the Linked List

*[↗ LeetCode: Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/fast-slow)

Return the middle node. If two middles (even length), return the second one.

**Example 1** — `[1,2,3,4,5]` → node `3`
**Example 2** — `[1,2,3,4,5,6]` → node `4`

---

## Approach 1 — Two-pass count

```java
ListNode middleNodeCount(ListNode h) {
    int n = 0;
    for (ListNode c = h; c != null; c = c.next) n++;
    ListNode cur = h;
    for (int i = 0; i < n / 2; i++) cur = cur.next;
    return cur;
}
```

**Complexity** — Time **O(n)**; Space **O(1)**. Works but takes two passes.

## Approach 2 — Fast/slow one-pass

```java
ListNode middleNode(ListNode h) {
    ListNode slow = h, fast = h;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow;                                          // second middle for even
}
```

<CodeTrace
  title="Fast/slow — [1,2,3,4,5,6]"
  :values="[1,2,3,4,5,6]"
  :windowKeys="['slow','fast']"
  :cellWidth="42"
  :steps='[
    { pointers: { slow: 0, fast: 0 }, vars: { }, note: "start at head" },
    { pointers: { slow: 1, fast: 2 }, vars: { }, note: "slow +1, fast +2" },
    { pointers: { slow: 2, fast: 4 }, vars: { }, note: "slow +1, fast +2" },
    { pointers: { slow: 3, fast: -1 }, vars: { }, note: "fast reaches null → slow is at 4 (second middle)", added: [3] }
  ]'
/>

**Complexity** — Time **O(n)** single pass; Space **O(1)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Two-pass count | O(n) | O(1) |
| Fast/slow | **O(n)** single pass | **O(1)** |

## Related problems

- [Linked List Cycle](/problems/linked-list-cycle) — Floyd
- [Palindrome Linked List](/problems/palindrome-linked-list) — find middle, reverse second half, compare
- [Reorder List](https://leetcode.com/problems/reorder-list/) — find middle, reverse, merge
