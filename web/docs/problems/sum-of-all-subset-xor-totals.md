# Bit Manipulation — Sum of All Subset XOR Totals

*[↗ LeetCode: Sum of All Subset XOR Totals](https://leetcode.com/problems/sum-of-all-subset-xor-totals/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

Return the sum of XOR of every subset of `nums` (including empty).

**Example** — `nums=[1,3]` → subsets XOR: 0,1,3,2 → sum = 6.

---

## Approach 1 — Enumerate all 2ⁿ subsets


```java
int subsetXORSum(int[] nums) {
    int n = nums.length, total = 0;
    for (int mask = 0; mask < 1 << n; mask++) {
        int x = 0;
        for (int i = 0; i < n; i++) if ((mask >> i & 1) == 1) x ^= nums[i];
        total += x;
    }
    return total;
}
```



O(2ⁿ · n).

---

## Approach 2 — Bit-by-bit contribution
**Insight.** Bit `b` contributes `2^b` to the XOR of a subset iff that subset contains an odd number of nums with bit `b` set. If `k` of the nums have bit `b` set, exactly half of the 2ⁿ subsets have an odd count → `2^(n-1)` subsets.

Therefore: bit `b` contributes `2^b · 2^(n-1)` if **any** number has bit b set, else 0.

Combining: `answer = (OR of all nums) · 2^(n-1)`.



```java
int subsetXORSum2(int[] nums) {
    int or = 0;
    for (int x : nums) or |= x;
    return or << (nums.length - 1);
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Enumerate all 2ⁿ subsets | O(2ⁿ · n) | — | baseline |
| Bit-by-bit contribution | O(n) | O(1) | optimum |

## When to use which

- **State it for signal** → Enumerate all 2ⁿ subsets (O(2ⁿ · n)). Correct baseline; call it out then move on.
- **Ship this** → Bit-by-bit contribution (O(n), O(1)). Expected optimum in interview.

## Related problems

- [Sum of Digits in Base K](https://leetcode.com/problems/sum-of-digits-in-base-k/) — contribution-based counting
- [Sum of Subarray Minimums](/problems/sum-of-subarray-minimums) — same "count contribution per element" mindset
