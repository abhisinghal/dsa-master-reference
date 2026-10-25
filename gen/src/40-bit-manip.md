# Bit Manipulation


<PatternVideo pattern-name="Bit Manipulation" duration="8–12 min" />

<PatternProgress pattern-id="bit-manip" problems="single-number, missing-number, find-the-difference, number-of-1-bits, hamming-distance, power-of-two, reverse-bits, maximum-product-of-word-lengths, sum-of-all-subset-xor-totals, subsets" />

<script setup>
const theTemplateCode = `// The bit-manip "template" is really a catalog of identities.
// Memorize these and 90% of problems collapse to one line.
int lowBit        = x & -x;              // isolate the lowest set bit
int clearLowest   = x & (x - 1);         // clear the lowest set bit
boolean kthBit    = ((x >> k) & 1) == 1; // read bit k
int setK          = x | (1 << k);        // set bit k
int clearK        = x & ~(1 << k);       // clear bit k
int toggleK       = x ^ (1 << k);        // toggle bit k
int bits          = Integer.bitCount(x); // hardware popcnt (~1ns)
// XOR cancellation: a ^ a == 0, a ^ 0 == a, XOR is commutative and associative`

const theTemplateInvariant = {
  statement: `A bit-manipulation algorithm maintains an INTEGER as the whole state. Each identity (AND / OR / XOR / shift) transforms the state in O(1), and the algorithm's correctness rests on a loop invariant stated over the bits of that integer — "after step i, bits 0..i-1 are correct" or "after step i, running XOR cancels every value seen an even number of times".`,
  initialization: `Start with 0 (XOR identity) or ~0 / (1 << n) - 1 (all-bits-set complement). The initial value is the identity element of the dominant operation.`,
  maintenance: `Each step applies one identity to update the integer. The invariant is a per-bit claim (bit k is correct) or a cross-bit claim (popcount parity, lowest set bit position).`,
  termination: `When the loop exits, the integer holds the answer — the surviving XOR, the counted bit, or the final mask. No separate "extract" step needed.`
}

const theTemplateComplexity = {
  time: `O(1) per identity · O(n) for a one-pass over an array · O(2^n) for enumerating all subset masks`,
  space: `O(1) — the integer IS the state`
}

const theTemplateSpecializations = [
  { slug: `isolate-the-low-bit-easy`,           title: `Isolate the low bit (easy)` },
  { slug: `single-number-xor-easy`,             title: `Single Number (XOR) (easy)` },
  { slug: `single-number-ii-easy`,              title: `Single Number II (easy)` },
  { slug: `single-number-iii-easy`,             title: `Single Number III (easy)` },
  { slug: `counting-bits-easy`,                 title: `Counting Bits (easy)` },
  { slug: `reverse-bits-easy`,                  title: `Reverse Bits (easy)` },
  { slug: `power-of-two-easy`,                  title: `Power of Two (easy)` },
  { slug: `subset-generation-via-masks-medium`, title: `Subset generation (medium)` },
  { slug: `swap-without-temp-easy`,             title: `Swap without temp (easy)` },
]

const theTemplateProblemShape = `Operations on sets, flags, or integers that reduce to a sequence of AND / OR / XOR / shift primitives — each O(1) on hardware, each with a one-line identity.`

const lowBitCode = `// Isolate the lowest set bit — the ur-bit-trick.
// How it works: two's-complement means -x = ~x + 1 bit-for-bit.
// So x & -x keeps only the lowest 1-bit (everything else flipped).
int lowBit(int x) {
    return x & -x;
}

// Example: x = 0b1011_0000 → low = 0b0001_0000
// Example: x = 0b0000_1100 → low = 0b0000_0100
// Example: x = 0 → low = 0 (no set bits)

// Common uses:
// - popcount via loop: while (x != 0) { x ^= lowBit(x); count++; }
// - Fenwick (BIT) traversal: i += i & -i
// - clear lowest set bit:   x & (x - 1)  (the complementary identity)`

const reverseBitsCode = `// Reverse the 32 bits of an unsigned integer.
// Approach: butterfly-swap halves/quarters/eighths/sixteenths with precomputed masks.
int reverseBits(int n) {
    n = ((n & 0xFFFF0000) >>> 16) | ((n & 0x0000FFFF) << 16);
    n = ((n & 0xFF00FF00) >>> 8)  | ((n & 0x00FF00FF) << 8);
    n = ((n & 0xF0F0F0F0) >>> 4)  | ((n & 0x0F0F0F0F) << 4);
    n = ((n & 0xCCCCCCCC) >>> 2)  | ((n & 0x33333333) << 2);
    n = ((n & 0xAAAAAAAA) >>> 1)  | ((n & 0x55555555) << 1);
    return n;
}
// O(1) in operations (5 masks, 10 shifts, 5 ORs).
// Note the >>> (unsigned shift) — >> would propagate the sign bit and corrupt the result.`

const powerOfTwoCode = `// Is x a power of two? (positive integer only)
boolean isPowerOfTwo(int x) {
    return x > 0 && (x & (x - 1)) == 0;
}
// Logic: a power of two has exactly ONE set bit. x & (x-1) clears the lowest set bit;
// if the result is 0, x had exactly one set bit. The x > 0 guard excludes 0 and negatives.

// Example: x = 8 = 0b1000, x - 1 = 7 = 0b0111, x & (x-1) = 0 ✓
// Example: x = 6 = 0b0110, x - 1 = 5 = 0b0101, x & (x-1) = 0b0100 ≠ 0 ✗
// Example: x = 0 → 0 > 0 fails, returns false ✓
// Example: x = -8 → -8 > 0 fails, returns false ✓ (two's complement of -8 has bit-31 set)`

const swapNoTempCode = `// Swap two integers without a temporary variable.
void swap(int[] a, int i, int j) {
    if (i == j) return;                   // CRITICAL — otherwise a[i] gets zeroed
    a[i] ^= a[j];                         // a[i] = a[i] ^ a[j]
    a[j] ^= a[i];                         // a[j] = a[j] ^ (a[i] ^ a[j]) = a[i]
    a[i] ^= a[j];                         // a[i] = (a[i] ^ a[j]) ^ a[i] = a[j]
}

// Why the i == j guard matters:
// If i == j, the first line sets a[i] = a[i] ^ a[i] = 0.
// Then a[j] = 0, a[i] = 0. The original value is destroyed.
// Interview-day failure if omitted.

// In practice: never use this in production code — modern CPUs do swap with
// one XCHG instruction, and a temp-based swap is clearer. Only interesting
// as a brainteaser or in constrained-memory assembly.`

const singleNumberXorCode = `// Single Number: every element appears twice except one; find the loner.
int singleNumber(int[] nums) {
    int x = 0;
    for (int n : nums) x ^= n;            // duplicates cancel, loner survives
    return x;
}
// O(n) time, O(1) space. Beats HashSet (O(n) space).
// Correctness: XOR is commutative + associative + self-inverse, so pairs cancel
// regardless of order.`

const singleNumberIICode = `// Single Number II: every element appears THREE times except one; find the loner.
// Approach: for each bit position, count occurrences across all nums. The loner's
// bit is 1 iff its count mod 3 is 1.
int singleNumberII(int[] nums) {
    int ones = 0, twos = 0;
    for (int n : nums) {
        ones = (ones ^ n) & ~twos;        // bit set in 'ones' iff seen 1 (mod 3) times
        twos = (twos ^ n) & ~ones;        // bit set in 'twos' iff seen 2 (mod 3) times
    }
    return ones;                          // bits seen 3 (mod 3) == 0 times vanish from both
}
// O(n) time, O(1) space. Beats bit-by-bit counting (O(32n) time).`

const singleNumberIIICode = `// Single Number III: every element appears twice EXCEPT two distinct loners; find both.
// Approach: XOR all → result is a ^ b where a, b are the two loners. a != b implies
// a ^ b has at least one set bit — pick any one (the lowest) as a discriminator.
// Partition nums into two groups by that bit; XOR each group separately.
int[] singleNumberIII(int[] nums) {
    int xor = 0;
    for (int n : nums) xor ^= n;
    int diff = xor & -xor;                // lowest set bit — a differs from b here
    int a = 0, b = 0;
    for (int n : nums) {
        if ((n & diff) == 0) a ^= n;      // group where this bit is 0
        else                 b ^= n;      // group where this bit is 1
    }
    return new int[]{a, b};
}
// O(n) time, O(1) space. Each loner is isolated in its own group; duplicates cancel.`

const mastery5 = [
  {
    q: `Why does XOR cancellation (ones ^= n for every n) solve "Single Number" (every other element appears twice)?`,
    choices: [
      { text: `XOR is commutative, associative, and self-inverse: x ^ x = 0, so duplicate pairs cancel regardless of order`, correct: true, explanation: `This is the entire theorem. Reorder the array into pairs + loner: pairs cancel to 0, loner stays.` },
      { text: `XOR is a hash function with no collisions`, correct: false, explanation: `XOR has many collisions (a ^ b = c ^ d is common).` },
      { text: `The problem guarantees unique values`, correct: false, explanation: `There are duplicates — that's the whole premise.` },
      { text: `By coincidence; it only works for powers of two`, correct: false }
    ]
  },
  {
    q: `What does x & -x compute, and why?`,
    choices: [
      { text: `The lowest set bit of x — because in two's complement, -x inverts bits above the lowest 1 and keeps the lowest 1 set`, correct: true, explanation: `Specifically -x = ~x + 1. AND-ing with x isolates only the single bit position where both agree, which is the lowest 1 of x.` },
      { text: `The absolute value of x`, correct: false, explanation: `Math.abs doesn't use bit tricks for arbitrary x.` },
      { text: `The highest set bit`, correct: false, explanation: `Lowest, not highest. Highest set bit needs Integer.highestOneBit.` },
      { text: `Nothing meaningful`, correct: false }
    ]
  },
  {
    q: `Why does Java's "1 << 31" give a NEGATIVE number?`,
    choices: [
      { text: `int is signed 32-bit; bit 31 is the sign bit. 1 << 31 = 0x80000000 = Integer.MIN_VALUE`, correct: true, explanation: `Use 1L << 31 to get 2^31 as a long.` },
      { text: `Shifts always produce negatives`, correct: false },
      { text: `Java has a bug in <<`, correct: false },
      { text: `It's a floating-point rounding error`, correct: false, explanation: `No floats involved.` }
    ]
  },
  {
    q: `For the XOR swap (a[i] ^= a[j]; a[j] ^= a[i]; a[i] ^= a[j]), what fails if i == j?`,
    choices: [
      { text: `The first line sets a[i] = 0 (self-XOR), destroying the value — subsequent XORs can't recover it`, correct: true, explanation: `Always guard with if (i == j) return; before the three-step swap.` },
      { text: `An ArithmeticException`, correct: false, explanation: `XOR of two ints is total — never throws.` },
      { text: `An infinite loop`, correct: false, explanation: `The swap is straight-line.` },
      { text: `Nothing — Java has special-case handling for i == j`, correct: false }
    ]
  },
  {
    q: `In Single Number II (every element appears 3× except one), the two-state (ones, twos) trick computes:`,
    choices: [
      { text: `For each bit position, the count mod 3 of occurrences — using 'ones' + 'twos' as a 2-bit counter per position`, correct: true, explanation: `Base-3 counting via two base-2 variables; third occurrence resets both. The loner's bits persist in 'ones'.` },
      { text: `A hash of all seen values`, correct: false },
      { text: `The XOR of alternating elements`, correct: false, explanation: `That solves Single Number I, not II.` },
      { text: `A sum modulo 3`, correct: false, explanation: `Would overflow for large values.` }
    ]
  }
]
</script>



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

## THE template — the identity catalog

<PatternTemplateCard
  slug="bit-manip"
  title="Bit Manipulation"
  language="java"
  :code="theTemplateCode"
  :invariant="theTemplateInvariant"
  :complexity="theTemplateComplexity"
  :specializations="theTemplateSpecializations"
  :problemShape="theTemplateProblemShape"
/>

<InvariantProof
  :statement="theTemplateInvariant.statement"
  :initialization="theTemplateInvariant.initialization"
  :maintenance="theTemplateInvariant.maintenance"
  :termination="theTemplateInvariant.termination"
/>

### The identities in one place

The sub-variations below are each a one-identity theorem. Memorize these and 90% of bit-trick interview questions collapse to one line.

| Operation | Identity | Example |
|---|---|---|
| Isolate low bit | `x & -x` | `0b1010 → 0b0010` |
| Clear low bit | `x & (x - 1)` | `0b1010 → 0b1000` |
| Set bit k | `x | (1 << k)` | `0b0000 | 1<<2 → 0b0100` |
| Clear bit k | `x & ~(1 << k)` | `0b1111 & ~(1<<2) → 0b1011` |
| Toggle bit k | `x ^ (1 << k)` | `0b1010 ^ 1<<1 → 0b1000` |
| Read bit k | `(x >> k) & 1` | reads bit at position k |
| Hardware popcount | `Integer.bitCount(x)` | 1 CPU cycle on x86-64 |

**Iterate subsets of a mask (3^n total work across all masks):**
```java
for (int sub = mask; sub != 0; sub = (sub - 1) & mask) { /* ... */ }
```

### Complexity reference

| Operation | Time | Space |
|---|---|---|
| Read/set/clear/toggle bit | O(1) | O(1) |
| Popcount (Kernighan loop) | O(popcount) | O(1) |
| Popcount (hardware) | O(1) | O(1) |
| Iterate subsets of mask | O(2^popcount) per mask | O(1) |
| Bitmask DP (TSP-style) | O(2^n · n^2) | O(2^n · n) |
| XOR-cancellation | O(n) | O(1) |

## When the mechanic breaks — three failure modes

<TrapTrace
  title="Signed vs. unsigned shift"
  bug="In Java, >> preserves the sign bit: -1 >> 1 == -1 (fills with 1s). For negative numbers passed into bit-counting or reverse-bits logic, >> propagates the sign and never terminates (or returns wrong). Reverse Bits with >> on bit 31 corrupts every lower result."
  fix="Use >>> (unsigned shift, zero-fills) whenever the value could be negative OR you're treating it as a bitmask. The one exception: arithmetic right-shift (dividing by 2^k with sign preservation) — then >> is correct. Rule: if the semantics are 'bitmask', use >>>."
/>

<TrapTrace
  title="1 << 31 overflow and operator precedence"
  bug="Two bugs that corrupt silently: (1) 1 << 31 is Integer.MIN_VALUE, not 2^31 — if you need the positive value, use 1L << 31. (2) if (x & mask == 0) parses as if (x & (mask == 0)) because == binds tighter than & — the compiler flags the type mismatch, but if the expression is in a context where booleans auto-convert, it compiles and silently returns wrong."
  fix="For (1): use long whenever a shift result might reach bit 31+. For (2): ALWAYS parenthesize bitwise comparisons: if ((x & mask) == 0). The parentheses are not optional — operator precedence is the single biggest source of bit-manip bugs in Java/C/C++."
/>

<TrapTrace
  title="XOR swap without the i == j guard"
  bug="The three-line XOR swap (a[i] ^= a[j]; a[j] ^= a[i]; a[i] ^= a[j]) destroys the value when i == j: first line sets a[i] = a[i] ^ a[i] = 0, and the rest cannot recover it. Common surprise in in-place algorithms that call swap(a, i, j) without checking indices."
  fix="Guard with if (i == j) return; at the top of swap. In practice, don't use XOR swap in production: modern CPUs have an XCHG instruction, and a temp-based swap is clearer. XOR swap is a brainteaser, not an optimization."
/>

## History — Kernighan's popcount trick (1988) and popcnt hardware (2000)

The bit-clearing trick `x & (x - 1)` was popularized by **Brian Kernighan** in his 1988 book *The C Programming Language* (2nd ed., co-authored with Dennis Ritchie). The trick appears in an exercise: count the number of 1-bits in an integer *in time proportional to the number of 1-bits*, not the number of bits. It's still the fastest software approach on architectures without native popcount.

In **2000**, Intel added the `popcnt` instruction as part of SSE4.2 — a single-cycle hardware popcount. AMD followed in 2006. Java's `Integer.bitCount()` compiles to this instruction on modern JVMs, making bit counting effectively free. Every LLVM-compiled bit-heavy algorithm (Bloom filter, geohash, HyperLogLog) uses it.

**Cryptography** has always been the largest consumer of bit tricks: SHA-256 mixes bits via 64 rounds of XOR, AND, OR, rotates, and additions. AES uses `xtime` — a specific `<< 1 XOR 0x1b` operation — to walk finite-field elements. In the compiler world, **register allocation** uses bitmask interference graphs to decide which variables can share a register.

Google's **Roaring Bitmap** (2013) is a compressed bitmap format used in Apache Lucene, Elasticsearch, Druid, Spark, and Snowflake for indexing sparse boolean columns. It combines the ideas from this chapter — bit tricks, bitmask iteration, popcount — into a real production data structure that indexes trillion-row datasets.

## Sub-variations of the template

<PatternSubVariationNav pattern="bit-manip" />

### Isolate the Low Bit <span class="diff diff-e">Easy</span>

The bare mechanic — one identity, one line. **`x & -x` returns the integer with only the lowest set bit of `x` kept, all other bits zeroed.**

> [key] Isolate the lowest set bit in O(1).

<TemplateReveal
  slug="low-bit"
  language="java"
  :canonical="lowBitCode"
/>

#### Why it works

In two's-complement representation, `-x = ~x + 1`. Walk from the lowest bit upward:
1. Bits strictly below the lowest set bit of `x`: in `x` they are 0; in `~x` they are 1; adding 1 to `~x` propagates a carry through them, flipping them back to 0.
2. The lowest set bit of `x`: in `x` it is 1; in `~x` it is 0; the carry from below flips it to 1 in `-x`.
3. Bits strictly above: in `x` the value; in `~x` the complement; adding 1 doesn't propagate past the lowest 1, so they stay complemented in `-x`.

Hence `x` and `-x` agree only on the lowest set bit; `x & -x` keeps it.

**Production uses:**
- **Fenwick tree (BIT) traversal** — `i += i & -i` for prefix sum, `i -= i & -i` for update. Every competitive-programming BIT.
- **`Integer.lowestOneBit(x)`** in Java 1.5+ compiles to exactly this.
- **Popcount via Kernighan loop** — `while (x != 0) { x ^= x & -x; count++; }` iterates once per set bit.

---

<details>
<summary><strong>Historical: the Single Number 3-approach ladder (HashSet → Sort → XOR)</strong></summary>

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

</details>

### Single Number (XOR) <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Single Number](https://leetcode.com/problems/single-number/)*

The ur-XOR-cancellation. Every element appears twice except one; find the loner in O(n) time, O(1) space.

> [key] Find the unique number in an array where every other number appears twice.

<TemplateReveal
  slug="single-number-xor"
  language="java"
  :canonical="singleNumberXorCode"
/>

> [inv] **Invariant** — At every iteration, running `x` equals the XOR of all values seen so far. Pairs cancel (`a ^ a = 0`); after the full sweep, only the loner remains.

**Trace** — `nums = [4,1,2,1,2]`. XOR accumulator: `0 → 4 → 5 → 7 → 6 → 4`. Pairs `1^1` and `2^2` cancel; the loner `4` survives.

**Complexity:** O(n) time, O(1) space. Strictly beats HashSet (O(n) space).

**Companion problems:**
- [Missing Number](https://leetcode.com/problems/missing-number/) — XOR all values 0..n AND all input values; the missing one is the XOR survivor.
- [Find the Difference](https://leetcode.com/problems/find-the-difference/) — same mechanic with chars.

### Core identities reference

**Grokking arc:** The motivating problem is representing tiny sets, parity, or binary properties without bulky data structures.

#### Core identities
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

### Single Number II <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Single Number II](https://leetcode.com/problems/single-number-ii/)*

Every element appears **three** times except one. Find the loner.

#### The move — base-3 counting in two base-2 variables

For each bit position, we want to know "mod 3, how often has this bit been set?" If a bit's count is 1 mod 3, that bit belongs to the loner; else it's part of a triple that cancels. Build this per-bit mod-3 counter using two int variables (`ones`, `twos`) that together track 2-bit per-position state (0, 1, or 2 — the third set resets).

> [key] Find the unique number where every other appears three times.

<TemplateReveal
  slug="single-number-ii"
  language="java"
  :canonical="singleNumberIICode"
/>

**State table per bit:** after seeing a bit `b`:
- Prev `(ones, twos) = (0, 0)`, `b = 1`: `(ones, twos) → (1, 0)` — seen once.
- Prev `(1, 0)`, `b = 1`: `(ones, twos) → (0, 1)` — seen twice.
- Prev `(0, 1)`, `b = 1`: `(ones, twos) → (0, 0)` — seen three times, both reset.

The two formulas `ones = (ones ^ b) & ~twos` and `twos = (twos ^ b) & ~ones` encode this truth table exactly.

**Complexity:** O(n) time, O(1) space. Beats bit-by-bit counting (O(32n)) because the whole 32-bit state updates per element.

**Generalization — "every element appears K times except one":** maintain `K-1` state variables and apply the same per-bit mod-K counting. For non-prime K, you can also sort + grab-every-Kth. See LeetCode Discuss for the finite-automaton derivation.

<ProgressCheck id="single-number-i-ii-iii-xor" />

```svg
<svg role="img" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" aria-label="Diagram illustrating: Single Number I / II / III (XOR) Easy">
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

### Single Number III <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Single Number III](https://leetcode.com/problems/single-number-iii/)*

Every element appears twice except **two distinct** loners. Return both (any order).

#### The move — XOR all, then split by one differing bit

XOR-ing everything gives `a ^ b` (duplicates cancel; the two loners are the only odd-count values). Since `a ≠ b`, `a ^ b` has at least one set bit — pick any (lowest is cheapest via `x & -x`). That bit is 0 in one loner and 1 in the other. Partition the input by that bit and XOR each partition separately — each loner is now alone in its group; duplicates still cancel inside their group.

> [key] Find the two unique numbers where every other appears twice.

<TemplateReveal
  slug="single-number-iii"
  language="java"
  :canonical="singleNumberIIICode"
/>

**Trace** — `nums = [1,2,1,3,2,5]`. XOR all = `3 ^ 5 = 6 = 0b110`. Lowest set bit of 6 is `2 = 0b010`. Partition: group where bit 1 is 0 = `[1,1,5]` → XOR = `5`. Group where bit 1 is 1 = `[2,2,3]` → XOR = `3`. Return `[5, 3]`.

**Complexity:** O(n) time, O(1) space.

**Companion:** [Missing Numbers I/II](https://leetcode.com/problems/missing-number/) — same mechanic, but XOR against 0..n to find the missing one.

### Counting Bits <span class="diff diff-e">Easy</span>

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

### Reverse Bits <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Reverse Bits](https://leetcode.com/problems/reverse-bits/)*

Reverse the 32 bits of an unsigned integer. The butterfly-swap approach does it in O(1) operations (5 masks, 10 shifts, 5 ORs) — strictly better than a 32-iteration loop.

> [key] Reverse the 32 bits of an unsigned integer.

<TemplateReveal
  slug="reverse-bits"
  language="java"
  :canonical="reverseBitsCode"
/>

**Why it works** — each line swaps `n`-bit halves at a given granularity. First line swaps the two 16-bit halves. Second swaps 8-bit halves within each 16-bit half. And so on down to adjacent bits (`0xAAAAAAAA / 0x55555555`). After five halving stages, every bit has moved to its mirror position.

**Trap: use `>>>` not `>>`** — `>>` propagates the sign bit; on a negative input (bit 31 set) the first stage would corrupt bits by filling in 1s instead of 0s.

### Power of Two <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Power of Two](https://leetcode.com/problems/power-of-two/)*

A positive integer is a power of two iff it has **exactly one set bit**. `x & (x - 1)` clears the lowest set bit; if the result is 0, the input had exactly one. One line.

> [key] Determine if an integer is a positive power of two in O(1).

<TemplateReveal
  slug="power-of-two"
  language="java"
  :canonical="powerOfTwoCode"
/>

**Variations** — "is `x` a power of four?" → `x > 0 && (x & (x-1)) == 0 && (x & 0x55555555) != 0`. The second AND requires the single set bit to be at an even position.

### Swap Without Temp <span class="diff diff-e">Easy</span>

The XOR-swap brainteaser. Three XORs swap two integers with no temp — but destroys the value when both indices are the same.

> [key] Swap two integers using only XOR; guard against the self-swap trap.

<TemplateReveal
  slug="swap-no-temp"
  language="java"
  :canonical="swapNoTempCode"
/>

**Production verdict:** don't use this in real code. Modern CPUs do swap in one `XCHG` instruction; a temp-based swap compiles to the same thing with better clarity. XOR-swap is an interview brainteaser about understanding XOR self-cancellation plus edge cases — not an optimization.

### Subset generation via masks <span class="diff diff-m">Medium</span>

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

## In the wild — JDK `Integer.bitCount` with `popcnt` intrinsic

Java's `Integer.bitCount(int)` is the production path for popcount. The source in `java.base/share/classes/java/lang/Integer.java` is a well-known **SWAR (SIMD Within A Register)** algorithm:

```java
/* java.base/share/classes/java/lang/Integer.java (JDK 21) */
public static int bitCount(int i) {
    // HD, Figure 5-2
    i = i - ((i >>> 1) & 0x55555555);                              // pairs of bits summed
    i = (i & 0x33333333) + ((i >>> 2) & 0x33333333);               // nibbles summed
    i = (i + (i >>> 4)) & 0x0f0f0f0f;                              // bytes summed
    return (i * 0x01010101) >>> 24;                                // high byte is total
}
```

**Why `(i * 0x01010101) >>> 24`?** The multiply-and-shift trick: multiplying by `0x01010101` adds four byte-sized counts into the high byte. The shift extracts it. One multiply replaces three adds.

**And then the HotSpot JIT replaces the whole thing** with a single `POPCNT` instruction when the CPU supports it (`-XX:UseCountTrailingZerosInstruction` is on by default on x86-64 since 2010). The Java bytecode calls `Integer.bitCount`; the native generated code emits one instruction. The library implementation is only used on CPUs lacking POPCNT (rare).

**Other production bit-manip:**
1. **Roaring Bitmaps (2013)** — Apache Lucene, Elasticsearch, Druid, Spark, Snowflake use roaring bitmaps for sparse boolean columns. Each container is a bitmap or sorted array; union/intersection use SIMD-accelerated bit operations. Google's benchmarks: 10×–100× faster than `java.util.BitSet`.
2. **Linux's `__builtin_ctz` / `__builtin_clz`** (count trailing / leading zeros) compile to `BSF`/`BSR` x86 instructions. Used in every bitmap allocator, every low-level graph algorithm.
3. **TCP's window-scale option** — the receiving window is a 16-bit value scaled by `1 << scale` (negotiated during handshake). All receive-window updates are literal `<< scale` operations in the kernel.
4. **Chrome's V8 small-integer representation (SMIs)** — JS numbers that fit in 31 bits are tagged by the low bit. Every arithmetic operation does a bit-check on the tag; this is how V8 avoids boxing for integer arithmetic.

## When NOT to use it

- **n > 25 or so** — 2^25 = 33M is barely tractable; 2^30 = 10^9 explodes. Bitmask DP over subsets is dead beyond that.
- **The set has real semantic complexity** — bit manipulation shines when set membership is a clean boolean. If you need weights, counts, or ordering, use `HashMap` or `SortedSet`.
- **Bit tricks that yield the same asymptotic complexity as a HashSet** — cleverness has readability cost. Only reach for the trick when the O(1) bitmap operation is genuinely a bottleneck win.
- **You're solving a real cryptographic problem** — the identities here are the *building blocks*, not the algorithm. Roll your own crypto with these primitives and you'll ship a vulnerability.
- **Cross-language / cross-platform code where signed/unsigned mismatch matters** — Java's signed shifts differ from C's, from JavaScript's, from Python's arbitrary-precision. Bit-level code doesn't port cleanly.
- **A team member cannot read the code in 30 seconds** — comment aggressively or use a helper method. Bit tricks are a maintainability tax.

## Recognition drill

<RecognitionDrill pattern="bit-manip" :count="10" />

## Advanced — follow-ups and failure modes

<details>
<summary><strong>What if the problem is "find K unique numbers where every other appears M times"?</strong></summary>

Generalize Single Number II/III:
- **M = 2, K = 1** → XOR all, result is the loner.
- **M = 2, K = 2** → XOR all, split by one differing bit (Single Number III).
- **M = 3, K = 1** → base-3 counting with 2 int variables (Single Number II).
- **M = K = anything** → bit-by-bit counting: for each bit position, count occurrences across all `n`; divide by `M` and look at the remainder.

The specialized versions are O(n) time + O(1) space; the generic O(32n) bit-by-bit is always available as a fallback.
</details>

<details>
<summary><strong>What if you need popcount on a 64-bit integer in Java?</strong></summary>

`Long.bitCount(long)` is the direct answer — same SWAR algorithm extended to 64 bits, compiled to `POPCNT r64` on x86-64. 2-3 ns.

If you're on a platform without hardware popcount (ARM Cortex-M, old MIPS), hand-write the SWAR version — never loop. For arrays of longs, `java.util.stream.LongStream.of(arr).map(Long::bitCount).sum()` auto-vectorizes with Vector API in recent JDKs.
</details>

<details>
<summary><strong>What if the bitmask doesn't fit in 64 bits (n > 64)?</strong></summary>

Use `java.util.BitSet` for arbitrary-size bitmaps. It's a long[] under the hood with the same identities — `and`, `or`, `xor`, `cardinality` (popcount), `nextSetBit`. For sparse bitmaps use **Roaring Bitmaps** (3rd-party RoaringBitmap library); for compressed storage with fast ops.

For bitmask DP where `n > 32`, split the mask into high and low halves and store `dp[maskHi][maskLo][...]`. Memory explodes fast; `n ≤ 25` is the practical ceiling.
</details>

<details>
<summary><strong>What if the problem wants the HIGHEST set bit, not the lowest?</strong></summary>

`Integer.highestOneBit(x)` returns the integer with only the highest set bit kept. It compiles to `BSR` (bit scan reverse) on x86-64.

For log₂(x) rounded down: `31 - Integer.numberOfLeadingZeros(x)`. Faster than `Math.log(x) / Math.log(2)` and exact.

For "round up to next power of 2": there's a classic sequence `x--; x |= x >> 1; x |= x >> 2; x |= x >> 4; x |= x >> 8; x |= x >> 16; x++;` — fills all bits below the highest set bit, then adds 1. O(1), no branches.
</details>

<details>
<summary><strong>What if performance matters and you need SIMD-level popcount throughput?</strong></summary>

For arrays of integers, batch popcount with Harley-Seal's algorithm or AVX-512's `VPOPCNTQ` (counts popcount of 8 longs in parallel). HotSpot's Vector API (JDK 16+) exposes these. Benchmark before: for arrays < 100 ints, scalar `Integer.bitCount` wins due to overhead.

Papers to read: Mula/Lemire 2016 "Faster Population Counts Using AVX2 Instructions." Used in Lemire's SIMDJson parser for CSV-counting commas and quotes.
</details>

### Breaking point

Bit manipulation **stops being useful** when:
- `n > 25` and the algorithm is bitmask DP — 2^n explodes.
- The set membership has structure (ordering, counts) that `bool` can't capture.
- Cross-language code where signed/unsigned semantics differ — bugs that only show up on specific inputs.
- The team can't read the trick in 30 seconds — the maintainability tax exceeds the perf win.

### Three cross-pattern problems

- [Sum of Two Integers](https://leetcode.com/problems/sum-of-two-integers/) — no `+`/`-` allowed; implement full-adder via XOR + AND + shift.
- [Maximum Product of Word Lengths](https://leetcode.com/problems/maximum-product-of-word-lengths/) — 26-bit mask per word; `mask[i] & mask[j] == 0` iff words share no letters.
- [Bitwise AND of Numbers Range](https://leetcode.com/problems/bitwise-and-of-numbers-range/) — classical trick: find the common prefix of `m` and `n` by right-shifting until they match, then left-shift back.

---

## Check your understanding

<Quiz pattern-id="bit-manip" :questions="mastery5" />

<PrintButton />

<RelatedPatterns pattern-id="bit-manip" />
