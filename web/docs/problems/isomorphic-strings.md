# Hashing — Isomorphic Strings

*[↗ LeetCode: Isomorphic Strings](https://leetcode.com/problems/isomorphic-strings/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/hashing)

Return true iff there's a **bijection** of characters mapping `s → t`.

## Approach — Two maps (or two arrays)

**Insight.** One-way map is insufficient — need to forbid two source chars mapping to the same target. Track both `s→t` and `t→s`.



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

**Alternative "first-index" trick.** Two strings are isomorphic iff `firstIndex(s[i]) == firstIndex(t[i])` for all i. One pass.

## Related problems

- [Word Pattern](https://leetcode.com/problems/word-pattern/) — same bijection with words
- [Group Shifted Strings](/problems/group-shifted-strings) — canonical-key variant
