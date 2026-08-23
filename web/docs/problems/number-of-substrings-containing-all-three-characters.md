# Sliding Window — Number of Substrings Containing All Three Characters

*[↗ LeetCode: Number of Substrings Containing All Three Characters](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Given a string `s` over `{a, b, c}`, return the number of substrings containing at least one `a`, one `b`, and one `c`.

**Example 1** — `s = "abcabc"` → `10`
**Example 2** — `s = "aaacb"` → `3`
**Example 3** — `s = "abc"` → `1`

**Constraints** — `3 ≤ n ≤ 5 · 10⁴`. `s[i] ∈ {a, b, c}`.

---

## Approach 1 — Every substring

**Intuition.** For each `[i, j]`, count occurrences of `a`, `b`, `c`; increment if all ≥ 1.



```java
int numberOfSubstringsBrute(String s) {
    int n = s.length(), count = 0;
    for (int i = 0; i < n; i++) {
        int[] c = new int[3];
        for (int j = i; j < n; j++) {
            c[s.charAt(j) - 'a']++;
            if (c[0] > 0 && c[1] > 0 && c[2] > 0) count++;
        }
    }
    return count;
}
```



**Complexity** — Time **O(n²)**; Space **O(1)**.

---

## Approach 2 — Sliding window: for each `right`, count valid `left`s

**Insight from brute.** For each `right`, find the smallest `left` such that `[left, right]` contains all three. Then any `left' ∈ [0, left]` gives a valid substring ending at `right` — so we add `(left + 1)` substrings, no wait we add `left` when using "smallest left such that INVALID" phrasing.

Cleaner phrasing: extend `right`; if window has all three, keep shrinking `left` while still all-three. When the window becomes invalid (some count hits 0), record: number of valid starts for this `right` is `left` (indices 0..left-1 all valid).



```java
int numberOfSubstrings(String s) {
    int[] cnt = new int[3];
    int left = 0, res = 0;
    for (int right = 0; right < s.length(); right++) {
        cnt[s.charAt(right) - 'a']++;
        while (cnt[0] > 0 && cnt[1] > 0 && cnt[2] > 0) {
            cnt[s.charAt(left) - 'a']--;
            left++;
        }
        res += left; // valid starts are 0..left-1
    }
    return res;
}
```



<CodeTrace
  title="Sliding — s='abcabc'"
  :values="['a','b','c','a','b','c']"
  :windowKeys="['left','right']"
  :cellWidth="36"
  :steps='[
    { pointers: { left: 0, right: 2 }, vars: { cnt: "{a:1,b:1,c:1}", res: 1 }, note: "all 3 present → shrink; left moves to 1; add left=1" },
    { pointers: { left: 1, right: 3 }, vars: { cnt: "{a:1,b:1,c:1}", res: 3 }, note: "add left=2 after shrink" },
    { pointers: { left: 2, right: 4 }, vars: { cnt: "{a:1,b:1,c:1}", res: 6 }, note: "add left=3" },
    { pointers: { left: 3, right: 5 }, vars: { cnt: "{a:1,b:1,c:1}", res: 10 }, note: "add left=4 — total 10" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Approach 3 — Track last-seen positions of each char (O(1) map)

**Insight from sliding.** For each `right`, the smallest `left` giving all-three is `min(lastA, lastB, lastC) + 1`. So valid starts = `min(lastA, lastB, lastC) + 1` if all three have been seen.



```java
int numberOfSubstringsLast(String s) {
    int[] last = {-1, -1, -1};
    int res = 0;
    for (int i = 0; i < s.length(); i++) {
        last[s.charAt(i) - 'a'] = i;
        res += Math.min(last[0], Math.min(last[1], last[2])) + 1;
    }
    return res;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**. One-pass, no inner while — slightly cleaner.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Every substring | O(n²) | O(1) | baseline |
| Sliding window | **O(n)** | O(1) | expected optimum |
| Last-seen tracking | **O(n)** | O(1) | polish — cleanest single pass |

## When to use which

- **First pass** — sliding window is the pattern-recognition answer.
- **Interviewer asks "simpler code?"** → last-seen version.
- **Generalize to k distinct required chars** → last-seen extends to `min(lastX) + 1`.
- **"Contains at least K of each char"** → this becomes a `need[]/have[]` problem — see [Minimum Window Substring](/problems/minimum-window-substring).

## Related problems

- [Minimum Window Substring](/problems/minimum-window-substring) — need/have generalization
- [Longest Substring with At Most K Distinct Characters](/problems/longest-substring-with-at-most-k-distinct-characters)
- [Subarrays with K Different Integers](/problems/subarrays-with-k-different-integers)
