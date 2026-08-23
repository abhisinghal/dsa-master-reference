# Hashing — Valid Anagram

*[↗ LeetCode: Valid Anagram](https://leetcode.com/problems/valid-anagram/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/hashing)

<CompanyTags companies="Meta, Amazon, Google, Bloomberg" />

Given two strings `s` and `t`, return `true` iff `t` is an anagram of `s`.

**Example 1** — `s = "anagram", t = "nagaram"` → `true`
**Example 2** — `s = "rat", t = "car"` → `false`
**Example 3** — `s = "aa", t = "a"` → `false` (different lengths)

**Constraints** — `1 ≤ n ≤ 5 · 10⁴`. Lowercase English.


<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/>
---

## Approach 1 — Sort both and compare

**Intuition.** Two strings are anagrams iff their sorted forms are equal.

```java
boolean isAnagramSort(String s, String t) {
    if (s.length() != t.length()) return false;
    char[] a = s.toCharArray(); Arrays.sort(a);
    char[] b = t.toCharArray(); Arrays.sort(b);
    return Arrays.equals(a, b);
}
```

**Complexity** — Time **O(n log n)**; Space **O(n)**.

---

## Approach 2 — Frequency array (ASCII)

**Insight from sort.** We don't need order — just multi-set equality. Increment on `s`, decrement on `t`; verify all zeros.

```java
boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] cnt = new int[26];
    for (int i = 0; i < s.length(); i++) {
        cnt[s.charAt(i) - 'a']++;
        cnt[t.charAt(i) - 'a']--;
    }
    for (int c : cnt) if (c != 0) return false;
    return true;
}
```

<CodeTrace
  title="Frequency — s='rat', t='car'"
  :values="['r','a','t','vs','c','a','r']"
  :windowKeys="['i']"
  :cellWidth="30"
  :steps='[
    { pointers: { i: 0 }, vars: { cnt: "{r:1, c:-1}", }, note: "s[0]=r, t[0]=c" },
    { pointers: { i: 1 }, vars: { cnt: "{r:1, c:-1, a:0}" }, note: "s[1]=a, t[1]=a → cancel" },
    { pointers: { i: 2 }, vars: { cnt: "{r:1, c:-1, a:0, t:1}" }, note: "s[2]=t, t[2]=r → r bumps to 2? wait" },
    { pointers: { i: 3 }, vars: { cnt: "{r:0, c:-1, a:0, t:1}", nonzero: "c, t" }, note: "non-zero c and t → return false" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)** (26 buckets).

---

## Approach 3 — Unicode-safe: HashMap

**Insight from ASCII.** If `s, t` may contain Unicode (surrogate pairs etc.), use `codePoints()` and a HashMap.

```java
boolean isAnagramUnicode(String s, String t) {
    if (s.codePointCount(0, s.length()) != t.codePointCount(0, t.length())) return false;
    Map<Integer, Integer> cnt = new HashMap<>();
    s.codePoints().forEach(c -> cnt.merge(c, 1, Integer::sum));
    t.codePoints().forEach(c -> cnt.merge(c, -1, Integer::sum));
    for (int v : cnt.values()) if (v != 0) return false;
    return true;
}
```

**Complexity** — Time **O(n)**; Space **O(σ)** where σ ≤ n.

---

## Try it yourself

<JavaRunner problem-slug="valid-anagram" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort both | O(n log n) | O(n) | baseline |
| Frequency array (ASCII) | **O(n)** | **O(1)** | expected optimum |
| HashMap (Unicode) | O(n) | O(σ) | generalization |

## When to use which

- **Lowercase English** → `int[26]` frequency array.
- **General ASCII** → `int[128]` or `int[256]`.
- **Unicode / emoji** → HashMap over code points.
- **Stream / can't materialize `t`** → maintain running count of `s` first, then decrement as `t` arrives; return false early on any negative overshoot.

<AiCompanion problem-slug="valid-anagram" pattern-hint="hashing" />

## Related problems

- [Find All Anagrams in a String](/problems/find-all-anagrams-in-a-string) — sliding window
- [Group Anagrams](https://leetcode.com/problems/group-anagrams/) — canonical-key hashing
- [Permutation in String](/problems/permutation-in-string) — sliding boolean version