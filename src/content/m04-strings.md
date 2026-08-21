## Concepts & Mental Models

Strings are arrays with meaning attached. In interviews, convert once with `toCharArray()` when repeated indexing matters, then reason over indices, intervals, and character state. A substring is a contiguous slice; most bugs come from losing that boundary discipline.

Frequency/count vectors are the default compact state. For lowercase letters, `int[26]` is faster and clearer than a map; for ASCII, `int[128]` is still O(1). Window problems ask: **what count state makes this interval valid?**

For substrings, sliding windows maintain a validity predicate while `R` expands and `L` shrinks monotonically. For substring search, two engines dominate: **rolling hash** treats windows as fingerprints; **prefix-function automata** treat the pattern as reusable state after failure. Rabin-Karp filters candidates; KMP proves worst-case linear matching.

---

## Longest Substring Without Repeating Characters

!!! pattern "Pattern: Variable Sliding Window · T: O(n) · S: O(1)"
    **Signals:** longest contiguous substring, no repeats, update state by adding/removing one character.

### 1. The Problem

Return the length of the longest contiguous substring of `s` with no repeated characters.

### 2. The Intuition

Maintain a window that is always duplicate-free. Adding `s[R]` is the only operation that can break validity; moving `L` is the only operation that can repair it.

### 3. The Naive Approach

Start at every index, scan right with a set until a duplicate appears, and keep the maximum. This repeats comparisons across overlapping substrings and is O(n²).

### 4. The Key Observation 🔑

!!! key "Key observation"
    The window is valid iff every character count is at most 1. After adding `s[R]`, only `s[R]` can have count 2, so shrink `L` until `freq[s[R]] == 1`.

### 5. Pattern Recognition

**Signals.** "Longest substring" plus a local validity condition.  
**Shortcut.** Expand until invalid; shrink until valid; record only valid windows.  
**Related.** At most K distinct, fruit baskets, character replacement.

### 6. The Invariant

After each `R` iteration finishes, `freq[c]` is the exact count of `c` in `s[L..R]`, the window has no duplicates, and `best` is the largest valid length seen.

### 7. Visual Explanation

```diagram
{"type":"array","title":"Expand creates a duplicate","values":["a","b","c","a","d","e"],"highlights":{"0":"red","3":"red"},"pointers":[{"name":"L","index":0,"color":"primary","side":"bottom"},{"name":"R","index":3,"color":"red","side":"top"}],"brackets":[{"from":0,"to":3,"label":"invalid window","color":"red","row":0}],"caption":"The second a violates uniqueness; the current window must shrink from the left."}
```

```diagram
{"type":"array","title":"Shrink restores validity","values":["a","b","c","a","d","e"],"highlights":{"1":"green","2":"green","3":"green"},"pointers":[{"name":"L","index":1,"color":"primary","side":"bottom"},{"name":"R","index":3,"color":"green","side":"top"}],"brackets":[{"from":1,"to":3,"label":"valid","color":"green","row":0}],"caption":"After the old a leaves, bca is valid and can update best."}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":460,"box":260,"title":"Uniqueness window","steps":[{"type":"start","text":"L=0, best=0"},{"type":"decision","text":"more R?","yes":"yes","branch":{"label":"no","text":"return best","role":"green"}},{"type":"process","text":"freq[s[R]]++"},{"type":"decision","text":"freq[s[R]] > 1?","yes":"yes","branch":{"label":"no","text":"best=max(best,R-L+1)","role":"primary"}},{"type":"process","text":"freq[s[L]]--; L++"}]}
```

### 9. Step-by-Step Walkthrough

For `abcade`: `abc` gives best 3; adding the second `a` forces removal of the old `a`; then `bcad` gives 4 and `bcade` gives 5.

| R | char | window after repair | best |
|---|---|---|---|
| 0 | a | `a` | 1 |
| 1 | b | `ab` | 2 |
| 2 | c | `abc` | 3 |
| 3 | a | `bca` | 3 |
| 5 | e | `bcade` | 5 |

### 10. Why It Works

For each right endpoint, the shrink loop finds the leftmost boundary that makes the window valid. Any earlier boundary is invalid; any later boundary is shorter. Taking the maximum over all right endpoints is therefore optimal.

### 11. Java Implementation

```java
int lengthOfLongestSubstring(String s) {
    int[] freq = new int[128];
    char[] a = s.toCharArray();
    int left = 0, best = 0;

    for (int right = 0; right < a.length; right++) {
        freq[a[right]]++;
        while (freq[a[right]] > 1) {
            freq[a[left]]--;
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

### 12. Code Walkthrough

The count array is the window state. The `while` loop checks only `a[right]` because no other character count changed upward.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n) — each pointer advances at most `n` times. **S:** O(1) for ASCII counts.

### 14. Edge Cases

Empty string returns 0; all identical characters return 1; all unique characters return `s.length()`. For full Unicode, iterate code points rather than Java `char` units.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Updating `best` before restoring validity, shrinking with `if` instead of `while`, or allocating substrings inside the loop.

### 16. Optimization

A `lastSeen[128]` array can jump `L` directly to `lastSeen[c] + 1`; the count version is usually easier to generalize.

### 17. Alternatives

A `HashSet<Character>` window is correct but heavier. Brute force is O(n²). Sorting is invalid because contiguity matters.

### 18. Interview Follow-Ups

Return the substring by tracking `bestStart`; support at most `k` distinct characters by tracking a `distinct` count; support Unicode with a map over code points.

### 19. Variations

Longest substring with at most two distinct characters, longest repeating character replacement, and minimum-size windows with coverage predicates.

### 20. Pattern Connection

This is the purest variable-window template: define validity, expand right, repair with left, and rely on monotonic pointers for linear time.

---

## Minimum Window Substring

!!! pattern "Pattern: Variable Window + Need/Have Counts · T: O(n + m) · S: O(1)"
    **Signals:** smallest substring covering another string, duplicates matter, valid window can be shrunk.

### 1. The Problem

Given `s` and `t`, return the shortest substring of `s` containing all characters of `t` with multiplicity, or `""` if none exists.

### 2. The Intuition

Expand until the window covers the target multiset; then shrink greedily while coverage remains. Every valid window before a shrink is a candidate.

### 3. The Naive Approach

Check all O(n²) substrings against the target counts. Even fast count checks still leave too many candidate intervals.

### 4. The Key Observation 🔑

!!! key "Key observation"
    Let `required` be the number of distinct required characters and `formed` be how many have `window[c] >= need[c]`. The window is valid exactly when `formed == required`; surplus characters are irrelevant except that they allow shrinking.

### 5. Pattern Recognition

**Signals.** "Minimum substring containing..." and target multiplicities.  
**Shortcut.** Expand to become valid; shrink while valid; record before removing.  
**Related.** Find all anagrams, permutation in string, smallest positive-sum subarray.

### 6. The Invariant

`need[c]` is fixed from `t`; `window[c]` is exact for `s[L..R]`; `formed` counts exactly the needed characters whose required multiplicity is currently satisfied.

### 7. Visual Explanation

```diagram
{"type":"array","title":"First valid covering window","values":["A","D","O","B","E","C","B","A","N","C"],"highlights":{"0":"green","3":"green","5":"green"},"pointers":[{"name":"L","index":0,"color":"primary","side":"bottom"},{"name":"R","index":5,"color":"green","side":"top"}],"brackets":[{"from":0,"to":5,"label":"valid","color":"green","row":0}],"caption":"ADOBEC covers A, B, and C, so the shrink phase starts."}
```

```diagram
{"type":"array","title":"Later shrink finds the answer","values":["A","D","O","B","E","C","B","A","N","C"],"highlights":{"6":"green","7":"green","9":"green"},"pointers":[{"name":"L","index":6,"color":"primary","side":"bottom"},{"name":"R","index":9,"color":"green","side":"top"}],"brackets":[{"from":6,"to":9,"label":"BANC","color":"green","row":0}],"caption":"After later expansion, BANC is valid and shorter."}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":500,"box":285,"title":"Covering window","steps":[{"type":"start","text":"build need; L=0; formed=0"},{"type":"decision","text":"more R?","yes":"yes","branch":{"label":"no","text":"return best or empty","role":"green"}},{"type":"process","text":"add s[R]; update formed"},{"type":"decision","text":"formed == required?","yes":"yes","branch":{"label":"no","text":"expand R","role":"primary"}},{"type":"process","text":"record; remove s[L]; L++"}]}
```

### 9. Step-by-Step Walkthrough

For `ADOBECODEBANC`, `ABC`: `ADOBEC` first satisfies all counts; removing `A` breaks validity. Later, after reaching the final `C`, repeated shrinking produces `BANC`.

| event | window | action |
|---|---|---|
| reach C at 5 | `ADOBEC` | record length 6 |
| remove A | `DOBEC` | invalid |
| reach A at 10 | `DOBECODEBA` | valid again |
| reach C at 12 | `BANC` | record length 4 |

### 10. Why It Works

For a fixed `R`, the shrink loop considers every valid left boundary until the next removal would violate coverage. Thus it finds the minimum valid window ending at `R`; scanning all `R` finds the global minimum.

### 11. Java Implementation

```java
String minWindow(String s, String t) {
    if (t.length() > s.length()) return "";

    int[] need = new int[128];
    int required = 0;
    for (char c : t.toCharArray()) {
        if (need[c] == 0) required++;
        need[c]++;
    }

    int[] window = new int[128];
    char[] a = s.toCharArray();
    int left = 0, formed = 0;
    int bestStart = 0, bestLen = Integer.MAX_VALUE;

    for (int right = 0; right < a.length; right++) {
        char in = a[right];
        window[in]++;
        if (need[in] > 0 && window[in] == need[in]) formed++;

        while (formed == required) {
            int len = right - left + 1;
            if (len < bestLen) {
                bestLen = len;
                bestStart = left;
            }
            char out = a[left++];
            window[out]--;
            if (need[out] > 0 && window[out] < need[out]) formed--;
        }
    }
    return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestStart, bestStart + bestLen);
}
```

### 12. Code Walkthrough

`formed` changes only when a count crosses the exact threshold: equality on entry, below-threshold on exit. Recording happens before removal because the current window is valid.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n + m), where `n = s.length()` and `m = t.length()`. **S:** O(1) for ASCII count arrays.

### 14. Edge Cases

`t` longer than `s`, duplicate target characters, no possible window, and case sensitivity. `t = "AABC"` requires two `A`s.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Counting total matched characters incorrectly, decrementing `formed` when removing surplus, or using `required = t.length()` instead of distinct required characters.

### 16. Optimization

If `t` is tiny and `s` is huge, pre-filter `s` to only indices whose characters appear in `t`, then run the same window over that compressed list.

### 17. Alternatives

Binary search on length with coverage checks is O(n log n). Prefix counts still require searching many intervals. The monotonic window is optimal.

### 18. Interview Follow-Ups

Return all minimum windows, stream the text, or support a larger alphabet with `Map<Character,Integer>` or code-point maps.

### 19. Variations

Permutation in String, Find All Anagrams, Minimum Window Subsequence. The last is different because order matters.

### 20. Pattern Connection

This is the canonical covering-window problem: unlike longest-unique, shrink while valid, not while invalid.

---

## Group Anagrams

!!! pattern "Pattern: Canonical Frequency Key · T: O(n · k) · S: O(n · k)"
    **Signals:** group strings by same multiset of letters; word order does not matter.

### 1. Problem

Group all strings that are anagrams of each other. Output order is usually irrelevant.

### 2. Key Observation

!!! key "Key observation"
    Anagrams have identical frequency vectors. A delimited encoding of `int[26]` is a collision-free canonical key for lowercase English words.

### 3. Invariant

After processing a prefix of the input, each map bucket contains exactly the words from that prefix whose count vector equals the bucket key.

### 4. Diagram

```diagram
{"type":"array","title":"Canonical keys group equivalent words","values":["eat","tea","tan","ate","nat","bat"],"highlights":{"0":"green","1":"green","3":"green","2":"amber","4":"amber","5":"purple"},"caption":"eat, tea, and ate share one count-vector key; tan and nat share another."}
```

### 5. Java

```java
List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String word : strs) {
        int[] count = new int[26];
        for (char c : word.toCharArray()) count[c - 'a']++;

        StringBuilder key = new StringBuilder();
        for (int x : count) key.append('#').append(x);
        groups.computeIfAbsent(key.toString(), k -> new ArrayList<>()).add(word);
    }
    return new ArrayList<>(groups.values());
}
```

### 6. Complexity

!!! complexity "Complexity"
    **T:** O(n · k) for `n` words of average length `k`; key creation is O(26). **S:** O(n · k) for output plus keys.

### 7. Pattern Connection

This is canonicalization: map every object in an equivalence class to the same stable key. Sorting each word also works but costs O(k log k).

### 8. Common Pitfall

Do not use `int[]` directly as a map key; Java arrays compare by identity. Use delimiters in the encoded key to avoid ambiguity.

---

## Longest Palindromic Substring (expand-around-center)

!!! pattern "Pattern: Center Expansion · T: O(n²) · S: O(1)"
    **Signals:** longest contiguous palindrome, symmetry around one character or a gap.

### 1. The Problem

Return the longest palindromic substring of `s`. If several answers tie, any one is acceptable unless specified otherwise.

### 2. The Intuition

Every palindrome has a center. Try every odd center `(i,i)` and even center `(i,i+1)`, expanding outward while boundary characters match.

### 3. The Naive Approach

Enumerate all substrings and test each for palindrome: O(n³). DP reduces time to O(n²) but spends O(n²) space.

### 4. The Key Observation 🔑

!!! key "Key observation"
    If `s[L+1..R-1]` is a palindrome and `s[L] == s[R]`, then `s[L..R]` is also a palindrome. Expansion grows a known-valid center until that condition fails.

### 5. Pattern Recognition

**Signals.** Symmetry, contiguous substring, longest palindrome.  
**Shortcut.** Enumerate minimal seeds: one character for odd length and one gap for even length.  
**Related.** Count palindromic substrings, Manacher's algorithm, longest palindromic subsequence.

### 6. The Invariant

During expansion, `s[L+1..R-1]` is palindromic. If both boundaries are in range and equal, expanding preserves the invariant. When the loop stops, the previous interval is maximal for that center.

### 7. Visual Explanation

```diagram
{"type":"array","title":"Odd center expansion","values":["b","a","b","a","d"],"highlights":{"1":"green","2":"purple","3":"green"},"pointers":[{"name":"L","index":1,"color":"primary","side":"bottom"},{"name":"R","index":3,"color":"primary","side":"bottom"}],"brackets":[{"from":1,"to":3,"label":"aba","color":"green","row":0}],"caption":"A center at b expands to aba because the boundary a characters match."}
```

```diagram
{"type":"array","title":"Even center expansion","values":["c","b","b","d","x"],"highlights":{"1":"green","2":"green"},"pointers":[{"name":"L","index":1,"color":"primary","side":"bottom"},{"name":"R","index":2,"color":"primary","side":"bottom"}],"brackets":[{"from":1,"to":2,"label":"bb","color":"green","row":0}],"caption":"Even-length palindromes start between adjacent characters."}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":470,"box":275,"title":"Try all centers","steps":[{"type":"start","text":"bestStart=0; bestLen=1"},{"type":"decision","text":"more centers?","yes":"yes","branch":{"label":"no","text":"return best substring","role":"green"}},{"type":"process","text":"expand(i,i) and expand(i,i+1)"},{"type":"decision","text":"longer found?","yes":"yes","branch":{"label":"no","text":"advance center","role":"primary"}},{"type":"process","text":"update bestStart,bestLen"}]}
```

### 9. Step-by-Step Walkthrough

For `babad`, center 1 yields `bab`; center 2 yields `aba`; both length 3 are valid answers.

| center | maximal palindrome | best |
|---|---|---|
| 0 odd | `b` | `b` |
| 1 odd | `bab` | `bab` |
| 2 odd | `aba` | `bab` or `aba` |
| even centers | none longer | unchanged |

### 10. Why It Works

Every palindrome has exactly one odd or even center. Since the algorithm computes the maximal palindrome for each center and returns the longest among them, it cannot miss the optimum.

### 11. Java Implementation

```java
String longestPalindrome(String s) {
    if (s.isEmpty()) return "";

    char[] a = s.toCharArray();
    int bestStart = 0, bestLen = 1;
    for (int i = 0; i < a.length; i++) {
        int odd = expand(a, i, i);
        if (odd > bestLen) {
            bestLen = odd;
            bestStart = i - odd / 2;
        }

        int even = expand(a, i, i + 1);
        if (even > bestLen) {
            bestLen = even;
            bestStart = i - even / 2 + 1;
        }
    }
    return s.substring(bestStart, bestStart + bestLen);
}

private int expand(char[] a, int left, int right) {
    while (left >= 0 && right < a.length && a[left] == a[right]) {
        left--;
        right++;
    }
    return right - left - 1;
}
```

### 12. Code Walkthrough

`expand` stops one step beyond the valid palindrome, so its length is `right - left - 1`. The start formulas convert center plus length back to Java substring indices.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n²) in the worst case, such as all equal characters. **S:** O(1) excluding the returned substring.

### 14. Edge Cases

Empty string, single character, even-length answer like `bb`, and ties such as `bab` versus `aba`.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Checking only odd centers, using an inclusive end in `substring`, or returning `right - left + 1` after the loop despite overshooting.

### 16. Optimization

You can skip centers that cannot beat `bestLen`, but Manacher's algorithm is the real O(n) upgrade.

### 17. Alternatives

DP over intervals gives O(n²)/O(n²). Manacher's algorithm stores palindrome radii after inserting separators and achieves O(n).

### 18. Interview Follow-Ups

Count all palindromic substrings by counting each successful expansion; longest palindromic subsequence is a different DP problem.

### 19. Variations

Count palindromic substrings, shortest palindrome, longest palindrome constructible from counts.

### 20. Pattern Connection

Center expansion is a two-pointer symmetry pattern: the pointers move outward from a seed rather than sliding forward as a window.

---

## KMP / Knuth-Morris-Pratt (prefix function)

!!! pattern "Pattern: Prefix Function Automaton · T: O(n + m) · S: O(m)"
    **Signals:** exact substring search, repeated prefixes, worst-case linear guarantee.

### 1. The Problem

Return the first index where `needle` occurs in `haystack`, or `-1` if absent. KMP does this without backing up in the text.

### 2. The Intuition

After matching `j` pattern characters, a mismatch does not erase all progress. A suffix of the matched prefix may also be a pattern prefix; resume from the longest such reusable prefix.

### 3. The Naive Approach

Try every starting index and compare the pattern. Repetitive inputs like `aaaaaaaab` with pattern `aaaab` cause O(nm) repeated comparisons.

### 4. The Key Observation 🔑

!!! key "Key observation"
    `lps[i]` is the longest proper prefix of `pattern[0..i]` that is also its suffix. On mismatch at pattern index `j`, the only longest viable fallback is `lps[j-1]`; longer fallbacks are impossible by definition.

### 5. Pattern Recognition

**Signals.** Exact matching, no probabilistic collisions, repeated pattern structure.  
**Shortcut.** Precompute where pattern state should go after failure.  
**Related.** Repeated substring pattern, longest happy prefix, Aho-Corasick.

### 6. The Invariant

During search, before comparing `text[i]` and `pat[j]`, `j` is the length of the longest pattern prefix matching a suffix of `text[0..i-1]`. During LPS construction, `len` is the longest border length for the prefix ending before `i`.

### 7. Visual Explanation

```diagram
{"type":"array","title":"Prefix function values under pattern chars","values":["a/0","b/0","a/1","b/2","a/3","c/0"],"highlights":{"0":"green","1":"green","2":"green","3":"green","4":"green","5":"red"},"pointers":[{"name":"i","index":5,"color":"red","side":"top"},{"name":"len","index":3,"color":"primary","side":"bottom"}],"brackets":[{"from":0,"to":3,"label":"candidate border","color":"primary","row":0}],"caption":"Each cell is char/lps. For ababac, c forces fallback through shorter borders to 0."}
```

```diagram
{"type":"array","title":"Fallback reuses text already read","values":["a","b","a","b","a","b","a","c"],"highlights":{"2":"green","3":"green","4":"green","5":"green"},"pointers":[{"name":"i","index":5,"color":"red","side":"top"},{"name":"j","index":5,"color":"red","side":"bottom"}],"brackets":[{"from":2,"to":5,"label":"suffix reused","color":"green","row":0}],"caption":"A mismatch changes j via lps; i never moves backward."}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":520,"box":300,"title":"KMP search","steps":[{"type":"start","text":"build lps; i=0; j=0"},{"type":"decision","text":"i < text.length?","yes":"yes","branch":{"label":"no","text":"return -1","role":"red"}},{"type":"decision","text":"text[i] == pat[j]?","yes":"yes","branch":{"label":"no","text":"if j>0: j=lps[j-1]\\nelse: i++","role":"primary"}},{"type":"process","text":"i++; j++"},{"type":"decision","text":"j == pat.length?","yes":"yes","branch":{"label":"no","text":"continue","role":"primary"}}]}
```

### 9. Step-by-Step Walkthrough

For pattern `ababac`, `lps = [0,0,1,2,3,0]`. After matching `ababa`, a mismatch against `c` falls back from `j=5` to `j=3`, preserving the suffix `aba`.

| event | `j` | action |
|---|---|---|
| match `ababa` | 5 | next expects `c` |
| mismatch | 5 → 3 | use `lps[4]` |
| match continues | 3 → 6 | full occurrence found |

### 10. Why It Works

The invariant says `j` represents the longest viable partial match ending before `i`. On mismatch, any valid continuation must be a border of the matched prefix, so `lps[j-1]` preserves all possible matches and discards impossible ones. Each match advances `i`; each fallback decreases `j`, giving O(n + m).

### 11. Java Implementation

```java
int strStr(String haystack, String needle) {
    if (needle.isEmpty()) return 0;

    char[] text = haystack.toCharArray();
    char[] pat = needle.toCharArray();
    int[] lps = buildLps(pat);
    int i = 0, j = 0;

    while (i < text.length) {
        if (text[i] == pat[j]) {
            i++;
            j++;
            if (j == pat.length) return i - j;
        } else if (j > 0) {
            j = lps[j - 1];
        } else {
            i++;
        }
    }
    return -1;
}

private int[] buildLps(char[] pat) {
    int[] lps = new int[pat.length];
    int len = 0;
    for (int i = 1; i < pat.length; ) {
        if (pat[i] == pat[len]) {
            lps[i++] = ++len;
        } else if (len > 0) {
            len = lps[len - 1];
        } else {
            lps[i++] = 0;
        }
    }
    return lps;
}
```

### 12. Code Walkthrough

LPS construction runs KMP-like matching on the pattern itself. In search, a mismatch with `j > 0` changes only pattern state; the text index is not consumed because that character may match the fallback state.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n + m): building `lps` is O(m), scanning text is O(n), and fallbacks cannot exceed prior increments. **S:** O(m) for `lps`.

### 14. Edge Cases

Empty pattern returns 0; pattern longer than text returns -1; highly repetitive patterns are handled in linear time.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Resetting `j` to 0 on every mismatch, advancing `i` after a nonzero fallback, or computing a prefix value that includes the whole prefix instead of a proper border.

### 16. Optimization

Reuse `lps` when searching many texts for the same pattern. A full DFA table can reduce branches at the cost of O(m·alphabet) space.

### 17. Alternatives

Rabin-Karp uses hashes and needs collision handling. Boyer-Moore often skips faster in practice but has more preprocessing and trickier worst-case behavior.

### 18. Interview Follow-Ups

Find all occurrences by recording matches and setting `j = lps[j - 1]`; detect string periods from `lps[m-1]`; extend to multiple patterns with Aho-Corasick.

### 19. Variations

Longest happy prefix, repeated substring pattern, shortest palindrome via `s + '#' + reverse(s)`.

### 20. Pattern Connection

KMP is the automaton side of string matching: it converts failure into state transition, just as DP converts repeated work into reusable state.

---

## Rabin-Karp (rolling hash)

!!! pattern "Pattern: Rolling Hash · Expected T: O(n + m) · S: O(1)"
    **Signals:** fixed-length substring windows, candidate filtering, multiple searches or duplicate-substring variants.

### 1. Problem

Find all starting indices where `pattern` occurs in `text` by comparing rolling hashes and verifying candidate matches.

### 2. Key Observation

!!! key "Key observation"
    A polynomial hash supports O(1) rolling: remove the outgoing leading character, multiply by the base, and add the incoming character. Equal hashes are candidates, not proof, unless verified or double-hashed with accepted risk.

### 3. Invariant

Before checking start `i`, `winHash` equals the hash of `text[i..i+m-1]` under the same base/modulus as `patHash`.

### 4. Diagram

```diagram
{"type":"array","title":"Roll the fixed-size hash window","values":["a","b","c","d","a","b","c"],"highlights":{"1":"green","2":"green","3":"green","4":"amber"},"pointers":[{"name":"out","index":0,"color":"red","side":"bottom"},{"name":"in","index":4,"color":"amber","side":"top"}],"brackets":[{"from":1,"to":3,"label":"next","color":"green","row":0}],"caption":"Drop a, shift bcd, and add a to obtain the next window hash."}
```

### 5. Java

```java
List<Integer> rabinKarp(String text, String pattern) {
    List<Integer> ans = new ArrayList<>();
    int n = text.length(), m = pattern.length();
    if (m == 0 || m > n) return ans;

    long mod = 1_000_000_007L, base = 257L, highPow = 1L;
    for (int i = 1; i < m; i++) highPow = (highPow * base) % mod;

    char[] t = text.toCharArray();
    char[] p = pattern.toCharArray();
    long patHash = 0, winHash = 0;
    for (int i = 0; i < m; i++) {
        patHash = (patHash * base + p[i]) % mod;
        winHash = (winHash * base + t[i]) % mod;
    }

    for (int i = 0; i <= n - m; i++) {
        if (patHash == winHash && matches(t, p, i)) ans.add(i);
        if (i < n - m) {
            winHash = (winHash - t[i] * highPow % mod + mod) % mod;
            winHash = (winHash * base + t[i + m]) % mod;
        }
    }
    return ans;
}

private boolean matches(char[] text, char[] pattern, int start) {
    for (int j = 0; j < pattern.length; j++) {
        if (text[start + j] != pattern[j]) return false;
    }
    return true;
}
```

### 6. Complexity

!!! complexity "Complexity"
    **Expected T:** O(n + m) with few collisions. **Worst-case T:** O(nm) if many hash matches require verification. **S:** O(1) excluding the result list.

### 7. Pattern Connection

Rabin-Karp is the hashing counterpart to KMP. It does not prove failure transitions; it cheaply filters candidate windows and verifies only likely matches.

### 8. Common Pitfall

Normalize subtraction with `+ mod` before `% mod`, use `long` for products, and verify substring equality on hash match to eliminate collision errors.
