# Sliding Window — Longest Palindromic Substring

*[↗ LeetCode: Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Amazon, Meta, Google, Microsoft, Bloomberg, Adobe" />

Return the longest palindromic substring of `s`.

**Example 1** — `s="babad"` → `"bab"` or `"aba"`
**Example 2** — `s="cbbd"` → `"bb"`
**Example 3** — `s="a"` → `"a"`

**Constraints** — `1 ≤ n ≤ 1000`.


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

<MarkSolved problem-slug="longest-palindromic-substring" /> <Bookmark problem-slug="longest-palindromic-substring" />

<InterviewTimer problem-slug="longest-palindromic-substring" />



## Approach 1 — Every substring O(n³)

## Approach 2 — DP `pal[i][j]`

O(n²) time and space.

## Approach 3 — Expand around each center (canonical)

**Insight.** A palindrome has an odd or even center — 2n-1 centers total. Expand outward while chars match.



```java
String longestPalindrome(String s) {
    int start = 0, end = 0;
    for (int i = 0; i < s.length(); i++) {
        int l1 = expand(s, i, i);
        int l2 = expand(s, i, i + 1);
        int len = Math.max(l1, l2);
        if (len > end - start) {
            start = i - (len - 1) / 2;
            end = i + len / 2;
        }
    }
    return s.substring(start, end + 1);
}
int expand(String s, int l, int r) {
    while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; }
    return r - l - 1;
}
```



<CodeTrace
  title="Expand around center — s='babad'"
  :values="['b','a','b','a','d']"
  :windowKeys="['l','r']"
  :cellWidth="34"
  :steps='[
    { pointers: { l: 0, r: 2 }, vars: { center: 1, len: 3, best: "bab" }, note: "center=1 (a), expand to bab" },
    { pointers: { l: 1, r: 3 }, vars: { center: 2, len: 3, best: "bab or aba" }, note: "center=2 (b), aba tied" },
    { pointers: { l: 3, r: 4 }, vars: { center: 3.5, len: 0 }, note: "no even palindrome" }
  ]'
/>

## Approach 4 — Manacher's O(n)

Sentinels + palindrome-radius array with reuse across mirrored centers.

**Complexity** — Time **O(n²)** expand; **O(n)** Manacher; Space **O(1)** expand.

---

## Try it yourself

<JavaRunner problem-slug="longest-palindromic-substring" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Every substring | O(n³) | O(1) | baseline |
| DP `pal[i][j]` | O(n²) | O(n²) | works |
| Expand around center | **O(n²)** | **O(1)** | canonical |
| Manacher | O(n) | O(n) | polish |

## When to use which

- **Standard interview** → expand around center.
- **Very large n** → Manacher.
- **Return count of palindromic substrings** → same expand, just count.

<AiCompanion problem-slug="longest-palindromic-substring" pattern-hint="sliding window" />

## Related problems

- [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/)
- [Longest Palindromic Subsequence](/problems/longest-palindromic-subsequence)
- [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)

<FeedbackWidget problem-slug="longest-palindromic-substring" />

<RelatedProblems problems="find-all-anagrams-in-a-string::Find All Anagrams In A String|sliding-window-longest-substring::Sliding Window Longest Substring|subarrays-with-k-different-integers::Subarrays With K Different Integers" />
