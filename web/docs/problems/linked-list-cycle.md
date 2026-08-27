# Fast &amp; Slow — Linked List Cycle

*[↗ LeetCode: Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/fast-slow)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Apple, Bloomberg" />

Given the head of a linked list, return `true` iff the list contains a cycle.

**Example 1** — `head = [3,2,0,-4]`, tail connects to index `1` → `true`
**Example 2** — `head = [1,2]`, tail connects to index `0` → `true`
**Example 3** — `head = [1]`, tail = null → `false`

**Constraints** — `0 ≤ n ≤ 10⁴`. Brute is O(n) time + O(n) memory with a visited HashSet — GC pressure adds ~10⁶ ns overhead per node. Floyd's tortoise & hare is O(n) time + O(1) space — half a dozen pointer chases per node.
<Hints
  hint1="Two pointers moving at different speeds detect cycles without extra memory."
  hint2="Slow steps 1, Fast steps 2. If they ever meet, there’s a cycle. If Fast hits null, no cycle."
  hint3="For cycle entry (Floyd’s Tortoise): after meeting, reset one pointer to head; walk both at speed 1; meet at entry."
/>
---

<MarkSolved problem-slug="linked-list-cycle" /> <Bookmark problem-slug="linked-list-cycle" />

<InterviewTimer problem-slug="linked-list-cycle" />



## Approach 1 — Hash set of visited nodes

**Intuition.** Walk the list; if a node reference reappears in the set, cycle found.



```java
boolean hasCycleHash(ListNode head) {
    Set<ListNode> seen = new HashSet<>();
    while (head != null) {
        if (!seen.add(head)) return true;
        head = head.next;
    }
    return false;
}
```



**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Approach 2 — Floyd's tortoise and hare (canonical)

**Insight from hash.** We don't need to store visited nodes; two pointers at different speeds will meet inside a cycle. `slow` advances 1; `fast` advances 2. If they ever meet, cycle exists. If `fast` hits null, no cycle.

**Why they meet.** Once both pointers are in the cycle, `fast` gains 1 step per iteration on `slow`. In a cycle of length `L`, `fast` catches up in ≤ L steps.



```java
boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}
```



<CodeTrace
  title="Floyd — 3→2→0→-4→(back to 2)"
  :values="['3','2','0','-4']"
  :windowKeys="['slow','fast']"
  :cellWidth="38"
  :steps='[
    { pointers: { slow: 0, fast: 0 }, vars: { step: 0 }, note: "both at head" },
    { pointers: { slow: 1, fast: 2 }, vars: { step: 1 }, note: "slow=2, fast=0" },
    { pointers: { slow: 2, fast: 1 }, vars: { step: 2 }, note: "fast wrapped: -4→2" },
    { pointers: { slow: 3, fast: 3 }, vars: { step: 3, met: true }, note: "both at -4 → cycle detected" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="linked-list-cycle" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Hash set | O(n) | O(n) | acceptable |
| Floyd's tortoise/hare | **O(n)** | **O(1)** | expected optimum |

## When to use which

- **Ship this** → Floyd's algorithm.
- **"Return the cycle entry node"** → Floyd + reset one pointer to head (see [Linked List Cycle II](/problems/fast-slow-linked-list-cycle-ii)).
- **"Return cycle length"** → after `slow == fast`, walk `fast` around the loop until it meets `slow` again — length = steps taken.
- **Modifying list allowed?** → some variants mark visited nodes; not standard.

<AiCompanion problem-slug="linked-list-cycle" pattern-hint="fast/slow pointers" />

## Related problems

- [Linked List Cycle II](/problems/fast-slow-linked-list-cycle-ii) — return entry node
- [Happy Number](/problems/happy-number) — cycle detection on integer sequence
- [Find the Duplicate Number](/problems/find-the-duplicate-number) — cycle detection on array as implicit list

<FeedbackWidget problem-slug="linked-list-cycle" />

<RelatedProblems problems="fast-slow-linked-list-cycle-ii::Fast Slow Linked List Cycle II|find-the-duplicate-number::Find The Duplicate Number|happy-number::Happy Number" />
