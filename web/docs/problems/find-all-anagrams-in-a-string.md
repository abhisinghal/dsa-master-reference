# Sliding Window — Find All Anagrams in a String

*[↗ LeetCode: Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft, Uber" /&gt;

Given strings `s` and `p`, return all starting indices in `s` where a permutation of `p` occurs as a substring.

**Example 1** — `s = "cbaebabacd", p = "abc"` → `[0, 6]` (windows `"cba"` and `"bac"`)
**Example 2** — `s = "abab", p = "ab"` → `[0, 1, 2]`
**Example 3** — `s = "aaaaaaaaaa", p = "aaaa"` → `[0,1,2,3,4,5,6]`

**Constraints** — `1 ≤ |s|, |p| ≤ 3 · 10⁴`. Lowercase English.


&lt;Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/&gt;
---

&lt;MarkSolved problem-slug="find-all-anagrams-in-a-string" /&gt;

&lt;InterviewTimer problem-slug="find-all-anagrams-in-a-string" /&gt;



## Approach 1 — Sort every window

**Intuition.** Slide window of size `|p|`; sort each substring; compare to sorted `p`.



```java
List<Integer> findAnagramsBrute(String s, String p) {
    List<Integer> out = new ArrayList<>();
    int k = p.length();
    char[] pa = p.toCharArray(); Arrays.sort(pa);
    String pt = new String(pa);
    for (int i = 0; i + k <= s.length(); i++) {
        char[] w = s.substring(i, i + k).toCharArray();
        Arrays.sort(w);
        if (pt.equals(new String(w))) out.add(i);
    }
    return out;
}
```



**Complexity** — Time **O((n − k) · k log k)**; Space **O(k)** per window.

---

## Approach 2 — Fixed window + `Arrays.equals`

**Insight.** Same as [Permutation in String](/problems/permutation-in-string) — a 26-int frequency map suffices; compare via `Arrays.equals` at each step.



```java
List<Integer> findAnagramsEq(String s, String p) {
    List<Integer> out = new ArrayList<>();
    int k = p.length();
    if (k > s.length()) return out;
    int[] need = new int[26], have = new int[26];
    for (char c : p.toCharArray()) need[c - 'a']++;
    for (int i = 0; i < s.length(); i++) {
        have[s.charAt(i) - 'a']++;
        if (i >= k) have[s.charAt(i - k) - 'a']--;
        if (i >= k - 1 && Arrays.equals(need, have)) out.add(i - k + 1);
    }
    return out;
}
```



**Complexity** — Time **O((n − k) · 26)** ≈ O(n); Space **O(1)**.

---

## Approach 3 — Running match counter

**Insight from previous.** Skip the 26-cost equality check by maintaining a `matches` counter that reflects how many of the 26 buckets currently satisfy `have[i] == need[i]`.



```java
List<Integer> findAnagrams(String s, String p) {
    List<Integer> out = new ArrayList<>();
    int k = p.length();
    if (k > s.length()) return out;
    int[] need = new int[26], have = new int[26];
    for (char c : p.toCharArray()) need[c - 'a']++;
    int matches = 0;
    for (int i = 0; i < 26; i++) if (need[i] == 0) matches++;
    for (int i = 0; i < s.length(); i++) {
        int r = s.charAt(i) - 'a';
        have[r]++;
        if (have[r] == need[r]) matches++;
        else if (have[r] == need[r] + 1) matches--;
        if (i >= k) {
            int l = s.charAt(i - k) - 'a';
            have[l]--;
            if (have[l] == need[l]) matches++;
            else if (have[l] == need[l] - 1) matches--;
        }
        if (matches == 26) out.add(i - k + 1);
    }
    return out;
}
```



<CodeTrace
  title="Running match — s='cbaebabacd', p='abc'"
  :values="['c','b','a','e','b','a','b','a','c','d']"
  :windowKeys="['left','right']"
  :cellWidth="30"
  :steps='[
    { pointers: { left: 0, right: 2 }, vars: { window: "cba", matches: 26 }, note: "match at start=0 → emit 0" },
    { pointers: { left: 1, right: 3 }, vars: { window: "bae", matches: 25 }, note: "e replaces c — mismatch" },
    { pointers: { left: 4, right: 6 }, vars: { window: "bab", matches: 24 }, note: "no match" },
    { pointers: { left: 6, right: 8 }, vars: { window: "bac", matches: 26 }, note: "match at start=6 → emit 6" }
  ]'
/>

**Complexity** — Time **O(n)** — O(1) per position; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="find-all-anagrams-in-a-string" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort every window | O((n−k) · k log k) | O(k) | baseline |
| Fixed window + `Arrays.equals` | O((n−k) · 26) | O(1) | acceptable |
| Running match counter | **O(n)** | O(1) | polish |

## When to use which

- **Standard interview answer** — fixed window + `Arrays.equals`. The 26-factor is a constant.
- **Interviewer probes for tighter bound** → running match counter.
- **Unicode alphabet** → running match with `HashMap` — same structure.
- **Return count only, not indices** → same skeleton; increment a counter instead of appending.

&lt;AiCompanion problem-slug="find-all-anagrams-in-a-string" pattern-hint="sliding window" /&gt;

## Related problems

- [Permutation in String](/problems/permutation-in-string) — boolean sibling
- [Valid Anagram](/problems/valid-anagram) — single pair
- [Minimum Window Substring](/problems/minimum-window-substring) — variable window with need/have
- [Substring with Concatenation of All Words](/problems/substring-with-concatenation-of-all-words)

&lt;FeedbackWidget problem-slug="find-all-anagrams-in-a-string" /&gt;

&lt;RelatedProblems problems="binary-subarrays-with-sum::Binary Subarrays With Sum|shortest-subarray-with-sum-at-least-k::Shortest Subarray With Sum At Least K|permutation-in-string::Permutation In String" /&gt;
