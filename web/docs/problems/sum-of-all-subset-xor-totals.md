# Bit Manipulation — Sum of All Subset XOR Totals

*[↗ LeetCode: Sum of All Subset XOR Totals](https://leetcode.com/problems/sum-of-all-subset-xor-totals/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

&lt;CompanyTags companies="Amazon, Google" /&gt;

Return the sum of XOR of every subset of `nums` (including empty).

**Example 1** — `nums=[1,3]` → `6` (subsets: {},{1},{3},{1,3}; XORs: 0,1,3,2; sum 6)
**Example 2** — `nums=[5,1,6]` → `28`

**Constraints** — `1 ≤ n ≤ 12`.


&lt;Hints
  hint1="Is there a bit-level trick? XOR cancels duplicates, `n & (n-1)` clears the lowest bit, `n | (1 << k)` sets bit k."
  hint2="For subset problems: iterate `mask` from 0 to 2ⁿ−1; bit `i` set means element `i` chosen."
  hint3="For ’find the unique/missing’: XOR the whole array with 0..n; pairs cancel, missing survives."
/&gt;
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



<CodeTrace
  title="Enumerate all 2ⁿ subsets"
  :values="['1', '3']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="sum-of-all-subset-xor-totals" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Enumerate | O(2ⁿ · n) | O(1) | works |
| OR × 2^(n-1) | **O(n)** | **O(1)** | canonical |

## When to use which

- **Sum over all subsets of X** → contribution per element or per bit.
- **AND / SUM over subsets** — similar bit-contribution insights.

&lt;AiCompanion problem-slug="sum-of-all-subset-xor-totals" pattern-hint="bit manipulation" /&gt;

## Related problems

- [Sum of Subarray Minimums](/problems/sum-of-subarray-minimums) — contribution counting
- [Subsets](/problems/bit-manip-subsets)

&lt;FeedbackWidget problem-slug="sum-of-all-subset-xor-totals" /&gt;
