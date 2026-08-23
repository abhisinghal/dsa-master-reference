# Bit Manipulation — Sum of All Subset XOR Totals

*[↗ LeetCode: Sum of All Subset XOR Totals](https://leetcode.com/problems/sum-of-all-subset-xor-totals/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

Return the sum of XOR of every subset of `nums` (including empty).

**Example 1** — `nums=[1,3]` → `6` (subsets: {},{1},{3},{1,3}; XORs: 0,1,3,2; sum 6)
**Example 2** — `nums=[5,1,6]` → `28`

**Constraints** — `1 ≤ n ≤ 12`.

---

## Approach 1 — Enumerate all 2ⁿ subsets

O(2ⁿ · n). Works for n ≤ 20.

## Approach 2 — Contribution-per-bit (canonical)

**Insight.** Bit `b` contributes `2^b` to a subset's XOR iff the subset contains an odd number of nums with bit `b` set. Exactly half of all 2ⁿ subsets have any specific parity → 2^(n-1) subsets contribute per bit-position that's set in **at least one** num.

So `answer = (OR of all nums) · 2^(n-1)`.



```java
int subsetXORSum(int[] nums) {
    int or = 0;
    for (int x : nums) or |= x;
    return or << (nums.length - 1);
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Enumerate | O(2ⁿ · n) | O(1) | works |
| OR × 2^(n-1) | **O(n)** | **O(1)** | canonical |

## When to use which

- **Sum over all subsets of X** → contribution per element or per bit.
- **AND / SUM over subsets** — similar bit-contribution insights.

## Related problems

- [Sum of Subarray Minimums](/problems/sum-of-subarray-minimums) — contribution counting
- [Subsets](/problems/bit-manip-subsets)
