# Sliding Window — Longest Substring With At Most K Distinct

*[↗ LeetCode: Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Longest substring containing at most `k` distinct characters.

## Approach — Variable window with distinct counter

**Insight.** Extend right; on new distinct char increment `distinct`. If `distinct > k`, shrink from left: decrement each char's count; when a count hits 0, decrement `distinct`.



```java
int lengthOfLongestSubstringKDistinct(String s, int k) {
    if (k == 0) return 0;
    int[] cnt = new int[128];
    int distinct = 0, best = 0, l = 0;
    for (int r = 0; r < s.length(); r++) {
        if (cnt[s.charAt(r)]++ == 0) distinct++;
        while (distinct > k) {
            if (--cnt[s.charAt(l++)] == 0) distinct--;
        }
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```



**Complexity** — Time **O(n)**; Space **O(σ)**.

## Related problems

- [Longest Substring Without Repeating Characters](/problems/sliding-window-longest-substring) — k = ∞
- [Fruit Into Baskets](/problems/fruit-into-baskets) — k = 2
- [Longest Substring with At Most Two Distinct](https://leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters/)
