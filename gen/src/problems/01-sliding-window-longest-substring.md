# Sliding Window — Longest Substring Without Repeating Characters

*[↗ LeetCode: Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Apple, Bloomberg" />

Given a string `s`, return the length of the longest substring with all distinct characters.

**Example 1** — `s = "abcabcbb"` → `3` (the substring `"abc"`)
**Example 2** — `s = "bbbbb"` → `1`
**Example 3** — `s = "pwwkew"` → `3` (the substring `"wke"`; note `"pwke"` is a *subsequence*, not a substring)

**Constraints** — `0 ≤ s.length ≤ 5·10⁴`; ASCII / extended ASCII characters.


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

<MarkSolved problem-slug="sliding-window-longest-substring" />

<InterviewTimer problem-slug="sliding-window-longest-substring" />



## Approach 1 — Brute force (all substrings, check distinct)

**Intuition.** Enumerate every substring `s[i..j]`; for each, verify all characters are distinct; track the max length.

```java
int lengthOfLongestSubstringBrute(String s) {
    int n = s.length(), best = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            if (allDistinct(s, i, j)) best = Math.max(best, j - i + 1);
        }
    }
    return best;
}
boolean allDistinct(String s, int i, int j) {
    Set<Character> seen = new HashSet<>();
    for (int k = i; k <= j; k++) if (!seen.add(s.charAt(k))) return false;
    return true;
}
```

<CodeTrace
  title="Brute force — s=&quot;abcabcbb&quot;, checking each substring"
  :values="['a','b','c','a','b','c','b','b']"
  :windowKeys="['i','j']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0, j: 0 }, vars: { substr: "a", distinct: true, best: 1 }, note: "check ‘a‘" },
    { pointers: { i: 0, j: 2 }, vars: { substr: "abc", distinct: true, best: 3 }, note: "check ‘abc‘ → best=3" },
    { pointers: { i: 0, j: 3 }, vars: { substr: "abca", distinct: false }, note: "duplicate a → invalid" },
    { pointers: { i: 1, j: 3 }, vars: { substr: "bca", distinct: true, best: 3 }, note: "still 3, no improvement" }
  ]'
/>

**Complexity** — Time **O(n³)** (O(n²) substrings × O(n) distinct check); Space **O(min(n, alphabet))** per check.

At n=5·10⁴ this is ~10¹⁴ ops. TLE.

---

## Approach 2 — Growing window with a set

**Insight from brute.** For a fixed left `i`, the maximal valid right `j` is monotonic in `i`. When we shrink `i`, the maximal `j` can only grow — never shrink. So we don't need to restart `j` from `i` each time.

Grow `right` while adding characters to a set. When a duplicate appears, shrink `left` (removing chars from the set) until the duplicate is gone.

```java
int lengthOfLongestSubstringSet(String s) {
    Set<Character> window = new HashSet<>();
    int left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        while (window.contains(c)) {
            window.remove(s.charAt(left));
            left++;
        }
        window.add(c);
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

<CodeTrace
  title="Set-based window — s=&quot;abcabcbb&quot;"
  :values="['a','b','c','a','b','c','b','b']"
  :windowKeys="['left','right']"
  :cellWidth="34"
  :steps='[
    { pointers: { left: 0, right: 0 }, vars: { window: "{a}", best: 1 }, note: "add a" },
    { pointers: { left: 0, right: 2 }, vars: { window: "{a,b,c}", best: 3 }, note: "add b, c → best=3" },
    { pointers: { left: 1, right: 3 }, vars: { window: "{b,c,a}", best: 3 }, note: "a duplicate → shrink left past first a" },
    { pointers: { left: 4, right: 5 }, vars: { window: "{b,c}", best: 3 }, note: "walk continues; no window beats 3" },
    { pointers: { left: 7, right: 7 }, vars: { window: "{b}", best: 3 }, note: "final bb → last window is 1" }
  ]'
/>

**Complexity** — Time **O(2n) = O(n)** (each char enters and leaves once); Space **O(min(n, alphabet))**.

Big win. But shrinking left one-at-a-time is wasteful — we walk past chars we already know are gone.

---

## Approach 3 — Last-seen index map (one pass)

**Insight from set window.** When the duplicate `s[right]` was last seen at position `prev`, we can jump `left` directly to `prev + 1` in O(1) instead of walking. Store the **last-seen index** of every character.

**Trap** — clamp `left` to its current value: `left = max(left, prev + 1)`. Otherwise `left` retreats on stale duplicates outside the current window.

```java
int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> last = new HashMap<>();
    int left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        if (last.containsKey(c)) {
            left = Math.max(left, last.get(c) + 1);
        }
        last.put(c, right);
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

<CodeTrace
  title="Last-seen jump — s=&quot;abba&quot; (shows the left-clamp trap)"
  :values="['a','b','b','a']"
  :windowKeys="['left','right']"
  :cellWidth="46"
  :steps='[
    { pointers: { left: 0, right: 0 }, vars: { last: "{a:0}", best: 1 }, note: "a → last[a]=0" },
    { pointers: { left: 0, right: 1 }, vars: { last: "{a:0,b:1}", best: 2 }, note: "b → last[b]=1" },
    { pointers: { left: 2, right: 2 }, vars: { last: "{a:0,b:2}", best: 2 }, note: "b duplicate → left=max(0, 1+1)=2. update last[b]=2" },
    { pointers: { left: 2, right: 3 }, vars: { last: "{a:3,b:2}", best: 2 }, note: "a duplicate stale (idx 0) → left=max(2, 0+1)=2. clamp works. best=2" }
  ]'
/>

**Complexity** — Time **O(n)** (single scan); Space **O(min(n, alphabet))** for the map.

Optimal. One pass, O(1) work per index.

---

## Try it yourself

<JavaRunner problem-slug="sliding-window-longest-substring" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Brute force | O(n³) | O(alphabet) | Baseline; TLE at n=5·10⁴ |
| Set-based window | O(n) | O(alphabet) | Correct, but shrinks step-by-step |
| Last-seen map | **O(n)** | O(alphabet) | Expected optimum |

## When to use which

- **First pass on a Sliding Window problem** → state brute for signal, then jump to last-seen.
- **Interviewer probes "why not shrink step-by-step?"** → it works, but wastes O(n) traversal on stale duplicates.
- **"Return the substring itself, not just length"** → track the best `(start, length)` pair.
- **"What if the alphabet is Unicode?"** → HashMap works unchanged; a `char[128]` array works for ASCII only.

<AiCompanion problem-slug="sliding-window-longest-substring" pattern-hint="sliding window" />

## Related problems (same ladder applies)

- [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) — same window skeleton, `need`/`have` counter for the validity check
- [Longest Substring with At Most K Distinct](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) — validity: `distinct ≤ k`
- [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) — window is valid if `(windowLen − maxFreq) ≤ k`
- [Permutation in String](https://leetcode.com/problems/permutation-in-string/) — fixed-size window, count-match

<FeedbackWidget problem-slug="sliding-window-longest-substring" />

<RelatedProblems problems="fruit-into-baskets::Fruit Into Baskets|count-number-of-nice-subarrays::Count Number Of Nice Subarrays|shortest-subarray-with-sum-at-least-k::Shortest Subarray With Sum At Least K" />
