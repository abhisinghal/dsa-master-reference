# Sliding Window — Permutation in String

*[↗ LeetCode: Permutation in String](https://leetcode.com/problems/permutation-in-string/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

&lt;CompanyTags companies="Meta, Google, Microsoft, Amazon, Apple" /&gt;

Given strings `s1` and `s2`, return `true` iff `s2` contains any permutation of `s1` as a substring.

**Example 1** — `s1 = "ab", s2 = "eidbaooo"` → `true` (`"ba"` is a permutation of `"ab"`)
**Example 2** — `s1 = "ab", s2 = "eidboaoo"` → `false`
**Example 3** — `s1 = "adc", s2 = "dcda"` → `true` (`"dca"` at index 0)

**Constraints** — `1 ≤ |s1|, |s2| ≤ 10⁴`. Lowercase English.


&lt;Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/&gt;
---

## Approach 1 — Sort every window

**Intuition.** Slide a window of size `|s1|` over `s2`; sort each and compare to sorted `s1`.



```java
boolean checkInclusionBrute(String s1, String s2) {
    int k = s1.length();
    if (k > s2.length()) return false;
    char[] a = s1.toCharArray();
    Arrays.sort(a);
    String target = new String(a);
    for (int i = 0; i + k <= s2.length(); i++) {
        char[] w = s2.substring(i, i + k).toCharArray();
        Arrays.sort(w);
        if (target.equals(new String(w))) return true;
    }
    return false;
}
```



<CodeTrace
  title="Brute — s1='ab', s2='eidbaooo'"
  :values="['e','i','d','b','a','o','o','o']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { window: "ei", sorted: "ei", target: "ab" }, note: "no match" },
    { pointers: { i: 2 }, vars: { window: "db", sorted: "bd", target: "ab" }, note: "no match" },
    { pointers: { i: 3 }, vars: { window: "ba", sorted: "ab", target: "ab" }, note: "match! return true" }
  ]'
/>

**Complexity** — Time **O((n − k) · k log k)**; Space **O(k)** per window.

---

## Approach 2 — Fixed window with frequency array

**Insight from brute.** Sorting is overkill — we just need the multiset. A 26-int frequency count is enough. Compare `need[]` vs current `have[]` at every position.



```java
boolean checkInclusionEq(String s1, String s2) {
    int k = s1.length();
    if (k > s2.length()) return false;
    int[] need = new int[26], have = new int[26];
    for (char c : s1.toCharArray()) need[c - 'a']++;
    for (int i = 0; i < s2.length(); i++) {
        have[s2.charAt(i) - 'a']++;
        if (i >= k) have[s2.charAt(i - k) - 'a']--;
        if (i >= k - 1 && Arrays.equals(need, have)) return true;
    }
    return false;
}
```



<CodeTrace
  title="Fixed window + Arrays.equals — s1='ab', s2='eidbaooo'"
  :values="['e','i','d','b','a','o','o','o']"
  :windowKeys="['left','right']"
  :cellWidth="34"
  :steps='[
    { pointers: { left: 0, right: 1 }, vars: { have: "{e:1,i:1}", need: "{a:1,b:1}" }, note: "not equal" },
    { pointers: { left: 2, right: 3 }, vars: { have: "{d:1,b:1}", need: "{a:1,b:1}" }, note: "not equal" },
    { pointers: { left: 3, right: 4 }, vars: { have: "{b:1,a:1}", need: "{a:1,b:1}" }, note: "equal — return true" }
  ]'
/>

**Complexity** — Time **O((n − k) · 26)**; Space **O(1)**.

---

## Approach 3 — Running match counter (O(1) per step)

**Insight from previous.** `Arrays.equals` costs 26 per position. Maintain a `matches` counter: for each of the 26 letters, track whether `have[c] == need[c]`. Increment/decrement `matches` incrementally on every add/remove.



```java
boolean checkInclusion(String s1, String s2) {
    int k = s1.length();
    if (k > s2.length()) return false;
    int[] need = new int[26], have = new int[26];
    for (char c : s1.toCharArray()) need[c - 'a']++;
    int matches = 0;
    for (int i = 0; i < 26; i++) if (need[i] == 0) matches++;
    for (int i = 0; i < s2.length(); i++) {
        int r = s2.charAt(i) - 'a';
        have[r]++;
        if (have[r] == need[r]) matches++;
        else if (have[r] == need[r] + 1) matches--;
        if (i >= k) {
            int l = s2.charAt(i - k) - 'a';
            have[l]--;
            if (have[l] == need[l]) matches++;
            else if (have[l] == need[l] - 1) matches--;
        }
        if (matches == 26) return true;
    }
    return false;
}
```



<CodeTrace
  title="Running match — s1='ab', s2='eidbaooo'"
  :values="['e','i','d','b','a','o','o','o']"
  :windowKeys="['left','right']"
  :cellWidth="34"
  :steps='[
    { pointers: { left: 0, right: 0 }, vars: { matches: 24 }, note: "24 letters already match (0=0); 2 mismatches (a, b)" },
    { pointers: { left: 3, right: 3 }, vars: { matches: 25 }, note: "have[b]=1=need[b] → matches++" },
    { pointers: { left: 3, right: 4 }, vars: { matches: 26 }, note: "have[a]=1=need[a] → matches=26 → return true" }
  ]'
/>

**Complexity** — Time **O(n)** — O(1) per position; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="permutation-in-string" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort every window | O((n−k) · k log k) | O(k) | brute; correct baseline |
| Fixed window + `Arrays.equals` | O((n−k) · 26) | O(1) | acceptable, since 26 is a constant |
| Running match counter | **O(n)** | O(1) | polish — mention if asked to justify |

## When to use which

- **Anagram / multi-set check** → fixed window + frequency array is the canonical answer.
- **Interviewer asks "can you do without the 26 factor?"** → running match counter.
- **Unicode alphabet** → use `HashMap<Character,Integer>`; running-match trick still applies with slightly more bookkeeping.
- **Return all match indices** → this is [Find All Anagrams in a String](/problems/find-all-anagrams-in-a-string).

&lt;AiCompanion problem-slug="permutation-in-string" pattern-hint="sliding window" /&gt;

## Related problems

- [Find All Anagrams in a String](/problems/find-all-anagrams-in-a-string) — return all match positions
- [Valid Anagram](/problems/valid-anagram) — single comparison
- [Minimum Window Substring](/problems/minimum-window-substring) — variable-size window with need/have
- [Substring with Concatenation of All Words](/problems/substring-with-concatenation-of-all-words) — window on word offsets