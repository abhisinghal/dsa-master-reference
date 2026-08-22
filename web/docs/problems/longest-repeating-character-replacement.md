# Sliding Window — Longest Repeating Character Replacement

*[↗ LeetCode: Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Longest substring achievable by replacing at most `k` characters so all become identical.

## Approach — Sliding window with `maxCount`

**Insight.** A window `[l, r]` is valid iff `windowLen - maxCount ≤ k` (where `maxCount` is the most frequent letter's count in the window). We don't need to shrink `maxCount` precisely — once we lock in a `maxCount`, only a **larger** window with a strictly larger max is interesting.



```java
int characterReplacement(String s, int k) {
    int[] cnt = new int[26];
    int l = 0, maxCount = 0, best = 0;
    for (int r = 0; r < s.length(); r++) {
        cnt[s.charAt(r) - 'A']++;
        maxCount = Math.max(maxCount, cnt[s.charAt(r) - 'A']);
        if (r - l + 1 - maxCount > k) {
            cnt[s.charAt(l++) - 'A']--;
        }
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```



**Why the "lazy maxCount" is OK.** We only care about finding the best `best`; if `maxCount` becomes stale (window's real max is lower), we still shrink by exactly one per step, but never grow the answer. The final `best` remains correct.

**Complexity** — Time **O(n)**; Space **O(1)**.

## Related problems

- [Longest Substring With At Most K Distinct](/problems/longest-substring-with-at-most-k-distinct)
- [Replace the Substring for Balanced String](/problems/replace-the-substring-for-balanced-string)
