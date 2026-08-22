# Hashing — Candy

*[↗ LeetCode: Candy](https://leetcode.com/problems/candy/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/greedy)

Every child gets ≥1 candy; higher-rated than a neighbor must receive strictly more. Minimize total.

---

## Approach 1 — Two-pass sweep
**Insight.** Left-to-right: enforce "left neighbor". Right-to-left: enforce "right neighbor". Take the max at each position.

```java
int candy(int[] ratings) {
    int n = ratings.length;
    int[] c = new int[n];
    Arrays.fill(c, 1);
    for (int i = 1; i < n; i++) if (ratings[i] > ratings[i - 1]) c[i] = c[i - 1] + 1;
    for (int i = n - 2; i >= 0; i--) if (ratings[i] > ratings[i + 1]) c[i] = Math.max(c[i], c[i + 1] + 1);
    int sum = 0;
    for (int x : c) sum += x;
    return sum;
}
```

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Approach 2 — One-pass slope counting
Track up-slope length, down-slope length, and current peak length. Trickier to get right; useful when interviewer asks for O(1) space.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Two-pass sweep | O(n) | O(n) | baseline |
| One-pass slope counting | O(1) | — | optimum |

## When to use which

- **State it for signal** → Two-pass sweep (O(n)). Correct baseline; call it out then move on.
- **Ship this** → One-pass slope counting (O(1), —). Expected optimum in interview.

## Related problems

- [Trapping Rain Water](/problems/trapping-rain-water) — same "max of two sweeps" idea
- [Gas Station](/problems/gas-station)
