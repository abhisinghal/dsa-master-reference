# Sliding Window — Longest Repeating Character Replacement

*[↗ LeetCode: Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

<CompanyTags companies="Meta, Google, Microsoft, Amazon" />

Given `s` (uppercase A–Z) and integer `k`, return the length of the longest substring you can make of a single repeated character by replacing at most `k` other characters.

**Example 1** — `s = "ABAB", k = 2` → `4` (replace both `A`s or both `B`s)
**Example 2** — `s = "AABABBA", k = 1` → `4` (window `AABA` → replace one `A` with `B`, or the reverse)
**Example 3** — `s = "AAAA", k = 0` → `4` (already all same)

**Constraints** — `1 ≤ n ≤ 10⁵`, `0 ≤ k ≤ n`.


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

<MarkSolved problem-slug="longest-repeating-character-replacement" />


## Approach 1 — Try every substring

**Intuition.** For each `s[i..j]`, count the most frequent letter `maxFreq`; the window is valid iff `(j - i + 1) - maxFreq ≤ k`. Track the longest.

```java
int characterReplacementBrute(String s, int k) {
    int n = s.length(), best = 0;
    for (int i = 0; i < n; i++)
        for (int j = i; j < n; j++) {
            int[] cnt = new int[26], maxFreq = {0};
            for (int p = i; p <= j; p++) {
                cnt[s.charAt(p) - 'A']++;
                maxFreq[0] = Math.max(maxFreq[0], cnt[s.charAt(p) - 'A']);
            }
            if (j - i + 1 - maxFreq[0] <= k) best = Math.max(best, j - i + 1);
        }
    return best;
}
```

<CodeTrace
  title="Brute — s='AABABBA', k=1 checking windows"
  :values="['A','A','B','A','B','B','A']"
  :windowKeys="['i','j']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0, j: 2 }, vars: { window: "AAB", maxFreq: 2, needFlips: 1, best: 3 }, note: "1 flip fits budget" },
    { pointers: { i: 0, j: 3 }, vars: { window: "AABA", maxFreq: 3, needFlips: 1, best: 4 }, note: "flip B — length 4" },
    { pointers: { i: 0, j: 4 }, vars: { window: "AABAB", maxFreq: 3, needFlips: 2 }, note: "would need 2 flips > k — invalid" },
    { pointers: { i: 3, j: 6 }, vars: { window: "ABBA", maxFreq: 2, needFlips: 2 }, note: "invalid — same story" }
  ]'
/>

**Complexity** — Time **O(n³)**; Space **O(1)**.

---

## Approach 2 — Sliding window with "lazy" maxFreq

**Insight from brute.** The window validity check `windowLen - maxFreq ≤ k` is monotone in one direction: growing `right` can only require **larger** `maxFreq` (or the same) to keep the window feasible. Grow right; if the window becomes invalid, shrink left by exactly one.

**Trap** — we don't need to recompute `maxFreq` when shrinking. Any window with size ≤ current best can't improve the answer regardless of stale `maxFreq`. So we lazily keep the max ever seen.

```java
int characterReplacement(String s, int k) {
    int[] cnt = new int[26];
    int left = 0, maxCount = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        cnt[s.charAt(right) - 'A']++;
        maxCount = Math.max(maxCount, cnt[s.charAt(right) - 'A']);
        if (right - left + 1 - maxCount > k)
            cnt[s.charAt(left++) - 'A']--;
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

<CodeTrace
  title="Sliding — s='AABABBA', k=1"
  :values="['A','A','B','A','B','B','A']"
  :windowKeys="['left','right']"
  :cellWidth="34"
  :steps='[
    { pointers: { left: 0, right: 0 }, vars: { cnt: "{A:1}", maxCount: 1, best: 1 }, note: "start" },
    { pointers: { left: 0, right: 3 }, vars: { cnt: "{A:3, B:1}", maxCount: 3, flips: 1, best: 4 }, note: "AABA — one flip fits — length 4" },
    { pointers: { left: 1, right: 4 }, vars: { cnt: "{A:2, B:2}", maxCount: 3, best: 4 }, note: "flips=2 > k → shrink left; maxCount stays lazily at 3" },
    { pointers: { left: 3, right: 6 }, vars: { cnt: "{A:2, B:2}", maxCount: 3, best: 4 }, note: "still shrinking as needed; best remains 4" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)** (26 buckets).

**Why "lazy max" is safe.** The answer we output is never smaller than `best`. If `maxCount` is stale (real max is lower), the window only grows if a **new** character bumps `maxCount` higher — which is real, not stale. Correctness preserved.

---

## Try it yourself

<JavaRunner problem-slug="longest-repeating-character-replacement" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Try every substring | O(n³) | O(1) | baseline; TLE at n=10⁵ |
| Sliding window + lazy maxFreq | **O(n)** | O(1) | expected optimum |

## When to use which

- **First pass** — state brute, then jump to sliding window.
- **"At most k operations"** signal → try replacing `maxFreq` with the constrained quantity in the validity formula.
- **"What if alphabet is Unicode?"** → replace `int[26]` with `HashMap<Character,Integer>`; recomputing max on every shrink is O(σ) — slower but still correct.
- **Follow-up: return the actual substring** → track `(bestL, bestLen)` and slice.

<AiCompanion problem-slug="longest-repeating-character-replacement" pattern-hint="sliding window" />

## Related problems

- [Longest Substring with At Most K Distinct Characters](/problems/longest-substring-with-at-most-k-distinct-characters) — sibling `≤ k distinct` variant
- [Max Consecutive Ones III](/problems/max-consecutive-ones-iii) — binary version
- [Replace the Substring for Balanced String](/problems/replace-the-substring-for-balanced-string) — window on outside counts
- [Longest Substring Without Repeating Characters](/problems/sliding-window-longest-substring) — the seed

<FeedbackWidget problem-slug="longest-repeating-character-replacement" />
