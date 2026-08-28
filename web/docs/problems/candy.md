# Hashing — Candy

*[↗ LeetCode: Candy](https://leetcode.com/problems/candy/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/greedy)

<CompanyTags companies="Amazon, Meta, Bloomberg" />

Every child gets ≥1 candy; higher-rated than a neighbor must receive strictly more. Minimize total.

**Example 1** — `ratings=[1,0,2]` → `5` (candies = 2,1,2)
**Example 2** — `ratings=[1,2,2]` → `4` (candies = 1,2,1)
**Example 3** — `ratings=[1,3,4,5,2]` → `11` (candies = 1,2,3,4,1)

**Constraints** — `1 ≤ n ≤ 2·10⁴`. Brute enumeration is 2·10⁴ ! — impossible. Two-pass is O(n) = 2·10⁴ ops (~50 µs). Brute repeatedly scans until no changes — O(n²) worst case = 4·10⁸ ops at n=2·10⁴. Two-pass left-then-right sweep is O(n) = 2·10⁴ ops on the hot path.
<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its 'canonical form' — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For 'first duplicate', a `HashSet` and single-pass `add()` is enough."
/>
---

<MarkSolved problem-slug="candy" /> <Bookmark problem-slug="candy" />

<InterviewTimer problem-slug="candy" />



## Approach 1 — Repeated pass until stable

**Intuition.** Give everyone 1 candy. Sweep left-to-right and right-to-left repeatedly, fixing any violation. Stop when no changes.



```java
int candyBrute(int[] r) {
    int n = r.length;
    int[] c = new int[n];
    Arrays.fill(c, 1);
    boolean changed = true;
    while (changed) {
        changed = false;
        for (int i = 1; i < n; i++)
            if (r[i] > r[i-1] && c[i] <= c[i-1]) { c[i] = c[i-1] + 1; changed = true; }
        for (int i = n - 2; i >= 0; i--)
            if (r[i] > r[i+1] && c[i] <= c[i+1]) { c[i] = c[i+1] + 1; changed = true; }
    }
    int s = 0; for (int x : c) s += x; return s;
}
```



**Complexity** — Time worst-case **O(n²)** if the ratings are strictly increasing then decreasing; Space **O(n)**. *In an interview* state this, then observe that two passes are always enough.

---

## Approach 2 — Two-pass sweep (canonical)

**Insight.** Left→right pass enforces every strictly-greater left constraint. Right→left pass enforces every strictly-greater right constraint. Take max at each position — a single 2-pass suffices because the two constraints are independent.



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

**Complexity** — Time **O(n)**; Space **O(n)**. *Say aloud in an interview:* "two-sweep = classic pattern for one-sided constraints on both sides. Same shape in Product of Array Except Self."

## Approach 3 — One-pass slope counting

Track up-slope and down-slope lengths + current peak. Trickier but O(1) extra space.

---

## Try it yourself

<JavaRunner problem-slug="candy" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Repeat-until-stable | O(n²) worst | O(n) | Reference; can TLE |
| **Two-sweep** | **O(n)** | O(n) | **Canonical** |
| One-pass slope | O(n) | O(1) | Polish |

## When to use which

- **Standard** → two-sweep.
- **O(1) space required** → one-pass slope.
- **Non-strict inequality** → different logic.

<AiCompanion problem-slug="candy" pattern-hint="hashing" />

## Related problems

- [Trapping Rain Water](/problems/trapping-rain-water)
- [Gas Station](/problems/gas-station)

<FeedbackWidget problem-slug="candy" />
