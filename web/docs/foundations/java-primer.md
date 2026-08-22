# Java Data Structures — A Visual Toolkit

Choosing the right structure is *most* of solving a problem: the correct container makes the algorithm obvious and the complexity fall out for free. This chapter is a behaviour-first tour of the Java structures you will actually reach for — how each one is laid out in memory, why its operations cost what they do, and the exact Java 17 calls for **access, search, insert, delete, and sort**. Later chapters assume this fluency.

<Callout kind="key" title="Mental model">

every structure is a trade. Arrays trade flexibility for O(1) indexing. Hash maps trade order and memory for O(1) lookup. Trees trade constant factors for *ordered* O(log n) queries. Heaps trade full ordering for a cheap *single* extreme. Pick the trade the problem rewards.

</Callout>

A one-line map from "what I need" to "what I use":

| I need… | Use | Why |
|---|---|---|
| Index by position, fixed size | `int[]` / array | contiguous memory → O(1) `a[i]` |
| Growable list, index access | `ArrayList` | array underneath + amortized O(1) append |
| Stack **or** queue | `ArrayDeque` | O(1) at both ends, no locking overhead |
| O(1) key→value lookup | `HashMap` / `HashSet` | hashing to a bucket |
| Lookup **and** insertion/LRU order | `LinkedHashMap` | hash + a doubly-linked order chain |
| Sorted keys, range / floor / ceiling | `TreeMap` / `TreeSet` | balanced BST, O(log n) ordered ops |
| Repeatedly take the min or max | `PriorityQueue` | binary heap, O(log n) push/pop |
| Prefix / dictionary queries | `Trie` (custom) | one node per character on a path |

---

## Array (`int[]`, `T[]`)

**What it is.** A fixed-length block of **contiguous** memory. Element `i` lives at address `base + i × elementSize`, so the CPU computes any position with one multiply-add — no traversal.





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 680 172" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <defs>
    <filter id="ar-s" x="-8%" y="-8%" width="116%" height="140%"><feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.5"/></filter>
  </defs>
  <rect x="0" y="0" width="680" height="172" fill="#fbfcfe"/>
  <text x="22" y="30" font-size="13" font-weight="700" fill="#2563eb">int[] a — one contiguous block of memory; any a[i] is instant</text>
  <g filter="url(#ar-s)">
    <rect x="40"  y="52" width="70" height="50" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="110" y="52" width="70" height="50" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="180" y="52" width="70" height="50" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="250" y="52" width="70" height="50" rx="7" fill="#eef5ff" stroke="#2563eb" stroke-width="2"/>
    <rect x="320" y="52" width="70" height="50" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  </g>
  <g font-size="19" font-weight="700" fill="#0b1220" text-anchor="middle">
    <text x="75" y="84">11</text><text x="145" y="84">4</text><text x="215" y="84">9</text>
    <text x="285" y="84">2</text><text x="355" y="84">7</text>
  </g>
  <g font-size="11" fill="#94a3b8" text-anchor="middle">
    <text x="75" y="120">0</text><text x="145" y="120">1</text><text x="215" y="120">2</text>
    <text x="285" y="120">3</text><text x="355" y="120">4</text>
  </g>
  <text x="215" y="146" text-anchor="middle" font-size="11" fill="#64748b">index</text>
  <line x1="40" y1="134" x2="390" y2="134" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3 3"/>
  <text x="215" y="164" text-anchor="middle" font-size="10.5" fill="#64748b">← contiguous: neighbours are adjacent in RAM → cache-friendly, but size is fixed ─→</text>
  <rect x="430" y="52" width="230" height="50" rx="8" fill="#eef5ff" stroke="#c7dbff"/>
  <text x="446" y="74" font-size="12.5" font-weight="700" fill="#0b1220">a[3] = base + 3 × 4 bytes</text>
  <text x="446" y="93" font-size="12" fill="#2563eb">one multiply-add → O(1), no scan</text>
</svg>
</div>




| Operation | Code | Cost | Why |
|---|---|---|---|
| Access | `a[i]` | O(1) | direct address arithmetic |
| Search (unsorted) | linear scan | O(n) | must inspect each element |
| Search (sorted) | `Arrays.binarySearch(a, x)` | O(log n) | halving on a monotone order |
| Insert / delete (middle) | shift elements | O(n) | everything after the gap must move |
| Sort | `Arrays.sort(a)` | O(n log n) | dual-pivot quicksort (primitives) |

<Callout kind="trap" title="Common Trap">

arrays can't grow: to append repeatedly, use `ArrayList`. And `Arrays.sort(int[])` is O(n²) on adversarial input and **not stable** — but *stable* is meaningless for raw `int`s anyway (two equal numbers are identical, so you could never tell whether their order changed). Stability only bites when you sort **objects** that carry extra fields beyond the sort key; there, use `Arrays.sort(Integer[])` / `Collections.sort` (stable Timsort). See the Sorting section for a worked example.

</Callout>

**Usage**


```java
int[] a = new int[5];              // [0, 0, 0, 0, 0]
a[0] = 11; a[1] = 4;               // set by index — O(1)
int x = a[0];                      // read — O(1)
int n = a.length;                  // 5  (length is a field, not a method!)
int[] b = {11, 4, 9, 2, 7};        // literal initialisation
Arrays.sort(b);                    // -> [2, 4, 7, 9, 11]
int idx = Arrays.binarySearch(b, 9);   // 3  (array must be sorted first)
for (int v : b) { /* visit v */ }
```



<Callout kind="def" title="Key terms">

<br/>**Contiguous:** stored as one unbroken block of memory, so element `i` sits at a fixed offset from the start — which is why indexing is a single address calculation, not a search.<br/>**Cache locality:** because neighbours sit next to each other in memory, reading one element pulls the next few into fast CPU cache, so scanning an array is much quicker than chasing pointers.<br/>**In-place:** an operation that rearranges the existing array without allocating a second one (O(1) extra space).<br/>**Stable sort:** a sort where elements that compare *equal* keep their original relative order. It matters only when items carry data beyond the sort key — e.g. sorting people by age, a stable sort leaves two 30-year-olds in the order you gave them; an unstable one may swap them.<br/>**Dual-pivot quicksort:** the primitive-array sort behind `Arrays.sort(int[])` — very fast, but not stable and O(n²) on adversarial input.

</Callout>

**Practice** — warm-ups to get fluent with the structure's API (no pattern insight needed; pattern-based problems come later in the book):

- [Running Sum of 1d Array](https://leetcode.com/problems/running-sum-of-1d-array/) — **Easy** — one pass carrying a running total
- [Build Array from Permutation](https://leetcode.com/problems/build-array-from-permutation/) — **Easy** — index into the array using its own values
- [Concatenation of Array](https://leetcode.com/problems/concatenation-of-array/) — **Easy** — allocate size `2n` and copy by index
- [Richest Customer Wealth](https://leetcode.com/problems/richest-customer-wealth/) — **Easy** — sum each row of a 2-D array
- [Find Numbers with Even Number of Digits](https://leetcode.com/problems/find-numbers-with-even-number-of-digits/) — **Easy** — plain iterate-and-count

## `ArrayList<T>` — the growable array

**What it is.** An array that **doubles** its backing store when full. Appends are O(1) *amortized*: most are a single write; occasionally a resize copies everything, but doublings are rare enough to average out.





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 680 212" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <defs><marker id="al-a" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#2563eb"/></marker></defs>
  <rect x="0" y="0" width="680" height="212" fill="#fbfcfe"/>
  <text x="22" y="28" font-size="13" font-weight="700" fill="#2563eb">ArrayList doubles its backing array when full → appends are O(1) amortized</text>
  <text x="22" y="58" font-size="11.5" font-weight="700" fill="#334155">size=4, cap=4 (full)</text>
  <g>
    <rect x="22"  y="66" width="40" height="38" rx="6" fill="#eef5ff" stroke="#2563eb"/>
    <rect x="62"  y="66" width="40" height="38" rx="6" fill="#eef5ff" stroke="#2563eb"/>
    <rect x="102" y="66" width="40" height="38" rx="6" fill="#eef5ff" stroke="#2563eb"/>
    <rect x="142" y="66" width="40" height="38" rx="6" fill="#eef5ff" stroke="#2563eb"/>
  </g>
  <g font-size="15" font-weight="700" fill="#0b1220" text-anchor="middle"><text x="42" y="91">a</text><text x="82" y="91">b</text><text x="122" y="91">c</text><text x="162" y="91">d</text></g>
  <line x1="196" y1="85" x2="248" y2="85" stroke="#2563eb" stroke-width="2" marker-end="url(#al-a)"/>
  <text x="222" y="76" font-size="10.5" fill="#dc2626" text-anchor="middle">add e → full!</text>
  <text x="222" y="100" font-size="10" fill="#64748b" text-anchor="middle">alloc cap 8, copy 4</text>
  <text x="262" y="58" font-size="11.5" font-weight="700" fill="#334155">cap=8 — next 3 adds are instant</text>
  <g>
    <rect x="262" y="66" width="40" height="38" rx="6" fill="#eef5ff" stroke="#2563eb"/>
    <rect x="302" y="66" width="40" height="38" rx="6" fill="#eef5ff" stroke="#2563eb"/>
    <rect x="342" y="66" width="40" height="38" rx="6" fill="#eef5ff" stroke="#2563eb"/>
    <rect x="382" y="66" width="40" height="38" rx="6" fill="#eef5ff" stroke="#2563eb"/>
    <rect x="422" y="66" width="40" height="38" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.8"/>
    <rect x="462" y="66" width="40" height="38" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-dasharray="3 3"/>
    <rect x="502" y="66" width="40" height="38" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-dasharray="3 3"/>
    <rect x="542" y="66" width="40" height="38" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-dasharray="3 3"/>
  </g>
  <g font-size="15" font-weight="700" fill="#0b1220" text-anchor="middle"><text x="282" y="91">a</text><text x="322" y="91">b</text><text x="362" y="91">c</text><text x="402" y="91">d</text><text x="442" y="91" fill="#16a34a">e</text></g>
  <rect x="22" y="132" width="620" height="60" rx="9" fill="#f6f8fb" stroke="#d9dee7"/>
  <text x="40" y="156" font-size="12" fill="#0b1220">Because capacity <tspan font-weight="700">doubles</tspan> (1, 2, 4, 8, …), resizes get exponentially rarer.</text>
  <text x="40" y="178" font-size="12" fill="#2563eb">Total copy work over n appends &lt; 2n → each add averages O(1) <tspan fill="#64748b">(that's "amortized")</tspan>.</text>
</svg>
</div>




| Operation | Code | Cost |
|---|---|---|
| Access | `list.get(i)` | O(1) |
| Search | `list.indexOf(x)` / `contains` | O(n) |
| Append | `list.add(x)` | O(1) amortized |
| Insert/delete at index | `list.add(i,x)` / `list.remove(i)` | O(n) (shift) |
| Sort | `list.sort(cmp)` / `Collections.sort(list)` | O(n log n), **stable** |

<Callout kind="note" title="Why append is O(1) amortized, not O(1) worst-case">

a single `add` that triggers a resize is O(n), but because capacity doubles, resizes happen at sizes 1,2,4,8,… so total copy work over `n` appends is `1+2+4+…+n < 2n`.

</Callout>

**Usage**


```java
List<Integer> l = new ArrayList<>();   // declare to the List interface
l.add(10);                 // append          -> [10]
l.add(20);                 //                 -> [10, 20]
l.add(1, 15);              // insert at index -> [10, 15, 20]
int first = l.get(0);      // 10
l.set(0, 99);              //                 -> [99, 15, 20]
l.remove(0);               // remove by index -> [15, 20]
l.remove(Integer.valueOf(15));  // remove by VALUE (not index!)
boolean has = l.contains(20);
int size = l.size();
for (int v : l) { /* visit v */ }
```



**Iterating**


```java
for (int i = 0; i < l.size(); i++) { int x = l.get(i); }   // classic index loop
for (int x : l) { /* ... */ }                              // enhanced for-each
l.forEach(x -> { /* ... */ });                             // lambda
Iterator<Integer> it = l.iterator();                       // explicit iterator
while (it.hasNext()) { int x = it.next(); if (drop) it.remove(); }  // SAFE delete mid-loop
ListIterator<Integer> back = l.listIterator(l.size());
while (back.hasPrevious()) { int x = back.previous(); }    // walk BACKWARD
```



<Callout kind="trap" title="ConcurrentModificationException">

never `l.remove(...)` (the list method) inside a for-each loop; it corrupts the iterator and throws. To delete while iterating, use `it.remove()` or `l.removeIf(x -> drop(x))`.

</Callout>

<Callout kind="def" title="Key terms">

<br/>**Amortized O(1):** the *average* cost per operation over a long run, even though a rare single operation (a resize) is expensive; averaged out, appends behave like O(1).<br/>**Dynamic (growable) array:** an array that reallocates a larger backing store when it fills.<br/>**Capacity vs size:** *size* is how many elements you've added; *capacity* is how many the backing array can hold before it must grow.<br/>**Geometric doubling:** growing capacity by a constant factor (×2) so resizes get exponentially rarer.<br/>**Timsort:** Java's stable, adaptive sort for object arrays and lists.

</Callout>

**Practice** — warm-ups for the growable-list API (no pattern insight needed; pattern-based problems come later):

- [Create Target Array in the Given Order](https://leetcode.com/problems/create-target-array-in-the-given-order/) — **Easy** — `add(index, value)` insertions
- [Kids With the Greatest Number of Candies](https://leetcode.com/problems/kids-with-the-greatest-number-of-candies/) — **Easy** — build a `List<Boolean>` in one pass
- [Shuffle the Array](https://leetcode.com/problems/shuffle-the-array/) — **Easy** — interleave into a new list by index
- [Number of Good Pairs](https://leetcode.com/problems/number-of-good-pairs/) — **Easy** — simple double loop over the list

## `ArrayDeque<T>` — stack and queue in one

**What it is.** A **ring (circular) buffer**: a backing array with `head` and `tail` indices that wrap around modulo capacity. Adding/removing at *either* end just moves a pointer → O(1). This is the modern replacement for both the legacy `Stack` and `LinkedList`-as-queue.





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 680 232" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <defs>
    <marker id="dq-b" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#2563eb"/></marker>
    <marker id="dq-r" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#dc2626"/></marker>
  </defs>
  <rect x="0" y="0" width="680" height="232" fill="#fbfcfe"/>
  <text x="22" y="28" font-size="13" font-weight="700" fill="#2563eb">ArrayDeque = a ring buffer — head/tail indices wrap around (mod 8)</text>
  <!-- ring of 8 slots, center (150,124) r=66 -->
  <g stroke-width="1.6">
    <circle cx="150" cy="58"  r="21" fill="#eef5ff" stroke="#2563eb"/>
    <circle cx="197" cy="77"  r="21" fill="#eef5ff" stroke="#2563eb"/>
    <circle cx="216" cy="124" r="21" fill="#f1f5f9" stroke="#cbd5e1"/>
    <circle cx="197" cy="171" r="21" fill="#f1f5f9" stroke="#cbd5e1"/>
    <circle cx="150" cy="190" r="21" fill="#f1f5f9" stroke="#cbd5e1"/>
    <circle cx="103" cy="171" r="21" fill="#f1f5f9" stroke="#cbd5e1"/>
    <circle cx="84"  cy="124" r="21" fill="#eef5ff" stroke="#2563eb"/>
    <circle cx="103" cy="77"  r="21" fill="#eef5ff" stroke="#2563eb"/>
  </g>
  <g font-size="16" font-weight="700" fill="#0b1220" text-anchor="middle">
    <text x="150" y="64">c</text><text x="197" y="83">d</text>
    <text x="84"  y="130">a</text><text x="103" y="83">b</text>
  </g>
  <g font-size="10" fill="#94a3b8" text-anchor="middle">
    <text x="150" y="34">0</text><text x="221" y="53">1</text><text x="245" y="128">2</text>
    <text x="221" y="196">3</text><text x="150" y="219">4</text><text x="79" y="196">5</text>
    <text x="52" y="128">6</text><text x="79" y="53">7</text>
  </g>
  <!-- head + tail pointers -->
  <text x="34" y="118" font-size="12" font-weight="700" fill="#2563eb" text-anchor="end">head</text>
  <line x1="36" y1="122" x2="61" y2="124" stroke="#2563eb" stroke-width="2" marker-end="url(#dq-b)"/>
  <text x="266" y="120" font-size="12" font-weight="700" fill="#dc2626">tail</text>
  <line x1="264" y1="124" x2="239" y2="124" stroke="#dc2626" stroke-width="2" marker-end="url(#dq-r)"/>
  <rect x="330" y="52" width="330" height="140" rx="9" fill="#f6f8fb" stroke="#d9dee7"/>
  <text x="348" y="78" font-size="12.5" font-weight="700" fill="#0b1220">Logical order: a → b → c → d</text>
  <text x="348" y="102" font-size="12" fill="#16a34a">poll() / pop() — remove from <tspan font-weight="700">head</tspan></text>
  <text x="348" y="124" font-size="12" fill="#dc2626">offer() / offerLast() — add at <tspan font-weight="700">tail</tspan></text>
  <text x="348" y="146" font-size="12" fill="#334155">push() / offerFirst() — add at head (stack top)</text>
  <text x="348" y="172" font-size="11.5" fill="#2563eb">every end operation just moves a pointer → O(1)</text>
</svg>
</div>




| Use as | Push | Pop / peek |
|---|---|---|
| **Stack** (LIFO) | `push(x)` / `offerFirst` | `pop()` / `peek()` |
| **Queue** (FIFO) | `offer(x)` / `offerLast` | `poll()` / `peek()` |
| Either end | `offerFirst/Last` | `pollFirst/Last`, `peekFirst/Last` |

<Callout kind="trap" title="Common Trap">

do **not** use `java.util.Stack` (synchronized, exposes indexing, iterates bottom-to-top) or `LinkedList` as a deque (pointer chasing, cache-unfriendly). `ArrayDeque` is faster and the interview-idiomatic choice. It rejects `null` elements — use a sentinel if you need "empty" markers.

</Callout>

**Usage — as a Stack (LIFO)**


```java
Deque<Integer> stack = new ArrayDeque<>();   // this is your stack
stack.push(1);              // -> [1]
stack.push(2);              // top is 2 -> [2, 1]
int top = stack.peek();     // 2   (look without removing)
int popped = stack.pop();   // 2   -> [1]
boolean empty = stack.isEmpty();
```



**Usage — as a Queue (FIFO)**


```java
Queue<Integer> queue = new ArrayDeque<>();   // this is your queue
queue.offer(1);             // enqueue -> [1]
queue.offer(2);             //         -> [1, 2]
int front = queue.peek();   // 1   (front, without removing)
int out = queue.poll();     // 1   dequeue -> [2]
// (poll/peek return null when empty; pop/element throw instead)
```



**Operations explained.** A `Deque` gives you *two families* of methods for every action — one that returns a sentinel on failure, one that throws:

| Action | Safe (null / false) | Throwing | What it actually does |
|---|---|---|---|
| add to head | `offerFirst(x)` | `addFirst(x)` / `push(x)` | put `x` at the **front** (a stack's top) |
| add to tail | `offer(x)` / `offerLast(x)` | `addLast(x)` | put `x` at the **back** (a queue's end) |
| remove head | `poll()` / `pollFirst()` | `pop()` / `removeFirst()` | **remove** the front and return it |
| remove tail | `pollLast()` | `removeLast()` | remove the back and return it |
| look at head | `peek()` / `peekFirst()` | `element()` / `getFirst()` | **read** the front, leave it in place |
| look at tail | `peekLast()` | `getLast()` | read the back |
| by value | `remove(x)` / `contains(x)` | — | delete / find a specific element (O(n)) |
| size | `size()` / `isEmpty()` | — | count / emptiness |

- **`peek`** = "show me the front but *don't* remove it." **`poll`/`pop`** = "remove the front and hand it to me." **`offer`/`push`** = "add one."
- **`offerFirst`** adds to the head, **`offerLast`** (= `offer`) adds to the tail — the difference only matters when you use *both* ends.
- The **null-returning** family (`offer`/`poll`/`peek`) is safe in loops; the **throwing** family (`add`/`remove`/`element`/`getFirst`) fails loudly on an empty deque — use it when "empty" would be a bug.

<Callout kind="key" title="What you actually need">

for a **stack**: `push`, `pop`, `peek`, `isEmpty`. For a **queue**: `offer`, `poll`, `peek`, `isEmpty`. Those eight methods cover ~90% of interview usage; the `First`/`Last` variants only come up when you genuinely work both ends (e.g. a monotonic deque).

</Callout>

**Iterating**


```java
for (int x : dq) { /* head → tail */ }
Iterator<Integer> it   = dq.iterator();             // head → tail (explicit)
Iterator<Integer> back = dq.descendingIterator();   // tail → head
while (!dq.isEmpty()) { int x = dq.poll(); }        // DRAINS it (destructive)
```



<Callout kind="def" title="Key terms">

<br/>**Deque** ("deck", double-ended queue): a sequence you can push/pop at *both* ends.<br/>**Ring / circular buffer:** a fixed array used as if its two ends were joined in a circle; `head` and `tail` indices wrap around with modulo, so neither end ever has to shift elements.<br/>**LIFO** (Last-In-First-Out): the most recent item leaves first — a **stack**.<br/>**FIFO** (First-In-First-Out): the oldest item leaves first — a **queue**.<br/>**Sentinel:** a placeholder/marker value that stands in for "nothing here"; needed because `ArrayDeque` forbids `null`.<br/>**Head / tail:** the front and back positions of the deque.

</Callout>

**Practice** — warm-ups for the stack/queue API (no pattern insight needed; pattern-based problems come later):

- [Baseball Game](https://leetcode.com/problems/baseball-game/) — **Easy** — push / pop / peek on a stack
- [Number of Recent Calls](https://leetcode.com/problems/number-of-recent-calls/) — **Easy** — enqueue, then drop stale front elements (queue)
- [Implement Stack using Queues](https://leetcode.com/problems/implement-stack-using-queues/) — **Easy** — build a stack from queue ops
- [Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) — **Easy** — build a queue from stack ops
- [Design Circular Queue](https://leetcode.com/problems/design-circular-queue/) — **Medium** — head/tail wrap-around, the ring buffer itself

## Linked list (nodes, and Java's `LinkedList`)

**What it is.** A chain of nodes, each holding a value and a reference to the next (and, for doubly-linked, the previous). There is **no** index arithmetic — reaching position `i` means walking `i` links.





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 680 176" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <defs>
    <marker id="ll-a" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#2563eb"/></marker>
    <filter id="ll-s" x="-8%" y="-8%" width="116%" height="150%"><feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.5"/></filter>
  </defs>
  <rect x="0" y="0" width="680" height="176" fill="#fbfcfe"/>
  <text x="22" y="28" font-size="13" font-weight="700" fill="#2563eb">Linked list — each node stores a value + a link to the next</text>
  <text x="40" y="58" font-size="12" font-weight="700" fill="#16a34a">head</text>
  <line x1="52" y1="64" x2="52" y2="86" stroke="#16a34a" stroke-width="2" marker-end="url(#ll-a)"/>
  <g filter="url(#ll-s)">
    <g><rect x="40"  y="90" width="46" height="42" rx="7" fill="#eef5ff" stroke="#2563eb" stroke-width="1.6"/><rect x="86"  y="90" width="26" height="42" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/></g>
    <g><rect x="182" y="90" width="46" height="42" rx="7" fill="#eef5ff" stroke="#2563eb" stroke-width="1.6"/><rect x="228" y="90" width="26" height="42" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/></g>
    <g><rect x="324" y="90" width="46" height="42" rx="7" fill="#eef5ff" stroke="#2563eb" stroke-width="1.6"/><rect x="370" y="90" width="26" height="42" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/></g>
    <g><rect x="466" y="90" width="46" height="42" rx="7" fill="#eef5ff" stroke="#2563eb" stroke-width="1.6"/><rect x="512" y="90" width="26" height="42" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.4"/></g>
  </g>
  <g font-size="18" font-weight="700" fill="#0b1220" text-anchor="middle">
    <text x="63" y="118">11</text><text x="205" y="118">4</text><text x="347" y="118">9</text><text x="489" y="118">2</text>
  </g>
  <g stroke="#2563eb" stroke-width="2">
    <line x1="99" y1="111" x2="176" y2="111" marker-end="url(#ll-a)"/>
    <line x1="241" y1="111" x2="318" y2="111" marker-end="url(#ll-a)"/>
    <line x1="383" y1="111" x2="460" y2="111" marker-end="url(#ll-a)"/>
  </g>
  <text x="525" y="116" font-size="15" fill="#dc2626">⏚</text>
  <text x="551" y="116" font-size="11" fill="#dc2626">null</text>
  <text x="40"  y="158" font-size="11" fill="#64748b">reach index i → walk i links (O(n))</text>
  <text x="360" y="158" font-size="11" fill="#16a34a">but given a node, splice = relink neighbours (O(1))</text>
</svg>
</div>




| Operation | Cost | Note |
|---|---|---|
| Access / search | O(n) | must traverse from head |
| Insert / delete **given the node** | O(1) | just relink pointers |
| Insert / delete **at index i** | O(n) | O(n) to *find* i, then O(1) to relink |

<Callout kind="note" title="When a linked list wins">

O(1) splicing when you already hold the node (e.g. an LRU cache's doubly-linked list), or building sequences with no random access. For almost everything else, `ArrayList`/`ArrayDeque` are faster due to cache locality. Interview linked-list problems are about **pointer discipline** (see the Linked Lists chapter), not about `java.util.LinkedList`.

</Callout>

**Usage**


```java
LinkedList<Integer> ll = new LinkedList<>();   // rarely needed; ArrayDeque usually wins
ll.addLast(1);              // -> [1]
ll.addFirst(0);             // -> [0, 1]
ll.removeFirst();           // -> [1]

// What interview problems actually use — a hand-rolled node:
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode head = new ListNode(1);
head.next = new ListNode(2);          // builds 1 -> 2
```



<Callout kind="def" title="Key terms">

<br/>**Node:** a small object holding a value plus a **reference** (link) to the next node — and, in a *doubly*-linked list, the previous one too.<br/>**Reference / pointer:** the handle by which one node addresses another.<br/>**Singly vs doubly linked:** singly has only `next`; doubly adds `prev`, enabling backward walks and O(1) deletion when you already hold the node.<br/>**Splice:** insert or remove a node by re-pointing its neighbours' links, leaving all other nodes untouched.<br/>**Dummy / sentinel node:** a throwaway node placed before the real head so edge cases (empty list, deleting the first node) need no special-casing.

</Callout>

**Practice** — warm-ups for pointer/traversal mechanics (no pattern insight needed; pattern-based problems come later):

- [Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) — **Easy** — walk the list and stop at the middle
- [Remove Linked List Elements](https://leetcode.com/problems/remove-linked-list-elements/) — **Easy** — splice out nodes using a dummy head
- [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) — **Easy** — relink nodes one at a time behind a dummy head
- [Design Linked List](https://leetcode.com/problems/design-linked-list/) — **Medium** — implement get / addAtHead / addAtTail / deleteAtIndex yourself
- [Delete Node in a Linked List](https://leetcode.com/problems/delete-node-in-a-linked-list/) — **Medium** — the copy-the-next-node trick

## `HashMap<K,V>` / `HashSet<E>`

**What it is.** A bucket array indexed by `hash(key)`. A good hash spreads keys evenly, so lookup is O(1) *average*. Collisions (two keys landing in the same bucket) form a short chain; Java 8+ converts a long chain into a balanced tree, capping the worst case at O(log n) per bucket.





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 680 212" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <defs><marker id="hm-a" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#2563eb"/></marker></defs>
  <rect x="0" y="0" width="680" height="212" fill="#fbfcfe"/>
  <text x="22" y="28" font-size="13" font-weight="700" fill="#2563eb">HashMap — hash(key) picks a bucket; keys that collide chain together</text>
  <rect x="26" y="86" width="94" height="40" rx="8" fill="#eef5ff" stroke="#2563eb" stroke-width="1.6"/>
  <text x="73" y="111" font-size="14" font-weight="700" fill="#0b1220" text-anchor="middle">key "cat"</text>
  <line x1="122" y1="106" x2="184" y2="106" stroke="#2563eb" stroke-width="2" marker-end="url(#hm-a)"/>
  <text x="153" y="98" font-size="10" fill="#64748b" text-anchor="middle">hash % cap</text>
  <!-- buckets -->
  <g font-size="12.5" fill="#475569">
    <rect x="190" y="56" width="150" height="30" rx="5" fill="#f1f5f9" stroke="#cbd5e1"/><text x="204" y="76">0:  —</text>
    <rect x="190" y="90" width="150" height="30" rx="5" fill="#f1f5f9" stroke="#cbd5e1"/><text x="204" y="110">1:  (dog, 3)</text>
    <rect x="190" y="124" width="150" height="30" rx="5" fill="#fef9ec" stroke="#e0a52b" stroke-width="1.6"/><text x="204" y="144" fill="#0b1220" font-weight="700">2:  ●</text>
    <rect x="190" y="158" width="150" height="30" rx="5" fill="#f1f5f9" stroke="#cbd5e1"/><text x="204" y="178">3:  —</text>
  </g>
  <text x="240" y="48" font-size="10.5" fill="#64748b">buckets</text>
  <!-- chain in bucket 2 -->
  <rect x="378" y="122" width="110" height="34" rx="7" fill="#fff" stroke="#e0a52b" stroke-width="1.6"/>
  <text x="433" y="144" font-size="12.5" font-weight="700" fill="#0b1220" text-anchor="middle">(cat, 7)</text>
  <rect x="520" y="122" width="110" height="34" rx="7" fill="#fff" stroke="#e0a52b" stroke-width="1.6"/>
  <text x="575" y="144" font-size="12.5" font-weight="700" fill="#0b1220" text-anchor="middle">(car, 9)</text>
  <line x1="340" y1="139" x2="374" y2="139" stroke="#e0a52b" stroke-width="2" marker-end="url(#hm-a)"/>
  <line x1="488" y1="139" x2="516" y2="139" stroke="#e0a52b" stroke-width="2" marker-end="url(#hm-a)"/>
  <text x="504" y="112" font-size="10.5" fill="#d97706" text-anchor="middle">collision → chain</text>
  <text x="26" y="204" font-size="11" fill="#64748b">Even spread → O(1). Adversarial pile-up → O(n), which Java caps by <tspan fill="#2563eb" font-weight="700">treeifying</tspan> a long chain to O(log n).</text>
</svg>
</div>




| Operation | Code | Cost (avg / worst) |
|---|---|---|
| Insert / update | `map.put(k,v)` | O(1) / O(log n) |
| Lookup | `map.get(k)` / `containsKey` | O(1) / O(log n) |
| Delete | `map.remove(k)` | O(1) / O(log n) |
| Iterate | `for (var e : map.entrySet())` | O(n), **no order guarantee** |

Idiomatic Java 17 helpers you will use constantly:



```java
Map<String,Integer> freq = new HashMap<>();
for (String w : words) freq.merge(w, 1, Integer::sum);        // count occurrences
int c = freq.getOrDefault("cat", 0);                          // default if absent
freq.computeIfAbsent("dogs", k -> 0);                         // init-then-use
map.putIfAbsent(k, v);
```



<Callout kind="trap" title="Common Trap">

keys must have consistent `hashCode`/`equals`. Mutable keys (e.g. a `List` or array you later modify) corrupt the map. Arrays use identity hashing — never use `int[]` as a key; build a canonical `String` or a small wrapper **class** (with proper `hashCode`/`equals`) instead.

</Callout>

**Usage — HashMap & HashSet**


```java
Map<String,Integer> map = new HashMap<>();
map.put("a", 1);                    // insert / overwrite
int v = map.get("a");               // 1   (returns null if absent — NPE on unbox!)
int d = map.getOrDefault("z", 0);   // 0   (safe default)
map.merge("a", 1, Integer::sum);    // "a" -> 2   (the counting idiom)
map.computeIfAbsent("g", k -> 0);   // init the slot if missing, then use it
boolean has = map.containsKey("a");
map.remove("a");
for (Map.Entry<String,Integer> e : map.entrySet()) { e.getKey(); e.getValue(); }

Set<Integer> set = new HashSet<>();
set.add(5);                         // -> {5}
boolean in = set.contains(5);       // true
set.remove(5);
set.addAll(List.of(1, 2, 3));       // bulk add
```



**Iterating** (order is **not** guaranteed for `HashMap`/`HashSet`)


```java
for (Map.Entry<String,Integer> e : map.entrySet()) { e.getKey(); e.getValue(); }  // key+value
for (String k : map.keySet())   { /* keys   */ }
for (int v    : map.values())   { /* values */ }
map.forEach((k, v) -> { /* ... */ });                    // lambda
var it = map.entrySet().iterator();                      // safe delete while iterating
while (it.hasNext()) { var e = it.next(); if (drop(e)) it.remove(); }

for (int x : set) { /* HashSet — any order */ }
```



<Callout kind="def" title="Key terms">

<br/>**Hash function:** turns a key into an integer (`hashCode()`).<br/>**Bucket:** one slot of the backing array; the key's hash mod capacity picks which bucket.<br/>**Collision:** two keys landing in the same bucket.<br/>**Chaining:** storing colliding keys together as a short list (or, once long, a balanced tree) inside that bucket.<br/>**Load factor:** the fill ratio (size ÷ capacity, default 0.75) that triggers a **resize** when exceeded.<br/>**Treeify:** Java 8+ converting an over-long collision chain into a red–black tree so the worst case is O(log n) instead of O(n).<br/>**Identity hashing:** hashing by object reference instead of contents — the reason mutable arrays make broken keys.

</Callout>

**Practice** — warm-ups for the map/set API (no pattern insight needed; pattern-based problems come later):

- [Design HashMap](https://leetcode.com/problems/design-hashmap/) — **Easy** — implement put / get / remove with buckets
- [Design HashSet](https://leetcode.com/problems/design-hashset/) — **Easy** — add / contains / remove
- [Jewels and Stones](https://leetcode.com/problems/jewels-and-stones/) — **Easy** — put items in a set, then membership-test each
- [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) — **Easy** — add to a set, detect the first repeat
- [Ransom Note](https://leetcode.com/problems/ransom-note/) — **Easy** — count letters in a map, then decrement

## `LinkedHashMap<K,V>` — hashing that remembers order

**What it is.** A `HashMap` plus a doubly-linked list threading all entries in **insertion order** (or **access order** if constructed that way). Same O(1) operations, but iteration is ordered — and access-order mode gives you an **LRU cache** almost for free.





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 680 196" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <defs>
    <marker id="lh-a" markerWidth="8" markerHeight="8" refX="4.5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#7c3aed"/></marker>
  </defs>
  <rect x="0" y="0" width="680" height="196" fill="#fbfcfe"/>
  <text x="22" y="28" font-size="13" font-weight="700" fill="#2563eb">LinkedHashMap = HashMap buckets + a doubly-linked order chain</text>
  <text x="40" y="60" font-size="11.5" font-weight="700" fill="#334155">buckets — O(1) lookup</text>
  <g>
    <rect x="40" y="72" width="150" height="26" rx="5" fill="#f1f5f9" stroke="#cbd5e1"/>
    <rect x="40" y="102" width="150" height="26" rx="5" fill="#f1f5f9" stroke="#cbd5e1"/>
    <rect x="40" y="132" width="150" height="26" rx="5" fill="#f1f5f9" stroke="#cbd5e1"/>
  </g>
  <g font-size="12" fill="#475569">
    <text x="52" y="90">0: (a) </text><text x="52" y="120">1: (c)</text><text x="52" y="150">2: (b)</text>
  </g>
  <text x="250" y="60" font-size="11.5" font-weight="700" fill="#334155">order chain — predictable iteration / recency</text>
  <g font-weight="700">
    <rect x="300" y="96" width="42" height="38" rx="8" fill="#f3f0fc" stroke="#7c3aed" stroke-width="1.6"/>
    <rect x="392" y="96" width="42" height="38" rx="8" fill="#f3f0fc" stroke="#7c3aed" stroke-width="1.6"/>
    <rect x="484" y="96" width="42" height="38" rx="8" fill="#f3f0fc" stroke="#7c3aed" stroke-width="1.6"/>
  </g>
  <g font-size="16" font-weight="700" fill="#0b1220" text-anchor="middle">
    <text x="321" y="121">a</text><text x="413" y="121">b</text><text x="505" y="121">c</text>
  </g>
  <g stroke="#7c3aed" stroke-width="1.8">
    <line x1="344" y1="108" x2="388" y2="108" marker-end="url(#lh-a)"/>
    <line x1="390" y1="122" x2="346" y2="122" marker-end="url(#lh-a)"/>
    <line x1="436" y1="108" x2="480" y2="108" marker-end="url(#lh-a)"/>
    <line x1="482" y1="122" x2="438" y2="122" marker-end="url(#lh-a)"/>
  </g>
  <text x="255" y="121" font-size="11" font-weight="700" fill="#7c3aed">head</text>
  <text x="536" y="121" font-size="11" font-weight="700" fill="#7c3aed">tail</text>
  <text x="300" y="156" font-size="10.5" fill="#dc2626">least-recently-used (evict here)</text>
  <text x="470" y="156" font-size="10.5" fill="#16a34a">most-recently-used</text>
  <text x="40" y="184" font-size="11" fill="#64748b">Access-order mode moves a touched key to the tail on every get/put → an LRU cache for free.</text>
</svg>
</div>






```java
// LRU cache in ~4 lines: access-order + capacity eviction
new LinkedHashMap<Integer,Integer>(16, 0.75f, true) {
    protected boolean removeEldestEntry(Map.Entry<Integer,Integer> e) { return size() > CAP; }
};
```



**Usage**


```java
Map<String,Integer> m = new LinkedHashMap<>();   // iterates in INSERTION order
m.put("b", 2); m.put("a", 1); m.put("c", 3);
for (var e : m.entrySet()) { /* visits b, a, c — the order you inserted */ }
// same put/get/getOrDefault/merge API as HashMap; only the iteration order differs
```



<Callout kind="def" title="Key terms">

<br/>**Insertion order:** entries iterate in the order you added them (the default).<br/>**Access order:** entries reorder on every `get`/`put` so the most-recently-used moves to the tail — constructed with the `true` third argument.<br/>**LRU (Least-Recently-Used):** an eviction policy that discards whichever entry has gone untouched the longest.<br/>**Eviction:** removing an entry to stay within a size cap.<br/>**`removeEldestEntry`:** the hook `LinkedHashMap` calls after each insert to decide whether to drop the oldest entry.

</Callout>

**Practice** — warm-ups for order-preserving maps (no pattern insight needed; pattern-based problems come later):

- [Design HashMap](https://leetcode.com/problems/design-hashmap/) — **Easy** — the plain-map baseline before you add ordering
- [First Unique Character in a String](https://leetcode.com/problems/first-unique-character-in-a-string/) — **Easy** — counting where insertion order matters
- [LRU Cache](https://leetcode.com/problems/lru-cache/) — **Medium** — the textbook direct use: access-order + eviction

## `TreeMap<K,V>` / `TreeSet<E>` — sorted keys

**What it is.** A self-balancing binary search tree (red–black tree). Keys are kept in sorted order, so besides O(log n) get/put/remove it answers **ordered** queries — floor, ceiling, ranges — that a hash map cannot.

<Callout kind="def" title="Binary-tree family — know these cold">

<br/>**Binary tree:** every node has at most two children (left, right).<br/>**Binary Search Tree (BST):** a binary tree with an *ordering rule* — every key in the left subtree &lt; the node &lt; every key in the right subtree — so a search follows one downward path instead of scanning.<br/>**Height:** the longest root-to-leaf path.<br/>**Balanced:** height stays ≈ log n (no long stringy chains); a **self-balancing** BST restructures itself on insert/delete to guarantee that.<br/>**Red–black tree:** the specific self-balancing BST behind `TreeMap`/`TreeSet`.<br/>**In-order traversal** (left → node → right): for a BST this emits keys in sorted order.<br/>**Predecessor / successor:** the next-smaller / next-larger key — exactly what `floor`/`lower` and `ceiling`/`higher` return.<br/>**Complete binary tree** (a *different* property, used by heaps): every level is completely filled except possibly the last, which fills strictly left-to-right with no gaps.<br/>**So the two ideas are orthogonal:** a **heap** is *complete* (a shape rule) but **not** ordered like a BST; a **BST** is kept *balanced* (and is usually **not** complete). A literal "complete binary **search** tree" would be a BST that also has that gap-free shape — you rarely build one on purpose. The takeaway: don't conflate the heap's *complete* **shape** with the BST's *ordering* **rule**.

</Callout>





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 680 238" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <rect x="0" y="0" width="680" height="238" fill="#fbfcfe"/>
  <text x="22" y="28" font-size="13" font-weight="700" fill="#2563eb">Balanced BST — smaller keys left, larger keys right; height ≈ log n</text>
  <!-- edges (search path 8→3→6 in green) -->
  <g stroke="#cbd5e1" stroke-width="2">
    <line x1="200" y1="60" x2="290" y2="122"/>
    <line x1="110" y1="122" x2="66" y2="184"/>
    <line x1="290" y1="122" x2="246" y2="184"/>
    <line x1="290" y1="122" x2="334" y2="184"/>
  </g>
  <g stroke="#16a34a" stroke-width="3">
    <line x1="200" y1="60" x2="110" y2="122"/>
    <line x1="110" y1="122" x2="154" y2="184"/>
  </g>
  <!-- nodes -->
  <g stroke-width="1.8" font-size="16" font-weight="700" text-anchor="middle">
    <circle cx="200" cy="58"  r="21" fill="#f0fdf4" stroke="#16a34a" stroke-width="2.4"/><text x="200" y="64" fill="#0b1220">8</text>
    <circle cx="110" cy="122" r="21" fill="#f0fdf4" stroke="#16a34a" stroke-width="2.4"/><text x="110" y="128" fill="#0b1220">3</text>
    <circle cx="290" cy="122" r="20" fill="#f8fafc" stroke="#cbd5e1"/><text x="290" y="128" fill="#0b1220">12</text>
    <circle cx="66"  cy="184" r="20" fill="#f8fafc" stroke="#cbd5e1"/><text x="66"  y="190" fill="#0b1220">1</text>
    <circle cx="154" cy="184" r="21" fill="#f0fdf4" stroke="#16a34a" stroke-width="2.4"/><text x="154" y="190" fill="#0b1220">6</text>
    <circle cx="246" cy="184" r="20" fill="#f8fafc" stroke="#cbd5e1"/><text x="246" y="190" fill="#0b1220">10</text>
    <circle cx="334" cy="184" r="20" fill="#f8fafc" stroke="#cbd5e1"/><text x="334" y="190" fill="#0b1220">14</text>
  </g>
  <rect x="400" y="60" width="258" height="120" rx="9" fill="#f0fdf4" stroke="#bbf7d0"/>
  <text x="416" y="84" font-size="12.5" font-weight="700" fill="#16a34a">search for 6</text>
  <text x="416" y="106" font-size="12" fill="#334155">6 &lt; 8  → go left</text>
  <text x="416" y="126" font-size="12" fill="#334155">6 &gt; 3  → go right</text>
  <text x="416" y="146" font-size="12" fill="#16a34a">found — one root-to-leaf path</text>
  <text x="416" y="168" font-size="11.5" fill="#2563eb">balanced → that path is ≈ log n steps</text>
  <text x="200" y="220" font-size="11" fill="#64748b" text-anchor="middle">in-order walk (left → node → right) prints keys sorted: 1 3 6 8 10 12 14</text>
</svg>
</div>




| Operation | Code | Cost | Why (how it's derived) |
|---|---|---|---|
| Lookup | `get(k)` / `containsKey(k)` | O(log n) | one root-to-leaf comparison path; the height is ≈ log n |
| Insert | `put(k, v)` | O(log n) | descend to the empty slot (log n), then a few O(1) rotations to rebalance |
| Delete | `remove(k)` | O(log n) | find the node (log n), then rebalance up the path |
| Floor / ceiling / lower / higher | `floorKey(x)` … | O(log n) | one downward walk, remembering the best candidate seen so far |
| Min / max | `firstKey()` / `lastKey()` | O(log n) | walk all-left / all-right to a leaf |
| Range view | `subMap(lo, hi)` | O(log n + k) | O(log n) to locate `lo`, then O(k) to emit the k keys in range |
| Iterate all | `for (var e : tm.entrySet())` | O(n) | an in-order traversal visits every node once |

<Callout kind="key" title="Why every operation is O(log n) — the derivation">

a `TreeMap` is a **balanced** tree (a red–black tree), which means it is never allowed to grow into a long stringy chain; its **height** (levels from root to deepest leaf) stays ≈ log₂ n. Every ordered operation is just *one walk from the root downward*: at each node you make a single comparison and step left or right, so you touch **one node per level**. Number of levels = height = log₂ n ⇒ **O(log n)**. Concretely, for n = 1,000,000 keys that's only ≈ 20 comparisons. (If the tree were *unbalanced* it could degrade into a straight line of height n → O(n); the red–black rotations during `put`/`remove` exist precisely to keep the height at log n.)

</Callout>

| Ordered query | Method | Meaning |
|---|---|---|
| Largest key ≤ x | `floorKey(x)` | predecessor-or-equal |
| Smallest key ≥ x | `ceilingKey(x)` | successor-or-equal |
| Strictly `<` / `>` | `lowerKey(x)` / `higherKey(x)` | strict neighbours |
| Ends | `firstKey()` / `lastKey()` | min / max |
| Range view | `subMap(lo, hi)` | keys in `[lo, hi)` |

<Callout kind="note" title="When TreeMap beats HashMap">

any time you need "the closest key," "the next event after time t," or "sum/count in a range" while inserting/deleting. Sweep-line and calendar problems lean on `floor`/`ceiling` heavily.

</Callout>

**Usage**


```java
TreeMap<Integer,String> tm = new TreeMap<>();   // keys kept sorted
tm.put(10, "a"); tm.put(20, "b"); tm.put(30, "c");
tm.get(20);                 // "b"
tm.floorKey(25);            // 20  (largest key ≤ 25)
tm.ceilingKey(25);          // 30  (smallest key ≥ 25)
tm.firstKey();              // 10   ;  tm.lastKey();  // 30
tm.subMap(10, 30);          // {10=a, 20=b}  (30 excluded)

TreeSet<Integer> ts = new TreeSet<>();          // sorted, unique
ts.add(5); ts.add(1); ts.add(9);                // iterates 1,5,9
ts.floor(6);   // 5      ts.ceiling(6);  // 9
ts.first();    // 1      ts.last();      // 9
```



**Iterating** (always in **sorted key order**)


```java
for (var e : tm.entrySet()) { /* keys ASCENDING */ }
for (var e : tm.descendingMap().entrySet()) { /* keys DESCENDING */ }
for (int k : tm.navigableKeySet()) { /* keys ascending */ }

for (int x : ts) { /* ascending */ }
Iterator<Integer> back = ts.descendingIterator();        // descending
```



**Practice** — warm-ups for BST / sorted-structure operations (no pattern insight needed; pattern-based problems come later):

- [Search in a Binary Search Tree](https://leetcode.com/problems/search-in-a-binary-search-tree/) — **Easy** — step left/right by comparison
- [Range Sum of BST](https://leetcode.com/problems/range-sum-of-bst/) — **Easy** — use the ordering to skip whole subtrees
- [Convert Sorted Array to BST](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) — **Easy** — pick the middle as the root, recurse
- [Two Sum IV - Input is a BST](https://leetcode.com/problems/two-sum-iv-input-is-a-bst/) — **Easy** — an in-order walk gives sorted keys
- [Insert into a Binary Search Tree](https://leetcode.com/problems/insert-into-a-binary-search-tree/) — **Medium** — follow the ordering to the empty slot

## `PriorityQueue<T>` — the binary heap

**What it is.** A **complete binary tree stored in an array**: node `i`'s children are at `2i+1` and `2i+2`. The heap invariant (parent ≤ children for a min-heap) keeps the smallest element at the root. Insert "sifts up," extract-min swaps the last leaf to the root and "sifts down" — each touches only one root-to-leaf path → O(log n). Java's `PriorityQueue` is a **min-heap** by default.





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 680 238" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <rect x="0" y="0" width="680" height="238" fill="#fbfcfe"/>
  <text x="22" y="28" font-size="13" font-weight="700" fill="#2563eb">Binary heap — a complete binary tree stored in a flat array</text>
  <!-- tree edges -->
  <g stroke="#94a3b8" stroke-width="2">
    <line x1="160" y1="58" x2="100" y2="118"/>
    <line x1="160" y1="58" x2="220" y2="118"/>
    <line x1="100" y1="118" x2="68" y2="178"/>
    <line x1="100" y1="118" x2="132" y2="178"/>
    <line x1="220" y1="118" x2="188" y2="178"/>
  </g>
  <!-- tree nodes -->
  <g stroke-width="1.8" font-size="16" font-weight="700" text-anchor="middle">
    <circle cx="160" cy="58"  r="20" fill="#eef5ff" stroke="#2563eb"/><text x="160" y="64" fill="#0b1220">2</text>
    <circle cx="100" cy="118" r="20" fill="#f8fafc" stroke="#cbd5e1"/><text x="100" y="124" fill="#0b1220">5</text>
    <circle cx="220" cy="118" r="20" fill="#f8fafc" stroke="#cbd5e1"/><text x="220" y="124" fill="#0b1220">3</text>
    <circle cx="68"  cy="178" r="20" fill="#f8fafc" stroke="#cbd5e1"/><text x="68"  y="184" fill="#0b1220">8</text>
    <circle cx="132" cy="178" r="20" fill="#f8fafc" stroke="#cbd5e1"/><text x="132" y="184" fill="#0b1220">6</text>
    <circle cx="188" cy="178" r="20" fill="#f8fafc" stroke="#cbd5e1"/><text x="188" y="184" fill="#0b1220">7</text>
  </g>
  <text x="160" y="44" font-size="10.5" fill="#16a34a" text-anchor="middle">root = min</text>
  <!-- array mapping -->
  <text x="380" y="70" font-size="11.5" font-weight="700" fill="#334155">same heap as an array</text>
  <g>
    <rect x="380" y="80" width="46" height="40" rx="6" fill="#eef5ff" stroke="#2563eb" stroke-width="1.6"/>
    <rect x="426" y="80" width="46" height="40" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
    <rect x="472" y="80" width="46" height="40" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
    <rect x="518" y="80" width="46" height="40" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
    <rect x="564" y="80" width="46" height="40" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
    <rect x="610" y="80" width="46" height="40" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
  </g>
  <g font-size="16" font-weight="700" fill="#0b1220" text-anchor="middle">
    <text x="403" y="106">2</text><text x="449" y="106">5</text><text x="495" y="106">3</text>
    <text x="541" y="106">8</text><text x="587" y="106">6</text><text x="633" y="106">7</text>
  </g>
  <g font-size="10" fill="#94a3b8" text-anchor="middle">
    <text x="403" y="136">0</text><text x="449" y="136">1</text><text x="495" y="136">2</text>
    <text x="541" y="136">3</text><text x="587" y="136">4</text><text x="633" y="136">5</text>
  </g>
  <rect x="380" y="156" width="276" height="60" rx="9" fill="#f6f8fb" stroke="#d9dee7"/>
  <text x="396" y="178" font-size="12" fill="#0b1220">children of i → <tspan font-weight="700" fill="#2563eb">2i+1</tspan> and <tspan font-weight="700" fill="#2563eb">2i+2</tspan></text>
  <text x="396" y="198" font-size="12" fill="#0b1220">parent of i → <tspan font-weight="700" fill="#2563eb">(i−1)/2</tspan></text>
  <text x="396" y="212" font-size="10.5" fill="#64748b">index math replaces pointers → no tree object needed</text>
</svg>
</div>




| Operation | Code | Cost |
|---|---|---|
| Peek min/max | `pq.peek()` | O(1) |
| Insert | `pq.offer(x)` | O(log n) |
| Extract min/max | `pq.poll()` | O(log n) |
| Build from n items | `new PriorityQueue<>(collection)` | O(n) |
| Arbitrary search/remove | `pq.remove(x)` | O(n) |



```java
PriorityQueue<Integer> minHeap = new PriorityQueue<>();                     // min at top
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
PriorityQueue<int[]> byDist = new PriorityQueue<>((a,b) -> a[1] - b[1]);    // custom order
```



**Usage**


```java
PriorityQueue<Integer> pq = new PriorityQueue<>();   // min-heap
pq.offer(5); pq.offer(1); pq.offer(3);   // insert — O(log n) each
int min = pq.peek();                     // 1   (smallest, not removed)
int out = pq.poll();                     // 1   (remove smallest) -> {3,5}
boolean empty = pq.isEmpty();
// max-heap or custom order: pass a comparator to the constructor (see above)
```



**Iterating** (a classic gotcha)


```java
for (int x : pq) { /* HEAP order — NOT sorted! */ }      // common bug
Iterator<Integer> it = pq.iterator();                    // also heap order
// To visit in SORTED order you must remove elements:
while (!pq.isEmpty()) { int x = pq.poll(); }             // ascending, but DRAINS the heap
```



<Callout kind="trap" title="Common Trap">

iterating a `PriorityQueue` does **not** give sorted order; only the root is guaranteed smallest. If you need sorted output, `poll()` until empty (or copy to a list and sort).

</Callout>

<Callout kind="trap" title="Common Trap">

a heap gives you *one* extreme cheaply, **not** a sorted view and **not** O(log n) arbitrary removal (`remove(x)` is O(n)). It also has **no decrease-key**; for Dijkstra, push a fresh entry and skip stale pops. For "kth largest," a size-k heap (O(n log k)) beats sorting; see Heaps.

</Callout>

<Callout kind="def" title="What &quot;decrease-key&quot; means (and why Java's `PriorityQueue` lacks it)">

*decrease-key* is the operation *"an item is already in the heap with priority 10; lower its priority to 3 and move it to its new correct spot."* Heaps that support it (a binary heap paired with a position-index map, or a Fibonacci heap) can do this in O(log n). Java's `PriorityQueue` **can't**: it keeps no index of where each element lives, so to even *find* the item is O(n). Why you'd want it: Dijkstra's core step is "relax an edge → *decrease* that neighbour's tentative distance," which is literally a decrease-key.<br/>**The idiomatic Java workaround — lazy deletion:** don't try to update the old entry. Just `offer` a **new** entry `(v, newDist)`, and when you `poll` a node, ignore it if it's stale — `if (d > dist[v]) continue;`. The heap may hold a few out-of-date duplicates, but they're harmless and the total cost stays O(E log E). This "push fresh, skip stale" trick is the standard way to write Dijkstra in Java.

</Callout>

<Callout kind="def" title="Key terms">

<br/>**Complete binary tree:** every level full except possibly the last, filled left-to-right — the gap-free shape that lets a heap live in a flat array with no pointers (child indices are just `2i+1`, `2i+2`).<br/>**Binary heap:** that array-backed complete tree obeying the heap property.<br/>**Heap property / invariant:** every parent ≤ its children (min-heap) or ≥ them (max-heap), forcing the extreme to the root.<br/>**Sift-up (percolate up):** after adding at the end, swap the new value upward until the parent rule holds.<br/>**Sift-down (percolate down):** after removing the root, move the last leaf to the top and swap it downward.<br/>**Heapify:** building a heap from n items in O(n).

</Callout>

**Practice** — warm-ups for the heap API (no pattern insight needed; pattern-based problems come later):

- [Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) — **Easy** — repeatedly poll the two largest, push their difference
- [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) — **Easy** — keep a size-k min-heap
- [Relative Ranks](https://leetcode.com/problems/relative-ranks/) — **Easy** — poll items out in sorted order
- [The K Weakest Rows in a Matrix](https://leetcode.com/problems/the-k-weakest-rows-in-a-matrix/) — **Easy** — heap ordered by a custom (strength, index) key

## Trie (prefix tree) — a preview

**What it is.** A tree where each edge is a character and each root-to-node path spells a prefix. Lookups cost O(L) in the key length `L`, independent of how many words are stored, and prefixes are shared. Full treatment in the Tries chapter.





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 680 196" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <rect x="0" y="0" width="680" height="196" fill="#fbfcfe"/>
  <text x="22" y="28" font-size="13" font-weight="700" fill="#2563eb">Trie — each edge is a character; a path spells a prefix</text>
  <!-- edges -->
  <g stroke="#94a3b8" stroke-width="2">
    <line x1="86" y1="104" x2="146" y2="104"/>
    <line x1="176" y1="104" x2="236" y2="104"/>
    <line x1="266" y1="96" x2="320" y2="70"/>
    <line x1="266" y1="112" x2="320" y2="140"/>
  </g>
  <!-- edge labels -->
  <g font-size="13" font-weight="700" fill="#2563eb" text-anchor="middle">
    <text x="116" y="98">c</text><text x="206" y="98">a</text>
    <text x="290" y="74">t</text><text x="290" y="142">r</text>
  </g>
  <!-- nodes -->
  <g stroke-width="1.8">
    <circle cx="66"  cy="104" r="20" fill="#e2e8f0" stroke="#64748b"/>
    <circle cx="161" cy="104" r="20" fill="#f8fafc" stroke="#cbd5e1"/>
    <circle cx="251" cy="104" r="20" fill="#f8fafc" stroke="#cbd5e1"/>
    <circle cx="340" cy="62"  r="21" fill="#f0fdf4" stroke="#16a34a" stroke-width="2.4"/>
    <circle cx="340" cy="146" r="21" fill="#f0fdf4" stroke="#16a34a" stroke-width="2.4"/>
  </g>
  <g font-size="12" font-weight="700" fill="#0b1220" text-anchor="middle">
    <text x="66" y="108">root</text>
    <text x="340" y="66">cat★</text><text x="340" y="150">car★</text>
  </g>
  <rect x="420" y="66" width="240" height="72" rx="9" fill="#f0fdf4" stroke="#bbf7d0"/>
  <text x="436" y="90" font-size="12" fill="#16a34a">★ = end-of-word flag (a complete word)</text>
  <text x="436" y="112" font-size="12" fill="#334155">"cat" and "car" <tspan font-weight="700">share</tspan> the "ca" path</text>
  <text x="436" y="132" font-size="11.5" fill="#2563eb">search "car" → walk c→a→r → O(length)</text>
</svg>
</div>




**Usage** (full `Trie` class in the Tries chapter)


```java
Trie trie = new Trie();
trie.insert("cat");
trie.insert("car");
trie.search("cat");        // true
trie.search("ca");         // false — "ca" is a prefix, not a stored word
trie.startsWith("ca");     // true
```



<Callout kind="def" title="Key terms">

<br/>**Prefix:** a leading portion of a string (`"ca"` is a prefix of `"cat"` and `"car"`).<br/>**Edge:** a link labelled with one character between two nodes.<br/>**Path:** the chain of edges from the root that spells a prefix.<br/>**End-of-word flag:** a boolean on a node marking that the path *to here* is a complete stored word, not merely a prefix.<br/>**Alphabet:** the fixed character set (e.g. 26 lowercase letters) that sizes each node's child array.

</Callout>

**Practice** — warm-ups for building and walking a trie (no pattern insight needed; pattern-based problems come later):

- [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) — **Easy** — the shared-leading-characters idea, no trie required
- [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) — **Medium** — the structure itself: insert / search / startsWith
- [Design Add and Search Words](https://leetcode.com/problems/design-add-and-search-words-data-structure/) — **Medium** — a trie plus a `.` wildcard that branches the walk
- [Implement Trie II (Prefix Tree)](https://leetcode.com/problems/implement-trie-ii-prefix-tree/) — **Medium** — store a count on each node

---

## Sorting &amp; Comparators — the part everyone fumbles

Sorting is a single method call. The only real question is **"in what order?"** — and that order is a `Comparator`. Let's build it up from the simplest case to sorting your own objects.

### 1. Sort numbers (the simplest case)



```java
int[] a = {5, 2, 9, 1};
Arrays.sort(a);                               // ascending -> [1, 2, 5, 9]

Integer[] b = {5, 2, 9, 1};
Arrays.sort(b, Collections.reverseOrder());   // descending -> [9, 5, 2, 1]  (needs objects, not int[])

List<Integer> list = new ArrayList<>(List.of(5, 2, 9, 1));
Collections.sort(list);                       // ascending
list.sort(Comparator.reverseOrder());         // descending
```



<Callout kind="trap" title="Common Trap (overflow)">

never write a comparator as `(a,b) -> a - b`. When the subtraction exceeds `int` range (e.g. `a = 2_000_000_000, b = -2_000_000_000`) it **overflows** to the wrong sign and corrupts the sort. Always use `Integer.compare(a, b)` / `Long.compare(a, b)`.

</Callout>

### 2. Sort your own objects (the part people actually need)

Say you have a class and want to sort by one of its fields. `Comparator.comparing` picks the field for you:



```java
class Person {
    String name; int age;
    Person(String name, int age) { this.name = name; this.age = age; }
    String name() { return name; }     // accessor used by Person::name
    int    age()  { return age;  }     // accessor used by Person::age
}
List<Person> people = new ArrayList<>(List.of(
    new Person("Ann", 30), new Person("Bob", 25), new Person("Cy", 30)));

people.sort(Comparator.comparingInt(Person::age));             // by age, ascending
people.sort(Comparator.comparingInt(Person::age).reversed());  // by age, descending
people.sort(Comparator.comparing(Person::name));               // by name, A → Z

// Multiple keys — age ascending, then name as the tie-breaker:
people.sort(Comparator.comparingInt(Person::age)
                      .thenComparing(Person::name));
```



That's really the whole toolkit: **`comparing` / `comparingInt`** to choose the key, **`thenComparing`** to break ties, **`reversed()`** to flip. Everything else is a variation on these three.

### 3. Sort any container (same comparator, different call)

The comparator you just learned works everywhere — only the *call* changes per container:

| Container | How to sort it |
|---|---|
| `int[]` (primitives) | `Arrays.sort(a)` — ascending only; to reverse, box to `Integer[]` or reverse after |
| `Integer[]` / `T[]` | `Arrays.sort(arr, cmp)` |
| `int[][]` (rows) | `Arrays.sort(grid, (r, s) -> Integer.compare(r[0], s[0]))` — e.g. intervals by start |
| `List<T>` | `list.sort(cmp)` or `Collections.sort(list, cmp)` |
| `PriorityQueue<T>` | pass the comparator to the **constructor** — it stays a sorted heap |
| `TreeMap` / `TreeSet` | pass the comparator to the **constructor** — keys stay sorted |
| indices (keep values put) | sort an `Integer[] idx` by `Comparator.comparingInt(i -> a[i])` |



```java
Arrays.sort(intervals, (x, y) -> Integer.compare(x[0], y[0]));          // 2D array by column 0
PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(p -> p[1]));  // min-heap by p[1]
TreeMap<String,Integer> desc = new TreeMap<>(Comparator.reverseOrder());            // keys Z → A
```



### 4. Map by one thing, sort by another (a very common combo)

A huge number of problems ask you to **count or score items in a map, then sort the items by that mapped value**. The trick: build the map first, then write a comparator that *looks up* the sort key from the map instead of reading it off the element.



```java
// Sort Characters By Frequency (LeetCode 451): most frequent character first
Map<Character,Integer> freq = new HashMap<>();
for (char c : s.toCharArray()) freq.merge(c, 1, Integer::sum);   // count each char

List<Character> chars = new ArrayList<>(freq.keySet());
chars.sort((x, y) -> freq.get(y) - freq.get(x));                 // sort by frequency, DESCENDING
// clearer: chars.sort(Comparator.comparingInt(freq::get).reversed());
```



Same idea powers several classics:

- **Top K Frequent Elements** — sort (or heap) the keys by `freq.get(key)`.
- **Relative Sort Array** — sort `arr1` by each value's position in `arr2` (`rank.get(v)`), pushing unranked values to the end.
- **Custom Sort String** — sort characters by their index in a given ordering string.

You can also sort a map's **entries** directly by key or by value:



```java
List<Map.Entry<String,Integer>> entries = new ArrayList<>(freq.entrySet());
entries.sort(Map.Entry.comparingByValue());                              // by value, ascending
entries.sort(Map.Entry.<String,Integer>comparingByValue().reversed());   // by value, descending
entries.sort(Map.Entry.comparingByKey());                                // by key
```



**Quick reference — the whole comparator toolkit**

| Builder | What it does |
|---|---|
| `Comparator.comparing(f)` / `comparingInt(f)` | order by the key `f(x)` |
| `.thenComparing(g)` | break ties with `g` |
| `.reversed()` | flip the order |
| `Comparator.naturalOrder()` / `reverseOrder()` | asc / desc for `Comparable` types |
| `Map.Entry.comparingByKey()` / `comparingByValue()` | sort map entries |
| `Comparator.nullsFirst(cmp)` | push `null`s to the front |

### `Comparable` vs `Comparator`

- **`Comparable<T>`** — the type's *one natural* ordering, via `int compareTo(T o)`. Implement it when there's an obvious default (e.g. numeric, alphabetical).
- **`Comparator<T>`** — an *external, swappable* ordering. Use it to sort the same type multiple ways without touching the class.



```java
class Task implements Comparable<Task> {
    int priority;
    public int compareTo(Task o) { return Integer.compare(this.priority, o.priority); }  // natural
}
// ...but sort a different way on demand:
tasks.sort(Comparator.comparing(Task::deadline));
```



<Callout kind="inv" title="Comparator contract (must hold or sorts misbehave)">

it must be *consistent*: `compare(a,b)` and `compare(b,a)` have opposite signs, and if `a<b` and `b<c` then `a<c` (transitive). A comparator that violates this (e.g. the overflow bug, or `return 1` for equal elements) can throw `IllegalArgumentException: Comparison method violates its general contract`.

</Callout>

<Callout kind="note" title="Stability recap">

a **stable** sort keeps elements that compare *equal* in their original order; an **unstable** one may shuffle them. Why care? Because you often sort by one field and want ties left as they were — e.g. sort people by age, and two 30-year-olds should stay in input order. `Arrays.sort(Object[])`, `Collections.sort`, and `List.sort` are stable (Timsort), so you can sort by a secondary key first, then the primary key, and the secondary order survives the ties (multi-pass sorting). `Arrays.sort(int[]/primitive[])` is **not** stable — but that's invisible for raw numbers (two equal `int`s are identical, so you can't tell if they moved); it only matters for objects. Need a stable primitive sort? Box to `Integer[]`, or sort an index array with a stable comparator.

</Callout>

**Practice** — exercises for writing comparators and sorting different containers (one per line):

- [Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/) — **Easy** — order by a simple key (even before odd)
- [Height Checker](https://leetcode.com/problems/height-checker/) — **Easy** — compare against a sorted copy
- [Relative Sort Array](https://leetcode.com/problems/relative-sort-array/) — **Easy** — sort by each value's rank in another array
- [Sort Characters By Frequency](https://leetcode.com/problems/sort-characters-by-frequency/) — **Medium** — the "map by one thing, sort by another" combo
- [Custom Sort String](https://leetcode.com/problems/custom-sort-string/) — **Medium** — sort by index in a given ordering string
- [Largest Number](https://leetcode.com/problems/largest-number/) — **Medium** — a custom comparator on concatenated strings
