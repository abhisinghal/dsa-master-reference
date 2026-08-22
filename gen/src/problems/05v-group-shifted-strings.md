# Hashing — Group Shifted Strings

*[↗ LeetCode: Group Shifted Strings](https://leetcode.com/problems/group-shifted-strings/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/hashing)

Group strings that are cyclic shifts of each other ("abc","bcd","xyz" all shift by 1 pattern).

---

## Approach 1 — Canonical key = diff pattern
**Insight.** Two strings are shifts iff their consecutive character-difference sequence (mod 26) matches.

```java
List<List<String>> groupStrings(String[] strings) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String s : strings) {
        StringBuilder key = new StringBuilder();
        for (int i = 1; i < s.length(); i++) {
            int d = (s.charAt(i) - s.charAt(i - 1) + 26) % 26;
            key.append(d).append('.');
        }
        groups.computeIfAbsent(key.toString(), k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(groups.values());
}
```

**Complexity** — Time **O(∑ length)**; Space **O(∑ length)**.

**Trap.** Modulo `+ 26` before `% 26` to avoid negative Java `%`. Delimiter (`.`) between numbers prevents `"11"` colliding with `"1,1"`.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Canonical key = diff pattern | O(∑ length) | O(∑ length) | primary |

## When to use which

- **Ship this** → Canonical key = diff pattern (O(∑ length), O(∑ length)). The pattern's standard solution.

## Related problems

- [Group Anagrams](https://leetcode.com/problems/group-anagrams/) — canonical key = sorted string
- [Isomorphic Strings](/problems/isomorphic-strings)
