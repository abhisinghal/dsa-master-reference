# Hashing — Group Shifted Strings

*[↗ LeetCode: Group Shifted Strings](https://leetcode.com/problems/group-shifted-strings/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/hashing)

<CompanyTags companies="Meta, Google, Uber" />

Group strings that are cyclic shifts of each other.

**Example 1** — `strings=["abc","bcd","acef","xyz","az","ba","a","z"]` → `[["abc","bcd","xyz"],["acef"],["az","ba"],["a","z"]]`

**Constraints** — `1 ≤ #strings ≤ 200`.


<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/>
---

<MarkSolved problem-slug="group-shifted-strings" /> <Bookmark problem-slug="group-shifted-strings" />

<InterviewTimer problem-slug="group-shifted-strings" />



## Approach — Canonical key = diff pattern (canonical)

**Insight.** Two strings are shifts iff their consecutive char-diffs (mod 26) match.

**Trap** — Java `%` can be negative. Use `+ 26) % 26`. Delimit numbers so `"11"` doesn't collide with `"1,1"`.



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



<CodeTrace
  title="Canonical key = diff pattern (canonical)"
  :values="['abc', 'bcd', 'acef', 'xyz', 'az', 'ba', 'a', 'z']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 4 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 7 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(Σ length)**; Space **O(Σ length)**.

---

## Try it yourself

<JavaRunner problem-slug="group-shifted-strings" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Canonical key | **O(Σ length)** | O(Σ length) | canonical |

## When to use which

- **Any "group by equivalence class"** → canonical key.
- **Group anagrams** → sort key.
- **Group similar words** → similar canonical hash.

<AiCompanion problem-slug="group-shifted-strings" pattern-hint="hashing" />

## Related problems

- [Group Anagrams](https://leetcode.com/problems/group-anagrams/)
- [Isomorphic Strings](/problems/isomorphic-strings)

<FeedbackWidget problem-slug="group-shifted-strings" />

<RelatedProblems problems="hashing-two-sum::Hashing Two Sum|longest-consecutive-sequence::Longest Consecutive Sequence|3sum::3sum" />
