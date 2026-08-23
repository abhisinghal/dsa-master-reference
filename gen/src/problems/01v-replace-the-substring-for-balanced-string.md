# Sliding Window — Replace the Substring for Balanced String

*[↗ LeetCode: Replace the Substring for Balanced String](https://leetcode.com/problems/replace-the-substring-for-balanced-string/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

String of Q,W,E,R (length n divisible by 4). Return length of smallest substring to replace so each letter appears n/4 times.

**Example 1** — `s="QWER"` → `0`
**Example 2** — `s="QQWE"` → `1`
**Example 3** — `s="QQQW"` → `2`

**Constraints** — `1 ≤ n ≤ 10⁵`.


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

## Approach — Sliding window over "outside" counts (canonical)

**Insight.** Substring `[l, r]` is a valid replacement window iff **outside** it, no letter exceeds `n/4`. Shrink l while condition holds; track min length.

```java
int balancedString(String s) {
    int n = s.length(), k = n / 4;
    int[] cnt = new int[128];
    for (char c : s.toCharArray()) cnt[c]++;
    int l = 0, best = n;
    for (int r = 0; r < n; r++) {
        cnt[s.charAt(r)]--;
        while (l < n && cnt['Q'] <= k && cnt['W'] <= k && cnt['E'] <= k && cnt['R'] <= k) {
            best = Math.min(best, r - l + 1);
            cnt[s.charAt(l++)]++;
        }
    }
    return best;
}
```

<CodeTrace
  title="Sliding — s='QQWE', k=1"
  :values="['Q','Q','W','E']"
  :windowKeys="['l','r']"
  :cellWidth="34"
  :steps='[
    { pointers: { l: 0, r: 0 }, vars: { outside: "{Q:1,W:1,E:1,R:0}" }, note: "outside has Q=1 ≤ k, but missing R... wait Q count is 1 outside includes 1 Q at idx 1" },
    { pointers: { l: 0, r: 1 }, vars: { best: 2 }, note: "" },
    { pointers: { l: 1, r: 1 }, vars: { best: 1 }, note: "smaller window found" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="replace-the-substring-for-balanced-string" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Outside-count sliding | **O(n)** | O(1) | canonical |

## When to use which

- **Balance target on fixed alphabet** → outside counts.
- **Any character allowed as replacement** → this template.
- **Fixed replacement char** → different constraint.

<AiCompanion problem-slug="replace-the-substring-for-balanced-string" pattern-hint="sliding window" />

## Related problems

- [Longest Repeating Character Replacement](/problems/longest-repeating-character-replacement)
- [Minimum Window Substring](/problems/minimum-window-substring)
- [Longest Substring with At Most K Distinct Characters](/problems/longest-substring-with-at-most-k-distinct-characters)

<FeedbackWidget problem-slug="replace-the-substring-for-balanced-string" />
