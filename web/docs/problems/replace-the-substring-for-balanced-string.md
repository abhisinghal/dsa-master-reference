# Sliding Window — Replace the Substring for Balanced String

*[↗ LeetCode: Replace the Substring for Balanced String](https://leetcode.com/problems/replace-the-substring-for-balanced-string/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

String of Q,W,E,R (length n divisible by 4). Return length of the smallest substring to replace so each letter appears n/4 times.

---

## Approach 1 — Sliding window over "outside" counts
**Insight.** A substring `[l, r]` is a valid replacement window iff **outside** it, no letter exceeds `n/4`. Equivalently, `outsideCount[x] ≤ n/4` for all x.

Sweep r, decrement inside-window-adjusted counts implicitly; shrink l while the outside-condition still holds; track min window length.



```java
int balancedString(String s) {
    int n = s.length(), k = n / 4;
    int[] cnt = new int[128];
    for (char c : s.toCharArray()) cnt[c]++;
    int l = 0, best = n;
    for (int r = 0; r < n; r++) {
        cnt[s.charAt(r)]--; // temporarily "remove" s[r] from outside
        while (l < n && cnt['Q'] <= k && cnt['W'] <= k && cnt['E'] <= k && cnt['R'] <= k) {
            best = Math.min(best, r - l + 1);
            cnt[s.charAt(l++)]++;
        }
    }
    return best;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sliding window over "outside" counts | O(n) | O(1) | primary |

## When to use which

- **Ship this** → Sliding window over "outside" counts (O(n), O(1)). The pattern's standard solution.

## Related problems

- [Longest Repeating Character Replacement](/problems/longest-repeating-character-replacement)
- [Minimum Operations to Make All Array Elements Equal](https://leetcode.com/problems/minimum-operations-to-make-array-equal/)
