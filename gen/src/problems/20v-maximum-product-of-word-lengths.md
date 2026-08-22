# Bit Manipulation — Maximum Product of Word Lengths

*[↗ LeetCode: Maximum Product of Word Lengths](https://leetcode.com/problems/maximum-product-of-word-lengths/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/bit-manip)

Return `max(len(a) * len(b))` over pairs whose character sets are disjoint (no shared letter).

**Example 1** — `words=["abcw","baz","foo","bar","xtfn","abcdef"]` → `16` (`"abcw"` × `"xtfn"`)
**Example 2** — `words=["a","aa","aaa","aaaa"]` → `0`

**Constraints** — `2 ≤ n ≤ 1000`; lowercase.

---

## Approach 1 — Set intersection per pair

For each pair build a `Set<Character>`; check intersection. O(n² · L).

## Approach 2 — Bitmask signatures (canonical)

**Insight.** Each word uses ≤ 26 letters → 26-bit signature. Two words share no letters iff `mask[i] & mask[j] == 0`. Pair comparison becomes a single AND.

```java
int maxProduct(String[] words) {
    int n = words.length;
    int[] mask = new int[n];
    for (int i = 0; i < n; i++)
        for (char c : words[i].toCharArray()) mask[i] |= 1 << (c - 'a');
    int best = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if ((mask[i] & mask[j]) == 0)
                best = Math.max(best, words[i].length() * words[j].length());
    return best;
}
```

**Complexity** — Time **O(n·L + n²)**; Space **O(n)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Per-pair set intersect | O(n²·L) | O(σ) | baseline |
| Bitmask + AND | **O(n·L + n²)** | O(n) | canonical |

## When to use which

- **Small fixed alphabet (≤ 64)** → bitmask signatures.
- **Larger alphabet** → hashed signatures + fingerprint check.
- **"Return the pair"** → track indices.

## Related problems

- [Design Bit Set](https://leetcode.com/problems/design-bitset/)
- [Number of Ways to Wear Different Hats](/problems/number-of-ways-to-wear-different-hats-to-each-other) — bitmask DP
