## The Pattern

Fast & slow pointers run two traversals over the same implicit sequence at different speeds. The speed difference converts structural questions — cycle existence, cycle entry, midpoint, periodicity — into pointer meetings.

!!! pattern "Recognition signals"
    Linked list with O(1) space constraint, "detect a cycle," "find cycle start," "find middle," "happy number," or an iterative function `x -> f(x)` over a finite state space where repeated states imply a loop.

```diagram
{"type":"linkedlist","values":["3","2","0","-4"],"pointers":[{"name":"slow","index":1},{"name":"fast","index":3}],"cycle_to":1,"doubly":false}
```

## The Invariant

After `t` loop iterations, slow has advanced `t` steps and fast has advanced `2t` steps, unless the sequence ended. Inside a cycle, the gap changes by one modulo the cycle length each iteration, so a meeting is inevitable. Once slow and fast meet, resetting one pointer to head and moving both one step preserves equal distance to the cycle entry.

## Template

```java
class ListNode {
    int val;
    ListNode next;
}

ListNode detectCycleStart(ListNode head) {
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
            return p;
        }
    }
    return null;
}

ListNode middleNode(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow; // second middle for even length
}

boolean isHappy(int n) {
    int slow = n, fast = nextHappy(n);
    while (fast != 1 && slow != fast) {
        slow = nextHappy(slow);
        fast = nextHappy(nextHappy(fast));
    }
    return fast == 1;
}

int nextHappy(int x) {
    int sum = 0;
    while (x > 0) {
        int d = x % 10;
        sum += d * d;
        x /= 10;
    }
    return sum;
}
```

## Worked Recognition

- **Linked List Cycle Detection (Floyd's) + Find Cycle Start**: canonical Floyd proof. Meeting proves a cycle; reset-to-head finds the entry by distance algebra.
- **Palindrome Linked List**: use fast/slow to find the middle before reversing the second half; the palindrome logic is separate.
- **Reorder List**: first split at the middle with fast/slow, then reverse and merge alternating halves.

```diagram
{"type":"flow","width":430,"box":260,"title":"Floyd cycle detection","steps":[{"type":"start","text":"slow = head; fast = head"},{"type":"decision","text":"fast and fast.next exist?","yes":"advance","branch":{"label":"no","text":"acyclic","role":"green"}},{"type":"process","text":"slow = slow.next\nfast = fast.next.next"},{"type":"decision","text":"slow == fast?","yes":"reset one pointer to head","branch":{"label":"no","text":"continue","role":"primary"}},{"type":"end","text":"move both one step;\nmeeting is cycle start"}]}
```

## Complexity

!!! complexity "Complexity"
    **T:** O(n) for finite lists/sequences; Floyd may traverse a prefix plus a bounded number of cycle laps. **S:** O(1), which is the main advantage over a visited set.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Dereferencing `fast.next.next` without checking `fast` and `fast.next`; returning the first meeting node as the cycle start; choosing the wrong middle convention for even lengths; mutating a linked list for palindrome/reorder and forgetting to restore it if the API expects no side effects.

## When NOT to use it

Do not use fast/slow when you need all repeated states, cycle length distribution, or path reconstruction; a hash set/map is clearer. It also does not replace binary search for sorted random-access arrays, even though both move at different "speeds."
