# Bit Manipulation — Single Number

*[↗ LeetCode: Single Number](https://leetcode.com/problems/single-number/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg, Adobe" />

Every element appears twice except one. Return that one, in **O(n)** time and **O(1)** space.

**Example 1** — `nums=[2,2,1]` → `1`
**Example 2** — `nums=[4,1,2,1,2]` → `4`

**Constraints** — `1 ≤ n ≤ 3·10⁴`; all fit in `int`.


<Hints
  hint1="Is there a bit-level trick? XOR cancels duplicates, `n & (n-1)` clears the lowest bit, `n | (1 << k)` sets bit k."
  hint2="For subset problems: iterate `mask` from 0 to 2ⁿ−1; bit `i` set means element `i` chosen."
  hint3="For ’find the unique/missing’: XOR the whole array with 0..n; pairs cancel, missing survives."
/>
---

## Approach 1 — HashSet toggle

**Intuition.** For each element, add if absent, remove if present. Last surviving element wins.

```java
int singleNumberSet(int[] nums) {
    Set<Integer> seen = new HashSet<>();
    for (int x : nums) if (!seen.add(x)) seen.remove(x);
    return seen.iterator().next();
}
```

**Complexity** — Time **O(n)**; Space **O(n)**. Fails the O(1) space bar.

---

## Approach 2 — Sort + pair scan

**Intuition.** Sort. Walk in steps of 2. The first index where `nums[i] != nums[i+1]` is the loner.

```java
int singleNumberSort(int[] nums) {
    Arrays.sort(nums);
    for (int i = 0; i < nums.length - 1; i += 2)
        if (nums[i] != nums[i + 1]) return nums[i];
    return nums[nums.length - 1];
}
```

**Complexity** — Time **O(n log n)**; Space **O(1)** (in-place sort). Doesn't beat the ideal.

---

## Approach 3 — XOR fold

**Insight.** XOR has these algebraic properties: `a ^ a = 0` and `a ^ 0 = a`. Folding XOR over every element cancels every duplicate pair; the survivor is the single number.

```java
int singleNumber(int[] nums) {
    int x = 0;
    for (int v : nums) x ^= v;
    return x;
}
```

<CodeTrace
  title="XOR fold — nums=[4,1,2,1,2]"
  :values="[4,1,2,1,2]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { xor: 4 }, note: "0 ^ 4 = 4" },
    { pointers: { i: 1 }, vars: { xor: 5 }, note: "4 ^ 1 = 5 (101)" },
    { pointers: { i: 2 }, vars: { xor: 7 }, note: "5 ^ 2 = 7 (111)" },
    { pointers: { i: 3 }, vars: { xor: 6 }, note: "7 ^ 1 = 6 (110)" },
    { pointers: { i: 4 }, vars: { xor: 4 }, note: "6 ^ 2 = 4 → answer", added: [0] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. Optimal.

---

## Try it yourself

<JavaRunner problem-slug="bit-manip-single-number" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| HashSet | O(n) | O(n) |
| Sort + pair scan | O(n log n) | O(1) |
| XOR fold | **O(n)** | **O(1)** |

## When to use which

- **Cold interview** → walk hash set → XOR. The XOR is the "aha" moment interviewers grade for.
- **Interviewer probes correctness** → state associativity + commutativity of XOR aloud.

## Related problems (same ladder applies)

- [Missing Number](https://leetcode.com/problems/missing-number/) — XOR nums with indices; the survivor is the missing index
- [Find the Difference](https://leetcode.com/problems/find-the-difference/) — XOR two strings; survivor is the added char
- [Single Number II](https://leetcode.com/problems/single-number-ii/) — every element thrice except one; bit-count mod 3
- [Single Number III](https://leetcode.com/problems/single-number-iii/) — two loners; XOR gives their xor, then split by any set bit