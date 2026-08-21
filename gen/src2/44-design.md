# Design &amp; Randomized

## Why design patterns exist — the story

A design interview question usually sounds like a tiny product requirement: "build a cache," "support random picks," "sample from a stream." The trap is that each operation wants a different superpower. A hash map finds a key in O(1), but it cannot tell you which item is least recent. An array gives O(1) random indexing, but deleting the middle leaves a hole. A linked list moves nodes in O(1), but cannot find the node without walking from the head. The pattern is to pair structures so each covers the other's weakness.

LRU Cache is the cleanest example. Suppose capacity is 2 and the calls are `put(1,A)`, `put(2,B)`, `get(1)`, `put(3,C)`. After the two puts, recency is `2 most recent → 1 least recent`. The `get(1)` must return `A` and also move key 1 to the front, so recency becomes `1 → 2`. Now `put(3,C)` evicts key 2, not key 1, because 2 is the least recently used. A `HashMap` alone can find `1`, but cannot reorder. A doubly linked list alone can reorder, but cannot find `1` quickly. Together, `map key→node` plus `list recency order` gives O(1) lookup, O(1) move-to-front, and O(1) tail eviction.

Randomized structures follow the same composition mindset. For `Insert Delete GetRandom O(1)`, an array gives uniform random index selection, while a map remembers where each value lives. For reservoir sampling, the "partner structure" is not another container but a probability invariant: after seeing `k` stream elements, your one stored sample must be uniform over those `k`. In all of these, name the invariant first; the implementation becomes bookkeeping.

> [key] **Key Insight** — Design questions are usually not about inventing a new data structure. They are about composing two familiar ones and keeping their invariants synchronized after every API call.

### Recognize by
- an API contract: `get`, `put`, `insert`, `remove`, `pick`, `getRandom`
- strict operation targets: "all operations O(1)," "average O(1)," "O(1) extra memory"
- one operation needs lookup while another needs ordering, random access, or eviction
- the input is a stream and you cannot store or revisit everything
- the interviewer asks what happens after a sequence of calls, not just for one input array

### When NOT to use it
- If operations do not need to persist state across calls, a plain algorithm may be simpler.
- If `O(log n)` is acceptable and ordering matters, `TreeMap`/`TreeSet` may reduce bug risk.
- If the data set is tiny, a list scan can be clearer than a delicate O(1) design.
- If deletion is arbitrary from a heap, remember Java `PriorityQueue.remove(x)` is O(n); add lazy deletion or use a different structure.
- If randomness must be cryptographically secure, `java.util.Random` is not the right tool.

## How to use it — LRU skeleton

The LRU cache skeleton has three moving parts: a map, a doubly linked list, and two dummy sentinels. Sentinels remove edge cases: every real node has both a previous and next node, even when it is logically first or last.

```java
class Node {
    int key, val;
    Node prev, next;
    Node(int key, int val) { this.key = key; this.val = val; }
}

Map<Integer, Node> map = new HashMap<>();
Node head = new Node(0, 0); // most-recent side sentinel
Node tail = new Node(0, 0); // least-recent side sentinel
// constructor links: head.next = tail; tail.prev = head;

void remove(Node n) {
    n.prev.next = n.next;
    n.next.prev = n.prev;
}

void addFirst(Node n) {
    n.next = head.next;
    n.prev = head;
    head.next.prev = n;
    head.next = n;
}
```

> [inv] **LRU invariant** — the map and list describe the same keys. The list order is most-recent near `head`, least-recent near `tail`; every successful `get` and every `put` of an existing key moves that node to the front.

---

## LRU Cache <span class="diff diff-m">Medium</span>

*[↗ LeetCode: LRU Cache](https://leetcode.com/problems/lru-cache/)* — **Medium**

### Problem

Design a cache with fixed capacity. `get(key)` returns the value or `-1`; `put(key, value)` inserts or updates. Whenever capacity is exceeded, evict the **least recently used** key. Both operations must be O(1).

**Example:** capacity 2; `put(1,1)`, `put(2,2)`, `get(1)`, `put(3,3)` evicts key 2.

**Example 1:** capacity 2: put(1,1), put(2,2), get(1) -> 1, put(3,3) evicts key 2.

**Example 2:** capacity 1: put(1,10), put(2,20), get(1) -> -1, get(2) -> 20.

### Solution — brute force

A simple implementation stores pairs in an array/list ordered by recency. On `get`, scan for the key, remove it, and append it at the front. On `put`, scan for the key, update or insert, and if capacity is exceeded remove the last item.

```text
get(k): scan list to find k; if found move entry to front
put(k,v): scan list; update/move if present; otherwise add front; trim tail
```

This is O(capacity) per call because the scan costs linear time. The optimized version replaces the scan with a map from key to the exact linked-list node.

### Solution — optimized

**Pattern:**
Hash map for direct key lookup; doubly linked list for recency order. The head side stores most-recent nodes, and the tail side stores the eviction candidate.

**Java:**
```java
class LRUCache {
    private static class Node {
        int key, value;
        Node prev, next;
        Node(int key, int value) { this.key = key; this.value = value; }
    }
    private final int capacity;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0), tail = new Node(0, 0);

    public LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) return -1;
        remove(node);
        addFirst(node);
        return node.value;
    }

    public void put(int key, int value) {
        Node node = map.get(key);
        if (node != null) {
            node.value = value;
            remove(node);
            addFirst(node);
            return;
        }
        Node fresh = new Node(key, value);
        map.put(key, fresh);
        addFirst(fresh);
        if (map.size() > capacity) {
            Node victim = tail.prev;
            remove(victim);
            map.remove(victim.key);
        }
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void addFirst(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
}
```

> [note] **Trace it** — Capacity 2. After `put(1,1), put(2,2)`, list is `2 → 1`. `get(1)` returns `1` and moves key 1 to the front: `1 → 2`. `put(3,3)` inserts `3 → 1 → 2`, then evicts `tail.prev`, which is key 2. The map removes key 2 at the same time.

### Time Complexity

O(1) average per get and put.

Original summary: Time O(1) for `get` and `put` · Space O(capacity).

### Space Complexity

O(capacity) for the map plus one linked-list node per cached key.

> [trap] **Common Trap** — Updating the map but not the list, or the list but not the map. *Example:* if `put(3,3)` evicts key 2 from the list but leaves `map.get(2)` pointing at the old node, a later `get(2)` returns a ghost value.

> [note] **Interview script** — "I need one structure for lookup and one for recency. The hash map gives key-to-node in O(1), and the doubly linked list lets me remove or move that exact node in O(1). I keep most recent next to the head and evict from the tail. Every operation updates both structures so the invariants stay aligned."

> [pat] **Pattern Connection** — LFU Cache adds frequency buckets; All O(1) Data Structure keeps buckets ordered by count. The recipe is the same: map to nodes, plus a linked structure that represents the ordering the map cannot provide.

### Learning notes

- Why doubly linked list, not singly? O(1) unlink from the middle after map lookup needs prev.
- Why dummy head/tail sentinels? They remove null-check edge cases.
- Why move on get? A read refreshes recency.
- Why store key in the node? Tail eviction must remove the exact map key.
- Why map key->node? The node is what gets moved in O(1).

#### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [LRU Cache](https://leetcode.com/problems/lru-cache/) | map key→node + recency list | O(1) |
| [LFU Cache](https://leetcode.com/problems/lfu-cache/) | map key→node plus frequency→linked-list buckets | O(1) |
| [All O(1) Data Structure](https://leetcode.com/problems/all-oone-data-structure/) | linked buckets ordered by count; keys move between buckets | O(1) |
| [Design Browser History](https://leetcode.com/problems/design-browser-history/) | pointer movement in a list/array; no hash map needed unless URLs are queried | O(1) |

## Insert Delete GetRandom O(1) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/)* — **Medium**

### Problem

Design a set supporting `insert`, `remove`, and **`getRandom`** (uniform over current elements) — all **average O(1)**. **Example:** `insert(1), insert(2), getRandom()` → 1 or 2 with equal probability; `remove(1), getRandom()` → always 2.

**Example 1:** insert(1), insert(2), getRandom() returns 1 or 2 with probability 1/2 each.

**Example 2:** insert(1), insert(2), remove(1), getRandom() always returns 2.

### Solution — brute force

A list-only design can append in O(1) and pick a random index in O(1), but `remove(v)` must scan to find `v`. A set-only design can insert/remove in O(1), but cannot choose a uniform random element by index.

```text
insert(v): if list does not contain v, append it
remove(v): scan list, remove matching value by shifting later values left
getRandom(): return list[random index]
```

The scan and shift make removal O(n). The optimized solution keeps the list but adds a map from value to index, then removes by swapping with the last element.

### Solution — optimized

**Pattern:**
A hash map alone can't do O(1) uniform random (you can't index a map); a dynamic array can't do O(1) delete of an arbitrary value. **Combine them:** array holds the values for random indexing; map holds `value → its index in the array`. To delete, **swap the victim with the last element** (O(1)), fix the moved element's index, then pop the tail.

> [inv] **Invariant** — `vals[map.get(v)] == v` for every present `v`, and `vals` has no gaps. The swap-with-last trick is the only way to delete from an array in O(1) while keeping it gap-free.

**Java:**
```java
class RandomizedSet {
    private final Map<Integer,Integer> idx = new HashMap<>();   // value -> index in vals
    private final List<Integer> vals = new ArrayList<>();
    private final Random rnd = new Random();

    public boolean insert(int v) {
        if (idx.containsKey(v)) return false;
        idx.put(v, vals.size());
        vals.add(v);
        return true;
    }
    public boolean remove(int v) {
        Integer i = idx.get(v);
        if (i == null) return false;
        int last = vals.get(vals.size() - 1);
        vals.set(i, last);           // move last element into the hole
        idx.put(last, i);            // fix its recorded index
        vals.remove(vals.size() - 1);
        idx.remove(v);
        return true;
    }
    public int getRandom() {
        return vals.get(rnd.nextInt(vals.size()));
    }
}
```

> [note] **Trace it** — `insert 3,7,9` → `vals=[3,7,9]`. `remove 3`: index of 3 is 0, last is 9, so write 9 into slot 0, update `idx{9:0, 7:1}`, pop the tail, and remove 3 from the map. `getRandom` now picks index 0 or 1 uniformly, so 9 and 7 each have probability 1/2.

### Time Complexity

O(1) average for insert, remove, and getRandom.

Original summary: Time O(1) average for all three ops · Space O(n).

### Space Complexity

O(n) for the value array and value-to-index map.

> [trap] **Common Trap** — Forgetting to update the moved element's index. *Example:* `insert 1,2,3` (`vals=[1,2,3]`, `idx={1:0,2:1,3:2}`). `remove(1)`: swap `vals[0]` with last (`3`) → `vals=[3,2]`. Without `idx.put(3, 0)`, a later `remove(3)` uses stale index `2` → wrong slot.

> [note] **Interview script** — "Uniform random needs an array because I can choose a random index. Fast delete needs a map because I need the value's index immediately. To delete without shifting, I move the last value into the removed slot, update that moved value's index, then pop the tail. The invariant is that the list has no gaps and the map always points to the current index."

> [pat] **Pattern Connection** — Same map+array skeleton solves *Insert Delete GetRandom — Duplicates allowed* (store a set of indices per value) and *Random Pick with Weight* (prefix sums + binary search). The broader "hash map + partner structure" recipe also underlies **LRU Cache** and **LFU Cache**.

### Learning notes

- Why ArrayList? Uniform random needs O(1) indexing.
- Why map value->index? Remove jumps directly to the victim slot.
- Why swap with last? It deletes without shifting.
- Why update the moved value's index? Its old index becomes stale immediately.
- Why average O(1)? HashMap operations are expected constant-time.

#### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) | map value→index + swap-with-last | O(1) |
| [… Duplicates allowed](https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed/) | map value→**set** of indices | O(1) avg |
| [LRU Cache](https://leetcode.com/problems/lru-cache/) | map + doubly-linked list for recency | O(1) |
| [Random Pick with Weight](https://leetcode.com/problems/random-pick-with-weight/) | prefix-sum array + binary search | O(log n) |

## Reservoir Sampling — uniform pick from a stream <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Linked List Random Node](https://leetcode.com/problems/linked-list-random-node/)* — **Medium**

### Problem

Return a uniformly random element from a sequence of **unknown or unbounded length**, seen once, using **O(1) extra memory**. **Example:** stream a linked list you can't index or re-read; each node must be returned with probability `1/n`.

**Example 1:** stream [10,20,30] returns each value with probability 1/3.

**Example 2:** A linked list of unknown length can be sampled in one pass without precomputing n.

### Solution — brute force

If the stream is actually a small linked list you can store, copy every value into an array and return a random index. That proves the desired distribution, but it violates the O(1) memory requirement and fails for unbounded streams.

```text
values = []
for each node in stream: values.add(node.val)
return values[random index from 0..values.size-1]
```

Reservoir sampling keeps only one value while preserving the same final probability.

### Solution — optimized

**Pattern:**
Keep the current pick. For the `k`-th element seen, replace the pick with it with probability `1/k`. By induction every element ends with probability `1/n` — no length needed up front.

> [inv] **Invariant** — after seeing `k` elements, the held sample is uniform over those `k`. Element `k` survives with prob `1/k`; an earlier one survives its own selection times all later non-replacements: `1/(k−1) · (k−1)/k = 1/k`.

**Java:**
```java
int getRandom(ListNode head) {
    ListNode cur = head;
    int result = head.val, count = 1;
    while (cur != null) {
        if (rnd.nextInt(count) == 0) result = cur.val;   // replace with prob 1/count
        count++;
        cur = cur.next;
    }
    return result;
}
```

> [note] **Trace it** — Three nodes `A,B,C`. `A` is chosen first. At `B`, replace with probability 1/2, so `A` and `B` are each 1/2 after two nodes. At `C`, replace with probability 1/3. `C` ends with 1/3; `A` keeps its earlier 1/2 chance and survives the final non-replacement with probability 2/3, so `A` ends at 1/3 too. Same for `B`.

### Time Complexity

O(n) for one pass over the stream or linked list.

Original summary: Time O(n) per sample · Space O(1) — no array of the stream needed.

### Space Complexity

O(1) auxiliary space for one sample and a counter.

> [trap] **Common Trap** — Sampling with the wrong probability. *Example:* if you replace with `rnd.nextInt(count-1) == 0` instead of `nextInt(count) == 0`, the k-th element has probability `1/(k-1)` (or the loop mis-fires at k=1). Off-by-one on the reservoir wrecks uniformity.

> [note] **Interview script** — "If I knew the length, I could pick a random index, but the stream length is unknown. I maintain one sample and, when I see the k-th item, I let it replace the sample with probability 1/k. That keeps the invariant that after k items, every item has probability 1/k. So I use constant space and one pass."

> [pat] **Pattern Connection** — Generalizes to **k samples** (keep a size-k reservoir; the `i`-th element joins with prob `k/i`, evicting a random current member) — powers *Random Pick Index* and big-data sampling. The **Fisher–Yates shuffle** is the mirror image: for an in-memory array, swap `a[i]` with a random `a[0..i]` to produce a uniform permutation in O(n).

### Learning notes

- Why probability 1/k? It preserves uniformity after k items.
- Why no length pre-pass? Streams may be unknown-length or non-rewindable.
- Why count in the random bound? Each seen item gets exactly one replacement chance.
- Why O(1) memory? The reservoir stores one sample.
- Why induction proof? Earlier samples survive later steps with the right product probability.

#### Same pattern, new tweaks

| Variation | The one thing that changes | Time · Space |
|---|---|---|
| [Linked List Random Node](https://leetcode.com/problems/linked-list-random-node/) | single reservoir of size 1 | O(n) · O(1) |
| [Random Pick Index](https://leetcode.com/problems/random-pick-index/) | reservoir over indices matching a target | O(n) · O(1) |
| [Shuffle an Array](https://leetcode.com/problems/shuffle-an-array/) | Fisher–Yates: swap i with random ≤ i | O(n) · O(1) |
| [Random Pick with Blacklist](https://leetcode.com/problems/random-pick-with-blacklist/) | remap blacklisted low indices to allowed high indices | O(1) pick |
