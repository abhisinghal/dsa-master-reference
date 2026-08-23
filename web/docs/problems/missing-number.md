# Bit Manipulation — Missing Number

*[↗ LeetCode: Missing Number](https://leetcode.com/problems/missing-number/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg" /&gt;

Given `nums` containing `n` distinct integers in `[0, n]`, return the missing one.

**Example 1** — `nums=[3,0,1]` → `2`
**Example 2** — `nums=[0,1]` → `2`
**Example 3** — `nums=[9,6,4,2,3,5,7,0,1]` → `8`

**Constraints** — `1 ≤ n ≤ 10⁴`.


&lt;Hints
  hint1="Is there a bit-level trick? XOR cancels duplicates, `n & (n-1)` clears the lowest bit, `n | (1 << k)` sets bit k."
  hint2="For subset problems: iterate `mask` from 0 to 2ⁿ−1; bit `i` set means element `i` chosen."
  hint3="For ’find the unique/missing’: XOR the whole array with 0..n; pairs cancel, missing survives."
/&gt;
---

&lt;MarkSolved problem-slug="missing-number" /&gt;


## Approach 1 — Sort, find gap

O(n log n). Baseline.

## Approach 2 — Hash set

O(n) time and O(n) space.

## Approach 3 — Gauss sum

`missing = n(n+1)/2 - Σ nums`.

## Approach 4 — XOR fold (canonical)

**Insight.** XOR `0..n` with all of `nums`. Every present index cancels with its value → missing survives.



```java
int missingNumber(int[] nums) {
    int x = nums.length;
    for (int i = 0; i < nums.length; i++) x ^= i ^ nums[i];
    return x;
}
```



<CodeTrace
  title="Sort, find gap"
  :values="['3', '0', '1']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="missing-number" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort | O(n log n) | O(1) | baseline |
| Hash | O(n) | O(n) | works |
| Gauss sum | O(n) | O(1) | risk overflow |
| XOR fold | **O(n)** | **O(1)** | canonical, no overflow |

## When to use which

- **Standard** → XOR fold.
- **"Multiple missing"** → set difference or sort.
- **"Overflow-sensitive"** → XOR beats sum.

&lt;AiCompanion problem-slug="missing-number" pattern-hint="bit manipulation" /&gt;

## Related problems

- [Single Number](/problems/bit-manip-single-number)
- [Find the Difference](/problems/find-the-difference)
- [Find All Numbers Disappeared in an Array](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)

&lt;FeedbackWidget problem-slug="missing-number" /&gt;
