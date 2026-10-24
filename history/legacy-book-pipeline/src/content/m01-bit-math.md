## Concepts & Mental Models

Bits are the substrate everything else is built on. For a senior engineer the value of this module is not the party tricks \u2014 it is developing a **second mental model of integers**: not as quantities, but as *fixed-width vectors of boolean flags* you can test, set, and combine in O(1).

Two ideas unlock almost every bit problem:

!!! key "The two levers of bit manipulation"
    **1. A bit is an independent boolean.** `x & (1 << i)` tests flag `i`; the 32 bits of an `int` are 32 parallel booleans you can process simultaneously.
    **2. XOR is addition without carry.** `a ^ a = 0`, `a ^ 0 = a`, and XOR is commutative & associative. That means XOR *cancels pairs and preserves order-independence* \u2014 the engine behind an entire family of "find the lonely element" problems.

### The operator toolkit

| Expression | Meaning | Typical use |
|---|---|---|
| `x & (1 << i)` | test bit `i` | membership in a bitmask set |
| `x \| (1 << i)` | set bit `i` | add element to bitmask |
| `x & ~(1 << i)` | clear bit `i` | remove element |
| `x ^ (1 << i)` | flip bit `i` | toggle |
| `x & (x - 1)` | clear lowest set bit | count set bits (Brian Kernighan) |
| `x & (-x)` | isolate lowest set bit | Fenwick trees, lowbit |
| `x & (x - 1) == 0` | is power of two | (for `x > 0`) |

!!! complexity "Why this matters for complexity"
    Every operation above is a single CPU instruction. Replacing a `HashSet<Integer>` of small integers with a 32- or 64-bit mask collapses O(n) membership state into O(1) space and O(1) tests \u2014 the core idea behind **bitmask DP** (Pattern 15).

This module covers: power sets via bits, the Sieve of Eratosthenes, the Single Number family, Counting Bits, and Missing Number via XOR. We treat **Single Number II** in full because it teaches a technique \u2014 *per-bit modular counting* \u2014 that generalizes far beyond the specific problem.

---

## Single Number

!!! pattern "Pattern: XOR cancellation \u00b7 T: O(n) \u00b7 S: O(1)"
    **Signals:** "every element appears twice except one", order irrelevant, must be O(1) space.

### 1. The Problem

You are given a non-empty array where **every value appears exactly twice except for one value, which appears once**. Return the single value. The interesting constraint is the follow-up: do it in **linear time and constant extra space**. That constraint is the whole problem \u2014 without it, a hash map is trivial.

### 2. The Intuition

If numbers came in pairs and you could somehow make a pair *annihilate itself*, whatever survived would be the answer. We need an operation where combining a value with itself yields "nothing," and combining with "nothing" is harmless. That is exactly XOR.

### 3. The Naive Approach

Count occurrences in a `HashMap<Integer,Integer>`, then scan for the entry with count 1.

```java
Map<Integer,Integer> freq = new HashMap<>();
for (int x : nums) freq.merge(x, 1, Integer::sum);
for (var e : freq.entrySet()) if (e.getValue() == 1) return e.getKey();
```

Correct, but **O(n) time and O(n) space**. The space violates the follow-up, and boxing every `int` into an `Integer` key is real overhead.

### 4. The Key Observation \ud83d\udd11

!!! key "Key observation"
    XOR of a number with itself is 0, and XOR is commutative and associative. Therefore XOR-ing **every** element together makes all the paired values cancel, leaving only the unique one: `x \u2295 x = 0`, so `(a\u2295a)\u2295(b\u2295b)\u2295c = 0\u22950\u2295c = c`.

### 5. Pattern Recognition

**Signals.** "Appears twice except one," "constant space," "find the element that breaks a pairing." Any time duplicates should *cancel*, think XOR.

**Recognition shortcut.** Ask: *"If I combine matching elements, do I want them to disappear?"* If yes, and the combine is associative/commutative, XOR (or a running parity) is the tool.

**Related problems.** Missing Number, Find the Duplicate (variant), Single Number II & III, detecting a single toggled bit.

### 6. The Invariant

After processing a prefix `nums[0..i]`, the accumulator `ans` equals the XOR of all elements seen so far. Because every fully-paired value contributes 0, `ans` always equals *the XOR of the elements whose pairs have not both appeared yet*. At the end, exactly one element is unpaired, so `ans` is the answer.

### 7. Visual Explanation

```diagram
{"type":"array","title":"XOR accumulates left-to-right; pairs cancel to 0",
 "values":[4,1,2,1,2],
 "highlights":{"0":"amber"},
 "caption":"4 is the only unpaired value; the two 1s and two 2s each XOR to 0."}
```

```diagram
{"type":"bars","title":"Running accumulator ans after each step",
 "values":[4,5,7,6,4],
 "highlights":{"4":"green"},
 "caption":"ans = 4 \u2192 4\u22951=5 \u2192 5\u22952=7 \u2192 7\u22951=6 \u2192 6\u22952=4. Final = 4."}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":430,"box":250,
 "steps":[
  {"type":"start","text":"ans = 0"},
  {"type":"decision","text":"more elements?","yes":"yes",
     "branch":{"label":"no","text":"return ans"}},
  {"type":"process","text":"ans ^= nums[i]"},
  {"type":"process","text":"advance i"}
 ]}
```

### 9. Step-by-Step Walkthrough

| step | element | `ans` (binary) | `ans` |
|---|---|---|---|
| init | \u2014 | `000` | 0 |
| 1 | 4 | `100` | 4 |
| 2 | 1 | `101` | 5 |
| 3 | 2 | `111` | 7 |
| 4 | 1 | `110` | 6 |
| 5 | 2 | `100` | 4 |

### 10. Why It Works

By induction on the invariant. **Base:** `ans = 0` is the XOR of the empty prefix. **Step:** if `ans` is the XOR of `nums[0..i-1]`, then `ans ^= nums[i]` makes it the XOR of `nums[0..i]`. **Termination:** the full XOR is `0` for every paired value and the unique value for the lonely one, i.e. the answer. Commutativity/associativity guarantee the pairing order is irrelevant.

### 11. Java Implementation

```java
int singleNumber(int[] nums) {
    int ans = 0;
    for (int x : nums) ans ^= x;
    return ans;
}
```

### 12. Code Walkthrough

The entire algorithm is one accumulator. `ans ^= x` is the induction step made literal. No map, no sorting, no second pass \u2014 the invariant does all the bookkeeping.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n) \u2014 one pass. **S:** O(1) \u2014 a single `int`. This is optimal: you must read every element at least once.

### 14. Edge Cases

- Single-element array `[7]` \u2192 returns 7 (XOR with initial 0).
- Negative numbers work unchanged \u2014 XOR operates on the two\u2019s-complement bit pattern.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Initializing `ans` to `nums[0]` and then re-XOR-ing it (double counting), or reaching for a `HashSet` and forgetting the O(1)-space requirement the interviewer is actually testing.

### 16. Optimization

Already optimal. The only micro-note: a classic `for` over the primitive array avoids iterator/boxing overhead versus streaming.

### 17. Alternatives

Sorting then scanning adjacent pairs is O(n log n)/O(1) \u2014 strictly worse in time and destroys input order. Hashing is O(n)/O(n). XOR dominates both.

### 18. Interview Follow-Ups

*"What if every element appears three times except one?"* XOR cancellation no longer applies \u2014 see **Single Number II**. *"Two unique elements?"* Partition by a distinguishing set bit (Single Number III).

### 19. Variations

- **Missing Number** \u2014 XOR indices and values together; the survivor is the missing index.
- **Find two single numbers** \u2014 XOR everything to get `a\u2295b`, isolate a set bit with `d = (a\u2295b) & -(a\u2295b)`, then partition.

### 20. Pattern Connection

This is the seed of **Bitmasking** (Pattern 15) and the parity idea reused in **Missing Number via XOR** below. The "combine so duplicates vanish" instinct also echoes in the cycle-detection parity arguments of Module 5.
