# Hashing — Valid Anagram

*[↗ LeetCode: Valid Anagram](https://leetcode.com/problems/valid-anagram/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/hashing)

Return true iff `t` is an anagram of `s`.

---

## Approach 1 — Sort both, compare
O(n log n).

---

## Approach 2 — Frequency map
For lowercase ASCII, size-26 int array. For Unicode, `HashMap<Character, Integer>`. Increment for `s`, decrement for `t`; verify all zeros.

```java
boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] cnt = new int[26];
    for (int i = 0; i < s.length(); i++) { cnt[s.charAt(i) - 'a']++; cnt[t.charAt(i) - 'a']--; }
    for (int c : cnt) if (c != 0) return false;
    return true;
}
```

**Complexity** — Time **O(n)**; Space **O(1)** for ASCII.

**Follow-up (Unicode).** Iterate `codePoints`; use `HashMap<Integer, Integer>`.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort both, compare | O(n log n) | — | baseline |
| Frequency map | O(n) | O(1) | optimum |

## When to use which

- **State it for signal** → Sort both, compare (O(n log n)). Correct baseline; call it out then move on.
- **Ship this** → Frequency map (O(n), O(1)). Expected optimum in interview.

## Related problems

- [Find All Anagrams in a String](/problems/find-all-anagrams-in-a-string) — sliding window
- [Group Anagrams](https://leetcode.com/problems/group-anagrams/) — canonical-key hashing
- [Permutation in String](/problems/permutation-in-string)
