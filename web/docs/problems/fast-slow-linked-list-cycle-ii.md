# Fast/Slow Pointers — Linked List Cycle II

*[↗ LeetCode: Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/fast-slow)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft, Apple, Bloomberg" /&gt;

Given the head of a linked list, return the node where the cycle begins, or `null` if no cycle.

**Example 1** — `3→2→0→-4→(back to 2)` → returns node `2`
**Example 2** — `1→2→(back to 1)` → returns node `1`
**Example 3** — `1` (no next) → returns `null`

**Constraints** — `0 ≤ n ≤ 10⁴`; O(1) extra space required for the follow-up.


&lt;Hints
  hint1="Two pointers moving at different speeds detect cycles without extra memory."
  hint2="Slow steps 1, Fast steps 2. If they ever meet, there’s a cycle. If Fast hits null, no cycle."
  hint3="For cycle entry (Floyd’s Tortoise): after meeting, reset one pointer to head; walk both at speed 1; meet at entry."
/&gt;
---

&lt;MarkSolved problem-slug="fast-slow-linked-list-cycle-ii" /&gt; &lt;Bookmark problem-slug="fast-slow-linked-list-cycle-ii" /&gt;

&lt;InterviewTimer problem-slug="fast-slow-linked-list-cycle-ii" /&gt;



## Approach 1 — Brute force (hash-set of visited nodes)

**Intuition.** Walk the list; store each node reference in a set; the first re-encountered node is the cycle entry.



```java
ListNode detectCycleHash(ListNode head) {
    Set<ListNode> seen = new HashSet<>();
    for (ListNode cur = head; cur != null; cur = cur.next) {
        if (!seen.add(cur)) return cur;
    }
    return null;
}
```



<CodeTrace
  title="Hash-set — list 3→2→0→-4 with -4.next=2"
  :values="[3,2,0,-4]"
  :windowKeys="['cur']"
  :cellWidth="42"
  :steps='[
    { pointers: { cur: 0 }, vars: { seen: "{3}" }, note: "add 3" },
    { pointers: { cur: 1 }, vars: { seen: "{3,2}" }, note: "add 2" },
    { pointers: { cur: 2 }, vars: { seen: "{3,2,0}" }, note: "add 0" },
    { pointers: { cur: 3 }, vars: { seen: "{3,2,0,-4}" }, note: "add -4" },
    { pointers: { cur: 1 }, vars: { seen: "…" }, note: "-4.next=2. 2 already in set → return node 2", added: [1] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)** for the set.

Correct but the O(n) space is what most interviewers push back on.

---

## Approach 2 — Floyd's tortoise and hare (O(1) space)

**Insight from hash-set.** Two pointers, one at 1x speed (slow) and one at 2x speed (fast), must collide inside the cycle if one exists (fast closes the gap by 1 per step). After a meeting, reset one pointer to head and advance both at 1x — they meet again exactly at the cycle entry.

**Why the reset trick works.** Let `A` = head → entry distance, `C` = cycle length, `B` = entry → meeting-point distance. When slow and fast meet: slow walked `A+B`, fast walked `2(A+B)`. The extra `A+B` fast walked is whole laps → `A+B = kC` → `A = kC - B`. So from the meeting point, walking `A` steps lands at the entry — exactly what the reset does.



```java
ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {                 // cycle proven
            ListNode p = head;
            while (p != slow) { p = p.next; slow = slow.next; }
            return p;                       // entry
        }
    }
    return null;
}
```



<CodeTrace
  title="Floyd — 3→2→0→-4 with -4.next=2"
  :values="[3,2,0,-4]"
  :windowKeys="['slow','fast']"
  :cellWidth="42"
  :steps='[
    { pointers: { slow: 0, fast: 0 }, vars: { phase: "detect" }, note: "start both at head" },
    { pointers: { slow: 1, fast: 2 }, vars: { phase: "detect" }, note: "slow +1, fast +2" },
    { pointers: { slow: 2, fast: 1 }, vars: { phase: "detect" }, note: "fast wraps -4→2" },
    { pointers: { slow: 3, fast: 3 }, vars: { phase: "detect" }, note: "meeting at -4. cycle proven", added: [3] },
    { pointers: { slow: 3, fast: 0 }, vars: { phase: "reset", p: 0 }, note: "reset one pointer to head; step both by 1" },
    { pointers: { slow: 1, fast: 1 }, vars: { phase: "entry", p: 1 }, note: "meet at 2 = cycle entry", added: [1] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. Optimal.

**Trap.** `fast != null && fast.next != null` — checking only `fast != null` NPEs on even-length lists like `1→2`.

---

## Try it yourself

<JavaRunner problem-slug="fast-slow-linked-list-cycle-ii" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Hash set of visited nodes | O(n) | O(n) |
| Floyd tortoise & hare | **O(n)** | **O(1)** |

## When to use which

- **Cold interview** → state hash-set, then Floyd for the O(1) space follow-up.
- **Interviewer probes "why reset works"** → the `A = kC − B` derivation.

&lt;AiCompanion problem-slug="fast-slow-linked-list-cycle-ii" pattern-hint="fast/slow pointers" /&gt;

## Related problems (same ladder applies)

- [Linked List Cycle (I)](https://leetcode.com/problems/linked-list-cycle/) — return true/false, no entry needed
- [Happy Number](https://leetcode.com/problems/happy-number/) — Floyd on the digit-square-sum sequence
- [Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) — Floyd on `next = nums[i]`
- [Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) — Floyd to find middle, reverse second half, compare

&lt;FeedbackWidget problem-slug="fast-slow-linked-list-cycle-ii" /&gt;

&lt;RelatedProblems problems="palindrome-linked-list::Palindrome Linked List|linked-list-cycle::Linked List Cycle|find-the-duplicate-number::Find The Duplicate Number" /&gt;
