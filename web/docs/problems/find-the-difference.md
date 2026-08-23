# Bit Manipulation — Find the Difference

*[↗ LeetCode: Find the Difference](https://leetcode.com/problems/find-the-difference/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

&lt;CompanyTags companies="Google, Amazon, Meta" /&gt;

`t` is `s` shuffled with **one extra letter**. Return that letter.

**Example 1** — `s="abcd", t="abcde"` → `'e'`
**Example 2** — `s="", t="y"` → `'y'`

**Constraints** — `0 ≤ |s| ≤ 1000`.


&lt;Hints
  hint1="Is there a bit-level trick? XOR cancels duplicates, `n & (n-1)` clears the lowest bit, `n | (1 << k)` sets bit k."
  hint2="For subset problems: iterate `mask` from 0 to 2ⁿ−1; bit `i` set means element `i` chosen."
  hint3="For ’find the unique/missing’: XOR the whole array with 0..n; pairs cancel, missing survives."
/&gt;
---

## Approach 1 — Sort both, walk

O(n log n). Baseline.

## Approach 2 — Frequency map

O(n) time O(σ) space.

## Approach 3 — XOR fold (canonical)

**Insight.** XOR all chars of `s` and `t`; duplicates cancel; only the added char survives.



```java
char findTheDifference(String s, String t) {
    int x = 0;
    for (char c : s.toCharArray()) x ^= c;
    for (char c : t.toCharArray()) x ^= c;
    return (char) x;
}
```



<CodeTrace
  title="Sort both, walk"
  :values="['a', 'b', 'c', 'd']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="find-the-difference" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort | O(n log n) | O(n) | baseline |
| Frequency | O(n) | O(σ) | works |
| XOR fold | **O(n)** | **O(1)** | canonical |

## When to use which

- **Any "find the odd one out"** → XOR fold.
- **"Multiple extra chars"** → count map.
- **"Which position was added"** → walk both with two pointers.

## Related problems

- [Missing Number](/problems/missing-number)
- [Single Number](/problems/bit-manip-single-number)
- [Valid Anagram](/problems/valid-anagram)