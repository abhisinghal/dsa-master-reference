# Sliding Window — Permutation in String

*[↗ LeetCode: Permutation in String](https://leetcode.com/problems/permutation-in-string/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Return true if `s2` contains any permutation of `s1` as a substring.

---

## Approach 1 — Fixed-size window with frequency-match
**Insight.** Same as anagram-matching: slide a window of size `|s1|` across `s2`; keep a 26-int count. Match when window count equals target count.



```java
boolean checkInclusion(String s1, String s2) {
    if (s1.length() > s2.length()) return false;
    int[] need = new int[26], win = new int[26];
    for (char c : s1.toCharArray()) need[c - 'a']++;
    int k = s1.length();
    for (int i = 0; i < s2.length(); i++) {
        win[s2.charAt(i) - 'a']++;
        if (i >= k) win[s2.charAt(i - k) - 'a']--;
        if (Arrays.equals(need, win)) return true;
    }
    return false;
}
```



**Complexity** — Time **O((n - k) · 26)**; Space **O(1)**.

---

## Approach 2 — Optimized comparison — running match count
Instead of `Arrays.equals` per step (26-cost), maintain a `matches` counter incrementally: increment when a frequency bucket becomes equal after add/remove, decrement when it moves away. Turns each step into O(1).

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Fixed-size window with frequency-match | O((n - k) · 26) | O(1) | baseline |
| Optimized comparison — running match count | O(1) | — | optimum |

## When to use which

- **State it for signal** → Fixed-size window with frequency-match (O((n - k) · 26)). Correct baseline; call it out then move on.
- **Ship this** → Optimized comparison — running match count (O(1), —). Expected optimum in interview.

## Related problems

- [Find All Anagrams in a String](/problems/find-all-anagrams-in-a-string) — return all indices
- [Substring with Concatenation of All Words](/problems/substring-with-concatenation-of-all-words)
