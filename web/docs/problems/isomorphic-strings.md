# Hashing — Isomorphic Strings

*[↗ LeetCode: Isomorphic Strings](https://leetcode.com/problems/isomorphic-strings/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/hashing)

<CompanyTags companies="LinkedIn, Meta, Amazon, Google" />

Return true iff there's a **bijection** of characters mapping `s → t`.

**Example 1** — `s="egg", t="add"` → `true`
**Example 2** — `s="foo", t="bar"` → `false`
**Example 3** — `s="paper", t="title"` → `true`

**Constraints** — `1 ≤ n ≤ 5·10⁴`. Brute character-comparison across all pairs is O(n²) = 2.5·10⁹ ops. Bijection tracking is O(n) = 5·10⁴.


<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its 'canonical form' — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For 'first duplicate', a `HashSet` and single-pass `add()` is enough."
/>
---

<MarkSolved problem-slug="isomorphic-strings" /> <Bookmark problem-slug="isomorphic-strings" />

<InterviewTimer problem-slug="isomorphic-strings" />



## Approach 1 — Brute force (single one-way map)

**Intuition.** Walk both strings. Maintain a map `s → t`. If the mapping conflicts, return false.



```java
boolean isIsomorphicBrute(String s, String t) {
    Map<Character, Character> m = new HashMap<>();
    for (int i = 0; i < s.length(); i++) {
        char a = s.charAt(i), b = t.charAt(i);
        if (m.containsKey(a)) {
            if (m.get(a) != b) return false;
        } else {
            m.put(a, b);
        }
    }
    return true;
}
```



**Complexity** — Time **O(n)**; Space **O(σ)**. **Wrong for `s="ab", t="aa"`** — one-way map allows two source chars to collide on the same target. *In an interview* recognize this and add the reverse map.

---

## Approach 2 — Two maps enforcing bijection (canonical)

**Insight.** A bijection requires **both directions**: no two source chars share a target *and* no two targets come from the same source. Track both `fwd[a] = b` and `bwd[b] = a`; any inconsistency = false.



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

**Complexity** — Time **O(n)**; Space **O(σ)**. *Say aloud in an interview:* "same bijection pattern as Word Pattern — one-way maps allow surjective, not bijective."

## Approach 3 — First-index trick (elegant one-liner)

`s` and `t` isomorphic iff `firstIndex(s[i]) == firstIndex(t[i])` for all `i`. Different data structure, same asymptotic complexity, tighter proof.

---

## Try it yourself

<JavaRunner problem-slug="isomorphic-strings" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| One-way map | O(n) | O(σ) | Wrong on collisions |
| **Two maps** | **O(n)** | O(σ) | **Canonical** |
| First-index | O(n) | O(σ) | Elegant alternative |

## When to use which

- **Bijection check** → two maps.
- **Word pattern** — similar bijection with words.

<AiCompanion problem-slug="isomorphic-strings" pattern-hint="hashing" />

## Related problems

- [Word Pattern](https://leetcode.com/problems/word-pattern/)
- [Group Shifted Strings](/problems/group-shifted-strings)
- [Valid Anagram](/problems/valid-anagram)

<FeedbackWidget problem-slug="isomorphic-strings" />

<RelatedProblems problems="group-shifted-strings::Group Shifted Strings|3sum::3sum|valid-anagram::Valid Anagram" />
