# Hashing — Isomorphic Strings

*[↗ LeetCode: Isomorphic Strings](https://leetcode.com/problems/isomorphic-strings/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/hashing)

Return true iff there's a **bijection** of characters mapping `s → t`.

**Example 1** — `s="egg", t="add"` → `true`
**Example 2** — `s="foo", t="bar"` → `false`
**Example 3** — `s="paper", t="title"` → `true`

**Constraints** — `1 ≤ n ≤ 5·10⁴`.

---

## Approach — Two maps (canonical)

**Insight.** One-way map is insufficient — two source chars must not map to the same target. Track both `s→t` and `t→s`.

```java
boolean isIsomorphic(String s, String t) {
    int[] fwd = new int[256], bwd = new int[256];
    for (int i = 0; i < s.length(); i++) {
        char a = s.charAt(i), b = t.charAt(i);
        if (fwd[a] == 0 && bwd[b] == 0) { fwd[a] = b; bwd[b] = a; }
        else if (fwd[a] != b || bwd[b] != a) return false;
    }
    return true;
}
```

**Complexity** — Time **O(n)**; Space **O(σ)**.

## Alternative — first-index trick

`s` and `t` isomorphic iff `firstIndex(s[i]) == firstIndex(t[i])` for all `i`.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Two maps | **O(n)** | O(σ) | canonical |
| First-index | O(n) | O(σ) | elegant |

## When to use which

- **Bijection check** → two maps.
- **Word pattern** — similar bijection with words.

## Related problems

- [Word Pattern](https://leetcode.com/problems/word-pattern/)
- [Group Shifted Strings](/problems/group-shifted-strings)
- [Valid Anagram](/problems/valid-anagram)
