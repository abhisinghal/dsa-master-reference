# Mock Interview Transcripts

*The Interview Playbook (Ch. 01) described the 6-phase loop abstractly. This chapter shows what those phases sound like when a real senior candidate is speaking. Three transcripts — Easy, Medium, Hard — annotated with what the interviewer is grading at each point.*

Read once for the shape, then again with the annotations covered — pretending you're the candidate — and see if you'd say the same things.

## Transcript 1 — Two Sum (Easy warmup — should take ≤ 15 min)

**Setup:** Interviewer opens with *"Given an array of integers `nums` and an integer `target`, return the indices of the two numbers that add up to `target`. You may assume each input has exactly one solution."*

---

**Candidate**: OK, before I dive in — a few clarifying questions. **[phase: clarify]**

*Can the array have negative numbers? Or duplicates?*

**Interviewer**: Yes to both.

*Can the same element be used twice? Like if `nums = [3]` and `target = 6`, is `[0, 0]` a valid answer?*

**Interviewer**: No, you can't use the same element twice. Two distinct indices.

*And you said "exactly one solution" — so I don't need to worry about no-solution or multiple-solution cases?*

**Interviewer**: Correct.

*Return the two indices in any order?*

**Interviewer**: Any order.

&gt; **What the interviewer sees:** The candidate is not rushing to code. They're pulling out the constraints that matter. "Same element twice" and "guaranteed solution" are both real ambiguities that separate candidates who read carefully from candidates who assume.

---

**Candidate**: Let me try a small example to make sure I understand. **[phase: examples]** If `nums = [2, 7, 11, 15]` and `target = 9`, the answer is `[0, 1]` because `nums[0] + nums[1] = 9`. If `nums = [3, 2, 4]` and `target = 6`, the answer is `[1, 2]` because `2 + 4 = 6`.

**Interviewer**: Correct.

---

**Candidate**: OK. **The brute force is O(n²) — for each element, scan the rest looking for `target - nums[i]`.** **[phase: brute]** Let me write that mentally:



```
for i in 0..n:
    for j in i+1..n:
        if nums[i] + nums[j] == target: return [i, j]
```



That's obviously correct but O(n²). For `n = 10⁴` it works; for `n = 10⁶` it doesn't.

To optimize — the inner loop is "does the array contain `target - nums[i]` at some index `> i`?" A hash map turns that from O(n) into O(1). **[phase: optimize]**

I'll scan once. At each `i`, I compute `complement = target - nums[i]`. If I've already seen `complement`, return `[stored_index, i]`. Otherwise, remember I've seen `nums[i]` at index `i`.

**Interviewer**: Sounds good. What's the complexity?

**Candidate**: Time O(n), space O(n) for the map. Better than sorting the array which would be O(n log n) — plus sorting loses original indices, so I'd need to store them, which just brings us back to a map anyway.

&gt; **What the interviewer sees:** Brute force stated explicitly. Complexity said aloud *before* coding. Compared to an alternative (sort + two pointers) and explained why the map is cleaner *for this problem*. This is a senior signal.

---

**Candidate**: OK, coding. **[phase: code]**



```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (seen.containsKey(complement)) {
            return new int[]{seen.get(complement), i};
        }
        seen.put(nums[i], i);
    }
    return new int[0];   // problem says one solution exists, but return empty defensively
}
```



*Let me trace `nums = [2, 7, 11, 15], target = 9`:* **[phase: verify]**

- i=0: complement=7, seen is empty, put(2→0). seen: {2:0}.
- i=1: complement=2, seen has 2! Return [0, 1]. ✓

*And `nums = [3, 2, 4], target = 6`:*

- i=0: complement=3, empty, put(3→0). {3:0}
- i=1: complement=4, not present, put(2→1). {3:0, 2:1}
- i=2: complement=2, present at index 1. Return [1, 2]. ✓

*Edge cases to think about:*

- Empty array: my loop won't execute, returns empty. Safe.
- Single element: same — loop iterates once, no match, returns empty. Safe.
- Duplicates like `nums = [3, 3], target = 6`: i=0 puts 3→0. i=1 finds complement=3 present. Returns [0, 1]. ✓

**Interviewer**: Great. What if the input was **sorted**? Would you change your approach?

**Candidate**: If it's sorted, two pointers becomes O(1) space and O(n) time — better than the map. `left=0, right=n-1`; while `left < right`: sum = nums[left] + nums[right]; if too small, `left++`; if too big, `right--`; if equal, return. Same time, better space.

&gt; **What the interviewer sees:** Candidate went beyond the asked question, showing pattern flexibility. Also — noticed defensive return, edge case walk-through. Total time: ~12 minutes. Strong hire signal.

---

## Transcript 2 — LRU Cache (Medium — should take 25–35 min)

**Setup:** *"Design a data structure that supports `get(key)` and `put(key, value)` in O(1) average time, with capacity `k` — evict least recently used when full."*

---

**Candidate**: Clarifying: **[phase: clarify]**

*When you `get` a key that's not present, what do I return?*

**Interviewer**: `-1`.

*When I `put` a key that already exists — do I update the value AND move it to "most recently used"?*

**Interviewer**: Yes, and yes.

*So an accessed key becomes "most recently used" — meaning `get` also counts as an access, moving it to MRU?*

**Interviewer**: Correct. Both `get` and `put` count as accesses.

*Do I need to handle thread safety?*

**Interviewer**: Not for now — single-threaded.

*And O(1) is worst-case or average?*

**Interviewer**: Amortized average is fine — that's what HashMap gives you.

---

**Candidate**: Great. **[phase: examples]** Let me trace an example. Capacity 2:

- `put(1, "a")` → cache: `[1→a]`
- `put(2, "b")` → cache: `[1→a, 2→b]`, 2 is MRU
- `get(1)` → returns "a", cache reorders: `[2→b, 1→a]`, 1 is MRU
- `put(3, "c")` → capacity full, evict LRU which is 2. Cache: `[1→a, 3→c]`.
- `get(2)` → returns -1.

**Interviewer**: Correct.

---

**Candidate**: **The key insight is I need TWO operations to be O(1):** **[phase: optimize]**

1. **Lookup by key** → hash map.
2. **Reorder to "most recently used"** → some kind of list where I can pull an element from the middle and put it at the end in O(1).

A `HashMap` alone gives me lookup but not ordered access. A `LinkedList` alone gives me ordered access but O(n) lookup. Combine them: a HashMap from key → node, and a doubly-linked list of nodes ordered from LRU (head) to MRU (tail).

**Interviewer**: Why doubly-linked?

**Candidate**: Because when I access a node, I need to unlink it from its current position — which requires knowing its previous node. Singly linked would be O(n) to find the previous. Doubly gives me `node.prev` in O(1).

Also — dummy head and tail sentinels. That way I never have to null-check when inserting or removing at the boundaries — every "real" node has both a `prev` and a `next`.

&gt; **What the interviewer sees:** Candidate justified every data-structure choice by tying it to an operation's complexity. Named "dummy sentinels" unprompted — mid-to-senior signal.

---

**Candidate**: **Coding.** **[phase: code]**



```java
class LRUCache {
    private static class Node {
        int key, val;
        Node prev, next;
        Node(int k, int v) { key = k; val = v; }
    }
    private final int capacity;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0);   // dummy: head.next = LRU
    private final Node tail = new Node(0, 0);   // dummy: tail.prev = MRU

    public LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) return -1;
        moveToTail(node);           // MRU
        return node.val;
    }

    public void put(int key, int value) {
        Node existing = map.get(key);
        if (existing != null) {
            existing.val = value;
            moveToTail(existing);
            return;
        }
        Node node = new Node(key, value);
        map.put(key, node);
        addAtTail(node);
        if (map.size() > capacity) {
            Node lru = head.next;
            removeNode(lru);
            map.remove(lru.key);
        }
    }

    private void addAtTail(Node node) {
        node.prev = tail.prev;
        node.next = tail;
        tail.prev.next = node;
        tail.prev = node;
    }
    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    private void moveToTail(Node node) {
        removeNode(node);
        addAtTail(node);
    }
}
```



*Trace with capacity 2:* **[phase: verify]**

- put(1, "a"): map={1→N1}, list: [head, N1, tail]
- put(2, "b"): map={1→N1, 2→N2}, list: [head, N1, N2, tail]
- get(1) → "a"; moveToTail(N1) → list: [head, N2, N1, tail]
- put(3, "c"): map has no 3, add N3. list: [head, N2, N1, N3, tail]. Size=3 &gt; cap=2 → evict LRU=N2. list: [head, N1, N3, tail], map={1→N1, 3→N3}. ✓

**Interviewer**: Great. What about thread safety?

**Candidate**: For a concurrent version, I'd wrap access in a `ReentrantReadWriteLock` — reads take read-lock, writes take write-lock. But that hurts throughput because reads also reorder (which is a write to the list). A better choice is `ConcurrentHashMap` + a segmented locking approach on the linked list — but honestly, at that point I'd use `Caffeine`. Building a concurrent LRU from scratch is a lot of code and gets subtle around eviction races.

&gt; **What the interviewer sees:** Correct implementation on first try. Answered follow-up with real-world honesty ("I'd use Caffeine"). Total time: ~28 minutes. Strong senior signal.

---

## Transcript 3 — Sliding Window Maximum (Hard — 35–45 min)

**Setup:** *"Given an array `nums` and window size `k`, return the max of each window of size `k`."*

---

**Candidate**: Clarifying: **[phase: clarify]**

*What's the range on n? On k?*

**Interviewer**: `1 ≤ k ≤ n ≤ 10⁵`.

*Values fit in int?*

**Interviewer**: Yes.

*Return an array of length `n - k + 1`?*

**Interviewer**: Correct.

---

**Candidate**: Example: **[phase: examples]** `nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3`. Windows:

- `[1, 3, -1]` → max 3
- `[3, -1, -3]` → max 3
- `[-1, -3, 5]` → max 5
- `[-3, 5, 3]` → max 5
- `[5, 3, 6]` → max 6
- `[3, 6, 7]` → max 7

Output: `[3, 3, 5, 5, 6, 7]`.

---

**Candidate**: **Brute force:** for each of the `n - k + 1` windows, scan `k` elements — O(n·k). At `n = k = 10⁵` that's 10¹⁰ operations. Way too slow. **[phase: brute → optimize]**

**Second attempt: sorted structure.** A `TreeMap<Integer, Integer>` from value → count. Insert `a[right]`, remove `a[left]`, look up max via `lastKey()`. Each op is O(log k). Total: O(n log k). Better, and this works.

**Third attempt — can we get O(n)?** The insight: within a window, if a smaller element appears *before* a larger one, the smaller one can never be the max as long as the larger is in the window. So we can *discard* the smaller ones eagerly.

This gives a **monotonic decreasing deque** — front is the current max, back holds candidates that might become the max later.

**Interviewer**: Explain the deque invariant more concretely.

**Candidate**: The deque holds indices — not values — in decreasing order of the values they refer to. Front (`peekFirst`) is the index of the current window's max. When I slide:

1. **Add** the new right index: while the back of the deque points to a value ≤ `a[right]`, pop it. Then push `right`.
2. **Expire** the front: while `peekFirst() < right - k + 1`, poll it.
3. **Record** `a[peekFirst()]` as the current window's max.

Each index enters the deque once and leaves once → amortized O(1) per slide → O(n) total.

&gt; **What the interviewer sees:** Candidate walked up the ladder — brute → TreeMap → monotonic deque — with complexity analysis at each rung. That IS the senior thought process.

---

**Candidate**: **Coding.** **[phase: code]**



```java
public int[] maxSlidingWindow(int[] nums, int k) {
    int n = nums.length;
    int[] result = new int[n - k + 1];
    ArrayDeque<Integer> dq = new ArrayDeque<>();  // stores indices, front = max
    for (int right = 0; right < n; right++) {
        // 1. Add: pop from back while back is smaller
        while (!dq.isEmpty() && nums[dq.peekLast()] <= nums[right]) {
            dq.pollLast();
        }
        dq.offerLast(right);
        // 2. Expire: front out of window
        if (dq.peekFirst() < right - k + 1) {
            dq.pollFirst();
        }
        // 3. Record once window is full
        if (right >= k - 1) {
            result[right - k + 1] = nums[dq.peekFirst()];
        }
    }
    return result;
}
```



*Trace on `[1, 3, -1, -3, 5, 3, 6, 7], k = 3`:* **[phase: verify]**

| right | nums[right] | after pop | after push | expired? | record? | dq → values |
|---|---|---|---|---|---|---|
| 0 | 1 | dq=[] | dq=[0] | no | no | [1] |
| 1 | 3 | pop 0 (1≤3), dq=[] | dq=[1] | no | no | [3] |
| 2 | -1 | -1&lt;3, no pop | dq=[1,2] | no | yes → **3** | [3,-1] |
| 3 | -3 | -3&lt;-1, no pop | dq=[1,2,3] | 1&lt;3-3+1=1? no | yes → **3** | [3,-1,-3] |
| 4 | 5 | pop 3,2,1 all ≤5 | dq=[4] | no | yes → **5** | [5] |
| 5 | 3 | no pop | dq=[4,5] | no | yes → **5** | [5,3] |
| 6 | 6 | pop 5 (3≤6) | dq=[4,6] | 4&lt;4? no | yes → **6** but wait: peekFirst=4, and 4&lt;6-3+1=4 is false. **6** | [5,6] → but 5 got popped too. Let me re-check |

Hmm — let me re-do right=6:

- right=6, nums[6]=6. Back is index 5 (value 3). 3≤6, pop. Back is index 4 (value 5). 5≤6, pop. dq=[]. Push 6. dq=[6].
- Expire: peekFirst=6, 6 &lt; 6-3+1=4? No.
- Record: right≥k-1=2. result[6-3+1=4] = nums[6] = 6. ✓

right=7, nums[7]=7. Back=6 (value 6). 6≤7, pop. dq=[]. Push 7. dq=[7]. Record: result[5]=7. ✓

Final: `[3, 3, 5, 5, 6, 7]`. ✓

**Interviewer**: You had a small confusion at r=6. What happened?

**Candidate**: I forgot I already popped index 5 at r=6, so my trace got out of sync. That's exactly why I trace on paper — to catch my own bookkeeping errors. The code is correct; my trace narration was off.

**Interviewer**: What's the complexity now?

**Candidate**: Each index is pushed once and popped at most once → O(1) amortized per iteration → O(n) total. Space O(k) for the deque. This is optimal — you can't beat O(n) since you must output n-k+1 answers.

&gt; **What the interviewer sees:** Candidate caught their own trace error and named the meta-lesson ("that's why I trace"). Stayed calm, delivered optimal solution. Named optimality bound at the end. Total time: ~40 minutes. Hire.

---

## What these transcripts reveal — the 6 senior signals

Reading all three, the same signals appear:

1. **Clarify before coding.** Every one starts with 3–4 targeted questions.
2. **Examples before code.** Traced by hand.
3. **Brute force explicitly stated with complexity.** Not skipped.
4. **Multiple optimization ladders.** "The map works, but what if it's sorted? Two pointers."
5. **Trace after coding.** Caught bookkeeping errors.
6. **Handled follow-ups by comparing to real-world tools.** "I'd use Caffeine." Shows judgment.

Miss any three of these and you're a mid-level candidate no matter how correct your code is. Hit all six and you're staff-track — even if your code has minor bugs, because you'll debug them yourself in front of the interviewer.
