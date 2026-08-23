# Sliding Window — Substring with Concatenation of All Words

*[↗ LeetCode: Substring with Concatenation of All Words](https://leetcode.com/problems/substring-with-concatenation-of-all-words/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/sliding-window)

Find starting indices of substrings that are concatenations of every word in `words` (each used exactly once, any order). All words same length `L`.

**Example 1** — `s="barfoothefoobarman", words=["foo","bar"]` → `[0, 9]`
**Example 2** — `s="wordgoodgoodgoodbestword", words=["word","good","best","word"]` → `[]`

**Constraints** — `1 ≤ |s| ≤ 10⁴`; each word ≤ 30 chars.


&lt;Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/&gt;
---

## Approach 1 — Try every start

O(n · k · L). Baseline.

## Approach 2 — Sliding window on word-aligned offsets (canonical)

**Insight.** Iterate `offset ∈ [0, L)`. Walk `s` in chunks of L. Maintain `have` count; on unknown word, reset window; on over-count, shrink from left.



```java
List<Integer> findSubstring(String s, String[] words) {
    List<Integer> out = new ArrayList<>();
    int L = words[0].length(), k = words.length;
    int total = L * k;
    if (s.length() < total) return out;
    Map<String, Integer> need = new HashMap<>();
    for (String w : words) need.merge(w, 1, Integer::sum);
    for (int off = 0; off < L; off++) {
        int l = off, have = 0;
        Map<String, Integer> win = new HashMap<>();
        for (int r = off; r + L <= s.length(); r += L) {
            String w = s.substring(r, r + L);
            if (!need.containsKey(w)) { win.clear(); have = 0; l = r + L; continue; }
            win.merge(w, 1, Integer::sum);
            have++;
            while (win.get(w) > need.get(w)) {
                String lw = s.substring(l, l + L);
                win.merge(lw, -1, Integer::sum);
                have--;
                l += L;
            }
            if (have == k) out.add(l);
        }
    }
    return out;
}
```



<CodeTrace
  title="Try every start"
  :values="['foo', 'bar']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n · L)**; Space **O(k · L)**.

---

## Try it yourself

<JavaRunner problem-slug="substring-with-concatenation-of-all-words" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Every start | O(n · k · L) | O(k) | baseline |
| Aligned sliding | **O(n · L)** | O(k · L) | canonical |

## When to use which

- **Fixed-length words concat** → offset-aligned sliding.
- **Variable-length words** → totally different — DP on word breaks.
- **Return only count** → same skeleton, count instead of appending.

&lt;AiCompanion problem-slug="substring-with-concatenation-of-all-words" pattern-hint="sliding window" /&gt;

## Related problems

- [Minimum Window Substring](/problems/minimum-window-substring)
- [Find All Anagrams in a String](/problems/find-all-anagrams-in-a-string)
- [Permutation in String](/problems/permutation-in-string)
