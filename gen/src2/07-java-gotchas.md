# Java DSA Gotchas

*Every language has a shortlist of features that silently corrupt your algorithm. In Java, most are Integer autoboxing, integer overflow, and a handful of container idioms. This chapter is a concentrated cheat sheet — 20 gotchas that cause 90% of Java-specific interview bugs.*

Every gotcha here has caused a real senior candidate to lose an offer. Read once, then re-read the day before an interview.

## 1. `Integer.MIN_VALUE` is its own negation

```java
int x = Integer.MIN_VALUE;
int y = -x;               // still Integer.MIN_VALUE, silently
int z = Math.abs(x);      // still Integer.MIN_VALUE, silently
```

Two's complement can represent `-2³¹` but not `+2³¹`, so negation overflows.

**Where it bites:** `Math.abs(nums[i])` in linked-list-cycle-with-index tricks, palindrome number's reverse, any "flip sign" heuristic. **Fix**: use `long` for the sign flip, or explicitly check `if (x == Integer.MIN_VALUE)`.

## 2. `(lo + hi) / 2` overflows in binary search

```java
int mid = (lo + hi) / 2;              // WRONG: overflow when lo+hi > 2³¹-1
int mid = lo + (hi - lo) / 2;         // right
int mid = (lo + hi) >>> 1;            // also right; unsigned shift, works even on overflow
```

**Interview signal:** the moment you write `mid`, say aloud: "using `lo + (hi-lo)/2` for overflow safety." Interviewers explicitly listen for this.

## 3. Autoboxing costs O(n) — silently

```java
Map<Integer,Integer> m = new HashMap<>();
for (int i = 0; i < 100_000; i++) m.put(i, i);   // 200k Integer objects allocated
```

Every `int → Integer` boxing allocates. In tight loops on `10⁶` inputs this dominates runtime. **Fix:** use `int[]` when the key domain is bounded (e.g., `int[26]` for lowercase counts), or `Trove` / `Eclipse Collections` for primitives (rarely allowed in interviews, so know the tradeoff and mention it).

## 4. `Integer` equality: `==` vs `equals`

```java
Integer a = 127, b = 127;
a == b;   // true — Integer cache reuses [-128, 127]
Integer c = 128, d = 128;
c == d;   // FALSE — outside cache, different objects
```

**Fix:** for `Integer` (and any boxed wrapper), always use `.equals()` or unbox to `int`.

## 5. `HashMap.get(key)` returns `null`, not `0`

```java
Map<Character,Integer> freq = new HashMap<>();
freq.get('x');                          // null — NullPointerException if unboxed to int
freq.getOrDefault('x', 0);              // 0 (safe)
freq.merge('x', 1, Integer::sum);       // insert-or-increment idiom
```

**Interview-standard idiom** — memorize `merge` for frequency counts. It's a one-liner that fetches, applies, and stores.

## 6. `ArrayDeque` over `Stack` (always)

```java
Stack<Integer> s = new Stack<>();               // legacy, synchronized, slow
ArrayDeque<Integer> s = new ArrayDeque<>();     // fast, idiomatic
s.push(x);  s.pop();  s.peek();
```

`Stack` extends `Vector` — every operation acquires a monitor lock. `ArrayDeque` is 2-3× faster in single-threaded code and is what senior Java devs use. Saying "I'd use `ArrayDeque`" in the interview is a small but consistent seniority signal.

## 7. `ArrayDeque` doesn't accept `null`

```java
ArrayDeque<Integer> q = new ArrayDeque<>();
q.offer(null);   // NullPointerException
```

Because `poll()` returns `null` for "empty", accepting `null` as a value would create ambiguity. **Fix:** use a sentinel like `-1` or wrap with `Optional`. If you must store nulls, use `LinkedList` (but then take the pointer-chasing perf hit).

## 8. `LinkedList` is almost never the right choice

`LinkedList` has O(1) insertion — but only if you already hold a pointer to the node. Random access via `get(i)` is O(i). For "queue" duties, use `ArrayDeque`. For "list", use `ArrayList`.

**The only justified use of `LinkedList`:** as an `Iterator`-based queue where you frequently insert/remove from BOTH ends *and* you never index into the middle. `ArrayDeque` covers this too — so realistically, never.

## 9. `List.sort(Comparator)` needs `-`-safe comparison

```java
list.sort((a, b) -> a - b);   // WRONG: overflows for a=Integer.MIN_VALUE, b=positive
list.sort(Integer::compare);  // right — uses safe compare
list.sort((a, b) -> Integer.compare(a, b));
```

Same trap for `PriorityQueue`. Overflow in a comparator gives you *nondeterministic* ordering — the JVM's TimSort assumes transitivity, and violating it can throw `IllegalArgumentException` mid-sort.

## 10. `PriorityQueue` iteration is NOT sorted

```java
PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.offer(3); pq.offer(1); pq.offer(2);
for (int x : pq) System.out.print(x);   // prints 1,3,2 (heap array order, NOT sorted)
```

`pq.iterator()` walks the underlying array — heap-order, not sort-order. To iterate in sorted order, keep polling: `while (!pq.isEmpty()) pq.poll()`.

## 11. `String.equals` vs `==` — but also interning

```java
String a = "hello", b = "hello";
a == b;                        // true — string literals are interned
String c = new String("hello");
a == c;                        // FALSE — new String() creates a new object
```

**Rule:** use `.equals()` for content comparison; never rely on `==` for strings even with literals (a refactor to `new String(...)` will break silently).

## 12. `String.substring(i, j)` is O(j - i) since Java 7

Older Java shared the backing char array; modern Java copies. So `substring` isn't free — repeated calls in a tight loop are quadratic. **Fix:** use `StringBuilder.substring` for repeated slicing, or work with indices.

## 13. `Character.getNumericValue('a')` returns 10, not `'a'`'s code point

```java
Character.getNumericValue('a');   // 10 — hex A
'a' - 'a';                        // 0 — what you probably wanted for 26-letter offset
```

For "letter to index" arithmetic, always use `c - 'a'` (or `c - 'A'`). Never trust `getNumericValue`.

## 14. `int[26]` vs `HashMap<Character,Integer>`

For lowercase-only frequency counts, `int[26]` is:
- 5× faster (no hashing, no boxing)
- Zero-initialized for free
- Constant memory
- More readable: `count[c - 'a']++`

Use `HashMap` only when the alphabet is large, sparse, or unknown. **Interview signal:** using `int[26]` unprompted for a lowercase problem is a mid-to-senior signal.

## 15. `Arrays.sort(int[])` is O(n log n) — but `Arrays.sort(Integer[])` uses different sort

`Arrays.sort` on primitives uses Dual-Pivot Quicksort (Java 7+); on Objects uses TimSort. For an interview problem where you need `n log n`, sorting primitives is faster (no boxing). This matters at `10⁶` inputs.

## 16. Recursion has no tail-call optimization

Java's JIT does not perform TCO. A recursive function that recurses `n` times keeps `n` frames on the stack — space complexity is O(n) even if you think it's tail-recursive.

**Interview trap:** "Isn't this O(1) space since it's tail-recursive?" — **No**, in Java it's O(n). Rewrite as a loop for genuine O(1) space.

## 17. `Iterator.remove()` is the only safe way to remove during iteration

```java
for (Integer x : list) if (x < 0) list.remove(x);   // ConcurrentModificationException
Iterator<Integer> it = list.iterator();
while (it.hasNext()) if (it.next() < 0) it.remove();  // safe
```

Or filter into a new collection. Never mutate the underlying structure while a `for-each` is walking it.

## 18. `TreeMap` gives you a sorted-map — cheaper than sorting keys

```java
TreeMap<Integer,V> m = new TreeMap<>();
m.floorKey(x);      // greatest key ≤ x
m.ceilingKey(x);    // smallest key ≥ x
m.firstKey();       // smallest
m.lastKey();        // largest
```

All O(log n). If your algorithm needs "nearest smaller / larger", `TreeMap.floorKey`/`ceilingKey` is often cleaner than a monotonic stack. It's the mid-level trick that senior interviewers appreciate.

## 19. `Long` division truncates, then cast happens

```java
long x = (long) (100 / 3);      // 33 — division happens as int first!
long x = (long) 100 / 3;        // 33 — same, cast binds tighter than /
long x = 100L / 3;              // 33 — but if either operand is long, still integer division
long x = 100 / 3.0;             // 33.33... — becomes double
```

For "average" or "midpoint" calculations, use `double` or `long` and be explicit about when integer truncation happens.

## 20. `HashMap` iteration order is *not stable across JVM versions*

Java 8 changed `HashMap` iteration order (via tree-buckets under collisions). Do NOT rely on any particular order. If you need deterministic iteration:
- `LinkedHashMap` — insertion order
- `TreeMap` — key-sorted order

**Trap:** interview solutions that "happen to work" because of iteration order will fail on graders that use a different JVM. Explicit ordering also demonstrates senior craftsmanship.

## Quick reference — the 10 idioms every senior Java DSA candidate writes without thinking

```java
// 1. Frequency map
map.merge(key, 1, Integer::sum);

// 2. Multi-value grouping
map.computeIfAbsent(key, k -> new ArrayList<>()).add(value);

// 3. Safe midpoint
int mid = lo + (hi - lo) / 2;

// 4. Char-to-index
int idx = c - 'a';

// 5. Grid neighbors
int[][] DIRS = {{-1,0},{1,0},{0,-1},{0,1}};
for (int[] d : DIRS) { int nr = r+d[0], nc = c+d[1]; /* ... */ }

// 6. Priority queue with primitive comparator
PriorityQueue<Integer> pq = new PriorityQueue<>(Integer::compare);

// 7. Stack via ArrayDeque
ArrayDeque<Integer> stack = new ArrayDeque<>();
stack.push(x); stack.pop(); stack.peek();

// 8. Reverse an int[] segment
for (int i = lo, j = hi; i < j; i++, j--) { int t = a[i]; a[i] = a[j]; a[j] = t; }

// 9. Copy array
int[] copy = Arrays.copyOfRange(src, from, to);   // half-open

// 10. Long overflow-safe sum
long sum = 0;
for (int x : nums) sum += x;   // always long, never int
```

Practice writing each of these blind. They should flow from your fingers by the time you interview.
