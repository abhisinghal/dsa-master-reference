# Hashing — Candy

*[↗ LeetCode: Candy](https://leetcode.com/problems/candy/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/greedy)

&lt;CompanyTags companies="Amazon, Meta, Bloomberg" /&gt;

Every child gets ≥1 candy; higher-rated than a neighbor must receive strictly more. Minimize total.

**Example 1** — `ratings=[1,0,2]` → `5`
**Example 2** — `ratings=[1,2,2]` → `4`

**Constraints** — `1 ≤ n ≤ 2·10⁴`.


&lt;Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/&gt;
---

&lt;MarkSolved problem-slug="candy" /&gt;

&lt;InterviewTimer problem-slug="candy" /&gt;



## Approach — Two-pass sweep (canonical)

**Insight.** Left→right: enforce "left neighbor". Right→left: enforce "right neighbor". Take max at each position.



```java
int candy(int[] ratings) {
    int n = ratings.length;
    int[] c = new int[n];
    Arrays.fill(c, 1);
    for (int i = 1; i < n; i++) if (ratings[i] > ratings[i-1]) c[i] = c[i-1] + 1;
    for (int i = n - 2; i >= 0; i--) if (ratings[i] > ratings[i+1]) c[i] = Math.max(c[i], c[i+1] + 1);
    int sum = 0; for (int x : c) sum += x;
    return sum;
}
```



<CodeTrace
  title="Two-pass sweep (canonical)"
  :values="['1', '0', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)**.

## Approach 2 — One-pass slope counting

Track up-slope and down-slope lengths + current peak. Trickier but O(1) extra space.

---

## Try it yourself

<JavaRunner problem-slug="candy" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Two-sweep | **O(n)** | O(n) | canonical |
| One-pass slope | O(n) | O(1) | polish |

## When to use which

- **Standard** → two-sweep.
- **O(1) space required** → one-pass slope.
- **Non-strict inequality** → different logic.

&lt;AiCompanion problem-slug="candy" pattern-hint="hashing" /&gt;

## Related problems

- [Trapping Rain Water](/problems/trapping-rain-water)
- [Gas Station](/problems/gas-station)

&lt;FeedbackWidget problem-slug="candy" /&gt;
