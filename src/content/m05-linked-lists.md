## Concepts & Mental Models

Linked-list problems are about maintaining ownership of edges while changing them. Arrays let you reason about indices; linked lists force you to reason about *links*. Before overwriting `node.next`, know whether the suffix it pointed to is still reachable through another variable.

!!! key "Pointer-surgery mindset"
    Treat every mutation as an edge deletion followed by an edge creation. At every loop boundary, state which prefix is already repaired, which suffix is untouched, and which variables keep both parts reachable.

Four mental models cover most interview variants:

- **Dummy-head technique.** A stable node before the real head makes deletion, insertion, and reversal at position 1 identical to middle-of-list cases.
- **Three-pointer reversal.** `prev` owns the reversed prefix, `curr` is the first unreversed node, and `next` preserves the suffix before `curr.next` is overwritten.
- **Fast/slow family.** Two cursors moving at different speeds detect cycles, find middles, split lists, and locate kth-from-end positions.
- **Sentinel doubly linked list.** Dummy `head`/`tail` sentinels remove empty-list and one-node special cases; every real node has exactly two neighboring links.

```diagram
{"type":"linkedlist","values":[1,2,3,4],"pointers":[{"name":"prev","index":0},{"name":"curr","index":1},{"name":"next","index":2}]}
```

---

## Reverse Linked List

!!! pattern "Pattern: Pointer reversal · T: O(n) · S: O(1) iterative"
    **Signals:** reverse every edge, singly linked list, preserve nodes rather than allocate replacements.

### 1. Problem

Given the head of a singly linked list, return the head of the same nodes with all links reversed. Provide iterative and recursive versions.

### 2. Intuition

Walk left to right and flip one edge at a time. The danger is that after `curr.next = prev`, the original successor is lost unless it was saved. Therefore each iteration has three moves: save `next`, reverse `curr.next`, then advance `prev` and `curr`.

### 3. Naive

Copy values into an array or stack, then write values back in reverse order. That returns the visible sequence but does **not** reverse node identities, and it costs O(n) extra space. Allocating a new reversed list has the same identity bug if callers hold references to existing nodes.

### 4. Key Observation

!!! key "Key observation"
    At loop start, `prev` is the head of a fully reversed prefix, `curr` is the first node of the untouched suffix, and every original node is reachable from exactly one of those two regions. Saving `next = curr.next` keeps the untouched suffix reachable while `curr.next` is repointed backward.

### 5. Pattern Recognition

**Signals.** "Reverse a list," "reverse k nodes," "reverse sublist," or any operation that moves the front node of one region into another.

**Shortcut.** If mutation of `curr.next` would strand the rest of the input, introduce a temporary successor variable before the write.

**Related.** Reverse Linked List II, Reverse Nodes in k-Group, Palindrome Linked List, Reorder List.

### 6. Invariant

At loop entry: `prev` points to the reversed prefix containing exactly the nodes originally before `curr`; `curr` points to the first node not yet reversed; the reversed prefix terminates at the original head with `next == null`; the untouched suffix still has original forward links. After one iteration, `curr` moves from the untouched suffix to the front of the reversed prefix.

### 7. Visual Explanation

```diagram
{"type":"linkedlist","values":[1,2,3,4],"pointers":[{"name":"prev","index":1},{"name":"curr","index":2},{"name":"next","index":3}]}
```

The snapshot is a loop boundary after nodes `1` and `2` have entered the reversed prefix. The next mutation makes node `3` point back to node `2`; `next` already remembers node `4`.

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":460,"box":260,"title":"Iterative three-pointer reversal","steps":[{"type":"start","text":"prev = null\ncurr = head"},{"type":"decision","text":"curr != null?","yes":"yes","branch":{"label":"no","text":"return prev","role":"green"}},{"type":"process","text":"next = curr.next"},{"type":"process","text":"curr.next = prev"},{"type":"process","text":"prev = curr\ncurr = next"}]}
```

### 9. Walkthrough

| iteration | `prev` reversed prefix | `curr` before write | saved `next` | write |
|---|---|---|---|---|
| 0 | `∅` | `1` | `2` | `1.next = null` |
| 1 | `1` | `2` | `3` | `2.next = 1` |
| 2 | `2→1` | `3` | `4` | `3.next = 2` |
| 3 | `3→2→1` | `4` | `null` | `4.next = 3` |

### 10. Why It Works

Initially, the reversed prefix is empty and the untouched suffix is the whole list. The loop body saves the suffix, redirects the first untouched node to the reversed prefix, and advances both region heads. When `curr == null`, the untouched suffix is empty, so `prev` contains every original node in reverse order.

The recursive version uses the call stack to defer edge flips. If `head.next` is already reversed by recursion and `newHead` points to the original tail, then `head.next.next = head` appends `head` after its successor, and `head.next = null` prevents a cycle.

### 11. Java

```java
class ListNode {
    int val;
    ListNode next;

    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class ReverseLinkedList {
    ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        return prev;
    }

    ListNode reverseListRecursive(ListNode head) {
        if (head == null || head.next == null) return head;
        ListNode newHead = reverseListRecursive(head.next);
        head.next.next = head;
        head.next = null;
        return newHead;
    }
}
```

### 12. Code Walkthrough

`next` is the only reference to the original suffix after `curr.next` is overwritten. In recursion, `head.next.next = head` reverses the local edge during stack unwinding; `head.next = null` is required for the original head and prevents a two-node cycle.

### 13. Complexity

!!! complexity "Complexity"
    **Iterative T:** O(n), one visit per node. **Iterative S:** O(1), three references. **Recursive T:** O(n). **Recursive S:** O(n) call stack, which can overflow on very long production lists.

### 14. Edge Cases

- `head == null` → `null`.
- One node → unchanged.
- Two nodes → good sanity test for accidentally creating `1↔2`.
- Duplicate values → irrelevant; node identity and edges define correctness.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Writing `curr.next = prev` before saving `curr.next`; returning `curr` instead of `prev`; forgetting `head.next = null` in recursion.

### 16. Optimization

The iterative solution is optimal in time and auxiliary space. In Java, prefer it for unbounded input because there is no guaranteed tail-call elimination.

### 17. Alternatives

A dummy-head insertion method repeatedly removes the current node and inserts it at the front of a new dummy list. It is also O(n)/O(1), but the direct three-pointer invariant is simpler.

### 18. Interview Follow-Ups

- Reverse only positions `left..right`.
- Reverse in groups of `k`.
- Reverse a doubly linked list by swapping `prev` and `next`.
- Reverse an immutable list without mutating original nodes.

### 19. Variations

The same invariant powers reversing a second half for palindrome checks, reversing the tail before interleaving in Reorder List, and reversing fixed windows for k-group problems.

### 20. Pattern Connection

This is the canonical **pointer surgery** pattern. Mastering `prev` reversed, `curr` untouched, and `next` saved makes later linked-list problems controlled compositions rather than ad hoc pointer juggling.

---

## Reverse Linked List II (Reverse a Sublist)

!!! pattern "Pattern: Dummy head + local reversal · T: O(n) · S: O(1)"
    **Signals:** reverse positions `left..right`, handle `left = 1`, preserve all outside nodes.

### Problem

Reverse the nodes from 1-indexed position `left` through `right` inclusive, and return the head of the modified list.

### Key Observation

!!! key "Key observation"
    A dummy node lets `before` always mean "node immediately before the sublist," even when the sublist starts at the real head. Repeated front-insertion moves `curr.next` to the front of the window without disturbing nodes before `before` or after the window.

### Invariant

Before each inner iteration, `before.next` is the current head of the partially reversed window, `curr` is the tail of that window, and `curr.next` is the next node to move to the front. Nodes outside the window remain correctly connected.

### Visual Explanation

```diagram
{"type":"linkedlist","values":[0,1,2,3,4,5],"pointers":[{"name":"dummy","index":0},{"name":"before","index":1},{"name":"curr","index":2},{"name":"move","index":3}]}
```

Here `0` is the dummy. To reverse `2..4`, detach `move = 3` from after `curr = 2` and insert it after `before = 1`; repeat for `4`.

### Java

```java
ListNode reverseBetween(ListNode head, int left, int right) {
    if (head == null || left == right) return head;

    ListNode dummy = new ListNode(0, head);
    ListNode before = dummy;
    for (int i = 1; i < left; i++) before = before.next;

    ListNode curr = before.next;
    for (int i = 0; i < right - left; i++) {
        ListNode move = curr.next;
        curr.next = move.next;
        move.next = before.next;
        before.next = move;
    }
    return dummy.next;
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n) to reach the window and reverse it. **S:** O(1), only a dummy and references.

### Pattern Connection

This is **dummy-head front insertion** layered on top of reversal. It is often simpler than a detached three-pointer reversal because the sublist tail (`curr`) never changes.

---

## Merge Two Sorted Lists

!!! pattern "Pattern: Dummy tail merge · T: O(n + m) · S: O(1)"
    **Signals:** two sorted linked lists, produce sorted union by reusing nodes.

### Problem

Given heads `list1` and `list2`, merge them into one sorted list and return its head. Existing nodes should be relinked, not copied.

### Key Observation

!!! key "Key observation"
    Keep a `tail` pointer to the last node of the merged prefix. At every step, append the smaller current head and advance only the list that contributed that node. The dummy node makes the first append identical to all later appends.

### Invariant

At loop entry, `dummy.next..tail` is sorted and contains exactly the smallest already-consumed nodes from both lists. `list1` and `list2` point to the unconsumed suffixes, each individually sorted. Appending the smaller head preserves sorted order.

### Visual Explanation

```diagram
{"type":"linkedlist","values":[0,1,1,2,3,4],"pointers":[{"name":"dummy","index":0},{"name":"tail","index":2},{"name":"list1","index":3},{"name":"list2","index":4}]}
```

The merged prefix ends at `tail`. The next append compares current heads `2` and `3` and advances the chosen source pointer.

### Java

```java
ListNode mergeTwoLists(ListNode list1, ListNode list2) {
    ListNode dummy = new ListNode(0);
    ListNode tail = dummy;

    while (list1 != null && list2 != null) {
        if (list1.val <= list2.val) {
            tail.next = list1;
            list1 = list1.next;
        } else {
            tail.next = list2;
            list2 = list2.next;
        }
        tail = tail.next;
    }
    tail.next = (list1 != null) ? list1 : list2;
    return dummy.next;
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n + m), each node is appended once. **S:** O(1) auxiliary space; the output list reuses input nodes.

### Pattern Connection

This is the linked-list analogue of the merge step in merge sort. The dummy-tail pattern also appears in partitioning, filtering, and stable concatenation problems.

---

## Linked List Cycle Detection (Floyd's) + Find Cycle Start

!!! pattern "Pattern: Fast/slow pointers · T: O(n) · S: O(1)"
    **Signals:** cycle in a linked structure, no extra memory, need existence or cycle entry.

### 1. Problem

Given the head of a singly linked list, determine whether it contains a cycle. If a cycle exists, return the node where the cycle begins; otherwise return `null`.

### 2. Intuition

Two runners move through the list: `slow` advances one edge and `fast` advances two. In an acyclic list, `fast` reaches `null`. In a cyclic list, once both are inside the cycle, `fast` gains one node per iteration modulo the cycle length, so it must eventually land on `slow`.

### 3. Naive

Store visited nodes in a `HashSet<ListNode>`. The first repeated node is the cycle start. This is simple, but it costs O(n) memory and relies on node identity hashing.

### 4. Key Observation

!!! key "Key observation"
    Floyd's algorithm has two phases. Phase 1 proves a cycle exists by a modular-speed collision. Phase 2 resets one pointer to `head`; moving both one step at a time makes them meet exactly at the entry because the distance from head to entry equals the remaining distance from collision to entry modulo the cycle length.

### 5. Pattern Recognition

**Signals.** "Detect cycle," "find duplicate without modifying array" (array as next pointers), "find loop start," or "constant space visitation."

**Shortcut.** If repeated traversal state would normally require a set, ask whether the structure is a functional graph: each node has at most one outgoing edge.

**Related.** Happy Number, Find Duplicate Number, circular-array loop detection, middle of linked list.

### 6. Invariant

Phase 1: after `t` iterations, `slow` has moved `t` edges and `fast` has moved `2t` edges. Once inside the cycle, the relative offset changes by `1 mod cycleLength` per iteration.

Phase 2: `finder` starts at `head`, `slow` starts at the collision. After `k` synchronized steps, `finder` is `k` edges from head and `slow` is `k` edges from the collision along the cycle.

### 7. Visual Explanation

```diagram
{"type":"linkedlist","values":[3,2,0,-4],"pointers":[{"name":"slow","index":1},{"name":"fast","index":2}],"cycle_to":1}
```

The tail node `-4` points back to node `2`. Once both pointers enter the cycle, `fast` reduces the cyclic distance to `slow` by one each iteration.

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":500,"box":290,"title":"Floyd detection and entry location","steps":[{"type":"start","text":"slow = head\nfast = head"},{"type":"decision","text":"fast and fast.next exist?","yes":"yes","branch":{"label":"no","text":"return null","role":"red"}},{"type":"process","text":"slow = slow.next\nfast = fast.next.next"},{"type":"decision","text":"slow == fast?","yes":"yes","branch":{"label":"no","text":"continue phase 1","role":"primary"}},{"type":"process","text":"finder = head"},{"type":"decision","text":"finder == slow?","yes":"yes","branch":{"label":"no","text":"advance both one step","role":"primary"}},{"type":"end","text":"return finder"}]}
```

### 9. Walkthrough

For `3→2→0→-4↘` with `-4.next = 2`:

| iteration | slow | fast | note |
|---|---|---|---|
| 0 | 3 | 3 | start |
| 1 | 2 | 0 | fast gained one inside path |
| 2 | 0 | 2 | both in cycle |
| 3 | -4 | -4 | collision |

Then reset `finder = 3`. Move both one step: `finder = 2`, `slow = 2`; the entry is found.

### 10. Why It Works

Let `a` be the number of edges from head to the cycle entry, `b` the number of edges from entry to the collision point, and `c` the remaining edges from collision back to entry. The cycle length is `L = b + c`.

At collision, `slow` has traveled `a + b`. `fast` has traveled twice as far, so `2(a + b) = a + b + qL` for some positive integer `q`; the difference is whole cycles. Thus `a + b = qL`, so `a = qL - b = (q - 1)L + c`. The distance from head to entry is congruent to the distance from collision to entry modulo `L`. Starting one pointer at head and one at collision makes them meet at entry after `a` steps.

Collision existence follows because after both pointers enter the cycle, the relative offset `fast - slow` increases by one modulo `L` each iteration, so it visits every residue and eventually becomes zero.

### 11. Java

```java
class CycleDetection {
    boolean hasCycle(ListNode head) {
        return detectCycle(head) != null;
    }

    ListNode detectCycle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                ListNode finder = head;
                while (finder != slow) {
                    finder = finder.next;
                    slow = slow.next;
                }
                return finder;
            }
        }
        return null;
    }
}
```

### 12. Code Walkthrough

The guard checks `fast.next` before the two-step move. Equality must be reference equality (`slow == fast`), not value equality. After collision, reusing `slow` is safe because it remains on the cycle; `finder` and `slow` advance at the same speed until the distance congruence forces their meeting at the entry.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n). Before collision, `slow` enters the cycle after `a` steps and meets `fast` within at most `L` more steps. Phase 2 costs `a` steps. **S:** O(1), only pointer variables.

### 14. Edge Cases

- Empty list or single acyclic node → guard fails and returns `null`.
- Single node self-cycle → first iteration collides at head and phase 2 returns head.
- Cycle begins at head → `a = 0`; the phase-2 argument still holds modulo the cycle length.
- Duplicate values do not matter; cycles are about node identity.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Comparing `val` fields instead of node references; using an unsafe `fast.next.next` guard; resetting both pointers after collision; returning the collision node as the entry without phase 2.

### 16. Optimization

Floyd is already optimal for O(1) memory. Brent's algorithm is a constant-factor alternative that moves one pointer in exponentially growing blocks and can reduce pointer dereferences.

### 17. Alternatives

A `HashSet` gives a shorter proof and directly returns the first repeated node, at O(n) space. Marking nodes by mutating them is usually unacceptable because it corrupts data structure invariants and fails for shared lists.

### 18. Interview Follow-Ups

- Find cycle length after collision by walking once around the cycle.
- Remove the cycle by finding the predecessor of entry inside the loop.
- Apply the same idea to `nums[i]` as a pointer for Find Duplicate Number.
- Detect whether two singly linked lists intersect, with or without cycles.

### 19. Variations

The tortoise-hare family includes middle-node discovery (`fast` two steps, `slow` one), kth-from-end with a fixed gap, and functional-graph cycle detection in state machines.

### 20. Pattern Connection

Fast/slow is a **relative motion invariant**. Instead of storing visited nodes, encode progress in speed difference and exploit either `null` termination or modulo-cycle collision.

---

## Reorder List

!!! pattern "Pattern: Split · reverse · weave · T: O(n) · S: O(1)"
    **Signals:** transform `L0→L1→...→Ln` into `L0→Ln→L1→Ln-1...` in-place.

### Problem

Reorder a list into first, last, second, second-last, and so on. Do not change node values.

### Key Observation

!!! key "Key observation"
    The target order is obtained by splitting at the middle, reversing the second half, then alternating nodes from the first half and reversed second half. Each phase has a simple invariant; trying to weave from the original tail directly is what makes the problem hard.

### Invariant

After splitting, `first` owns the front half and `second` owns the reversed back half. During weaving, the prefix before `first` is already in final order; `first` and `second` point to the next nodes to append from their respective halves. Save both successors before rewiring.

### Visual Explanation

```diagram
{"type":"linkedlist","values":[1,2,3,5,4],"pointers":[{"name":"first","index":1},{"name":"second","index":3}]}
```

After reversing the second half of `1→2→3→4→5`, the back half is `5→4`; weaving alternates `1,5,2,4,3`.

### Java

```java
void reorderList(ListNode head) {
    if (head == null || head.next == null) return;

    ListNode slow = head;
    ListNode fast = head;
    while (fast.next != null && fast.next.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }

    ListNode second = slow.next;
    slow.next = null;
    second = reverse(second);

    ListNode first = head;
    while (second != null) {
        ListNode firstNext = first.next;
        ListNode secondNext = second.next;
        first.next = second;
        second.next = firstNext;
        first = firstNext;
        second = secondNext;
    }
}

private ListNode reverse(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n), three linear passes: find middle, reverse half, weave. **S:** O(1) auxiliary space.

### Pattern Connection

Reorder List composes two primitives from this module: fast/slow splitting and three-pointer reversal. The final merge is the same alternating-tail discipline used in list zipping.

---

## Palindrome Linked List

!!! pattern "Pattern: Middle + reverse second half · T: O(n) · S: O(1)"
    **Signals:** compare symmetric positions in a singly linked list without extra array storage.

### Problem

Return whether the sequence of values in a singly linked list reads the same forward and backward.

### Key Observation

!!! key "Key observation"
    A singly linked list has no backward traversal, so create one by reversing the second half in place. Then compare the first half and reversed second half node by node. For odd length, the middle node is skipped naturally by the comparison length.

### Invariant

During comparison, all nodes before `p1` in the first half and before `p2` in the reversed second half have matched pairwise. `p2` bounds the comparison length; if the second half is exhausted, every symmetric pair matched.

### Visual Explanation

```diagram
{"type":"linkedlist","values":[1,2,3,2,1],"pointers":[{"name":"slow","index":2},{"name":"p1","index":0},{"name":"p2","index":4}]}
```

For odd length, `slow` lands on the middle value `3`; reversing from `slow` produces traversal sequence `1,2,3`, and comparing while `p2` is non-null validates all needed pairs.

### Java

```java
boolean isPalindrome(ListNode head) {
    if (head == null || head.next == null) return true;

    ListNode slow = head;
    ListNode fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }

    ListNode second = reverse(slow);
    ListNode restoreHead = second;
    ListNode first = head;
    boolean ok = true;

    while (second != null) {
        if (first.val != second.val) {
            ok = false;
            break;
        }
        first = first.next;
        second = second.next;
    }

    reverse(restoreHead);
    return ok;
}

private ListNode reverse(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n). Finding the middle, reversing, comparing, and optional restoration are linear. **S:** O(1) auxiliary space.

### Pattern Connection

This is the canonical case where modifying the list temporarily is cheaper than storing values. In production, restoring the second half is often part of the contract even if interview platforms do not require it.

---

## LRU Cache (HashMap + Doubly Linked List)

!!! pattern "Pattern: Hash index + recency DLL · T: O(1) get/put · S: O(capacity)"
    **Signals:** bounded cache, evict least recently used, reads update recency, O(1) operations required.

### 1. Problem

Design an LRU cache with positive capacity. `get(key)` returns the value if present, otherwise `-1`, and marks the key as most recently used. `put(key, value)` inserts or updates a key, marks it most recently used, and evicts the least recently used key when capacity is exceeded.

### 2. Intuition

Two operations are in tension: lookup by key wants a hash table; eviction by age wants an ordered sequence. Combine them: `Map<Integer, Node>` gives direct access to a node, while a doubly linked list stores nodes from least recent to most recent. Touching a node removes it from its current position and appends it at the MRU end.

### 3. Naive

A `HashMap` plus timestamps can find values in O(1), but eviction requires scanning all entries for the smallest timestamp: O(capacity). A plain list can evict in O(1), but lookup is O(capacity). `LinkedHashMap` solves this in Java, but implementing the structure demonstrates the invariant interviewers want.

### 4. Key Observation

!!! key "Key observation"
    Store exactly one node per cached key, and make the hash map point to that node. Because each node has `prev` and `next`, removal is O(1) after lookup. Dummy `head` and `tail` sentinels make every insertion/removal a four-pointer splice with no empty-list branches.

### 5. Pattern Recognition

**Signals.** "Least/most recently used," "O(1) get and put," "evict oldest by access order," "read changes priority."

**Shortcut.** If an item must be both addressable by key and movable inside an ordering, use a map to a linked-list node, not a map to a value.

**Related.** LFU Cache uses frequency buckets plus DLLs; browser history uses a cursor in a doubly linked list; scheduler queues often combine maps with intrusive list nodes.

### 6. Invariant

At all public method boundaries:

1. `head.next` is the least recently used real node, or `tail` if empty.
2. `tail.prev` is the most recently used real node, or `head` if empty.
3. For every cached key `k`, `map.get(k)` is the unique node in the DLL with `node.key == k`.
4. Every real node in the DLL is present in the map; sentinels are never present in the map.
5. For every adjacent pair `a <-> b`, `a.next == b` and `b.prev == a`.

### 7. Visual Explanation

```diagram
{"type":"linkedlist","values":[-1,10,20,30,-1],"pointers":[{"name":"head","index":0},{"name":"LRU","index":1},{"name":"MRU","index":3},{"name":"tail","index":4}],"doubly":true}
```

The list stores recency, not sorted keys. The map stores `10 → node(10)`, `20 → node(20)`, `30 → node(30)`. A `get(20)` removes node `20` from the middle and inserts it before `tail`, making it MRU.

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":520,"box":300,"title":"LRU operations","steps":[{"type":"start","text":"operation(key,value?)"},{"type":"decision","text":"key in map?","yes":"yes","branch":{"label":"no","text":"create node for put\nor return -1 for get","role":"red"}},{"type":"process","text":"read/update node.value"},{"type":"process","text":"remove node from DLL"},{"type":"process","text":"insert node before tail"},{"type":"decision","text":"size > capacity?","yes":"yes","branch":{"label":"no","text":"done","role":"green"}},{"type":"process","text":"evict head.next\nremove from map and DLL"},{"type":"end","text":"return result"}]}
```

### 9. Walkthrough

Capacity `2`:

| operation | map keys | recency list LRU→MRU | result |
|---|---|---|---|
| `put(1,1)` | `{1}` | `1` | — |
| `put(2,2)` | `{1,2}` | `1,2` | — |
| `get(1)` | `{1,2}` | `2,1` | `1` |
| `put(3,3)` | `{1,3}` | `1,3` | evict `2` |
| `get(2)` | `{1,3}` | `1,3` | `-1` |
| `put(4,4)` | `{3,4}` | `3,4` | evict `1` |

### 10. Why It Works

The map ensures O(1) access to the exact node for a key. The DLL invariant ensures that deleting that node needs only its two neighbors, and inserting at MRU needs only `tail.prev` and `tail`. Every successful `get` and every `put` represents use of that key, so moving the node to the MRU end preserves recency order. When capacity is exceeded, the least recent real node is exactly `head.next` by invariant, so evicting it implements the LRU policy.

### 11. Java

```java
import java.util.HashMap;
import java.util.Map;

class LRUCache {
    private static final class Node {
        int key;
        int value;
        Node prev;
        Node next;

        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }

    private final int capacity;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0);
    private final Node tail = new Node(0, 0);

    LRUCache(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException("capacity must be positive");
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    int get(int key) {
        Node node = map.get(key);
        if (node == null) return -1;
        moveToMostRecent(node);
        return node.value;
    }

    void put(int key, int value) {
        Node node = map.get(key);
        if (node != null) {
            node.value = value;
            moveToMostRecent(node);
            return;
        }

        Node created = new Node(key, value);
        map.put(key, created);
        addBeforeTail(created);

        if (map.size() > capacity) {
            Node lru = head.next;
            remove(lru);
            map.remove(lru.key);
        }
    }

    private void moveToMostRecent(Node node) {
        remove(node);
        addBeforeTail(node);
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void addBeforeTail(Node node) {
        Node prevMostRecent = tail.prev;
        prevMostRecent.next = node;
        node.prev = prevMostRecent;
        node.next = tail;
        tail.prev = node;
    }
}
```

### 12. Code Walkthrough

`head` and `tail` are sentinels and never represent cache entries. `addBeforeTail` always makes a node MRU. `remove` assumes the node is currently linked; that is true for every node obtained from the map. On update, no new node is created, preserving the one-map-entry/one-DLL-node invariant. On eviction, removal from the DLL and removal from the map must both happen or the structures diverge.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(1) average for `get` and `put`: one hash lookup plus constant pointer splices. **S:** O(capacity): one node and one map entry per cached key, plus two sentinels.

### 14. Edge Cases

- Updating an existing key must not increase size.
- Capacity `1` should repeatedly evict the previous key on distinct inserts.
- `get` of a missing key must not mutate recency.
- Negative keys/values are fine if the API allows them; `-1` is only the miss sentinel for `get`.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Storing `map<key,value>` instead of `map<key,node>`; forgetting to move a key on `get`; evicting after update of an existing key; removing from the DLL but not the map; handling real head/tail nodes with branches instead of sentinels.

### 16. Optimization

Pre-sizing the `HashMap` can reduce rehashing for large capacities, but does not change complexity. In production Java, `LinkedHashMap` with access-order mode implements this policy directly; interviews typically expect the manual DLL to show O(1) splice reasoning.

### 17. Alternatives

`LinkedHashMap<Integer,Integer>` can override `removeEldestEntry` for concise production code. A heap plus timestamps gives O(log n) updates and stale entries. A queue plus map fails because moving an arbitrary existing key to MRU is not O(1) without a node handle.

### 18. Interview Follow-Ups

- Implement `delete(key)` in O(1).
- Make the cache thread-safe and discuss coarse locks versus segmented locks.
- Add TTL expiration; distinguish time-based eviction from recency eviction.
- Design LFU Cache where frequency ties break by recency.

### 19. Variations

The same map-to-node + DLL pattern powers MRU caches, ordered sets with O(1) delete given a handle, and frequency-bucket caches where each bucket is itself a recency DLL.

### 20. Pattern Connection

LRU is the flagship **index + linked order** design. The linked list supplies stable O(1) local mutation; the hash map supplies global addressability. Senior-level correctness comes from keeping the two representations perfectly synchronized at every method boundary.
