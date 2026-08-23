# Sliding Window — Get Equal Substrings Within Budget

*[↗ LeetCode: Get Equal Substrings Within Budget](https://leetcode.com/problems/get-equal-substrings-within-budget/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Given `s`, `t`, `maxCost`. Convert `s[i]` → `t[i]` costs `|s[i] - t[i]|`. Return longest substring convertible within budget.

**Example 1** — `s="abcd", t="bcdf", maxCost=3` → `3`
**Example 2** — `s="abcd", t="cdef", maxCost=3` → `1`
**Example 3** — `s="abcd", t="acde", maxCost=0` → `1`

**Constraints** — `1 ≤ n ≤ 10⁵`; `0 ≤ maxCost ≤ 10⁶`.


&lt;Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/&gt;
---

## Approach — Sliding window on the diff array (canonical)

**Insight.** Compute `diff[i] = |s[i] - t[i]|`. Now: longest subarray with sum ≤ maxCost.



```java
int equalSubstring(String s, String t, int maxCost) {
    int l = 0, cost = 0, best = 0;
    for (int r = 0; r < s.length(); r++) {
        cost += Math.abs(s.charAt(r) - t.charAt(r));
        while (cost > maxCost) cost -= Math.abs(s.charAt(l) - t.charAt(l++));
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```



<CodeTrace
  title="Budget window — s='abcd', t='bcdf', maxCost=3"
  :values="['1','1','1','2']"
  :windowKeys="['l','r']"
  :cellWidth="34"
  :steps='[
    { pointers: { l: 0, r: 2 }, vars: { cost: 3, best: 3 }, note: "1+1+1=3 ≤ 3 → best=3" },
    { pointers: { l: 3, r: 3 }, vars: { cost: 2, best: 3 }, note: "shrink after 4th elem" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="get-equal-substrings-within-budget" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sliding budget | **O(n)** | O(1) | canonical |

## When to use which

- **"Convert within budget"** → diff array + sliding window.
- **Multi-alphabet Unicode** → codePoints instead of chars.
- **"Return the substring"** → track `(bestL, bestLen)` and slice.

&lt;AiCompanion problem-slug="get-equal-substrings-within-budget" pattern-hint="sliding window" /&gt;

## Related problems

- [Longest Substring with At Most K Distinct Characters](/problems/longest-substring-with-at-most-k-distinct-characters)
- [Max Consecutive Ones III](/problems/max-consecutive-ones-iii)
- [Minimum Size Subarray Sum](/problems/minimum-size-subarray-sum)

&lt;FeedbackWidget problem-slug="get-equal-substrings-within-budget" /&gt;
