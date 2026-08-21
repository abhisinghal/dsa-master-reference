# Fast / Slow Pointers (Floyd)

## Why fast / slow exists — the story

Imagine walking through a linked list where each node only tells you one thing: "go to my next node." There is no index, no length you can trust, and no way to jump backward. If the list is clean, eventually you hit `null`. If the list loops, you can walk forever and never know whether you are just on a long list or trapped in a cycle. The fast/slow pattern exists for exactly this kind of one-way maze. Instead of remembering every room you have visited, you send two walkers through the maze: one moves one step at a time, the other moves two. If there is a loop, the faster walker eventually laps the slower one like runners on a track.

Take `3→2→0→-4`, where `-4.next` points back to `2`. Start both pointers at `3`. After one round, slow is at `2`, fast is at `0`. After two rounds, slow is at `0`, fast is back at `2`. After three rounds, slow is at `-4`, fast is at `-4`. They meet, so you know there is a cycle. The clever second half is not just "there is a loop" — it is "where does the loop begin?" Reset one pointer to the head and leave the other at the meeting point. Move both one step at a time: head pointer goes `3→2`; meeting pointer goes `-4→2`; they collide at `2`, the entry.

Why should a junior engineer care? Because this pattern saves you from the default HashSet answer. A set of visited nodes is easy and correct, but it costs O(n) extra memory. Floyd's algorithm gives the same detection and entry location in O(1) space, which is exactly the kind of upgrade interviewers look for after you state the brute force.

> [key] **Key Insight** — After `k` steps, slow is at k, fast is at 2k. If they meet, they're inside a cycle. The distance from the meeting point to the cycle start equals the distance from the head to the cycle start — so reset slow to head, step both by 1, they meet exactly at the cycle entry.

## When to use it — one-successor structures

Fast/slow pointers are not "two pointers" in the sorted-array sense. They are a tool for structures where every state has exactly one next state, so repeatedly applying `next` forms either a chain that ends or a cycle that repeats.

### Recognize by
- "linked-list cycle", "detect a loop", "return the node where the cycle begins"
- "middle of linked list" or "second half of list" where one pointer should arrive halfway when another reaches the end
- "nth from end" where a fixed gap between two pointers replaces measuring length first
- "repeated transformation eventually reaches 1 or loops" such as Happy Number
- "array values point to indices" or "find duplicate without modifying array" — the array is secretly a functional graph
- "O(1) extra space" paired with a one-way structure

### When NOT to use it
Anything that isn't a single-successor structure. For general graphs (each node has multiple neighbours), use BFS/DFS. For two-pointer *on a sorted array*, the mechanism is entirely different — that's [Two Pointers](#two-pointers), driven by sortedness, not by a speed differential.

Also avoid this pattern when you must list every node in the cycle, when the structure can branch, or when the input is already indexed and a prefix/suffix computation answers the question more directly. Fast/slow tells you about meeting, distance, and relative position. It is not a replacement for graph traversal or sorting-based pair search.

## How to use it — template

```java
ListNode slow = head, fast = head;
while (fast != null && fast.next != null) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow == fast) {
        ListNode p = head;
        while (p != slow) {
            p = p.next;
            slow = slow.next;
        }
        return p;              // cycle entry
    }
}
return null;                   // no cycle
```

The template has two phases. Phase one moves at different speeds and answers "do the pointers ever meet?" The guard must check both `fast` and `fast.next`, because the fast pointer takes a double hop. Phase two starts one pointer from the head and one from the meeting point; moving both at speed one turns the algebra into code. If the problem only asks for detection, stop at `slow == fast`. If it asks for a middle node, keep the first phase but return `slow` when `fast` falls off the list.

---

## Linked List Cycle II (Floyd) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/)*

<ProgressCheck id="linked-list-cycle-ii-floyd" />

### Problem
Detect whether a singly linked list has a **cycle**, and if so return the node where the cycle **begins** — using O(1) space.

**Constraints:** up to `10⁴` nodes; the cycle (if present) is reachable by following `next`.

**Example 1:** `3→2→0→-4` with `-4` linking back to `2` → returns node `2`.

**Example 2:** `1→2→null` → `null` (no cycle, so no entry node).

### Solution — brute force
The first correct idea is to remember every node reference you have seen. Walk from `head`; before visiting a node, ask whether it is already in the set. If yes, that exact node is the cycle entry. If you reach `null`, there is no cycle.

```text
seen = empty HashSet
cur = head
while cur != null:
    if cur in seen: return cur
    add cur to seen
    cur = cur.next
return null
```

This is easy to explain and handles the entry node naturally. The cost is O(n) time and O(n) space, because in the no-cycle case you store every node. Floyd keeps the O(n) time but removes the set.

```java
ListNode detectCycleBrute(ListNode head) {
    Set<ListNode> seen = new HashSet<>();
    ListNode cur = head;
    while (cur != null) {
        if (seen.contains(cur)) return cur;
        seen.add(cur);
        cur = cur.next;
    }
    return null;
}
```

**Brute-force cost:** O(n) time, O(n) space — correct, but the extra visited set is what Floyd removes.

### Solution — optimized
Floyd turns "remember every node" into a speed difference. If a loop exists, fast eventually laps slow; then resetting one pointer to head makes both pointers walk equal remaining distances to the entry.

**Pattern.**
Detect a cycle and find its entry using two-speed pointers.

**Java.**
```java
ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {                 // meeting point
            ListNode p = head;
            while (p != slow) { p = p.next; slow = slow.next; }
            return p;                       // cycle entry
        }
    }
    return null;
}
```

### Time Complexity
Existing summary: Time O(n) · Space O(1).

The time is linear because the first phase visits at most a constant number of laps after slow enters the cycle, and the second phase walks from head to the entry once. No node values are copied and no visited set is stored.

The optimized method is O(n): before the meeting, fast/slow traverse at most the non-cycle prefix plus a bounded number of cycle steps; after the reset, both pointers walk only to the entry.

### Space Complexity
Space is O(1) because it keeps only pointer variables. Unlike the brute-force set, it never stores visited nodes.

### Learning notes
- Why guard `fast != null && fast.next != null`? — fast takes a two-hop step.
- Why move slow by one and fast by two? — the speed difference guarantees a collision inside a cycle.
- Why test `slow == fast` by reference? — equal node values do not prove the same node.
- Why create `ListNode p = head`? — one pointer must restart to locate the entry.
- Why move both one step after reset? — their distances to the cycle entry are equal modulo the loop length.

> [key] **Key Insight** — Slow and fast meet inside the cycle. From the head and from the meeting point, advancing both one step at a time, they meet exactly at the cycle entry (distance algebra: `head→entry == meeting→entry` modulo cycle length).

> [inv] **Invariant** — If a cycle of length `C` exists, after slow enters it, fast closes the gap by 1 per step, so they meet within `C` steps.

> [note] **Trace it** — Use `3→2→0→-4`, with `-4.next = 2`.
>
> | Round | slow moves to | fast moves to | Meaning |
> |---|---|---|---|
> | start | 3 | 3 | both begin at head |
> | 1 | 2 | 0 | fast is one node ahead inside the future loop |
> | 2 | 0 | 2 | fast has wrapped around the cycle |
> | 3 | -4 | -4 | pointers meet, so a cycle exists |
> | reset | p = 3 | slow = -4 | start entry-finding phase |
> | step 1 | p = 2 | slow = 2 | collision gives the cycle entry |
>
> The important part is that the first meeting point is not necessarily the entry. It is just a proof that a cycle exists. The reset-and-walk phase converts that proof into the exact node to return.

> [trap] **Common Trap** — Only checking `fast != null`. *Example:* even-length list `1→2`. After one step, `fast` is at `2` (non-null), so `fast.next.next` NPEs on the missing `next`. Check both `fast != null && fast.next != null` before the double hop.

> [note] **Interview script** — First, I'd verify this is a singly linked list and I need the entry node, not just true/false. The brute force is a `HashSet<ListNode>`: return the first repeated node in O(n) time and O(n) space. To optimize space, I'll use Floyd's two pointers: slow moves one step, fast moves two, and a meeting proves a cycle. Then I reset one pointer to head and move both one step at a time; their next meeting is the entry, so the final complexity is O(n) time and O(1) space.

> [pat] **Pattern Connection** — *Find the Duplicate Number* maps an array to a functional graph (`next = nums[i]`) and applies the identical algorithm — a classic "array is secretly a linked list" reframe.

### Why the reset works without memorizing algebra

Suppose the distance from head to the cycle entry is `A`, the cycle length is `C`, and the meeting point is `B` steps after the entry. Slow has walked `A + B`. Fast has walked twice that. The extra distance fast walked must be whole laps of the cycle, so `2(A+B) - (A+B) = A+B = mC`. Rearranged, `A = mC - B`. That means from the meeting point, walking `A` steps lands exactly at the entry because `C - B` steps complete the current lap, and the remaining laps do not change the final node. The code does not need to know `A`, `B`, or `C`; it just walks both pointers until equality.

A simpler mental model: once the two runners collide, one runner is exactly "head-to-entry distance" away from the entry if it keeps running around the loop. So put the other runner at the head and let both move at the same speed.

### How this pattern changes in common variants

For **Linked List Cycle I**, you stop at the first `slow == fast` and return `true`. There is no reset phase because the problem only asks whether a loop exists. For **Middle of the Linked List**, the same speeds are used but with no equality check; when `fast` reaches the end, `slow` is halfway. For **Happy Number**, a number is the node and `next(x)` is "sum of squared digits"; reaching 1 is success, while a fast/slow meeting away from 1 proves you are trapped in a cycle.

For **Find the Duplicate Number**, the values are valid indices. If `nums = [1,3,4,2,2]`, index `0` points to `1`, `1` points to `3`, `3` points to `2`, and `2` points to `4`, then `4` points back to `2`. The duplicate value creates the cycle entry. That is the same algorithm wearing an array costume.

### Edge cases to rehearse

Fast/slow code is short, so most interview mistakes come from not rehearsing the edge cases. A `null` head should return `null`; the while guard handles it before any dereference. A single node with `next = null` should also return `null`; `fast.next != null` fails. A single node with `next` pointing to itself should return that node; after one loop iteration, slow and fast are both back at the same node, then the reset phase immediately returns head. A two-node list with no cycle is the case that catches bad guards, because `fast.next.next` would cross past the tail.

Another detail: compare nodes by reference, not by value. If two different nodes both store value `7`, they are not the same location in the list. The cycle test is `slow == fast`, meaning the pointers have landed on the identical object. In Java LeetCode-style linked-list problems, `ListNode` usually does not override equality, but saying "reference equality" makes your intent clear.

For the duplicate-number array version, the edge cases look different but the mental model is the same. The array values must be valid next indices, and the usual LeetCode constraints guarantee one duplicate and values in `1..n`. If those constraints are missing, Floyd may walk out of bounds or find a cycle that does not mean "duplicate." Always attach the pattern to the constraint that every state has one safe next state.

### Debug checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Null pointer exception on short lists | guard checks only `fast != null` | use `fast != null && fast.next != null` |
| returns the meeting node, not entry | skipped reset phase | after collision, start `p` at head and walk both by one |
| infinite loop in no-cycle list | forgot to advance one pointer | update both `slow` and `fast` every iteration |
| wrong on duplicate values | compared `node.val` | compare node references with `==` |
| array duplicate version crashes | values are not valid indices | verify functional-graph constraints first |

### How to explain the proof without losing the interviewer

You do not need to dump equations immediately. Start with the runner analogy: once both pointers are inside the cycle, fast gains one node on slow each round, so a collision is inevitable. Then say the collision gives a special offset: the distance from head to entry matches the remaining distance from meeting point to entry, modulo the loop length. That is why one pointer from head and one from the meeting point land together at the entry.

If the interviewer wants the algebra, give the short version. Let `A` be head-to-entry, `B` entry-to-meeting, and `C` the cycle length. Slow traveled `A+B`; fast traveled twice that. The difference is `A+B`, and because they meet in a cycle, that difference is some whole number of cycle laps. Therefore `A+B = mC`, so `A = mC-B`, exactly the distance from the meeting point around to the entry. Then return to the code: the reset loop is just walking those equal distances.

### Same pattern, new tweaks

Two pointers at different speeds detect loops and locate structure without extra memory:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | stop as soon as fast meets slow; no need to locate the entry | O(n) |
| [Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | fast moves 2×, slow 1×; when fast ends, slow is the middle | O(n) |
| [Happy Number](https://leetcode.com/problems/happy-number/) | the "next" step is digit-square-sum; a cycle not containing 1 means unhappy | O(log n per step) |
| [Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) | treat `nums[i]` as a next pointer and return the cycle entry value | O(n) |
| [Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) | use fast/slow only to find the middle; then reverse the second half | O(n) |

---

## 🧠 Check your understanding

<Quiz patternId="fast-slow" :questions='[
  {
    "q": "A linked list may contain a cycle, and you need O(1) extra space. Which pattern fits?",
    "choices": [
      {
        "text": "Prefix sum with hash map"
      },
      {
        "text": "Fast and slow pointers",
        "correct": true,
        "explanation": "Yes. The two speeds guarantee a meeting inside a cycle without extra storage."
      },
      {
        "text": "K-way merge heap"
      },
      {
        "text": "Topological sort"
      }
    ]
  },
  {
    "q": "What loop guard prevents a null-pointer bug in fast-slow linked-list code?",
    "choices": [
      {
        "text": "fast is not null only",
        "explanation": "Not enough. fast.next may be null before fast.next.next is read."
      },
      {
        "text": "slow is not null only"
      },
      {
        "text": "fast and fast.next are not null",
        "correct": true,
        "explanation": "Correct. The two-step move needs both fast and its next node to exist."
      },
      {
        "text": "head equals tail"
      }
    ]
  },
  {
    "q": "When is fast-slow the wrong tool for cycle detection?",
    "choices": [
      {
        "text": "There is one deterministic next pointer"
      },
      {
        "text": "The structure is a linked list"
      },
      {
        "text": "The graph has arbitrary branching",
        "correct": true,
        "explanation": "Right. Branching graphs need visited sets, DFS, BFS, or Union-Find, not two runners on one path."
      },
      {
        "text": "Extra space must be constant"
      }
    ]
  }
]' />
