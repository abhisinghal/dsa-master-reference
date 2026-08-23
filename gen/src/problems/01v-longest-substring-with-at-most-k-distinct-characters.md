# Sliding Window — Longest Substring with At Most K Distinct Characters

*[↗ LeetCode: Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

<CompanyTags companies="Meta, Google, Amazon, LinkedIn" />

Given a string `s` and integer `k`, return the length of the longest substring containing at most `k` distinct characters.

**Example 1** — `s = "eceba", k = 2` → `3` (window `"ece"`)
**Example 2** — `s = "aa", k = 1` → `2`
**Example 3** — `s = "a", k = 0` → `0`

**Constraints** — `1 ≤ n ≤ 5 · 10⁴`; `0 ≤ k ≤ 50`.


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

<MarkSolved problem-slug="longest-substring-with-at-most-k-distinct-characters" />

<InterviewTimer problem-slug="longest-substring-with-at-most-k-distinct-characters" />



## Approach 1 — Try every substring

**Intuition.** For each `s[i..j]`, count distinct characters; track the longest window with ≤ `k` distinct.

```java
int lengthOfLongestSubstringKDistinctBrute(String s, int k) {
    int n = s.length(), best = 0;
    for (int i = 0; i < n; i++) {
        Set<Character> distinct = new HashSet<>();
        for (int j = i; j < n; j++) {
            distinct.add(s.charAt(j));
            if (distinct.size() <= k) best = Math.max(best, j - i + 1);
            else break;
        }
    }
    return best;
}
```

**Complexity** — Time **O(n²)**; Space **O(σ)**.

---

## Approach 2 — Sliding window with distinct counter

**Insight from brute.** Growing `right` never decreases `distinct`. Once `distinct > k`, we shrink `left` — decrementing each char's count; if a count hits 0, `distinct` drops.

```java
int lengthOfLongestSubstringKDistinct(String s, int k) {
    if (k == 0) return 0;
    int[] cnt = new int[128];
    int left = 0, distinct = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        if (cnt[s.charAt(right)]++ == 0) distinct++;
        while (distinct > k)
            if (--cnt[s.charAt(left++)] == 0) distinct--;
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

<CodeTrace
  title="Sliding — s='eceba', k=2"
  :values="['e','c','e','b','a']"
  :windowKeys="['left','right']"
  :cellWidth="36"
  :steps='[
    { pointers: { left: 0, right: 0 }, vars: { cnt: "{e:1}", distinct: 1, best: 1 }, note: "e" },
    { pointers: { left: 0, right: 2 }, vars: { cnt: "{e:2,c:1}", distinct: 2, best: 3 }, note: "ece — 2 distinct — best 3" },
    { pointers: { left: 0, right: 3 }, vars: { cnt: "{e:2,c:1,b:1}", distinct: 3 }, note: "b enters — 3 distinct > k → shrink" },
    { pointers: { left: 2, right: 3 }, vars: { cnt: "{e:1,b:1}", distinct: 2, best: 3 }, note: "left past c; distinct=2 again" },
    { pointers: { left: 3, right: 4 }, vars: { cnt: "{b:1,a:1}", distinct: 2, best: 3 }, note: "final window ba; best stays 3" }
  ]'
/>

**Complexity** — Time **O(n)** — each char enters and leaves once; Space **O(σ)** (≤ 128).

---

## Approach 3 — Ordered map for `k` large (interview polish)

**Insight from sliding.** If `k` is very large (10⁴+), tracking `distinct` explicitly is still O(n), but managing a `LinkedHashMap` of last-seen indices can express the same logic in a tighter algorithm — remove the least-recently-used char and advance `left` past it in O(1).

```java
int lengthOfLongestSubstringKDistinctLRU(String s, int k) {
    LinkedHashMap<Character, Integer> lastIdx = new LinkedHashMap<>(k, 0.75f, false);
    int left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        lastIdx.remove(c);
        lastIdx.put(c, right);
        if (lastIdx.size() > k) {
            Map.Entry<Character, Integer> oldest = lastIdx.entrySet().iterator().next();
            left = oldest.getValue() + 1;
            lastIdx.remove(oldest.getKey());
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

**Complexity** — Time **O(n)**; Space **O(k)**.

---

## Try it yourself

<JavaRunner problem-slug="longest-substring-with-at-most-k-distinct-characters" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Every substring | O(n²) | O(σ) | baseline |
| Sliding window | **O(n)** | O(σ) | expected optimum |
| LRU-style ordered map | O(n) | O(k) | polish |

## When to use which

- **k = 2** → this is exactly [Fruit Into Baskets](/problems/fruit-into-baskets).
- **k = ∞** → this is [Longest Substring Without Repeating Characters](/problems/sliding-window-longest-substring) (k is unconstrained).
- **k = size(alphabet)** → answer is trivially `n`.
- **Return the substring** → track `(bestL, bestLen)` and slice.

<AiCompanion problem-slug="longest-substring-with-at-most-k-distinct-characters" pattern-hint="sliding window" />

## Related problems

- [Longest Substring Without Repeating Characters](/problems/sliding-window-longest-substring) — k = ∞
- [Fruit Into Baskets](/problems/fruit-into-baskets) — k = 2
- [Subarrays with K Different Integers](/problems/subarrays-with-k-different-integers) — count, not length
- [Longest Substring with At Most Two Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters/)

<FeedbackWidget problem-slug="longest-substring-with-at-most-k-distinct-characters" />

<RelatedProblems problems="number-of-substrings-containing-all-three-characters::Number Of Substrings Containing All Three Characters|minimum-window-substring::Minimum Window Substring|shortest-subarray-with-sum-at-least-k::Shortest Subarray With Sum At Least K" />
