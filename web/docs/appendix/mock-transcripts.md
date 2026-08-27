# Mock Interview Transcripts

*The Interview Playbook (Ch. 01) described the 6-phase loop abstractly. This chapter shows what those phases sound like when a real senior candidate is speaking. Six transcripts — Easy, Medium (LRU / Coin Change / Merge Intervals / Islands), Hard — annotated with what the interviewer is grading at each point.*

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

<CodeTrace
  title="Transcript 1 — Two Sum verify: nums=[2,7,11,15], target=9"
  :values="[2,7,11,15]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { complement: 7, seen: "{}" }, note: "miss. put seen[2]=0" },
    { pointers: { i: 1 }, vars: { complement: 2, "seen[2]": 0 }, note: "HIT → return [0,1]", added: [0,1] }
  ]'
/>

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

<CodeTrace
  title="Transcript 2 — LRU Cache walkthrough, capacity=2"
  :values="['put 1,a','put 2,b','get 1','put 3,c','get 2']"
  :windowKeys="['op']"
  :cellWidth="70"
  :steps='[
    { pointers: { op: 0 }, vars: { list: "1", map: "{1}" }, note: "head=1", added: [0] },
    { pointers: { op: 1 }, vars: { list: "2 → 1", map: "{1,2}" }, note: "put 2 → head=2 (MRU)", added: [1] },
    { pointers: { op: 2 }, vars: { list: "1 → 2", ret: "a" }, note: "get(1) → move 1 to head", added: [2] },
    { pointers: { op: 3 }, vars: { list: "3 → 1", map: "{1,3}" }, note: "put 3 evicts LRU=2", added: [3] },
    { pointers: { op: 4 }, vars: { list: "3 → 1", ret: -1 }, note: "get(2) → -1 (evicted)" }
  ]'
/>

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

<CodeTrace
  title="Transcript 3 — Sliding Window Max: nums=[1,3,-1,-3,5,3,6,7], k=3"
  :values="[1,3,-1,-3,5,3,6,7]"
  :windowKeys="['left','right']"
  :cellWidth="34"
  :steps='[
    { pointers: { left: 0, right: 2 }, vars: { dq: "[1(idx),2]", output: "[3]" }, note: "first full window. front=3" },
    { pointers: { left: 1, right: 3 }, vars: { dq: "[1,2,3]", output: "[3,3]" }, note: "-3 pushes, front still 3" },
    { pointers: { left: 2, right: 4 }, vars: { dq: "[4(5)]", output: "[3,3,5]" }, note: "5 pops all smaller. front=5" },
    { pointers: { left: 3, right: 5 }, vars: { dq: "[4,5]", output: "[3,3,5,5]" }, note: "3 pushes below 5" },
    { pointers: { left: 5, right: 7 }, vars: { dq: "[7]", output: "[3,3,5,5,6,7]" }, note: "final: 7 dominates" }
  ]'
/>

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

## Transcript 4 — Coin Change (Medium DP — should take 25–35 min)

**Setup:** *"Given an integer array `coins` of denominations and an integer `amount`, return the fewest number of coins needed to make up `amount`. If it can't be made, return -1."*

---

**Candidate**: A few clarifying questions. **[phase: clarify]**

*Can I use each coin an unlimited number of times, or is it 0/1?*

**Interviewer**: Unlimited.

*Can `amount` be zero?*

**Interviewer**: Yes. Answer is 0 coins.

*What are the constraint sizes?*

**Interviewer**: `1 ≤ coins.length ≤ 12`, `1 ≤ amount ≤ 10⁴`, `1 ≤ coins[i] ≤ 2³¹−1`.

*Any negative amounts or coins?*

**Interviewer**: No, both positive.

---

**Candidate**: Let me trace two examples. **[phase: examples]** `coins=[1,2,5], amount=11` → I can do `5+5+1 = 3 coins`. `coins=[2], amount=3` → impossible → `-1`.

**Interviewer**: Correct.

---

**Candidate**: A common instinct is greedy — always pick the largest coin ≤ remaining. **[phase: brute]** But that's wrong for arbitrary denominations. `coins=[1,3,4], amount=6` — greedy takes `4+1+1=3 coins`, but optimal is `3+3=2 coins`. So greedy is out.

That means we need to explore. Brute force: recursive — `minCoins(a) = 1 + min(minCoins(a - c) for c in coins)`. That's exponential — for `amount = 10⁴` and coin `1`, the recursion depth alone is 10⁴, with branching 12 at each level. Won't finish in a lifetime.

But **subproblems repeat**: `minCoins(3)` is called from `minCoins(6)`, `minCoins(7)`, `minCoins(8)`, etc. Classic overlapping subproblems → memoize. **[phase: optimize]**

I'll do bottom-up DP. `dp[a]` = min coins to make amount `a`.
- `dp[0] = 0`.
- `dp[a] = 1 + min(dp[a - c] for c in coins if c ≤ a)`, or ∞ if unreachable.
- Answer: `dp[amount]`, or `-1` if it stayed ∞.

**Interviewer**: Complexity?

**Candidate**: Time O(amount · |coins|). For 10⁴ × 12 = 1.2·10⁵ ops — trivial. Space O(amount).

Alternative: BFS on amounts. Level = coin count, edges = coin subtractions. Same time, gives shortest-path semantics naturally. I'll code DP because it's shorter.

---

**Candidate**: Coding. **[phase: code]**



```java
int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);        // sentinel > any real answer
    dp[0] = 0;
    for (int a = 1; a <= amount; a++)
        for (int c : coins)
            if (c <= a) dp[a] = Math.min(dp[a], dp[a - c] + 1);
    return dp[amount] > amount ? -1 : dp[amount];
}
```



Two things I want to explain:
1. **Sentinel `amount + 1`** instead of `Integer.MAX_VALUE`. If I used `MAX_VALUE`, `dp[a-c] + 1` would overflow when unreachable. `amount + 1` is safe because a real answer never exceeds `amount` (all-ones case).
2. The outer loop is over amounts, not coins. Either direction works for unbounded knapsack. Ascending amounts, ascending coins — both fine.

---

**Candidate**: Trace on `coins=[1,2,5], amount=11`. **[phase: verify]**

`dp[0]=0`, `dp[1]=1` (via 1), `dp[2]=1` (via 2), `dp[3]=2` (1+2), `dp[4]=2` (2+2), `dp[5]=1` (5), … `dp[11]=3` (5+5+1). ✓

**Interviewer**: What if I asked you to return the actual coin sequence, not just the count?

**Candidate**: Store a parent array — `parent[a] = c` when `dp[a]` gets updated. Then walk back: start at `amount`, subtract `parent[a]`, repeat until 0. That reconstructs any *one* optimal sequence — not unique.

**Interviewer**: What if `amount` was 10⁹ but `|coins|` still small?

**Candidate**: DP is O(amount) — 10⁹ won't fit in memory. That's a matrix-exponentiation / number-theoretic territory. Or for the Frobenius-like case with just a few coins, closed-form after a threshold. If it's real interview scope, I'd say "this becomes a research problem and I'd flag it."

&gt; **What the interviewer sees:** Ruled out greedy with a concrete counter-example, chose DP for the right reason (overlapping subproblems), justified the sentinel value, handled both follow-ups without panic. Time: ~30 min. Strong hire.

---

## Transcript 5 — Merge Intervals (Medium — should take 20–30 min)

**Setup:** *"Given `intervals[][]` where each `intervals[i] = [start, end]`, merge all overlapping intervals and return the result."*

---

**Candidate**: Clarifying. **[phase: clarify]**

*Are intervals inclusive on both ends? So `[1,3]` and `[3,5]` — do they overlap?*

**Interviewer**: Yes, both endpoints inclusive, so `[1,3]` and `[3,5]` overlap → `[1,5]`.

*Is the input sorted?*

**Interviewer**: No. Assume unsorted.

*Sizes?*

**Interviewer**: `n ≤ 10⁴`.

*Can `start > end`? Or `start == end` (zero-length interval)?*

**Interviewer**: Guaranteed `start ≤ end`. Zero-length is valid.

---

**Candidate**: Two examples. **[phase: examples]** `[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`. `[[1,4],[4,5]]` → `[[1,5]]` (touching counts as overlapping per your definition).

---

**Candidate**: Brute force. **[phase: brute]** For each pair, check overlap; merge; restart. O(n³) or worse depending on how many merges cascade. Bad.

Observation: **if I sort by start, then two intervals overlap iff current.start ≤ prev.end**. That's the invariant. Sort → sweep once. **[phase: optimize]**

- Sort by `start` — O(n log n).
- Walk through. Keep a "current" interval. For each next: if it overlaps, extend `current.end = max(current.end, next.end)`. Else emit `current`, start fresh.
- At end, emit the last current.

**Interviewer**: Why is sorting by start sufficient? Why not by end?

**Candidate**: Because after sort-by-start, if `intervals[i].start > intervals[i-1].end`, then `intervals[i].start` also exceeds all *earlier* ends — because `intervals[i-1].end ≥ prev-merged.end` by our extension rule. So one prev pointer is enough. Sort-by-end would work for "min meeting rooms" but not for merge — you'd lose the start ordering.

&gt; **What the interviewer sees:** Candidate stated the invariant *before coding* and justified it against an alternative sort. That's the difference between "I've done this problem" and "I understand this problem."

---

**Candidate**: Coding. **[phase: code]**



```java
int[][] merge(int[][] intervals) {
    if (intervals.length == 0) return intervals;
    Arrays.sort(intervals, (a, b) -> a[0] - b[0]);       // stable enough here
    List<int[]> out = new ArrayList<>();
    int[] cur = intervals[0].clone();
    for (int i = 1; i < intervals.length; i++) {
        int[] nx = intervals[i];
        if (nx[0] <= cur[1]) cur[1] = Math.max(cur[1], nx[1]);   // overlap
        else { out.add(cur); cur = nx.clone(); }
    }
    out.add(cur);
    return out.toArray(new int[0][]);
}
```



Two nits I'd mention:
1. `a[0] - b[0]` is fine only if starts fit in int without overflow. For unbounded, use `Integer.compare(a[0], b[0])`.
2. Cloning `intervals[0]` protects against callers reusing the input array. Interview code — probably fine to skip, but I'd mention it.

---

**Candidate**: Trace `[[1,3],[2,6],[8,10],[15,18]]`. **[phase: verify]** Already sorted. `cur=[1,3]`, next `[2,6]`, overlap (`2 ≤ 3`) → `cur=[1,6]`. Next `[8,10]`, no overlap (`8 > 6`) → emit `[1,6]`, `cur=[8,10]`. Next `[15,18]`, no overlap → emit `[8,10]`, `cur=[15,18]`. Final emit `[15,18]`. Output `[[1,6],[8,10],[15,18]]`. ✓

**Interviewer**: What if the array is enormous — say `n = 10⁹`? Sorting is O(n log n) memory.

**Candidate**: Then intervals arrive as a stream and I'd use a **balanced BST keyed by start** (`TreeMap<Integer, Integer>` in Java). Insert `[s, e]`: find floor and ceiling in the map; merge overlapping; delete replaced entries; insert combined. Amortized O(log n) per insert. Total O(n log n) time, O(m) space where m is the number of surviving intervals — usually much smaller than n.

**Interviewer**: What if I also want to know the total length covered, not just merged intervals?

**Candidate**: Just accumulate `end - start` as I emit each merged interval. O(n) after the sort.

&gt; **What the interviewer sees:** Named the invariant, justified sort choice, offered a scalable follow-up (TreeMap) and a natural extension (total length). Time: ~25 min. Strong hire.

---

## Transcript 6 — Number of Islands (Medium graph — should take 20–30 min)

**Setup:** *"Given `grid[m][n]` of `'1'` (land) and `'0'` (water), return the number of connected islands. Diagonal cells don't connect."*

---

**Candidate**: Clarifying. **[phase: clarify]**

*Can I mutate the input grid, or should I preserve it?*

**Interviewer**: You can mutate it.

*Grid dimensions?*

**Interviewer**: `1 ≤ m, n ≤ 300`.

*Is the grid guaranteed rectangular?*

**Interviewer**: Yes.

*Just 4-directional adjacency, no diagonals — confirmed?*

**Interviewer**: Correct.

---

**Candidate**: Example. **[phase: examples]**



```
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```



Answer: 3 islands (top-left 4-cell blob, single `1` at `(2,2)`, right-bottom pair).

---

**Candidate**: Brute force is basically the answer here — this is the canonical flood-fill problem. **[phase: brute/optimize]** For every land cell we haven't visited, run a flood fill (DFS or BFS), mark all connected land as visited, increment counter.

- Time: each cell visited O(1) times → O(m·n) total. Optimal — you can't do less than looking at every cell to know if it's land.
- Space: DFS stack up to O(m·n) worst case (snake-shape island).

**Interviewer**: Any concern with DFS vs BFS?

**Candidate**: Recursive DFS in Java risks stack overflow at 300×300 = 90,000 cells in the worst case (single spiral island). Default JVM stack is ~512 KB, each frame ~64 bytes → maybe 8,000 frames. BFS with an explicit queue is safer. I'll use BFS.

Alternative: **Union-Find**. Iterate cells, union each land cell with its right and down land neighbours. Count roots. Same O(m·n·α) time. I'd only reach for this if the problem needed *dynamic* islands — e.g. addLand queries streaming in (that's Number of Islands II).

---

**Candidate**: Coding BFS. **[phase: code]**



```java
static final int[][] DIRS = {{-1,0},{1,0},{0,-1},{0,1}};

int numIslands(char[][] grid) {
    int m = grid.length, n = grid[0].length, count = 0;
    Deque<int[]> q = new ArrayDeque<>();
    for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) {
        if (grid[i][j] != '1') continue;
        count++;
        q.offer(new int[]{i, j});
        grid[i][j] = '0';                            // mark visited by mutation
        while (!q.isEmpty()) {
            int[] c = q.poll();
            for (int[] d : DIRS) {
                int ni = c[0] + d[0], nj = c[1] + d[1];
                if (ni < 0 || ni >= m || nj < 0 || nj >= n) continue;
                if (grid[ni][nj] != '1') continue;
                grid[ni][nj] = '0';                  // mark BEFORE enqueue
                q.offer(new int[]{ni, nj});
            }
        }
    }
    return count;
}
```



Critical detail: **mark visited before enqueue, not on dequeue.** If you mark on dequeue, the same cell gets enqueued 4× from its 4 neighbours — memory blows up. I've seen candidates fail this problem on runtime because of it.

---

**Candidate**: Trace on my earlier example. **[phase: verify]** Scan row 0: `(0,0)=1` → BFS marks all of the top-left 4-cell blob, count=1. Continue scanning, all `0`s until `(2,2)=1` → BFS marks it alone, count=2. Continue, `(3,3)=1` → BFS marks `(3,3)` and `(3,4)`, count=3. Return 3. ✓

**Interviewer**: What if the grid is 10⁶ × 10⁶ but sparse — 99.99% water?

**Candidate**: Then O(m·n) is 10¹² — dead. I'd change the data model: store only the coordinates of land cells in a HashSet&lt;Long&gt; keyed by `i·n + j`. Iterate the set; for each unvisited land cell BFS through its neighbours (also HashSet lookups). Time O(L) where L is land count. That's the sparse-graph trick.

**Interviewer**: What if you *can't* mutate the grid?

**Candidate**: Parallel `boolean[m][n] visited` array. O(m·n) extra space. Same time complexity.

**Interviewer**: How would Union-Find compare?

**Candidate**: Same worst-case complexity but higher constant factor and more code — no reason to prefer it here. Union-Find shines when the graph structure changes over time (add/remove land cells).

&gt; **What the interviewer sees:** Chose BFS over DFS with a stack-overflow justification, named the enqueue-time marking trap, gave two well-reasoned follow-ups (sparse via HashSet, immutable via visited array). Time: ~25 min. Strong hire.

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
