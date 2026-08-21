# Math &amp; Number Theory

Some problems aren't about a data structure at all — they hinge on a **numeric trick** you either know or you don't. The good news: a small toolkit covers almost all of them. The recurring theme is *"don't do n multiplications/divisions when `log n` will do"* — the same halving idea behind binary search, applied to arithmetic. The other half is defensive: interview inputs overflow `int` constantly, so know when to reach for `long` and modular arithmetic.

> [key] **Key Insight** — Three moves solve most math questions: **binary exponentiation** (turn `xⁿ` into `log n` squarings), **Euclid's algorithm** (GCD in `log` steps via repeated remainder), and the **sieve** (mark composites once to list all primes up to n). Everything else is overflow discipline.

> [trap] **Common Trap** — Overflow. `a * b` on two `int`s near 10⁹ wraps silently. Use `long` for products and running sums, take `% mod` *after every multiply* (not once at the end), and compute midpoints as `lo + (hi-lo)/2`.

## Fast (Binary) Exponentiation — Pow(x, n)
*[↗ LeetCode: Pow(x, n)](https://leetcode.com/problems/powx-n/)* — **Medium**

### Problem
Compute `xⁿ` (x a double, n a signed integer) in better than O(n). **Example:** `pow(2, 10) = 1024`; `pow(2, -2) = 0.25`.

**Constraints:** `−2³¹ ≤ n ≤ 2³¹−1` — note `n = −2³¹` overflows if you naively negate it, so widen to `long`.

### Pattern
Every exponent is a sum of powers of two (its binary form). Square the base repeatedly; multiply it into the result whenever the current bit of `n` is set. `n` loses a bit each step → O(log n).

> [inv] **Invariant** — after processing the low `k` bits, `result` equals `x` raised to the value of those `k` bits, and `x` has been squared `k` times (so it equals the original base to the `2ᵏ`).

### Java
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

> [note] **Trace it** — `pow(2, 10)`, `10 = 1010₂`. Bits (low→high) 0,1,0,1: skip, ×(2²)=4→result 4, skip, ×(2⁸)=256→result 1024. Four squarings, not ten multiplications.

### Complexity
Time O(log n) · Space O(1).

> [pat] **Pattern Connection** — The identical loop with `% mod` after each multiply is **modular exponentiation** (`aᵇ mod m`), the backbone of hashing, combinatorics (`nCr mod p` via Fermat's inverse `a^(p−2)`), and *Super Pow*. Swap `double` for a 2×2 matrix and you get **matrix exponentiation** for linear recurrences (Fibonacci in O(log n)).

> [trap] **Common Trap** — Not widening `n` before negating. *Example:* `n = Integer.MIN_VALUE = -2³¹`. `-n` overflows back to itself, so `n < 0 ? -n : n` yields a negative `n` — the while-loop never terminates. Widen to `long` first.

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Pow(x, n)](https://leetcode.com/problems/powx-n/) | real base, handle negative exponent | O(log n) |
| [Super Pow](https://leetcode.com/problems/super-pow/) | huge exponent as a digit array, mod 1337 | O(k log) |
| [Modular exponentiation](https://leetcode.com/problems/powx-n/) | take `% m` after every multiply (overflow-safe) | O(log n) |
| [Matrix exponentiation](https://leetcode.com/problems/fibonacci-number/) | base is a matrix → nth Fibonacci / linear recurrence | O(k³ log n) |

## Euclid's Algorithm — GCD &amp; LCM
*[↗ LeetCode: Greatest Common Divisor of Strings](https://leetcode.com/problems/greatest-common-divisor-of-strings/)* — **Easy**

### Problem
Compute `gcd(a, b)` (largest integer dividing both) and, from it, `lcm(a, b)`. **Example:** `gcd(12, 18) = 6`, `lcm(12, 18) = 36`.

### Pattern
`gcd(a, b) = gcd(b, a mod b)` — the remainder shrinks the pair fast (worst case is consecutive Fibonacci numbers → O(log min(a,b))). LCM follows: `a / gcd × b` (divide first to avoid overflow).

### Java
```java
long gcd(long a, long b) { return b == 0 ? a : gcd(b, a % b); }
long lcm(long a, long b) { return a / gcd(a, b) * b; }   // divide before multiply
```

> [note] **Trace it** — `gcd(18, 12) → gcd(12, 6) → gcd(6, 0) = 6`. Each step replaces the larger with the remainder; the last non-zero value is the answer.

### Complexity
Time O(log min(a,b)) · Space O(1) (iterative) or O(log) recursion stack.

> [trap] **Common Trap** — `a * b` in LCM overflows even when the LCM fits. *Example:* `a = b = 10⁹`. `gcd = 10⁹`, but `a*b = 10¹⁸` overflows `long`. Always `a / gcd(a,b) * b` — divide before multiplying.

> [pat] **Pattern Connection** — GCD reasoning drives *GCD of Strings* (the answer exists iff `s+t == t+s`, and its length is `gcd(|s|,|t|)`), *Fraction to Recurring Decimal*, *Water and Jug Problem* (solvable iff `target % gcd(a,b) == 0`), and *Nim/game* parity arguments.

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [GCD of Strings](https://leetcode.com/problems/greatest-common-divisor-of-strings/) | GCD of lengths; verify `s+t == t+s` | O(n) |
| [Water and Jug Problem](https://leetcode.com/problems/water-and-jug-problem/) | feasible iff `target % gcd(x,y) == 0` (Bézout) | O(log) |
| [Fraction to Recurring Decimal](https://leetcode.com/problems/fraction-to-recurring-decimal/) | track remainders to find the repeating cycle | O(len) |

## Sieve of Eratosthenes — Count Primes
*[↗ LeetCode: Count Primes](https://leetcode.com/problems/count-primes/)* — **Medium**

### Problem
Count primes strictly below `n`. **Example:** `n = 10 → 4` (2, 3, 5, 7).

**Constraints:** `0 ≤ n ≤ 5·10⁶` — so an O(n√n) per-number test is too slow; the sieve is O(n log log n).

### Pattern
Every composite has a smallest prime factor. Walk `i` from 2; the first time you reach an unmarked `i` it's prime, so mark all its multiples starting at `i²` (smaller multiples were already marked by smaller primes).

### Java
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

> [note] **Trace it** — `n = 10`. i=2 prime → mark 4,6,8; i=3 prime → mark 9; i=5,7 prime (nothing to mark below 10). Count = 4.

### Complexity
Time O(n log log n) · Space O(n).

> [trap] **Common Trap** — Starting the inner loop at `2*i` (redundant) or forgetting to widen. *Example:* i ≈ 46341, `i*i` overflows `int` to negative → index out of range. Use `(long)i*i`; start there because smaller multiples were marked by smaller primes.

> [pat] **Pattern Connection** — A **linear sieve** also records each number's smallest prime factor, giving O(1) factorization afterwards — powers *Closest Prime Numbers*, *Distinct Prime Factors*, and any problem needing fast factorization over a range.

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Count Primes](https://leetcode.com/problems/count-primes/) | count marks left unmarked | O(n log log n) |
| [Ugly Number II](https://leetcode.com/problems/ugly-number-ii/) | multiply-and-merge instead of mark (3 pointers) | O(n) |
| [Smallest-prime-factor sieve](https://leetcode.com/problems/count-primes/) | store `spf[x]` → factorize any x ≤ n in O(log x) | O(n) |

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

> [pat] **Pattern Connection** — This unlocks the counting-DP finale: *Unique Paths* / *Distinct Subsequences* / *Number of Ways* problems that ask for the count `mod p`. Precompute `fact[]` and `invFact[]` once (O(n)), then every `nCr` is O(1).

> [trap] **Common Trap** — Forgetting `(a − b + MOD) % MOD` when a subtraction can go negative, or applying the mod only at the very end (the intermediate product already overflowed). Reduce early and often.
