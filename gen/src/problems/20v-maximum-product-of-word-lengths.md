# Bit Manipulation — Maximum Product of Word Lengths

*[↗ LeetCode: Maximum Product of Word Lengths](https://leetcode.com/problems/maximum-product-of-word-lengths/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/bit-manip)

Return `max(len(w[i]) * len(w[j]))` over pairs whose character sets are disjoint (no shared letter).

---

## Approach 1 — Set intersection per pair
For each pair build a `Set<Character>` and check intersection. **O(n² · L)**.

---

## Approach 2 — Bitmask signatures
**Insight.** Each word only uses 26 lowercase letters → represent its letter set as a 26-bit int. Two words share no letters iff `mask[i] & mask[j] == 0`. Pair comparison becomes a single AND.

```java
int maxProduct(String[] words) {
    int n = words.length;
    int[] mask = new int[n];
    for (int i = 0; i < n; i++)
        for (char c : words[i].toCharArray())
            mask[i] |= 1 << (c - 'a');
    int best = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if ((mask[i] & mask[j]) == 0)
                best = Math.max(best, words[i].length() * words[j].length());
    return best;
}
```

**Complexity** — Time **O(n · L + n²)**; Space **O(n)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Set intersection per pair | O(n² · L) | — | baseline |
| Bitmask signatures | O(n · L + n²) | O(n) | optimum |

## When to use which

- **State it for signal** → Set intersection per pair (O(n² · L)). Correct baseline; call it out then move on.
- **Ship this** → Bitmask signatures (O(n · L + n²), O(n)). Expected optimum in interview.

## Related problems

- [Bitmask Subset Enumeration] — same 26-bit letter-set idea appears in word-existence/anagram problems
