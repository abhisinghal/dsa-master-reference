# Fast &amp; Slow — Palindrome Linked List

*[↗ LeetCode: Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/fast-slow)

<CompanyTags companies="Meta, Amazon, Microsoft, Adobe" />

Given the head of a singly linked list, return `true` iff it's a palindrome.

**Example 1** — `1 → 2 → 2 → 1` → `true`
**Example 2** — `1 → 2` → `false`
**Example 3** — `1` → `true`

**Constraints** — `1 ≤ n ≤ 10⁵`. Follow-up: O(n) time, O(1) space.


<Hints
  hint1="Two pointers moving at different speeds detect cycles without extra memory."
  hint2="Slow steps 1, Fast steps 2. If they ever meet, there’s a cycle. If Fast hits null, no cycle."
  hint3="For cycle entry (Floyd’s Tortoise): after meeting, reset one pointer to head; walk both at speed 1; meet at entry."
/>
---

<MarkSolved problem-slug="palindrome-linked-list" />


## Approach 1 — Copy to array, two-pointer

**Intuition.** Materialize into `int[]`, then classic two-pointer palindrome check.

```java
boolean isPalindromeArr(ListNode head) {
    List<Integer> a = new ArrayList<>();
    for (ListNode c = head; c != null; c = c.next) a.add(c.val);
    int l = 0, r = a.size() - 1;
    while (l < r) if (!a.get(l++).equals(a.get(r--))) return false;
    return true;
}
```

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Approach 2 — Reverse second half in place (O(1) space)

**Insight from array.** We can compare in place by splitting the list at the middle (fast/slow), reversing the second half, then walking two pointers from head and reversed-head.

**Trap** — restore the list at the end for good citizenship in library code (interviewers care). The naive version leaves the list mutated.

```java
boolean isPalindrome(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
    // slow is at second-half start (or exact middle for odd length)
    ListNode second = reverse(slow);
    ListNode secondHead = second;
    ListNode p1 = head, p2 = second;
    boolean ok = true;
    while (p2 != null) {
        if (p1.val != p2.val) { ok = false; break; }
        p1 = p1.next; p2 = p2.next;
    }
    // restore
    reverse(secondHead);
    return ok;
}
ListNode reverse(ListNode h) {
    ListNode prev = null;
    while (h != null) { ListNode n = h.next; h.next = prev; prev = h; h = n; }
    return prev;
}
```

<CodeTrace
  title="Reverse-half — 1→2→2→1"
  :values="['1','2','2','1']"
  :windowKeys="['slow','fast']"
  :cellWidth="38"
  :steps='[
    { pointers: { slow: 0, fast: 0 }, vars: {}, note: "both at head" },
    { pointers: { slow: 2, fast: 4 }, vars: { note: "fast is null" }, note: "slow at index 2 → mid; second half [2,1]" },
    { pointers: {}, vars: { secondReversed: "1→2" }, note: "reverse second half → 1 → 2" },
    { pointers: {}, vars: { compare: "1==1 ✓; 2==2 ✓" }, note: "walk head and reversed second — palindrome" }
  ]'
/>

**Complexity** — Time **O(n)** (3 passes); Space **O(1)**.

---

## Approach 3 — Recursive comparison (O(n) stack)

**Insight.** Recurse to end; compare with a "front pointer" as recursion unwinds.

```java
ListNode front;
boolean isPalindromeRec(ListNode head) {
    front = head;
    return check(head);
}
boolean check(ListNode node) {
    if (node == null) return true;
    if (!check(node.next)) return false;
    if (node.val != front.val) return false;
    front = front.next;
    return true;
}
```

**Complexity** — Time **O(n)**; Space **O(n)** call stack. Cleaner code but same asymptotics as Approach 1.

---

## Try it yourself

<JavaRunner problem-slug="palindrome-linked-list" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Copy to array | O(n) | O(n) | baseline |
| Reverse second half in place | **O(n)** | **O(1)** | canonical follow-up |
| Recursive front pointer | O(n) | O(n) stack | elegant but same space |

## When to use which

- **Standard interview** → reverse-half in-place.
- **Interviewer allows O(n) extra** → copy-to-array is safer and clearer.
- **"Restore list at end"** → always mention; some interviewers require it.
- **Doubly linked list** → true two-pointer O(1) space and no reversal.

<AiCompanion problem-slug="palindrome-linked-list" pattern-hint="fast/slow pointers" />

## Related problems

- [Middle of the Linked List](/problems/middle-of-the-linked-list) — the split primitive
- [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) — the reversal primitive
- [Reorder List](https://leetcode.com/problems/reorder-list/) — same split + reverse + interleave

<FeedbackWidget problem-slug="palindrome-linked-list" />
