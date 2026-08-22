# Bit Manipulation — Find the Difference

*[↗ LeetCode: Find the Difference](https://leetcode.com/problems/find-the-difference/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

`t` is `s` shuffled with **one extra letter**. Return that letter.

**Example 1** — `s="abcd", t="abcde"` → `'e'`
**Example 2** — `s="", t="y"` → `'y'`

**Constraints** — `0 ≤ |s| ≤ 1000`.

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

**Complexity** — Time **O(n)**; Space **O(1)**.

---

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
