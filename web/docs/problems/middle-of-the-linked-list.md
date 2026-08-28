# Fast &amp; Slow — Middle of the Linked List

*[↗ LeetCode: Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/fast-slow)

<CompanyTags companies="Meta, Amazon, Microsoft, Google" />

Given the head of a singly linked list, return the middle node. If there are two middles, return the second.

**Example 1** — `1 → 2 → 3 → 4 → 5` → node with value `3`
**Example 2** — `1 → 2 → 3 → 4 → 5 → 6` → node with value `4` (second middle)
**Example 3** — `1` → `1`

**Constraints** — `1 ≤ n ≤ 100`. Brute two-pass (count then walk) is O(n) time but two full traversals — hot service pays 2x cache misses. Fast/slow single pass is O(n) time, ~10⁶ pointer chases with one traversal.
<Hints
  hint1="Two pointers moving at different speeds detect cycles without extra memory."
  hint2="Slow steps 1, Fast steps 2. If they ever meet, there’s a cycle. If Fast hits null, no cycle."
  hint3="For cycle entry (Floyd’s Tortoise): after meeting, reset one pointer to head; walk both at speed 1; meet at entry."
/>
---

<MarkSolved problem-slug="middle-of-the-linked-list" /> <Bookmark problem-slug="middle-of-the-linked-list" />

<InterviewTimer problem-slug="middle-of-the-linked-list" />



## Approach 1 — Two passes: count then jump

**Intuition.** Walk once to get length `n`; walk again `n/2` steps.



```java
ListNode middleNodeCount(ListNode head) {
    int n = 0;
    for (ListNode c = head; c != null; c = c.next) n++;
    ListNode m = head;
    for (int i = 0; i < n / 2; i++) m = m.next;
    return m;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Approach 2 — Fast &amp; slow (canonical)

**Insight from two-pass.** `fast` at 2× speed reaches the end when `slow` is at the middle — exactly. Odd length: `fast` ends at last node, `slow` at true middle. Even length: `fast` at null, `slow` at second middle.



```java
ListNode middleNode(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow;
}
```



<CodeTrace
  title="Fast/slow — 1→2→3→4→5→6"
  :values="['1','2','3','4','5','6']"
  :windowKeys="['slow','fast']"
  :cellWidth="34"
  :steps='[
    { pointers: { slow: 0, fast: 0 }, vars: {}, note: "both at head" },
    { pointers: { slow: 1, fast: 2 }, vars: {}, note: "slow=2, fast=3" },
    { pointers: { slow: 2, fast: 4 }, vars: {}, note: "slow=3, fast=5" },
    { pointers: { slow: 3, fast: 6 }, vars: { fast: "null" }, note: "fast is null → slow=4 (second middle)" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

**Trap.** If you use `while (fast.next != null && fast.next.next != null)` you get the *first* middle instead of the second. LC spec asks for second — the loop condition matters.

---

## Try it yourself

<JavaRunner problem-slug="middle-of-the-linked-list" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Two passes | O(n) | O(1) | acceptable |
| Fast/slow | **O(n)** | **O(1)** | canonical — one pass |

## When to use which

- **Ship this** → fast/slow pointers.
- **"Return first middle"** → switch loop condition to check `fast.next`.
- **"Return both middles for even n"** → `slow` is second; `slow.prev` (if doubly-linked) is first.
- **Splitting into halves** → fast/slow gives O(1) space split; use for [Sort List](/problems/sort-list).

<AiCompanion problem-slug="middle-of-the-linked-list" pattern-hint="fast/slow pointers" />

## Related problems

- [Linked List Cycle](/problems/linked-list-cycle) — same technique for detection
- [Linked List Cycle II](/problems/fast-slow-linked-list-cycle-ii) — find entry
- [Palindrome Linked List](/problems/palindrome-linked-list) — split at middle, reverse half
- [Sort List](/problems/sort-list) — merge sort using middle split

<FeedbackWidget problem-slug="middle-of-the-linked-list" />

<RelatedProblems problems="fast-slow-linked-list-cycle-ii::Fast Slow Linked List Cycle II|palindrome-linked-list::Palindrome Linked List|find-the-duplicate-number::Find The Duplicate Number" />
