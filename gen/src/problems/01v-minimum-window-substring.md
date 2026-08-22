# Sliding Window — Minimum Window Substring

*[↗ LeetCode: Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/sliding-window)

Given strings `s` and `t`, return the smallest substring of `s` that contains every character of `t` (with multiplicity). Return `""` if impossible.

**Example 1** — `s = "ADOBECODEBANC", t = "ABC"` → `"BANC"`
**Example 2** — `s = "a", t = "a"` → `"a"`
**Example 3** — `s = "a", t = "aa"` → `""` (not enough `a`s in `s`)

**Constraints** — `1 ≤ m, n ≤ 10⁵`. Uppercase + lowercase ASCII.

---

## Approach 1 — Enumerate every substring

**Intuition.** Try every `s[i..j]`; for each, check whether it contains all characters of `t`. Keep the shortest.

```java
String minWindowBrute(String s, String t) {
    int n = s.length(), bestL = -1, bestLen = Integer.MAX_VALUE;
    for (int i = 0; i < n; i++)
        for (int j = i; j < n; j++)
            if (contains(s, i, j, t) && j - i + 1 < bestLen) {
                bestLen = j - i + 1; bestL = i;
            }
    return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestL, bestL + bestLen);
}
boolean contains(String s, int l, int r, String t) {
    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;
    for (int i = l; i <= r; i++) if (need[s.charAt(i)] > 0) need[s.charAt(i)]--;
    for (int x : need) if (x > 0) return false;
    return true;
}
```

<CodeTrace
  title="Brute — s='ADOBEC', t='ABC' (first valid window)"
  :values="['A','D','O','B','E','C']"
  :windowKeys="['i','j']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0, j: 0 }, vars: { substr: "A", contains: "no" }, note: "missing B, C" },
    { pointers: { i: 0, j: 2 }, vars: { substr: "ADO", contains: "no" }, note: "missing B, C" },
    { pointers: { i: 0, j: 5 }, vars: { substr: "ADOBEC", contains: "yes", best: 6 }, note: "first valid; length 6" },
    { pointers: { i: 3, j: 5 }, vars: { substr: "BEC", contains: "no" }, note: "missing A — cant improve here" }
  ]'
/>

**Complexity** — Time **O(n² · (n + σ))**; Space **O(σ)**.

At `n = 10⁵` this is ~10¹⁵ ops. TLE.

---

## Approach 2 — Sliding window with need/have counter

**Insight from brute.** For a fixed `left`, the smallest valid `right` grows monotonically as `left` advances. So we never restart `right` — extend `right` until the window is valid, then shrink `left` while still valid, tracking the best.

Track `need[c]` (positive for chars we still need) and `have` = number of characters currently satisfied. Window is valid iff `have == t.length()`.

**Trap** — decrement `need[c]` for every char in `s` (may go negative for over-represented chars). Only increment `have` when the decrement crossed from `>0` to `≥0` — i.e., `need[c]-- > 0` **before** decrement.

```java
String minWindow(String s, String t) {
    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;
    int required = t.length(), have = 0;
    int bestL = 0, bestLen = Integer.MAX_VALUE, left = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        if (need[c]-- > 0) have++;
        while (have == required) {
            if (right - left + 1 < bestLen) { bestLen = right - left + 1; bestL = left; }
            char lc = s.charAt(left++);
            if (++need[lc] > 0) have--;
        }
    }
    return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestL, bestL + bestLen);
}
```

<CodeTrace
  title="Sliding window — s='ADOBECODEBANC', t='ABC'"
  :values="['A','D','O','B','E','C','O','D','E','B','A','N','C']"
  :windowKeys="['left','right']"
  :cellWidth="30"
  :steps='[
    { pointers: { left: 0, right: 5 }, vars: { have: 3, window: "ADOBEC", best: 6 }, note: "first valid window at r=5; try to shrink" },
    { pointers: { left: 3, right: 5 }, vars: { have: 3, window: "BEC", best: 3 }, note: "shrink left; window still valid — no, need A again" },
    { pointers: { left: 1, right: 10 }, vars: { have: 3, window: "DOBECODEBA", best: 6 }, note: "extend right; found second A at r=10" },
    { pointers: { left: 5, right: 12 }, vars: { have: 3, window: "CODEBANC", best: 4 }, note: "shrink; best window BANC of length 4" }
  ]'
/>

**Complexity** — Time **O(n + m)** — each char enters and leaves the window at most once; Space **O(σ)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Enumerate every substring | O(n² · (n+σ)) | O(σ) | baseline; TLE at n=10⁵ |
| Sliding window + need/have | **O(n + m)** | O(σ) | expected optimum |

## When to use which

- **First pass** — always state brute for signal, then jump to sliding window.
- **"Contains every char of t"** → need/have counter; skeleton reusable.
- **"What if t may repeat characters?"** → the need[] array handles it because you compare counts, not presence.
- **Follow-up: return all min windows** → track ties, or convert to two-pointer with restart.

## Related problems

- [Minimum Window Subsequence](/problems/minimum-window-subsequence) — order matters, DP or two-pointer forward/backward
- [Permutation in String](/problems/permutation-in-string) — fixed-size window variant
- [Substring with Concatenation of All Words](/problems/substring-with-concatenation-of-all-words) — window on word offsets
- [Find All Anagrams in a String](/problems/find-all-anagrams-in-a-string) — return all indices
