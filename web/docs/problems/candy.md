# Hashing — Candy

*[↗ LeetCode: Candy](https://leetcode.com/problems/candy/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/greedy)

Every child gets ≥1 candy; higher-rated than a neighbor must receive strictly more. Minimize total.

**Example 1** — `ratings=[1,0,2]` → `5`
**Example 2** — `ratings=[1,2,2]` → `4`

**Constraints** — `1 ≤ n ≤ 2·10⁴`.

---

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



**Complexity** — Time **O(n)**; Space **O(n)**.

## Approach 2 — One-pass slope counting

Track up-slope and down-slope lengths + current peak. Trickier but O(1) extra space.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Two-sweep | **O(n)** | O(n) | canonical |
| One-pass slope | O(n) | O(1) | polish |

## When to use which

- **Standard** → two-sweep.
- **O(1) space required** → one-pass slope.
- **Non-strict inequality** → different logic.

## Related problems

- [Trapping Rain Water](/problems/trapping-rain-water)
- [Gas Station](/problems/gas-station)
