# Hashing — Group Shifted Strings

*[↗ LeetCode: Group Shifted Strings](https://leetcode.com/problems/group-shifted-strings/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/hashing)

<CompanyTags companies="Meta, Google, Uber" />

Group strings that are cyclic shifts of each other.

**Example 1** — `strings=["abc","bcd","acef","xyz","az","ba","a","z"]` → `[["abc","bcd","xyz"],["acef"],["az","ba"],["a","z"]]`
**Example 2** — `strings=["a"]` → `[["a"]]`
**Example 3** — `strings=["abc","bcd","def"]` → `[["abc","bcd","def"]]` (all three shift-equivalent)

**Constraints** — `1 ≤ #strings ≤ 200`; string length ≤ 50. Brute pairwise-check is O(N²·L) = 200²·50 = 2·10⁶ — passes but fragile. Canonical key is O(Σ length) — a single linear scan.


<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its 'canonical form' — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For 'first duplicate', a `HashSet` and single-pass `add()` is enough."
/>
---

<MarkSolved problem-slug="group-shifted-strings" /> <Bookmark problem-slug="group-shifted-strings" />

<InterviewTimer problem-slug="group-shifted-strings" />



## Approach 1 — Brute force pairwise shift check

**Intuition.** For each pair (s, t), check whether one is a shift of the other by trying all 26 shift amounts. Group them via union-find or grouping-by-first-member.

```java
boolean isShift(String s, String t) {
    if (s.length() != t.length()) return false;
    int delta = (t.charAt(0) - s.charAt(0) + 26) % 26;
    for (int i = 0; i < s.length(); i++) {
        int d = (t.charAt(i) - s.charAt(i) + 26) % 26;
        if (d != delta) return false;
    }
    return true;
}
```

**Complexity** — Time **O(N²·L)** for the pairwise check; Space **O(N)** for group assignments. For `N=200, L=50` → 2·10⁶ — passes but O(N²) doesn't scale. *In an interview* say "canonical-key hashing collapses this to a linear scan."

---

## Approach 2 — Canonical key = diff pattern (canonical)

**Insight.** Two strings are shifts iff their **consecutive character diffs mod 26** match. `"abc"` → `(1, 1)`; `"bcd"` → `(1, 1)`; `"xyz"` → `(1, 1)`. All hash to the same key.

**Trap** — Java `%` can be negative on negative operands. Use `+ 26) % 26`. Delimit numbers so `"11"` doesn't collide with `"1,1"`.

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

**Complexity** — Time **O(Σ length)**; Space **O(Σ length)**. *Say aloud in an interview:* "canonical-key hashing is the pattern behind Group Anagrams, Isomorphic Strings, Group Shifted Strings — same three lines, different key function."

---

## Try it yourself

<JavaRunner problem-slug="group-shifted-strings" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Pairwise shift check | O(N²·L) | O(N) | Correct but O(N²) |
| **Canonical diff-key** | **O(Σ length)** | O(Σ length) | **Canonical** |

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
