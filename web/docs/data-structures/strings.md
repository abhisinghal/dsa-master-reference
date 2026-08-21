# Strings

A string is just an array of characters, so almost everything from the Arrays chapter carries straight over. There are only a handful of genuinely *string-specific* tricks worth knowing: **expand-around-center** (grow outward from the middle of a palindrome), **rolling hash** (Rabin–Karp — treat a window of characters as a number you can update in O(1) as it slides), and the **KMP failure function** (after a mismatch, skip ahead instead of re-reading the text). Two practical Java notes: reach for a `char[]` or a `StringBuilder`, because Java `String`s are immutable — gluing one together with `+` inside a loop is secretly O(n²).

<Callout kind="key" title="Key Insight">

Fixed alphabet ⇒ an `int[26]`/`int[128]` frequency vector *is* your hash: O(1) comparison and update. Reach for it before `HashMap<Character,Integer>`.

</Callout>

## Longest Palindromic Substring (Expand Around Center)

*[↗ LeetCode: Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/)*

### Problem

Return the **longest contiguous substring** of `s` that reads the same forwards and backwards (a palindrome).

**Constraints:** `1 ≤ n ≤ 1000`; any characters; any one longest answer is accepted.

**Example:** `"babad"` → `"bab"` (or `"aba"`); `"cbbd"` → `"bb"`.

**Example 1:** "babad" -&gt; "bab" or "aba".

**Example 2:** "cbbd" -&gt; "bb".

### Solution — brute force

Ignore the structural shortcut and scan/recompute from scratch for each decision.



```text
for each query or candidate:
  scan the relevant array/list/tree/graph state
  recompute the answer directly
```



Brute-force complexity: usually O(n) per operation or O(n^2)+ overall, with extra space when a copied structure is used.

### Solution — optimized

**Pattern:**
Every palindrome has a center (a char, or a gap between two). Expand outward from each of the `2n−1` centers.

<Callout kind="inv" title="Invariant">

While `s[l]==s[r]`, `s[l..r]` is a palindrome; expansion preserves the palindrome property symmetrically.

</Callout>

**Java:**


```java
String longestPalindrome(String s) {
    if (s == null || s.length() < 2) return s;
    int start = 0, len = 1;
    for (int i = 0; i < s.length(); i++) {
        int a = expand(s, i, i);       // odd length
        int b = expand(s, i, i + 1);   // even length
        int m = Math.max(a, b);
        if (m > len) { len = m; start = i - (m - 1) / 2; }
    }
    return s.substring(start, start + len);
}
int expand(String s, int l, int r) {
    while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; }
    return r - l - 1;   // length of palindrome
}
```



<Callout kind="note" title="Trace it">

`"cbbd"`. The even center between indices 1–2 (`b|b`) expands to `"bb"`; no other center beats length 2 → answer `"bb"`.

</Callout>

### Time Complexity

O(n^2): 2n-1 centers, each can expand O(n).

Original summary: Time O(n²) · Space O(1). (Manacher's algorithm gives O(n) but is rarely required.)

### Space Complexity

O(1) auxiliary space.

<Callout kind="trap" title="Common Trap">

Only expanding **odd**-length centers. *Example:* `"abba"` has an even-length palindrome centered between indices 1 and 2. Skip the even-center expansion and you miss `"abba"` entirely. Expand twice per index — `(i,i)` and `(i,i+1)`.

</Callout>

<Callout kind="pat" title="Pattern Connection">

Expansion also counts palindromic substrings (*Palindromic Substrings*). The DP alternative (`dp[i][j]`) is the bridge to interval DP.

</Callout>

### Learning notes

- Why two centers per index? Palindromes can be odd or even length.
- Why expand while equal? Symmetry is the palindrome invariant.
- Why start = i - (m-1)/2? It handles odd and even centers uniformly.
- Why not DP by default? Same O(n^2) time but O(n^2) space.
- Why not Manacher? O(n) but rarely expected.

#### Same pattern, new tweaks

"Grow outward from a center while it stays a palindrome" bends a few ways:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) | count every successful expansion instead of keeping only the longest | — |
| [Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) | not contiguous → DP; it's the LCS of `s` and `reverse(s)` | — |
| [Shortest Palindrome](https://leetcode.com/problems/shortest-palindrome/) | use the KMP failure function on `s + '#' + reverse(s)` to find the longest palindromic prefix | — |

## String Matching: Rabin–Karp &amp; KMP (concept)

### Problem

Given a text and a pattern, find occurrences of the pattern without rechecking characters that earlier comparisons already ruled out.

**Example 1:** text="ababc", pattern="abc" -&gt; match at index 2.

**Example 2:** text="aaaaa", pattern="aaa" -&gt; overlapping matches at 0, 1, 2.

### Solution — brute force

Try every alignment of the pattern and compare from the first character each time.



```text
for i in 0..n-m:
  j = 0
  while j < m and text[i+j] == pat[j]: j++
  if j == m: report i
```



Brute-force complexity: O(nm) time and O(1) space.

### Solution — optimized

<p class="secgoal"><b>What & why:</b> the two classic substring-search algorithms and when to name them. Goal — sketch rolling-hash and the KMP failure function well enough to signal depth, and know which one powers <i>Repeated Substring Pattern</i> / <i>Shortest Palindrome</i>.</p>

You rarely implement these fully in interviews, but naming and sketching them signals depth.

**Rabin–Karp** — rolling polynomial hash of each length-m window; compare hashes in O(1), verify on match. Average O(n+m); worst O(nm) under hash collisions. Great for *multiple* pattern search and duplicate-substring detection (*Longest Duplicate Substring* = binary search on length + rolling hash).

**KMP** — precompute the longest proper prefix-that-is-also-suffix (`lps`) of the pattern; on mismatch, jump the pattern pointer to `lps[j-1]` instead of restarting. Deterministic O(n+m).

<Callout kind="key" title="Key Insight">

KMP's `lps[i]` answers "after matching `pattern[0..i]`, what is the longest prefix I can fall back to without rereading text?" This failure-function idea also solves *Shortest Palindrome* and *Repeated Substring Pattern*.

</Callout>

**Java (KMP failure function):**


```java
int[] buildLps(String p) {
    int[] lps = new int[p.length()];
    int len = 0;
    for (int i = 1; i < p.length(); ) {
        if (p.charAt(i) == p.charAt(len)) lps[i++] = ++len;
        else if (len > 0) len = lps[len - 1];    // fall back
        else lps[i++] = 0;
    }
    return lps;
}
```



<Callout kind="note" title="Trace it">

pattern `"ABAB"` has `lps = [0,0,1,2]`: after matching `"ABAB"` then hitting a mismatch, you fall back to `lps[3]=2` (the prefix `"AB"` already re-matched), so the text pointer never rewinds.

</Callout>

<Callout kind="pat" title="Pattern Connection">

Rolling hash is the string face of prefix-sum thinking (a window aggregate updated in O(1)); the failure function is a precomputed-DP over the pattern.

</Callout>

### Time Complexity

KMP is O(n + m). Rabin-Karp is average O(n + m), worst O(nm) under collisions.

### Space Complexity

O(m) for KMP lps; O(1) or O(number of hashes) for rolling-hash variants.

### Learning notes

- Why lps? It records the fallback prefix after mismatch.
- Why text pointer never rewinds? KMP reuses matched prefix information.
- Why Rabin-Karp can be worst O(nm)? Collisions force verification.
- Why rolling hash? Window hashes update in O(1).
- Why separator in palindrome tricks? It prevents cross-boundary matches.

## Encode and Decode Strings (Length Prefixing)

*[↗ LeetCode: Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/)*

### Problem

Design `encode(List<String>)` → one string and `decode(String)` → the original list, so that **any** strings round-trip correctly — even ones that contain your delimiter.

**Constraints:** strings may contain any characters (digits, separators, empty strings); the encoding must be unambiguous.

**Example:** `["abc","d#e",""]` → `"3#abc3#d#e0#"` → decodes back to `["abc","d#e",""]`.

**Example 1:** ["abc","d#e",""] -&gt; "3#abc3#d#e0#" -&gt; original list.

**Example 2:** ["#","12"] -&gt; "1##2#12"; the # inside data is payload.

### Solution — brute force

Ignore the structural shortcut and scan/recompute from scratch for each decision.



```text
for each query or candidate:
  scan the relevant array/list/tree/graph state
  recompute the answer directly
```



Brute-force complexity: usually O(n) per operation or O(n^2)+ overall, with extra space when a copied structure is used.

### Solution — optimized

**Pattern:**
Serialize a list of arbitrary strings unambiguously with a length + delimiter header.

<Callout kind="key" title="Key Insight">

Delimiters fail when data can contain the delimiter. Prefix each string with its length: `"4#word3#abc"`. Decoding reads the count, then exactly that many chars — content-agnostic.

</Callout>

**Java:**


```java
String encode(List<String> strs) {
    StringBuilder sb = new StringBuilder();
    for (String s : strs) sb.append(s.length()).append('#').append(s);
    return sb.toString();
}
List<String> decode(String s) {
    List<String> res = new ArrayList<>();
    int i = 0;
    while (i < s.length()) {
        int j = s.indexOf('#', i);
        int len = Integer.parseInt(s.substring(i, j));
        res.add(s.substring(j + 1, j + 1 + len));
        i = j + 1 + len;
    }
    return res;
}
```




<Callout kind="inv" title="Invariant">

The decode cursor always sits at the start of a `length#payload` frame; reading the count fixes exactly how many following bytes belong to this string.

</Callout>

<Callout kind="trap" title="Common Trap">

Fixed delimiter with unescaped payload. *Example:* strings `["a#b","c"]` with delimiter `#` → encode `"a#b#c"`, decode as `["a","b","c"]` (wrong). Length-prefixing `"3#a#b1#c"` bypasses escaping — read the count, then exactly that many chars.

</Callout>

<Callout kind="pat" title="Pattern Connection">

Length-prefix framing is exactly how binary protocols and tree serialization avoid ambiguity — see *Serialize/Deserialize Binary Tree*.

</Callout>

### Time Complexity

O(total characters): every character is written and read once.

Original summary: Time O(total chars) · Space O(1) aux.

### Space Complexity

O(1) auxiliary space beyond output and builder.

### Learning notes

- Why length prefix? Payload may contain any delimiter.
- Why read only to # for the header? Payload length then decides the exact slice.
- Why StringBuilder? Repeated + in loops copies too much.
- Why advance to j+1+len? That lands on the next frame.
- Why support len=0? Empty strings must round-trip.

#### Same pattern, new tweaks

"Frame each piece unambiguously so it can be parsed back" recurs whenever you serialize:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Serialize/Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | pre-order with `#` null markers makes the traversal reversible | — |
| [Serialize N-ary Tree](https://leetcode.com/problems/serialize-and-deserialize-n-ary-tree/) | prefix each node with its child count so the parser knows when to stop | — |
| [Encode/Decode TinyURL](https://leetcode.com/problems/encode-and-decode-tinyurl/) | map long↔short with a counter or base-62 id instead of embedding the payload | — |
