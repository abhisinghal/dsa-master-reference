# Math &amp; Number Theory

**Grokking arc:** The motivating problem is numeric work that is too slow or unsafe when performed literally. Brute force repeats multiplication, division tests, or factor checks. **Can we do better?** Use halving, remainders, marking, and overflow-safe `long` arithmetic to turn the loop into a known number-theory pattern.

Some problems aren't about a data structure at all — they hinge on a **numeric trick** you either know or you don't. The good news: a small toolkit covers almost all of them. The recurring theme is *"don't do n multiplications/divisions when `log n` will do"* — the same halving idea behind binary search, applied to arithmetic. The other half is defensive: interview inputs overflow `int` constantly, so know when to reach for `long` and modular arithmetic.

<Callout kind="key" title="Key Insight">

Three moves solve most math questions: **binary exponentiation** (turn `xⁿ` into `log n` squarings), **Euclid's algorithm** (GCD in `log` steps via repeated remainder), and the **sieve** (mark composites once to list all primes up to n). Everything else is overflow discipline.

</Callout>

<Callout kind="trap" title="Common Trap">

Overflow. `a * b` on two `int`s near 10⁹ wraps silently. Use `long` for products and running sums, take `% mod` *after every multiply* (not once at the end), and compute midpoints as `lo + (hi-lo)/2`.

</Callout>

## Fast (Binary) Exponentiation — Pow(x, n) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Pow(x, n)](https://leetcode.com/problems/powx-n/)* — **Medium**

<ProgressCheck id="fast-binary-exponentiation-pow-x-n" />

### Problem
Compute `xⁿ` (x a double, n a signed integer) in better than O(n). **Example 1:** `pow(2, 10) = 1024`; `pow(2, -2) = 0.25`.

**Example 2:** `pow(3, 5) = 243`.

**Constraints:** `−2³¹ ≤ n ≤ 2³¹−1` — note `n = −2³¹` overflows if you naively negate it, so widen to `long`.

### Solution — brute force
The direct baseline multiplies by `x` one exponent step at a time, then handles a negative exponent by taking the reciprocal.

**Brute-force sketch:**



```text
result = 1
repeat |n| times: result *= x
if original n was negative: return 1 / result
```



**Baseline complexity:** O(|n|) time and O(1) space; also unsafe for `Integer.MIN_VALUE` if `n` is negated as an int.

### Solution — optimized
The optimized solution keeps the original Java intact and explains the pattern that removes the brute-force bottleneck.

#### Pattern
Every exponent is a sum of powers of two (its binary form). Square the base repeatedly; multiply it into the result whenever the current bit of `n` is set. `n` loses a bit each step → O(log n).

<Callout kind="inv" title="Invariant">

after processing the low `k` bits, `result` equals `x` raised to the value of those `k` bits, and `x` has been squared `k` times (so it equals the original base to the `2ᵏ`).

</Callout>

#### Java


```java
double myPow(double x, int nRaw) {
    long n = nRaw;                       // widen so -2^31 negates safely
    if (n < 0) { x = 1 / x; n = -n; }
    double result = 1;
    while (n > 0) {
        if ((n & 1) == 1) result *= x;   // this bit of the exponent is set
        x *= x;                          // square the base for the next bit
        n >>= 1;
    }
    return result;
}
```



<Callout kind="note" title="Trace it">

`pow(2, 10)`, `10 = 1010₂`. Bits (low→high) 0,1,0,1: skip, ×(2²)=4→result 4, skip, ×(2⁸)=256→result 1024. Four squarings, not ten multiplications.

</Callout>

<CodeTrace
  title="Fast Power — pow(2, 10)"
  :values="[2,4,16,256]"
  :windowKeys="['bit']"
  :cellWidth="52"
  :steps='[
    { pointers: { bit: 0 }, vars: { base: 2, exp: 10, result: 1 }, note: "start: exp=10=1010₂" },
    { pointers: { bit: 0 }, vars: { base: 4, exp: 5, result: 1 }, note: "bit 0 of 10 = 0 → skip; base=2²=4, expgtgt=1" },
    { pointers: { bit: 1 }, vars: { base: 16, exp: 2, result: 4 }, note: "bit 0 of 5 = 1 → result *= 4; base=16, expgtgt=1", added: [1] },
    { pointers: { bit: 2 }, vars: { base: 256, exp: 1, result: 4 }, note: "bit 0 of 2 = 0 → skip; base=256, expgtgt=1" },
    { pointers: { bit: 3 }, vars: { base: 65536, exp: 0, result: 1024 }, note: "bit 0 of 1 = 1 → result *= 256 = 1024. done", added: [3] }
  ]'
/>

#### Same pattern, new tweaks
| Variation | The one thing that changes | Time |
|---|---|---|
| [Pow(x, n)](https://leetcode.com/problems/powx-n/) | real base, handle negative exponent | O(log n) |
| [Super Pow](https://leetcode.com/problems/super-pow/) | huge exponent as a digit array, mod 1337 | O(k log) |
| [Modular exponentiation](https://leetcode.com/problems/powx-n/) | take `% m` after every multiply (overflow-safe) | O(log n) |
| [Matrix exponentiation](https://leetcode.com/problems/fibonacci-number/) | base is a matrix → nth Fibonacci / linear recurrence | O(k³ log n) |

<Callout kind="pat" title="Pattern Connection">

The identical loop with `% mod` after each multiply is **modular exponentiation** (`aᵇ mod m`), the backbone of hashing, combinatorics (`nCr mod p` via Fermat's inverse `a^(p−2)`), and *Super Pow*. Swap `double` for a 2×2 matrix and you get **matrix exponentiation** for linear recurrences (Fibonacci in O(log n)).

</Callout>

<Callout kind="trap" title="Common Trap">

Not widening `n` before negating. *Example:* `n = Integer.MIN_VALUE = -2³¹`. `-n` overflows back to itself, so `n < 0 ? -n : n` yields a negative `n` — the while-loop never terminates. Widen to `long` first.

</Callout>

### Time Complexity
Time O(log n) · Space O(1).

O(log |n|): each loop consumes one binary bit of the exponent.


### Space Complexity
O(1): only the base, exponent, and result variables are kept.

### Learning notes
- Why `long n = nRaw`? — `-Integer.MIN_VALUE` overflows as an `int`, but not after widening.
- Why invert `x` when `n < 0`? — `x^-n` equals `(1/x)^n`, turning the exponent positive.
- Why `result = 1`? — one is the multiplication identity and represents the processed value of zero bits.
- Why test `(n & 1) == 1`? — the current binary bit says whether this power of `x` participates in the answer.
- Why `x *= x` and `n >>= 1`? — squaring advances to the next power of two while shifting drops the bit just processed.

## Euclid's Algorithm — GCD &amp; LCM <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Greatest Common Divisor of Strings](https://leetcode.com/problems/greatest-common-divisor-of-strings/)* — **Easy**

<ProgressCheck id="euclid-s-algorithm-gcd-amp-lcm" />

### Problem
Compute `gcd(a, b)` (largest integer dividing both) and, from it, `lcm(a, b)`. **Example 1:** `gcd(12, 18) = 6`, `lcm(12, 18) = 36`.

**Example 2:** `gcd(17, 13) = 1`, `lcm(17, 13) = 221`.

### Solution — brute force
The direct baseline scans possible divisors from large to small until it finds one that divides both numbers.

**Brute-force sketch:**



```text
for d from min(a,b) down to 1:
    if a % d == 0 and b % d == 0: return d
```



**Baseline complexity:** O(min(a,b)) time and O(1) space for the scan.

### Solution — optimized
The optimized solution keeps the original Java intact and explains the pattern that removes the brute-force bottleneck.

#### Pattern
`gcd(a, b) = gcd(b, a mod b)` — the remainder shrinks the pair fast (worst case is consecutive Fibonacci numbers → O(log min(a,b))). LCM follows: `a / gcd × b` (divide first to avoid overflow).

#### Java


```java
long gcd(long a, long b) { return b == 0 ? a : gcd(b, a % b); }
long lcm(long a, long b) { return a / gcd(a, b) * b; }   // divide before multiply
```



<Callout kind="note" title="Trace it">

`gcd(18, 12) → gcd(12, 6) → gcd(6, 0) = 6`. Each step replaces the larger with the remainder; the last non-zero value is the answer.

</Callout>

<CodeTrace
  title="Euclid GCD — gcd(18, 12)"
  :values="[18,12,6,0]"
  :windowKeys="['step']"
  :cellWidth="52"
  :steps='[
    { pointers: { step: 0 }, vars: { a: 18, b: 12 }, note: "gcd(18, 12). 18 % 12 = 6", added: [0,1] },
    { pointers: { step: 1 }, vars: { a: 12, b: 6 }, note: "gcd(12, 6). 12 % 6 = 0", added: [1,2] },
    { pointers: { step: 2 }, vars: { a: 6, b: 0, result: 6 }, note: "b=0 → return a = 6", added: [2] }
  ]'
/>

#### Same pattern, new tweaks
| Variation | The one thing that changes | Time |
|---|---|---|
| [GCD of Strings](https://leetcode.com/problems/greatest-common-divisor-of-strings/) | GCD of lengths; verify `s+t == t+s` | O(n) |
| [Water and Jug Problem](https://leetcode.com/problems/water-and-jug-problem/) | feasible iff `target % gcd(x,y) == 0` (Bézout) | O(log) |
| [Fraction to Recurring Decimal](https://leetcode.com/problems/fraction-to-recurring-decimal/) | track remainders to find the repeating cycle | O(len) |

<Callout kind="trap" title="Common Trap">

`a * b` in LCM overflows even when the LCM fits. *Example:* `a = b = 10⁹`. `gcd = 10⁹`, but `a*b = 10¹⁸` overflows `long`. Always `a / gcd(a,b) * b` — divide before multiplying.

</Callout>

<Callout kind="pat" title="Pattern Connection">

GCD reasoning drives *GCD of Strings* (the answer exists iff `s+t == t+s`, and its length is `gcd(|s|,|t|)`), *Fraction to Recurring Decimal*, *Water and Jug Problem* (solvable iff `target % gcd(a,b) == 0`), and *Nim/game* parity arguments.

</Callout>

### Time Complexity
Time O(log min(a,b)) · Space O(1) (iterative) or O(log) recursion stack.

O(log min(a,b)): remainders shrink quickly under Euclid's algorithm.


### Space Complexity
O(1) for the iterative version; recursive form uses O(log min(a,b)) stack.

### Learning notes
- Why `gcd(b, a % b)`? — any divisor of `a` and `b` also divides the remainder, and vice versa.
- Why stop at `b == 0`? — the last nonzero remainder is the greatest common divisor.
- Why use `long` parameters? — products and remainders often exceed `int` in LCM-style problems.
- Why compute `a / gcd(a,b) * b`? — dividing first reduces overflow risk before multiplication.
- Why can this solve string GCD? — the candidate length is the numeric gcd of the two string lengths.

## Sieve of Eratosthenes — Count Primes <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Count Primes](https://leetcode.com/problems/count-primes/)* — **Medium**

<ProgressCheck id="sieve-of-eratosthenes-count-primes" />

### Problem
Count primes strictly below `n`. **Example 1:** `n = 10 → 4` (2, 3, 5, 7).

**Example 2:** `n = 0` or `n = 2` → `0` primes strictly below n.

**Constraints:** `0 ≤ n ≤ 5·10⁶` — so an O(n√n) per-number test is too slow; the sieve is O(n log log n).

### Solution — brute force
The direct baseline tests each candidate number independently by trial division up to its square root.

**Brute-force sketch:**



```text
for each x from 2 to n-1:
    test divisibility by every d from 2 to sqrt(x)
    count x if no divisor is found
```



**Baseline complexity:** O(n√n) time and O(1) extra space beyond the loop variables.

### Solution — optimized
The optimized solution keeps the original Java intact and explains the pattern that removes the brute-force bottleneck.

#### Pattern
Every composite has a smallest prime factor. Walk `i` from 2; the first time you reach an unmarked `i` it's prime, so mark all its multiples starting at `i²` (smaller multiples were already marked by smaller primes).

#### Java


```java
int countPrimes(int n) {
    if (n < 3) return 0;
    boolean[] composite = new boolean[n];
    int count = 0;
    for (int i = 2; i < n; i++) {
        if (composite[i]) continue;
        count++;
        for (long j = (long) i * i; j < n; j += i)   // start at i*i; long avoids overflow
            composite[(int) j] = true;
    }
    return count;
}
```



<Callout kind="note" title="Trace it">

`n = 10`. i=2 prime → mark 4,6,8; i=3 prime → mark 9; i=5,7 prime (nothing to mark below 10). Count = 4.

</Callout>

<CodeTrace
  title="Sieve of Eratosthenes — n=10 (count primes below 10)"
  :values="[2,3,4,5,6,7,8,9]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { primes: "[2]", marked: "{}" }, note: "2 prime. mark 4,6,8 as composite", added: [0], removed: [2,4,6] },
    { pointers: { i: 1 }, vars: { primes: "[2,3]", marked: "{4,6,8}" }, note: "3 prime. mark 9 as composite", added: [1], removed: [7] },
    { pointers: { i: 3 }, vars: { primes: "[2,3,5]", marked: "+9" }, note: "5 prime. next multiple 25 gt 10 → skip", added: [3] },
    { pointers: { i: 5 }, vars: { primes: "[2,3,5,7]", marked: "same" }, note: "7 prime. count = 4", added: [5] }
  ]'
/>

#### Same pattern, new tweaks
| Variation | The one thing that changes | Time |
|---|---|---|
| [Count Primes](https://leetcode.com/problems/count-primes/) | count marks left unmarked | O(n log log n) |
| [Ugly Number II](https://leetcode.com/problems/ugly-number-ii/) | multiply-and-merge instead of mark (3 pointers) | O(n) |
| [Smallest-prime-factor sieve](https://leetcode.com/problems/count-primes/) | store `spf[x]` → factorize any x ≤ n in O(log x) | O(n) |

<Callout kind="trap" title="Common Trap">

Starting the inner loop at `2*i` (redundant) or forgetting to widen. *Example:* i ≈ 46341, `i*i` overflows `int` to negative → index out of range. Use `(long)i*i`; start there because smaller multiples were marked by smaller primes.

</Callout>

<Callout kind="pat" title="Pattern Connection">

A **linear sieve** also records each number's smallest prime factor, giving O(1) factorization afterwards — powers *Closest Prime Numbers*, *Distinct Prime Factors*, and any problem needing fast factorization over a range.

</Callout>

### Time Complexity
Time O(n log log n) · Space O(n).

O(n log log n): each prime marks its multiples, starting at its square.


### Space Complexity
O(n): the `composite` boolean array stores one mark per number below n.

### Learning notes
- Why `if (n < 3) return 0`? — there are no primes strictly below 2, and below 3 only 2 exists but n=2 excludes it.
- Why skip `composite[i]`? — a smaller prime already proved it non-prime.
- Why start marking at `i*i`? — smaller multiples of `i` were already marked by smaller factors.
- Why cast `(long) i * i`? — `i*i` can overflow `int` before the comparison with n.
- Why count when first seen unmarked? — every composite has a smallest prime factor, so unmarked `i` must be prime.

## Modular Arithmetic &amp; Combinatorics (toolkit)
<p class="secgoal"><b>What &amp; why:</b> the overflow-safe identities behind "answer modulo 10⁹+7" problems. Goal — never lose points to a wrapped <code>int</code>, and know how to divide under a modulus.</p>

Answers are asked `mod 1_000_000_007` precisely so they fit in a `long`. The rules: `(a+b) % m`, `(a−b+m) % m` (keep it non-negative), `(a*b) % m` — apply after **every** operation. Division is the catch: you can't `/` under a modulus; multiply by the **modular inverse** instead. When `m` is prime, Fermat's little theorem gives `a⁻¹ ≡ a^(m−2) (mod m)` — computed with the fast-exponentiation loop above.



```java
static final int MOD = 1_000_000_007;
long inv(long a) { return modpow(a, MOD - 2, MOD); }             // Fermat inverse, m prime
long nCr(int n, int r, long[] fact, long[] invFact) {           // precomputed factorials
    return fact[n] * invFact[r] % MOD * invFact[n - r] % MOD;
}
long modpow(long b, long e, long m) {
    long r = 1; b %= m;
    while (e > 0) { if ((e & 1) == 1) r = r * b % m; b = b * b % m; e >>= 1; }
    return r;
}
```



<Callout kind="pat" title="Pattern Connection">

This unlocks the counting-DP finale: *Unique Paths* / *Distinct Subsequences* / *Number of Ways* problems that ask for the count `mod p`. Precompute `fact[]` and `invFact[]` once (O(n)), then every `nCr` is O(1).

</Callout>

<Callout kind="trap" title="Common Trap">

Forgetting `(a − b + MOD) % MOD` when a subtraction can go negative, or applying the mod only at the very end (the intermediate product already overflowed). Reduce early and often.

</Callout>
