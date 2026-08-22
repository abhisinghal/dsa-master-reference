# Bit Manipulation — Find the Difference

*[↗ LeetCode: Find the Difference](https://leetcode.com/problems/find-the-difference/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

`t` is `s` with one extra letter shuffled. Find that letter.

**Example** — `s="abcd", t="abcde"` → `'e'`

---

## Approach 1 — XOR fold
XOR every character of s and t; duplicates cancel; result is the added letter.



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

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| XOR fold | O(n) | O(1) | primary |

## When to use which

- **Ship this** → XOR fold (O(n), O(1)). The pattern's standard solution.

## Related problems

- [Single Number](/problems/bit-manip-single-number)
- [Missing Number](/problems/missing-number)
