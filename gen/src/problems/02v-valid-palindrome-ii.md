# Two Pointers — Valid Palindrome II

*[↗ LeetCode: Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

Given `s`, return true if you can delete at most one character to make it a palindrome.

## Approach — Two pointers + one skip

**Insight.** Advance `l`, `r` from ends. On mismatch, try skipping `l` OR skipping `r` — check whichever remaining substring is a palindrome.

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

**Complexity** — Time **O(n)**; Space **O(1)**.

**Extension.** Delete-at-most-k → recursive two-pointer with memoization, or use LCS with reverse (LPS-based).

## Related problems

- [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) — 0 deletions
- [Longest Palindromic Subsequence](/problems/longest-palindromic-subsequence) — k-deletion generalization
