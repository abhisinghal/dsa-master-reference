# Hashing — Isomorphic Strings

*[↗ LeetCode: Isomorphic Strings](https://leetcode.com/problems/isomorphic-strings/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/hashing)

&lt;CompanyTags companies="LinkedIn, Meta, Amazon, Google" /&gt;

Return true iff there's a **bijection** of characters mapping `s → t`.

**Example 1** — `s="egg", t="add"` → `true`
**Example 2** — `s="foo", t="bar"` → `false`
**Example 3** — `s="paper", t="title"` → `true`

**Constraints** — `1 ≤ n ≤ 5·10⁴`.


&lt;Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/&gt;
---

&lt;MarkSolved problem-slug="isomorphic-strings" /&gt;

&lt;InterviewTimer problem-slug="isomorphic-strings" /&gt;



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



<CodeTrace
  title="Two maps (canonical)"
  :values="['e', 'g', 'g']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(σ)**.

## Alternative — first-index trick

`s` and `t` isomorphic iff `firstIndex(s[i]) == firstIndex(t[i])` for all `i`.

---

## Try it yourself

<JavaRunner problem-slug="isomorphic-strings" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Two maps | **O(n)** | O(σ) | canonical |
| First-index | O(n) | O(σ) | elegant |

## When to use which

- **Bijection check** → two maps.
- **Word pattern** — similar bijection with words.

&lt;AiCompanion problem-slug="isomorphic-strings" pattern-hint="hashing" /&gt;

## Related problems

- [Word Pattern](https://leetcode.com/problems/word-pattern/)
- [Group Shifted Strings](/problems/group-shifted-strings)
- [Valid Anagram](/problems/valid-anagram)

&lt;FeedbackWidget problem-slug="isomorphic-strings" /&gt;

&lt;RelatedProblems problems="group-shifted-strings::Group Shifted Strings|3sum::3sum|valid-anagram::Valid Anagram" /&gt;
