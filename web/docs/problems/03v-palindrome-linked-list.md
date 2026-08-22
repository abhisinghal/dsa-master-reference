# Fast/Slow — Palindrome Linked List

*[↗ LeetCode: Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/fast-slow)

Return `true` if the linked list is a palindrome. O(1) space follow-up.

**Example** — `[1,2,2,1]` → `true`; `[1,2]` → `false`

---

## Approach 1 — Copy to array, two pointers



```java
boolean isPalindromeArray(ListNode h) {
    List<Integer> a = new ArrayList<>();
    for (ListNode c = h; c != null; c = c.next) a.add(c.val);
    int lo = 0, hi = a.size() - 1;
    while (lo < hi) if (!a.get(lo++).equals(a.get(hi--))) return false;
    return true;
}
```



**Complexity** — Time **O(n)**; Space **O(n)** for the array.

## Approach 2 — Fast/slow + reverse second half (O(1) space)

**Insight.** Find middle via Floyd; reverse the second half; walk both halves in lockstep comparing values.



```java
boolean isPalindrome(ListNode h) {
    ListNode slow = h, fast = h;
    while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
    ListNode right = reverse(slow);
    ListNode left = h;
    while (right != null) {
        if (left.val != right.val) return false;
        left = left.next; right = right.next;
    }
    return true;
}
ListNode reverse(ListNode h) { ListNode p = null; while (h != null) { ListNode n = h.next; h.next = p; p = h; h = n; } return p; }
```



<CodeTrace
  title="Fast/slow + reverse — [1,2,2,1]"
  :values="[1,2,2,1]"
  :windowKeys="['slow']"
  :cellWidth="42"
  :steps='[
    { pointers: { slow: 0, fast: 0 }, vars: { phase: "find middle" }, note: "start" },
    { pointers: { slow: 2, fast: -1 }, vars: { phase: "middle" }, note: "slow at middle (idx 2)", added: [2] },
    { pointers: { slow: 2, fast: 3 }, vars: { phase: "reverse right", reversed: "[1,2]" }, note: "reverse [2,1] into [1,2]" },
    { pointers: { slow: 0, fast: 3 }, vars: { compare: "1=1 ✓" }, note: "match", added: [0,3] },
    { pointers: { slow: 1, fast: 2 }, vars: { compare: "2=2 ✓" }, note: "match → palindrome true", added: [1,2] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Copy to array | O(n) | O(n) |
| Fast/slow + reverse | **O(n)** | **O(1)** |

## Related problems

- [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) — the reversal step used inside
- [Reorder List](https://leetcode.com/problems/reorder-list/) — find middle, reverse, merge
- [Middle of the Linked List](/problems/middle-of-the-linked-list) — the middle-finding step
