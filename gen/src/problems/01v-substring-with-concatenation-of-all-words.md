# Sliding Window — Substring With Concatenation of All Words

*[↗ LeetCode: Substring with Concatenation of All Words](https://leetcode.com/problems/substring-with-concatenation-of-all-words/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/sliding-window)

Find start indices of substrings that are concatenations of every word in `words` (each used exactly once, any order). All words same length `L`.

## Approach 1 — Try every start

O(n · k · L). Too slow for large.

## Approach 2 — Sliding window on word-aligned offsets

**Insight.** Iterate `offset ∈ [0, L)`. For each offset, walk `s` in chunks of L. Maintain a `have` count; if a word not in `words`, reset window; if a word over-count, shrink from left until fine. Emit start when `have == k` words.

```java
List<Integer> findSubstring(String s, String[] words) {
    List<Integer> out = new ArrayList<>();
    int L = words[0].length(), k = words.length;
    int total = L * k;
    if (s.length() < total) return out;
    Map<String, Integer> need = new HashMap<>();
    for (String w : words) need.merge(w, 1, Integer::sum);
    for (int off = 0; off < L; off++) {
        int l = off, have = 0;
        Map<String, Integer> win = new HashMap<>();
        for (int r = off; r + L <= s.length(); r += L) {
            String w = s.substring(r, r + L);
            if (!need.containsKey(w)) { win.clear(); have = 0; l = r + L; continue; }
            win.merge(w, 1, Integer::sum);
            have++;
            while (win.get(w) > need.get(w)) {
                String lw = s.substring(l, l + L);
                win.merge(lw, -1, Integer::sum);
                have--;
                l += L;
            }
            if (have == k) out.add(l);
        }
    }
    return out;
}
```

**Complexity** — Time **O(n · L)** total across offsets; Space **O(k · L)**.

## Related problems

- [Minimum Window Substring](/problems/minimum-window-substring)
- [Find All Anagrams in a String](/problems/find-all-anagrams-in-a-string)
