# Two Pointers — Valid Palindrome II

*[↗ LeetCode: Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Meta, Amazon, Google" />

Given a string `s`, return `true` if it can become a palindrome by deleting **at most one** character.

**Example 1** — `s = "aba"` → `true`
**Example 2** — `s = "abca"` → `true` (delete `c` or `b`)
**Example 3** — `s = "abc"` → `false`

**Constraints** — `1 ≤ n ≤ 10⁵`. Lowercase ASCII.


<Hints
  hint1="Sort first if the input isn’t already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/>
---

## Approach 1 — Try deleting each position

**Intuition.** For each `i`, check if `s` minus index `i` is a palindrome. Plus check the original.

```java
boolean validPalindromeBrute(String s) {
    if (isPali(s, 0, s.length() - 1)) return true;
    for (int i = 0; i < s.length(); i++) {
        String t = s.substring(0, i) + s.substring(i + 1);
        if (isPali(t, 0, t.length() - 1)) return true;
    }
    return false;
}
boolean isPali(String s, int l, int r) {
    while (l < r) if (s.charAt(l++) != s.charAt(r--)) return false;
    return true;
}
```

**Complexity** — Time **O(n²)**; Space **O(n)** per substring.

---

## Approach 2 — Two pointers with one deletion budget

**Insight from brute.** Walk from ends. On mismatch, we have exactly two options: skip `l` OR skip `r`. Try both and return whether either remaining substring is a palindrome. Any subsequent mismatch would exceed the budget.

```java
boolean validPalindrome(String s) {
    int l = 0, r = s.length() - 1;
    while (l < r) {
        if (s.charAt(l) != s.charAt(r))
            return isPali(s, l + 1, r) || isPali(s, l, r - 1);
        l++; r--;
    }
    return true;
}
boolean isPali(String s, int l, int r) {
    while (l < r) if (s.charAt(l++) != s.charAt(r--)) return false;
    return true;
}
```

<CodeTrace
  title="Two pointers — s='abca'"
  :values="['a','b','c','a']"
  :windowKeys="['l','r']"
  :cellWidth="38"
  :steps='[
    { pointers: { l: 0, r: 3 }, vars: { match: true }, note: "a == a → advance" },
    { pointers: { l: 1, r: 2 }, vars: { match: false }, note: "b ≠ c → try skip l OR skip r" },
    { pointers: { l: 2, r: 2 }, vars: { branchA: "check s[2..2]=c" }, note: "skip l — trivially palindrome" },
    { pointers: { l: 1, r: 1 }, vars: { branchB: "check s[1..1]=b" }, note: "skip r — trivially palindrome → return true" }
  ]'
/>

**Complexity** — Time **O(n)** — each mismatch triggers at most 2 O(n) checks; Space **O(1)**.

---

## Approach 3 — Generalization to k deletions

**Insight.** For `k > 1` deletions, recursion on the two options at each mismatch with memoization gives O(n · k). Equivalent to: is `s` k-close to a palindrome — related to LPS (Longest Palindromic Subsequence): answer yes iff `n - LPS(s) ≤ k`.

```java
boolean validPalindromeK(String s, int k) {
    int lps = longestPalindromicSubseq(s);
    return s.length() - lps <= k;
}
```

**Complexity** — Time **O(n²)** via LPS DP; Space **O(n²)** or O(n) with roll-down. Overkill for `k = 1`.

---

## Try it yourself

<JavaRunner problem-slug="valid-palindrome-ii" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Try deleting each position | O(n²) | O(n) | baseline |
| Two pointers + budget | **O(n)** | O(1) | expected optimum |
| LPS DP for general k | O(n²) | O(n) | generalization |

## When to use which

- **Standard "at most 1 deletion"** → two-pointer with budget.
- **Larger k** → LPS DP.
- **"Return the resulting palindrome"** → trace the branch that succeeded and construct the string.
- **Case-insensitive / alphanumeric-only** — see [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) for the parsing rules.

<AiCompanion problem-slug="valid-palindrome-ii" pattern-hint="two pointers" />

## Related problems

- [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) — zero deletions
- [Longest Palindromic Subsequence](/problems/longest-palindromic-subsequence) — LPS DP
- [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/)