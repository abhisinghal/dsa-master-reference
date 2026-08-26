# Bit Manipulation


<PatternVideo pattern-name="Bit Manipulation" duration="8–12 min" />

<PatternProgress pattern-id="bit-manip" problems="single-number, missing-number, find-the-difference, number-of-1-bits, hamming-distance, power-of-two, reverse-bits, maximum-product-of-word-lengths, sum-of-all-subset-xor-totals, subsets" />



## Why bit manipulation exists — the story

You're implementing a game engine's collision system. Every game object has a set of tags: `enemy`, `friendly`, `flying`, `underwater`, `explosive`, `pickup`, ... twenty tags total. On every frame, for every object, you need to answer: *"Does this object have any of tags X, Y, or Z?"*

The obvious approach: `HashSet<String>` for each object's tags, iterate over the query tags, `set.contains(tag)`. It works. It's readable. And for 10 objects it's fine.

But your game has **100,000 active objects**, and you check tags **60 times per second**. That's 6 million tag queries per second, each doing 3 HashMap lookups (hash calc, bucket walk, string equals). Rough cost: 100 ns per query × 6M = **600 ms per frame** — 36× over your frame budget. The game stutters. Your engine ships slow.

The fix is to represent each object's tags as **a single integer**, one bit per tag. `enemy` is bit 0, `friendly` bit 1, `flying` bit 2, ... A "has any of these tags" query becomes: `(object.tags & queryMask) != 0` — **one AND, one comparison, done in 1 nanosecond**. 100 ns → 1 ns is a 100× speedup, and now you have 594 ms of frame budget back. This is exactly how every AAA game engine (Unreal, Unity, Frostbite) implements object filtering, physics layer masks, and collision queries.

Bit manipulation is what happens when you realize the CPU handles 32 or 64 bits in parallel for free. Any time your data fits in ≤ 64 flags, a single integer beats every fancy data structure. XOR cancels duplicates. `x & -x` isolates the lowest set bit. `x & (x-1)` clears it. These aren't tricks for showing off — they're production optimizations used in networking (IP filter masks), cryptography (SHA-256 avalanche), compilers (register allocation), and databases (bitmap indexes on columns with few distinct values).

The catch: bit manipulation is *unforgiving*. Off-by-one on a shift and your program silently returns garbage. Confuse `>>` (arithmetic shift, preserves sign) with `>>>` (logical shift, zero-fills) in Java and negative numbers explode. Java's `int` is signed 32-bit, so `1 << 31` is `Integer.MIN_VALUE` — negative. The interview trap isn't the algorithm; it's the arithmetic subtlety.

## The core idea — a few identities do all the work

<BitManipAnim />

**Memorize these seven identities.** Half of the "clever" bit problems reduce to one of them.

```java
x & (x - 1)     // clear the lowest set bit           e.g. 0b1010 -> 0b1000
x & -x          // isolate the lowest set bit         e.g. 0b1010 -> 0b0010
x | (x + 1)     // set the lowest unset bit           e.g. 0b1010 -> 0b1011
x ^ x           // 0  (any value XOR'd with itself)   fundamental to "find single" family
x ^ 0           // x  (identity)
(x >> k) & 1    // read bit k
x | (1 << k)    // set bit k
x & ~(1 << k)   // clear bit k
x ^ (1 << k)    // toggle bit k
```

**Java landmines to internalize:**
- `int` is signed 32-bit. `1 << 31` is `Integer.MIN_VALUE`, not 2^31. Use `1L << 31` for the positive value.
- `>>` is *arithmetic* shift (preserves sign bit). `>>>` is *logical* shift (zero-fills). For unsigned bit counting or hashing, use `>>>`.
- `~x` is bitwise complement, flips all 32 bits. `~5 == -6` (two's complement).
- `Integer.bitCount(x)` uses a hardware `popcnt` instruction — vastly faster than looping.

## When to use it — recognition signals

- **n ≤ 20** and you're enumerating subsets — a mask *is* the set. Bitmask DP.
- **"Single number that appears once, all others twice"** — XOR everything → duplicates cancel → result is the single. XOR-cancellation family.
- **"Count set bits" / "lowest set bit" / "is power of two"** — bit tricks, one-liners.
- **You need a compact set with fast union/intersection** — set as `int`; union is `|`, intersection is `&`, complement is `~`.
- **Bitmask DP over subsets** — `dp[mask]` where mask indicates which items are used. Traveling Salesman, Assignment, "shortest superstring."
- **Hash-like fingerprinting on small alphabets** — 26-bit mask for lowercase letters used, for "Maximum Product of Word Lengths" (two words have no common letters iff `mask1 & mask2 == 0`).
- **Fast integer arithmetic simulations** — multiplying by 2^k is `<< k`; dividing is `>>> k`.
- **Parity or checksum problems** — XOR is its own inverse, so parity computations are one line.

## When NOT to use it

- **n > 25 or so** — 2^25 = 33M is barely tractable; 2^30 = 10^9 explodes. Bitmask DP over subsets is dead beyond that.
- **The set has real semantic complexity** — bit manipulation shines when set membership is a clean boolean. If you need weights, counts, or ordering, use `HashMap` or `SortedSet`.
- **Bit tricks that yield the same asymptotic complexity as a HashSet** — cleverness has readability cost. Only reach for the trick when the O(1) bitmap operation is genuinely a bottleneck win.
- **You're solving a real cryptographic problem** — the identities here are the *building blocks*, not the algorithm. Roll your own crypto with these primitives and you'll ship a vulnerability.
- **Cross-language / cross-platform code where signed/unsigned mismatch matters** — Java's signed shifts differ from C's, from JavaScript's, from Python's arbitrary-precision. Bit-level code doesn't port cleanly.
- **A team member cannot read the code in 30 seconds** — comment aggressively or use a helper method. Bit tricks are a maintainability tax.

## The templates

### Template 1: Iterate all set bits (Kernighan's trick)

```java
int popcount(int x) {
    int count = 0;
    while (x != 0) {
        x &= (x - 1);                       // clear lowest set bit
        count++;
    }
    return count;
}
// or: Integer.bitCount(x) — hardware popcnt, ~1 ns
```

**Why Kernighan wins:** each iteration removes one bit, so loop runs exactly popcount(x) times — not 32 times. For sparse bitmasks (few 1s), this is faster than shifting-and-testing every bit.

### Template 2: Iterate all subsets of a mask

```java
for (int sub = mask; sub != 0; sub = (sub - 1) & mask) {
    // sub is now a non-empty subset of mask
    process(sub);
}
// Total iterations across all masks: 3^n (each of n bits is either in mask-not-sub, in-sub, or absent from both)
```

**Trick:** `(sub - 1) & mask` skips values that would violate the subset property. Classic subset-DP over a mask.

### Template 3: XOR cancellation (Single Number)

```java
int singleNumber(int[] nums) {
    int x = 0;
    for (int n : nums) x ^= n;              // duplicates cancel, single survives
    return x;
}
```

**Complexity:** O(n) time, O(1) space. Compare with hash-set: O(n) time, O(n) space. Bit trick is strictly better here.

### Template 4: Bitmask DP (traveling salesman skeleton)

```java
int tsp(int[][] dist) {
    int n = dist.length;
    int[][] dp = new int[1 << n][n];         // dp[mask][last] = min cost to visit mask, ending at last
    for (int[] row : dp) Arrays.fill(row, Integer.MAX_VALUE / 2);
    dp[1][0] = 0;                             // start at city 0
    for (int mask = 1; mask < (1 << n); mask++)
        for (int last = 0; last < n; last++) {
            if ((mask & (1 << last)) == 0 || dp[mask][last] == Integer.MAX_VALUE / 2) continue;
            for (int next = 0; next < n; next++)
                if ((mask & (1 << next)) == 0) {
                    int newMask = mask | (1 << next);
                    dp[newMask][next] = Math.min(dp[newMask][next], dp[mask][last] + dist[last][next]);
                }
        }
    int best = Integer.MAX_VALUE;
    for (int last = 1; last < n; last++)
        best = Math.min(best, dp[(1 << n) - 1][last] + dist[last][0]);   // return to start
    return best;
}
```

**Complexity:** O(2^n · n^2) time, O(2^n · n) space. For n ≤ 20, tractable.

### Complexity summary

| Operation | Time | Space |
|---|---|---|
| Read/set/clear/toggle bit | O(1) | O(1) |
| Popcount (via Kernighan) | O(popcount) | O(1) |
| Popcount (hardware) | O(1) | O(1) |
| Iterate subsets of mask | O(2^popcount) per mask | O(1) |
| Bitmask DP (TSP-style) | O(2^n · n^2) | O(2^n · n) |
| XOR-cancellation | O(n) | O(1) |

## Traps & gotchas — the 5 that fail candidates on interview day

> [trap] **Trap 1 — Signed vs. unsigned shift.** In Java, `>>` preserves the sign bit — for negative numbers, `-1 >> 1 == -1` (fills with 1s). `>>>` zero-fills — `-1 >>> 1 == Integer.MAX_VALUE`. For bit counting on 32-bit ints of arbitrary sign, always use `>>>`. **Rule: if in doubt, use `>>>`.**

> [trap] **Trap 2 — `1 << 31` overflow.** `int` is signed 32-bit, so `1 << 31` is `Integer.MIN_VALUE == -2147483648`. If you meant "the value 2^31 = 2147483648," use `1L << 31`. **Rule: if the shift result might reach or exceed bit 31, use `long`.**

> [trap] **Trap 3 — Wrong precedence of `&` vs. `==`.** `if (x & mask == 0)` parses as `if (x & (mask == 0))` — checking whether `mask == 0` gives boolean 0, then AND-ing with `x`, then implicit conversion. Almost never what you want. **Rule: always parenthesize: `if ((x & mask) == 0)`.**

> [trap] **Trap 4 — Iterating all 32 bits when the value is sparse.** `for (int i = 0; i < 32; i++) if ((x >> i) & 1)` is O(32) regardless of the popcount. `while (x != 0) { x &= x - 1; count++; }` is O(popcount) — sometimes 1 iteration. **Rule: use Kernighan's trick when iteration count depends on popcount.**

> [trap] **Trap 5 — Assuming XOR undoes any operation.** XOR undoes XOR (`x ^ y ^ y == x`), but doesn't undo AND or OR. Candidates sometimes write `x = x ^ mask` when they mean `x = x & ~mask`. **Rule: be explicit about the operation: `set = |`, `clear = & ~`, `toggle = ^`.**

## History — Kernighan's popcount trick (1988) and popcnt hardware (2000)

The bit-clearing trick `x & (x - 1)` was popularized by **Brian Kernighan** in his 1988 book *The C Programming Language* (2nd ed., co-authored with Dennis Ritchie). The trick appears in an exercise: count the number of 1-bits in an integer *in time proportional to the number of 1-bits*, not the number of bits. It's still the fastest software approach on architectures without native popcount.

In **2000**, Intel added the `popcnt` instruction as part of SSE4.2 — a single-cycle hardware popcount. AMD followed in 2006. Java's `Integer.bitCount()` compiles to this instruction on modern JVMs, making bit counting effectively free. Every LLVM-compiled bit-heavy algorithm (Bloom filter, geohash, HyperLogLog) uses it.

**Cryptography** has always been the largest consumer of bit tricks: SHA-256 mixes bits via 64 rounds of XOR, AND, OR, rotates, and additions. AES uses `xtime` — a specific `<< 1 XOR 0x1b` operation — to walk finite-field elements. In the compiler world, **register allocation** uses bitmask interference graphs to decide which variables can share a register.

Google's **Roaring Bitmap** (2013) is a compressed bitmap format used in Apache Lucene, Elasticsearch, Druid, Spark, and Snowflake for indexing sparse boolean columns. It combines the ideas from this chapter — bit tricks, bitmask iteration, popcount — into a real production data structure that indexes trillion-row datasets.

## Canonical problem walkthrough — Single Number

**Problem** ([↗ LeetCode](https://leetcode.com/problems/single-number/)): Given a non-empty array of integers where every element appears **twice** except for one, find that single one. Solve in linear time using constant extra space.

### Approach 1 — HashSet

Track seen elements; anything already there gets removed. Whatever remains is the single.

```java
int singleNumberSet(int[] nums) {
    Set<Integer> seen = new HashSet<>();
    for (int n : nums) {
        if (!seen.add(n)) seen.remove(n);
    }
    return seen.iterator().next();
}
```

**Complexity:** O(n) time, O(n) space. Violates the "constant space" constraint but is correct.

### Approach 2 — Sort and scan

Sort. Adjacent duplicates flank the single number.

```java
int singleNumberSort(int[] nums) {
    Arrays.sort(nums);
    for (int i = 0; i < nums.length - 1; i += 2) {
        if (nums[i] != nums[i + 1]) return nums[i];
    }
    return nums[nums.length - 1];
}
```

**Complexity:** O(n log n) time, O(1) space if in-place sort. Violates the "linear time" constraint.

### Approach 3 — XOR cancellation (the interview answer)

Since `x ^ x == 0` and XOR is associative and commutative, XORing every number in the array cancels all pairs. What remains is the single.

```java
int singleNumber(int[] nums) {
    int x = 0;
    for (int n : nums) x ^= n;
    return x;
}
```

**Complexity:** O(n) time, O(1) space. Meets both constraints. **One loop, one line.**

**Interview commentary:**
- *"HashSet is O(n) time but O(n) space — doesn't meet the constraint."*
- *"Sort-and-scan is O(1) space but O(n log n) time — also fails."*
- *"XOR-cancellation: since `x ^ x = 0` and XOR is commutative, XORing everything leaves only the single element. One pass, one line, both constraints met."*

### Complexity ladder

| Approach | Time | Space | When |
|---|---|---|---|
| HashSet | O(n) | O(n) | Violates constant-space constraint |
| Sort + scan | O(n log n) | O(1) | Violates linear-time constraint |
| **XOR cancellation** | **O(n)** | **O(1)** | **Interview default** |

---

**Grokking arc:** The motivating problem is representing tiny sets, parity, or binary properties without bulky data structures.

---

## Core identities
<p class="secgoal"><b>What & why:</b> the handful of bit tricks that most bit problems reduce to. Goal — memorize them so operations like "lowest set bit", "clear it", "toggle", and parity become one-liners.</p>

| Trick | Expression | Use |
|---|---|---|
| Test bit i | `(x >> i) & 1` | read a flag |
| Set bit i | `x \| (1 << i)` | add to set |
| Clear bit i | `x & ~(1 << i)` | remove from set |
| Toggle bit i | `x ^ (1 << i)` | flip |
| Lowest set bit | `x & -x` | isolate rightmost 1 |
| Clear lowest set bit | `x & (x - 1)` | count bits, power-of-two test |
| Is power of two | `x > 0 && (x & (x-1)) == 0` | — |
| Count set bits | `Integer.bitCount(x)` | popcount |
| XOR properties | `a^a=0`, `a^0=a`, commutative | pair cancellation |
| All subsets of mask | `for (s = m; s > 0; s = (s-1) & m)` | submask enumeration |

> [key] **Key Insight** — Two workhorses: `x & (x-1)` **removes** the lowest set bit (Brian Kernighan's popcount, power-of-two test), and `x & -x` **isolates** it (Fenwick tree indexing). XOR's self-cancellation (`a^a=0`) makes it the tool for "find the unpaired element."

## Single Number I / II / III (XOR) <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Single Number](https://leetcode.com/problems/single-number/)*

<ProgressCheck id="single-number-i-ii-iii-xor" />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="24" text-anchor="middle" font-family="var(--dsa-font)" font-size="13" font-weight="700" fill="var(--dsa-primary)">XOR accumulator cancels duplicate pairs</text>
  <g font-family="var(--dsa-font)" text-anchor="middle">
    <g font-size="17" font-weight="700" fill="var(--dsa-ink)">
      <rect x="34" y="50" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="56" y="78">4</text>
      <rect x="84" y="50" width="44" height="44" rx="7" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)" stroke-width="1.6"/><text x="106" y="78">1</text>
      <rect x="134" y="50" width="44" height="44" rx="7" fill="var(--dsa-info-soft)" stroke="var(--dsa-info)" stroke-width="1.6"/><text x="156" y="78">2</text>
      <rect x="184" y="50" width="44" height="44" rx="7" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)" stroke-width="1.6"/><text x="206" y="78">1</text>
      <rect x="234" y="50" width="44" height="44" rx="7" fill="var(--dsa-info-soft)" stroke="var(--dsa-info)" stroke-width="1.6"/><text x="256" y="78">2</text>
    </g>
    <g font-size="11" fill="var(--dsa-neutral)">
      <text x="56" y="108">i=0</text><text x="106" y="108">i=1</text><text x="156" y="108">i=2</text><text x="206" y="108">i=3</text><text x="256" y="108">i=4</text>
    </g>
  </g>
  <g font-family="var(--dsa-font)" font-size="12" font-weight="700">
    <text x="38" y="140" fill="var(--dsa-neutral)">0 ⊕ 4 = 4</text>
    <text x="38" y="162" fill="var(--dsa-neutral)">4 ⊕ 1 = 5</text>
    <text x="38" y="184" fill="var(--dsa-neutral)">5 ⊕ 2 = 7</text>
    <text x="38" y="206" fill="var(--dsa-neutral)">7 ⊕ 1 = 6</text>
    <text x="38" y="228" fill="var(--dsa-neutral)">6 ⊕ 2 = 4</text>
  </g>
  <rect x="292" y="146" width="76" height="62" rx="10" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="2.4"/>
  <text x="330" y="170" text-anchor="middle" font-family="var(--dsa-font)" font-size="12" font-weight="700" fill="var(--dsa-primary)">answer</text>
  <text x="330" y="196" text-anchor="middle" font-family="var(--dsa-font)" font-size="24" font-weight="700" fill="var(--dsa-ink)">4</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> duplicates cancel via XOR; the lone number remains.</div>

### Problem
Every element appears **twice except one**; find the single one — in O(n) time, O(1) space. (Variants II/III: one element appears 3×, or there are two singles.)

**Constraints:** `1 ≤ n ≤ 3·10⁴`; exactly one loner in the base version.

**Example 1:** `[4,1,2,1,2]` → `4`.

<ExamplePreview compact :input="['4', '1', '2', '1', '2']" :output="['4']" />

**Example 2:** `[2,2,1]` → `1`.

<ExamplePreview compact :input="['2', '2', '1']" :output="['1']" />

### Solution — brute force
Brute force counts frequencies in a hash map, then returns the value whose count is one. That is O(n) time and O(n) space, and a sort-based variant is O(n log n) time with less extra space. The optimized XOR version uses pair cancellation: `a ^ a = 0` and `a ^ 0 = a`, so one accumulator leaves only the unpaired number.

**Brute-force sketch:**

```text
count frequencies in a HashMap
scan the entries and return the key with count == 1
```

**Baseline complexity:** O(n) time and O(n) extra space for the hash map.

### Solution — optimized
The optimized solution keeps the original Java intact and explains the pattern that removes the brute-force bottleneck.

#### Pattern
XOR everything: pairs cancel, the loner survives.

> [inv] **Invariant** — Running XOR equals the XOR of all values seen; identical values annihilate, so after the full pass only odd-count values remain.

#### Java
```java
int singleNumber(int[] a) {            // every other element appears twice
    int x = 0;
    for (int v : a) x ^= v;
    return x;
}
```

> [note] **Trace it** — `[4,1,2,1,2]`. XOR all: `1^1=0`, `2^2=0`, leaving `4`. The duplicates annihilate, so the single number is **4**.

<CodeTrace
  title="Single Number — nums=[4,1,2,1,2]"
  :values="[4,1,2,1,2]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { xor: 4 }, note: "xor ^ 4 = 4" },
    { pointers: { i: 1 }, vars: { xor: 5 }, note: "4 ^ 1 = 5 (101)" },
    { pointers: { i: 2 }, vars: { xor: 7 }, note: "5 ^ 2 = 7 (111)" },
    { pointers: { i: 3 }, vars: { xor: 6 }, note: "7 ^ 1 = 6 (110)" },
    { pointers: { i: 4 }, vars: { xor: 4 }, note: "6 ^ 2 = 4. answer = 4", added: [0] }
  ]'
/>

**Time** O(n) single pass · **Space** O(1) — one accumulator, no hash map.

> [note] **Interview script** — "I first confirm every number appears exactly twice except the single value in the base problem. I start with brute force by counting frequencies in a hash map, which is O(n) time and O(n) space. I optimize with XOR cancellation, scanning once with one accumulator for O(n) time and O(1) space."


**Single Number III** (two loners, rest in pairs): XOR all → `xy = a ^ b`. A set bit of `xy` differs between `a` and `b`; split all numbers by that bit and XOR each group separately.

**Single Number II** (every element thrice except one): count bits mod 3 across all numbers, or use two-variable bit-state automata (`ones`, `twos`).

> [trap] **Common Trap** — Whole-XOR as split mask. *Example:* `nums=[1,2,3,4,1,2]`. `xy = 3^4 = 7 (0b111)`. Splitting by whole `xy` puts `1,2,3` in one group and `4` in the other — but `1^2^3 = 0`, losing the loner. Isolate a **single** distinguishing bit via `xy & -xy`.

<TrapTrace title="Whole-XOR as split mask" input="nums=[1,2,3,4,1,2]" bug="'nums=[1,2,3,4,1,2]'. 'xy = 3^4 = 7 (0b111)'. Splitting by whole 'xy' puts '1,2,3' in one group and '4' in the other — but '1^2^3 = 0', losing the loner. Isolate a **single** distinguishing bit via 'xy & -xy'." fix="See the guidance in the trap description and the code snippet." />

> [pat] **Pattern Connection** — XOR-cancellation also finds the *Missing Number* (`XOR of indices ^ XOR of values`) and the duplicated/missing pair in *Set Mismatch*.

#### Same pattern, new tweaks
XOR's "equal values cancel to 0" powers a whole family:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Missing Number](https://leetcode.com/problems/missing-number/) | XOR all indices `0..n` with all values; the survivor is the missing one | — |
| - **Single Number II** (every element three times) — *tweak:* count each bit position mod 3. |  | — |
| - **Single Number III** (two loners) — *tweak:* XOR everything, grab one distinguishing bit (`xy & -xy`), split into two groups. |  | — |
| [Find the Difference / Set Mismatch](https://leetcode.com/problems/find-the-difference/) | XOR the two collections so shared characters cancel, leaving the odd one out | — |

### Time Complexity
O(n): one XOR pass over the array.

### Space Complexity
O(1): one accumulator.

### Learning notes
- Why initialize `x = 0`? — zero is XOR's identity, so it does not change the first value.
- Why `x ^= v`? — equal numbers cancel because `v ^ v == 0`.
- Why does order not matter? — XOR is commutative and associative, so pairs cancel regardless of position.
- Why does the loner survive? — it is the only value with odd count in the base problem.
- Why isolate one bit for Single Number III? — the two loners differ on that bit, so it separates them into different XOR groups.

## Counting Bits (DP on bits) <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Counting Bits](https://leetcode.com/problems/counting-bits/)*

<ProgressCheck id="counting-bits-dp-on-bits" />

### Problem
For every number `0 … n`, return how many **1-bits** it has (its popcount), in O(n).

**Constraints:** `0 ≤ n ≤ 10⁵`.

**Example 1:** `n = 5` → `[0,1,1,2,1,2]`.

<ExamplePreview compact :input="['5']" :output="['0', '1', '1', '2', '1', '2']" />

**Example 2:** `n = 2` → `[0,1,1]`.

<ExamplePreview compact :input="['2']" :output="['0', '1', '1']" />

### Solution — brute force
Brute force computes the popcount of every integer from `0` to `n` independently, shifting or clearing bits until each number becomes zero. That is O(n log n) time and O(n) output space because each integer may need one step per bit. The optimized DP reuses `i >> 1`: dropping the lowest bit gives a smaller number whose count is already known, then adds `i & 1`.

**Brute-force sketch:**

```text
for i in 0..n:
    count = 0; x = i
    while x != 0: count += x & 1; x >>= 1
```

**Baseline complexity:** O(n log n) time and O(n) output space.

### Solution — optimized
The optimized solution keeps the original Java intact and explains the pattern that removes the brute-force bottleneck.

#### Pattern
`dp[i] = dp[i >> 1] + (i & 1)` — `i` has the bits of `i/2` plus its own lowest bit.

> [key] **Key Insight** — Right-shifting drops the lowest bit, so `popcount(i) = popcount(i/2) + (i & 1)`. This recurrence fills `[0..n]` in O(n) instead of O(n log n) individual counts.

#### Java
```java
int[] countBits(int n) {
    int[] dp = new int[n + 1];
    for (int i = 1; i <= n; i++) dp[i] = dp[i >> 1] + (i & 1);
    return dp;
}
```

> [note] **Trace it** — for `i=5` (`101`): `dp[5] = dp[2] + 1 = 1 + 1 = 2`. Sequence `0..5` → `[0,1,1,2,1,2]`.

<CodeTrace
  title="Counting Bits (Kernighan DP) — n=5"
  :values="[0,1,1,2,1,2]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { dp: 0 }, note: "dp[0] = 0" },
    { pointers: { i: 1 }, vars: { dp: 1, from: "dp[0]+1" }, note: "1 = 0b1: 1 bit", added: [1] },
    { pointers: { i: 2 }, vars: { dp: 1, from: "dp[0]+1" }, note: "2 = 0b10: dp[2gtgt1]+2%2 = 1", added: [2] },
    { pointers: { i: 3 }, vars: { dp: 2, from: "dp[1]+1" }, note: "3 = 0b11: 2 bits", added: [3] },
    { pointers: { i: 4 }, vars: { dp: 1, from: "dp[2]gtgt1 = 0+0" }, note: "4 = 0b100: 1 bit", added: [4] },
    { pointers: { i: 5 }, vars: { dp: 2, from: "dp[2]+1" }, note: "5 = 0b101: dp[5gtgt1]+1%2 = 1+1 = 2", added: [5] }
  ]'
/>

Time O(n) · Space O(n).

> [note] **Interview script** — "I first confirm I need counts for every number from 0 through `n`, not just one number. I start with brute force by popcounting each number separately, which is O(n log n) time and O(n) output space. I optimize with `dp[i] = dp[i >> 1] + (i & 1)`, giving O(n) time and O(n) space."


> [pat] **Pattern Connection** — Alternative recurrence `dp[i] = dp[i & (i-1)] + 1`; both express popcount as a self-DP. Submask enumeration `(s-1) & m` powers *Sum of Subset XOR/AND* and bitmask-DP transitions.

> [trap] **Common Trap** — Recomputing popcount per number. *Example:* naïve `Integer.bitCount(i)` for i=0..n is O(n log n). The DP recurrence `bits[i] = bits[i >> 1] + (i & 1)` reuses the answer for `i/2` → O(n).

<TrapTrace title="Recomputing popcount per number" input="Integer.bitCount(i)" bug="naïve 'Integer.bitCount(i)' for i=0..n is O(n log n). The DP recurrence 'bits[i] = bits[i gtgt 1] + (i & 1)' reuses the answer for 'i/2' → O(n)." fix="See the guidance in the trap description and the code snippet." />

#### Same pattern, new tweaks
Small bit identities each unlock a classic:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | Brian Kernighan's `x &= x - 1` clears the lowest set bit each step | — |
| [Hamming Distance](https://leetcode.com/problems/hamming-distance/) | `Integer.bitCount(a ^ b)` — count differing bits | — |
| [Power of Two](https://leetcode.com/problems/power-of-two/) | `x > 0 && (x & (x-1)) == 0` | — |
| [Reverse Bits](https://leetcode.com/problems/reverse-bits/) | shift bits out of one int and into another, one position at a time | — |

### Time Complexity
O(n): each number from 1 through n is computed once.

### Space Complexity
O(n): the returned `dp` array is the output.

### Learning notes
- Why start the loop at `i = 1`? — `dp[0]` is already 0 by default.
- Why `i >> 1`? — shifting right removes the lowest bit and gives a smaller solved number.
- Why add `(i & 1)`? — the dropped lowest bit contributes one exactly when it is set.
- Why is this DP? — every `dp[i]` reuses the answer for `i/2` instead of recounting bits.
- Why not call `Integer.bitCount` repeatedly in the teaching version? — the recurrence exposes the reusable subproblem and avoids per-number bit loops.

## Subset generation via masks <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Subsets](https://leetcode.com/problems/subsets/)*

<ProgressCheck id="subset-generation-via-masks" />

### Problem
Generate **all subsets** of an `n`-element set by iterating bitmasks `0 … 2ⁿ−1` (bit `i` set = element `i` included).

**Constraints:** `n ≤ 20` so `2ⁿ` is tractable.

**Example 1:** `[a,b,c]` → all 8 subsets, one per bit pattern `000 … 111`.

<ExamplePreview compact :input="['a', 'b', 'c']" :output="['000 … 111']" />

**Example 2:** `[x,y]` → masks `00,01,10,11` → `[[],[x],[y],[x,y]]`.

<ExamplePreview compact :input="['x', 'y']" :output="['00,01,10,11']" />

Enumerate all `2ⁿ` subsets of an `n`-element set by counting masks `0..2ⁿ-1`; bit `i` set means element `i` is included.

### Solution — brute force
Brute force recursively chooses include or exclude for each element and records the subset at the leaf. That is O(n·2ⁿ) time and O(n) recursion depth, which is unavoidable because there are `2ⁿ` subsets to output. The bitmask version is the iterative form of the same idea: every integer mask encodes one subset, making membership checks constant-time bit tests.

**Brute-force sketch:**

```text
dfs(i, path):
    if i == n: record path
    else recurse once excluding a[i] and once including a[i]
```

**Baseline complexity:** O(n·2ⁿ) time and O(n) recursion space excluding output.

### Solution — optimized
The optimized solution keeps the original Java intact and explains the pattern that removes the brute-force bottleneck.

#### Java
```java
List<List<Integer>> subsets(int[] a) {
    int n = a.length;
    List<List<Integer>> res = new ArrayList<>();
    for (int mask = 0; mask < (1 << n); mask++) {
        List<Integer> sub = new ArrayList<>();
        for (int i = 0; i < n; i++)
            if ((mask & (1 << i)) != 0) sub.add(a[i]);
        res.add(sub);
    }
    return res;
}
```

> [note] **Trace it** — `[a,b,c]`. Mask `000`→`{}`, `101`→`{a,c}`, `111`→`{a,b,c}`; counting `0..7` enumerates all **8** subsets, one per bit pattern.

<CodeTrace
  title="Subsets via Bitmask — nums=[a,b,c], enumerate 000..111"
  :values="['a','b','c']"
  :windowKeys="['bit']"
  :cellWidth="52"
  :steps='[
    { pointers: { bit: 0 }, vars: { mask: "000", subset: "{}" }, note: "mask 0: empty set" },
    { pointers: { bit: 0 }, vars: { mask: "001", subset: "{a}" }, note: "mask 1: bit 0 set → a", added: [0] },
    { pointers: { bit: 0 }, vars: { mask: "010", subset: "{b}" }, note: "mask 2: bit 1 → b", added: [1] },
    { pointers: { bit: 0 }, vars: { mask: "011", subset: "{a,b}" }, note: "mask 3: bits 0,1", added: [0,1] },
    { pointers: { bit: 0 }, vars: { mask: "100", subset: "{c}" }, note: "mask 4: bit 2 → c", added: [2] },
    { pointers: { bit: 0 }, vars: { mask: "101", subset: "{a,c}" }, note: "mask 5", added: [0,2] },
    { pointers: { bit: 0 }, vars: { mask: "110", subset: "{b,c}" }, note: "mask 6", added: [1,2] },
    { pointers: { bit: 0 }, vars: { mask: "111", subset: "{a,b,c}" }, note: "mask 7: full set. total 8", added: [0,1,2] }
  ]'
/>

Time O(n·2ⁿ) · Space O(n·2ⁿ).

> [note] **Interview script** — "I first confirm `n` is small enough that outputting all 2ⁿ subsets is intended. I start with brute force include/exclude recursion, which is O(n·2ⁿ) time and O(n) stack space. I optimize the implementation with masks from `0` to `2ⁿ - 1`, keeping O(n·2ⁿ) time and using O(n·2ⁿ) output space."


> [pat] **Pattern Connection** — This iterative masking is the non-recursive twin of backtracking subsets, and the substrate for bitmask DP (*TSP*, *Partition to K Equal Sum Subsets*).

#### Same pattern, new tweaks
Treating an integer as a set of bits:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Subsets](https://leetcode.com/problems/subsets/) | loop masks `0 .. 2ⁿ-1`; bit `i` set means element `i` is included | — |
| [Maximum Product of Word Lengths](https://leetcode.com/problems/maximum-product-of-word-lengths/) | encode each word's letters as a 26-bit mask; two words share no letter iff `maskA & maskB == 0` | — |
| [Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) | DP over the mask of used elements, tracking the current bucket's fill | — |
| [Sum of All Subset XOR / SOS DP](https://leetcode.com/problems/sum-of-all-subset-xor-totals/) | enumerate submasks with `for (s = m; s > 0; s = (s-1) & m)` | — |

### Time Complexity
O(n·2ⁿ): 2ⁿ masks and up to n bit tests per mask.

### Space Complexity
O(n·2ⁿ) for output; O(n) temporary subset per mask.

### Learning notes
- Why `(1 << n)` masks? — n bits encode every include/exclude choice, so there are 2ⁿ subsets.
- Why bit `i` means element `i`? — it gives O(1) membership testing for that element.
- Why `(mask & (1 << i)) != 0`? — the expression tests whether the subset includes index `i`.
- Why create a new `sub` for each mask? — each output subset needs its own list object.
- Why cap this around `n ≤ 20`? — 2ⁿ output size explodes beyond interview-feasible limits.

---

## Check your understanding

<Quiz
  pattern-id="bit-manip"
  :questions='[{"q": "What does `n & (n-1)` do?", "choices": [{"text": "Clears the lowest set bit", "correct": true, "explanation": "Foundation for Kernighan’s popcount and power-of-2 tests."}, {"text": "Sets the lowest bit", "correct": false}, {"text": "Flips all bits", "correct": false}, {"text": "Nothing", "correct": false}]}, {"q": "How do you test if n is a power of 2?", "choices": [{"text": "n > 0 && (n & (n-1)) == 0", "correct": true, "explanation": "Exactly one bit set."}, {"text": "n % 2 == 0", "correct": false, "explanation": "Even, not power of 2."}, {"text": "n / 2 == 0", "correct": false}, {"text": "log2(n) is integer", "correct": false, "explanation": "Works but FP-risky."}]}, {"q": "XOR of all numbers 0..n missing exactly one equals:", "choices": [{"text": "The missing number", "correct": true, "explanation": "Pairs cancel; missing survives."}, {"text": "0", "correct": false}, {"text": "n", "correct": false}, {"text": "Sum(0..n) - sum(nums)", "correct": false, "explanation": "That is Gauss sum, works too but overflow risk."}]}, {"q": "For subset enumeration on n ≤ 20 items, what pattern is used?", "choices": [{"text": "Iterate mask 0..(1<<n)-1; bit i set means item i chosen", "correct": true, "explanation": "Bitmask enumeration; often paired with DP."}, {"text": "Recursion only", "correct": false, "explanation": "Works but slower."}, {"text": "Sort", "correct": false}, {"text": "HashSet", "correct": false}]}, {"q": "For Maximum Product of Word Lengths, how do you check \"no shared letter\" in O(1)?", "choices": [{"text": "26-bit mask per word; `mask[i] & mask[j] == 0`", "correct": true, "explanation": "Single AND is O(1) regardless of word length."}, {"text": "Iterate every character", "correct": false, "explanation": "O(L) per pair."}, {"text": "HashSet intersection", "correct": false, "explanation": "Works but slower."}, {"text": "Sort both words", "correct": false}]}]'
/>

<PrintButton />

<RelatedPatterns pattern-id="bit-manip" />
