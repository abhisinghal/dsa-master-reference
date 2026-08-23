# Bit Manipulation


<PatternVideo pattern-name="Bit Manipulation" duration="8–12 min" />
<PatternProgress pattern-id="bit-manip" problems="single-number, missing-number, find-the-difference, number-of-1-bits, hamming-distance, power-of-two, reverse-bits, maximum-product-of-word-lengths, sum-of-all-subset-xor-totals, subsets" />



**Grokking arc:** The motivating problem is representing tiny sets, parity, or binary properties without bulky data structures. Brute force counts, scans, or stores everything. **Can we do better?** Treat bits as flags and use identities like XOR cancellation or lowest-set-bit removal to collapse work into O(1) operations per element.

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
