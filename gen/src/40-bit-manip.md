# Bit Manipulation

Bits let you treat an integer as a tiny array of on/off switches you can flip in O(1). That unlocks three things interviewers love: fast **set operations** (union, intersection, membership on up to ~30 elements with a single number), **parity/XOR tricks** (where duplicates cancel out to zero), and **compact state** for bitmask DP. A handful of identities do most of the heavy lifting — memorize them and a lot of "hard" bit problems collapse into one line. One Java landmine to internalize: `int` is 32-bit **signed**, so use `>>>` (not `>>`) when you want a logical shift, and switch to `1L << k` once `k` climbs past 30.

### Recognize by
- n ≤ 20 and you're enumerating subsets — a mask is the set
- "single number" / "XOR of everything cancels pairs"
- "count set bits" / "lowest set bit" / "is power of two?"

### When NOT to use it
n > ~20 and you're considering bitmask DP — 2ⁿ blows past 10⁶. Also, bit tricks that look clever but yield the same complexity as a `HashSet` add reading cost with no gain — reserve them for problems where the O(1) bitmap operation is genuinely a win.

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

## Single Number I / II / III (XOR)
*[↗ LeetCode: Single Number](https://leetcode.com/problems/single-number/)*

### Problem
Every element appears **twice except one**; find the single one — in O(n) time, O(1) space. (Variants II/III: one element appears 3×, or there are two singles.)

**Constraints:** `1 ≤ n ≤ 3·10⁴`; exactly one loner in the base version.

**Example:** `[4,1,2,1,2]` → `4`.

### Brute force
Brute force counts frequencies in a hash map, then returns the value whose count is one. That is O(n) time and O(n) space, and a sort-based variant is O(n log n) time with less extra space. The optimized XOR version uses pair cancellation: `a ^ a = 0` and `a ^ 0 = a`, so one accumulator leaves only the unpaired number.

### Pattern
XOR everything: pairs cancel, the loner survives.

> [inv] **Invariant** — Running XOR equals the XOR of all values seen; identical values annihilate, so after the full pass only odd-count values remain.

### Java
```java
int singleNumber(int[] a) {            // every other element appears twice
    int x = 0;
    for (int v : a) x ^= v;
    return x;
}
```

> [note] **Trace it** — `[4,1,2,1,2]`. XOR all: `1^1=0`, `2^2=0`, leaving `4`. The duplicates annihilate, so the single number is **4**.

**Time** O(n) single pass · **Space** O(1) — one accumulator, no hash map.

> [note] **Interview script** — "I first confirm every number appears exactly twice except the single value in the base problem. I start with brute force by counting frequencies in a hash map, which is O(n) time and O(n) space. I optimize with XOR cancellation, scanning once with one accumulator for O(n) time and O(1) space."


**Single Number III** (two loners, rest in pairs): XOR all → `xy = a ^ b`. A set bit of `xy` differs between `a` and `b`; split all numbers by that bit and XOR each group separately.

**Single Number II** (every element thrice except one): count bits mod 3 across all numbers, or use two-variable bit-state automata (`ones`, `twos`).

> [trap] **Common Trap** — Whole-XOR as split mask. *Example:* `nums=[1,2,3,4,1,2]`. `xy = 3^4 = 7 (0b111)`. Splitting by whole `xy` puts `1,2,3` in one group and `4` in the other — but `1^2^3 = 0`, losing the loner. Isolate a **single** distinguishing bit via `xy & -xy`.

> [pat] **Pattern Connection** — XOR-cancellation also finds the *Missing Number* (`XOR of indices ^ XOR of values`) and the duplicated/missing pair in *Set Mismatch*.

### Same pattern, new tweaks

XOR's "equal values cancel to 0" powers a whole family:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Missing Number](https://leetcode.com/problems/missing-number/) | XOR all indices `0..n` with all values; the survivor is the missing one | — |
| - **Single Number II** (every element three times) — *tweak:* count each bit position mod 3. |  | — |
| - **Single Number III** (two loners) — *tweak:* XOR everything, grab one distinguishing bit (`xy & -xy`), split into two groups. |  | — |
| [Find the Difference / Set Mismatch](https://leetcode.com/problems/find-the-difference/) | XOR the two collections so shared characters cancel, leaving the odd one out | — |

## Counting Bits (DP on bits)
*[↗ LeetCode: Counting Bits](https://leetcode.com/problems/counting-bits/)*

### Problem
For every number `0 … n`, return how many **1-bits** it has (its popcount), in O(n).

**Constraints:** `0 ≤ n ≤ 10⁵`.

**Example:** `n = 5` → `[0,1,1,2,1,2]`.

### Brute force
Brute force computes the popcount of every integer from `0` to `n` independently, shifting or clearing bits until each number becomes zero. That is O(n log n) time and O(n) output space because each integer may need one step per bit. The optimized DP reuses `i >> 1`: dropping the lowest bit gives a smaller number whose count is already known, then adds `i & 1`.

### Pattern
`dp[i] = dp[i >> 1] + (i & 1)` — `i` has the bits of `i/2` plus its own lowest bit.

> [key] **Key Insight** — Right-shifting drops the lowest bit, so `popcount(i) = popcount(i/2) + (i & 1)`. This recurrence fills `[0..n]` in O(n) instead of O(n log n) individual counts.

### Java
```java
int[] countBits(int n) {
    int[] dp = new int[n + 1];
    for (int i = 1; i <= n; i++) dp[i] = dp[i >> 1] + (i & 1);
    return dp;
}
```

> [note] **Trace it** — for `i=5` (`101`): `dp[5] = dp[2] + 1 = 1 + 1 = 2`. Sequence `0..5` → `[0,1,1,2,1,2]`.

Time O(n) · Space O(n).

> [note] **Interview script** — "I first confirm I need counts for every number from 0 through `n`, not just one number. I start with brute force by popcounting each number separately, which is O(n log n) time and O(n) output space. I optimize with `dp[i] = dp[i >> 1] + (i & 1)`, giving O(n) time and O(n) space."


> [pat] **Pattern Connection** — Alternative recurrence `dp[i] = dp[i & (i-1)] + 1`; both express popcount as a self-DP. Submask enumeration `(s-1) & m` powers *Sum of Subset XOR/AND* and bitmask-DP transitions.

> [trap] **Common Trap** — Recomputing popcount per number. *Example:* naïve `Integer.bitCount(i)` for i=0..n is O(n log n). The DP recurrence `bits[i] = bits[i >> 1] + (i & 1)` reuses the answer for `i/2` → O(n).

### Same pattern, new tweaks

Small bit identities each unlock a classic:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | Brian Kernighan's `x &= x - 1` clears the lowest set bit each step | — |
| [Hamming Distance](https://leetcode.com/problems/hamming-distance/) | `Integer.bitCount(a ^ b)` — count differing bits | — |
| [Power of Two](https://leetcode.com/problems/power-of-two/) | `x > 0 && (x & (x-1)) == 0` | — |
| [Reverse Bits](https://leetcode.com/problems/reverse-bits/) | shift bits out of one int and into another, one position at a time | — |

## Subset generation via masks
*[↗ LeetCode: Subsets](https://leetcode.com/problems/subsets/)*

### Problem
Generate **all subsets** of an `n`-element set by iterating bitmasks `0 … 2ⁿ−1` (bit `i` set = element `i` included).

**Constraints:** `n ≤ 20` so `2ⁿ` is tractable.

**Example:** `[a,b,c]` → all 8 subsets, one per bit pattern `000 … 111`.

Enumerate all `2ⁿ` subsets of an `n`-element set by counting masks `0..2ⁿ-1`; bit `i` set means element `i` is included.

### Brute force
Brute force recursively chooses include or exclude for each element and records the subset at the leaf. That is O(n·2ⁿ) time and O(n) recursion depth, which is unavoidable because there are `2ⁿ` subsets to output. The bitmask version is the iterative form of the same idea: every integer mask encodes one subset, making membership checks constant-time bit tests.

### Java
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

Time O(n·2ⁿ) · Space O(n·2ⁿ).

> [note] **Interview script** — "I first confirm `n` is small enough that outputting all 2ⁿ subsets is intended. I start with brute force include/exclude recursion, which is O(n·2ⁿ) time and O(n) stack space. I optimize the implementation with masks from `0` to `2ⁿ - 1`, keeping O(n·2ⁿ) time and using O(n·2ⁿ) output space."


> [pat] **Pattern Connection** — This iterative masking is the non-recursive twin of backtracking subsets, and the substrate for bitmask DP (*TSP*, *Partition to K Equal Sum Subsets*).

### Same pattern, new tweaks

Treating an integer as a set of bits:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Subsets](https://leetcode.com/problems/subsets/) | loop masks `0 .. 2ⁿ-1`; bit `i` set means element `i` is included | — |
| [Maximum Product of Word Lengths](https://leetcode.com/problems/maximum-product-of-word-lengths/) | encode each word's letters as a 26-bit mask; two words share no letter iff `maskA & maskB == 0` | — |
| [Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) | DP over the mask of used elements, tracking the current bucket's fill | — |
| [Sum of All Subset XOR / SOS DP](https://leetcode.com/problems/sum-of-all-subset-xor-totals/) | enumerate submasks with `for (s = m; s > 0; s = (s-1) & m)` | — |
