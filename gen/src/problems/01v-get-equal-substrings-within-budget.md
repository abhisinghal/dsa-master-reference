# Sliding Window — Get Equal Substrings Within Budget

*[↗ LeetCode: Get Equal Substrings Within Budget](https://leetcode.com/problems/get-equal-substrings-within-budget/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Given `s`, `t`, `maxCost`. Convert `s[i]` → `t[i]` costs `|s[i] - t[i]|`. Return the longest substring convertible within `maxCost`.

---

## Approach 1 — Sliding window on the cost array
**Insight.** Compute `diff[i] = |s[i] - t[i]|`. Now: longest subarray with sum ≤ maxCost — classic positive-only sliding window.

```java
int equalSubstring(String s, String t, int maxCost) {
    int l = 0, cost = 0, best = 0;
    for (int r = 0; r < s.length(); r++) {
        cost += Math.abs(s.charAt(r) - t.charAt(r));
        while (cost > maxCost) cost -= Math.abs(s.charAt(l) - t.charAt(l++));
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sliding window on the cost array | O(n) | O(1) | primary |

## When to use which

- **Ship this** → Sliding window on the cost array (O(n), O(1)). The pattern's standard solution.

## Related problems

- [Longest Substring With At Most K Distinct](/problems/longest-substring-with-at-most-k-distinct)
- [Max Consecutive Ones III](/problems/max-consecutive-ones-iii)
