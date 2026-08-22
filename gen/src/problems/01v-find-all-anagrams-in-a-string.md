# Sliding Window — Find All Anagrams in a String

*[↗ LeetCode: Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Return all starting indices where `p`'s anagram appears in `s`.

## Approach — Fixed-window with `matches` counter

**Insight.** Same skeleton as Permutation in String, but collect every matching index instead of returning early. Use a `matches` counter (26 buckets equal) for O(1) per step.

```java
List<Integer> findAnagrams(String s, String p) {
    List<Integer> out = new ArrayList<>();
    if (p.length() > s.length()) return out;
    int[] need = new int[26], have = new int[26];
    for (char c : p.toCharArray()) need[c - 'a']++;
    int distinct = 0;
    for (int c : need) if (c > 0) distinct++;
    int matches = 0, k = p.length();
    for (int i = 0; i < s.length(); i++) {
        int idx = s.charAt(i) - 'a';
        have[idx]++;
        if (have[idx] == need[idx]) matches++;
        else if (have[idx] == need[idx] + 1) matches--;
        if (i >= k) {
            int out_idx = s.charAt(i - k) - 'a';
            have[out_idx]--;
            if (have[out_idx] == need[out_idx]) matches++;
            else if (have[out_idx] == need[out_idx] - 1) matches--;
        }
        if (matches == distinct) out.add(i - k + 1);
    }
    return out;
}
```

**Complexity** — Time **O(n)**; Space **O(1)**.

## Related problems

- [Permutation in String](/problems/permutation-in-string) — return boolean
- [Valid Anagram](/problems/valid-anagram)
