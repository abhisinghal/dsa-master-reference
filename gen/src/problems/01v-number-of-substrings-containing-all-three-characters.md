# Sliding Window — Number of Substrings Containing All Three Characters

*[↗ LeetCode: Number of Substrings Containing All Three Characters](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Count substrings containing at least one 'a', one 'b', one 'c'.

---

## Approach 1 — For each r, count valid `l`s
**Insight.** Once window `[l, r]` contains all three, **every** `l' ≤ l` also works up to r. So for each r, add `l` (the smallest left with all three) to the answer. Then continue extending r.

```java
int numberOfSubstrings(String s) {
    int[] cnt = new int[3];
    int l = 0, res = 0;
    for (int r = 0; r < s.length(); r++) {
        cnt[s.charAt(r) - 'a']++;
        while (cnt[0] > 0 && cnt[1] > 0 && cnt[2] > 0) {
            cnt[s.charAt(l++) - 'a']--;
        }
        res += l; // number of valid starts is `l` (0..l-1)
    }
    return res;
}
```

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| For each r, count valid `l`s | O(n) | O(1) | primary |

## When to use which

- **Ship this** → For each r, count valid `l`s (O(n), O(1)). The pattern's standard solution.

## Related problems

- [Longest Substring With At Most K Distinct](/problems/longest-substring-with-at-most-k-distinct)
- [Subarrays with K Different Integers](/problems/subarrays-with-k-different-integers)
